"""
functions to prepare requests for consumption
"""

from collections import defaultdict
from typing import Iterable, Dict, List, Union

import re
import pandas as pd


def create_aggregation_function(aggregation_function: str) -> dict:
    """
    Create a dictionary containing the aggregation function in a format necessary
    for the aggregation API request.

    Args:
        aggregation_function:
            A string denoting the aggregation function to use.
            Can be one of ["min", "max", "sum", "mean", "median", "variance",
            "standardDeviation"] or a percentile as a string starting with "p"
            followed by the percentile value.

    Returns:
        A dictionary containing the aggregation function string.
    """
    if re.match('^p[0-9]{1,3}', aggregation_function):
        return ({'aggregationFunction': {'type': 'percentile',
                                         'percentile': int(aggregation_function[1:])}})
    else:
        return {'aggregationFunction': aggregation_function}


def create_metric(metric_value: str, aggregation_function: str = 'sum') -> dict:
    """
    Create a dictionary containing the metric in a format necessary
    for the aggregation API request.

    Args:
        metric_value:
            A string denoting the metric to use. For the value
            "frequency", a frequency metric is returned and for "duration" a
            duration metric is returned. Otherwise the value is interpreted
            as a numeric attribute metric.
        aggregation_function:
            A string denoting the aggregation function to use.
            Can be one of ["min", "max", "sum", "mean", "median", "variance",
            "standardDeviation"] or a percentile as a string starting with "p"
            followed by the percentile value.

    Returns:
        A dictionary containing the metric in the right format for the request.
    """
    if metric_value == 'frequency':
        return {'type': 'frequency'}
    elif metric_value == 'duration':
        metric = {'type': 'duration'}
        metric.update(create_aggregation_function(aggregation_function))
        return metric
    else:
        metric = {'type': 'attribute',
                  'attribute': metric_value}
        metric.update(create_aggregation_function(aggregation_function))
        return metric


def create_grouping(grouping_value: Union[str, Iterable], date_type: str = 'startDate') -> dict:
    """
    Create a dictionary containing the grouping in a format necessary
    for the aggregation API request.

    Args:
        grouping_value:
            A string or iterable denoting the grouping to use. For the value
            "byDuration", a duration grouping is returned and for one of
            ["byYear", "byMonth", "byQuarter", "byDayOfWeek", "byDayOfYear",
            "byHourOfDay"] a time grouping is returned. If an iterable is passed,
            the elements will be interpreted as selected activities for a grouping
            by activity. Otherwise the value is interpreted as a categorical attribute
            grouping.
        date_type:
            A string denoting the aggregation function to use.

    Returns:
        A dictionary containing the metric in the right format for the request.
    """
    intervals = ['byYear', 'byMonth', 'byQuarter', 'byDayOfWeek', 'byDayOfYear', 'byHourOfDay']
    if grouping_value == 'byDuration':
        return {'type': 'byDuration'}
    elif grouping_value in intervals:
        return {'type': grouping_value,
                'dateType': date_type,
                'timeZone': 'Europe/Berlin'}
    elif isinstance(grouping_value, Iterable):
        return {'type': 'byActivity',
                'selectedActivities': grouping_value}
    else:
        return {'type': 'byAttribute',
                'attribute': grouping_value}


# TODO: check whether this function is actually required
def create_semantics(columns: Iterable[str],
                     case_id: str = 'id', action: str = 'action', start: str = 'start', complete: str = 'complete',
                     numerical_attributes: Iterable[str] = tuple(), time_format: str = 'yyyy-MM-dd HH:mm:ss') \
        -> List[Dict[str, str]]:
    """
    create semantics including numeric and categorical attributes

    Args:
        columns: strings representing the columns  of the table
        case_id: the column name for the case ids
        action: the column name for the activities
        start: the column name for the start timestamp
        complete: the column name for the complete timestamp
        numerical_attributes: the column names for the numerical attributes
        time_format: the time format for start and complete columns

    Returns:
        a list of dicts representing the semantics file
    """

    semantics = defaultdict(lambda: 'CategorialAttribute')

    semantics_fixed = {case_id: 'Case ID', action: 'Action', start: 'Start', complete: 'Complete'}
    semantics_numeric = {numeric: 'NumericAttribute' for numeric in numerical_attributes}

    semantics.update(semantics_fixed)
    semantics.update(semantics_numeric)

    return [
        {
            'idx': idx,
            'name': col,
            'semantic': semantics[col],
            'format': time_format if semantics[col] in ['Start', 'Complete'] else None
        } for idx, col in enumerate(columns)
    ]


def create_event_semantics_from_df(df: pd.DataFrame, case_id: str = 'Case_ID', action: str = 'Action',
                                   start: str = 'Start', complete: str = 'Complete',
                                   time_format: str = "yyyy-MM-dd'T'HH:mm:ss.SSSSSS") -> List[dict]:
    """
    create event semantics from a pandas data frame

    The columns semantic for lana will be derived from the data frame's dtypes. All types
    will be converted to categorical attributes, besides numbers. The Start and Complete
    time stamps need to have the same time format. For an overview over time stamp formats
    see https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html#patterns
    """
    semantics = []
    id_mappings = {
        case_id: 'Case ID', action: 'Action'
    }
    timestamps_mappings = {
        start: 'Start', complete: 'Complete'
    }

    for i, col in enumerate(df.columns):
        is_lana_categorial = \
            pd.api.types.is_object_dtype(df[col]) or \
            pd.api.types.is_bool_dtype(df[col])
        is_lana_numeric = \
            pd.api.types.is_numeric_dtype(df[col]) and not \
                pd.api.types.is_bool_dtype(df[col])

        if col in id_mappings:
            # the most general branch, that exists in all logs
            semantics += [{
                'name': col,
                'semantic': id_mappings[col],
                'format': None,
                'idx': i}]
        elif col in timestamps_mappings:
            # the second most general branch, Start exists always, Complete sometimes
            semantics += [{
                'name': col,
                'semantic': timestamps_mappings[col],
                'format': time_format,
                'idx': i}]
        else:
            # an optional branch, defined by not being (partially) required and thus inferred
            if is_lana_categorial:
                semantics += [{
                    'name': col,
                    'semantic': 'CategorialAttribute',
                    'format': None,
                    'idx': i}]
            elif is_lana_numeric:
                semantics += [{
                    'name': col,
                    'semantic': 'NumericAttribute',
                    'format': None,
                    'idx': i}]

    return semantics


def create_case_semantics_from_df(df: pd.DataFrame, case_id: str = 'Case_ID') -> List[dict]:
    """
    create case semantics from a pandas data frame

    The columns semantic for lana will be derived from the data frame's dtypes. All types
    will be converted to categorical attributes, besides numbers.
    """

    semantics = []
    id_mappings = {case_id: 'Case ID'}
    for i, col in enumerate(df.columns):
        is_lana_categorial = \
            pd.api.types.is_object_dtype(df[col]) or \
            pd.api.types.is_bool_dtype(df[col])
        is_lana_numeric = \
            pd.api.types.is_numeric_dtype(df[col]) and not \
                pd.api.types.is_bool_dtype(df[col])

        if col in id_mappings:
            semantics += [{
                'name': col,
                'semantic': id_mappings[col],
                'format': None,
                'idx': i}]
        elif is_lana_categorial:
            semantics += [{
                'name': col,
                'semantic': 'CategorialAttribute',
                'format': None,
                'idx': i}]
        elif is_lana_numeric:
            semantics += [{
                'name': col,
                'semantic': 'NumericAttribute',
                'format': None,
                'idx': i}]

    return semantics
