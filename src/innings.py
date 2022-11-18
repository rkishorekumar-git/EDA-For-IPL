import numpy as np
import pandas as pd
from collections import defaultdict
from matplotlib import pyplot as plt

class Innings(object):
    def __init__(self, data, match_id):
        assert isinstance(data, pd.DataFrame)
        self.data = data
        self.id = match_id
        self.match_deets = self.data.loc[self.data["match_id"] == self.id]

    def get_over_info(self, inning_deets, over):
        over_deets = inning_deets.loc[inning_deets["over"] == over]
        bowler_name = np.unique(over_deets["bowler"])

        runs_conceived = over_deets["total_runs"].sum()
        return bowler_name[0], runs_conceived

    def get_bowling_stat_inning(self, innings):
        assert isinstance(innings, int) and innings in [1, 2]

        bowler_dict = defaultdict(list) #List of bowlers per innings
        inning_deets = self.match_deets.loc[self.data["inning"] == innings]
        overs = np.unique(inning_deets["over"])
        for over in overs:
            bowler, runs = self.get_over_info(inning_deets, over)
            bowler_dict[bowler].append(runs)

        return bowler_dict
    
if __name__ == "__main__":
    data = pd.read_csv("../data/deliveries_2017.csv")
    id = 1
    innings = 1
    game = Innings(data, id)
    bowler_runs_stat = game.get_bowling_stat_inning(innings)
    total_runs = {}
    for key in bowler_runs_stat:
            total_runs[key] = [len(bowler_runs_stat[key]), np.array(bowler_runs_stat[key]).sum()]

    plt.subplots(1, 2, figsize=(10, 5))
    total_overs_list = np.array(list(total_runs.values()))[:, 0]
    total_runs_list = np.array(list(total_runs.values()))[:, 1]
    labels = np.array(list(total_runs.keys()))
    plt.subplot(121)
    plt.title("Total runs conceeded")
    p, tx, autotexts = plt.pie(total_runs_list, labels=labels, autopct="%1.1f%%",)
    for i, a in enumerate(autotexts):
        a.set_text("{}".format(total_runs_list[i]))
    plt.subplot(122)
    plt.title("Number of overs bowled")
    _, _, autotexts = plt.pie(total_overs_list, labels=labels, autopct="")
    for i, a in enumerate(autotexts):
        a.set_text("{}".format(total_overs_list[i]))
    plt.show()  
