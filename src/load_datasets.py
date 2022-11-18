from dataframe import csv_dataset

def load_datasets():
    '''
    Returns each dataset handle
    '''
    matches = csv_dataset("data/matches.csv").d_frame
    deliveries = csv_dataset("data/deliveries.csv").d_frame
    player_auction = csv_dataset("data/IPLPlayerAuctionData.csv").d_frame
    return matches, deliveries, player_auction

matches, deliveries, auction = load_datasets()

#Unit test
if __name__ == "__main__":
    cities = matches["city"]
    print(cities)
    batsman = deliveries["batsman"]
    print(batsman)
    print(auction)