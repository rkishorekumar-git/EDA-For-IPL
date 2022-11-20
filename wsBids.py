import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import os
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


def parse_web(url, index, ignoreColumn, year, columnHeader, conversion):
    '''
    Using beautiful soup to parse html of a url from web
    Find the tables.
    Since the tables don't have a specific class or id and the column -
        headers may vary I manualy found the index of the tables that -
        display auction information
    Find the Table headers and place them in a list
    Create a pandas DataFrame using the table headers as columns
    Place all the table rows from selected table in the parsed html in to the DataFrame
    Remove any spacing or special characters 
    Remove unnecessary columns
    Change the Name of the columns to be same as other tables
    Change the type of columns as needed
    Convert the money as needed
    Add Year column
    '''
    assert isinstance(url, str)
    assert isinstance(index, int)
    assert isinstance(ignoreColumn, list)
    assert isinstance(year, int)
    assert isinstance(columnHeader, dict)
    assert isinstance(conversion, (int, float))
    assert index >= 0 and year > 2007 and conversion > 0.0
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all("table")
    headers = []
    for th in table[index].find_all('th'):
        title = th.text.strip()
        headers.append(title)

    theTable = pd.DataFrame(columns=headers)
    for tr in table[index].find_all('tr')[1:]:
        rowData = tr.find_all('td')
        row = [elem.text.strip().replace('$', '').replace(',', '')
               for elem in rowData]
        length = len(theTable)
        theTable.loc[length] = row
    theTable = theTable.drop(theTable.columns[ignoreColumn], axis=1)
    theTable = theTable.rename(
        columns=columnHeader)
    theTable["Amount"] = pd.to_numeric(theTable["Amount"])
    theTable['Amount'] = theTable["Amount"].apply(lambda x: x*conversion)
    theTable["Year"] = year
    return theTable


def combine_tables(theTables):
    '''
    Combine all the DataFrames from 2008 to 2012
    Read in csv to DataFrames
    Remove unnecessary columns
    Combine DataFrames to include data from 2008 to 2022
    Write to a new csv file
    '''
    assert isinstance(theTables, list)
    assert all(isinstance(elem, pd.DataFrame) for elem in theTables)
    assert len(theTables) > 0
    theTable08To12 = pd.concat(theTables)
    theTable13_22 = pd.read_csv(
        '/Users/sepehr/Documents/ECE143/Final/IPLPlayerAuctionData13-22.csv')
    theTable13_22 = theTable13_22.drop(theTable13_22.columns[[1, 5]], axis=1)
    theTable = pd.concat([theTable08To12, theTable13_22])
    theTable["Amount"] = pd.to_numeric(theTable["Amount"])
    theTable['Amount'] = theTable["Amount"].apply(lambda x: x//81.53).round(-3)
    theTable.loc[theTable['Team'] ==
                 'Pune Warriors India', 'Team'] = 'Pune Warriors'
    thePath = os.getcwd() + '/IPL Player Auction 08-22.csv'
    theTable.to_csv(thePath, index=False)
    return theTable


table2008 = parse_web("https://en.wikipedia.org/wiki/List_of_2008_Indian_Premier_League_auctions_and_personnel_signings",
                      2, [0, 1, 3, 4, 5], 2008, {"Name": "Player", "Auctioned Price(in US$ thousands)": "Amount"}, 81525)

table2009 = parse_web("https://en.wikipedia.org/wiki/List_of_2009_Indian_Premier_League_personnel_changes",
                      7, [0, 4], 2009, {"Winning bid": "Amount"}, 81.53)

table2010 = parse_web("https://en.wikipedia.org/wiki/List_of_2010_Indian_Premier_League_personnel_changes",
                      0, [3], 2010, {"Franchise": "Team", "Sold price (USD)": "Amount"}, 81.53)

table2011 = parse_web("https://en.wikipedia.org/wiki/List_of_2011_Indian_Premier_League_personnel_changes",
                      2, [0, 4], 2011, {"Winning bid": "Amount"}, 81.53)

table2012 = parse_web("https://en.wikipedia.org/wiki/List_of_2012_Indian_Premier_League_personnel_changes",
                      9, [0, 3], 2012, {"Winning bid": "Amount"}, 81.53)

theTable = combine_tables(
    [table2008, table2009, table2010, table2011, table2012])

matches = pd.read_csv('data/matches.csv')
matches = matches.drop(
    matches.columns[[0, 2, 3, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17]], axis=1)
matches = matches.rename(columns={"season": "Year", "winner": "Winner",
                                  "player_of_match": "MVP", "team1": "Team1", "team2": "Team2"})


totalBidYr = []
for elem in matches["Team1"].unique():
    yearbid = []
    for year in range(8, 17):
        yearbid.append(sum(theTable[(theTable['Year'] == (
            2000+year)) & (theTable['Team'] == elem)]['Amount'].tolist()))
    totalBidYr.append(yearbid)

totalWLYr = []
for elem in matches["Team1"].unique():
    winLossYr = []
    for year in range(8, 17):
        gamesYr = matches[(matches['Year'] == (2000+year)) & ((matches['Team1']
                                                               == elem) | (matches['Team2'] == elem))]["Winner"].tolist()
        occuranceYr = gamesYr.count(elem)
        # print(len(gamesYr), occuranceYr, elem, year)
        # if len(gamesYr) > 0:
        #     if (occuranceYr/(len(gamesYr) - occuranceYr)) >= 1:
        #         winLossYr.append(1)
        #     else:
        #         winLossYr.append(-1)
        # else:
        #     winLossYr.append(0)
        if len(gamesYr) > 0:
            winLossYr.append((occuranceYr/(len(gamesYr) - occuranceYr)))
        else:
            winLossYr.append(np.nan)  # np.nan or -1
    totalWLYr.append(winLossYr)

# sum of bids per year for each team until 2016
totalBidMat16 = np.array([np.array(xi) for xi in totalBidYr])
# Win Loss ration for each team per year until 2016
totalWLMat = np.array([np.array(xi) for xi in totalWLYr])

years = []
for elem in range(len(matches["Year"].unique().tolist())):
    years.append(matches["Year"].unique()[elem].astype(str))

totalBidPerYear16 = pd.DataFrame(totalBidMat16, columns=years, index=[
                                 matches["Team1"].unique()])
# dataframe of sum of bids until 2016
winLossPerYear = pd.DataFrame(totalWLMat, columns=years, index=[
                              matches["Team1"].unique()])
# dataframe win loss ratio until 2016

thePath = os.getcwd() + '/auctionSpending.csv'
totalBidPerYear16.to_csv(thePath, index=True)
thePath = os.getcwd() + '/IwinLossRatio.csv'
winLossPerYear.to_csv(thePath, index=True)

plt.plot((winLossPerYear.corrwith(totalBidPerYear16, axis=0).to_numpy()), 'o')
plt.plot((winLossPerYear.corrwith(totalBidPerYear16, axis=1).to_numpy()), 'o')
plt.plot(matches["Year"].unique(), winLossPerYear.corrwith(
    totalBidPerYear16, axis=0).to_numpy())

allTeamWLRatio = []
for i in range(len(years)):
    allTeamWLRatio.append(sum(winLossPerYear[winLossPerYear[years[i]].notna(
    )][years[i]].to_numpy())/winLossPerYear.count()[i])
allTeamBidYear = []
for i in range(len(years)):
    allTeamBidYear.append(sum(totalBidPerYear16[years[i]].to_numpy()))
plt.plot(allTeamBidYear, allTeamWLRatio, 'o')  # spending to win/ratio
