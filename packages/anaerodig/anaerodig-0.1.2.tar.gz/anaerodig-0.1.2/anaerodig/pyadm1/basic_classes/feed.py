"""ADM1 Feed class"""
from typing import Optional

import anaerodig.nb_typ as nbt
import numba as nb
import numpy as np
import pandas as pd
from apicutils.basic_io import combine_to_path
from anaerodig.pyadm1.basic_classes.Phy import COD_VS, R, T_base

influent_state_cols = [
    "time",
    "T_op",  # Kelvin
    "S_su",  # kgCOD M-3
    "S_aa",  # kgCOD M-3
    "S_fa",  # kgCOD M-3
    "S_va",  # kgCOD M-3
    "S_bu",  # kgCOD M-3
    "S_pro",  # kgCOD M-3
    "S_ac",  # kgCOD M-3
    "S_h2",  # kgCOD M-3
    "S_ch4",  # kgCOD M-3
    "S_IC",  # kmole C M-3
    "S_IN",  # kmole N M-3
    "S_I",  # kgCOD M-3
    "X_c",  # kgCOD m-3
    "X_ch",  # kgCOD m-3
    "X_pr",  # kgCOD M-3
    "X_li",  # kgCOD M-3
    "X_su",  # kgCOD M-3
    "X_aa",  # kgCOD M-3
    "X_fa",  # kgCOD M-3
    "X_c4",  # kgCOD M-3
    "X_pro",  # kgCOD M-3
    "X_ac",  # kgCOD M-3
    "X_h2",  # kgCOD M-3
    "X_I",  # kgCOD M-3
    "S_cation",  # kmole M-3
    "S_anion",  # kmole M-3
    "Q",  # M3 Day-1
]

influent_state_units = {
    "time": "Day",
    "T_op": "Kelvin",
    "S_su": "kgCOD M-3",
    "S_aa": "kgCOD M-3",
    "S_fa": "kgCOD M-3",
    "S_va": "kgCOD M-3",
    "S_bu": "kgCOD M-3",
    "S_pro": "kgCOD M-3",
    "S_ac": "kgCOD M-3",
    "S_h2": "kgCOD M-3",
    "S_ch4": "kgCOD M-3",
    "S_IC": "kmole C M-3",
    "S_IN": "kmole N M-3",
    "S_I": "kgCOD M-3",
    "X_c": "kgCOD M-3",
    "X_ch": "kgCOD M-3",
    "X_pr": "kgCOD M-3",
    "X_li": "kgCOD M-3",
    "X_su": "kgCOD M-3",
    "X_aa": "kgCOD M-3",
    "X_fa": "kgCOD M-3",
    "X_c4": "kgCOD M-3",
    "X_pro": "kgCOD M-3",
    "X_ac": "kgCOD M-3",
    "X_h2": "kgCOD M-3",
    "X_I": "kgCOD M-3",
    "S_cation": "kmole M-3",
    "S_anion": "kmole M-3",
    "Q": "M3 Day-1",
}

influent_state_cols_dict = {name: i for i, name in enumerate(influent_state_cols)}
feed_idx_time = influent_state_cols_dict["time"]
feed_idx_T_op = influent_state_cols_dict["T_op"]
feed_idx_S_su = influent_state_cols_dict["S_su"]
feed_idx_S_aa = influent_state_cols_dict["S_aa"]
feed_idx_S_fa = influent_state_cols_dict["S_fa"]
feed_idx_S_va = influent_state_cols_dict["S_va"]
feed_idx_S_bu = influent_state_cols_dict["S_bu"]
feed_idx_S_pro = influent_state_cols_dict["S_pro"]
feed_idx_S_ac = influent_state_cols_dict["S_ac"]
feed_idx_S_h2 = influent_state_cols_dict["S_h2"]
feed_idx_S_ch4 = influent_state_cols_dict["S_ch4"]
feed_idx_S_IC = influent_state_cols_dict["S_IC"]
feed_idx_S_IN = influent_state_cols_dict["S_IN"]
feed_idx_S_I = influent_state_cols_dict["S_I"]
feed_idx_X_c = influent_state_cols_dict["X_c"]
feed_idx_X_ch = influent_state_cols_dict["X_ch"]
feed_idx_X_pr = influent_state_cols_dict["X_pr"]
feed_idx_X_li = influent_state_cols_dict["X_li"]
feed_idx_X_su = influent_state_cols_dict["X_su"]
feed_idx_X_aa = influent_state_cols_dict["X_aa"]
feed_idx_X_fa = influent_state_cols_dict["X_fa"]
feed_idx_X_c4 = influent_state_cols_dict["X_c4"]
feed_idx_X_pro = influent_state_cols_dict["X_pro"]
feed_idx_X_ac = influent_state_cols_dict["X_ac"]
feed_idx_X_h2 = influent_state_cols_dict["X_h2"]
feed_idx_X_I = influent_state_cols_dict["X_I"]
feed_idx_S_cation = influent_state_cols_dict["S_cation"]
feed_idx_S_anion = influent_state_cols_dict["S_anion"]
feed_idx_Q = influent_state_cols_dict["Q"]

cod_vs_feed_cols = np.array([influent_state_cols_dict[name] for name in COD_VS])
q_col = influent_state_cols_dict["Q"]


# Build time assert: check that all columns have a unit

__delta = set(influent_state_cols).symmetric_difference(influent_state_units)
if __delta:
    raise ValueError(f"Unnexplained columns in ADM1Feed: {__delta}")


@nb.njit(nbt.UTuple(nbt.f1D, 7)(nbt.f1D))
def compute_K_H_s(
    T_op: np.ndarray,
) -> tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray
]:
    """Helper function to perform some precomputation on feed
    Args:
        T_op
    """
    delta_1_T = 1.0 / T_base - 1.0 / T_op
    p_gas_h2o = 0.0313 * np.exp(5290.0 * delta_1_T)  # bar #0.0557
    K_H_co2 = 0.035 * np.exp(
        (-19410.0 / (100.0 * R)) * delta_1_T
    )  # Mliq.bar^-1 #0.0271
    K_H_ch4 = 0.0014 * np.exp(
        (-14240.0 / (100.0 * R)) * delta_1_T
    )  # Mliq.bar^-1 #0.00116
    K_H_h2 = (
        7.8 * 10**-4 * np.exp(-4180.0 / (100.0 * R) * delta_1_T)
    )  # Mliq.bar^-1 #7.38*10^-4
    K_a_co2 = 10.0**-6.35 * np.exp((7646.0 / (100.0 * R)) * delta_1_T)
    # M #2.08 * 10 ^ -14
    K_a_IN = 10.0 ** (-9.25) * np.exp(
        (51965.0 / (100.0 * R)) * delta_1_T
    )  # M #1.11 * 10 ^ -9
    K_w = 10**-14.0 * np.exp(
        (55900.0 / (100.0 * R)) * delta_1_T
    )  # M #2.08 * 10 ^ -14
    return p_gas_h2o, K_H_co2, K_H_ch4, K_H_h2, K_a_co2, K_a_IN, K_w


class ADM1Feed:
    """Feed information for ADM1 model"""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    @property
    def np_data(self):
        """numpy.ndarray view of the Feed data"""
        return self._df.to_numpy()

    @property
    def n_time(self) -> int:
        """Length of time index in Feed data"""
        return self._df.shape[0]

    @property
    def df(self) -> pd.DataFrame:
        """Pandas.DataFrame representation of the Feed data"""
        return self._df

    @df.setter
    def df(self, value: pd.DataFrame):
        # Filter volume information if present
        if "V_liq" in value.columns:
            self.__V_liq_s = value.pop("V_liq").to_numpy()
        else:
            self.__V_liq_s = None

        # Check col names
        extra_cols = set(value.columns).difference(influent_state_cols)
        missing_cols = set(influent_state_cols).difference(value.columns)
        unexplained = set(value.columns).symmetric_difference(influent_state_cols)

        if extra_cols or missing_cols:
            raise ValueError(
                "\n".join(
                    [
                        f"Passed dataframe has extra columns or missing columns.",
                        f"Extra columns: {extra_cols}",
                        f"Missing columns: {missing_cols}"]))

        time = value["time"].to_numpy()
        if (len(time) > 1) and np.any(time[1:] - time[:-1] <= 0):
            raise ValueError("Time information should be increasing")
        self._df = value[influent_state_cols]
        (
            self.__p_gas_h2o,
            self.__K_H_co2,
            self.__K_H_ch4,
            self.__K_H_h2,
            self.__K_a_co2,
            self.__K_a_IN,
            self.__K_w,
        ) = compute_K_H_s(self._df["T_op"].to_numpy())

    @property
    def V_liq_s(self) -> Optional[np.ndarray]:
        """Liquid volume information (Optional)"""
        if self.__V_liq_s is None:
            return None
        return self.__V_liq_s.copy()

    @property
    def p_gas_h2o_s(self) -> np.ndarray:
        return self.__p_gas_h2o.copy()

    @property
    def K_H_co2_s(self) -> np.ndarray:
        return self.__K_H_co2.copy()

    @property
    def K_H_ch4_s(self) -> np.ndarray:
        return self.__K_H_ch4.copy()

    @property
    def K_H_h2_s(self) -> np.ndarray:
        return self.__K_H_h2.copy()

    @property
    def K_a_co2_s(self) -> np.ndarray:
        return self.__K_a_co2.copy()

    @property
    def K_a_IN_s(self) -> np.ndarray:
        return self.__K_a_IN.copy()

    @property
    def K_w_s(self) -> np.ndarray:
        return self.__K_w.copy()

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save DigesterFeed object to a .csv file"""

        path = combine_to_path(name, "csv", directory)
        self._df.to_csv(path, index=False)
        return path

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        return cls(pd.read_csv(combine_to_path(name, "csv", directory)))

    def __repr__(self):
        return self._df.__repr__()

    def __str__(self):
        return self._df.__str__()

    def split(self, time_split: float):
        """
        Returns a tuple containing the feed information up to 'time_split' and the feed
        information after 'time_split'.
        Split is done so that the first information can give prediction up to time included.
        """
        time_feed = self._df["time"]
        cond = time_feed < time_split

        feed_before = self._df.loc[cond]
        feed_after = self._df.loc[~cond]
        return (ADM1Feed(feed_before), ADM1Feed(feed_after))

    def noise(self, noise_lev: float, inplace: bool = False):
        """Add multiplicative noise
        (uniform noise between -noise_lev and noise_lev in log space)"""
        noise = np.exp(
            np.random.uniform(
                -noise_lev, noise_lev, (self.df.shape[0], self.df.shape[1] - 1)
            )
        )
        cols_to_noise = [col for col in influent_state_cols if col != "time"]
        if inplace:
            self.df[cols_to_noise] *= noise
            return None

        df = self.df.copy()
        df[cols_to_noise] *= noise

        return ADM1Feed(df)
