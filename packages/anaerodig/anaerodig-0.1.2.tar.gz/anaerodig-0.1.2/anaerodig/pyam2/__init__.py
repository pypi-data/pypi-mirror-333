"""
PyAM2 - Anaerobic digestion modelisation with Anerobic Model 2 (AM2)

Details about the modelisation can be found at https://doi.org/10.1002/bit.10036 .

The implementation follows the description of the above reference with a few modifications. See
run_AM2 documentation for more details.

PyAM2 is designed for:
    - Modelling (run_am2)

Anaerobic Digestion objects (DigesterInfo, DigesterFeed, DigesterParameter, DigesterState,
DigesterStates) are stored as human readable files (csv, json) and can be loaded/saved using
load and save methods.

Main class is AM2Dig with methods
    simulate (AM2 modeling of digester from initial state, digester information, digester
        parameter and influent)
    err (measures the difference between predictions and observations)
    score_param (measures the difference between predictions using a specific parameters and
        observations)
    am2_derivative (computes the derivative of AM2 with respect to the digester parameter)
"""

from anaerodig.pyam2.basic_classes.config import AM2Config
from anaerodig.pyam2.basic_classes.feed import AM2Feed
from anaerodig.pyam2.basic_classes.param import AM2Param
from anaerodig.pyam2.basic_classes.states import AM2State, AM2States
from anaerodig.pyam2.data import data_dir, param_file
from anaerodig.pyam2.digester import AM2Dig

toy_dig = AM2Dig.load(data_dir)
toy_param = AM2Param.load(param_file, data_dir)
