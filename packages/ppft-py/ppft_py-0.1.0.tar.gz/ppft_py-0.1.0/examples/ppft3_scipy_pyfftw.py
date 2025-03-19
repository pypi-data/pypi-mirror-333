"""Example of the 3D Pseudo-Polar Fourier Transform with pyFFTW backend."""

import numpy as np
import pyfftw.interfaces.scipy_fft as pyfftw
from scipy import fft

from ppftpy import ppft3

data = np.random.default_rng().random((32, 32, 32))

with fft.set_backend(pyfftw):
    transformed = ppft3(data, scipy_fft=True)
