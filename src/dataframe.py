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
        #Drop umpire 3 column as it is empty
        if "matches" in path:
            self.data = self.data.drop("umpire3", axis=1)

    @property
    def d_frame(self):
        '''
        Return the dataframe
        '''
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

#Unit test
if __name__ == "__main__":
    matches_path = "../data/matches.csv"
    deliveries_path = "../data/deliveries.csv"
    dataset = csv_dataset(matches_path)
    data = dataset.d_frame
    cities = data["city"]
    print(cities)


