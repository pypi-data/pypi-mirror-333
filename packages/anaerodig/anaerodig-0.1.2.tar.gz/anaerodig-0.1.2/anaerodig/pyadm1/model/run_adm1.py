
import anaerodig.nb_typ as nbt
import numba as nb
import numpy as np
from anaerodig.pyadm1.model.helpers import adm1_ode, N_DAY_VSR
from anaerodig.pyadm1.basic_classes.feed import (
    feed_idx_Q,
    feed_idx_S_aa,
    feed_idx_S_ac,
    feed_idx_S_anion,
    feed_idx_S_bu,
    feed_idx_S_cation,
    feed_idx_S_ch4,
    feed_idx_S_fa,
    feed_idx_S_h2,
    feed_idx_S_I,
    feed_idx_S_IC,
    feed_idx_S_IN,
    feed_idx_S_pro,
    feed_idx_S_su,
    feed_idx_S_va,
    feed_idx_T_op,
    feed_idx_time,
    feed_idx_X_aa,
    feed_idx_X_ac,
    feed_idx_X_c,
    feed_idx_X_c4,
    feed_idx_X_ch,
    feed_idx_X_fa,
    feed_idx_X_h2,
    feed_idx_X_I,
    feed_idx_X_li,
    feed_idx_X_pr,
    feed_idx_X_pro,
    feed_idx_X_su,
)
from anaerodig.pyadm1.basic_classes.Phy import R, p_atm
from anaerodig.pyadm1.basic_classes.state import (
    n_pred_col,
    ode_idx_pH,
    ode_idx_S_gas_ch4,
    ode_idx_S_gas_co2,
    ode_idx_S_gas_h2,
    ode_states_idx_in_initial_state,
    ode_states_idx_in_pred,
    pred_idx_p_ch4,
    pred_idx_p_co2,
    pred_idx_pH,
    pred_idx_q_ch4,
    pred_idx_q_gas,
    pred_idx_S_co2,
    pred_idx_S_hco3_ion,
    pred_idx_S_IC,
    pred_idx_S_IN,
    pred_idx_S_nh3,
    pred_idx_S_nh4_ion,
    pred_idx_VS,
    pred_idx_VS_in,
    pred_idx_VSR,
    time_idx_initial_state,
)
from anaerodig.pyadm1.model.vs_computation import dig_states_vs, feed_vs, volume_per_day


@nb.njit(
    nbt.Tuple((nbt.f1D, nbt.b, nbt.f))(
        nbt.f1D, # state_zero: np.ndarray,
        nbt.f,   # t0:float,
        nbt.f,   # t1:float,
        nbt.f,   # dt:float,
        nbt.i,   # n_t:int, 
        nbt.f1D, # t_coeffs:np.ndarray,
        nbt.f2D, # A_coeffs:np.ndarray,
        nbt.f1D, # b0:np.ndarray,
        nbt.f1D, # b1:np.ndarray,
        nbt.i,  # order:int,
        nbt.f,  # tol:float,
        nbt.f,  # dt_min:float,
        nbt.f,  # K_pH_aa: float,
        nbt.f,  # nn_aa: float,
        nbt.f,  # K_pH_h2: float,
        nbt.f,  # n_h2: float,
        nbt.f,  # K_pH_ac:float,
        nbt.f,  # n_ac:float,
        nbt.f,  # K_S_IN,
        nbt.f,  # K_I_h2_fa,
        nbt.f,  # K_H_h2,
        nbt.f,  # K_I_h2_c4,
        nbt.f,  # K_I_h2_pro,
        nbt.f,  # K_I_nh3,
        nbt.f,  # k_dis,
        nbt.f,  # k_hyd_ch,
        nbt.f,  # k_hyd_pr,
        nbt.f,  # k_hyd_li,
        nbt.f,  # k_m_su,
        nbt.f,  # K_S_su,
        nbt.f,  # k_m_aa,
        nbt.f,  # K_S_aa,
        nbt.f,  # k_m_pro: float,
        nbt.f,  # K_S_pro: float,
        nbt.f,  # k_m_fa: float,
        nbt.f,  # K_S_fa: float,
        nbt.f,  # k_m_c4,
        nbt.f,  # K_S_c4,
        nbt.f,  # k_m_ac,
        nbt.f,  # K_S_ac,
        nbt.f,  # k_dec: float,
        nbt.f,  # k_m_h2: float,
        nbt.f,  # K_S_h2: float,
        nbt.f,  # T_op: float,
        nbt.f,  # p_gas_h2o,
        nbt.f,  # V_liq: float,
        nbt.f,  # ratio_q_ad_V_liq: float,
        nbt.f,  # K_H_ch4,
        nbt.f,  # K_H_co2,
        nbt.f,  # S_su_in,
        nbt.f,  # S_aa_in,
        nbt.f,  # S_fa_in,
        nbt.f,  # S_va_in,
        nbt.f,  # S_bu_in,
        nbt.f,  # S_pro_in,
        nbt.f,  # S_ac_in,
        nbt.f,  # S_ch4_in,
        nbt.f,  # s_1,
        nbt.f,  # s_2,
        nbt.f,  # s_3,
        nbt.f,  # s_4,
        nbt.f,  # s_5,
        nbt.f,  # s_6,
        nbt.f,  # s_7,
        nbt.f,  # s_8,
        nbt.f,  # s_9,
        nbt.f,  # s_10,
        nbt.f,  # s_11,
        nbt.f,  # s_12,
        nbt.f,  # s_13,
        nbt.f,  # V_gas,
        nbt.f,  # S_IC_in,
        nbt.f,  # S_IN_in,
        nbt.f,  # S_I_in,
        nbt.f,  # X_c_in,
        nbt.f,  # X_ch_in,
        nbt.f,  # X_pr_in,
        nbt.f,  # X_li_in,
        nbt.f,  # X_su_in,
        nbt.f,  # X_aa_in,
        nbt.f,  # X_fa_in,
        nbt.f,  # X_c4_in,
        nbt.f,  # X_pro_in,
        nbt.f,  # X_ac_in,
        nbt.f,  # X_h2_in,
        nbt.f,  # X_I_in,
        nbt.f,  # S_cation_in,
        nbt.f,  # S_anion_in,
        nbt.f,  # N_xc
        nbt.f,  # N_I
        nbt.f,  # N_aa
        nbt.f,  # N_bac
        nbt.f,  # f_sI_xc
        nbt.f,  # f_xI_xc
        nbt.f,  # f_ch_xc
        nbt.f,  # f_pr_xc
        nbt.f,  # f_li_xc
        nbt.f,  # f_fa_li
        nbt.f,  # f_bu_su
        nbt.f,  # f_pro_su
        nbt.f,  # f_ac_su
        nbt.f,  # f_va_aa
        nbt.f,  # f_bu_aa
        nbt.f,  # f_pro_aa
        nbt.f,  # f_ac_aa
        nbt.f,  # Y_su
        nbt.f,  # Y_aa
        nbt.f,  # Y_fa
        nbt.f,  # Y_c4
        nbt.f,  # Y_pro
        nbt.f,  # Y_ac
        nbt.f,  # Y_h2
        nbt.f,  # k_p
        nbt.f,  # k_L_a
    )
)
def adm1_ode_solve(
    state_zero: np.ndarray,
    t0:float,
    t1:float,
    dt:float,
    n_t:int, 
    t_coeffs:np.ndarray,
    A_coeffs:np.ndarray,
    b0:np.ndarray,
    b1:np.ndarray,
    order:int,
    tol:float,
    dt_min:float,
    # Parameter description
    K_pH_aa: float,
    nn_aa: float,
    K_pH_h2: float,
    n_h2: float,
    K_pH_ac: float,
    n_ac: float,
    K_S_IN: float,
    K_I_h2_fa: float,
    K_H_h2: float,
    K_I_h2_c4: float,
    K_I_h2_pro: float,
    K_I_nh3: float,
    k_dis: float,
    k_hyd_ch: float,
    k_hyd_pr: float,
    k_hyd_li: float,
    k_m_su: float,
    K_S_su: float,
    k_m_aa: float,
    K_S_aa: float,
    k_m_pro: float,
    K_S_pro: float,
    k_m_fa: float,
    K_S_fa: float,
    k_m_c4: float,
    K_S_c4: float,
    k_m_ac: float,
    K_S_ac: float,
    k_dec: float,
    k_m_h2: float,
    K_S_h2: float,
    T_op: float,
    p_gas_h2o: float,
    V_liq: float,
    ratio_q_ad_V_liq: float,
    K_H_ch4: float,
    K_H_co2: float,
    S_su_in: float,
    S_aa_in: float,
    S_fa_in: float,
    S_va_in: float,
    S_bu_in: float,
    S_pro_in: float,
    S_ac_in: float,
    S_ch4_in: float,
    s_1: float,
    s_2: float,
    s_3: float,
    s_4: float,
    s_5: float,
    s_6: float,
    s_7: float,
    s_8: float,
    s_9: float,
    s_10: float,
    s_11: float,
    s_12: float,
    s_13: float,
    V_gas: float,
    # Influent description
    S_IC_in: float,
    S_IN_in: float,
    S_I_in: float,
    X_c_in: float,
    X_ch_in: float,
    X_pr_in: float,
    X_li_in: float,
    X_su_in: float,
    X_aa_in: float,
    X_fa_in: float,
    X_c4_in: float,
    X_pro_in: float,
    X_ac_in: float,
    X_h2_in: float,
    X_I_in: float,
    S_cation_in: float,
    S_anion_in: float,
    # New parameters
    N_xc: float,
    N_I: float,
    N_aa: float,
    N_bac: float,
    f_sI_xc: float,
    f_xI_xc: float,
    f_ch_xc: float,
    f_pr_xc: float,
    f_li_xc: float,
    f_fa_li: float,
    f_bu_su: float,
    f_pro_su: float,
    f_ac_su: float,
    f_va_aa: float,
    f_bu_aa: float,
    f_pro_aa: float,
    f_ac_aa: float,
    Y_su: float,
    Y_aa: float,
    Y_fa: float,
    Y_c4: float,
    Y_pro: float,
    Y_ac: float,
    Y_h2: float,
    k_p: float,
    k_L_a: float,   
):
    
    reached_dt_min = False
    y = state_zero
    n_y = len(y)
    t = t0

    while t < t1:
        if t + dt > t1:
            dt = t1 - t

        k = np.zeros((n_t, n_y))
        for i in range(n_t):
            sum_k = np.zeros(n_y)
            for j in range(i):
                sum_k += A_coeffs[i,j] * k[j]

            loc_state = y  + sum_k

            
            dy_dt = adm1_ode(
                t=t+ t_coeffs[i] * dt,
                state_zero=loc_state,
                K_pH_aa=K_pH_aa,
                nn_aa=nn_aa,
                K_pH_h2=K_pH_h2,
                n_h2=n_h2,
                K_pH_ac=K_pH_ac,
                n_ac=n_ac,
                K_S_IN=K_S_IN,
                K_I_h2_fa=K_I_h2_fa,
                K_H_h2=K_H_h2,
                K_I_h2_c4=K_I_h2_c4,
                K_I_h2_pro=K_I_h2_pro,
                K_I_nh3=K_I_nh3,
                k_dis=k_dis,
                k_hyd_ch=k_hyd_ch,
                k_hyd_pr=k_hyd_pr,
                k_hyd_li=k_hyd_li,
                k_m_su=k_m_su,
                K_S_su=K_S_su,
                k_m_aa=k_m_aa,
                K_S_aa=K_S_aa,
                k_m_pro=k_m_pro,
                K_S_pro=K_S_pro,
                k_m_fa=k_m_fa,
                K_S_fa=K_S_fa,
                k_m_c4=k_m_c4,
                K_S_c4=K_S_c4,
                k_m_ac=k_m_ac,
                K_S_ac=K_S_ac,
                k_dec=k_dec,
                k_m_h2=k_m_h2,
                K_S_h2=K_S_h2,
                T_op=T_op,
                p_gas_h2o=p_gas_h2o,
                V_liq=V_liq,
                ratio_q_ad_V_liq=ratio_q_ad_V_liq,
                K_H_ch4=K_H_ch4,
                K_H_co2=K_H_co2,
                S_su_in=S_su_in,
                S_aa_in=S_aa_in,
                S_fa_in=S_fa_in,
                S_va_in=S_va_in,
                S_bu_in=S_bu_in,
                S_pro_in=S_pro_in,
                S_ac_in=S_ac_in,
                S_ch4_in=S_ch4_in,
                s_1=s_1,
                s_2=s_2,
                s_3=s_3,
                s_4=s_4,
                s_5=s_5,
                s_6=s_6,
                s_7=s_7,
                s_8=s_8,
                s_9=s_9,
                s_10=s_10,
                s_11=s_11,
                s_12=s_12,
                s_13=s_13,
                V_gas=V_gas,
                S_IC_in=S_IC_in,
                S_IN_in=S_IN_in,
                S_I_in=S_I_in,
                X_c_in=X_c_in,
                X_ch_in=X_ch_in,
                X_pr_in=X_pr_in,
                X_li_in=X_li_in,
                X_su_in=X_su_in,
                X_aa_in=X_aa_in,
                X_fa_in=X_fa_in,
                X_c4_in=X_c4_in,
                X_pro_in=X_pro_in,
                X_ac_in=X_ac_in,
                X_h2_in=X_h2_in,
                X_I_in=X_I_in,
                S_cation_in=S_cation_in,
                S_anion_in=S_anion_in,
                # New parameters
                N_xc=N_xc,
                N_I=N_I,
                N_aa=N_aa,
                N_bac=N_bac,
                f_sI_xc=f_sI_xc,
                f_xI_xc=f_xI_xc,
                f_ch_xc=f_ch_xc,
                f_pr_xc=f_pr_xc,
                f_li_xc=f_li_xc,
                f_fa_li=f_fa_li,
                f_bu_su=f_bu_su,
                f_pro_su=f_pro_su,
                f_ac_su=f_ac_su,
                f_va_aa=f_va_aa,
                f_bu_aa=f_bu_aa,
                f_pro_aa=f_pro_aa,
                f_ac_aa=f_ac_aa,
                Y_su=Y_su,
                Y_aa=Y_aa,
                Y_fa=Y_fa,
                Y_c4=Y_c4,
                Y_pro=Y_pro,
                Y_ac=Y_ac,
                Y_h2=Y_h2,
                k_p=k_p,
                k_L_a=k_L_a,
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
    return y, reached_dt_min, dt

@nb.njit(nbt.Tuple((nbt.f2D, nbt.b))(
    nbt.f2D, # influent_state: np.ndarray,
    nbt.f1D, # p_gas_h2o_s: np.ndarray,
    nbt.f1D, # K_H_co2_s: np.ndarray,
    nbt.f1D, # K_H_ch4_s: np.ndarray,
    nbt.f1D, # K_H_h2_s: np.ndarray,
    nbt.f1D, # K_a_co2_s: np.ndarray,
    nbt.f1D, # K_a_IN_s: np.ndarray,
    nbt.f1D, # K_w_s: np.ndarray,
    nbt.f1D, # V_liq_s: np.ndarray,
    nbt.f1D, # V_gas_s: np.ndarray,
    nbt.f1D, # initial_state: np.ndarray,
    nbt.f, # N_xc: float,
    nbt.f, # N_I: float,
    nbt.f, # N_aa: float,
    nbt.f, # N_bac: float,
    nbt.f, # C_xc: float,
    nbt.f, # C_sI: float,
    nbt.f, # C_ch: float,
    nbt.f, # C_pr: float,
    nbt.f, # C_li: float,
    nbt.f, # C_xI: float,
    nbt.f, # C_su: float,
    nbt.f, # C_aa: float,
    nbt.f, # C_fa: float,
    nbt.f, # C_bu: float,
    nbt.f, # C_pro: float,
    nbt.f, # C_ac: float,
    nbt.f, # C_bac: float,
    nbt.f, # C_va: float,
    nbt.f, # C_ch4: float,
    nbt.f, # K_a_va: float,
    nbt.f, # K_a_bu: float,
    nbt.f, # K_a_pro: float,
    nbt.f, # K_a_ac: float,
    nbt.f, # f_sI_xc: float,
    nbt.f, # f_xI_xc: float,
    nbt.f, # f_ch_xc: float,
    nbt.f, # f_pr_xc: float,
    nbt.f, # f_li_xc: float,
    nbt.f, # f_fa_li: float,
    nbt.f, # f_h2_su: float,
    nbt.f, # f_bu_su: float,
    nbt.f, # f_pro_su: float,
    nbt.f, # f_ac_su: float,
    nbt.f, # f_h2_aa: float,
    nbt.f, # f_va_aa: float,
    nbt.f, # f_bu_aa: float,
    nbt.f, # f_pro_aa: float,
    nbt.f, # f_ac_aa: float,
    nbt.f, # Y_su: float,
    nbt.f, # Y_aa: float,
    nbt.f, # Y_fa: float,
    nbt.f, # Y_c4: float,
    nbt.f, # Y_pro: float,
    nbt.f, # Y_ac: float,
    nbt.f, # Y_h2: float,
    nbt.f, # k_p: float,
    nbt.f, # k_L_a: float,
    nbt.f, # k_dis: float,
    nbt.f, # k_hyd_ch: float,
    nbt.f, # k_hyd_pr: float,
    nbt.f, # k_hyd_li: float,
    nbt.f, # k_m_su: float,
    nbt.f, # k_m_aa: float,
    nbt.f, # k_m_fa: float,
    nbt.f, # k_m_c4: float,
    nbt.f, # k_m_pro: float,
    nbt.f, # k_m_ac: float,
    nbt.f, # k_m_h2: float,
    nbt.f, # k_dec: float,
    nbt.f, # K_S_IN: float,
    nbt.f, # K_S_su: float,
    nbt.f, # K_S_aa: float,
    nbt.f, # K_S_fa: float,
    nbt.f, # K_S_c4: float,
    nbt.f, # K_S_pro: float,
    nbt.f, # K_S_ac: float,
    nbt.f, # K_S_h2: float,
    nbt.f, # K_I_h2_fa: float,
    nbt.f, # K_I_h2_c4: float,
    nbt.f, # K_I_h2_pro: float,
    nbt.f, # K_I_nh3: float,
    nbt.f, # pH_UL_aa: float,
    nbt.f, # pH_LL_aa: float,
    nbt.f, # pH_UL_ac: float,
    nbt.f, # pH_LL_ac: float,
    nbt.f, # pH_UL_h2: float,
    nbt.f, # pH_LL_h2: float,
    nbt.i, # n_t:int,
    nbt.f1D, # t_coeffs:np.ndarray,
    nbt.f2D, # A_coeffs:np.ndarray,
    nbt.f1D, # b0:np.ndarray,
    nbt.f1D, # b1:np.ndarray,
    nbt.i, # order:int,
    nbt.f, # tol:float=1e-5,
    nbt.f, # dt: float = 60.0 / (24.0 * 60.0),
    nbt.f, # dt_min:float = 1e-8,
    nbt.i,# n_day_vsr: int = N_DAY_VSR,  
))
def run_adm1(
    influent_state: np.ndarray,
    p_gas_h2o_s: np.ndarray,
    K_H_co2_s: np.ndarray,
    K_H_ch4_s: np.ndarray,
    K_H_h2_s: np.ndarray,
    K_a_co2_s: np.ndarray,
    K_a_IN_s: np.ndarray,
    K_w_s: np.ndarray,
    V_liq_s: np.ndarray,
    V_gas_s: np.ndarray,
    initial_state: np.ndarray,
    N_xc: float,
    N_I: float,
    N_aa: float,
    N_bac: float,
    C_xc: float,
    C_sI: float,
    C_ch: float,
    C_pr: float,
    C_li: float,
    C_xI: float,
    C_su: float,
    C_aa: float,
    C_fa: float,
    C_bu: float,
    C_pro: float,
    C_ac: float,
    C_bac: float,
    C_va: float,
    C_ch4: float,
    K_a_va: float,
    K_a_bu: float,
    K_a_pro: float,
    K_a_ac: float,
    f_sI_xc: float,
    f_xI_xc: float,
    f_ch_xc: float,
    f_pr_xc: float,
    f_li_xc: float,
    f_fa_li: float,
    f_h2_su: float,
    f_bu_su: float,
    f_pro_su: float,
    f_ac_su: float,
    f_h2_aa: float,
    f_va_aa: float,
    f_bu_aa: float,
    f_pro_aa: float,
    f_ac_aa: float,
    Y_su: float,
    Y_aa: float,
    Y_fa: float,
    Y_c4: float,
    Y_pro: float,
    Y_ac: float,
    Y_h2: float,
    k_p: float,
    k_L_a: float,
    k_dis: float,
    k_hyd_ch: float,
    k_hyd_pr: float,
    k_hyd_li: float,
    k_m_su: float,
    k_m_aa: float,
    k_m_fa: float,
    k_m_c4: float,
    k_m_pro: float,
    k_m_ac: float,
    k_m_h2: float,
    k_dec: float,
    K_S_IN: float,
    K_S_su: float,
    K_S_aa: float,
    K_S_fa: float,
    K_S_c4: float,
    K_S_pro: float,
    K_S_ac: float,
    K_S_h2: float,
    K_I_h2_fa: float,
    K_I_h2_c4: float,
    K_I_h2_pro: float,
    K_I_nh3: float,
    pH_UL_aa: float,
    pH_LL_aa: float,
    pH_UL_ac: float,
    pH_LL_ac: float,
    pH_UL_h2: float,
    pH_LL_h2: float,
    n_t:int,
    t_coeffs:np.ndarray,
    A_coeffs:np.ndarray,
    b0:np.ndarray,
    b1:np.ndarray,
    order:int,
    tol:float=1e-5,
    dt: float = 10.0 / (24.0 * 60.0),
    dt_min:float = 0.1 / (24.0 * 60.0),
    n_day_vsr: int = N_DAY_VSR,
) -> np.ndarray:
    """
    Runs ADM1 with Python.
    This function code is based on original PyADM1 package (https://github.com/CaptainFerMag/PyADM1)

    ADM1 models an anaerobic digestion process from feed data and a description of
    the microbial populations in the digester (stored in param).

    This implementation is modified to only use numpy arrays and to address issues
    of the original code. It relies on an internal function adm1_ode, which relies on
    regularly updated variables in the function environnement.

    Args:
        param: Description of the microbial population in the digester (calibration parameter)
        influent_state: Multidimensional time series describing what goes inside the digester
        initial_state: Description of what is inside the digester at time 0
        V_liq: Volume of liquid part of the digester in m3
        V_gas: Volume of the gas part of the digester in m3
        T_op: Temperature in the digester
        solver_method: Type of solver used to integrate between time steps
        log_path: where should run log be written ?

    Returns:
        A multidimensional time series describing the successive digester states. There is one state per day,
        initial state is not stored. The successive digester states are computed by integrating the ADM1
        differential equation system between time t_n and t_{n+1} using the feed information specified at t_{n+1}.
        t_0 is the time information specified by initial_state.

    Remarks:
        Will fail if two feed consecutive feed events are not either in the same day or in consecutive
        days.

    Minor issues:
        Launching scipy.solve_ivp repeatedly seems to be expensive. No simple patch due to DAE
        state solving part.
    """
    ###################################################s#############
    K_pH_aa = 10.0 ** (-1.0 * (pH_LL_aa + pH_UL_aa) / 2.0)
    nn_aa = 3.0 / (
        pH_UL_aa - pH_LL_aa
    )  # we need a differece between N_aa and n_aa to avoid typos and nn_aa refers to the n_aa in BSM2 report
    K_pH_ac = 10.0 ** (-1.0 * (pH_LL_ac + pH_UL_ac) / 2.0)
    n_ac = 3.0 / (pH_UL_ac - pH_LL_ac)
    K_pH_h2 = 10.0 ** (-1.0 * (pH_LL_h2 + pH_UL_h2) / 2.0)
    n_h2 = 3.0 / (pH_UL_h2 - pH_LL_h2)

    ## Add equation parameter
    s_1 = (
        -1.0 * C_xc
        + f_sI_xc * C_sI
        + f_ch_xc * C_ch
        + f_pr_xc * C_pr
        + f_li_xc * C_li
        + f_xI_xc * C_xI
    )
    s_2 = -1.0 * C_ch + C_su
    s_3 = -1.0 * C_pr + C_aa
    s_4 = -1.0 * C_li + (1.0 - f_fa_li) * C_su + f_fa_li * C_fa
    s_5 = (
        -1.0 * C_su
        + (1.0 - Y_su) * (f_bu_su * C_bu + f_pro_su * C_pro + f_ac_su * C_ac)
        + Y_su * C_bac
    )
    s_6 = (
        -1.0 * C_aa
        + (1.0 - Y_aa)
        * (f_va_aa * C_va + f_bu_aa * C_bu + f_pro_aa * C_pro + f_ac_aa * C_ac)
        + Y_aa * C_bac
    )
    s_7 = -1.0 * C_fa + (1.0 - Y_fa) * 0.7 * C_ac + Y_fa * C_bac
    s_8 = (
        -1.0 * C_va
        + (1.0 - Y_c4) * 0.54 * C_pro
        + (1.0 - Y_c4) * 0.31 * C_ac
        + Y_c4 * C_bac
    )
    s_9 = -1.0 * C_bu + (1.0 - Y_c4) * 0.8 * C_ac + Y_c4 * C_bac
    s_10 = -1.0 * C_pro + (1.0 - Y_pro) * 0.57 * C_ac + Y_pro * C_bac
    s_11 = -1.0 * C_ac + (1.0 - Y_ac) * C_ch4 + Y_ac * C_bac
    s_12 = (1.0 - Y_h2) * C_ch4 + Y_h2 * C_bac
    s_13 = -1.0 * C_bac + C_xc

    ############################################

    ## Create initial values
    t0 = initial_state[time_idx_initial_state]
    # Initial state elements follow the order of pred_col in helper_pd_np file
    # For internal use, the pH information is converted to concentration
    # Part of the information in initial state is disregarded (S_co2, S_nh4_ion,
    # q_gas, q_ch4, p_ch4, p_co2, VS & VSR)

    state_zero = initial_state[ode_states_idx_in_initial_state]
    state_zero[ode_idx_pH] = 10 ** (
        -state_zero[ode_idx_pH]
    )  # Converting pH to concentration

    ts = influent_state[:, feed_idx_time]

    # Number of days in feed
    day_begin = int(t0) + 1
    day_end = int(ts[-1])

    n_days = day_end - day_begin + 1

    ## Create empty accu for results
    simulate_results = np.full(shape=(n_days, n_pred_col), fill_value=np.nan)
    simulate_results[0, ode_states_idx_in_pred] = state_zero
    # columns 36, 37 and 42 are created in the end.
    # For columns 38 to 41, need to compute intermediary values
    S_gas_h2 = state_zero[ode_idx_S_gas_h2]
    S_gas_ch4 = state_zero[ode_idx_S_gas_ch4]
    S_gas_co2 = state_zero[ode_idx_S_gas_co2]

    T_op = influent_state[0, feed_idx_T_op]

    p_gas_h2 = S_gas_h2 * R * T_op / 16
    p_gas_ch4 = S_gas_ch4 * R * T_op / 64
    p_gas_co2 = S_gas_co2 * R * T_op
    p_gas = p_gas_h2 + p_gas_ch4 + p_gas_co2 + p_gas_h2o_s[0]


    simulate_results[0, pred_idx_q_gas] = k_p * (p_gas - p_atm)
    simulate_results[0, pred_idx_q_ch4] = k_p * (p_gas - p_atm) * (p_gas_ch4 / p_gas)
    simulate_results[0, pred_idx_p_ch4] = p_gas_ch4
    simulate_results[0, pred_idx_p_co2] = p_gas_co2


    ########################################################################
    ## ADM1 Ordinary Differential Equation

    ################################################################
    ## Main loop
    n = 0
    loc_day = int(t0) + 1  # Keep track of when to save information
    count_day = 0
    q_ch4_accu = 0
    q_gas_accu = 0
    p_co2_day_mean_accu = 0
    p_ch4_day_mean_accu = 0
    count_in_day = 0

    reached_dt_min=False

    for t_next in ts:
        count_in_day += 1
        ## Set up influent state
        (
            T_op,
            S_su_in,
            S_aa_in,
            S_fa_in,
            S_va_in,
            S_bu_in,
            S_pro_in,
            S_ac_in,
            S_h2_in,
            S_ch4_in,
            S_IC_in,
            S_IN_in,
            S_I_in,
            X_c_in,
            X_ch_in,
            X_pr_in,
            X_li_in,
            X_su_in,
            X_aa_in,
            X_fa_in,
            X_c4_in,
            X_pro_in,
            X_ac_in,
            X_h2_in,
            X_I_in,
            S_cation_in,
            S_anion_in,
            q_ad,
        ) = influent_state[
            n,
            np.array([
                feed_idx_T_op,
                feed_idx_S_su,
                feed_idx_S_aa,
                feed_idx_S_fa,
                feed_idx_S_va,
                feed_idx_S_bu,
                feed_idx_S_pro,
                feed_idx_S_ac,
                feed_idx_S_h2,
                feed_idx_S_ch4,
                feed_idx_S_IC,
                feed_idx_S_IN,
                feed_idx_S_I,
                feed_idx_X_c,
                feed_idx_X_ch,
                feed_idx_X_pr,
                feed_idx_X_li,
                feed_idx_X_su,
                feed_idx_X_aa,
                feed_idx_X_fa,
                feed_idx_X_c4,
                feed_idx_X_pro,
                feed_idx_X_ac,
                feed_idx_X_h2,
                feed_idx_X_I,
                feed_idx_S_cation,
                feed_idx_S_anion,
                feed_idx_Q,
            ]),
        ]  # 0 is for time and not used here

        # Unpack other feed information
        p_gas_h2o = p_gas_h2o_s[n]
        K_H_co2 = K_H_co2_s[n]
        K_H_ch4 = K_H_ch4_s[n]
        K_H_h2 = K_H_h2_s[n]
        K_a_co2 = K_a_co2_s[n]
        K_a_IN = K_a_IN_s[n]
        K_w = K_w_s[n]
        V_liq = V_liq_s[n]
        V_gas = V_gas_s[n]

        ratio_q_ad_V_liq = q_ad / V_liq

        # Run integration to next step
        simulated_results, reached_dt_min, dt = adm1_ode_solve(
            state_zero=state_zero,
            t0=t0,
            t1=t_next,
            dt=dt, 
            n_t=n_t,
            t_coeffs=t_coeffs,
            A_coeffs=A_coeffs,
            b0=b0,
            b1=b1,
            order=order,
            tol=tol,
            dt_min=dt_min,
            K_pH_aa=K_pH_aa,
            nn_aa=nn_aa,
            K_pH_h2=K_pH_h2,
            n_h2=n_h2,
            K_pH_ac=K_pH_ac,
            n_ac=n_ac,
            K_S_IN=K_S_IN,
            K_I_h2_fa=K_I_h2_fa,
            K_H_h2=K_H_h2,
            K_I_h2_c4=K_I_h2_c4,
            K_I_h2_pro=K_I_h2_pro,
            K_I_nh3=K_I_nh3,
            k_dis=k_dis,
            k_hyd_ch=k_hyd_ch,
            k_hyd_pr=k_hyd_pr,
            k_hyd_li=k_hyd_li,
            k_m_su=k_m_su,
            K_S_su=K_S_su,
            k_m_aa=k_m_aa,
            K_S_aa=K_S_aa,
            k_m_pro=k_m_pro,
            K_S_pro=K_S_pro,
            k_m_fa=k_m_fa,
            K_S_fa=K_S_fa,
            k_m_c4=k_m_c4,
            K_S_c4=K_S_c4,
            k_m_ac=k_m_ac,
            K_S_ac=K_S_ac,
            k_dec=k_dec,
            k_m_h2=k_m_h2,
            K_S_h2=K_S_h2,
            T_op=T_op,
            p_gas_h2o=p_gas_h2o,
            V_liq=V_liq,
            ratio_q_ad_V_liq=ratio_q_ad_V_liq,
            K_H_ch4=K_H_ch4,
            K_H_co2=K_H_co2,
            S_su_in=S_su_in,
            S_aa_in=S_aa_in,
            S_fa_in=S_fa_in,
            S_va_in=S_va_in,
            S_bu_in=S_bu_in,
            S_pro_in=S_pro_in,
            S_ac_in=S_ac_in,
            S_ch4_in=S_ch4_in,
            s_1=s_1,
            s_2=s_2,
            s_3=s_3,
            s_4=s_4,
            s_5=s_5,
            s_6=s_6,
            s_7=s_7,
            s_8=s_8,
            s_9=s_9,
            s_10=s_10,
            s_11=s_11,
            s_12=s_12,
            s_13=s_13,
            V_gas=V_gas,
            S_IC_in=S_IC_in,
            S_IN_in=S_IN_in,
            S_I_in=S_I_in,
            X_c_in=X_c_in,
            X_ch_in=X_ch_in,
            X_pr_in=X_pr_in,
            X_li_in=X_li_in,
            X_su_in=X_su_in,
            X_aa_in=X_aa_in,
            X_fa_in=X_fa_in,
            X_c4_in=X_c4_in,
            X_pro_in=X_pro_in,
            X_ac_in=X_ac_in,
            X_h2_in=X_h2_in,
            X_I_in=X_I_in,
            S_cation_in=S_cation_in,
            S_anion_in=S_anion_in,
            N_xc=N_xc,
            N_I=N_I,
            N_aa=N_aa,
            N_bac=N_bac,
            f_sI_xc=f_sI_xc,
            f_xI_xc=f_xI_xc,
            f_ch_xc=f_ch_xc,
            f_pr_xc=f_pr_xc,
            f_li_xc=f_li_xc,
            f_fa_li=f_fa_li,
            f_bu_su=f_bu_su,
            f_pro_su=f_pro_su,
            f_ac_su=f_ac_su,
            f_va_aa=f_va_aa,
            f_bu_aa=f_bu_aa,
            f_pro_aa=f_pro_aa,
            f_ac_aa=f_ac_aa,
            Y_su=Y_su,
            Y_aa=Y_aa,
            Y_fa=Y_fa,
            Y_c4=Y_c4,
            Y_pro=Y_pro,
            Y_ac=Y_ac,
            Y_h2=Y_h2,
            k_p=k_p,
            k_L_a=k_L_a,
        )

        # Check if simulations results are all positive
        # They should be but unfortunately negative pressures
        # observed in previous run_adm1 runs for h2 and ch4
        # can only be explained by negative S_h2 and S_ch4

        # *********************** POST_TREATMENT ***********************
        if np.any(simulated_results < 0.0):
            # If negative result, divide by 2 previous result
            wrong_terms = simulated_results < 0.0
            simulated_results[wrong_terms] = 0.5 * state_zero[wrong_terms]

        (
            S_su,
            S_aa,
            S_fa,
            S_va,
            S_bu,
            S_pro,
            S_ac,
            S_h2,
            S_ch4,
            S_IC,
            S_IN,
            S_I,
            X_c,
            X_ch,
            X_pr,
            X_li,
            X_su,
            X_aa,
            X_fa,
            X_c4,
            X_pro,
            X_ac,
            X_h2,
            X_I,
            S_cation,
            S_anion,
            S_H_ion,
            S_va_ion,
            S_bu_ion,
            S_pro_ion,
            S_ac_ion,
            S_hco3_ion,
            S_nh3,
            S_gas_h2,
            S_gas_ch4,
            S_gas_co2,
        ) = simulated_results

        # Solve DAE states
        eps = 0.0000001
        prevS_H_ion = S_H_ion

        # initial values for Newton-Raphson solver parameter
        shdelta = 1.0
        shgradeq = 1.0
        S_h2delta = 1.0
        S_h2gradeq = 1.0
        dae_tol = 10.0 ** (-12)  # solver accuracy tolerance
        maxIter = 1000  # maximum number of iterations for solver
        i = 1
        j = 1

        while (shdelta > dae_tol or shdelta < -dae_tol) and (i <= maxIter):
            S_va_ion = K_a_va * S_va / (K_a_va + S_H_ion)
            S_bu_ion = K_a_bu * S_bu / (K_a_bu + S_H_ion)
            S_pro_ion = K_a_pro * S_pro / (K_a_pro + S_H_ion)
            S_ac_ion = K_a_ac * S_ac / (K_a_ac + S_H_ion)
            S_hco3_ion = K_a_co2 * S_IC / (K_a_co2 + S_H_ion)
            S_nh3 = K_a_IN * S_IN / (K_a_IN + S_H_ion)
            shdelta = (
                S_cation
                + (S_IN - S_nh3)
                + S_H_ion
                - S_hco3_ion
                - S_ac_ion / 64.0
                - S_pro_ion / 112.0
                - S_bu_ion / 160.0
                - S_va_ion / 208.0
                - K_w / S_H_ion
                - S_anion
            )
            shgradeq = (
                1
                + K_a_IN * S_IN / ((K_a_IN + S_H_ion) * (K_a_IN + S_H_ion))
                + K_a_co2 * S_IC / ((K_a_co2 + S_H_ion) * (K_a_co2 + S_H_ion))
                + 1.0 / 64.0 * K_a_ac * S_ac / ((K_a_ac + S_H_ion) * (K_a_ac + S_H_ion))
                + 1.0
                / 112.0
                * K_a_pro
                * S_pro
                / ((K_a_pro + S_H_ion) * (K_a_pro + S_H_ion))
                + 1.0 / 160.0 * K_a_bu * S_bu / ((K_a_bu + S_H_ion) * (K_a_bu + S_H_ion))
                + 1.0 / 208.0 * K_a_va * S_va / ((K_a_va + S_H_ion) * (K_a_va + S_H_ion))
                + K_w / (S_H_ion * S_H_ion)
            )
            S_H_ion = S_H_ion - shdelta / shgradeq
            if S_H_ion <= 0:
                S_H_ion = dae_tol
            i += 1

        ## DAE solver for S_h2 from Rosen et al. (2006)
        while (S_h2delta > dae_tol or S_h2delta < -dae_tol) and (j <= maxIter):
            I_pH_aa = (K_pH_aa**nn_aa) / (prevS_H_ion**nn_aa + K_pH_aa**nn_aa)

            I_pH_h2 = (K_pH_h2**n_h2) / (prevS_H_ion**n_h2 + K_pH_h2**n_h2)
            I_IN_lim = S_IN / (S_IN + K_S_IN)
            I_h2_fa = K_I_h2_fa / (K_I_h2_fa + S_h2)
            I_h2_c4 = K_I_h2_c4 / (K_I_h2_c4 + S_h2)
            I_h2_pro = K_I_h2_pro / (K_I_h2_pro + S_h2)

            I_5 = I_pH_aa * I_IN_lim
            I_6 = I_5
            I_7 = I_pH_aa * I_IN_lim * I_h2_fa
            I_8 = I_pH_aa * I_IN_lim * I_h2_c4
            I_9 = I_8
            I_10 = I_pH_aa * I_IN_lim * I_h2_pro

            I_12 = I_pH_h2 * I_IN_lim
            Rho_5 = k_m_su * (S_su / (K_S_su + S_su)) * X_su * I_5  # Uptake of sugars
            Rho_6 = k_m_aa * (S_aa / (K_S_aa + S_aa)) * X_aa * I_6  # Uptake of amino-acids
            Rho_7 = (
                k_m_fa * (S_fa / (K_S_fa + S_fa)) * X_fa * I_7
            )  # Uptake of LCFA (long-chain fatty acids)
            Rho_8 = (
                k_m_c4
                * (S_va / (K_S_c4 + S_va))
                * X_c4
                * (S_va / (S_bu + S_va + 1e-6))
                * I_8
            )  # Uptake of valerate
            Rho_9 = (
                k_m_c4
                * (S_bu / (K_S_c4 + S_bu))
                * X_c4
                * (S_bu / (S_bu + S_va + 1e-6))
                * I_9
            )  # Uptake of butyrate
            Rho_10 = (
                k_m_pro * (S_pro / (K_S_pro + S_pro)) * X_pro * I_10
            )  # Uptake of propionate
            Rho_12 = k_m_h2 * (S_h2 / (K_S_h2 + S_h2)) * X_h2 * I_12  # Uptake of hydrogen
            p_gas_h2 = S_gas_h2 * R * T_op / 16
            Rho_T_8 = k_L_a * (S_h2 - 16 * K_H_h2 * p_gas_h2)
            S_h2delta = (
                ratio_q_ad_V_liq * (S_h2_in - S_h2)
                + (1.0 - Y_su) * f_h2_su * Rho_5
                + (1.0 - Y_aa) * f_h2_aa * Rho_6
                + (1.0 - Y_fa) * 0.3 * Rho_7
                + (1.0 - Y_c4) * 0.15 * Rho_8
                + (1.0 - Y_c4) * 0.2 * Rho_9
                + (1.0 - Y_pro) * 0.43 * Rho_10
                - Rho_12
                - Rho_T_8
            )
            S_h2gradeq = (
                -ratio_q_ad_V_liq
                - 3.0
                / 10.0
                * (1.0 - Y_fa)
                * k_m_fa
                * S_fa
                / (K_S_fa + S_fa)
                * X_fa
                * I_pH_aa
                * S_IN
                / (K_S_IN + S_IN)
                * K_I_h2_fa
                / ((K_I_h2_fa + S_h2) ** 2)
                - 3.0
                / 20.0
                * (1.0 - Y_c4)
                * k_m_c4
                * S_va
                * S_va
                / (K_S_c4 + S_va)
                * X_c4
                / (S_bu + S_va + eps)
                * I_pH_aa
                * S_IN
                / (S_IN + K_S_IN)
                * K_I_h2_c4
                / ((K_I_h2_c4 + S_h2) ** 2)
                - 1.0
                / 5.0
                * (1.0 - Y_c4)
                * k_m_c4
                * S_bu
                * S_bu
                / (K_S_c4 + S_bu)
                * X_c4
                / (S_bu + S_va + eps)
                * I_pH_aa
                * S_IN
                / (S_IN + K_S_IN)
                * K_I_h2_c4
                / ((K_I_h2_c4 + S_h2) ** 2)
                - 43.0
                / 100.0
                * (1.0 - Y_pro)
                * k_m_pro
                * S_pro
                / (K_S_pro + S_pro)
                * X_pro
                * I_pH_aa
                * S_IN
                / (S_IN + K_S_IN)
                * K_I_h2_pro
                / ((K_I_h2_pro + S_h2) ** 2)
                - k_m_h2 / (K_S_h2 + S_h2) * X_h2 * I_pH_h2 * S_IN / (S_IN + K_S_IN)
                + k_m_h2
                * S_h2
                / ((K_S_h2 + S_h2) * (K_S_h2 + S_h2))
                * X_h2
                * I_pH_h2
                * S_IN
                / (S_IN + K_S_IN)
                - k_L_a
            )
            S_h2 = S_h2 - S_h2delta / S_h2gradeq
            if S_h2 <= 0:
                S_h2 = dae_tol
            j += 1
        # DAE states solved

        # Algebraic equations
        p_gas_h2 = S_gas_h2 * R * T_op / 16.0
        p_gas_ch4 = S_gas_ch4 * R * T_op / 64.0
        p_gas_co2 = S_gas_co2 * R * T_op
        p_gas = p_gas_h2 + p_gas_ch4 + p_gas_co2 + p_gas_h2o
        q_gas = k_p * (p_gas - p_atm)
        if q_gas < 0:
            q_gas = 0
        q_gas_accu += q_gas * (t_next - t0)

        q_ch4 = q_gas * (p_gas_ch4 / p_gas)  # methane flow
        if q_ch4 < 0.0:  ## q_gas is positive, only negative if negative pression...
            q_ch4 = 0.0
        q_ch4_accu += q_ch4 * (t_next - t0)

        p_co2_day_mean_accu += p_gas_co2
        p_ch4_day_mean_accu += p_gas_ch4

        state_zero[:] = np.array(
            [
                S_su,
                S_aa,
                S_fa,
                S_va,
                S_bu,
                S_pro,
                S_ac,
                S_h2,
                S_ch4,
                S_IC,
                S_IN,
                S_I,
                X_c,
                X_ch,
                X_pr,
                X_li,
                X_su,
                X_aa,
                X_fa,
                X_c4,
                X_pro,
                X_ac,
                X_h2,
                X_I,
                S_cation,
                S_anion,
                S_H_ion,
                S_va_ion,
                S_bu_ion,
                S_pro_ion,
                S_ac_ion,
                S_hco3_ion,
                S_nh3,
                S_gas_h2,
                S_gas_ch4,
                S_gas_co2,
            ]
        )

        # End of DAE treatment

        # Storing values
        if int(t_next) >= loc_day:
            simulate_results[count_day, ode_states_idx_in_pred] = state_zero
            simulate_results[count_day, pred_idx_q_gas] = q_gas_accu
            simulate_results[count_day, pred_idx_q_ch4] = q_ch4_accu
            simulate_results[count_day, pred_idx_p_ch4] = p_ch4_day_mean_accu / count_in_day
            simulate_results[count_day, pred_idx_p_co2] = p_co2_day_mean_accu / count_in_day

            count_day = count_day + 1
            loc_day = int(t_next) + 1  # Should be loc_day + 1 as well

            ## Refresh accus
            q_gas_accu = 0
            q_ch4_accu = 0
            p_ch4_day_mean_accu = 0
            p_co2_day_mean_accu = 0
            count_in_day = 0

        n = n + 1
        t0 = t_next

    ## END OF LOOP
    simulate_results[:, pred_idx_pH] = -np.log10(
        simulate_results[:, pred_idx_pH]
    )  # Transforming back pH from concentration
    simulate_results[:, pred_idx_S_co2] = (
        simulate_results[:, pred_idx_S_IC]
        - simulate_results[:, pred_idx_S_hco3_ion]  # S_co2 creation
    )
    simulate_results[:, pred_idx_S_nh4_ion] = (
        simulate_results[:, pred_idx_S_IN] - simulate_results[:, pred_idx_S_nh3]
    )  # S_nh4_ion creation

    # VSR computation
    VS_dig = dig_states_vs(simulate_results)  # type: ignore
    VS_in, q_day = feed_vs(influent_state)

    v_liq_d = volume_per_day(influent_state[:, feed_idx_time], V_liq_s)

    vs_mass = v_liq_d * VS_dig
    vs_in_mass = q_day * VS_in
    vs_out_mass = q_day * VS_dig

    simulate_results[:, pred_idx_VS] = VS_dig
    simulate_results[:, pred_idx_VS_in] = VS_in
    simulate_results[:, pred_idx_VSR] = np.nan  # Fill in first values

    # Check that sufficient number of days to compute VSR
    if n_day_vsr < n_days:

        c_vs_in_mass = np.cumsum(vs_in_mass)
        c_vs_out_mass = np.cumsum(vs_out_mass)

        d_vs_in_mass = c_vs_in_mass[n_day_vsr:] - c_vs_in_mass[:-n_day_vsr]
        d_vs_out_mass = c_vs_out_mass[n_day_vsr:] - c_vs_out_mass[:-n_day_vsr]

        VS_rmvd = (
            d_vs_in_mass - d_vs_out_mass + vs_mass[:-n_day_vsr] - vs_mass[n_day_vsr:]
        )
        VSR = VS_rmvd / d_vs_in_mass

        simulate_results[:(-n_day_vsr), pred_idx_VSR] = VSR

    # Add time to results
    simulate_results[:, 0] = np.arange(day_begin, day_end + 1, 1)

    return simulate_results, reached_dt_min
