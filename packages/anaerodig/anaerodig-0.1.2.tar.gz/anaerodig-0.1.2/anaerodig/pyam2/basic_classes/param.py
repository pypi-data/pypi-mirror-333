from typing import Optional

import pandas as pd
from apicutils.basic_io import combine_to_path, rw_jsonlike

param_list = ["mu1max", "mu2max", "KS1", "KS2", "KI2"]

parameter_dict = {key: i for i, key in enumerate(param_list)}

parameter_units = {
    "mu1max": r"$d^{-1}$",
    "mu2max": r"$d^{-1}",
    "KS1": r"gCOD $L^{-1}$",
    "KS2": r"mmol $L^{-1}$",
    "KI2": r"mmol $L^{-1}$",
}


class AM2Param:
    # By default, the list of parameters expected
    param_list = ["mu1max", "mu2max", "KS1", "KS2", "KI2"]

    def __init__(self, series: pd.Series):
        self.series = series

    @property
    def series(self):
        return self._series

    @series.setter
    def series(self, value: pd.Series):
        if not isinstance(value, pd.Series):
            _value = pd.Series(value)
        else:
            _value = value

        missing = set(_value.index).difference(param_list)
        extra = set(param_list).difference(_value.index)
        err_msg = []

        if missing:
            err_msg.append(f"Missing indexes: {missing}")

        if extra:
            err_msg.append(f"Unknown indexes: {missing}")

        err_str = "\nFurthermore: ".join(err_msg)
        if err_str:
            raise ValueError(err_str)

        self._series = _value

    @property
    def mu1max(self) -> float:
        return self._series["mu1max"]

    @property
    def mu2max(self) -> float:
        return self._series["mu2max"]

    @property
    def KS1(self) -> float:
        return self._series["KS1"]

    @property
    def KS2(self) -> float:
        return self._series["KS2"]

    @property
    def KI2(self) -> float:
        return self._series["KI2"]

    @property
    def param_dict(self) -> dict[str, float]:
        """Transform AM2Param in a dictionnary of str, float usable in AM2 simulations"""
        # Crucial: param_list and not self.param_list!
        # Explanation: for subclass, we want to maintain the same output.
        # This guarantees that as long as the properties are correctly coded,
        # the correct parameter will be returned without having to redefine param_dict
        # For exemple, if one considers mu2max / KS2 and mu2max * KS2 as parameters, as
        # long as one defines KS2 and mu2max properties, there will not be any issue
        # This avoids relying on a series which might not be valid.

        return {key: getattr(self, key) for key in param_list}

    def save(self, name: str, directory: Optional[str] = None) -> str:
        path = combine_to_path(name, rw_jsonlike.ext, directory)
        rw_jsonlike.save(path, self._series)
        return path

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load ADM1Param from file"""
        return cls(rw_jsonlike.load(combine_to_path(name, rw_jsonlike.ext, directory)))


default_param = AM2Param(
    {"mu1max": 1.2, "mu2max": 0.74, "KS1": 7.1, "KS2": 9.28, "KI2": 256.0}
)
