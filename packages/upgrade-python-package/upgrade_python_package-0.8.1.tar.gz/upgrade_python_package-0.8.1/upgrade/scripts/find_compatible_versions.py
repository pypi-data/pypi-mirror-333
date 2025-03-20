import argparse
import json
import logging
from enum import Enum
from typing import Any, List, Optional
from urllib.parse import urljoin

import lxml.etree as et
import requests as requests
from packaging.utils import parse_wheel_filename
from packaging.version import Version

from upgrade.scripts.requirements import (
    filter_versions,
    parse_requirements_txt,
    to_requirements_obj,
)
from upgrade.scripts.utils import get_venv_executable, is_package_already_installed
from upgrade.scripts.validations import is_cloudsmith_url_valid


class CompatibleUpgradeStatus(Enum):
    AVAILABLE = "AVAILABLE"
    AT_LATEST_VERSION = "AT_LATEST_VERSION"
    ERROR = "ERROR"


def _get_package_index_html(cloudsmith_url: str, package_name: str) -> str:
    package_index_url = urljoin(cloudsmith_url, package_name)
    package_full_index_url = (
        package_index_url
        if package_index_url.endswith("/")
        else package_index_url + "/"
    )
    return requests.get(package_full_index_url).text


def get_compatible_upgrade_versions(
    requirements_obj: Any, cloudsmith_url: str
) -> Optional[List[str]]:
    """Parse the package index HTML list of available packages
    and return a list of package versions that are compatible with the requirements specifier
    """
    package_index_html = _get_package_index_html(cloudsmith_url, requirements_obj.name)

    tree = et.HTML(package_index_html)
    anchor_tags_el = tree.xpath("//a")
    parsed_packages_versions = [
        parse_wheel_filename(tag_el.text)[1] for tag_el in anchor_tags_el
    ]
    logging.debug(f"Parsed packages versions: {parsed_packages_versions}")

    compatible_versions = filter_versions(
        requirements_obj.specifier, parsed_packages_versions
    )
    logging.debug(f"Found compatible versions: {compatible_versions}")

    return sorted(compatible_versions, reverse=True, key=Version)


def get_installed_version(requirements_obj: Any, venv_executable: str) -> Optional[str]:
    """Return the version of the package that is installed in the virtualenv."""
    try:
        return is_package_already_installed(requirements_obj.name, venv_executable)
    except Exception as e:
        logging.error(f"Error occurred while getting installed version: {str(e)}")
        raise e


def get_compatible_version(
    requirements_obj: Any,
    venv_path: str,
    cloudsmith_url: Optional[str] = None,
) -> Optional[str]:
    """Return the latest compatible version of the package that is installed in the virtualenv.
    Returns None if no compatible version is found.
    """
    venv_executable = get_venv_executable(venv_path)

    installed_version = get_installed_version(requirements_obj, venv_executable)
    if not installed_version:
        raise Exception(f"Package {requirements_obj.name} is not installed")
    logging.info(f"Found installed version: {installed_version}")

    upgrade_versions = get_compatible_upgrade_versions(requirements_obj, cloudsmith_url)
    for upgrade_version in upgrade_versions:
        if Version(upgrade_version) > Version(installed_version):
            return upgrade_version

    return None


def find_compatible_versions(
    venv_path: str,
    requirements: Optional[str],
    requirements_file: Optional[str],
    cloudsmith_url: Optional[str] = None,
    log_location: Optional[str] = None,
    test: Optional[bool] = None,
):
    """
    Entry point that retrieves the latest compatible version of a package that is installed in the virtualenv.
    This function is expected to be run periodically to check for available upgrades.

    Prerequisites:
    - virtualenv is created
    - package is installed in the virtualenv
    - requirements.txt file is present in the repository or requirements are passed as an argument

    There are three possible response states:
    - AVAILABLE: compatible version is available
    - AT_LATEST_VERSION: at latest version
    - ERROR: error occurred

    Raises an exception if expected package is not installed in the venv,
    or if requirements or requirements_file is not provided.
    """
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
        upgrade_version = get_compatible_version(
            to_requirements_obj(requirements), venv_path, cloudsmith_url
        )
        if upgrade_version:
            response_status["responseStatus"] = CompatibleUpgradeStatus.AVAILABLE.value
            logging.info(f"Found compatible upgrade version: {upgrade_version}")
        else:
            response_status[
                "responseStatus"
            ] = CompatibleUpgradeStatus.AT_LATEST_VERSION.value
            logging.info("At latest upgrade version")
    except Exception as e:
        response_status["responseStatus"] = CompatibleUpgradeStatus.ERROR.value
        logging.error(e)
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
    type=str,
    help="Path to the requirements.txt file within a repository."
    + "Requirements file is passed to pip install -r <requirements_file>.",
)
parser.add_argument(
    "--venv-path",
    action="store",
    type=str,
    required=True,
    help="Path to the virtualenv directory.",
)
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
    help="Determines whether log messages will be output to stdout, written to a log file and is used to determine logging level.",
)


def main():
    parsed_args = parser.parse_args()
    requirements = parsed_args.requirements
    requirements_file = parsed_args.requirements_file
    venv_path = parsed_args.venv_path
    cloudsmith_url = parsed_args.cloudsmith_url
    log_location = parsed_args.log_location
    test = parsed_args.test

    find_compatible_versions(
        venv_path=venv_path,
        requirements=requirements,
        requirements_file=requirements_file,
        cloudsmith_url=cloudsmith_url,
        log_location=log_location,
        test=test,
    )


if __name__ == "__main__":
    main()
