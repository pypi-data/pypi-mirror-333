from __future__ import annotations

import io
import json
import mimetypes
import pathlib
import shutil
import tempfile
import zipfile
from datetime import datetime
from os import PathLike
from typing import Any, Dict, List, Optional, Union

import h2o_mlops_autogen
from h2o_mlops import _core, _projects, _utils, options


class MLOpsExperimentArtifact:
    def __init__(self, client: _core.Client, raw_info: Any):
        self._client = client
        self._raw_info = raw_info

    def __repr__(self) -> str:
        return (
            f"<class '{self.__class__.__module__}.{self.__class__.__name__}(\n"
            f"    uid={self.uid!r},\n"
            f"    experiment_uid={self.experiment_uid!r},\n"
            f"    name={self.name!r},\n"
            f"    state={self.state!r},\n"
            f"    mime_type={self.mime_type!r},\n"
            f"    size={self.size},\n"
            f"    md5_digest={self.md5_digest!r},\n"
            f"    created_time={self.created_time!r},\n"
            f"    uploaded_time={self.uploaded_time!r},\n"
            f"    last_modified_time={self.last_modified_time!r}\n"
            f")'>"
        )

    def __str__(self) -> str:
        return (
            f"UID: {self.uid}\n"
            f"Experiment UID: {self.experiment_uid}\n"
            f"Name: {self.name}\n"
            f"State: {self.state}\n"
            f"MIME Type: {self.mime_type}\n"
            f"Size: {self.size} bytes\n"
            f"MD5 Digest: {self.md5_digest}\n"
            f"Created Time: {self.created_time}\n"
            f"Uploaded Time: {self.uploaded_time}\n"
            f"Last Modified Time: {self.last_modified_time}"
        )

    @property
    def uid(self) -> str:
        """Experiment Artifact unique ID."""
        return self._raw_info.id

    @property
    def experiment_uid(self) -> str:
        """Associated parent Experiment unique ID."""
        self._update()
        return self._raw_info.entity_id

    @property
    def name(self) -> str:
        """Experiment Artifact display name."""
        self._update()
        return self._raw_info.type

    @property
    def state(self) -> str:
        """Experiment Artifact state."""
        return self._raw_info.state

    @property
    def mime_type(self) -> str:
        """Experiment Artifact MIME type."""
        return self._raw_info.mime_type

    @property
    def size(self) -> int:
        """Experiment Artifact size."""
        return self._raw_info.size

    @property
    def md5_digest(self) -> str:
        """Experiment Artifact MD5 Digest."""
        return self._raw_info.md5_digest

    @property
    def created_time(self) -> datetime:
        """Experiment Artifact created time."""
        return self._raw_info.created_time

    @property
    def uploaded_time(self) -> datetime:
        """Experiment Artifact uploaded time."""
        return self._raw_info.uploaded_time

    @property
    def last_modified_time(self) -> datetime:
        """Experiment Artifact modified time."""
        return self._raw_info.last_modified_time

    def get_model_info(self) -> Dict[str, Any]:
        """Get model details of Experiment Artifact."""
        return self._client._backend.ingest.model.create_model_ingestion(
            h2o_mlops_autogen.IngestModelIngestion(
                artifact_id=self.uid,
            )
        ).ingestion.to_dict()

    def update(
        self,
        name: Optional[str] = None,
        parent_experiment: Optional[MLOpsExperiment] = None,
    ) -> None:
        """Update Experiment Artifact.

        Args:
           name: display name for the Experiment Artifact.
           parent_experiment: parent Experiment to associate with the Artifact.
        """
        self._update()
        artifact = self._raw_info
        if name:
            artifact.type = name
        if parent_experiment:
            artifact.entity_id = parent_experiment.uid
        self._client._backend.storage.artifact.update_artifact(
            h2o_mlops_autogen.StorageUpdateArtifactRequest(
                artifact=artifact, update_mask="type,entityId"
            )
        )

    def download(
        self,
        directory: Optional[str] = None,
        file_name: Optional[str] = None,
        overwrite: bool = False,
        buffer: Optional[io.BytesIO] = None,
    ) -> Union[str, io.BytesIO]:
        """Download an Experiment Artifact.

        Args:
            directory: path to the directory where the file should be saved.
                By default, the current working directory is used.
            file_name: set the name of the file the artifact is saved to.
                By default, the artifact name is used.
            overwrite: overwrite existing files.
            buffer: in-memory buffer to store the downloaded artifact
                instead of saving it to a file.
        """
        if buffer:
            self._client._backend.storage.artifact.download_artifact(
                artifact_id=self.uid,
                file=buffer,
            )
            return buffer

        if directory:
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        else:
            directory = "./"
        if not file_name:
            file_name = self.name.replace("/", "_")
        dst_path = str(pathlib.Path(directory, file_name))

        try:
            if overwrite:
                mode = "wb"
            else:
                mode = "xb"
            with open(dst_path, mode) as f:
                self._client._backend.storage.artifact.download_artifact(
                    artifact_id=self.uid, file=f
                )
        except FileExistsError:
            print(f"{dst_path} already exists. Use `overwrite` to force download.")
            raise

        return dst_path

    def delete(self) -> None:
        """Delete Experiment Artifact."""
        self._client._backend.storage.artifact.delete_artifact(
            h2o_mlops_autogen.StorageDeleteArtifactRequest(self.uid)
        )

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Experiment Artifact to a Python dictionary, if possible."""
        if self.mime_type not in ["application/json"] and self.name != "vllm/config":
            raise RuntimeError(
                f"Artifact with mime_type '{self.mime_type}' "
                "cannot be converted to a dictionary, "
                "except for artifacts named 'vllm/config'."
            )
        return json.loads(self.to_string())

    def to_string(self) -> str:
        """Convert the Experiment Artifact to a Python string, if possible."""
        srv = self._client._backend.storage.artifact
        if self.mime_type not in ["application/json", "text/plain"]:
            if self.name == "vllm/config":
                with io.BytesIO() as f:
                    srv.download_artifact(artifact_id=self.uid, file=f)
                    with zipfile.ZipFile(f) as z:
                        with z.open("artifacts/vllm.json") as c:
                            return c.read().decode()
            raise RuntimeError(
                f"Artifact with mime_type '{self.mime_type}' "
                "cannot be converted to a string, "
                "except for artifacts named 'vllm/config'."
            )
        with io.BytesIO() as f:
            srv.download_artifact(artifact_id=self.uid, file=f)
            return f.getvalue().decode()

    def _update(self) -> None:
        self._raw_info = self._client._backend.storage.artifact.get_artifact(
            h2o_mlops_autogen.StorageGetArtifactRequest(id=self.uid)
        ).artifact


class MLOpsExperimentArtifacts:
    def __init__(self, client: _core.Client, experiment: MLOpsExperiment):
        self._client = client
        self._experiment = experiment

    def add(
        self, data: Union[str, io.BytesIO], mime_type: Optional[str] = None
    ) -> MLOpsExperimentArtifact:
        """Add a new artifact to an Experiment.

        Args:
            data: relative path to the artifact file or
                an in-memory buffer (`io.BytesIO`) containing the artifact data.
            mime_type: specify the data's media type in the MIME type format.
                If not specified, auto-detection of the media type will be attempted.
        """
        if isinstance(data, io.BytesIO):
            artifact_type = "in-memory buffer"
            mime_type = mime_type or mimetypes.types_map[".zip"]
        else:
            artifact_type = pathlib.Path(data).name
            try:
                mime_type = mime_type or mimetypes.types_map[pathlib.Path(data).suffix]
            except KeyError:
                raise RuntimeError("File MIME type not recognized.")
        artifact = self._client._backend.storage.artifact.create_artifact(
            h2o_mlops_autogen.StorageCreateArtifactRequest(
                artifact=h2o_mlops_autogen.StorageArtifact(
                    entity_id=self._experiment.uid,
                    mime_type=mime_type,
                    type=artifact_type,
                )
            )
        ).artifact
        if isinstance(data, io.BytesIO):
            self._client._backend.storage.artifact.upload_artifact(
                file=data, artifact_id=artifact.id
            )
        else:
            with open(data, mode="rb") as f:
                self._client._backend.storage.artifact.upload_artifact(
                    file=f, artifact_id=artifact.id
                )
        return self.get(uid=artifact.id)

    def get(self, uid: str) -> MLOpsExperimentArtifact:
        """Get the Artifact object corresponding to an H2O MLOps Artifact.

        Args:
            uid: H2O MLOps unique ID for the Artifact.
        """
        raw_info = self._client._backend.storage.artifact.get_artifact(
            h2o_mlops_autogen.StorageGetArtifactRequest(id=uid)
        ).artifact
        return MLOpsExperimentArtifact(client=self._client, raw_info=raw_info)

    def list(  # noqa A003
        self, exclude_deleted: bool = True, **selectors: Any
    ) -> _utils.Table:
        """List all Artifacts for the Experiment.

        Examples::

            # filter on columns by using selectors
            experiment.artifacts.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            artifact = experiment.artifacts.list()[0]

            # get a new Table using multiple indexes or slices
            table = experiment.artifacts.list()[2,4]
            table = experiment.artifacts.list()[2:4]
        """
        artifacts = self._client._backend.storage.artifact.list_entity_artifacts(
            h2o_mlops_autogen.StorageListEntityArtifactsRequest(
                entity_id=self._experiment.uid,
            )
        ).artifact
        data_as_dicts = [
            {
                "name": a.type,
                "mime_type": a.mime_type[:25],
                "uid": a.id,
            }
            for a in artifacts
            if not (
                exclude_deleted
                and a.state == h2o_mlops_autogen.ArtifactArtifactState.DELETED
            )
        ]
        return _utils.Table(
            data=data_as_dicts,
            keys=["name", "mime_type", "uid"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )


class MLOpsExperimentComments:
    def __init__(self, client: _core.Client, experiment: MLOpsExperiment):
        self._client = client
        self._experiment = experiment

    def add(self, message: str) -> None:
        """Add a new Comment to the Experiment.

        Args:
            message: text displayed by the Comment.
        """
        self._client._backend.storage.experiment.create_experiment_comment(
            h2o_mlops_autogen.StorageCreateExperimentCommentRequest(
                experiment_id=self._experiment.uid, comment_message=message
            )
        )

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """List Comments for the Experiment.

        Examples::

            # filter on columns by using selectors
            experiment.comments.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            comment = experiment.comments.list()[0]

            # get a new Table using multiple indexes or slices
            table = experiment.comments.list()[2,4]
            table = experiment.comments.list()[2:4]
        """
        comments = []
        response = self._client._backend.storage.experiment.list_experiment_comments(
            h2o_mlops_autogen.StorageListExperimentCommentsRequest(
                experiment_id=self._experiment.uid,
            )
        )
        comments += response.comment
        while response.paging:
            response = (
                self._client._backend.storage.experiment.list_experiment_comments(
                    h2o_mlops_autogen.StorageListExperimentCommentsRequest(
                        experiment_id=self._experiment.uid,
                        paging=h2o_mlops_autogen.StoragePagingRequest(
                            page_token=response.paging.next_page_token
                        ),
                    )
                )
            )
            comments += response.comment
        data = [
            dict(
                created=comment.created_time.strftime("%Y-%m-%d %I:%M:%S %p"),
                author=self._client._get_username(comment.author_id),
                message=comment.message,
            )
            for comment in comments
        ]
        data = sorted(data, key=lambda x: x["created"])
        return _utils.Table(
            data=data,
            keys=["created", "author", "message"],
            get_method=lambda x: x,
            **selectors,
        )


class MLOpsExperimentTags:
    def __init__(
        self,
        client: _core.Client,
        experiment: MLOpsExperiment,
        project: _projects.MLOpsProject,
    ):
        self._client = client
        self._experiment = experiment
        self._project = project

    def add(self, label: str) -> None:
        """Add a Tag to the Experiment.

        Args:
            label: text displayed by the Tag.
        """
        tag = self._experiment._project.tags.get_or_create(label)
        self._client._backend.storage.experiment.tag_experiment(
            h2o_mlops_autogen.StorageTagExperimentRequest(
                experiment_id=self._experiment.uid, tag_id=tag.uid
            )
        )

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """List Tags for the Experiment.

        Examples::

            # filter on columns by using selectors
            experiment.tags.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            tag = experiment.tags.list()[0]

            # get a new Table using multiple indexes or slices
            table = experiment.tags.list()[2,4]
            table = experiment.tags.list()[2:4]
        """
        # refresh list of tags
        tags = self._experiment._project.experiments.get(
            self._experiment.uid
        )._raw_info.tag
        data = [
            {"label": t.display_name, "uid": t.id}
            for t in tags
            if t.project_id == self._project.uid
        ]
        return _utils.Table(
            data=data,
            keys=["label"],
            get_method=lambda x: _projects.MLOpsProjectTag(
                self._client, self._project, x
            ),
            **selectors,
        )

    def remove(self, label: str) -> None:
        """Remove a Tag from the Experiment.

        Args:
            label: text displayed by the Tag.
        """
        tags = self._experiment.tags.list(label=label)
        if not tags:
            return
        tag = tags[0]
        self._client._backend.storage.experiment.untag_experiment(
            h2o_mlops_autogen.StorageUntagExperimentRequest(
                experiment_id=self._experiment.uid, tag_id=tag.uid
            )
        )


class MLOpsExperiment:
    """Interact with an Experiment on H2O MLOps."""

    def __init__(
        self, client: _core.Client, project: _projects.MLOpsProject, raw_info: Any
    ):
        self._artifacts: Optional[List[Any]] = None
        self._client = client
        self._project = project
        self._raw_info = raw_info

    @property
    def artifacts(self) -> MLOpsExperimentArtifacts:
        """Interact with artifacts for the Experiment."""
        return MLOpsExperimentArtifacts(self._client, self)

    @property
    def comments(self) -> MLOpsExperimentComments:
        """Interact with comments for the Experiment."""
        return MLOpsExperimentComments(self._client, self)

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._raw_info.metadata.values

    @property
    def name(self) -> str:
        """Experiment display name."""
        return self._raw_info.display_name

    @property
    def owner(self) -> str:
        """Experiment owner name."""
        return self._client._get_username(self._raw_info.owner_id)

    @property
    def scoring_artifact_types(self) -> List[str]:
        """List artifact types available for scoring."""
        if not self._artifacts:
            srv = self._client._backend.storage.artifact
            self._artifacts = srv.list_entity_artifacts(
                h2o_mlops_autogen.StorageArtifact(entity_id=self.uid)
            ).artifact

        artifact_name_mapping = {
            "python/mlflow": "python/mlflow.zip",
            "dai/mojo_pipeline": "dai_mojo_pipeline",
            "dai/scoring_pipeline": "dai_python_scoring_pipeline",
            "h2o3/mojo": "h2o3_mojo",
            "mlflow/mojo_pipeline": "mlflow_mojo_pipeline",
            "mlflow/scoring_pipeline": "mlflow_scoring_pipeline",
            "mlflow/h2o3_mojo": "mlflow_h2o3_mojo",
            "vllm/config": "vllm_config",
        }

        return [
            artifact_name_mapping[a.type]
            for a in self._artifacts
            if a.type in artifact_name_mapping
        ]

    @property
    def tags(self) -> MLOpsExperimentTags:
        """Interact with Tags for the Experiment."""
        return MLOpsExperimentTags(self._client, self, self._project)

    @property
    def input_schema(self) -> Optional[Dict[str, Any]]:
        """Experiment input schema."""
        input_schema = self._raw_info.metadata.values.get("input_schema", None)
        if input_schema:
            return input_schema.to_dict()

        return None

    @property
    def output_schema(self) -> Optional[Dict[str, Any]]:
        """Experiment output schema."""
        output_schema = self._raw_info.metadata.values.get("output_schema", None)
        if output_schema:
            return output_schema.to_dict()

        return output_schema

    @property
    def uid(self) -> str:
        """Experiment unique ID."""
        return self._raw_info.id

    @property
    def vllm_config(self) -> Optional[Dict[str, Any]]:
        """vLLM Experiment configuration."""
        artifacts = self.artifacts.list(name="vllm/config")
        return artifacts[0].to_dictionary() if artifacts else None

    def delete(self) -> None:
        """Delete Experiment from the Project in H2O MLOps."""
        self._client._backend.storage.experiment.delete_experiment(
            h2o_mlops_autogen.StorageDeleteExperimentRequest(
                id=self.uid, project_id=self._project.uid
            )
        )


class MLOpsExperiments:
    def __init__(self, client: _core.Client, project: _projects.MLOpsProject):
        self._client = client
        self._project = project

    def create(
        self,
        data: str | bytes | PathLike[str] | PathLike[bytes] | int,
        name: str,
    ) -> MLOpsExperiment:
        """Create an Experiment in H2O MLOps.

        Args:
            data: relative path to the experiment artifact being uploaded
            name: display name for Experiment
        """
        artifact = self._client._backend.storage.artifact.create_artifact(
            h2o_mlops_autogen.StorageCreateArtifactRequest(
                h2o_mlops_autogen.StorageArtifact(
                    entity_id=self._project.uid, mime_type=mimetypes.types_map[".zip"]
                )
            )
        ).artifact

        with open(data, mode="rb") as z:
            self._client._backend.storage.artifact.upload_artifact(
                file=z, artifact_id=artifact.id
            )

        ingestion = self._client._backend.ingest.model.create_model_ingestion(
            h2o_mlops_autogen.IngestModelIngestion(artifact_id=artifact.id)
        ).ingestion
        model_metadata = _utils._convert_metadata(ingestion.model_metadata)
        model_params = h2o_mlops_autogen.StorageExperimentParameters()
        if ingestion.model_parameters is not None:
            model_params.target_column = ingestion.model_parameters.target_column

        experiment = self._client._backend.storage.experiment.create_experiment(
            h2o_mlops_autogen.StorageCreateExperimentRequest(
                project_id=self._project.uid,
                experiment=h2o_mlops_autogen.StorageExperiment(
                    display_name=name,
                    metadata=model_metadata,
                    parameters=model_params,
                ),
            )
        ).experiment

        artifact.entity_id = experiment.id
        artifact.type = ingestion.artifact_type

        self._client._backend.storage.artifact.update_artifact(
            h2o_mlops_autogen.StorageUpdateArtifactRequest(
                artifact=artifact, update_mask="type,entityId"
            )
        )

        return self.get(experiment.id)

    def create_vllm(
        self,
        hub_model_id: str,
        name: Optional[str] = None,
        prompt_adapters: Optional[List[options.PromptAdapter]] = None,
        chat_template: Optional[str] = None,
        response_role: Optional[str] = None,
        gpu_memory_utilization: Optional[float] = None,
        kv_cache_dtype: Optional[str] = None,
        max_tokens_per_batch: Optional[int] = None,
        max_model_len: Optional[int] = None,
        quantization_method: Optional[str] = None,
    ) -> MLOpsExperiment:
        """Create an Experiment for vLLM Config in H2O MLOps.

        Args:
            hub_model_id: model repo id on a model hub.
            name: display name for deployment.
            prompt_adapters: list of prompt adapters to make available on
                the deployment server.
            chat_template: JINJA template for deployment tokenizer to follow.
            response_role: display name for chat response role.
            gpu_memory_utilization: approximate amount of GPU memory to allocate
                to the deployment. Values greater than 0.9 may cause GPU OOM errors.
            kv_cache_dtype: data type for KV cache.
            max_tokens_per_batch: deprecated.
            max_model_len: reducing this reduces the GPU memory requirements
                but also reduces the max context length.
            quantization_method: specify quantization method used by the model.
        """
        name = name or hub_model_id

        optional_params = {
            "chat_template": chat_template,
            "response_role": response_role,
            "gpu_memory_utilization": gpu_memory_utilization,
            "kv_cache_dtype": kv_cache_dtype,
            "max_tokens_per_batch": max_tokens_per_batch,
            "max_model_len": max_model_len,
            "quantization_method": quantization_method,
        }

        vllm_config: Dict[str, Any] = {
            "model": hub_model_id,
            "name": name,
            **{
                key: value
                for key, value in optional_params.items()
                if value is not None
            },
        }

        with tempfile.TemporaryDirectory() as workspace:
            vllm_config_path = pathlib.Path(workspace, "artifacts")
            vllm_config_path.mkdir(parents=True, exist_ok=True)

            if prompt_adapters:
                vllm_config["prompt_adapters"] = [
                    {"name": adapter.uid, "path": adapter.uid}
                    for adapter in prompt_adapters
                ]
                for adapter in prompt_adapters:
                    shutil.copytree(
                        src=adapter.path,
                        dst=vllm_config_path.joinpath(adapter.uid),
                    )

            vllm_config_file = vllm_config_path.joinpath("vllm.json")
            with open(vllm_config_file, "w") as f:
                json.dump(vllm_config, f)

            artifact_name = hub_model_id.split("/")[-1]
            artifact_archive_path = shutil.make_archive(
                base_name=str(pathlib.Path(workspace, f"{artifact_name}.zip")),
                format="zip",
                base_dir="artifacts",
                root_dir=workspace,
            )
            return self.create(data=artifact_archive_path, name=name)

    def get(self, uid: str) -> MLOpsExperiment:
        """Get the Experiment object corresponding to an H2O MLOps Experiment.

        Args:
            uid: H2O MLOps unique ID for the Experiment.
        """
        experiment = self._client._backend.storage.experiment.get_experiment(
            h2o_mlops_autogen.StorageGetExperimentRequest(
                id=uid,
                response_metadata=h2o_mlops_autogen.StorageKeySelection(
                    pattern=[
                        "source",
                        "score",
                        "dai/score",
                        "scorer",
                        "dai/scorer",
                        "test_score",
                        "dai/test_score",
                        "validation_score",
                        "dai/validation_score",
                        "tool_version",
                        "dai/tool_version",
                        "model_parameters",
                        "dai/model_parameters",
                        "model_type",
                        "tool",
                        "mlflow/flavors/python_function/loader_module",
                        "input_schema",
                        "output_schema",
                    ]
                ),
            )
        ).experiment
        return MLOpsExperiment(self._client, self._project, experiment)

    def list(  # noqa A003
        self, filter_vllm: bool = False, **selectors: Any
    ) -> _utils.Table:
        """Retrieve Table of Experiments available in the Project.

        Examples::

            # filter on columns by using selectors
            project.experiments.list(name="experiment-demo")

            # use an index to get an H2O MLOps entity referenced by the table
            experiment = project.experiments.list()[0]

            # get a new Table using multiple indexes or slices
            table = project.experiments.list()[2,4]
            table = project.experiments.list()[2:4]
        """
        experiments = self._list(**selectors)
        if filter_vllm:
            data = [
                {
                    "name": e.name,
                    "uid": e.uid,
                    "tags": "\n".join([t.label for t in e.tags.list()]),
                }
                for e in experiments
                if e.vllm_config
            ]
            return _utils.Table(
                data=data,
                keys=["name", "uid", "tags"],
                get_method=lambda x: self.get(x["uid"]),
            )
        return experiments

    def _list(self, **selectors: Any) -> _utils.Table:
        # construct tag filter if possible and asked for
        tag_filter = None
        tag_label = selectors.pop("tag", None)
        if tag_label and self._project.tags.list(label=tag_label):
            tag = self._project.tags.get_or_create(tag_label)
            tag_filter = h2o_mlops_autogen.StorageFilterRequest(
                query=h2o_mlops_autogen.StorageQuery(
                    clause=[
                        h2o_mlops_autogen.StorageClause(
                            tag_constraint=[
                                h2o_mlops_autogen.StorageTagConstraint(tag_id=tag.uid)
                            ]
                        )
                    ]
                )
            )
        # no need to search experiments if tag asked for does not exist in project
        if tag_filter is None and tag_label:
            data = []
        else:
            experiments = []
            response = self._client._backend.storage.experiment.list_experiments(
                h2o_mlops_autogen.StorageListExperimentsRequest(
                    project_id=self._project.uid, filter=tag_filter
                )
            )
            experiments += response.experiment
            while response.paging:
                response = self._client._backend.storage.experiment.list_experiments(
                    h2o_mlops_autogen.StorageListExperimentsRequest(
                        project_id=self._project.uid,
                        paging=h2o_mlops_autogen.StoragePagingRequest(
                            page_token=response.paging.next_page_token
                        ),
                        filter=tag_filter,
                    )
                )
                experiments += response.experiment
            data = [
                {
                    "name": m.display_name,
                    "uid": m.id,
                    "tags": "\n".join(
                        [
                            t.display_name
                            for t in m.tag
                            if t.project_id == self._project.uid
                        ]
                    ),
                }
                for m in experiments
            ]
        return _utils.Table(
            data=data,
            keys=["name", "uid", "tags"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )
