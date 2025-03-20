from typing import Optional, Union
import warnings

import numpy as np
import pandas as pd
from apicutils.basic_io import combine_to_path
from anaerodig.pyad.digester import AnaerobicDigesterModel
from anaerodig.pyam2.basic_classes.config import AM2Config
from anaerodig.pyam2.basic_classes.feed import AM2Feed
from anaerodig.pyam2.basic_classes.param import AM2Param, default_param
from anaerodig.pyam2.basic_classes.states import AM2State, AM2States, states_col
from anaerodig.pyam2.model.der_am2 import am2_with_der
from anaerodig.pyam2.model.run_am2 import run_am2
from anaerodig.ode_solver.runge_kutta import ButcherTableau, infer_butcher_tableau, Butcher45


class AM2Failure(Exception):
    """Failure of AM2"""


class AM2Dig(AnaerobicDigesterModel):
    """Digester class designed for AM2 simulations

    DEV NOTE:
    Subclass of AM2Dig should in most cases have the load method rewritten.
    The exception is when the __init__ arguments are not modified (no field added, no field removed, no types change).
    In that setting, the load method of the subclass shoud return a member of the subclass
    """

    ERROR_STATES_COL = ["S1", "S2", "qm", "qc"]

    def __init__(
        self,
        feed: AM2Feed,
        ini_state: AM2State,
        obs: Optional[AM2States] = None,
        dig_info: Optional[AM2Config] = None,
    ):
        # Use properties' setters to check validity of data
        self.feed = feed
        self.ini_state = ini_state
        self.obs = obs

        # Set dig_info
        if dig_info is None:
            self.dig_info = AM2Config()
        else:
            self.dig_info = dig_info

    @property
    def dig_info(self) -> AM2Config:
        """Digester information"""
        return self._dig_info

    @dig_info.setter
    def dig_info(self, value):
        if not isinstance(value, AM2Config):
            raise TypeError("dig_info must be a AM2Config")
        self._dig_info = value

    @property
    def feed(self) -> AM2Feed:
        """AM2Feed data"""
        return self._feed

    @feed.setter
    def feed(self, value):
        if not isinstance(value, AM2Feed):
            raise TypeError("feed must be a AM2Feed")
        self._feed = value
        self._np_feed = self._feed.np_data

    @property
    def ini_state(self) -> AM2States:
        """Initial state"""
        return self._ini_state

    @ini_state.setter
    def ini_state(self, value):
        if not isinstance(value, AM2State):
            raise TypeError("ini_state must be a AM2State")
        self._ini_state = value
        self._np_ini_state = self._ini_state.np_data

    @property
    def obs(self) -> Optional[AM2States]:
        """Observations data (Optional)"""
        return self._obs

    @obs.setter
    def obs(self, value):
        if isinstance(value, AM2States):
            self._obs = value
            self._np_obs = self._obs.np_data
        elif value is None:
            self._obs = None
            self._np_obs = None
        else:
            raise TypeError("obs must be a AM2States")

    def _simulate(
        self,
        param:AM2Param,
        n_t:int,
        t_coeffs:np.ndarray,
        A_coeffs:np.ndarray,
        b0:np.ndarray,
        b1:np.ndarray,
        order:int,
        dt:float =5/(24*60),
        min_step:float = (0.5)/(24 * 60),
        tol:float=1e-5
        ) -> np.ndarray:
        """Call to run_am2"""

        res, reached_dt_min = run_am2(
            **param.param_dict, 
            n_t=n_t,
            t_coeffs=t_coeffs,
            A_coeffs=A_coeffs,
            b0=b0,
            b1=b1,
            order=order,
            tol=tol,
            # Feed
            ts=self._feed.time,
            Ds=self._feed.D,
            S1_ins=self._feed.S1,
            S2_ins=self._feed.S2,
            Z_ins=self._feed.Z,
            C_ins=self._feed.C,
            pHs=self._feed.pH,
            # Initial state
            X1_0=self._ini_state.X1,
            X2_0=self._ini_state.X2,
            S1_0=self._ini_state.S1,
            S2_0=self._ini_state.S2,
            Z_0=self._ini_state.Z,
            C_0=self._ini_state.C,
            # Other hyparameters
            dt=dt,
            min_step=min_step,)
        if reached_dt_min:
            warnings.warn("Reached minimum time step")
        return res

    @classmethod
    def convert_pred_array_to_states(cls, x: np.ndarray) -> AM2States:
        """Convert predictions, as returned by model, to AM2States"""
        return AM2States(
            pd.DataFrame(
                x,
                columns=states_col,
            )
        )
    
    def simulate(
        self,
        param:AM2Param=default_param,
        butcher:Union[str, ButcherTableau]=Butcher45,
        dt:float=5/(24*60),
        min_step:float = (0.5)/(24 * 60),
        tol:float=1e-5
        ):
        """Perform simulation using AM2.

        Args:
            param: an AM2Param (if not provided, the default parameter is used
        Return:
            the predictions, in AM2States format

        IMPLEMENTATION NOTES:
        Implementation derived from original AM2 description by Bernard et al. 2001
        (https://doi.org/10.1002/bit.10036).

        Following Hassam et al. 2015 (https://doi.org/10.1016/j.bej.2015.03.007), a mortality rate of 0.1
        was added when computing growth rate.

        The equation to compute CO2 was also modified to account for the knowledge of the pH:

        CO2 = C / (
            1 + 10 ** (pH - pKb)
        )

        which amounts to eq 53 in Bernard et al. 2001 or equivalently from combining eq 3. and 5. from
        the same source.
        """
        _butcher = infer_butcher_tableau(butcher)
        try:
            res = self._simulate(
                param=param,
                n_t=_butcher.n_t,
                t_coeffs=_butcher.t_coeffs,
                A_coeffs=_butcher.coeffs,
                b0=_butcher.b0,
                b1=_butcher.b1,
                order=_butcher.order,
                dt=dt,
                min_step=min_step,
                tol=tol)
        except Exception as exc:
            raise AM2Failure from exc
        
        return self.convert_pred_array_to_states(res)


    # def derivative(self, param: AM2Param, **kwargs) -> np.ndarray:
    #     """Compute derivative of simulation with respect to param"""
    #     return am2_derivative(
    #         **param.param_dict,
    #         # Influent
    #         ts=self._feed.time,
    #         Ds=self._feed.D,
    #         S1_ins=self._feed.S1,
    #         S2_ins=self._feed.S2,
    #         Z_ins=self._feed.Z,
    #         C_ins=self._feed.C,
    #         pHs=self._feed.pH,
    #         # Initial state
    #         X1_0=self._ini_state.X1,
    #         X2_0=self._ini_state.X2,
    #         S1_0=self._ini_state.S1,
    #         S2_0=self._ini_state.S2,
    #         Z_0=self._ini_state.Z,
    #         C_0=self._ini_state.C,
    #         # Other params
    #         **kwargs,
    #     )

    # def simu_and_der(self, param: AM2Param, **kwargs):
    #     """Simulate with AM2 and compute derivative of simulation with respect to the AM2Param

    #     Returns a tuple (first element, the simulation in np.ndarray form,
    #     second element the derivative in np.ndarray form)"""

    #     return am2_with_der(
    #         **param.param_dict,
    #         # Influent
    #         ts=self._feed.time,
    #         Ds=self._feed.D,
    #         S1_ins=self._feed.S1,
    #         S2_ins=self._feed.S2,
    #         Z_ins=self._feed.Z,
    #         C_ins=self._feed.C,
    #         pHs=self._feed.pH,
    #         # Initial state
    #         X1_0=self._ini_state.X1,
    #         X2_0=self._ini_state.X2,
    #         S1_0=self._ini_state.S1,
    #         S2_0=self._ini_state.S2,
    #         Z_0=self._ini_state.Z,
    #         C_0=self._ini_state.C,
    #         # Other params
    #         **kwargs,
    #     )

    def simu_and_der(
        self,
        param: AM2Param,
        butcher:Union[str, ButcherTableau]=Butcher45,
        dt:float=5/(24*60),
        min_step:float = (0.1)/(24 * 60),
        tol:float=1e-5
        ):
        """Simulate with AM2 and compute derivative of simulation with respect to the AM2Param

        Returns a tuple (first element, the simulation in np.ndarray form,
        second element the derivative in np.ndarray form)"""
        _butcher = infer_butcher_tableau(butcher)
        res, der_res, reached_dt_min = am2_with_der(
            **param.param_dict,
            # Influent
            ts=self._feed.time,
            Ds=self._feed.D,
            S1_ins=self._feed.S1,
            S2_ins=self._feed.S2,
            Z_ins=self._feed.Z,
            C_ins=self._feed.C,
            pHs=self._feed.pH,
            # Initial state
            X1_0=self._ini_state.X1,
            X2_0=self._ini_state.X2,
            S1_0=self._ini_state.S1,
            S2_0=self._ini_state.S2,
            Z_0=self._ini_state.Z,
            C_0=self._ini_state.C,
            # Other params
            n_t=_butcher.n_t,
            t_coeffs=_butcher.t_coeffs,
            A_coeffs=_butcher.coeffs,
            b0=_butcher.b0,
            b1=_butcher.b1,
            order=_butcher.order,
            dt=dt,
            min_step=min_step,
            tol=tol
        )
        if reached_dt_min:
            warnings.warn("Reached minimum time step")
        return res, der_res   

    def error(self, predictions: AM2States) -> float:
        """Compute error between predictions and observations"""
        eps = 10**-8
        residuals = np.log(
            ((predictions.df + eps) / (self.obs.df + eps))[
                self.ERROR_STATES_COL
            ].to_numpy()
        )
        return np.sqrt(np.nanmean(np.nanmean(residuals**2, 0)))

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load a AM2Dig from file."""
        path = combine_to_path(name, "", directory)
        try:
            obs = AM2States.load(cls.OBS_PATH, directory=path)
        except FileNotFoundError:
            # Broad except should be reset to FileNotFound
            # (this implies improving the basic_io module)
            obs = None

        try:
            dig_info = AM2Config.load(cls.DIG_CONFIG_PATH, directory=path)
        except FileNotFoundError:
            dig_info = None
        return cls(
            dig_info=dig_info,
            feed=AM2Feed.load(cls.FEED_PATH, directory=path),
            ini_state=AM2State.load(cls.INI_STATE_PATH, directory=path),
            obs=obs,
        )


if __name__ == "__main__":
    from time import time

    from anaerodig.pyam2.data import data_dir, param_file

    digester = AM2Dig.load(data_dir)
    param = AM2Param.load(param_file, data_dir)

    print("Simulating with AM2")
    tic = time()
    pred = digester.simulate(param)
    tac = time()
    print(f"Predictions done in {tac-tic}:\n{pred}")
