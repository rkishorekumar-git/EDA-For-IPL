import numpy as np
from load_datasets import deliveries, matches


class Batsman():
    """
    Batsman class. has all methods and variable for obtaining batsman stats
    """

    def __init__(self, batsman_name):
        """
        Initialize batsman_name and valid years for IPL

        Args:
            batsman_name (str): player name
        """

        assert isinstance(batsman_name, str) 
        self.batsman_name = batsman_name
        self.valid_years = np.arange(2008, 2018)

    def get_batsman_match_stat(self, year):
        """
        Get the batsman statistics for given year.

        Args:
            year (int): Given season to obtains sub dataframe of batsman

        Returns:
            batsman_match_stat (pd.dataFrame): Sub dataframe holding batsman data only for given season
        """

        assert 2008 <= year <= 2017
        match_ids = matches.query(f"season == {year}")["id"]
        batsman_col = deliveries.loc[deliveries["batsman"] == self.batsman_name]
        batsman_match_stat = batsman_col[batsman_col.match_id.isin(list(match_ids))]
        return batsman_match_stat
    
    def get_number_of_games(self, year):
        """
        Get number of games played by batsman in given season

        Args:
            year (int): Given IPl season/ year

        Returns:
            (int): Number of games played by the batsman
        """

        assert 2008 <= year <= 2017
        batsman_stat = self.get_batsman_match_stat(year)
        return batsman_stat["match_id"].nunique()

    def get_match_ids_played(self, year):
        """
        Get match IDs played by batsman in given season

        Args:
            year (int): Given IPl season/ year

        Returns:
            (list): Match IDs the player participated in of the given season.
        """

        assert 2008 <= year <= 2017
        batsman_stat = self.get_batsman_match_stat(year)
        return batsman_stat["match_id"].unique()

    def get_number_of_runs(self, year):
        """
        Get total number of runs scored by the batsman in the given season

        Args:
            year (int): IPL season/ year

        Returns:
            (int): Total runs per season
        """

        assert 2008 <= year <= 2017
        #Get batsman statistics for the season
        batsman_stat = self.get_batsman_match_stat(year)
        return batsman_stat["batsman_runs"].sum()
    
    def get_runs_per_match(self, match_id):
        """
        Get runs scored by the batsman in the given match ID

        Args:
            match_id (int): Match Id of one of the matches he played

        Returns:
            balls_faced (int): total balls faced as a striker in this match
            runs        (int): Total runs scored in this match
        """

        batsman_col = deliveries.loc[deliveries["batsman"] == self.batsman_name]
        batsman_match_id_stat = batsman_col[batsman_col.match_id.isin([match_id])]
        balls_faced = len(batsman_match_id_stat)
        runs = batsman_match_id_stat["batsman_runs"].sum()
        return balls_faced, runs

    def get_average_runs(self, year):
        """
        Get the average runs scored in the season

        Args:
            year (int): IPL season/ year

        Returns:
            (float): Average runs scored by the batsman in the given year. (Rounded to 2 deminals)
        """

        assert 2008 <= year <= 2017
        runs = self.get_number_of_runs(year)
        games = self.get_number_of_games(year)
        return round(runs / games, 2)

    def get_batsman_strike_rate(self, year):
        """
        Get batsman runs for all matches in a given year/ season

        Args:
            year (int): IPL season/ year

        Returns:
            strike_rate (list): Average strike rate of a batsman in a given season
        """

        assert 2008 <= year <= 2017
        batsman_stat = self.get_batsman_match_stat(year)
        game_ids = batsman_stat["match_id"].unique()
        strike_rate = 0
        if len(game_ids) > 0:
            for id in game_ids:
                balls_faced, runs = self.get_runs_per_match(id)
                strike_rate += round((runs / balls_faced)*100, 2)
            strike_rate = strike_rate / len(game_ids)
        return strike_rate

    def get_per_match_runs(self, match_id):
        """
        Get runs scored by a batsman i given match is

        Args:
            match_id (int): Match Id of one of the matches the batsman played

        Returns:
            runs (int): Runs scored by the batsman in given match
        """

        _, runs = self.get_runs_per_match(match_id)
        return runs

    def get_highest_runs(self, year):
        """
        Get the max runs scored by the batsman in a single match in the given season

        Args:
            year (int): IPL season / year

        Returns:
            max_runs (int): Max runs scored in a single match by the batsman
        """

        assert 2008 <= year <= 2017
        batsman_stat = self.get_batsman_match_stat(year)
        game_ids = batsman_stat["match_id"].unique()
        max_runs = 0
        for id in game_ids:
            _, runs = self.get_runs_per_match(id)
            max_runs = max(max_runs, runs)
        return max_runs

    def get_batsman_stats(self, year):
        """
        Get seasonal stats of batsman given year

        Args:
            year (int): IPL season/ year

        Returns:
            strike_rate (float): Strike rate in this season
            max_runs      (int): max runs scored in this season
            average     (float): Batsman average in this season
            total_runs    (int): Total runs scored in this season
        """
        strike_rate = self.get_batsman_strike_rate(year)
        max_runs = self.get_highest_runs(year)
        average = self.get_average_runs(year)
        total_runs = self.get_number_of_runs(year)
        return strike_rate, max_runs, average, total_runs

if __name__ == "__main__":
    batsman_name_1 = "DA Warner"
    batsman_name_2 = "MC Henriques"

    Batsman(batsman_name_1).get_batsman_stats(2009)
