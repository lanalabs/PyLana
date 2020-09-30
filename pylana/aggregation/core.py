"""
api  for aggregation requests
"""

from typing import Optional

import pandas as pd

from pylana.aggregation.groupings import create_grouping
from pylana.aggregation.metrics import create_metric
from pylana.api import API


def extract_chart_values(jsn):
    """Cast json into data frame and remove artifacts columns.

    No error is raised in case we don't find artifact columns.
    """
    return pd.DataFrame(jsn['chartValues']) \
        .drop(columns=['$type'], errors='ignore')


def normalise_chart_values(df, json_col):
    df_aux = df \
        .explode(json_col) \
        .drop(columns=['$type'], errors='ignore') \
        .reset_index(drop=True)
    return pd.concat(
        [
            pd.json_normalize(df_aux.loc[:, json_col]).drop(columns=[
                '$type'], errors='ignore'),
            df_aux.drop(columns=[json_col])
        ], axis=1
    )


class AggregationAPI(API):

    def aggregate(self, log_id: str, metric: str,
                  grouping: str = None,
                  secondary_grouping: str = None,
                  max_amount_attributes: int = 10,
                  trace_filter_sequence: list = [],
                  activity_exclusion_filter: list = [],
                  value_sorting: str = 'caseCount',
                  sorting_order: str = 'descending',
                  values_from: str = 'allCases',
                  aggregation_function: Optional[str] = None,
                  percentile: Optional[float] = None,
                  attribute: Optional[str] = None,
                  secondary_attribute: Optional[str] = None,
                  activities: Optional[list] = None,
                  secondary_activities: Optional[list] = None,
                  date_type: Optional[str] = None,
                  secondary_date_type: Optional[str] = None,
                  **kwargs) -> pd.DataFrame:
        """
        An aggregation function for the computation of KPIs and grouping by
        metrics allowing the creation of bar-charts, line-charts, and other
        visualizations.

        Args:
            log_id:
                A string denoting the id of the log to aggregate.
            metric:
                A string denoting the metric to use. For the value
                "frequency", a frequency metric is returned and for "duration" a
                duration metric is returned. Otherwise the value is interpreted
                as a numeric attribute metric.
            grouping:
                A string denoting the grouping to use. For the value
                "byDuration", a duration grouping is returned. For "byAttribute"
                a grouping by a categorical attribute (the variable attribute
                needs to be passed) is returned. For one of ["byYear", "byMonth",
                "byQuarter", "byDayOfWeek", "byDayOfYear","byHourOfDay"] a time
                grouping is returned (date_type also needs to be set). If the
                activity aggregation "byActivity" is used, the activities to
                aggregate over need to be passed as list.
            secondary_grouping:
                A string denoting the optional secondary grouping to use.
                For the value "byDuration", a duration grouping is returned. For
                "byAttribute" a grouping by a categorical attribute (the variable
                secondary_attribute needs to be passed) is returned. For one of
                ["byYear", "byMonth", "byQuarter", "byDayOfWeek", "byDayOfYear",
                "byHourOfDay"] a time grouping is returned (secpmdary_date_type
                also needs to be set). If the activity aggregation "byActivity"
                is used, the secondary_activities to aggregate over need to be
                passed as list.
            max_amount_attributes:
                An integer denoting the maximum amount of attributes to return.
            trace_filter_sequence:
                A list containing the sequence of filters to apply.
            activity_exclusion_filter:
                A list containing the activities to exclude.
            value_sorting:
                A string denoting the metric to sort the aggregation by.
            sorting_order:
                A string denoting the order of the sorting.
            values_from:
                A string denoting which values to consider for the aggregation.
            aggregation_function:
                An optional string denoting the aggregation function to use for
                numeric attribute metrics.
                Can be one of ["min", "max", "sum", "mean", "median", "variance",
                "standardDeviation"].
            percentile:
                An optional float denoting the percentile to use if instead of
                the available aggregation types listed for aggregation_function
                a percentile aggregation should be used.
            attribute:
                An optional string denoting the attribute to use when grouping
                is set to 'byAttribute'.
            activities:
                An optional list denoting the activities to use when grouping
                is set to 'byActivity'.
            date_type:
                An optional string denoting the date type to use when a time
                grouping is used. It has to be 'startDate' or 'endDate'.
            secondary_attribute:
                An optional string denoting the attribute to use when secondary
                grouping is set to 'byAttribute'.
            secondary_activities:
                An optional list denoting the activities to use when secondary
                grouping is set to 'byActivity'.
            secondary_date_type:
                An optional string denoting the date type to use when a secondary
                time grouping is used. It has to be 'startDate' or 'endDate'.
            **kwargs:
                Keyword arguments passed to requests functions.

        Returns:
            A pandas DataFrame containing the aggregated data.
        """
        request_data = {'metric': create_metric(metric, aggregation_function, percentile),
                        'valuesFrom': {'type': values_from},
                        'miningRequest': {'logId': log_id,
                                          'activityExclusionFilter': activity_exclusion_filter,
                                          'traceFilterSequence': trace_filter_sequence},
                        'options': {'maxAmountAttributes': max_amount_attributes,
                                    'valueSorting': value_sorting,
                                    'sortingOrder': sorting_order}}

        if grouping is not None:
            request_data['grouping'] = create_grouping(grouping, date_type, activities,
                                                       attribute)

        if secondary_grouping is not None:
            request_data['secondaryGrouping'] = create_grouping(secondary_grouping,
                                                                secondary_date_type,
                                                                secondary_activities,
                                                                secondary_attribute
                                                                )

        aggregate_response = self.post('/api/v2/aggregate-data', json=request_data, **kwargs)

        if aggregate_response.status_code >= 400:
            return pd.DataFrame()

        response_df = extract_chart_values(aggregate_response.json())
        if secondary_grouping is not None:
            response_df = normalise_chart_values(response_df, 'values')

        response_df = response_df.rename(columns={'xAxis': attribute
                                                  if attribute is not None else grouping,
                                                  'yAxis': metric,
                                                  'zAxis': secondary_attribute
                                                  if secondary_attribute is not None
                                                  else secondary_grouping})
        return response_df

    def boxplot_stats(self, log_id: str, metric: str, grouping: str = None,
                      attribute: str = None, activities: list = None,
                      date_type: str = None, values_from: str = 'allCases',
                      **kwargs) -> pd.DataFrame:
        """
        An aggregation function for the computation the metrics necessary for
        building a standard boxplot graph by using the 25th, 50th and 75th
        percentile of the data.

        Args:
            log_id:
                A string denoting the id of the log to aggregate.
            metric:
                A string denoting the metric.
            grouping:
                A string denoting the grouping to use. For the value
                "byDuration", a duration grouping is returned. For "byAttribute"
                a grouping by a categorical attribute (the variable attribute
                needs to be passed) is returned. For one of ["byYear", "byMonth",
                "byQuarter", "byDayOfWeek", "byDayOfYear","byHourOfDay"] a time
                grouping is returned (date_type also needs to be set). If the
                activity aggregation "byActivity" is used, the activities to
                aggregate over need to be passed as list.
            attribute:
                An optional string denoting the attribute to use when grouping
                is set to 'byAttribute'.
            activities:
                An optional list denoting the activities to use when grouping
                is set to 'byActivity'.
            date_type:
                An optional string denoting the date type to use when a time
                grouping is used. It has to be 'startDate' or 'endDate'.
            values_from:
                A string denoting which values to consider for the aggregation.
            **kwargs:
                Keyword arguments passed to aggregate and request function.

        Returns:
            A pandas DataFrame containing the metrics needed for building a boxplot.
        """
        aggregations = [self.aggregate(log_id=log_id, metric=metric, grouping=grouping,
                                       values_from=values_from,
                                       aggregation_function=function, attribute=attribute,
                                       activities=activities, date_type=date_type,
                                       **kwargs) for function in ['min', 'max', 'median']]
        percentiles = [self.aggregate(log_id=log_id, metric=metric, grouping=grouping,
                                      values_from=values_from, percentile=percentile,
                                      attribute=attribute, activities=activities,
                                      **kwargs) for percentile in [25, 75]]

        boxplot_stats = pd.DataFrame({'min': aggregations[0][metric],
                                      'max': aggregations[1][metric],
                                      'median': aggregations[2][metric],
                                      'p25': percentiles[0][metric],
                                      'p75': percentiles[1][metric]})

        if grouping is not None:
            boxplot_stats.index = aggregations[0][attribute]

        return boxplot_stats
