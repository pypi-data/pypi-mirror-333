import warnings

warnings.warn(
    "waveforms.quantum.clifford is deprecated. Please use cycles or qlisp instead.",
    DeprecationWarning)

from qlisp.circuits._rb.clifford import *