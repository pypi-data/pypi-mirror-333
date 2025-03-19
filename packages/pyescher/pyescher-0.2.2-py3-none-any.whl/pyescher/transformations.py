import numpy as np


def dB(y: np.ndarray) -> np.ndarray:
    return 20*np.log10(np.abs(y))

def dB10(y: np.ndarray) -> np.ndarray:
    return 10*np.log10(np.abs(y))

dB20 = dB

