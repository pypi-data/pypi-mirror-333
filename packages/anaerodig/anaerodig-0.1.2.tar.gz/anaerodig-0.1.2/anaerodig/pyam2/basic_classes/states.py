# import warnings
from copy import deepcopy
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from apicutils.basic_io import combine_to_path, rw_jsonlike

state_col = [
    "X1",
    "X2",
    "S1",
    "S2",
    "Z",
    "C",
]

states_col = ["time"] + state_col + ["qm", "qc"]

state_units_dict = {
    "time": "Day",
    "X1": "gVS L-1",  # conc. acidogenic bacteria
    "X2": "gVS L-1",  # conc. methanogenic bacteria
    "S1": "gCOD L-1",  # conc. substrate
    "S2": "mmol L-1",  # conc. VFA
    "Z": "mmol L-1",  # tot. alkalinity
    "C": "mmol L-1",  # tot. inorg carbon conc.
    "qm": "mmol L-1 Day-1",  # Noted as mM in Hassam, check
    "qc": "mmol L-1 Day-1",  # carbon dioxide flow
}

states_col_dict = {name: i for i, name in enumerate(states_col)}


class AM2States:
    states_col = states_col

    def __init__(self, df: pd.DataFrame):
        self.states_col_dict = {name: i for i, name in enumerate(self.states_col)}

        _df = deepcopy(df)
        self.df = _df

    @property
    def np_data(self):
        return self._df.to_numpy()

    @property
    def df(self) -> pd.DataFrame:
        """Panda dataframe representation of the data"""
        return self._df

    @df.setter
    def df(self, value: pd.DataFrame):
        # Check col names
        missing_cols = set(value.columns).difference(self.states_col)
        extra_cols = set(self.states_col).difference(value.columns)
        if len(extra_cols) > 0:
            raise ValueError(f"Could not interpret the following columns: {extra_cols}")

        if not "time" in value.columns:
            raise ValueError("Observations should have a 'time' column")

        time = value["time"].to_numpy()
        if (len(time) > 1) and np.any(time[1:] - time[:-1] <= 0):
            raise ValueError("Time information should be increasing")

        # Fill missing columns
        if len(missing_cols):
            value[missing_cols] = np.NaN

        self._df = value[self.states_col]

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save Observations object to a .csv file"""
        path = combine_to_path(name, "csv", directory)
        self._df.to_csv(path, index=False)
        return path

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load Observations object to a .csv file"""
        return cls(pd.read_csv(combine_to_path(name, "csv", directory)))

    def __repr__(self):
        return self._df.__repr__()

    def __str__(self):
        return self._df.__str__()

    @property
    def time_index(self):
        return self._df["time"]

    def split(self, time_split: float):
        """
        Returns a tuple containing the feed information up to time and the feed information after time.
        Split is done so that the first information can give prediction up to time included.
        """
        time_feed = self.time_index
        cond = time_feed < time_split

        obs_before = self._df.iloc[cond]
        obs_after = self._df.iloc[~cond]
        return (self.__class__(obs_before), self.__class__(obs_after))

    def plot(self, pred_name: str, *args, **kwargs):
        data = self._df[pred_name]
        name_with_unit = f"{pred_name} (in {state_units_dict[pred_name]})"
        if "label" in kwargs.keys():
            plt.plot(self.time_index, data, *args, **kwargs)
        else:
            plt.plot(self.time_index, data, *args, label=name_with_unit, **kwargs)
        return plt

    def get_state(self, index):
        return AM2State(self._df.iloc[index])


class AM2State:
    state_col = state_col
    """AM2 State: this is what is predicted by AM2 ODE"""

    def __init__(self, state: pd.Series):
        self.df = state.copy()

    @property
    def np_data(self) -> np.ndarray:
        return self._df.to_numpy()

    @property
    def df(self) -> pd.Series:
        """Panda dataframe representation of the data"""
        return self._df

    @df.setter
    def df(self, value: pd.Series):
        # Check if all data is present
        if not isinstance(value, pd.Series):
            _value = pd.Series(value)
        else:
            _value = value
        missing = set(state_col).difference(_value.index)
        extra = set(_value.index).difference(state_col)

        err_msg = []
        if missing:
            err_msg.append(f"Missing indexes: {missing}")

        if extra:
            err_msg.append(f"Unknown indexes: {missing}")

        err_str = "\nFurthermore: ".join(err_msg)
        if err_str:
            raise ValueError(err_str)

        self._df = _value[state_col]

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save ADM1State object to a .json file"""
        path = combine_to_path(name, rw_jsonlike.ext, directory)
        rw_jsonlike.save(path, self._df)
        return path

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        return cls(rw_jsonlike.load(combine_to_path(name, rw_jsonlike.ext, directory)))

    @property
    def X1(self) -> float:
        return self._df["X1"]

    @property
    def X2(self) -> float:
        return self._df["X2"]

    @property
    def S1(self) -> float:
        return self._df["S1"]

    @property
    def S2(self) -> float:
        return self._df["S2"]

    @property
    def Z(self) -> float:
        return self._df["Z"]

    @property
    def C(self) -> float:
        return self._df["C"]
