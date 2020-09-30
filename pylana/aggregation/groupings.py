"""
functions to create the aggregation request grouping
"""

from typing import Optional

from pylana.aggregation.utils import _raise


def create_by_duration(kind: str) -> dict:
    return {'type': 'byDuration'} if kind == 'byDuration' else dict()


def create_by_time(kind: str, date_type: str) -> dict:
    intervals = ['byYear', 'byMonth', 'byQuarter', 'byDayOfWeek',
                 'byDayOfYear', 'byHourOfDay']
    return {'type': kind,
            'dateType': date_type,
            'timeZone': 'Europe/Berlin'} if kind in intervals and \
                                            date_type in ['startDate',
                                                          'endDate'] else dict()


def create_by_activity(kind: str, activities: list) -> dict:
    return {'type': 'byActivity',
            'selectedActivities': activities} if kind == 'byActivity' and \
                                                 activities else dict()


def create_by_attribute(kind: str, attribute: str) -> dict:
    return {'type': kind,
            'attribute': attribute} if kind == 'byAttribute' and \
                                       attribute is not None else dict()


def create_by_with_params(
        kind: str,
        date_type: str,
        activities: list,
        attribute: str) -> dict:
    if [date_type, activities, attribute].count(None) < 2:
        raise Exception('Only one of date_type, activities and attribute can '
                        'be set, not more.')
    return \
        create_by_time(kind, date_type) or \
        create_by_activity(kind, activities) or \
        create_by_attribute(kind, attribute)


def create_grouping(
        kind: str,
        date_type: Optional[str] = None,
        activities: Optional[list] = None,
        attribute: Optional[str] = None
) -> dict:
    """
    Create a dictionary containing the grouping in a format necessary
    for the aggregation API request.

    Args:
        kind:
            A string denoting the kind of grouping to use. For the value
            "byDuration", a duration grouping is returned. For "byAttribute"
            a grouping by a categorical attribute (the variable attribute
            needs to be passed) is returned. For one of ["byYear", "byMonth",
            "byQuarter", "byDayOfWeek", "byDayOfYear","byHourOfDay"] a time
            grouping is returned (date_type also needs to be set). If the
            activity aggregation "byActivity" is used, the activities to
            aggregate over need to be passed as list.
        date_type:
            An optional string denoting the date type to use when a time
            grouping is used. It has to be 'startDate' or 'endDate'.
        activities:
            An optional list denoting the activities to use when grouping
            kind is set to 'byActivity'.
        attribute:
            An optional string denoting the attribute to use when grouping
            kind is set to 'byAttribute'.

    Returns:
        A dictionary containing the grouping in the right format for the request.
    """
    return \
        create_by_duration(kind) or \
        create_by_with_params(kind, date_type, activities, attribute) or \
        _raise(Exception(f'Impossible to create grouping for {kind}. Make '
                         f'sure that a valid aggregation type was used and '
                         f'that an attribute was supplied for attribute groupings, '
                         f'a date type was supplied for time groupings or '
                         f'activities were supplied for activity groupings.'))
