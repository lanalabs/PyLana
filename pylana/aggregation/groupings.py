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


def create_grouping(
        kind: str,
        date_type: Optional[str] = None,
        activities: Optional[list] = None,
        attribute: Optional[str] = None
) -> dict:
    return \
        create_by_duration(kind) or \
        create_by_time(kind, date_type) or \
        create_by_activity(kind, activities) or \
        create_by_attribute(kind, attribute) or \
        _raise(Exception(f'Impossible to create grouping for {kind}. Make '
                         f'sure that a valid aggregation type was used and '
                         f'that an attribute was supplied for attribute groupings, '
                         f'a date type was supplied for time groupings or '
                         f'activities were supplied for activity groupings.'))
