"""
Utility functions for wrangling data. 

"""
import pandas as pd
import numpy as np


def _load_df(team: str, year: int):
    """
    Returns a pandas DataFrame of game results for a given `team` and `year`.

    Credit: Data is retrieved from http://www.basketball-reference.com/

    Parameters
    -----------------
    team (str) - The 3-letter NBA team abbreviation (e.g. Chicago Bulls is 'CHI') 
    year (int) - The year of season. Because a season starts and ends in different years,
                 the year provided is assumed to be the year the season ends. Thus,
                 passing in `2022` retrieves the game results for the 2021-2022 season
    """
    url = 'https://www.basketball-reference.com/teams/{team}/{year}_games.html'.format(
        team=team.upper(), year=str(year))
    df = pd.read_html(url)[0]
    return df


def _clean_df(df: pd.DataFrame):
    """
    Cleans a pandas DataFrame retrieved from the `load_df` function.
    """
    df = pd.DataFrame(df[['Date', 'Opponent', 'Tm', 'Opp', 'Unnamed: 5']])
    # Cleaning the home/away game column ('Unnamed: 5') to something easier to read
    df['Venue'] = df['Unnamed: 5'].apply(lambda x: 'H' if x is np.nan else 'A')
    # The HTML table is such that it shows the column names every 20 rows. We
    # remove the rows where the value is just the column name.
    for col in df.columns:
        df[col] = df[col].loc[df[col] != col]
    return df[['Date', 'Opponent', 'Tm', 'Opp', 'Venue']].dropna()


def get_results(team: str, year: int):
    """
    Returns a pre-processed pandas DataFrame of a given team's results during a given
    season.
    """
    df = _clean_df(_load_df(team, year))
    return df
