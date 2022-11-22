import pandas as pd
import os
import seaborn as sns
from matplotlib import pyplot as plt
from data_process import Matches


def city_toss_winner(city: str):
    """
    Args:
        city (str): The city name which you want to calculate the probability for toss winner to win

    Returns:
        float float float: win_rate, #win, #competition
    """

    assert isinstance(city, str)

    # load and select specific data
    matches = Matches(file_name="data\matches.csv")
    cols = ['city', 'toss_winner', 'winner']
    df = matches.get_frame(cols=cols)
    df.fillna("missing", inplace=True)

    # check input is valid or not
    cities = set(df['city'])
    if city not in cities:
        print("You enter a city not in our dataset, try again!")
        return -1

    city_df = df.loc[df['city'] == city]

    wr, cn, wn = calculate_wr(city_df=city_df)

    return wr, cn, wn


def calculate_wr(city_df: str):
    """
    Args:
        city_df (str): City name

    Returns:
        float float float: win_rate, #win, #competition
    """
    competition_num = len(city_df)
    win_num = 0
    for row in city_df.iterrows():
        if row[1]['winner'] == "missing":
            competition_num -= 1
            continue
        if row[1]['toss_winner'] == row[1]['winner']:
            win_num += 1
    # print(win_num,competition_num)
    return round(win_num/competition_num, 4), competition_num, win_num


def city_toss_winner_graph():
    
    """
    Draw a bar plot. Y axis is the city name; X axis is the rate that the toss winner win the competition finally
    
    No explicitly input and output!!!
    """
    matches = Matches(file_name="data\matches.csv")
    cols = ['city', 'toss_winner', 'winner']
    df = matches.get_frame(cols=cols)
    df.fillna("missing", inplace=True)

    cities = set(df['city'])

    city_wr_dict = {}

    for city in cities:
        if city == "missing":
            continue

        if city not in city_wr_dict:
            # print(city)
            wr, cn, wn = calculate_wr(df.loc[df['city'] == city])
            city_wr_dict[city] = [wr, wn, cn]

    city_wr_frame = pd.DataFrame.from_dict(
        data=city_wr_dict, orient='index', columns=['win_rate', 'win', 'competition'])
    city_wr_frame.reset_index(inplace=True)
    city_wr_frame.rename(columns={'index': 'city'}, inplace=True)
    city_wr_frame.sort_values(by="win_rate", inplace=True, ascending=False)
    pic = sns.barplot(data=city_wr_frame, x='win_rate', y='city',
                      ci=None, hue_order=city_wr_frame["win_rate"])
    i = 1
    for index, row in city_wr_frame.iterrows():
        pic.text(row['win_rate']+0.01, i-0.6, row['competition'], ha="center")
        pic.text(row['win_rate']+0.04, i-0.6, row['win_rate'], ha="center")
        i += 1
    pic.set_title('City to toss and winner', fontsize=18)
    pic.set_xlabel('Probability of toss winner = winner', fontsize=18)
    pic.set_ylabel('City', fontsize=18)
    plt.show()
    print(city_wr_frame)


if __name__ == "__main__":
    #res = city_toss_winner("Bangalore")

    city_toss_winner_graph()
