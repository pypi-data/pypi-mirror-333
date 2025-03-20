import argparse
import logging
import re
import shutil
import subprocess
import sys
import json
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional

from upgrade.scripts.requirements import parse_requirements_txt, to_requirements_obj
from upgrade.scripts.utils import (
    is_development_cloudsmith,
    run,
    pip,
    create_directory,
    get_venv_executable,
    on_rm_error,
)
from upgrade.scripts.validations import is_cloudsmith_url_valid
from upgrade.scripts.exceptions import UpgradeError


class VenvUpgradeStatus(Enum):
    UPGRADED = "UPGRADED"
    ERROR = "ERROR"


SYSTEM_DEPENDENCIES = ["pip", "setuptools"]
upgrade_success_re = re.compile(r'{"success": (true|false)')
response_output_re = re.compile(r'"responseOutput": "(.*?)"')


def ensure_pip(venv_executable, *args, **kwargs):
    try:
        return run(*((venv_executable, "-m", "ensurepip") + args), **kwargs)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while running pip in venv {str(e)}")
        raise e


def venv(*args, **kwargs):
    try:
        return run(*((sys.executable, "-m", "venv", "--without-pip") + args), **kwargs)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while creating venv {str(e)}")
        raise e


def install_system_dependencies(venv_executable: str) -> None:
    for dependency in SYSTEM_DEPENDENCIES:
        try:
            pip(
                "install",
                "--upgrade",
                f"{dependency}",
                py_executable=venv_executable,
            )
        except subprocess.CalledProcessError as e:
            logging.error(
                f"Error occurred while upgrading running pip upgrade {dependency} {str(e)}"
            )
            raise e


def install_upgrade_python_package(
    venv_executable: str,
    upgrade_python_package_version: Optional[str] = None,
    local_installation_path: Optional[str] = None,
) -> None:
    upgrade_python_package = "upgrade-python-package"
    if upgrade_python_package_version:
        upgrade_python_package += f"=={upgrade_python_package_version}"
    try:
        if local_installation_path:
            # for local testing of unreleased upgrade-python-package
            pip(
                "install",
                "-e",
                str(Path(local_installation_path)),
                py_executable=venv_executable,
            )
        else:
            pip(
                "install",
                "--upgrade",
                upgrade_python_package,
                py_executable=venv_executable,
            )
    except subprocess.CalledProcessError as e:
        logging.error(
            f"Error occurred while installing upgrade-python-package {str(e)}"
        )
        raise e


def upgrade_venv(
    venv_executable: str,
    requirements_obj: Any,
    cloudsmith_url: Optional[str],
    wheels_path: Optional[str],
    update_from_local_wheels: Optional[bool],
    additional_dependencies: Optional[List[str]],
    log_location: Optional[str] = None,
) -> str:
    try:
        result = ""
        for dependency in [requirements_obj.name] + additional_dependencies:
            upgrade_args = [
                venv_executable,
                "-m",
                "upgrade.scripts.upgrade_python_package",
                dependency,
            ]
            if is_development_cloudsmith(cloudsmith_url):
                upgrade_args.append("'--pre'")
            else:
                specifier = str(requirements_obj.specifier)
                if len(specifier) > 0:
                    upgrade_args.append(f"--version={specifier}")

            if cloudsmith_url:
                upgrade_args.append(f"--cloudsmith-url={cloudsmith_url}")

            if log_location:
                upgrade_args.append(f"--log-location={log_location}")

            upgrade_args.extend(
                [
                    "--skip-post-install",
                    "--format-output",
                    "--update-all",
                ]
            )
            if wheels_path:
                upgrade_args.append(f"--wheels-path={wheels_path}")
            if update_from_local_wheels:
                upgrade_args.append("--update-from-local-wheels")

            result += run(*(upgrade_args), check=False)

        return result
    except Exception as e:
        logging.error(
            f"Error occurred while upgrading {requirements_obj.name}{requirements_obj.specifier} {str(e)}"
        )
        raise e


def _check_venv_consistent(
    requirements_obj: Any, venv_executable: str, venv_response: Optional[str] = None
) -> None:
    try:
        pip("check", py_executable=venv_executable)
    except:
        msg = f"Error occurred while checking venv at path: {venv_executable}"
        if venv_response is not None:
            msg += response_output_re.search(venv_response).group(1)
        logging.error(msg)
        raise UpgradeError(msg)

    logging.debug(f"{str(requirements_obj)} venv is consistent.")


def _switch_venvs(venv_path: str) -> None:
    """
    Switch the virtualenv environments after a successful upgrade,
    since we first upgrade packages in a temporary `<venv_name>_green` venv.
    """
    backup_venv_path = Path(str(venv_path) + "_green")
    temp_venv_path = Path(str(venv_path) + "_temp")
    shutil.move(venv_path, temp_venv_path)
    shutil.move(backup_venv_path, venv_path)
    shutil.rmtree(temp_venv_path, onerror=on_rm_error)


def _get_venv_path(envs_home: str, requirements: str) -> Path:
    """Get the path to the virtualenv directory.
    Example:
    If requirements.txt contains:
        ```
        dependency==2.0.0 # oll.dependency.module.*
        ```
    Then the name of expected virtualenv directory is `<VENV_PATH> / dependency==2.0.0`
    """
    return Path(envs_home) / requirements


def create_venv(
    envs_home: str,
    requirements: str,
    upgrade_python_package_version: Optional[str],
    local_installation_path: Optional[str] = None,
) -> str:
    """Create a virtualenv and install upgrade-python-package in it."""
    env_path = _get_venv_path(envs_home, requirements)
    create_directory(env_path)
    venv(*[str(env_path)])
    py_executable = get_venv_executable(str(env_path))
    ensure_pip(py_executable)
    install_system_dependencies(py_executable)
    install_upgrade_python_package(
        py_executable, upgrade_python_package_version, local_installation_path
    )

    return py_executable


@contextmanager
def temporary_upgrade_venv(venv_path: str, blue_green_deployment: bool) -> str:
    """Create a temporary virtualenv and return the path to the python executable.
    The temporary virtualenv is created in the same directory as the original virtualenv.

    The purpose of temporary virtualenv is to fully upgrade packages. Once the upgrade is successful,
    the original virtualenv is replaced with the temporary (now fully upgraded) virtualenv.
    If the upgrade fails, the original virtualenv is not replaced with the temporary virtualenv.

    If blue_green_deployment is True, the original virtualenv is not replaced with the temporary virtualenv.
    In such a case, the temporary virtualenv is expected to be manually handled by the caller.
    """
    try:
        backup_venv_path = Path(str(venv_path) + "_green")
        if backup_venv_path.exists():
            shutil.rmtree(backup_venv_path, onerror=on_rm_error)

        shutil.copytree(venv_path, str(backup_venv_path))
        yield get_venv_executable(backup_venv_path)
    except Exception as e:
        logging.error(f"Error occurred while creating temporary venv: {str(e)}")
        raise UpgradeError(e)
    finally:
        if backup_venv_path.exists() and not blue_green_deployment:
            shutil.rmtree(backup_venv_path, onerror=on_rm_error)


def build_and_upgrade_venv(
    requirements: str,
    envs_home: str,
    auto_upgrade: bool,
    cloudsmith_url: Optional[str] = None,
    wheels_path: Optional[str] = None,
    update_from_local_wheels: Optional[bool] = None,
    additional_dependencies: Optional[List[str]] = None,
    blue_green_deployment: Optional[bool] = False,
    upgrade_python_package_version: Optional[str] = None,
    log_location: Optional[str] = None,
    local_installation_path: Optional[str] = None,
) -> str:
    """Build and upgrade a virtualenv."""
    venv_path = str(_get_venv_path(envs_home, requirements))
    error_message = None
    requirements_obj = to_requirements_obj(requirements)
    if not Path(venv_path).exists():
        auto_upgrade = True
        msg = "Requirements changed. Creating new virtualenv."
        print(msg)
        logging.info(msg)
        py_executable = create_venv(
            envs_home,
            requirements,
            upgrade_python_package_version,
            local_installation_path,
        )
    else:
        py_executable = get_venv_executable(venv_path)
        if not auto_upgrade:
            msg = "Requirements did not change. Returning venv executable."
            print(msg)
            logging.info(msg)
            return py_executable
        _check_venv_consistent(requirements_obj, py_executable)

    if auto_upgrade:
        with temporary_upgrade_venv(
            venv_path, blue_green_deployment
        ) as temp_venv_executable:
            try:
                response = upgrade_venv(
                    temp_venv_executable,
                    requirements_obj,
                    cloudsmith_url,
                    wheels_path,
                    update_from_local_wheels,
                    additional_dependencies or [],
                    log_location,
                )
                logging.info(response)
            except Exception as e:
                logging.error(
                    f"Unexpected error occurred while upgrading {requirements_obj.name}{requirements_obj.specifier} {str(e)}"
                )
                raise UpgradeError(e)

            _check_venv_consistent(requirements_obj, temp_venv_executable, response)
            if not blue_green_deployment:
                _switch_venvs(venv_path)

    return py_executable, error_message


def manage_venv(
    envs_home: str,
    requirements: Optional[str] = None,
    requirements_file: Optional[str] = None,
    auto_upgrade: bool = False,
    cloudsmith_url: Optional[str] = None,
    log_location: Optional[str] = None,
    test: Optional[bool] = False,
    update_from_local_wheels: Optional[bool] = False,
    wheels_path: Optional[str] = None,
    additional_dependencies: Optional[List[str]] = None,
    blue_green_deployment: Optional[bool] = False,
    upgrade_python_package_version: Optional[str] = None,
    local_installation_path: Optional[str] = None,
):
    response_status = {}
    try:
        if requirements is None and requirements_file is None:
            raise Exception("Either requirements or requirements_file is required.")

        if test:
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
        else:
            log_location = log_location or "/var/log/manage_venv.log"
            logging.basicConfig(
                filename=log_location,
                level=logging.WARNING,
                format="%(asctime)s %(message)s",
            )
        if cloudsmith_url:
            is_cloudsmith_url_valid(cloudsmith_url)

        requirements = requirements or parse_requirements_txt(requirements_file)

        build_and_upgrade_venv(
            requirements,
            envs_home,
            auto_upgrade,
            cloudsmith_url,
            wheels_path,
            update_from_local_wheels,
            additional_dependencies,
            blue_green_deployment,
            upgrade_python_package_version,
            log_location,
            local_installation_path,
        )
        response_status["responseStatus"] = VenvUpgradeStatus.UPGRADED.value
    except Exception as e:
        logging.error(e)
        response_status["responseStatus"] = VenvUpgradeStatus.ERROR.value
        raise e
    finally:
        response = json.dumps(response_status)
        print(response)


parser = argparse.ArgumentParser()

parser.add_argument(
    "--requirements",
    action="store",
    default=None,
    type=str,
    help="Dependency name, specifier and version in the format: <dependency_name><specifier><version>.",
)
parser.add_argument(
    "--requirements-file",
    action="store",
    default=None,
    type=str,
    help="Path to the requirements.txt file within a repository."
    + "Requirements file is passed to pip install -r <requirements_file>.",
)
parser.add_argument(
    "--envs-home",
    action="store",
    type=str,
    required=True,
    default=None,
    help="Path to the home of all virtualenv directories",
)
parser.add_argument(
    "--auto-upgrade",
    action="store_true",
    help="Whether to automatically install/upgrade the package or "
    + "notify the user that a new version is available",
)
parser.add_argument("--no-auto-upgrade", dest="auto-upgrade", action="store_false")
parser.add_argument(
    "--cloudsmith-url",
    action="store",
    type=str,
    default=None,
    help="Cloudsmith URL with an API key necessary during local testing.",
)
parser.add_argument("--log-location", help="Specifies where to store the log file")
parser.add_argument(
    "--test",
    action="store_true",
    help="Determines whether log messages will be output to stdout "
    + "or written to a log file",
)
parser.add_argument(
    "--update-from-local-wheels",
    action="store_true",
    help="Determines whether to install packages from local wheels, which "
    + "are expected to be in /vagrant/wheels directory",
)
parser.add_argument(
    "--wheels-path",
    action="store",
    type=str,
    default=None,
    help="Path to the directory containing the wheels.",
)
parser.add_argument(
    "--additional-dependencies",
    type=lambda s: [item for item in s.split(",")],
    help="Any additional dependencies that need to be installed with the requirements.",
)
parser.add_argument(
    "--blue-green-deployment", action="store_true", help="Run in blue-green deployment"
)
parser.add_argument(
    "--upgrade-python-package-version",
    action="store",
    default=None,
    type=str,
    help="Version of upgrade python package script to install in the virtual environment.",
)
parser.add_argument(
    "--local-installation-path",
    action="store",
    type=str,
    default=None,
    help="Path to the local unreleased upgrade-python-package directory to install in editable mode.",
)


def main():
    parsed_args = parser.parse_args()
    requirements = parsed_args.requirements
    requirements_file = parsed_args.requirements_file
    envs_home = parsed_args.envs_home
    auto_upgrade = parsed_args.auto_upgrade
    cloudsmith_url = parsed_args.cloudsmith_url
    log_location = parsed_args.log_location
    test = parsed_args.test
    update_from_local_wheels = parsed_args.update_from_local_wheels
    wheels_path = parsed_args.wheels_path
    additional_dependencies = parsed_args.additional_dependencies
    blue_green_deployment = parsed_args.blue_green_deployment
    upgrade_python_package_version = parsed_args.upgrade_python_package_version
    local_installation_path = parsed_args.local_installation_path
    manage_venv(
        envs_home=envs_home,
        requirements=requirements,
        requirements_file=requirements_file,
        auto_upgrade=auto_upgrade,
        cloudsmith_url=cloudsmith_url,
        log_location=log_location,
        test=test,
        update_from_local_wheels=update_from_local_wheels,
        wheels_path=wheels_path,
        additional_dependencies=additional_dependencies,
        blue_green_deployment=blue_green_deployment,
        upgrade_python_package_version=upgrade_python_package_version,
        local_installation_path=local_installation_path,
    )


if __name__ == "__main__":
    main()
