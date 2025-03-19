"""Example of the 3D Pseudo-Polar Fourier Transform with pyFFTW backend."""

import numpy as np

from ppftpy import ppft3

data = np.random.default_rng().random((32, 32, 32))

transformed = ppft3(data, scipy_fft=True)
