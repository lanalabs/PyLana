"""
Functions to preparing requests for consumption.
"""

from typing import Iterable, Dict, List, Optional

import pandas as pd


def _try_to_map(key, value):
    return {key: value} if key is not None else dict()


def create_semantics(columns: Iterable[str],
                     case_id: str = 'id', action: Optional[str] = 'action',
                     start: Optional[str] = 'start', complete: Optional[str] =
                     'complete',
                     numerical_attributes: Iterable[str] = tuple(),
                     impact_attributes: Iterable[str] = tuple(),
                     descriptive_attributes: Iterable[str] = tuple(),
                     time_format: str = 'yyyy-MM-dd HH:mm:ss') -> List[Dict[str, str]]:
    """
    create semantics including numeric and categorical attributes

    Args:
        columns:
            A list of strings representing the column names of the
            table.
        case_id:
            A string representing the column name for the case id.
        action:
            A string representing the column name for the activities
            (optional).
        start:
            A string representing the column name for the start timestamp
            (optional).
        complete:
            A string representing the column name for the complete timestamp
            (optional).
        numerical_attributes:
            A list of strings representing the column names for numerical
            attributes (optional), defaults to empty tuple.
        impact_attributes:
            A list of strings representing the column names for impact
            attributes (optional), defaults to empty tuple.
        descriptive_attributes:
            A list of strings representing  the column names for
            descriptive attributes (optional), defaults to empty tuple.
        time_format:
            A string representing the time format for start and complete
            columns.

    Returns:
        A list of dictionaries representing the semantics.
    """

    semantics_map = {
        **{case_id: 'Case ID'},
        **_try_to_map(action, 'Action'),
        **_try_to_map(start, 'Start'),
        **_try_to_map(complete, 'Complete'),
        **{att: 'NumericAttribute' for att in numerical_attributes},
        **{att: 'DescriptiveAttribute' for att in descriptive_attributes},
        **{att: 'ImpactAttribute' for att in impact_attributes}
    }

    return [
        {
            'idx': idx,
            'name': col,
            'semantic': semantics_map.get(col, 'CategorialAttribute'),
            'format': time_format if col in [start, complete] else None
        } for idx, col in enumerate(columns)
    ]


def _is_lana_numeric(ser):
    return \
        pd.api.types.is_numeric_dtype(ser) and \
        not pd.api.types.is_bool_dtype(ser)


def create_event_semantics_from_df(
        df: pd.DataFrame, case_id: str = 'Case_ID', action: str = 'Action',
        start: str = 'Start', complete: str = 'Complete',
        impact_attributes: Iterable[str] = tuple(),
        descriptive_attributes: Iterable[str] = tuple(),
        time_format: str = "yyyy-MM-dd'T'HH:mm:ss.SSSSSS") -> List[dict]:
    """
    Create event semantics from a pandas data frame.

    The columns semantic for lana will be derived from the data frame's dtypes.
    All types will be converted to categorical attributes, besides numbers,
    impact and descriptive attributes. Descriptive attributes are special
    cases of categorial attributes with the dtype 'object', impact
    attributes are special cases of numerical attributes. Columns with
    either of these semantics can not be inferred. They have to be passed
    to this function.

    The Start and Complete time stamps need to have the same time format.
    For an overview over time stamp formats see
    https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html#patterns

    Args:
        df:
            A data frame representing an event log.
        case_id:
            A string representing the column name for the case id.
        action:
            A string representing the column name for the activity.
        start:
            A string representing the column name for the start timestamp.
        complete:
            A string representing the column name for the complete timestamp.
        impact_attributes:
            A list of strings representing the column names for impact
            attributes.
        descriptive_attributes:
            A list of strings representing the column names for descriptive
            attributes.
        time_format:
            A string representing the time format for start and complete
            columns.

    Returns:
        A list of dictionaries representing the log semantics.
    """
    return create_semantics(
        df.columns,
        case_id,
        action,
        start,
        complete,
        numerical_attributes=[col for col in df.columns
                              if _is_lana_numeric(df.loc[:, col]) and
                              col not in [case_id, action, start, complete]],
        impact_attributes=impact_attributes,
        descriptive_attributes=descriptive_attributes,
        time_format=time_format
    )


def create_case_semantics_from_df(
        df: pd.DataFrame, case_id: str = 'Case_ID',
        impact_attributes: Iterable[str] = tuple(),
        descriptive_attributes: Iterable[str] = tuple()) -> List[dict]:
    """
    Create event semantics from a pandas data frame.

    The columns semantic for lana will be derived from the data frame's dtypes.
    All types will be converted to categorical attributes, besides numbers,
    impact and descriptive attributes. Descriptive attributes are special
    cases of categorial attributes with the dtype 'object', impact
    attributes are special cases of numerical attributes. Columns with
    either of these semantics can not be inferred. They have to be passed
    to this function.

    Args:
        df:
            A data frame representing amn event log.
        case_id:
            A string representing the column name for the case id.
        impact_attributes:
            A list of strings representing the column names for impact
            attributes.
        descriptive_attributes:
            A list of strings representing the column names for descriptive
            attributes.

    Returns:
        A list of dictionaries representing the log semantics.
    """
    return create_semantics(
        df.columns,
        case_id,
        numerical_attributes=[col for col in df.columns
                              if _is_lana_numeric(df.loc[:, col]) and \
                              col != case_id],
        impact_attributes=impact_attributes,
        descriptive_attributes=descriptive_attributes
    )
