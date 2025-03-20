from typing import Optional

import numpy as np
import pandas as pd
from apicutils.basic_io import combine_to_path

feed_cols = ["time", "D", "S1", "S2", "Z", "C", "pH"]

influent_state_units_dict = {
    "time": "Day",
    "D": "Day-1",
    "S1": "gCOD L-1",
    "S2": "mmol L-1",
    "Z": "mmol L-1",
    "C": "mmol L-1",
    "pH": "",
}


class AM2Feed:
    feed_cols = feed_cols
    influent_state_units_dict = influent_state_units_dict

    def __init__(self, df: pd.DataFrame):
        # initialize feed_cols_dict (done here to cover inheritance)
        self.feed_cols_dict = {key: i for i, key in enumerate(self.feed_cols)}

        self.df = df.copy()

    @property
    def np_data(self) -> np.ndarray:
        """Numpy npdarray representation of the data"""
        return self._np_data

    @property
    def n_time(self) -> int:
        return self._df.shape[0]

    @property
    def df(self) -> pd.DataFrame:
        """Pandas dataframe representation of the data"""
        return self._df

    @df.setter
    def df(self, value: pd.DataFrame):
        # Check col names
        unexplained = set(value.columns).symmetric_difference(self.feed_cols)
        if not len(unexplained) == 0:
            raise ValueError(
                f"Passed dataframe has extra/missing columns: {unexplained}"
            )

        time = value["time"].to_numpy()
        if (len(time) > 1) and np.any(time[1:] - time[:-1] <= 0):
            raise ValueError("Time information should be increasing")
        self._df = value[feed_cols]  # Reorder

        self._np_data = self._df.to_numpy()

        # Loop using set_attr would be more concise, but linter would not
        # like it much.
        self._time = self._np_data[:, self.feed_cols_dict["time"]]
        self._D = self._np_data[:, self.feed_cols_dict["D"]]
        self._S1 = self._np_data[:, self.feed_cols_dict["S1"]]
        self._S2 = self._np_data[:, self.feed_cols_dict["S2"]]
        self._Z = self._np_data[:, self.feed_cols_dict["Z"]]
        self._C = self._np_data[:, self.feed_cols_dict["C"]]
        self._pH = self._np_data[:, self.feed_cols_dict["pH"]]

    @property
    def time(self):
        return self._time

    @property
    def D(self):
        return self._D

    @property
    def S1(self):
        return self._S1

    @property
    def S2(self):
        return self._S2

    @property
    def Z(self):
        return self._Z

    @property
    def C(self):
        return self._C

    @property
    def pH(self):
        return self._pH

    def __repr__(self):
        return f"AM2 Feed:\n{self._df.__repr__()}"

    def __str__(self):
        return f"AM2 Feed:\n{self._df.__str__()}"

    def split(self, time_split: float):
        """
        Returns a tuple containing the feed information up to time and the feed information after time.
        Split is done so that the first information can give prediction up to time included.
        """
        time_feed = self._df["time"]
        cond = time_feed < time_split

        feed_before = self._df.loc[cond]
        feed_after = self._df.loc[~cond]
        return (AM2Feed(feed_before), AM2Feed(feed_after))

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save DigesterFeed object to a .csv file"""

        path = combine_to_path(name, "csv", directory)
        self._df.to_csv(path, index=False)
        return path

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        return cls(pd.read_csv(combine_to_path(name, "csv", directory)))
