import warnings

warnings.warn(
    "waveforms.quantum.clifford is deprecated. Please use cycles or qlisp instead.",
    DeprecationWarning)

from cycles.clifford import cliffordOrder
