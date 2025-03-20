import enum
import functools
from copy import copy
from typing import Any, Callable, Dict, List, Optional

from h2o_mlops.options import (
    BaselineData,
    CategoricalAggregate,
    Column,
    LogicalType,
    MissingValues,
    MonitoringRecordOptions,
    NumericalAggregate,
)

try:
    import numpy
    import pyspark as _pyspark
    import pyspark.sql as _pyspark_sql
    import pyspark.sql.functions as fun

    spark_available = True
except ImportError:
    spark_available = False


def spark_required(func: Callable) -> Callable:
    @functools.wraps(func)
    def check_spark(*args: Any, **kwargs: Any) -> Any:
        if not spark_available:
            raise RuntimeError("PySpark is required to use this function.")
        return func(*args, **kwargs)

    return check_spark


class Format(enum.Enum):
    """Data formats for source/sink."""

    BIGQUERY = "Google BigQuery table"
    CSV = "CSV file"
    JDBC_QUERY = "SQL query through JDBC connection"
    JDBC_TABLE = "SQL table through JDBC connection"
    ORC = "ORC file"
    PARQUET = "Parquet file"
    SNOWFLAKE_QUERY = "Snowflake query"
    SNOWFLAKE_TABLE = "Snowflake table"


format_map: Dict[Format, Dict[str, str]] = {
    Format.BIGQUERY: {"format": "bigquery"},
    Format.CSV: {"format": "csv", "header": "true", "inferschema": "true"},
    Format.JDBC_QUERY: {"format": "jdbc"},
    Format.JDBC_TABLE: {"format": "jdbc"},
    Format.ORC: {"format": "orc"},
    Format.PARQUET: {"format": "parquet"},
    Format.SNOWFLAKE_QUERY: {"format": "net.snowflake.spark.snowflake"},
    Format.SNOWFLAKE_TABLE: {"format": "net.snowflake.spark.snowflake"},
}


@spark_required
def read_source(
    spark: _pyspark_sql.SparkSession,
    source_data: str,
    source_format: Format,
    source_config: Optional[Dict[str, str]] = None,
) -> _pyspark_sql.DataFrame:
    _source_config = copy(format_map[source_format])
    if source_config:
        _source_config.update(source_config)
    if source_format in [Format.JDBC_QUERY, Format.SNOWFLAKE_QUERY]:
        _source_config["query"] = source_data
    if source_format in [Format.JDBC_TABLE, Format.SNOWFLAKE_TABLE]:
        _source_config["dbtable"] = source_data
    if source_format in [
        Format.JDBC_QUERY,
        Format.JDBC_TABLE,
    ] and not _source_config.get("url"):
        raise RuntimeError("JDBC connection URL required for source.")
    if source_format in [
        Format.SNOWFLAKE_QUERY,
        Format.SNOWFLAKE_TABLE,
    ]:
        required_sf_options = {
            "sfDatabase",
            "sfURL",
            "sfUser",
        }
        missing_sf_options = required_sf_options.difference(_source_config.keys())
        if missing_sf_options:
            raise RuntimeError(
                f"Snowflake option(s) {missing_sf_options} required for source."
            )

    if source_format in [
        Format.JDBC_QUERY,
        Format.JDBC_TABLE,
        Format.SNOWFLAKE_QUERY,
        Format.SNOWFLAKE_TABLE,
    ]:
        return spark.read.load(**_source_config)
    else:
        return spark.read.load(source_data, **_source_config)


@spark_required
def get_spark_master() -> str:
    active_session = _pyspark_sql.SparkSession.getActiveSession()
    if active_session:
        return active_session.conf.get("spark.master")

    if hasattr(_pyspark.SparkContext, "_active_spark_context"):
        active_context = _pyspark.SparkContext._active_spark_context
        if hasattr(active_context, "master") and active_context.master:
            return active_context.master

    return "local[*]"


@spark_required
def get_spark_session(
    app_name: str = "mlops_spark_scorer_job",
    mini_batch_size: int = 1000,
    master: Optional[str] = None,
    spark_config: Optional[Dict[str, Any]] = None,
) -> _pyspark_sql.SparkSession:
    if not spark_config:
        spark_config = {}
    conf = _pyspark.SparkConf()
    conf.setAppName(app_name)
    if master:
        conf.setMaster(master)
    if master and master.startswith("local"):
        driver_memory = conf.get("spark.driver.memory", "5g")
        conf.set("spark.driver.memory", driver_memory)
    conf.get("spark.sql.caseSensitive", "true")
    conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", str(mini_batch_size))
    conf.setAll([(k, str(v)) for k, v in spark_config.items()])
    spark = _pyspark_sql.SparkSession.builder.config(conf=conf).getOrCreate()
    return spark


@spark_required
def prepare_monitoring_record_options_from_data_frame(
    data_frame: _pyspark_sql.DataFrame,
    logical_type_overrides: Optional[Dict[str, LogicalType]] = None,
    monitored_columns: Optional[List[Column]] = None,
    name: Optional[str] = None,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    timestamp_column: Optional[str] = "__timestamp__",
) -> MonitoringRecordOptions:
    data_frame.cache()
    data_frame = data_frame.withColumn(
        timestamp_column,
        col=fun.lit(0).cast(_pyspark_sql.types.TimestampType()),
    )

    logical_types = _infer_logical_type(
        data_frame,
        logical_type_overrides=logical_type_overrides,
        timestamp_column=timestamp_column,
        monitored_columns=monitored_columns,
    )

    baseline = _get_categorical_aggs(
        data_frame,
        logical_types=logical_types,
        timestamp_column=timestamp_column,
    )

    baseline_numerical_edges = _get_numerical_edges(
        data_frame,
        logical_types=logical_types,
    )

    baseline_numerical_aggs = _get_numerical_aggs(
        data_frame,
        baseline_numerical_edges=baseline_numerical_edges,
        timestamp_column=timestamp_column,
    )

    baseline.extend(baseline_numerical_aggs)

    if not monitored_columns:
        monitored_columns = [
            Column(
                name=base.column_name,
                logical_type=base.logical_type,
            )
            for base in baseline
        ]

    return MonitoringRecordOptions(
        name=name,
        display_name=display_name,
        description=description,
        timestamp_column=timestamp_column,
        columns=monitored_columns,
        baseline_data=baseline,
    )


def _infer_logical_type(
    sdf: _pyspark_sql.DataFrame,
    logical_type_overrides: Optional[Dict[str, LogicalType]] = None,
    timestamp_column: str = "__timestamp__",
    monitored_columns: Optional[List[Column]] = None,
) -> Dict[str, LogicalType]:
    logical_types = {}
    for field in sdf.schema.fields:
        if not monitored_columns or field.name in monitored_columns:
            if isinstance(field.dataType, _pyspark_sql.types.StringType):
                if sdf.select(fun.count_distinct(field.name)).first()[0] < 10000:
                    logical_types[field.name] = LogicalType.CATEGORICAL
                else:
                    logical_types[field.name] = LogicalType.UNKNOWN
            else:
                logical_types[field.name] = LogicalType.NUMERICAL
    if logical_type_overrides:
        logical_types.update(logical_type_overrides)
    logical_types[timestamp_column] = LogicalType.TIMESTAMP
    return logical_types


def _get_categorical_aggs(
    sdf: _pyspark_sql.DataFrame,
    logical_types: Dict[str, LogicalType],
    timestamp_column: str,
) -> List[BaselineData]:
    aggregates: List[BaselineData] = []
    categorical_columns = [
        k for k, v in logical_types.items() if v == LogicalType.CATEGORICAL
    ]
    for column_name in categorical_columns:
        counts = sdf.groupby(timestamp_column, column_name).count()
        counts = (
            counts.groupby(timestamp_column)
            .pivot(column_name)
            .sum()
            .fillna(0)
            .drop(timestamp_column)
        )
        value_counts_dict = counts.toPandas().iloc[0].to_dict()  # type: ignore
        data = BaselineData(
            column_name=column_name,
            logical_type=LogicalType.CATEGORICAL,
            categorical_aggregate=CategoricalAggregate(
                value_counts=value_counts_dict,
            ),
        )
        aggregates.append(data)
    return aggregates


def _get_numerical_edges(
    sdf: _pyspark_sql.DataFrame, logical_types: Dict[str, LogicalType]
) -> Dict[str, List[float]]:
    numerical_columns = [
        k for k, v in logical_types.items() if v == LogicalType.NUMERICAL
    ]
    numerical_edges = {}
    edges = sdf.approxQuantile(
        col=numerical_columns,
        probabilities=[x / 10 for x in range(0, 11)],
        relativeError=1e-6,
    )
    for k, v in zip(numerical_columns, edges):
        numerical_edges[k] = [float("-inf")] + list(dict.fromkeys(v)) + [float("inf")]
    return numerical_edges


def _get_numerical_aggs(
    sdf: _pyspark_sql.DataFrame,
    baseline_numerical_edges: Dict[str, List[float]],
    timestamp_column: str,
) -> List[BaselineData]:
    aggregates: List[BaselineData] = []
    grouped_sdf = sdf.groupby(timestamp_column)
    for column_name, edges in baseline_numerical_edges.items():
        col = sdf[column_name]
        native_aggs = grouped_sdf.agg(
            fun.count(fun.when(fun.isnull(col), timestamp_column)).alias(
                f"missing_count({column_name})"
            ),
            fun.count(col),
            fun.sum(col),
            fun.min(col),
            fun.max(col),
            fun.mean(col),
            fun.stddev(col),
        )
        rdd = sdf.select(timestamp_column, column_name).dropna().rdd
        num_bins = len(edges) - 1
        rdd_aggs = (
            rdd.aggregateByKey(  # type: ignore
                zeroValue=numpy.zeros(num_bins, dtype=int),
                seqFunc=lambda x, y: x
                + numpy.histogram(y, bins=edges)[0],  # noqa: B023
                combFunc=lambda x, y: x + y,
            )
            .map(lambda x: (x[0], x[1].tolist()))
            .toDF(
                _pyspark_sql.types.StructType(
                    [
                        _pyspark_sql.types.StructField(
                            timestamp_column,
                            _pyspark_sql.types.TimestampType(),
                            True,
                        ),
                        _pyspark_sql.types.StructField(
                            "histogram_counts",
                            _pyspark_sql.types.ArrayType(
                                _pyspark_sql.types.LongType(), True
                            ),
                            True,
                        ),
                    ]
                )
            )
        )
        result_df = native_aggs.join(rdd_aggs, on=timestamp_column).cache()

        rows = result_df.collect()
        for row in rows:

            baseline_data = BaselineData(
                column_name=column_name,
                logical_type=LogicalType.NUMERICAL,
                numerical_aggregate=NumericalAggregate(
                    bin_edges=edges,
                    bin_count=row["histogram_counts"],
                    mean_value=row[f"avg({column_name})"],
                    standard_deviation=row[f"stddev({column_name})"],
                    min_value=row[f"min({column_name})"],
                    max_value=row[f"max({column_name})"],
                    sum_value=row[f"sum({column_name})"],
                ),
                missing_values=MissingValues(
                    row_count=row[f"missing_count({column_name})"],
                ),
            )
            aggregates.append(baseline_data)

        result_df.unpersist()

    return aggregates
