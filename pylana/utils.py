"""
functions to prepare requests for consumption
"""

from collections import defaultdict
from typing import Iterable, Dict, List, Tuple

import pandas as pd


# TODO: check whether this function is actually required
def create_semantics(columns: Iterable[str],
                     case_id: str = "id", action: str = "action", start: str = "start", complete: str = "complete",
                     numerical_attributes: Iterable[str] = tuple(), time_format: str = "yyyy-MM-dd HH:mm:ss") \
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

    semantics = defaultdict(lambda: "CategorialAttribute")

    semantics_fixed = {case_id: "Case ID", action: "Action", start: "Start", complete: "Complete"}
    semantics_numeric = {numeric: "NumericAttribute" for numeric in numerical_attributes}

    semantics.update(semantics_fixed)
    semantics.update(semantics_numeric)

    return [
        {
            "idx": idx,
            "name": col,
            "semantic": semantics[col],
            "format": time_format if semantics[col] in ["Start", "Complete"] else None
        } for idx, col in enumerate(columns)
    ]


def create_event_semantics_from_df(df: pd.DataFrame, time_format: str = "yyyy-MM-dd'T'HH:mm:ss.SSSSSS") -> List[dict]:
    """
    create event semantics from a pandas data frame

    We expect specific names for columns
        * case id column: Case ID
        * activity column: Action
        * first timestamp of activity: Start
        * last timestamp of activity: Complete

    The columns semantic for lana will be derived from the data frame's dtypes. All types
    will be converted to categorical attributes, besides numbers. The Start and Complete
    time stamps need to have the same time format. For an overview over time stamp formats
    see https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html#patterns
    """
    dct_bare = []
    ids = ["Case ID", "Action"]
    timestamps = ["Start", "Complete"]

    for i, col in enumerate(df.columns):

        if col in ids:
            # the most general branch, that exists in all logs
            dct_bare += [{
                'name': col,
                'semantic': col,
                'format': None,
                'idx': i}]
        elif col in timestamps:
            # the second most general branch, Start exists always, Complete sometimes
            dct_bare += [{
                'name': col,
                'semantic': col,
                'format': time_format,
                'idx': i}]
        else:
            # an optional branch, defined by not being (partially) required and thus inferred
            if pd.api.types.is_object_dtype(df[col]):
                dct_bare += [{
                    'name': col,
                    'semantic': 'CategorialAttribute',
                    'format': None,
                    'idx': i}]
            elif pd.api.types.is_numeric_dtype(df[col]):
                dct_bare += [{
                    'name': col,
                    'semantic': 'NumericAttribute',
                    'format': None,
                    'idx': i}]

    return dct_bare


def create_case_semantics_from_df(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[dict]]:
    """
    create case semantics from a pandas data frame

    We expect specific names for columns
        * case id column: Case_ID

    The columns semantic for lana will be derived from the data frame's dtypes. All types
    will be converted to categorical attributes, besides numbers.
    """

    bares = ['Case ID']
    dct_bare = []
    for i in range(0, len(df.columns)):
        col = df.columns[i]
        if pd.api.types.is_object_dtype(df[col]) and col not in bares:
            dct_bare += [{
                'name': col,
                'semantic': 'CategorialAttribute',
                'format': None,
                'idx': i}]
        elif pd.api.types.is_numeric_dtype(df[col]) and col not in bares:
            dct_bare += [{
                'name': col,
                'semantic': 'NumericAttribute',
                'format': None,
                'idx': i}]
        else:
            dct_bare += [{
                'name': col,
                'semantic': col,
                'format': None,
                'idx': i}]

    return dct_bare
