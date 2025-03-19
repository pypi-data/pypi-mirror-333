import warnings

warnings.warn(
    "waveforms.quantum.clifford is deprecated. Please use qlisp instead.",
    DeprecationWarning)

from qlisp.clifford.utils import mat2num, num2mat
