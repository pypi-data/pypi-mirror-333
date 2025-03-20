"""
Modelisation of Anaerobic digestion with AM2

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


Main Input:
    param, description of the microbiology which is to be calibrated
    influent_state, description of what is fed the digester
    initial_state, description of what is inside the digester at the beginning
Further argument:
    solver_method, the solver by scipy to solve the ODE. Default is LSODA
    min_step, the minimal time increment for the solver (to avoid long simulation time)
    max_step, the maximum time increment for the solver (to force good precision)
"""

import warnings

import anaerodig.nb_typ as nbt
import numba as nb
import numpy as np
import scipy.integrate as si

# ------------ Prepare constants ------------

# Hassam 2015
# k1 = 23.0 # gCOD gVS^{-1}
# k2 = 464.0 # mmol gVS^{-1}
# k3 = 514.0 # mmol gVS^{-1}
# k4 = 310.0 # mmol gVS^{-1}
# k5 = 600.0 # mmol gVS^{-1}
# k6 = 253.0 # mmol gVS^{-1}

# kLa = 24.0 # day-1

# Bernard 2001
k1 = 42.14  # gCOD gVS^{-1}
k2 = 116.5  # mmol gVS^{-1}
k3 = 268.0  # mmol gVS^{-1}
k4 = 50.6  # mmol gVS^{-1}
k5 = 343.6  # mmol gVS^{-1}
k6 = 453.0  # mmol gVS^{-1}

kLa = 19.8  # day-1

KH = 26.7  # mmol L^{-1} atm^{-1}
pKb = -np.log10(6.5 * 10 ** (-7))  # Kb in mol/L

P_T = 1.0  # bar \simeq 1 atm

alpha = 1.0

# ------------ helper functions ------------


def day_index(ts: np.ndarray):
    """Given time stamps ts (in float), returns index where a new day is started"""
    u = np.zeros(len(ts), dtype=int)
    loc_day = int(ts[0]) + 1
    compt = 0
    for i, t in enumerate(ts):
        if t >= loc_day:
            u[compt] = i
            loc_day += 1
            compt += 1
    return u[:compt]


@nb.njit(
    nbt.f1D(
        nbt.f,
        nbt.f1D,  # y
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
def am2_ode(
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
    dS/dt (t) = am2_ode(t, S)
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
    X1, X2, S1, S2, Z, C = y

    # Compute intermediary
    mu1 = mu1max * (S1 / (KS1 + S1) - 0.1)  # D-1  # Hassam Eq 6
    mu2 = mu2max * (S2 / (KS2 + S2 * (1 + S2 / KI2)) - 0.1)  # D-1 # Hassam Eq 7

    qM = k6 * mu2 * X2  # mmol L-1 D-1 # Bernard Eq 28
    CO2 = C / (1 + 10 ** (pH - pKb))  # Alternative to Bernard used since pH is known

    phi = CO2 + KH * P_T + qM / kLa  # mmol L-1 # Below Bernard Eq 27 + Bernard Eq 19

    KH_PC = (phi - np.sqrt(phi**2 - 4 * KH * P_T * CO2)) / 2  # mmol L-1 # from Eq 27

    qC = kLa * (CO2 - KH_PC)  # mmol L-1 D-1 # from Bernard Eq 26 + Bernard Eq 19

    return np.array(
        [
            (mu1 - alpha * D) * X1,  # dX1 # g L-1 D-1 # Bernard Eq 20
            (mu2 - alpha * D) * X2,  # dX2 # mmol L-1 D-1 # Bernard Eq 21
            D * (S1_in - S1) - k1 * mu1 * X1,  # dS1 # gCod L-1 D-1 # Bernard Eq 23
            D * (S2_in - S2)
            + k2 * mu1 * X1
            - k3 * mu2 * X2,  # dS2 # mmol L-1 D-1 # Bernard Eq 24
            D * (Z_in - Z),  # dZ # mmol L-1 D-1 # Bernard Eq 22
            D * (C_in - C)
            - qC
            + k4 * mu1 * X1
            + k5 * mu2 * X2,  # dC # mmol L-1 D-1 # Bernard Eq 25
        ]
    )


class ParamHandling(Warning):
    pass


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
def am2_ode_solve(
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
                dy_dt = am2_ode(
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




# ------------ Main function ------------
def run_am2(
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
    """
    Models digester evolution using AM2.

    Default solver for differential equation is LSODA.
    The step size is inferred from the feed file, with a maximum value of 15 minute, and a minum value of 20 seconds

    Output is a np.ndarray.
        First column is time (one information per day),
        Remaining columns are
            "X1", in gVS L-1 # conc. acidogenic bacteria
            "X2", in gVS L-1 # conc. methanogenic bacteria
            "S1", in gCOD L-1 # conc. substrate
            "S2", in mmol L-1 # conc. VFA
            "Z", in mmol L-1 # tot. alkalinity
            "C", in mmol L-1 # tot. inorg carbon conc.
            "qm", in mmol L-1 Day-1 # methane flow
            "qc", in mmol L-1 Day-1 # carbon dioxide flow
    """
    # Get index at the end of each day
    keep_index = day_index(ts)

    # Initial state to array
    initial_state = np.array([X1_0, X2_0, S1_0, S2_0, Z_0, C_0])

    # Call to scipy ODE solver
    out, reached_dt_min = am2_ode_solve(
        y0 = initial_state, 
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

    mu2 = mu2max * (out[:,3] / (KS2 + out[:,3] * (1 + out[:,3] / KI2)) - 0.1)
    qM = k6 * mu2 * out[:,1]

    CO2 = out[:,5] / (1 + 10 ** (pHs[keep_index] - pKb))
    # CO2 = out[5] + out[3] - out[4]
    phi = CO2 + KH * P_T + qM / kLa

    KH_PC = (phi - np.sqrt(phi**2 - 4 * KH * P_T * CO2)) / 2

    qC = kLa * (CO2 - KH_PC)

    return np.array(
        [ts[keep_index], out[:,0], out[:,1], out[:,2], out[:,3], out[:,4], out[:,5], qM, qC]
    ).T, reached_dt_min



# # ------------ Main function ------------
# def run_am2(
#     # Param
#     mu1max: float,
#     mu2max: float,
#     KS1: float,
#     KS2: float,
#     KI2: float,
#     # Feed
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
#     # Other hyparameters
#     solver_method: str = "LSODA",
#     min_step: float = 10**-4,
#     **kwargs
# ) -> np.ndarray:
#     """
#     Models digester evolution using AM2.

#     Default solver for differential equation is LSODA.
#     The step size is inferred from the feed file, with a maximum value of 15 minute, and a minum value of 20 seconds

#     Output is a np.ndarray.
#         First column is time (one information per day),
#         Remaining columns are
#             "X1", in gVS L-1 # conc. acidogenic bacteria
#             "X2", in gVS L-1 # conc. methanogenic bacteria
#             "S1", in gCOD L-1 # conc. substrate
#             "S2", in mmol L-1 # conc. VFA
#             "Z", in mmol L-1 # tot. alkalinity
#             "C", in mmol L-1 # tot. inorg carbon conc.
#             "qm", in mmol L-1 Day-1 # methane flow
#             "qc", in mmol L-1 Day-1 # carbon dioxide flow
#     """
#     # Get index at the end of each day
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
#     res = si.solve_ivp(
#         am2_ode,
#         t_span=(ts[0], ts[-1]),
#         y0=np.array(initial_state),
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

#     mu2 = mu2max * (out[3] / (KS2 + out[3] * (1 + out[3] / KI2)) - 0.1)
#     qM = k6 * mu2 * out[1]

#     CO2 = out[5] / (1 + 10 ** (pHs[keep_index] - pKb))
#     # CO2 = out[5] + out[3] - out[4]
#     phi = CO2 + KH * P_T + qM / kLa

#     KH_PC = (phi - np.sqrt(phi**2 - 4 * KH * P_T * CO2)) / 2

#     qC = kLa * (CO2 - KH_PC)

#     return np.array(
#         [ts[keep_index], out[0], out[1], out[2], out[3], out[4], out[5], qM, qC]
#     ).T
