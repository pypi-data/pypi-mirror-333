from uuid import UUID
from mitm_tooling.data_types import MITMDataType
from mitm_tooling.utilities.python_utils import unique
from .core import mk_empty_adhoc_time_filter, mk_adhoc_metric, mk_pivot_post_processing, mk_adhoc_column
from .query import mk_query_object, mk_query_context, \
    mk_empty_query_object_time_filter_clause
from .utils import mk_uuid
from ..definitions import SupersetChartDef, PieChartParams, DatasourceIdentifier, SupersetAggregate, \
    SupersetVizType, TimeSeriesBarParams, TimeGrain, QueryObjectFilterClause, SupersetAdhocFilter, \
    TimeSeriesLineParams, QueryObjectExtras
from mitm_tooling.representation import ColumnName


def mk_pie_chart(name: str, datasource_identifier: DatasourceIdentifier, col: ColumnName, dt: MITMDataType,
                 groupby_cols: list[ColumnName] | None = None, uuid: UUID | None = None) -> SupersetChartDef:
    groupby_cols = groupby_cols or []
    metric = mk_adhoc_metric(col, agg=SupersetAggregate.COUNT, dt=dt)
    params = PieChartParams(datasource=datasource_identifier,
                            metric=metric,
                            groupby=groupby_cols,
                            adhoc_filters=[mk_empty_adhoc_time_filter()])
    # TODO may not be necessary to add groupby
    qo = mk_query_object(unique([col], groupby_cols), metrics=[metric],
                         filters=[mk_empty_query_object_time_filter_clause()])
    qc = mk_query_context(datasource=datasource_identifier, queries=[qo], form_data=params)

    return SupersetChartDef(slice_name=name,
                            viz_type=SupersetVizType.PIE,
                            dataset_uuid=datasource_identifier.dataset_uuid,
                            params=params,
                            query_context=qc,
                            uuid=uuid or mk_uuid())


def mk_time_series_bar_chart(name: str,
                             datasource_identifier: DatasourceIdentifier,
                             y_col: ColumnName,
                             y_dt: MITMDataType,
                             x_col: ColumnName,
                             groupby_cols: list[ColumnName] | None = None,
                             filters: list[SupersetAdhocFilter] | None = None,
                             uuid: UUID | None = None,
                             time_grain: TimeGrain | None = None) -> SupersetChartDef:
    groupby_cols = groupby_cols or []
    metric = mk_adhoc_metric(y_col, agg=SupersetAggregate.COUNT, dt=y_dt)
    adhoc_filters = [mk_empty_adhoc_time_filter()]
    if filters:
        adhoc_filters.extend(filters)
    params = TimeSeriesBarParams(datasource=datasource_identifier,
                                 metrics=[metric],
                                 groupby=groupby_cols,
                                 adhoc_filters=adhoc_filters,
                                 x_axis=x_col,
                                 time_grain_sqla=time_grain
                                 )

    pp = mk_pivot_post_processing(x_col, cols=[y_col], aggregations={metric.label: 'mean'},
                                  renames={metric.label: None})
    adhoc_x = mk_adhoc_column(x_col, timeGrain=time_grain)
    qo = mk_query_object(columns=unique([adhoc_x, y_col], groupby_cols),
                         metrics=[metric],
                         filters=[QueryObjectFilterClause.from_adhoc_filter(af) for af in adhoc_filters],
                         post_processing=pp,
                         series_columns=[y_col])
    qc = mk_query_context(datasource=datasource_identifier, queries=[qo], form_data=params)

    return SupersetChartDef(slice_name=name,
                            viz_type=SupersetVizType.TIMESERIES_BAR,
                            dataset_uuid=datasource_identifier.dataset_uuid,
                            params=params,
                            query_context=qc,
                            uuid=uuid or mk_uuid())


def mk_avg_count_time_series_chart(name: str,
                                   datasource_identifier: DatasourceIdentifier,
                                   groupby_cols: list[ColumnName],
                                   time_col: ColumnName = 'time',
                                   filters: list[SupersetAdhocFilter] | None = None,
                                   uuid: UUID | None = None,
                                   time_grain: TimeGrain | None = None):
    groupby_cols = groupby_cols or []
    metric = mk_adhoc_metric(time_col, agg=SupersetAggregate.COUNT, dt=MITMDataType.Datetime)
    adhoc_filters = [mk_empty_adhoc_time_filter()]
    if filters:
        adhoc_filters.extend(filters)
    params = TimeSeriesLineParams(datasource=datasource_identifier,
                                  metrics=[metric],
                                  groupby=groupby_cols,
                                  adhoc_filters=adhoc_filters,
                                  x_axis=time_col,
                                  time_grain_sqla=time_grain
                                  )

    pp = mk_pivot_post_processing(time_col, cols=groupby_cols, aggregations={metric.label: 'mean'},
                                  renames={metric.label: None})
    adhoc_time_col = mk_adhoc_column(time_col, timeGrain=time_grain)
    qo = mk_query_object(columns=unique([adhoc_time_col], groupby_cols),
                         metrics=[metric],
                         filters=[QueryObjectFilterClause.from_adhoc_filter(af) for af in adhoc_filters],
                         post_processing=pp,
                         series_columns=groupby_cols,
                         extras=QueryObjectExtras(time_grain_sqla=time_grain))
    qc = mk_query_context(datasource=datasource_identifier, queries=[qo], form_data=params)

    return SupersetChartDef(slice_name=name,
                            viz_type=SupersetVizType.TIMESERIES_LINE,
                            dataset_uuid=datasource_identifier.dataset_uuid,
                            params=params,
                            query_context=qc,
                            uuid=uuid or mk_uuid())
