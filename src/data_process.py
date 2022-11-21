import pandas as pd


class Matches:
    """
    The class is aim for some basic data processing and fetch specific data from the data set
    """
    def __init__(self, file_name: str) -> None:
        """
        construct function

        Args:
            file_name (str): dataset's file name
        """
        assert isinstance(file_name, str)
        self.file = pd.read_csv(file_name)

    def get_frame(self, cols: list) -> pd.DataFrame:
        """
        Fetch specific data from dataset

        Args:
            cols (list): fetch specific columns from dataset

        Returns:
            pd.DataFrame: return colums if column names in cols exist; else return -1
        """
        assert isinstance(cols, list)
        if set(cols).issubset(self.file.columns):
            return pd.DataFrame(self.file, columns=cols)
        else:
            return -1
