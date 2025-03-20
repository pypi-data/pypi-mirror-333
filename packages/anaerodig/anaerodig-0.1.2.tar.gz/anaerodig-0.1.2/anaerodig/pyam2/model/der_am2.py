"""
Derivative of AM2 with respect to the calibration parameters.

Used to compute Fisher's information matrix (FIM) for UQ.
"""

import warnings
from typing import Optional

import numba as nb
import numpy as np
import scipy.integrate as si
import anaerodig.nb_typ as nbt
from anaerodig.pyam2.model.run_am2 import (
    KH,
    P_T,
    ParamHandling,
    alpha,
    day_index,
    k1,
    k2,
    k3,
    k4,
    k5,
    k6,
    kLa,
    pKb,
)


@nb.njit
def am2_ode_with_der(
    t: float,
    y: np.ndarray,
    ts: np.ndarray,
    Ds: np.ndarray,
    S1_ins: np.ndarray,
    S2_ins: np.ndarray,
    Z_ins: np.ndarray,
    C_ins: np.ndarray,
    pHs: np.ndarray,
    mu1max: float,
    KS1: float,
    mu2max: float,
    KS2: float,
    KI2: float,
) -> np.ndarray:
    """
    Computes the derivative of the digester state (S) at time t, i.e.

    dS/dt (t) = AM2_ODE(t, S)
    """

    # Read feed information
    index = min(np.sum(t > ts), len(ts) - 1)  # type: ignore
    D, S1_in, S2_in, Z_in, C_in, pH = (
        Ds[index],
        S1_ins[index],
        S2_ins[index],
        Z_ins[index],
        C_ins[index],
        pHs[index],
    )

    # Unpack current digester state information
    X1 = y[0]
    X2 = y[1]
    S1 = y[2]
    S2 = y[3]
    Z = y[4]
    C = y[5]

    # Compute intermediary
    mu1 = mu1max * (S1 / (KS1 + S1) - 0.1)  # D-1
    mu2 = mu2max * (S2 / (KS2 + S2 * (1 + S2 / KI2)) - 0.1)  # D-1

    d_mu1_mu1max = S1 / (KS1 + S1) - 0.1
    d_mu1_KS1 = mu1max * (-S1 / (KS1 + S1) ** 2)

    d_mu2_mu2max = S2 / (KS2 + S2 * (1 + S2 / KI2)) - 0.1
    d_mu2_KS2 = -mu2max * S2 / (KS2 + S2 * (1 + S2 / KI2)) ** 2
    d_mu2_KI2 = mu2max * (S2**3 / (KI2 * (KS2 + S2) + S2**2) ** 2)

    d_mu1_S1 = mu1max * (KS1 / (KS1 + S1) ** 2)
    d_mu2_S2 = mu2max * (
        1 / (KS2 + S2 * (1 + S2 / KI2))
        - S2 * (1 + 2 * S2 / KI2) / (KS2 + S2 * (1 + S2 / KI2)) ** 2
    )

    qM = k6 * mu2 * X2  # mmol L-1 D-1

    d_qM_mu2 = k6 * X2

    d_qM_X2 = k6 * mu2
    d_qM_S2 = k6 * d_mu2_S2 * X2

    CO2 = C / (1 + 10 ** (pH - pKb))
    d_CO2_C = 1 / (1 + 10 ** (pH - pKb))

    # CO2 = C + S2 - Z # mmol L-1

    phi = CO2 + KH * P_T + qM / kLa  # mmol L-1
    d_phi_C = d_CO2_C
    d_phi_qM = 1 / kLa

    KH_PC = (phi - np.sqrt(phi**2 - 4 * KH * P_T * CO2)) / 2  # mmol L-1
    d_KHPC_phi = (1 - phi / np.sqrt(phi**2 - 4 * KH * P_T * CO2)) / 2
    d_KHPC_CO2 = KH * P_T / (np.sqrt(phi**2 - 4 * KH * P_T * CO2))

    d_KHPC_C = d_KHPC_phi * d_phi_C + d_KHPC_CO2 * d_CO2_C
    d_KHPC_X2 = d_KHPC_phi * d_phi_qM * d_qM_X2
    d_KHPC_S2 = d_KHPC_phi * d_phi_qM * d_qM_S2

    qC = kLa * (CO2 - KH_PC)  # mmol L-1 D-1

    d_qC_mu2 = -kLa * d_KHPC_phi * d_phi_qM * d_qM_mu2

    d_qC_C = kLa * (d_CO2_C - d_KHPC_C)
    d_qC_X2 = -kLa * d_KHPC_X2
    d_qC_S2 = -kLa * d_KHPC_S2

    der_state_t = np.array(
        [
            (mu1 - alpha * D) * X1,  # dX1 # g L-1 D-1
            (mu2 - alpha * D) * X2,  # dX2 # mmol L-1 D-1
            D * (S1_in - S1) - k1 * mu1 * X1,  # dS1 # gCod L-1 D-1
            D * (S2_in - S2) + k2 * mu1 * X1 - k3 * mu2 * X2,  # dS2 # mmol L-1 D-1
            D * (Z_in - Z),  # dZ # mmol L-1 D-1
            D * (C_in - C) - qC + k4 * mu1 * X1 + k5 * mu2 * X2,  # dC # mmol L-1 D-1
        ]
    )

    # # der_state_t_param = np.zeros((6, 5))
    # # der_state_t_param[0] =
    der_state_t_param = np.array(
        [
            [
                X1 * d_mu1_mu1max,
                0.0,
                X1 * d_mu1_KS1,
                0.0,
                0.0,
            ],  # mu1max, mu2max, KS1, KS2, KI2
            [0.0, X2 * d_mu2_mu2max, 0.0, X2 * d_mu2_KS2, X2 * d_mu2_KI2],
            [-k1 * d_mu1_mu1max * X1, 0.0, -k1 * d_mu1_KS1 * X1, 0.0, 0.0],
            [
                k2 * d_mu1_mu1max * X1,
                -k3 * d_mu2_mu2max * X2,
                k2 * d_mu1_KS1 * X1,
                -k3 * d_mu2_KS2 * X2,
                -k3 * d_mu2_KI2 * X2,
            ],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [
                k4 * d_mu1_mu1max * X1,
                (k5 * X2 - d_qC_mu2) * d_mu2_mu2max,
                k4 * d_mu1_KS1 * X1,
                (k5 * X2 - d_qC_mu2) * d_mu2_KS2,
                (k5 * X2 - d_qC_mu2) * d_mu2_KI2,
            ],
        ]
    ).flatten()

    der_state_t_state = np.array(
        [
            [
                mu1 - alpha * D,  # X1
                0.0,  # X2
                d_mu1_S1 * X1,  # S1
                0.0,  # S2
                0.0,  # Z
                0.0,  # C
            ],  # dX1/dt
            [
                0.0,  # X1
                (mu2 - alpha * D),  # X2
                0.0,  # S1
                d_mu2_S2 * X2,  # S2
                0.0,  # Z
                0.0,  # C
            ],  # dX2/dt
            [
                -k1 * mu1,  # X1
                0.0,  # X2
                -D - k1 * d_mu1_S1 * X1,  # S1
                0.0,  # S2
                0.0,  # Z
                0.0,  # C
            ],  # dS1/dt
            [
                k2 * mu1,  # X1
                -k3 * mu2,  # X2
                k2 * d_mu1_S1 * X1,  # S1
                -D - k3 * d_mu2_S2 * X2,  # S2
                0.0,  # Z
                0.0,  # C
            ],  # dS2/dt
            [
                0.0,  # X1
                0.0,  # X2
                0.0,  # S1
                0.0,  # S2
                -D,  # Z
                0.0,  # C
            ],  # dZ/dt
            [
                k4 * mu1,  # X1
                k5 * mu2 - d_qC_X2,  # X2
                k4 * d_mu1_S1 * X1,  # S1
                k5 * d_mu2_S2 * X2 - d_qC_S2,  # S2
                0.0,  # Z
                -D - d_qC_C,  # C
            ],  # dC/dt
        ]
    )

    y_matrix = np.ascontiguousarray(y[6:]).reshape((6, 5))
    der_state_param_t = (der_state_t_state @ y_matrix).flatten()

    der = np.zeros(36)
    der[:6] = der_state_t
    der[6:] = der_state_param_t + der_state_t_param
    return der


@nb.njit(
    nbt.Tuple((nbt.f2D,nbt.b))(
        nbt.f1D, #y0: np.ndarray,
        nbt.f, # dt:float,
        nbt.i, # n_t:int,
        nbt.f1D, # t_evals:np.ndarray,
        nbt.f1D, # t_coeffs:np.ndarray,
        nbt.f2D, # A_coeffs:np.ndarray,
        nbt.f1D, # b0:np.ndarray,
        nbt.f1D, # b1:np.ndarray,
        nbt.i, # order:int,
        nbt.f, # tol:float,
        nbt.f, # dt_min:float,
        nbt.f1D,  # ts
        nbt.f1D,  # Ds
        nbt.f1D,  # S1_ins
        nbt.f1D,  # S2_ins
        nbt.f1D,  # Z_ins
        nbt.f1D,  # C_ins
        nbt.f1D,  # pHs
        nbt.f,  # mu1max
        nbt.f,  # KS1
        nbt.f,  # mu2max
        nbt.f,  # KS2
        nbt.f,  # KI2
    )
)
def am2_ode_with_der_solve(
    y0: np.ndarray,
    dt:float,
    n_t:int,
    t_evals:np.ndarray,
    t_coeffs:np.ndarray,
    A_coeffs:np.ndarray,
    b0:np.ndarray,
    b1:np.ndarray,
    order:int,
    tol:float,
    dt_min:float,
    # Intrant description
    ts: np.ndarray,
    Ds: np.ndarray,
    S1_ins: np.ndarray,
    S2_ins: np.ndarray,
    Z_ins: np.ndarray,
    C_ins: np.ndarray,
    pHs: np.ndarray,
    # Parameter description
    mu1max: float,
    KS1: float,
    mu2max: float,
    KS2: float,
    KI2: float,
):

    reached_dt_min = False
    y = y0
    n_y = len(y)
    t = ts[0]
    
    res = np.zeros((len(t_evals), n_y))
    res[0] = y0

    for count, t_goal in enumerate(t_evals):
        # The goal is to evaluate the solution of the ODE at all time specified in ts
        # We assume that the time index specified in ts is increasing
        # Currently we store the value obtained the first time after crossing the index
        # (i.e. this not exactly computed at the time index).
        # We will change the code so that we compute the value at the time index exactly
        # later on.

        # Continue til you cross approach
        while t < t_goal:

            # This is the main code for Runge Kutta embedded version
            k = np.zeros((n_t, n_y))
            for i in range(n_t):
                sum_k = np.zeros(n_y)
                for j in range(i):
                    sum_k += A_coeffs[i,j] * k[j]

                loc_state = y  + sum_k
                dy_dt = am2_ode_with_der(
                    t=t+ t_coeffs[i] * dt,
                    y = loc_state,
                    ts=ts,
                    Ds=Ds,
                    S1_ins=S1_ins,
                    S2_ins=S2_ins,
                    Z_ins=Z_ins,
                    C_ins=C_ins,
                    pHs=pHs,
                    mu1max=mu1max,
                    KS1=KS1,
                    mu2max=mu2max,
                    KS2=KS2,
                    KI2=KI2,
                )
                k[i] = dt * dy_dt

            ye0 = y + np.dot(b0, k)
            ye1 = y + np.dot(b1, k)

            error = np.sqrt(np.sum((ye1-ye0)**2))

            if error <= tol:
                y = ye0
                t+= dt

                dt_new = 0.9 * dt * (tol/error) ** (1/ order)
                dt = min(dt_new, dt * 2)
            else:
                dt_new = 0.5 * dt
                if dt_new < dt_min:
                    reached_dt_min = True
                    dt = dt_min
                else:
                    dt = dt_new

        # Store value
        res[count] = y 
            
    return res, reached_dt_min


def am2_with_der(
    # Param
    mu1max: float,
    mu2max: float,
    KS1: float,
    KS2: float,
    KI2: float,
    # Solving ODE specs
    n_t:int,
    t_coeffs:np.ndarray,
    A_coeffs:np.ndarray,
    b0:np.ndarray,
    b1:np.ndarray,
    order:int,
    tol:float,
    # Feed
    ts: np.ndarray,
    Ds: np.ndarray,
    S1_ins: np.ndarray,
    S2_ins: np.ndarray,
    Z_ins: np.ndarray,
    C_ins: np.ndarray,
    pHs: np.ndarray,
    # Initial state
    X1_0: float,
    X2_0: float,
    S1_0: float,
    S2_0: float,
    Z_0: float,
    C_0: float,
    # Other hypeparameters
    dt:float = 5/ (24* 60),
    min_step: float = (0.5)/ (24* 60),
) -> np.ndarray:
    # Get index at the end of each day
    keep_index = day_index(ts)

    # Initial state to array
    initial_state = np.array([X1_0, X2_0, S1_0, S2_0, Z_0, C_0])

    ini_solver = np.zeros(36)
    ini_solver[:6] = initial_state

    _out, reached_dt_min = am2_ode_with_der_solve(
        y0=ini_solver, 
        dt=dt,
        n_t=n_t,
        t_evals=ts[keep_index],
        t_coeffs=t_coeffs,
        A_coeffs=A_coeffs,
        b0=b0,
        b1=b1,
        order=order,
        tol=tol,
        dt_min=min_step,
        # Intrant description
        ts=ts,
        Ds=Ds,
        S1_ins=S1_ins,
        S2_ins=S2_ins,
        Z_ins=Z_ins,
        C_ins=C_ins,
        pHs=pHs,
        # Parameter description
        mu1max=mu1max,
        KS1=KS1,
        mu2max=mu2max,
        KS2=KS2,
        KI2=KI2,
        )
    out = _out.T


    der_out = out[6:].reshape((6, 5, out.shape[1]))

    vect0 = np.zeros(out.shape[1])

    X2, S2, C = out[1], out[3], out[5]
    der_X2, der_S2, der_C = der_out[1].T, der_out[3].T, der_out[5].T

    mu2 = mu2max * (S2 / (KS2 + S2 * (1 + S2 / KI2)) - 0.1)

    d_mu2_mu2max = S2 / (KS2 + S2 * (1 + S2 / KI2)) - 0.1
    d_mu2_KS2 = -mu2max * S2 / (KS2 + S2 * (1 + S2 / KI2)) ** 2
    d_mu2_KI2 = mu2max * (S2**3 / (KI2 * (KS2 + S2) + S2**2) ** 2)

    d_mu2_S2 = mu2max * (
        1 / (KS2 + S2 * (1 + S2 / KI2))
        - S2 * (1 + 2 * S2 / KI2) / (KS2 + S2 * (1 + S2 / KI2)) ** 2
    )

    der_mu2 = np.array(
        [vect0, d_mu2_mu2max, vect0, d_mu2_KS2, d_mu2_KI2]
    )  # Change 0 into lists of adequate shape
    qM = k6 * mu2 * X2

    der_qM = (k6 * mu2 * der_X2.T + k6 * (der_mu2 + d_mu2_S2 * der_S2.T) * X2).T

    CO2 = C / (1 + 10 ** (pHs[keep_index] - pKb))
    der_CO2 = (der_C.T / (1 + 10 ** (pHs[keep_index] - pKb))).T

    # CO2 = out[5] + out[3] - out[4]
    # der_CO2 = der_C + der_S2 - der_out[4].T

    phi = CO2 + KH * P_T + qM / kLa
    der_phi = der_CO2 + der_qM / kLa

    KH_PC = (phi - np.sqrt(phi**2 - 4 * KH * P_T * CO2)) / 2

    d_KHPC_phi = (1 - phi / np.sqrt(phi**2 - 4 * KH * P_T * CO2)) / 2
    d_KHPC_CO2 = KH * P_T / (np.sqrt(phi**2 - 4 * KH * P_T * CO2))

    der_KHPC = (d_KHPC_phi * der_phi.T + d_KHPC_CO2 * der_CO2.T).T

    qC = kLa * (CO2 - KH_PC)

    der_qC = kLa * (der_CO2 - der_KHPC)

    derivative = np.zeros((8, 5, out.shape[1]))

    derivative[:6] = out[6:].reshape((6, 5, out.shape[1]))
    derivative[6] = der_qM.T
    derivative[7] = der_qC.T

    return (
        np.array(
            [ts[keep_index], out[0], out[1], out[2], out[3], out[4], out[5], qM, qC]
        ).T,
        np.transpose(derivative, (1, 2, 0)),
        reached_dt_min
    )

# def am2_with_der(
#     # parameter
#     mu1max: float,
#     mu2max: float,
#     KS1: float,
#     KS2: float,
#     KI2: float,
#     # Influent
#     ts: np.ndarray,
#     Ds: np.ndarray,
#     S1_ins: np.ndarray,
#     S2_ins: np.ndarray,
#     Z_ins: np.ndarray,
#     C_ins: np.ndarray,
#     pHs: np.ndarray,
#     # Initial state
#     X1_0: float,
#     X2_0: float,
#     S1_0: float,
#     S2_0: float,
#     Z_0: float,
#     C_0: float,
#     # Other hyperparams
#     solver_method: str = "LSODA",
#     min_step: float = 10**-4,
#     **kwargs,
# ) -> tuple[np.ndarray, np.ndarray]:

#     # Read time
#     keep_index = day_index(ts)

#     # Initial state to array
#     initial_state = np.array([X1_0, X2_0, S1_0, S2_0, Z_0, C_0])

#     # Find max step_size
#     if "max_step" not in kwargs.keys():
#         # At least an evaluation every quarter of an hour for stability
#         max_step = max(min(np.min(ts[1:] - ts[:-1]), 1 / 96), 20 / (96 * 60))
#         kwargs["max_step"] = max_step

#     # Check max_step > min_step
#     if kwargs["max_step"] < min_step:
#         warnings.warn(
#             "Minimal step larger than maximum step. Setting min step to .5 * max step",
#             category=ParamHandling,
#         )
#         min_step = kwargs["max_step"] / 2

#     # Call to scipy ODE solver
#     ini_solver = np.zeros(36)
#     ini_solver[:6] = initial_state
#     res = si.solve_ivp(
#         am2_ode_with_der,
#         t_span=(ts[0], ts[-1]),
#         y0=ini_solver,
#         t_eval=ts[keep_index],
#         method=solver_method,
#         min_step=min_step,
#         args=(
#             ts,
#             Ds,
#             S1_ins,
#             S2_ins,
#             Z_ins,
#             C_ins,
#             pHs,
#             mu1max,
#             KS1,
#             mu2max,
#             KS2,
#             KI2,
#         ),
#         **kwargs,
#     )

#     # Recompute the values of qM, qC
#     out = res.y
#     der_out = out[6:].reshape((6, 5, out.shape[1]))

#     vect0 = np.zeros(out.shape[1])

#     X2, S2, C = out[1], out[3], out[5]
#     der_X2, der_S2, der_C = der_out[1].T, der_out[3].T, der_out[5].T

#     mu2 = mu2max * (S2 / (KS2 + S2 * (1 + S2 / KI2)) - 0.1)

#     d_mu2_mu2max = S2 / (KS2 + S2 * (1 + S2 / KI2)) - 0.1
#     d_mu2_KS2 = -mu2max * S2 / (KS2 + S2 * (1 + S2 / KI2)) ** 2
#     d_mu2_KI2 = mu2max * (S2**3 / (KI2 * (KS2 + S2) + S2**2) ** 2)

#     d_mu2_S2 = mu2max * (
#         1 / (KS2 + S2 * (1 + S2 / KI2))
#         - S2 * (1 + 2 * S2 / KI2) / (KS2 + S2 * (1 + S2 / KI2)) ** 2
#     )

#     der_mu2 = np.array(
#         [vect0, d_mu2_mu2max, vect0, d_mu2_KS2, d_mu2_KI2]
#     )  # Change 0 into lists of adequate shape
#     qM = k6 * mu2 * X2

#     der_qM = (k6 * mu2 * der_X2.T + k6 * (der_mu2 + d_mu2_S2 * der_S2.T) * X2).T

#     CO2 = C / (1 + 10 ** (pHs[keep_index] - pKb))
#     der_CO2 = (der_C.T / (1 + 10 ** (pHs[keep_index] - pKb))).T

#     # CO2 = out[5] + out[3] - out[4]
#     # der_CO2 = der_C + der_S2 - der_out[4].T

#     phi = CO2 + KH * P_T + qM / kLa
#     der_phi = der_CO2 + der_qM / kLa

#     KH_PC = (phi - np.sqrt(phi**2 - 4 * KH * P_T * CO2)) / 2

#     d_KHPC_phi = (1 - phi / np.sqrt(phi**2 - 4 * KH * P_T * CO2)) / 2
#     d_KHPC_CO2 = KH * P_T / (np.sqrt(phi**2 - 4 * KH * P_T * CO2))

#     der_KHPC = (d_KHPC_phi * der_phi.T + d_KHPC_CO2 * der_CO2.T).T

#     qC = kLa * (CO2 - KH_PC)

#     der_qC = kLa * (der_CO2 - der_KHPC)

#     derivative = np.zeros((8, 5, out.shape[1]))

#     derivative[:6] = out[6:].reshape((6, 5, out.shape[1]))
#     derivative[6] = der_qM.T
#     derivative[7] = der_qC.T

#     return (
#         np.array(
#             [ts[keep_index], out[0], out[1], out[2], out[3], out[4], out[5], qM, qC]
#         ).T,
#         np.transpose(derivative, (1, 2, 0)),
#     )


# def am2_derivative(
#     # parameter
#     mu1max: float,
#     mu2max: float,
#     KS1: float,
#     KS2: float,
#     KI2: float,
#     # Influent
#     ts: np.ndarray,
#     Ds: np.ndarray,
#     S1_ins: np.ndarray,
#     S2_ins: np.ndarray,
#     Z_ins: np.ndarray,
#     C_ins: np.ndarray,
#     pHs: np.ndarray,
#     # Initial state
#     X1_0: float,
#     X2_0: float,
#     S1_0: float,
#     S2_0: float,
#     Z_0: float,
#     C_0: float,
#     # Extra arguments
#     log_am2: bool = True,
#     am2_out: Optional[np.ndarray] = None,  # pylint: disable=W0613
#     rel_step: Optional[float] = None,  # pylint: disable=W0613
#     parallel: bool = True,  # pylint: disable=W0613
#     **kwargs,
# ) -> np.ndarray:
#     """
#     Compute the Jacobian of (log-)AM2 close to param
#     for parameters dimension in params_to_der. Time output is dropped.

#     The derivative with respect to the parameter is computed by solving an ODE with scipy.
#     See documentation of am2_with_der function.

#     Some disregarded parameters are included to keep the notations coherent with ADM1 - for which
#     a numeric derivation scheme is used.

#     Args:
#         - param, the parameter at which the derivative of AM2 is to be computed
#         - params_to_der, the list of parameter dimensions on which to compute the derivative
#         - digester_info, solver_method -> see run_am2 doc
#         - log_am2: if False, computes the derivative of AM2, if True, computes the derivative of
#             log(AM2). True by default.
#         - am2_out: Optional output of AM2 at param (even if log_am2 is True). Disregarded
#         - rel_step, parallel: disregarded (kept for similarity with ADM1 module)

#     Returns:
#         The jacobian in shape P, T, K (P number of parameters, T number of time points, K number of observations)
#     """
#     # Compute derivative
#     preds, der_preds = am2_with_der(
#         # Parameter
#         mu1max=mu1max,
#         KS1=KS1,
#         mu2max=mu2max,
#         KS2=KS2,
#         KI2=KI2,
#         # Feed
#         ts=ts,
#         Ds=Ds,
#         S1_ins=S1_ins,
#         S2_ins=S2_ins,
#         Z_ins=Z_ins,
#         C_ins=C_ins,
#         pHs=pHs,
#         # Initial state
#         X1_0=X1_0,
#         X2_0=X2_0,
#         S1_0=S1_0,
#         S2_0=S2_0,
#         Z_0=Z_0,
#         C_0=C_0,
#         **kwargs,
#     )

#     if log_am2:
#         der_preds = der_preds / preds[:, 1:]

#     return der_preds
