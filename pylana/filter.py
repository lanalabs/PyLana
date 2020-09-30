"""
functions to create and combine trace filters
"""

from dateutil.parser import parse
from collections.abc import Iterable


def combine_filters(*filters) -> list:
    """
    Create a list of combined filters.

    Args:
        *filters:
            Filter arguments to be combined into a trace filter sequence. They
            can be either a single filter as a dictionary or multiple filters in
            a list.

    Returns:
        A list containing the combined filters.
    """
    combined_filter = []

    for trace_filter in filters:
        if isinstance(trace_filter, Iterable):
            combined_filter += trace_filter
        else:
            combined_filter += [trace_filter]

    return combined_filter


def create_timespan_filter(start: str, end: str) -> dict:
    """
    Create a timespan filter to be used in a trace filter sequence.

    Args:
        start:
            A string denoting the start timestamp. The local time is used,
            it is recommended to use ISO-8601 date time formats (e.g.
            'YYYY-MM-DDThh:mm:ss'), but every format that dateutil can parse
            works.
        end:
            A string denoting the end timestamp. The local time is used,
            it is recommended to use ISO-8601 date time formats (e.g.
            'YYYY-MM-DDThh:mm:ss'), but every format that dateutil can parse
            works.

    Returns:
        A dictionary containing the filter.
    """
    return {
        'startInRange': False,
        'endInRange': False,
        'type': 'timeRangeFilter',
        'from': parse(start).timestamp() * 1000,
        'to': parse(end).timestamp() * 1000
    }


def create_attribute_filter(attribute_name: str, values: list) -> dict:
    """
    Create a categorical attribute filter to be used in a trace filter sequence.

    Args:
        attribute_name:
            A string denoting the name of the attribute.
        values:
            A list of values to be filtered.

    Returns:
        A dictionary containing the filter.
    """
    return {
        'type': 'attributeFilter',
        'attributeName': attribute_name,
        'values': values
    }


def create_numeric_attribute_filter(attribute_name: str, value_min: float, value_max: float) -> dict:
    """
    Create a numeric attribute filter to be used in a trace filter sequence.

    Args:
        attribute_name:
            A string denoting the name of the attribute.
        value_min:
            An integer or float denoting the minimum value.
        value_max:
            An integer or float denoting the maximum value.

    Returns:
        A dictionary containing the filter.
    """
    return {
        'type': 'numericAttributeFilter',
        'attributeName': attribute_name,
        'min': value_min,
        'max': value_max
    }


def create_variant_slider_filter(min_variant_group: int, max_variant_group: int) -> dict:
    """
    Create a variant slider filter to be used in a trace filter sequence.

    Args:
        min_variant_group:
            An integer denoting the variant group on the lower bound.
        max_variant_group:
            An integer denoting the variant group on the upper bound.

    Returns:
        A dictionary containing the filter.
    """
    return {
        'type': 'variantSliderFilter',
        'min': min_variant_group,
        'max': max_variant_group
    }


def create_activity_filter(activity: str, include: bool = True) -> dict:
    """
    Create an activity filter to be used in a trace filter sequence.

    Args:
        activity:
            A string denoting the activity to filter.
        include:
            A boolean denoting if the activity should be included or excluded.

    Returns:
        A dictionary containing the filter.
    """
    return {
        'type': 'activityFilter',
        'activity': activity,
        'inverted': not include
    }


def create_activity_filters(include: list, exclude: list = []) -> list:
    """
    Create a list of activity filters to be used in a trace filter sequence.

    Args:
        include:
            A list of strings denoting the activities to include.
        exclude:
            A list of strings denoting the activities to exclude.

    Returns:
        A list containing the activity filters.
    """
    return [create_activity_filter(activity) for activity in include] + \
           [create_activity_filter(activity, include=False) for activity in exclude]


def create_follower_filter(pre: str, succ: str, direct_follower=False, include=True) -> dict:
    """
    Create a follower filter to be used in a trace filter sequence.

    Args:
        pre:
            A string denoting the predecessor activity of the follower relation.
        succ:
            A string denoting the successor activity of the follower relation.
        direct_follower:
            A boolean denoting if the activities have to directly
            follow each other.
        include:
            A boolean denoting if the follower relation should be included
            or excluded.

    Returns:
        A list containing the activity filters.
    """
    mapping = {'Start': '__LANA_START__', 'End': '__LANA_END__'}

    return {
        'type': 'followerFilter',
        'pre': mapping.get(pre, pre),
        'succ': mapping.get(succ, succ),
        'direct': direct_follower,
        'inverted': not include
    }
