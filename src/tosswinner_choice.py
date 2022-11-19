import pandas as pd
import os
import seaborn as sns
from matplotlib import pyplot as plt
from data_process import Matches


def toss_winner_choice_table():
    # preprocess
    matches = Matches(file_name="data\matches.csv")
    cols = ['toss_winner', 'toss_decision', 'winner']
    df = matches.get_frame(cols=cols)
    df.fillna("missing", inplace=True)

    team_choice_dict = {}

    # calculate necessary data
    for index, row in df.iterrows():
        if row['winner'] == "missing":
            continue

        if row['toss_winner'] not in team_choice_dict:
            team_choice_dict[row['toss_winner']] = [0, 0, 0, 0, 0]

        team_choice_dict[row['toss_winner']][4] += 1

        choice = row['toss_decision']
        print(choice)
        if choice == "bat":
            team_choice_dict[row['toss_winner']][0] += 1
            if row['toss_winner'] == row['winner']:
                team_choice_dict[row['toss_winner']][2] += 1

        elif choice == "field":
            team_choice_dict[row['toss_winner']][1] += 1
            if row['toss_winner'] == row['winner']:
                team_choice_dict[row['toss_winner']][3] += 1

    for k in team_choice_dict.keys():
        data_list = team_choice_dict[k]
        if data_list[0] != 0:
            data_list[2] = round(data_list[2]/data_list[0], 4)
            data_list[0] = round(data_list[0]/data_list[4], 4)

        if data_list[1] != 0:
            data_list[3] = round(data_list[3]/data_list[1], 4)
            data_list[1] = round(data_list[1]/data_list[4], 4)

    # draw the graph
    team_choice_frame = pd.DataFrame.from_dict(data=team_choice_dict, orient='index', columns=[
        'toss_decision_bat', 'toss_decision_field', 'choose_bat_win', 'choose_field_win', 'toss_win_num'])

    team_choice_frame = pd.DataFrame(team_choice_frame, columns=[
                                     'toss_decision_bat', 'toss_decision_field', 'choose_bat_win', 'choose_field_win'])

    pic = sns.heatmap(team_choice_frame, annot=True, xticklabels=[
                      "Bat", "Field", "Bat win", "Field win"], cmap="Blues", annot_kws={"fontsize": 15})
    pic.xaxis.tick_top()
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=12)
    plt.show()


if __name__ == "__main__":
    toss_winner_choice_table()
