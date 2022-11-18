import numpy as np
import pandas as pd

class FixDataset():
    def __init__(self, path):
        self.data_path = path
        self.data = pd.read_csv(self.data_path)

    def fix_match_id(self, other, key="id"):
        assert isinstance(key, str) and isinstance(other, FixDataset)

        first_dset = self.data if max(self.data[key]) > min(other.data[key]) else other.data
        second_dset = other.data if max(self.data[key]) > min(other.data[key]) else self.data
        # print(min(second_dset[key]))

        second_dset[key] += max(first_dset[key])
        return second_dset