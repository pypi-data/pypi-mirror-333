from functools import partial
from typing import Optional, Union
import warnings

import numpy as np
import pandas as pd
from apicutils import interpretation, num_der, post_modif
from apicutils.basic_io import combine_to_path
from anaerodig.pyad.digester import AnaerobicDigesterModel, NoObservationError
from anaerodig.pyadm1.basic_classes.config import ADM1Config
from anaerodig.pyadm1.basic_classes.feed import ADM1Feed
from anaerodig.pyadm1.basic_classes.param import ADM1Param
from anaerodig.pyadm1.basic_classes.state import ADM1State, ADM1States, pred_col
from anaerodig.pyadm1.model.helpers import N_DAY_VSR
from anaerodig.pyadm1.model.run_adm1 import run_adm1
from anaerodig.pyadm1.prediction_error import adm1_err
from anaerodig.ode_solver.runge_kutta import ButcherTableau, infer_butcher_tableau

class ADM1Failure(Exception):
    """Failure of ADM1"""


class ADM1Dig(AnaerobicDigesterModel):
    """Digester class designed for ADM1 simulations

    DEV NOTE:
    Subclass of ADM1Dig should in most cases have the load method rewritten.
    The exception is when the __init__ arguments are not modified (no field added, no field removed, no types change).
    In that setting, the load method of the subclass shoud return a member of the subclass
    """

    @property
    def dig_config(self) -> ADM1Config:
        return self._dig_config

    @dig_config.setter
    def dig_config(self, value):
        if not isinstance(value, ADM1Config):
            raise TypeError("dig_config must be a ADM1Config")
        self._dig_config = value

    @property
    def feed(self) -> ADM1Feed:
        """ADM1Feed data"""
        return self._feed

    @feed.setter
    def feed(self, value):
        if not isinstance(value, ADM1Feed):
            raise TypeError("feed must be a ADM1Feed")
        self._feed = value
        self._np_feed = self._feed.np_data

    @property
    def V_liq_s(self):
        if self._feed.V_liq_s is None:
            return np.full(self._feed.n_time, self._dig_config.V_liq)
        else:
            return self._feed.V_liq_s

    @property
    def V_gas_s(self) -> np.ndarray:
        """This is the volume of gas in m3"""
        return self._dig_config.V_liq + self._dig_config.V_gas - self.V_liq_s


    @property
    def ini_state(self) -> ADM1State:
        """Initial state"""
        return self._ini_state

    @ini_state.setter
    def ini_state(self, value):
        if not isinstance(value, ADM1State):
            raise TypeError("ini_state must be a ADM1State")
        self._ini_state = value
        self._np_ini_state = self._ini_state.np_data

    @property
    def obs(self) -> Optional[ADM1States]:
        """Observation Data"""
        return self._obs

    @obs.setter
    def obs(self, value):
        if isinstance(value, ADM1States):
            self._obs = value
            self._np_obs = self._obs.np_data
        elif value is None:
            self._obs = None
            self._np_obs = None
        else:
            raise TypeError("obs must be a ADM1States")

    def _simulate(self, param: ADM1Param, **kwargs) -> np.ndarray:

        res, reached_dtmin =  run_adm1(
            influent_state=self._np_feed,
            p_gas_h2o_s=self._feed.p_gas_h2o_s,
            K_H_co2_s=self._feed.K_H_co2_s,
            K_H_ch4_s=self._feed.K_H_ch4_s,
            K_H_h2_s=self._feed.K_H_h2_s,
            K_a_co2_s=self._feed.K_a_co2_s,
            K_a_IN_s=self._feed.K_a_IN_s,
            K_w_s=self._feed.K_w_s,
            V_liq_s=self.V_liq_s,
            V_gas_s=self.V_gas_s,
            initial_state=self._np_ini_state,
            **param.param,
            **kwargs,
        )
        if reached_dtmin:
            warnings.warn("Reached dt_min")
        return res

    def error(self, predictions: ADM1States) -> float:
        """Compute error between predictions and observations"""
        if not self.has_obs:
            raise NoObservationError()
        return adm1_err(predictions, self.obs)

    def simulate(
            self,
            param: ADM1Param,
            butcher:Union[str, ButcherTableau] = "45",
            max_step: float = 10.0 / (24.0 * 60.0),
            min_step: float = 10**-6,
            n_day_vsr: int = N_DAY_VSR,
            tol:float = 1e-5
        ):
        """
        Performs a simulation

        Args:
            param: parameter used for the simulation
            butcher: Butcher Table for Runge-Kutta ODE solver
            max_step: maximum time step for Runge Kutta ODE Solver
            min_step: minimum time step for Runge Kutta ODE Solver
            n_day_vsr: number of days used to compute VSR
            tol: tolerance for Runge Kutta ODE Solver (default 1e-5)
        """
        _butcher = infer_butcher_tableau(butcher)
        try:
            return ADM1States(
                pd.DataFrame(
                    self._simulate(
                        param=param,
                        n_t=_butcher.n_t,
                        t_coeffs=_butcher.t_coeffs,
                        A_coeffs=_butcher.coeffs,
                        b0=_butcher.b0,
                        b1=_butcher.b1,
                        order=_butcher.order,
                        tol=tol,
                        dt=max_step,
                        dt_min=min_step,
                        n_day_vsr=n_day_vsr,
                    ),
                    columns=pred_col,
                )
            )
        except Exception as exc:
            raise ADM1Failure from exc


    def derivative(
        self,
        param: ADM1Param,
        params_to_der: list,
        log_adm1: bool = True,
        rel_step: Optional[float] = 10**-7,
        parallel=True,
        **kwargs,
    ) -> np.ndarray:
        """
        Compute the Jacobian of (log-)ADM1 (run_adm1 implementation) close to param for parameters
        dimension in params_to_der. Time output is dropped.
        Built on top of comp_3d_jacob which does the main numerical derivation.

        Jacobian is outputed as a np.ndarray of shape (P, T, K) where
            P is number of parameters in params_eval
            T is the number of time points
            K is the number of predictions type

        adm1_derivative is user friendly (use pandas input rather than numpy).
        Conversion is done inside function.

        To avoid computation issues, relatives increments are considered to the parameter when
        computing the derivative (i.e. we consider ADM1(param_j * (1 + epsilon)) - AMD1(param_j)).
        The difference is then corrected for the value of param_j so that the output gives absolute
        derivative.

        With FUN = ADM1 or log(ADM1) depending on log_adm1, computes the derivative by approximating:
        (FUN(param + param_i * epsilon)) - FUN(param))/(epsilon * param_i)

        Args:
            - param, the parameter at which the derivative of ADM1 is to be computed
            - params_to_der, the list of parameter dimensions on which to compute the derivative.
            - log_adm1: if False, computes the derivative of ADM1, if True, computes the derivative of
                log(ADM1).
                True by default.
            - adm1_out: Optional output of ADM1 at param (even if log_adm1 is True). If false, not
                needed. Currently disregarded in all cases.
        kwargs are passed to run_adm1

        Returns:
            The jacobian in shape P, T, K (P number of parameters, T number of time points, K number of
                observations)

        Note:
            The default max_step argument of run_adm1 is set to half a minute. This is necessary to
            neutralize the effect of the max_step argument for small variation on parameter (spurious
            high frequency, small amplitude perturbations which impact the quality of the derivative).
            For similar reasons, one ought to be careful not to set the rel_step too low (or force
            the max_step to be low as well).
        """

        # Prepare ADM1 function
        set_adm1 = partial(
            self.simulate,
            **kwargs,
        )

        if log_adm1:
            post_mod = post_modif(lambda y: np.log(y[:, 1:]))
        else:
            post_mod = post_modif(lambda y: y[:, 1:])

        # Prepare numpy param -> ADM1Param Back/forth
        ini_param = np.array([param._param[name] for name in params_to_der])

        def to_param(x):
            return ADM1Param({name: val for name, val in zip(params_to_der, x)})

        translate_par = interpretation(to_param)

        # Modify ADM1
        loc_adm1 = translate_par(post_mod(set_adm1))

        der = num_der(fun=loc_adm1, x0=ini_param, rel_step=rel_step, parallel=parallel)

        return der

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load a ADM1Dig from file."""
        path = combine_to_path(name, "", directory)
        try:
            obs = ADM1States.load(cls.OBS_PATH, directory=path)
        except FileNotFoundError:
            obs = None

        return cls(
            dig_config=ADM1Config.load(cls.DIG_CONFIG_PATH, directory=path),
            feed=ADM1Feed.load(cls.FEED_PATH, directory=path),
            ini_state=ADM1State.load(cls.INI_STATE_PATH, directory=path),
            obs=obs,
        )


if __name__ == "__main__":
    from time import time

    from anaerodig.pyadm1.data import data_dir, param_file

    digester = ADM1Dig.load(data_dir)
    adm1_param = ADM1Param.load(param_file, data_dir)

    print("Simulating with ADM1")
    tic = time()
    pred = digester.simulate(adm1_param)
    tac = time()
    print(f"Predictions done in {tac-tic}:\n{pred}")
