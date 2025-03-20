"""Custom numpy typing nicknames shared throughout the package.

This module is introduced to avoid having redundant notations and different
aliases created locally for the same purpose in the package. Eventually,
the definition of the aliases should be improved, and if succint and informative
numpy notations are found, these should replace the aliases in the code.

Information on arrays: dtype, number of dimensions.
"""

import numpy as np

# Some type hints alias
array_2D = np.ndarray
array_1D = np.ndarray
array_3D = np.ndarray
sparse_1D = np.ndarray
sparse_2D = np.ndarray
