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
    matches = Matches(file_name="../data/matches.csv")
    cols = ['toss_winner', 'winner']
    df = matches.get_frame(cols=cols)
    df.fillna("missing",inplace=True)
    
    team_toss_dict={}
    
    for index,row in df.iterrows():
        if row['toss_winner'] not in team_toss_dict:
            team_toss_dict[row['toss_winner']]=[0,0,0] #toss_winner win, toss_winner, win rate
        
        if row['toss_winner']==row['winner']:
            team_toss_dict[row['toss_winner']][0]+=1
            team_toss_dict[row['toss_winner']][1]+=1
        else:
            team_toss_dict[row['toss_winner']][1]+=1
    
    for i in team_toss_dict.keys():
        team_toss_dict[i][2]=round(team_toss_dict[i][0]/team_toss_dict[i][1],4)
            
            
    team_toss_frame = pd.DataFrame.from_dict(data=team_toss_dict,orient='index',columns=['tosswinner_win','tosswinner','win_rate'])
    team_toss_frame.reset_index(inplace=True)
    team_toss_frame.rename(columns={'index': 'team'},inplace=True)
    team_toss_frame.sort_values(by="win_rate",inplace=True,ascending=False)
    pic=sns.barplot(data=team_toss_frame,x='win_rate',y='team',errorbar=None,hue_order=team_toss_frame["win_rate"])
    #sns.set(rc={'figure.figsize':(8.7,11.27)}) #The graph size may not fit your computer or screen, feel free to change it!
    i=1
    for index,row in team_toss_frame.iterrows():
        pic.text(row['win_rate']+0.01,i-0.8,row['tosswinner'],ha="center")
        pic.text(row['win_rate']+0.03,i-0.8,row['win_rate'],ha="center")
        i+=1
    
    #Feel free to change the settings below!
    pic.set_title('Toss winner to winner',fontsize=18)
    pic.set_xlabel('Probability of toss winner team = winner',fontsize=16)
    pic.set_ylabel('Team',fontsize=16)
    
    pic.set_xlim(0,0.8) 
    plt.subplot(111)
    plt.show()
    
def toss_winner_choice_table():
    """
    Draw a heat map with four colums.
    1st column: The probabilty that toss winner choose to bat
    2nd column: The probabilty that toss winner choose to field
    3rd column: The probabilty that toss winner choose to bat win the competition finally
    4th column: The probabilty that toss winner choose to field win the competition finally
    """
    # preprocess
    matches = Matches(file_name="../data/matches.csv")
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
        #print(choice)
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
    #sns.set(rc={'figure.figsize':(8.7,11.27)})
    
    # Feel free to change the settings!
    pic.xaxis.tick_top()
    plt.subplot(111)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=12)
    plt.show()


