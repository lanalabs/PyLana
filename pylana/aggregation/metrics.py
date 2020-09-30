"""
functions to create the aggregation request metric
"""

from typing import Optional, Any

from pylana.aggregation.utils import _raise


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


def create_metric(
        kind: str,
        aggregator: Optional[str] = None,
        percentile: Optional[float] = None) -> dict:
    """
    Create a dictionary containing the metric in a format necessary
    for the aggregation API request.

    Args:
        kind:
            A string denoting the metric to use. For the value
            "frequency", a frequency metric is returned and for "duration" a
            duration metric is returned. Otherwise the value is interpreted
            as a numeric attribute metric. For these metrics and duration
            metrics an aggregator or percentile needs to be passed.
        aggregator:
            An optional string denoting the aggregation function to use.
            Can be one of ["min", "max", "sum", "mean", "median", "variance",
            "standardDeviation"].
        percentile:
            An optional float denoting the percentile to use if instead of
            the available aggregation types listed for aggregation_function
            a percentile aggregation should be used.

    Returns:
        A dictionary containing the metric in the right format for the request.
    """
    return \
        aggregate_summable(create_summable(kind), aggregator, percentile) or \
        create_frequency(kind) or \
        _raise(Exception(f'Impossible to create metric for {kind} without '
                         f'aggregator or percentile.'))
