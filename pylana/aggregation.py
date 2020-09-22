import pandas as pd
from pandas.io.json import json_normalize

from pylana.api import API
from pylana.utils import create_metric, create_grouping

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
                  aggregation_function: str = 'sum',
                  date_type: str = 'startDate',
                  secondary_date_type: str = 'startDate',
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
                "byDuration", a duration grouping is returned and for one of
                ["byYear", "byMonth", "byQuarter", "byDayOfWeek", "byDayOfYear",
                "byHourOfDay"] a time grouping is returned. Otherwise the value is
                interpreted as a categorical attribute grouping.
            secondary_grouping:
                A string denoting an optional second grouping. For the value
                "byDuration", a duration grouping is returned and for one of
                ["byYear", "byMonth", "byQuarter", "byDayOfWeek", "byDayOfYear",
                "byHourOfDay"] a time grouping is returned. Otherwise the value is
                interpreted as a categorical attribute grouping.
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
                A string denoting the aggregation function to use.
                Can be one of ["min", "max", "sum", "mean", "median", "variance",
                "standardDeviation"] or a percentile as a string starting with "p"
                followed by the percentile value.
            date_type:
                A string denoting the date type of the grouping.
            secondary_date_type:
                A string denoting the date type of the secondary grouping.
            **kwargs:
                Keyword arguments passed to requests functions.

        Returns:
            A pandas DataFrame containing the aggregated data.
        """

        request_data = {'metric': create_metric(metric, aggregation_function),
                        'valuesFrom': {'type': values_from},
                        'miningRequest': {'logId': log_id,
                                          'activityExclusionFilter': activity_exclusion_filter,
                                          'traceFilterSequence': trace_filter_sequence},
                        'options': {'maxAmountAttributes': max_amount_attributes,
                                    'valueSorting': value_sorting,
                                    'sortingOrder': sorting_order}}

        if grouping is not None:
            request_data['grouping'] = create_grouping(grouping, date_type)

        if secondary_grouping is not None:
            request_data['secondaryGrouping'] = create_grouping(secondary_grouping, secondary_date_type)

        aggregate_response = self.post('/api/v2/aggregate-data', json = request_data, **kwargs)

        if aggregate_response.status_code >= 400:
            return pd.DataFrame()

        response_df = pd.DataFrame(aggregate_response.json()['chartValues'])

        if secondary_grouping is not None:
            response_df = response_df.explode('values').reset_index(drop = True)

            z_axis = response_df['zAxis']

            response_df = json_normalize(response_df['values'])

            response_df['zAxis'] = z_axis

        response_df.drop('$type', axis = 1, inplace = True)

        response_df = response_df.rename(columns = {'xAxis': grouping,
                                                    'yAxis': metric,
                                                    'zAxis': secondary_grouping})
        return(response_df)


    def boxplot_stats(self, log_id: str, metric: str, grouping: str = None,
                      values_from: str = 'allCases', **kwargs):
        """
        An aggregation function for the computation the metrics necessary for
        building a boxplot graph.

        Args:
            log_id:
                A string denoting the id of the log to aggregate.
            metric:
                A string denoting the metric.
            grouping:
                A string denoting the time or attribute grouping.
            values_from:
                A string denoting which values to consider for the aggregation.
            **kwargs:
                Keyword arguments passed to aggregate and request function.

        Returns:
            A pandas DataFrame containing the metrics needed for building a boxplot.
        """

        min_agg = self.aggregate(log_id = log_id, metric = metric, grouping = grouping,
                                 values_from = values_from, aggregation_function = 'min',
                                 **kwargs)
        max_agg = self.aggregate(log_id = log_id, metric = metric, grouping = grouping,
                                 values_from = values_from, aggregation_function = 'max',
                                 **kwargs)
        median_agg = self.aggregate(log_id = log_id, metric = metric, grouping = grouping,
                                    values_from = values_from, aggregation_function = 'median',
                                    **kwargs)
        p25_agg = self.aggregate(log_id = log_id, metric = metric, grouping = grouping,
                                 values_from = values_from, aggregation_function = 'p25',
                                 **kwargs)
        p75_agg = self.aggregate(log_id = log_id, metric = metric, grouping = grouping,
                                 values_from = values_from, aggregation_function = 'p75',
                                 **kwargs)

        boxplot_stats_df = pd.DataFrame({'min': min_agg[metric],
                                         'max': max_agg[metric],
                                         'median': median_agg[metric],
                                         'p25': p25_agg[metric],
                                         'p75': p75_agg[metric]})

        if grouping is not None:
            boxplot_stats_df.index = median_agg[grouping]

        return(boxplot_stats_df)
