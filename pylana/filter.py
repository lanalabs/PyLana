import time
from dateutil.parser import parse

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
        if type(trace_filter) is list:
            combined_filter += trace_filter
        else:
            combined_filter.append(trace_filter)

    return combined_filter


def create_timespan_filter(start: str, end: str) -> dict:
    """
    Create a timespan filter to be used in a trace filter sequence.

    Args:
        start:
            A string denoting the start timestamp.
        end:
            A string denoting the end timestamp.

    Returns:
        A dictionary containing the filter.
    """
    timespan_filter = {'startInRange': False,
                       'endInRange': False,
                       'type': 'timeRangeFilter',
                       'from': time.mktime(parse(start).timetuple()) * 1000,
                       'to': time.mktime(parse(end).timetuple()) * 1000}

    return timespan_filter


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
    attribute_filter = {
        'type': 'attributeFilter',
        'attributeName': attribute_name,
        'values': values
        }

    return attribute_filter


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
    numeric_attribute_filter = {
        'type': 'numericAttributeFilter',
        'attributeName': attribute_name,
        'min': value_min,
        'max': value_max
        }

    return numeric_attribute_filter


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
    variant_slider_filter = {
        'type': 'variantSliderFilter',
        'min': min_variant_group,
        'max': max_variant_group
        }

    return variant_slider_filter


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
    activity_filter = {
        'type': 'activityFilter',
        'activity': activity,
        'inverted': not include
        }

    return activity_filter


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
    activity_filters = [create_activity_filter(activity) for activity in include] +\
        [create_activity_filter(activity, include = False) for activity in exclude]

    return activity_filters


def create_follower_filter(pre: str, succ: str, direct_follower = False, include = True) -> dict:
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

    follower_filter = {
        'type': 'followerFilter',
        'pre': mapping.get(pre, pre),
        'succ': mapping.get(succ, succ),
        'direct': direct_follower,
        'inverted': not include
    }

    return follower_filter
