import numpy as np
from load_datasets import deliveries, matches
import pandas as pd
from matplotlib import pyplot as plt


class Batsman():
    def __init__(self, batsman_name):
        assert isinstance(batsman_name, str) 
        self.batsman_name = batsman_name
        self.valid_years = np.arange(2008, 2018)

    def get_batsman_match_stat(self, year):
        assert 2008 <= year <= 2017
        #Extract given years match IDs
        match_ids = matches.query(f"season == {year}")["id"]
        batsman_col = deliveries.loc[deliveries["batsman"] == self.batsman_name]
        batsman_match_stat = batsman_col[batsman_col.match_id.isin(list(match_ids))]
        return batsman_match_stat
    
    def get_number_of_games(self, year):
        assert 2008 <= year <= 2017
        batsman_stat = self.get_batsman_match_stat(year)
        return batsman_stat["match_id"].nunique()

    def get_match_ids_played(self, year):
        assert 2008 <= year <= 2017
        batsman_stat = self.get_batsman_match_stat(year)
        return batsman_stat["match_id"].unique()

    def get_number_of_runs(self, year):
        assert 2008 <= year <= 2017
        #Get batsman statistics for the season
        batsman_stat = self.get_batsman_match_stat(year)
        number_of_games_played = self.get_number_of_games(year)
        return (number_of_games_played, batsman_stat["batsman_runs"].sum())
    
    def get_runs_per_match(self, match_id):
        batsman_col = deliveries.loc[deliveries["batsman"] == self.batsman_name]
        batsman_match_id_stat = batsman_col[batsman_col.match_id.isin([match_id])]
        overs_faced = len(batsman_match_id_stat)/6
        runs = batsman_match_id_stat["batsman_runs"].sum()
        return overs_faced, runs

    def get_average_runs(self, year):
        assert 2008 <= year <= 2017
        games, runs = self.get_number_of_runs(year)
        return round(runs / games, 2)

    def get_batsman_strike_rate(self, year):
        assert 2008 <= year <= 2017
        batsman_stat = self.get_batsman_match_stat(year)
        game_ids = batsman_stat["match_id"].unique()
        strike_rate = 0
        for id in game_ids:
            overs_faced, runs = self.get_runs_per_match(id)
            strike_rate += round(runs / overs_faced, 2)
        strike_rate = strike_rate / len(game_ids)
        return strike_rate

    def get_per_match_strike_rate(self, match_id):
        overs_faced, runs = self.get_runs_per_match(match_id)
        strike_rate = round(runs / overs_faced, 2)
        return strike_rate

    def get_highest_runs(self, year):
        assert 2008 <= year <= 2017
        batsman_stat = self.get_batsman_match_stat(year)
        game_ids = batsman_stat["match_id"].unique()
        max_runs = 0
        for id in game_ids:
            _, runs = self.get_runs_per_match(id)
            max_runs = max(max_runs, runs)
        return max_runs

    # def compare_batsmen(self, other):
    #     assert isinstance(other, Batsman), "Only two batsmen can be compared"
    #     #Calculate runs scored per year, games played per year and batsman average per year
    #     batsman_runs = [[], []]
    #     batsman_games = [[], []]
    #     batsman_avg_runrate = [[], []]
    #     for i in range(len(self.valid_years)):
    #         year = self.valid_years[i]
    #         num_games_1, runs_1 = self.get_number_of_runs(year)
    #         num_games_2, runs_2 = other.get_number_of_runs(year)
    #         b1_avg_runrate = self.get_batsman_runrate(year)
    #         b2_avg_runrate = other.get_batsman_runrate(year)
    #         batsman_runs[0].append(runs_1)
    #         batsman_games[0].append(num_games_1)
    #         batsman_avg_runrate[0].append(b1_avg_runrate)
    #         batsman_runs[1].append(runs_2)
    #         batsman_games[1].append(num_games_2)
    #         batsman_avg_runrate[1].append(b2_avg_runrate)

    #     runs_combined = np.array(list(zip(batsman_runs[0], batsman_runs[1])))
    #     games_combined = np.array(list(zip(batsman_games[0], batsman_games[1])))
    #     average_combined = np.array(list(zip(batsman_avg_runrate[0], batsman_avg_runrate[1])))
    #     return runs_combined, games_combined, average_combined

    def get_batsman_stats(self, year):
        strike_rate = self.get_batsman_strike_rate(year)
        max_runs = self.get_highest_runs(year)
        avg_runs = self.get_average_runs(year)
        _, total_runs = self.get_number_of_runs(year)
        return {"strike_rate": strike_rate, "max_runs": max_runs, "avg_runs": avg_runs, "total_runs": total_runs}

if __name__ == "__main__":
    batsman_name_1 = "DA Warner"
    batsman_name_2 = "MC Henriques"

    #print(Batsman(batsman_name_1).compare_batsmen(Batsman(batsman_name_2)))

# BATSMAN


# BATSMAN PERSONAL STATS
#       Strike rate per season - year  
#       Average runs per season - year (COMBINE THESE THREE) -> PLOT STRIKE RATE AND AVERAGE AS LINEPLOT and BAR PLOT FOR TOTAL RUNS
#       Total runs in a season - year

# COMPARISON BETWEEN BATSMEN
# Runs per match - match_id (Violin plot)

# BATSMAN STATS AGAINST OPPONENTS
# Scores against each team by a batsman


# OTHERS
# Max runs in per season - year  (LINEPLOT FROM SEABORN) -> NO
# Games played as a batsman - year
# Average and strike rate of a batsman in the first and second half of the season - yearly

