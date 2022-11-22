import numpy as np
from dataframe import csv_dataset
import pandas as pd
from matplotlib import pyplot as plt


class Bowler():
    '''
    Helper class to extract information related to bowlers
    Match information has been extracted from "matches.csv"
    Bowler information has been extracted from "deliveries.csv"
    '''
    def __init__(self, bowler_name, match_dataframe, deliveries_dataframe):
        '''
        Constructor of the class
        Inputs:
        bowler_name: Name of the bowler whose information is to be extracted
        match_dataframe: Dataframe containing match IDs
        deliveries_dataframe: Data containing bowler information for the given match_ids
        '''
        assert isinstance(bowler_name, str) and isinstance(deliveries_dataframe, pd.DataFrame) \
            and isinstance(match_dataframe, pd.DataFrame)
        self.bowler_name = bowler_name
        self.data = deliveries_dataframe
        self.match_data = match_dataframe
        self.valid_years = np.arange(2008, 2018)

    def get_bowler_match_stat(self, year):
        '''
        This method fetches the bowler information fiven a match id
        Input:
        year: Season for which the given bowler's details need to be extracted
        Return:
        bowler_match_stat: Statistics of the given bowler for the mentioned season
        '''
        assert 2008 <= year <= 2017
        #Extract IDs
        match_ids = self.match_data.query(f"season == {year}")["id"]
        bowler_col = self.data.loc[self.data["bowler"] == self.bowler_name]
        bowler_match_stat = bowler_col[bowler_col.match_id.isin(list(match_ids))]
        return bowler_match_stat
    
    def get_number_of_games(self, year):
        '''
        Method to fetch the total number of games played by a bowler in the given season
        Input:
        year: Season for which the number of games played by the bowler needs to be fetched
        Return:
        Number of games played by the given bowler, match_id is used as the identifier
        '''
        assert 2008 <= year <= 2017
        bowler_stat = self.get_bowler_match_stat(year)
        return bowler_stat["match_id"].nunique()

    def get_number_of_runs(self, year):
        '''
        Method to return the total number of runs conceeded by the bowler in a given year
        Input:
        year: Season for which the total runs conceeded needs to be fetched
        Return:
        Tuple containing number of games played and total runs conceeded by the bowler
        '''
        assert 2008 <= year <= 2017
        #Get bowler's statistics for the season
        bowler_stat = self.get_bowler_match_stat(year)
        number_of_games_played = self.get_number_of_games(year)
        return (number_of_games_played, bowler_stat["total_runs"].sum())
    
    def get_average_runs(self, year):
        '''
        Function to return the average runs conceeded per match in a given season by the given bowler
        Input:
        year: Season to calculate the average number of years
        Return:
        Total number of runs/total number of games played in the given season
        '''
        assert 2008 <= year <= 2017
        games, runs = self.get_number_of_runs(year)
        return round(runs / games, 2)

    def compare_bowlers(self, other):
        '''
        Method that returns comparison between two bowlers
        Input:
        other: Instance of another bowler for type Bowler
        Return:
        Runs conceeded, games played and average runs per match by the two bowlers
        '''
        #Calculate runs conceived per year and games played per year
        assert isinstance(other, Bowler)
        bowler_1_runs, bowler_2_runs = [], []
        bowler_1_games, bowler_2_games = [], []
        for year in self.valid_years:
            num_games_1, runs_1 = self.get_number_of_runs(year)
            num_games_2, runs_2 = other.get_number_of_runs(year)
            bowler_1_runs.append(runs_1)
            bowler_2_runs.append(runs_2)
            bowler_1_games.append(num_games_1)
            bowler_2_games.append(num_games_2)

        runs_combined = np.array(list(zip(bowler_1_runs, bowler_2_runs)))
        games_combined = np.array(list(zip(bowler_1_games, bowler_2_games)))
        # return runs_combined, games_combined
        
        #Calculate bowling average per year
        bowler_1_avg, bowler_2_avg = [], []
        for year in self.valid_years:
            b1_avg = self.get_average_runs(year)
            b2_avg = other.get_average_runs(year)
            bowler_2_avg.append(b2_avg)
            bowler_1_avg.append(b1_avg)
        average_combined = np.array(list(zip(bowler_1_avg, bowler_2_avg)))
        return runs_combined, games_combined, average_combined


