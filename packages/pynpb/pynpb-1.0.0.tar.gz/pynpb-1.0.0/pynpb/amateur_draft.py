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
    url = f'https://www.baseball-reference.com/bullpen/{year}_NPB_Amateur_Draft'

    response = session.get(url)

    return response.text

def _get_draft_round_names(year: int, html: str) -> List:
    # Get a list of the names of the draft rounds
    soup = BeautifulSoup(html, 'html.parser')

    draft_rounds = soup.find_all('span', class_='mw-headline')
    draft_rounds_list = [draft_round.text for draft_round in draft_rounds]

    return draft_rounds_list

def get_draft_results(year: Optional[int] = None) -> dict:
    """
    Get NPB amateur draft results
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A dict with pandas dataframe with the amateur draft results from the year entered.
    """

    if year is None:
        # If year is none, get most recent season
        year = most_recent_season()
    if year < 1965:
        raise ValueError(
                "This query currently only returns draft results from 1965 and after. "
                "This was the first season where the NPB Amateur Draft took place"
                "Try looking at years from 1965 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    html = _get_html(year)

    # Get the tables for each round and convert to a dict with the identifier being the draft round name
    datasets = pd.read_html(StringIO(html))[0 : len(get_draft_round_names(year, html))]
    datasets = [df.fillna(" ") for df in datasets]

    draft_rounds = {name: df for name, df in zip(get_draft_round_names(year, html), datasets)}

    if len(datasets) == 0:
        # Deal with the case where the season has started or been completed and the amateur draft has not yet taken place
        raise ValueError(
            "No draft results found. Either draft hasn't happened yet or no draft took place this year."
        )

    return draft_rounds

def get_round_results(round: str, year: Optional[int] = None) -> pd.DataFrame:
    """
    Get NPB amateur draft results for the round entered
    
    Parameters
    ----------
    round: str
        A string value representing the round of the draft for which to retrieve data.

    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the amateur draft results from the round and year entered.
    """

    draft_results = get_draft_results(year)

    # Get dataframe for the desired round, if not found, return ValueError
    try:
        round_results = draft_results[round]
    except:
        raise ValueError(
            "Invalid input. Round was not found for desired draft. "
            "To get a list of the draft round names, use the get_draft_round_names function."
        )

    return round_results

def get_draft_results_by_team(team: str, year: Optional[int] = None) -> pd.DataFrame:
    """
    Get NPB amateur draft results for the team entered
    
    Parameters
    ----------
    team: str
        A string value representing the NPB team for which to retrieve data.

    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the amateur draft results for the desired team and year.
    """

    data = get_draft_results(year)

    draft_df = []

    for round_name, df in data.items():
        df['Round'] = round_name
        draft_df.append(df)

    # Get one dataframe with all draft results
    all_draft_results = pd.concat(draft_df, ignore_index = True)

    # Get draft results for team, if not found, return value error and list of team names
    if (len(all_draft_results[all_draft_results['Team'] == team]) > 0):
        return all_draft_results[all_draft_results['Team'] == team]
    else:
        team_names = all_draft_results['Team'].unique().tolist()
        raise ValueError(
            "Invalid input. Team could not be found. "
            "Here is a list of valid inputs, which are all the teams that participated in the draft "
            f"in {year}: {team_names}"
        )