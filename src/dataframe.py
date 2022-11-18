import pandas as pd
import os


class csv_dataset():
    '''
    Helper class to obtain values from the given pandas dataframe
    '''

    def __init__(self, path):
        '''
        path: Path to the csv file
        '''
        assert isinstance(path, str) and os.path.exists(path)
        self.data_path = path
        self.data = pd.read_csv(self.data_path) 

        if 'matches' in path:
            #Drop umpire 3 column as it is empty
            self.data = self.data.drop("umpire3", axis=1)

    @property
    def d_frame(self):
        return self.data

    def get_column_val_by_name(self, column_name):
        '''
        Returns the pd.Series given a name of a column
        '''
        assert isinstance(column_name, str)
        assert column_name in self.data, "Column does not exist in the data frame"
        return self.data[column_name]

    def get_column_val_by_index(self, column_idx):
        '''
        Returns the pd.Series given the index of a column
        '''
        assert isinstance(column_idx, int)
        assert column_idx > len(self.data.columns)
        return self.data[self.data.columns[column_idx]]


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