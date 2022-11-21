import pandas as pd
import os
import seaborn as sns
from matplotlib import pyplot as plt
from data_process import Matches


def team_toss_winner_graph():
    """
    Draw a bar plot. The Y axis is the team name. 
    The X axis is probabilty the team can win finally when it is the toss winner!!!
    """
    
    # preprocess
    matches = Matches(file_name="data\matches.csv")
    cols = ['toss_winner', 'winner']
    df = matches.get_frame(cols=cols)
    df.fillna("missing", inplace=True)

    team_toss_dict = {}

    # calculate necessary data
    for index, row in df.iterrows():
        if row['winner']=="missing":
            continue
        
        if row['toss_winner'] not in team_toss_dict:
            # toss_winner win, toss_winner, win rate
            team_toss_dict[row['toss_winner']] = [0, 0, 0]

        if row['toss_winner'] == row['winner']:
            team_toss_dict[row['toss_winner']][0] += 1
            team_toss_dict[row['toss_winner']][1] += 1
        else:
            team_toss_dict[row['toss_winner']][1] += 1

    for i in team_toss_dict.keys():
        team_toss_dict[i][2] = round(
            team_toss_dict[i][0]/team_toss_dict[i][1], 4)

    # draw the graph
    team_toss_frame = pd.DataFrame.from_dict(data=team_toss_dict, orient='index', columns=[
                                             'tosswinner_win', 'tosswinner', 'win_rate'])
    team_toss_frame.reset_index(inplace=True)
    team_toss_frame.rename(columns={'index': 'team'}, inplace=True)
    team_toss_frame.sort_values(by="win_rate", inplace=True, ascending=False)
    pic = sns.barplot(data=team_toss_frame, x='win_rate',
                      y='team', ci=None, hue_order=team_toss_frame["win_rate"])
    i = 1
    for index, row in team_toss_frame.iterrows():
        pic.text(row['win_rate']+0.01, i-0.8, row['tosswinner'], ha="center")
        pic.text(row['win_rate']+0.03, i-0.8, row['win_rate'], ha="center")
        i += 1

    pic.set_title('Toss winner to winner', fontsize=18)
    pic.set_xlabel('Probability of toss winner team = winner', fontsize=16)
    pic.set_ylabel('Team', fontsize=16)
    pic.set_xlim(0, 0.8)
    plt.show()
    # print(team_toss_frame)


if __name__ == "__main__":
    team_toss_winner_graph()
