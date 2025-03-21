from collections import namedtuple
from datetime import date, datetime, timedelta
import functools
import io
from typing import Dict, Iterator, Optional, Tuple, Union
import zipfile

import pandas as pd
import requests

DATE_FORMAT = "%Y-%m-%d"

@ functools.lru_cache()
def most_recent_season() -> int:
    """
    Find the most recent season. This will either be this year if the season has started or last year
    if the current season has not yet started 

    Parameters
    ----------

    Returns
    -------
    Returns an integer for the most recent season
    """

    recent_season_dates = date_range(
        (datetime.today() - timedelta(weeks=52)).date(),
        datetime.today().date(),
        verbose=False,
    )

    return list(recent_season_dates)[-1][0].year


def date_range(start: date, stop: date, step: int = 1, verbose: bool = True) -> Iterator[Tuple[date, date]]:
    """
    Iterate over dates. Skip the offseason dates. Returns a pair of dates for beginning and end of each segment.
    Range is inclusive of the stop date.
    If verbose is enabled, it will print a message if it skips offseason dates.

    Parameters
    ----------

    Returns
    -------
    Returns a range of dates in the form of a tuple
    """

    low = start

    while low <= stop:
        if (low.month, low.day) < (3, 23):
            low = low.replace(month=3, day=23)
            if verbose:
                print("Skipping offseason dates")
        elif (low.month, low.day) > (11, 15):
            low = low.replace(month=3, day=15, year=low.year + 1)
            if verbose:
                print("Skipping offseason dates")

        if low > stop:
            return
        high = min(low + timedelta(step - 1), stop)
        yield low, high
        low += timedelta(days=step)