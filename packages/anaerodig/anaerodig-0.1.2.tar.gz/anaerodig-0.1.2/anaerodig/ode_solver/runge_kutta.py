import numpy as np
from typing import Union

class ButcherTableau:
    def __init__(
            self,
            t_coeffs:np.ndarray, 
            coeffs:np.ndarray,
            b0:np.ndarray,
            b1:np.ndarray,
            order:int
        ):
        _coeffs = np.asarray(coeffs)
        _t_coeffs = np.asarray(t_coeffs)
        _b0 = np.asarray(b0)
        _b1 = np.asarray(b1)
        n_t, n_x = _coeffs.shape

        assert _t_coeffs.shape == (n_t,)
        assert _b0.shape == (n_x,)
        assert _b1.shape == (n_x,)

        self.n_x = n_x
        self.n_t = n_t
        self.t_coeffs = _t_coeffs
        self.coeffs = _coeffs
        self.b0 = _b0
        self.b1 = _b1
        self.order= order

Butcher45 = ButcherTableau(
    t_coeffs = [0.0, 1/4, 3/8, 12/13, 1.0, 1/2],
    coeffs = [
        [0.0,0.0,0.0, 0.0,0.0,0.0],
        [1/4, 0,0, 0.0, 0.0, 0.0],
        [3/32, 9/32, 0, 0, 0, 0],
        [1932/2197, -7200/2197, 7296/2197, 0.0, 0.0, 0.0],
        [439/216, -8.0, 3680/513, -845/4104, 0.0, 0.0],
        [-8/27, 2.0, -3544/2565, 1859/4104, -11/40, 0.0]
        ],
    b0 = [16/135, 0.0, 6656/12825, 28561/56430, - 9/50, 2/55],
    b1 = [25/216, 0.0, 1408/2565, 2197/4104, -1/5, 0.0],
    order=4
)

ButcherBogacki = ButcherTableau(
    t_coeffs = [0.0, 1/2, 3/4, 1.0],
    coeffs = [[0.0, 0.0, 0.0, 0.0], 
              [1/2, 0.0, 0.0, 0.0],
              [0.0, 3/4, 0.0, 0.0],
              [2/9, 1/3, 4/9, 0.0]],
    b0= [2/9, 1/3, 4/9, 0.0],
    b1 = [7/24, 1/4, 1/3, 1/8],
    order=2
)

ButcherHeunEuler = ButcherTableau(
    t_coeffs = [0.0, 1.0],
    coeffs = [
        [0.0,0.0],
        [1.0, 0.0],
    ],
    b0 = [1/2, 1/2],
    b1 = [1.0, 0.0],
    order=1
)

ButcherFehlberg12 = ButcherTableau(
    t_coeffs=[0.0, 1/2, 1.0],
    coeffs = [[0.0, 0.0, 0.0],
              [0.5, 0.0, 0.0],
              [1/256, 255/256, 0.0]],
    b0 = [1/512, 255/256, 1/512],
    b1 = [1/256, 255/256, 0.0],
    order=1
)

ButcherCashKarp = ButcherTableau(
    t_coeffs =[0.0, 1/5, 3/10, 3/5, 1.0, 7/8],
    coeffs = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1/5, 0.0, 0.0, 0.0, 0.0, 0.0],
        [3/40, 9/40, 0.0, 0.0, 0.0, 0.0],
        [3/10, -9/10, 6/5, 0.0, 0.0, 0.0],
        [-11/54, 5/2, -70/27, 35/27, 0.0, 0.0],
        [1631/55296, 175/512, 575/13824, 44275/ 110592, 253/4096, 0.0]],
    b0 = [37/378, 0.0, 250/621, 125/594, 0.0, 512/1771],
    b1 = [2825/27648, 0.0, 18575/48384, 13525/55296, 277/14336, 1/4],
    order=4
)

ButcherDormandPrince = ButcherTableau(
    t_coeffs = [0.0, 1/5, 3/10, 4/5, 8/9, 1.0, 1.0],
    coeffs =[
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1/5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [3/40, 9/40, 0.0, 0.0, 0.0, 0.0, 0.0],
        [44/45, -56/15, 32/9, 0.0, 0.0, 0.0, 0.0],
        [19372/6561, -25360/2187, 64448/6561, -212/729, 0.0, 0.0, 0.0],
        [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656, 0.0, 0.0], 
        [35/384, 0.0, 500/1113, 125/192, -2187/6784, 11/84, 0.0]
        ], 
    b0 = [35/384, 0.0, 500/1113, 125/192, -2187/6784, 11/84, 0.0],
    b1 = [5179/57600, 0.0, 7571/16695, 393/640, -92097/339200, 187/2100, 1/40 ],
    order=4
)

BUTCHER_ALIASES = {
    "FEHLBERG_45": Butcher45,
    "FEHLBERG45":Butcher45,
    "45": Butcher45,
    "FEHLBERG_12": ButcherFehlberg12,
    "FEHLBERG_12":ButcherFehlberg12,
    "12": ButcherFehlberg12,
    "CASHKARP": ButcherCashKarp,
    "BOGACKI":ButcherBogacki,
    "DORMANDPRINCE":ButcherDormandPrince,
    "HEUNEULER":ButcherHeunEuler
}

def infer_butcher_tableau(table_indic:Union[ButcherTableau, str]):
    if isinstance(table_indic, ButcherTableau):
        return table_indic
    return BUTCHER_ALIASES[str(table_indic).upper()]