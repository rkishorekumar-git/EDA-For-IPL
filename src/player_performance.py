from load_datasets import deliveries
from bowler_stats import Bowler
from batsman_stats import Batsman
from matplotlib import pyplot as plt
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
        # List of all bowlers and batsmen 
        # self.bowlers = deliveries.bowler.unique()
        self.batsmen =  deliveries.batsman.unique()

    def get_strike_rate_per_match(self):
        if self._player in self.batsmen:
            batsman = Batsman(self._player)

            # Strike rate per match
            year = []
            strike_rate_years = []
            for i in range(len(self.valid_years)):
                year.append(self.valid_years[i])
                batsman_stat = batsman.get_batsman_match_stat(self.valid_years[i])
                game_ids = batsman_stat["match_id"].unique()
                strike_rate = []
                for j in range(len(game_ids)):
                    strike_rate.append(batsman.get_per_match_strike_rate(game_ids[j]))
                strike_rate_years.append(strike_rate)
        else:
            print("Player Entry not found.")
        return dict(zip(year, strike_rate_years))

    def get_player_performance(self):
        if self._player in self.batsmen:
            batsman = Batsman(self._player)
            year = []
            batsman_stats = []
            for i in range(len(self.valid_years)):
                year.append(self.valid_years[i])
                stats = batsman.get_batsman_stats(self.valid_years[i])
                batsman_stats.append(stats)
        else:
            print("Player Entry not found.")
        return dict(zip(year, batsman_stats))

batsman_1_name = "MS Dhoni"
player = PlayerPerformance(batsman_1_name)
print("strike rate:",player.get_strike_rate_per_match()) # { year: [per match strike rate ]}
print("other stats:",player.get_player_performance()) # { year: {overall_strike_rate, max_runs, avg_runs, total_runs}}

