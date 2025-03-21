import requests
from io import StringIO
import pandas as pd

from typing import Optional, List
from .utils import most_recent_season
from .data_sources.baseball_reference import baseball_reference_session

session = baseball_reference_session()

def _get_html(year: int) -> str:
    # if year is before 2007, get data from npb official site, if not use baseball reference
    if year > 2007:
        url = f'https://npb.jp/bis/eng/{year}/standings/'
        response = requests.get(url)
    else:
        url = f'http://www.baseball-reference.com/bullpen/{year}_in_Japanese_Baseball'
        response = session.get(url)

    html = response.text
    return html

def get_pacific_standings(year: Optional[int] = None) -> pd.DataFrame:
    """
    Get pacific league standings
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the pacific league standings from the year entered.
    """

    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    html = _get_html(year)

    # Get table from html code and apply modifications to make it easier to read and use
    if year > 2007:
        pacific_standings = pd.read_html(StringIO(html))[4]
        pacific_standings.columns = pacific_standings.iloc[1]
        pacific_standings = pacific_standings.drop([0, 1])
        pacific_standings = pacific_standings.reset_index(drop=True)
        pacific_standings = _get_full_team_names(pacific_standings, 'pacific', year)

        pacific_standings['G'] = pacific_standings['G'].astype(int)
        pacific_standings['W'] = pacific_standings['W'].astype(int)
        pacific_standings['L'] = pacific_standings['L'].astype(int)
        pacific_standings['T'] = pacific_standings['T'].astype(int)
        pacific_standings['PCT'] = pacific_standings['PCT'].astype(float)
    else:
        pacific_standings = pd.read_html(StringIO(html))[2]
        pacific_standings = pacific_standings.iloc[:, :7]
        pacific_standings.columns = ['Team', 'G', 'W', 'L', 'T', 'PCT', 'GB']
        pacific_standings['GB'] = pacific_standings['GB'].replace({'-.-' : '--'}).astype(str)
        pacific_standings['GB'] = pacific_standings['GB'].replace({'0.0' : '--'}).astype(str)
        pacific_standings['Team'] = pacific_standings['Team'].str.replace('*', '', regex=False)
        
    pacific_standings.index = pacific_standings.index + 1
    pacific_standings.columns.name = 'Pacific Standings'

    return pacific_standings

def get_central_standings(year: Optional[int] = None) -> pd.DataFrame:
    """
    Get central league standings
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the central league standings from the year entered.
    """

    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    html = _get_html(year)

    # Get table from html code and apply modifications to make it easier to read and use
    if year > 2007:
        central_standings = pd.read_html(StringIO(html))[2]
        central_standings.columns = central_standings.iloc[1]
        central_standings = central_standings.drop([0, 1])
        central_standings = central_standings.reset_index(drop=True)
        central_standings = _get_full_team_names(central_standings, 'central', year)

        central_standings['G'] = central_standings['G'].astype(int)
        central_standings['W'] = central_standings['W'].astype(int)
        central_standings['L'] = central_standings['L'].astype(int)
        central_standings['T'] = central_standings['T'].astype(int)
        central_standings['PCT'] = central_standings['PCT'].astype(float)
    else:
        central_standings = pd.read_html(StringIO(html))[1]
        central_standings = central_standings.iloc[:, :7]
        central_standings.columns = ['Team', 'G', 'W', 'L', 'T', 'PCT', 'GB']
        central_standings['GB'] = central_standings['GB'].replace({'-.-' : '--'}).astype(str)
        central_standings['GB'] = central_standings['GB'].replace({'0.0' : '--'}).astype(str)
        central_standings['Team'] = central_standings['Team'].str.replace('*', '', regex=False)
        
    central_standings.index = central_standings.index + 1
    central_standings.columns.name = 'Central Standings'

    return central_standings

def get_all_standings(year: Optional[int] = None) -> List[pd.DataFrame]:
    """
    Get both central league and pacific league standings as seperate dataframes
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A list of pandas dataframes with the central and pacific league standings from the year entered.
    """
    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    datasets = []

    central_standings = get_central_standings(year)
    datasets.append(central_standings)

    pacific_standings = get_pacific_standings(year)
    datasets.append(pacific_standings)

    return datasets


def get_combined_standings(year: Optional[int] = None) -> pd.DataFrame:
    """
    Get overall league standings
    
    Parameters
    ----------
    year: int, optional
        An integer value representing the year for which to retrieve data. If not entered, results from
        most recent season will be retrieved.

    Returns
    -------
    A pandas dataframe with the overall league standings from the year entered.
    """

    if year is None:
        year = most_recent_season()
    if year < 1950:
        raise ValueError(
                "This query currently only returns standings until the 1950 Season. "
                "This was the first season where the Pacific and Central Leagues were created."
                "Try looking at years from 1950 to present."
        )
    if year > most_recent_season():
        raise ValueError(
            "Invalid input. Season for the year entered must have begun. It cannot be greater than the current year."
        )

    central_standings = get_central_standings(year)
    pacific_standings = get_pacific_standings(year)

    overall_standings = pd.concat([central_standings, pacific_standings], axis=0, ignore_index = True)

    # Combine central and pacific standings, and recalculate games behind
    overall_standings = overall_standings.sort_values(by='PCT', ascending=False)
    overall_standings = overall_standings.drop('GB', axis = 1)
    overall_standings['W'] = overall_standings['W'].astype(int)
    overall_standings['L'] = overall_standings['L'].astype(int)
    overall_standings = overall_standings.reset_index(drop=True)
    overall_standings.index = overall_standings.index + 1
    overall_standings.columns.name = 'Overall Standings'

    overall_standings['GB'] = ['--'] + (((overall_standings['W'][1] - overall_standings['L'][1]) - (overall_standings['W'][1:] - overall_standings['L'][1:])) / 2).tolist()

    return overall_standings

def _get_full_team_names(standings: pd.DataFrame, league: str, year: int) -> pd.DataFrame:
    if league == 'pacific':
        standings['Team'] = standings['Team'].replace({'Seibu' : 'Saitama Seibu Lions', 'Orix' : 'Orix Buffaloes', 'Nippon-Ham' : 'Hokkaido Nippon-Ham Fighters',
                                                        'Lotte' : 'Chiba Lotte Marines', 'Rakuten' : 'Tohoku Rakuten Golden Eagles', 'Softbank' :'Fukuoka Softbank Hawks', 'ORIX' : 'Orix Buffaloes' })
    elif league == 'central':
        standings['Team'] = standings['Team'].replace({'Yomiuri' : 'Yomiuri Giants', 'Hanshin' : 'Hanshin Tigers', 'Chunichi' : 'Chunichi Dragons',
                                                        'Hiroshima' : 'Hiroshima Toyo Carp', 'Yakult' : 'Tokyo Yakult Swallows'})
        if year >= 2012:
            standings['Team'] = standings['Team'].replace({'DeNA' : 'Yokohama DeNA BayStars'})
        else:
            standings['Team'] = standings['Team'].replace({'Yokohama' : 'Yokohama BayStars'})
        
    return standings
