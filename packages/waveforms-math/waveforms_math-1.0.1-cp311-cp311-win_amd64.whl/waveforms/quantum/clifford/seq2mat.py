import warnings

warnings.warn(
    "waveforms.quantum.clifford is deprecated. Please use qlisp instead.",
    DeprecationWarning)

from qlisp.circuits._rb.seq2mat import *