from abc import ABC
from typing import Any

from mitm_tooling.representation import ColumnName
from .constants import *


class SupersetPostProcessing(pydantic.BaseModel, ABC):
    @pydantic.computed_field()
    @property
    def operation(self) -> str:
        raise NotImplementedError()


class DatasourceIdentifier(FrozenSupersetDefinition):
    id: SupersetId = '-1' # -1 as a placeholder
    type: Literal['table', 'annotation'] = 'table'

    dataset_uuid: StrUUID = pydantic.Field(exclude=True)

    @property
    def datasource_uid(self):
        return f'{self.id}__{self.type}'


class SupersetColumn(FrozenSupersetDefinition):
    column_name: str
    verbose_name: str | None = None
    id: SupersetId | None = None
    is_dttm: bool = False
    is_active: bool = True
    type: str = str(MITMDataType.Text.sa_sql_type)
    type_generic: GenericDataType = GenericDataType.STRING
    advanced_data_type: str | None = None
    groupby: bool = True
    filterable: bool = True
    expression: str | None = None
    description: str | None = None
    python_date_format: str | None = None
    extra: dict[str, Any] = pydantic.Field(default_factory=dict)


class IdentifiedSupersetColumn(SupersetColumn):
    id: SupersetId


class SupersetMetric(FrozenSupersetDefinition):
    metric_name: str
    verbose_name: str
    expression: str
    metric_type: str | None = None
    description: str | None = None
    d3format: str | None = None
    currency: str | None = None
    extra: dict[str, Any] = pydantic.Field(default_factory=dict)
    warning_text: str | None = None


class SupersetAdhocFilter(FrozenSupersetDefinition):
    clause: str = 'WHERE'
    subject: ColumnName
    operator: FilterOperator
    operatorId: FilterStringOperators | None = None
    comparator: str | None = 'No filter'
    expressionType: ExpressionType = ExpressionType.SIMPLE
    isExtra: bool = False
    isNew: bool = False
    sqlExpression: str | None = None


class SupersetAdhocMetric(FrozenSupersetDefinition):
    label: str
    column: SupersetColumn
    expressionType: ExpressionType = ExpressionType.SIMPLE
    aggregate: SupersetAggregate = SupersetAggregate.COUNT
    sqlExpression: str | None = None
    datasourceWarning: bool = False
    hasCustomLabel: bool = False
    optionName: str | None = None


class SupersetAdhocColumn(FrozenSupersetDefinition):
    label: str
    sqlExpression: str
    columnType: str = 'BASE_AXIS'
    expressionType: str = 'SQL'
    timeGrain: TimeGrain | None = None


OrderBy = tuple[SupersetAdhocMetric | str, bool]


class AnnotationOverrides(FrozenSupersetDefinition):
    time_range: str | None = None


class AnnotationLayer(FrozenSupersetDefinition):
    name: str
    value: int
    annotationType: AnnotationType
    sourceType: AnnotationSource = AnnotationSource.Table
    opacity: str = ''
    overrides: AnnotationOverrides
    hideLine: bool = False
    show: bool = False
    showLabel: bool = False
    showMarkers: bool = False
    style: str = 'solid'
    width: int = 1


class TimeAnnotationLayer(AnnotationLayer):
    annotationType: Literal[AnnotationType.Event, AnnotationType.Interval] = AnnotationType.Event
    titleColumn: str
    timeColumn: str = 'time'
    intervalEndColumn: str = ''
    color: str | None = None
    descriptionColumns: list[str] = pydantic.Field(default_factory=list)


class QueryObjectFilterClause(FrozenSupersetDefinition):
    col: ColumnName
    op: FilterOperator
    val: FilterValues | None = None
    grain: str | None = None
    isExtra: bool | None = None

    @classmethod
    def from_adhoc_filter(cls, adhoc_filter: SupersetAdhocFilter) -> Self:
        return cls(col=adhoc_filter.subject, op=adhoc_filter.operator, val=adhoc_filter.comparator)


class QueryObjectExtras(FrozenSupersetDefinition):
    having: str = ''
    where: str = ''
    time_grain_sqla: TimeGrain | None = None


AnnotationLayers = Annotated[list[AnnotationLayer] | None, pydantic.SerializeAsAny]
PostProcessingList = Annotated[list[SupersetPostProcessing | dict[str, Any]], pydantic.SerializeAsAny]


class QueryObject(BaseSupersetDefinition):
    annotation_layers: list[AnnotationLayer] = pydantic.Field(default_factory=list)
    applied_time_extras: dict[str, str] = pydantic.Field(default_factory=dict)
    columns: list[ColumnName | SupersetAdhocColumn] = pydantic.Field(default_factory=list)
    datasource: DatasourceIdentifier | None = None
    extras: QueryObjectExtras = pydantic.Field(default_factory=QueryObjectExtras)
    filters: list[QueryObjectFilterClause] = pydantic.Field(default_factory=list)
    metrics: list[SupersetAdhocMetric] | None = None
    granularity: str | None = None
    from_dttm: StrDatetime | None = None
    to_dttm: StrDatetime | None = None
    inner_from_dttm: StrDatetime | None = None
    inner_to_dttm: StrDatetime | None = None
    is_rowcount: bool = False
    is_timeseries: bool | None = None
    order_desc: bool = True
    orderby: list[OrderBy] = pydantic.Field(default_factory=list)
    post_processing: list[SupersetPostProcessing | dict[str, Any]] = pydantic.Field(default_factory=list)
    result_type: ChartDataResultType | None = None
    row_limit: int | None = None
    row_offset: int | None = None
    series_columns: list[ColumnName] = pydantic.Field(default_factory=list)
    series_limit: int = 0
    series_limit_metric: SupersetAdhocMetric | None = None
    time_offsets: list[str] = pydantic.Field(default_factory=list)
    time_shift: str | None = None
    time_range: str | None = None
    url_params: dict[str, str] | None = pydantic.Field(default_factory=dict)


class FormData(BaseSupersetDefinition):
    pass


class QueryContext(BaseSupersetDefinition):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    datasource: DatasourceIdentifier
    queries: list[QueryObject] = pydantic.Field(default_factory=list)
    form_data: FormData | None = pydantic.Field(default=None)
    result_type: ChartDataResultType = ChartDataResultType.FULL
    result_format: ChartDataResultFormat = ChartDataResultFormat.JSON
    force: bool = False
    custom_cache_timeout: int | None = None
