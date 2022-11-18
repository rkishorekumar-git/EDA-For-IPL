import pandas as pd

class Matches:
    def __init__(self, file_name: str) -> None:
        assert isinstance(file_name, str)
        self.file = pd.read_csv(file_name)

    def get_frame(self, cols: list) -> pd.DataFrame:
        assert isinstance(cols, list)
        if set(cols).issubset(self.file.columns):
            return pd.DataFrame(self.file, columns=cols)
        else:
            return -1
