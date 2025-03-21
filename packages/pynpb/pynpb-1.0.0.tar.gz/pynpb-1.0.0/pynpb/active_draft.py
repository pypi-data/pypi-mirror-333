import requests
import pandas as  pd
from io import StringIO
import numpy as np

from typing import List, Optional

from bs4 import BeautifulSoup
from .utils import most_recent_season
from .data_sources.baseball_reference import baseball_reference_session

session = baseball_reference_session()

def _get_html(year: int) -> str:
    # Pull html from url and return as a string
    url = f'https://www.baseball-reference.com/bullpen/{year}_NPB_Active_draft'

    response = session.get(url)

    return response.text

def get_active_draft_results(year: Optional[int] = None) -> pd.DataFrame:
    """
    Get NPB active draft results
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the active draft results from the year entered.
    """
    if year is None:
        # If year is none, get most recent season
        year = most_recent_season()
    if year < 1965:
        raise ValueError(
                "This query currently only returns draft results from 2022 and after. "
                "This was the first season where the NPB Active Draft took place"
                "Try looking at years from 2022 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    html = _get_html(year)

    # Get first table from the html, which is the active draft results
    draft_df = pd.read_html(StringIO(html))[0]

    if len(draft_df) == 0:
        # Deal with the case where the season has started or been completed and the amateur draft has not yet taken place
        raise ValueError(
            "No draft results found. Either draft hasn't happened yet or no draft took place this year."
        )

    # Drop empty notes column
    draft_df = draft_df.drop('Notes', axis=1)

    return draft_df

