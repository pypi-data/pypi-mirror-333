"""Exemple of map between array to ADM1Param which can be used to calibrate 30 parameters"""

import numpy as np
from anaerodig.pyadm1.basic_classes.param import ADM1Param


class ADM1FreeParam(ADM1Param):
    """Free space for ADM1 Param"""

    params_to_cal = [
        "k_dis",
        "k_hyd_ch",
        "k_hyd_pr",
        "k_hyd_li",
        "k_m_su",
        "k_m_aa",
        "k_m_fa",
        "k_m_c4",
        "k_m_pro",
        "k_m_ac",
        "k_m_h2",
        "k_dec",
        "K_S_IN",
        "K_S_su",
        "K_S_aa",
        "K_S_fa",
        "K_S_c4",
        "K_S_pro",
        "K_S_ac",
        "K_S_h2",
        "K_I_h2_fa",
        "K_I_h2_c4",
        "K_I_h2_pro",
        "K_I_nh3",
        "pH_UL:LL_aa",
        "pH_LL_aa",
        "pH_UL:LL_ac",
        "pH_LL_ac",
        "pH_UL:LL_h2",
        "pH_LL_h2",
    ]
    _to_do = {"aa", "ac", "h2"}  # Action required for pH min/max order preserving

    def __init__(self, x: np.ndarray):
        self.x = x
        param_dict = dict(zip(self.params_to_cal, np.exp(x)))
        for name in self._to_do:
            delta_pH = param_dict.pop(f"pH_UL:LL_{name}")
            param_dict[f"pH_UL_{name}"] = param_dict[f"pH_LL_{name}"] + delta_pH
        super().__init__(param_dict)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        _value = np.asarray(value)
        if len(_value) != len(self.params_to_cal):
            raise ValueError(f"Expected array of len {len(self.params_to_cal)}")
        self._x = _value

    @classmethod
    def mult_convert(cls, xs: np.ndarray):
        """Convert multiple parameters"""
        return [cls(x) for x in xs]

    @classmethod
    def from_param(cls, param: ADM1Param) -> np.ndarray:
        """Infer x value for a AM2Param"""
        param_series = param.param.copy()
        for name in cls.params_to_cal:
            param_series[f"pH_UL:LL_{name}"] = (
                param_series[f"pH_UL_{name}"] - param_series[f"pH_LL_{name}"]
            )
        return np.log(param_series[cls.params_to_cal].to_numpy())
