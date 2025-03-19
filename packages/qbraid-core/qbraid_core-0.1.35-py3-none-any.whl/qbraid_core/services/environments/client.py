# Copyright (c) 2025, qBraid Development Team
# All rights reserved.

"""
Module providing client for interacting with qBraid environments service.

"""
import logging
from pathlib import Path
from typing import Any

from qbraid_core.client import QbraidClient
from qbraid_core.exceptions import AuthError, RequestsApiError
from qbraid_core.registry import register_client
from qbraid_core.system.executables import get_python_executables

from .exceptions import EnvironmentServiceRequestError
from .paths import get_default_envs_paths
from .schema import EnvironmentConfig
from .validate import is_valid_env_name, is_valid_slug

logger = logging.getLogger(__name__)


@register_client()
class EnvironmentManagerClient(QbraidClient):
    """Client for interacting with qBraid environment services."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.envs_paths = get_default_envs_paths()

    @property
    def envs_paths(self) -> list[Path]:
        """Returns a dictionary of environment paths.

        Returns:
            A dictionary containing the environment paths.
        """
        return self._envs_paths

    @envs_paths.setter
    def envs_paths(self, value: list[Path]):
        """Sets the qBraid environments paths."""
        self._envs_paths = value

    def _validate_python_version(self, python_version: str) -> None:
        """Checks if the given python version is valid according to the system and conda
        python installations.

        Args:
            python_version: The python version to check.

        Returns:
            True if the python version is valid, False otherwise.
        """
        python_versions = get_python_executables()

        system_py_versions = python_versions["system"]
        value_in_system = python_version in system_py_versions

        conda_py_versions = python_versions["conda"]
        value_in_conda = python_version in conda_py_versions

        qbraid_client = None

        try:
            qbraid_client = QbraidClient()
        except (AuthError, EnvironmentServiceRequestError) as err:
            logger.error("Error creating QbraidClient: %s", err)

        if qbraid_client and qbraid_client.running_in_lab() is True:
            if value_in_system is False and value_in_conda is False:
                raise ValueError(
                    f"Python version '{python_version}' not found in system or conda"
                    " python installations"
                )
        else:
            if value_in_system is False:
                logger.warning(
                    "Python version '%s' not found in system python installations", python_version
                )
            # set the default here
            python_version = list(python_versions["system"].keys())[0]

        logger.info("Using python version '%s' for custom environment", python_version)

    def create_environment(self, config: EnvironmentConfig) -> dict[str, Any]:
        """Creates a new environment with the given configruation

        Args:
            config: Environment configuration.

        Returns:
            A dictionary containing the environment data.

        Raises:
            ValueError: If the environment name is invalid or the description is too long.
            EnvironmentServiceRequestError: If the create environment request fails.
        """
        if not is_valid_env_name(config.name):
            raise ValueError(f"Invalid environment name: {config.name}")

        if config.description and len(config.description) > 300:
            raise ValueError("Description is too long. Maximum length is 300 characters.")

        if config.python_version:
            self._validate_python_version(config.python_version)

        req_body = {}
        req_files = {}

        req_body.update(config.model_dump(by_alias=True))
        # TODO: update API to remove below logic

        # rename fields to conform with API request
        req_body["code"] = req_body.pop("pythonPackages")
        req_body["prompt"] = req_body.pop("shellPrompt")
        req_body["origin"] = "CORE"

        if config.icon:
            # need to pass an open file object to requests
            img_file = open(config.icon, "rb")  # pylint: disable=consider-using-with
            req_files["image"] = (Path(config.icon).stem, img_file, "image/png")

        try:
            env_data = self.session.post(
                "/environments/create", data=req_body, files=req_files
            ).json()
        except RequestsApiError as err:
            raise EnvironmentServiceRequestError(
                f"Create environment request failed: {err}"
            ) from err

        if env_data is None or len(env_data) == 0 or env_data.get("slug") is None:
            raise EnvironmentServiceRequestError(
                "Create environment request responded with invalid environment data"
            )

        return env_data

    def delete_environment(self, slug: str) -> None:
        """Deletes the environment with the given slug.

        Args:
            slug: The slug of the environment to delete.

        Returns:
            None

        Raises:
            ValueError: If the environment slug is invalid.
            EnvironmentServiceRequestError: If the delete environment request fails.
        """
        if not is_valid_slug(slug):
            raise ValueError(f"Invalid environment slug: {slug}")

        try:
            self.session.delete(f"/environments/{slug}")
        except RequestsApiError as err:
            raise EnvironmentServiceRequestError(
                f"Delete environment request failed: {err}"
            ) from err
