import enum
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List
from typing import Optional

import h2o_mlops_autogen

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


class KubernetesOptions:
    def __init__(
        self,
        replicas: int = 1,
        requests: Optional[Dict[str, str]] = None,
        limits: Optional[Dict[str, str]] = None,
        affinity: Optional[str] = None,
        toleration: Optional[str] = None,
    ):
        self._replicas = replicas
        self._requests = requests
        self._limits = limits
        self._affinity = affinity
        self._toleration = toleration

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'>"

    def __str__(self) -> str:
        return (
            f"replicas: {self.replicas}\n"
            f"requests: {self.requests}\n"
            f"limits: {self.limits}\n"
            f"affinity: {self.affinity}\n"
            f"toleration: {self.toleration}"
        )

    @property
    def replicas(self) -> int:
        return self._replicas

    @replicas.setter
    def replicas(self, x: int) -> None:
        self._replicas = x

    @property
    def requests(self) -> Optional[Dict[str, str]]:
        return self._requests

    @requests.setter
    def requests(self, x: Optional[Dict[str, str]]) -> None:
        self._requests = x

    @property
    def limits(self) -> Optional[Dict[str, str]]:
        return self._limits

    @limits.setter
    def limits(self, x: Optional[Dict[str, str]]) -> None:
        self._limits = x

    @property
    def affinity(self) -> Optional[str]:
        return self._affinity

    @affinity.setter
    def affinity(self, x: Optional[str]) -> None:
        self._affinity = x

    @property
    def toleration(self) -> Optional[str]:
        return self._toleration

    @toleration.setter
    def toleration(self, x: Optional[str]) -> None:
        self._toleration = x


@dataclass
class CORSOptions:
    origins: Optional[List[str]] = None


class MonitoringOptions:
    def __init__(
        self,
        enable: Optional[bool] = False,
        save_scoring_inputs: Optional[bool] = False,
    ):
        self._enable = enable
        self._save_scoring_inputs = save_scoring_inputs

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'>"

    def __str__(self) -> str:
        return (
            f"enable: {self.enable}\n"
            f"save_scoring_inputs: {self.save_scoring_inputs}"
        )

    @property
    def enable(self) -> Optional[bool]:
        return self._enable

    @enable.setter
    def enable(self, value: Optional[bool]) -> None:
        self._enable = value

    @property
    def save_scoring_inputs(self) -> Optional[bool]:
        return self._save_scoring_inputs

    @save_scoring_inputs.setter
    def save_scoring_inputs(self, value: Optional[bool]) -> None:
        self._save_scoring_inputs = value


class SecurityOptions:
    def __init__(
        self,
        passphrase: Optional[str] = None,
        hashed_passphrase: Optional[bool] = None,
        oidc_token_auth: Optional[bool] = None,
        disabled_security: Optional[bool] = None,
    ):
        self._passphrase = passphrase
        self._hashed_passphrase = hashed_passphrase
        self._oidc_token_auth = oidc_token_auth
        self._disabled_security = disabled_security

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'>"

    def __str__(self) -> str:
        return (
            f"passphrase: {self.passphrase}\n"
            f"hashed_passphrase: {self.hashed_passphrase}\n"
            f"oidc_token_auth: {self.oidc_token_auth}\n"
            f"disabled_security: {self.disabled_security}"
        )

    @property
    def passphrase(self) -> Optional[str]:
        return self._passphrase

    @passphrase.setter
    def passphrase(self, x: Optional[str]) -> None:
        self._passphrase = x

    @property
    def hashed_passphrase(self) -> Optional[bool]:
        return self._hashed_passphrase

    @hashed_passphrase.setter
    def hashed_passphrase(self, x: Optional[bool]) -> None:
        self._hashed_passphrase = x

    @property
    def oidc_token_auth(self) -> Optional[bool]:
        return self._oidc_token_auth

    @oidc_token_auth.setter
    def oidc_token_auth(self, x: Optional[bool]) -> None:
        self._oidc_token_auth = x

    @property
    def disabled_security(self) -> Optional[bool]:
        return self._disabled_security

    @disabled_security.setter
    def disabled_security(self, x: Optional[bool]) -> None:
        self._disabled_security = x

    @property
    def _is_bcrypt_hash(self) -> bool:
        return (
            self.passphrase is not None
            and re.match(
                re.compile(r"^\$2[ayb]?\$\d+\$[./A-Za-z0-9]{53}$"),
                self.passphrase,
            )
            is not None
        )

    @property
    def _is_pbkdf2_hash(self) -> bool:
        return (
            self.passphrase is not None
            and re.match(
                re.compile(r"^pbkdf2:sha(256|512):\d+\$.+\$.+$"),
                self.passphrase,
            )
            is not None
        )


class RequestContributionsOptions(Enum):
    NONE = h2o_mlops_autogen.ModelRequestParametersShapleyType.NONE
    ORIGINAL = h2o_mlops_autogen.ModelRequestParametersShapleyType.ORIGINAL
    TRANSFORMED = h2o_mlops_autogen.ModelRequestParametersShapleyType.TRANSFORMED


@dataclass
class ModelRequestParameters:
    id_field: Optional[str] = None
    contributions: Optional[RequestContributionsOptions] = None
    prediction_intervals: bool = False


@dataclass
class BatchKubernetesOptions:
    replicas: int = 1
    min_replicas: int = 1
    requests: Optional[Dict[str, str]] = None
    limits: Optional[Dict[str, str]] = None


class MimeTypeOptions(StrEnum):
    """
    Enum for specifying the MIME type of a batch source or sink.

    Attributes:
        CSV (str): The MIME type for CSV files.
        JSONL (str): The MIME type for JSONL files.
    """

    CSV = "text/csv"
    JSONL = "text/jsonl"


@dataclass
class BatchSourceOptions:
    """
    Dataclass for specifying a batch source.

    Attributes:
        spec_uid (str): The unique identifier for the batch source specification.
        config (Dict[str, Any]): The configuration for the batch source.
        mime_type (MimeTypeOptions): The MIME type of the batch source.
        location (str): The location of the batch source.
    """

    spec_uid: str
    config: Dict[str, Any]
    mime_type: MimeTypeOptions
    location: str


@dataclass
class BatchSinkOptions:
    """
    Dataclass for specifying a batch sink.

    Attributes:
        spec_uid (str): The unique identifier for the batch sink specification.
        config (Dict[str, str]): The configuration for the batch sink.
        mime_type (MimeTypeOptions): The MIME type of the batch sink.
        location (str): The location of the batch sink.
    """

    spec_uid: str
    config: Dict[str, Any]
    mime_type: MimeTypeOptions
    location: str


class LogicalType(Enum):
    """
    Enum representing the possible logical types for columns.

    Attributes:
        CATEGORICAL: Categorical/nominal data type
        NUMERICAL: Numerical/continuous data type
        DATETIME: DateTime column type
        TEXT: Text/string column type
        IMAGE: Image data type
        UNKNOWN: Unknown or undefined data type
    """

    CATEGORICAL = enum.auto()
    NUMERICAL = enum.auto()
    DATETIME = enum.auto()
    TEXT = enum.auto()
    IMAGE = enum.auto()
    TIMESTAMP = enum.auto()
    ID = enum.auto()
    UNKNOWN = enum.auto()

    def convert_to_proto(self) -> h2o_mlops_autogen.V2LogicalType:
        return {
            self.CATEGORICAL.value: h2o_mlops_autogen.V2LogicalType.CATEGORICAL,
            self.NUMERICAL.value: h2o_mlops_autogen.V2LogicalType.NUMERICAL,
            self.DATETIME.value: h2o_mlops_autogen.V2LogicalType.DATETIME,
            self.TEXT.value: h2o_mlops_autogen.V2LogicalType.TEXT,
            self.IMAGE.value: h2o_mlops_autogen.V2LogicalType.IMAGE,
            self.TIMESTAMP.value: h2o_mlops_autogen.V2LogicalType.TIMESTAMP,
            self.ID.value: h2o_mlops_autogen.V2LogicalType.ID,
        }.get(self.value, h2o_mlops_autogen.V2LogicalType.LOGICAL_TYPE_UNSPECIFIED)


@dataclass
class Column:
    """
    Dataclass for specifying a column in the deployment that will be monitored.

    Attributes:
    name (str): The name of the column
    logicalType (LogicalType): The logical type of the column
    is_model_output (bool): A flag indicating whether the column represents
        the output of a model (default is False)
    """

    name: str
    logical_type: LogicalType
    is_model_output: bool = False

    def convert_to_request(self) -> h2o_mlops_autogen.V2Column:
        return h2o_mlops_autogen.V2Column(
            name=self.name,
            logical_type=self.logical_type.convert_to_proto(),
            is_model_output=self.is_model_output,
        )


@dataclass
class NumericalAggregate:
    bin_edges: List[float]
    bin_count: List[int]
    mean_value: float
    standard_deviation: float
    min_value: float
    max_value: float
    sum_value: float

    def convert_to_request(self) -> h2o_mlops_autogen.V2NumericalAggregate:
        return h2o_mlops_autogen.V2NumericalAggregate(
            bin_edges=self.__infinity_edges(self.bin_edges),
            bin_count=self.bin_count,
            mean=self.mean_value,
            standard_deviation=self.standard_deviation,
            min=self.min_value,
            max=self.max_value,
            sum=self.sum_value,
        )

    @staticmethod
    def __infinity_edges(infinity_edges: List[float]) -> List[float]:
        return [x for x in infinity_edges if x not in {float("-inf"), float("inf")}]


@dataclass
class CategoricalAggregate:
    value_counts: Optional[Dict[str, int]] = None

    def convert_to_request(self) -> h2o_mlops_autogen.V2CategoricalAggregate:
        return h2o_mlops_autogen.V2CategoricalAggregate(
            value_counts=self.value_counts,
        )


@dataclass
class MissingValues:
    row_count: int

    def convert_to_request(self) -> h2o_mlops_autogen.V2MissingValues:
        return h2o_mlops_autogen.V2MissingValues(
            row_count=self.row_count,
        )


@dataclass
class BaselineData:
    column_name: str
    logical_type: LogicalType
    numerical_aggregate: Optional[NumericalAggregate] = None
    categorical_aggregate: Optional[CategoricalAggregate] = None
    missing_values: Optional[MissingValues] = None

    def convert_to_request(self) -> h2o_mlops_autogen.V2BaselineAggregation:
        return h2o_mlops_autogen.V2BaselineAggregation(
            column_name=self.column_name,
            logical_type=self.logical_type.convert_to_proto(),
            numerical_aggregate=(
                self.numerical_aggregate.convert_to_request()
                if self.numerical_aggregate
                else None
            ),
            categorical_aggregate=(
                self.categorical_aggregate.convert_to_request()
                if self.categorical_aggregate
                else None
            ),
            missing_values=(
                self.missing_values.convert_to_request()
                if self.missing_values
                else None
            ),
        )


@dataclass
class MonitoringRecordOptions:
    """
    Dataclass for specifying a monitoring record.

    Attributes:
        name (Optional[str]): The unique identifier for the monitoring record.
        display_name (Optional[str]): The display name of the monitoring record.
        description (Optional[str]): The description of the monitoring record.
        timestamp_column (Optional[str]): The name of timestamp column
            to use in monitoring.
        columns (Optional[List[Column]]): The list of columns to monitor.
        baseline_data (Optional[List[BaselineData]]): The list of baseline
    """

    name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    timestamp_column: Optional[str] = None
    columns: Optional[List[Column]] = None
    baseline_data: Optional[List[BaselineData]] = None

    def convert_to_request_options(self) -> h2o_mlops_autogen.V2MonitoringOptions:
        return h2o_mlops_autogen.V2MonitoringOptions(
            display_name=self.display_name if self.display_name else "",
            description=self.description if self.description else "",
            timestamp_column=self.timestamp_column if self.timestamp_column else "",
            columns=(
                [c.convert_to_request() for c in self.columns] if self.columns else []
            ),
            baseline_aggregations=(
                [a.convert_to_request() for a in self.baseline_data]
                if self.baseline_data
                else []
            ),
        )


@dataclass
class PromptAdapter:
    """
    Configure a PEFT Prompt Adapter to be used by the vLLM server.

    Args:
        uid: Unique identifier used for requesting the Prompt Adapter.
        path: Path to directory of adapter files created through PEFT.
    """

    uid: str
    path: str
