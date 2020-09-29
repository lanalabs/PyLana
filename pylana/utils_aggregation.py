"""
functions to prepare aggregation requests
"""

from typing import Optional, Any


def create_frequency(kind: str) -> dict:
    return {'type': kind} if kind == 'frequency' else dict()


def create_duration(kind: str) -> dict:
    return {'type': kind} if kind == 'duration' else dict()


def create_attribute(att: str) -> dict:
    return {'type': 'attribute',
            'attribute': att} if att not in ['frequency', 'duration'] \
        else dict()


def _is_summable(metric: dict, arg: Any) -> bool:
    return metric and arg and metric.get('type') != 'frequency'


def add_percentile(metric: dict, p: float) -> dict:
    return {
        **metric,
        **{'aggregationFunction': {
            'type': 'percentile',
            'percentile': p
        }
        }
    } if _is_summable(metric, p) else dict()


def add_aggregation(metric: dict, agg: str) -> dict:
    return {
        **metric,
        **{'aggregationFunction': agg}
    } if _is_summable(metric, agg) else dict()


def create_summable(kind):
    return create_duration(kind) or create_attribute(kind)


def aggregate_summable(summable, aggregator, percentile):
    if aggregator and percentile:
        raise Exception('Either aggregator or percentile can be not None, '
                        'not both.')
    return \
        add_aggregation(summable, aggregator) or \
        add_percentile(summable, percentile)


def _raise(exception):
    raise exception


def create_metric(
        kind: str,
        aggregator: Optional[str] = None,
        percentile: Optional[float] = None) -> dict:
    return \
        aggregate_summable(create_summable(kind), aggregator, percentile) or \
        create_frequency(kind) or \
        _raise(Exception(f'Impossible to create metric for {kind} without '
                         f'aggregator or percentile.'))


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
