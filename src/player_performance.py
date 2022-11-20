from load_datasets import deliveries
from batsman_stats import Batsman
import numpy as np

class PlayerPerformance():
    '''
    Class to compute players performance characteristics
    '''

    def __init__(self, player):
        """
        Declare player as a protected variable

        Args:
            player (str): Player name
        """
        self._player = player
        self.valid_years = np.arange(2008, 2018)
        self.batsmen =  deliveries.batsman.unique()

    def get_runs_per_match(self):
        """
        Get runs per match in a given season for the player "self"

        Returns:
            years           (list): list of years batsman played any matches
            runs_all_years  (list): list of list of runs scored in every match played in that year for all years
        """

        if self._player in self.batsmen:
            batsman = Batsman(self._player)

            # Runs per match
            years = []
            runs_all_years = []
            for i in range(len(self.valid_years)):
                batsman_stat = batsman.get_batsman_match_stat(self.valid_years[i])
                game_ids = batsman_stat["match_id"].unique()
                runs = []
                if len(game_ids) > 0:
                    for j in range(len(game_ids)):
                        runs.append(batsman.get_per_match_runs(game_ids[j]))
                    runs_all_years.append(runs)
                    years.append(self.valid_years[i])
        else:
            print("Player Entry not found.")

        return dict(zip(years, runs_all_years))

    def get_player_performance(self):
        """
        Get batsman stats for all years

        Returns:
            (dict): Batsman stats over all seasons zips are a dict with years as keys
        """

        if self._player in self.batsmen:
            batsman = Batsman(self._player)
            years = []
            strike_rate_all_years = []
            max_runs_all_years = []
            average_all_years = []
            total_runs_all_years = []
            for i in range(len(self.valid_years)):
                years.append(self.valid_years[i])
                strike_rate, max_runs, average, total_runs  = batsman.get_batsman_stats(self.valid_years[i])
                strike_rate_all_years.append(strike_rate)
                max_runs_all_years.append(max_runs)
                average_all_years.append(average)
                total_runs_all_years.append(total_runs)
        else:
            print("Player Entry not found.")

        return years, strike_rate_all_years, max_runs_all_years, average_all_years, total_runs_all_years
