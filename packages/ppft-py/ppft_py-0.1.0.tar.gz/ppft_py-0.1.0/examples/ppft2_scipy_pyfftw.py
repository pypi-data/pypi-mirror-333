"""Example of the 2D Pseudo-Polar Fourier Transform with pyFFTW backend."""

import numpy as np
import pyfftw.interfaces.scipy_fft as pyfftw
from scipy import fft

from ppftpy import ppft2

data = np.random.default_rng().random((128, 128))

with fft.set_backend(pyfftw):
    transformed = ppft2(data, scipy_fft=True)
