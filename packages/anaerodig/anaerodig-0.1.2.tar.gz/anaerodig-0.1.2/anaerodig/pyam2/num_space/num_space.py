"""
Numerical space for AM2 parameter.
This defines a parametrization on R^5 of the parameter, avoiding the positivity requirement
for the parameter values (and hence simplifying tasks such as optimisation).

This is given as a template to follow when interfacing anaerodig package to optimisation
packages
"""

import numpy as np
import pandas as pd
from anaerodig.pyam2.basic_classes.param import AM2Param

# Standard deviation of the log parameters
std_log_devs_dict = {"mu1max": 0.5, "mu2max": 1.2, "KS1": 0.8, "KS2": 1.2, "KI2": 1.0}

std_log_devs = np.array([std_log_devs_dict[name] for name in AM2Param.param_list])


class AM2FreeParam(AM2Param):
    """Free space for AM2 Param.
    This subclass of AM2Param provides a mapping between np.ndarray objects and AM2Param
    This mapping can be used when interfacing to optimisation routines (e.g. when calibrating)
    Note that AM2FreeParam is only an instance of such a mapping, and there is basically no
    limit to one's creativity when designing such maps. It is provided more as a guideline
    for users interested in such aspects.

    """

    # Optimisation typical ranges
    # (can be replaced by [-alpha low_ranges -b, alpha low_ranges + b]
    # for a, b > 0 in practical implementations
    low_ranges = -std_log_devs
    high_ranges = std_log_devs

    def __init__(self, x: np.ndarray):
        self.x = x
        super().__init__(pd.Series(np.exp(x), AM2Param.param_list))

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        _value = np.asarray(value)
        if len(_value) != len(AM2Param.param_list):
            raise ValueError(f"Expected array of len {len(AM2Param.param_list)}")
        self._x = _value

    @classmethod
    def mult_convert(cls, xs: np.ndarray):
        """Convert multiple parameters"""
        return [cls(x) for x in xs]

    @classmethod
    def from_param(cls, param: AM2Param) -> np.ndarray:
        """Infer x value for a AM2Param"""
        return np.log(param.series[AM2Param.param_list].to_numpy())
