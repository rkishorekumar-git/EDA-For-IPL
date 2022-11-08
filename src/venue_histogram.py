import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sb
from dataframe import csv_dataset

def get_city_count(data, venue, year):
    '''
    Method to count the number of matches played in a particular venue given a year
    venue: Name of the stadium where the game was played
    year: Parameter to provide information about which year to count the matches in a venue
    bypass: When True, calculates the overall venue histogram
    '''
    assert isinstance(venue, str) and isinstance(year, int), "Type error"
    assert isinstance(data, pd.DataFrame)
    year_list = [i for i in range(2008, 2017)]
    assert year in year_list, "Out of dataset value"
    
    count = 0
    data = data[["season", "venue"]]
    venue_list = data.loc[data["season"] == year]
    count = venue_list.loc[venue_list["venue"] == venue].count()
    return count["venue"]

def get_line_plot(data, venue, year_list):
    assert isinstance(data, pd.DataFrame) and isinstance(year_list, list)
    count = {}
    for year in year_list:
        count[year] = get_city_count(data, venue, year)
    df = pd.DataFrame(count.items(), columns=["Year", "Number of matches played"])
    df = df.set_index("Year")
    plt.figure(figsize=(6, 6))

    sb.lineplot(df, x="Year", y="Number of matches played", markers=True)
    plt.ylim(0, 10)
    plt.show()

def get_line_plot_all_venues(data):
    assert isinstance(data, pd.DataFrame)
    df = data.groupby(["season", "venue"]).count().reset_index()
    df = pd.DataFrame(df, columns=["season", "venue", "id"]).rename(columns={"id":"count"})
    ax = sb.lineplot(df, x="season", y="count", hue="venue", markers=True)

    plt.show()
    # plt.plot(count.keys(), count.values())
    # plt.show()


if __name__ == "__main__":
    path = "../data/matches.csv"
    dataset = csv_dataset(path)
    data = dataset.d_frame
    venue = "Rajiv Gandhi International Stadium, Uppal"
    year  = [i for i in range(2008, 2017)]
    get_line_plot(data, venue, year)


