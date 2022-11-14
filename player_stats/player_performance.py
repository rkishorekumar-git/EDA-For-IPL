from src.dataframe import deliveries

class PerformanceClassifier():
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

    def get_batsman_stats(self):
        """
        Compute batsman statistics from the data in deliveries.csv

        Returns:
            (dict): Dictionary of batsman statistics
                matches_played, overs_faced, run_rate, dismissals
        """
        player_dataset = deliveries.loc[deliveries['batsman'] == self._player]
        matches_played = player_dataset['match_id'].nunique()
        run_rate = 0
        if matches_played:
            runs = sum(player_dataset['batsman_runs'])
            overs_faced = len(player_dataset)/6
            run_rate = runs/overs_faced
            dismissals = len(player_dataset['player_dismissed'].dropna())
        return {"matches_played": matches_played, "overs_faced": overs_faced, "run_rate": run_rate, "dismissals": dismissals}

    def get_bowler_stats(self):
        """
        Compute bowler statistics from the data in deliveries.csv

        Returns:
            (dict): Dictionary of batsman statistics
                matches_played, overs_bowled, economy, wickets_taken
        """
        player_dataset = deliveries.loc[deliveries['bowler'] == self._player] 
        matches_played = player_dataset['match_id'].nunique()
        economy_rate = 0
        wickets_taken = 0
        if matches_played:
            overs_bowled = len(player_dataset)/6
            runs = sum(player_dataset['batsman_runs']) + sum(player_dataset['extra_runs'])
            economy_rate = runs/ overs_bowled
            wickets_taken = len(player_dataset.loc[player_dataset['dismissal_kind'].isin(['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket'])])

        return {"matches_player": matches_played, "overs_bowled": overs_bowled, "economy_rate": economy_rate, "wickets_taken": wickets_taken}

# List of all bowlers and batsmen 
bowlers = deliveries.bowler.unique()
batsmen =  deliveries.batsman.unique()

i = 0
batsmen_stats = dict()
bowlers_stats = dict()

# Fetch stats for all players
for i in range(max(len(bowlers), len(batsmen))):
    if i < len(batsmen):
        batsmen_stats[batsmen[i]] = PerformanceClassifier(batsmen[i]).get_batsman_stats()
    if i < len(bowlers):
        bowlers_stats[bowlers[i]] = PerformanceClassifier(bowlers[i]).get_bowler_stats()

# Print Performance Stats
print(batsmen_stats, bowlers_stats)

# To-Do:
# How can the stats be stored? Dataframe/ dict
# Ideas for visualizing this set? For run_rate, dismissal_rate, economy_rate and wickets taken plot a dotted graph.
# Say that the lower half are unlikely to be chosen in coming seasons.
# If a player os under both sections - rate them as all rounder, plot a graph for that player and show if he has more potential as a batter/ bowler
# Verify how this player was mostly used as, see the number of overs bowled vs num of overs faced.


# Further, per match analysis can be done to predict man of the match
