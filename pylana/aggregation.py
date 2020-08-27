from pylana.api import API
import pandas as pd
from pandas.io.json import json_normalize

class AggregationAPI(API):
    
    def create_metric(metric_value, aggregation_function = 'sum'):
        if metric_value == 'frequency':
            return({'type': 'frequency'})
        elif metric_value == 'duration':
            return({'type': 'duration',
                    'aggregationFunction': aggregation_function})
        else:
            return({'type': 'attribute',
                    'attribute': metric_value,
                    'aggregationFunction': aggregation_function})

    def create_grouping(grouping_value, date_type = 'startDate'):
        if grouping_value == 'byDuration':
            return({'type': 'byDuration'})
        elif grouping_value in ['byYear', 'byMonth', 'byQuarter', 'byDayOfWeek', 'byDayOfYear', 'byHourOfDay']:
            return({'type': grouping_value,
                    'dateType': date_type,
                    'timeZone': 'Europe/Berlin'})
        else:
            return({'type': 'byAttribute',
                    'attribute': grouping_value})
    
    def aggregate(self, metric: str, grouping: str = None, 
                  secondary_grouping: str = None,
                  log_id: str, max_amount_attributes: int = 10, 
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
            metric: 
                A string denoting the metric.
            grouping:
                A string denoting the time or attribute grouping.
            secondary_grouping:
                A string denoting an additional time or attribute grouping.
            log_id:
                A string denoting the id of the log to aggregate.
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
                A string denoting the function to aggregate the metric by.
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
        
        print(request_data)
        
        aggregate_response = self.post('/api/v2/aggregate-data', json = request_data, **kwargs)
        
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