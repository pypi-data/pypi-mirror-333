from __future__ import annotations

from typing import Any

import h2o_mlops_autogen
from h2o_mlops import _core
from h2o_mlops import _projects
from h2o_mlops import _utils


class MLOpsEnvironment:
    """Interact with an Environment on H2O MLOps."""

    def __init__(self, raw_info: Any):
        self._raw_info = raw_info

    @property
    def name(self) -> str:
        """Environment display name."""
        return self._raw_info.display_name

    @property
    def uid(self) -> str:
        """Environment unique ID."""
        return self._raw_info.id


class MLOpsEnvironments:
    def __init__(self, client: _core.Client, project: _projects.MLOpsProject):
        self._client = client
        self._project = project

    def get(self, uid: str) -> MLOpsEnvironment:
        """Get the Environment object corresponding to an Environment in H2O MLOps.

        Args:
            uid: H2O MLOps unique ID for the Environment.
        """
        storage = self._client._backend.storage
        raw_info = storage.deployment_environment.get_deployment_environment(
            h2o_mlops_autogen.StorageGetDeploymentEnvironmentRequest(
                deployment_environment_id=uid
            )
        ).deployment_environment
        return MLOpsEnvironment(raw_info)

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """Retrieve Table of Environments available in the Project.

        Examples::

            # filter on columns by using selectors
            project.environments.list(name="DEV")

            # use an index to get an H2O MLOps entity referenced by the table
            environment = project.environments.list()[0]

            # get a new Table using multiple indexes or slices
            table = project.environments.list()[2,4]
            table = project.environments.list()[2:4]
        """
        storage = self._client._backend.storage
        environments = storage.deployment_environment.list_deployment_environments(
            h2o_mlops_autogen.StorageListDeploymentEnvironmentsRequest(
                self._project.uid
            )
        ).deployment_environment
        data = [{"name": e.display_name, "uid": e.id} for e in environments]
        return _utils.Table(
            data=data,
            keys=["name", "uid"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )
