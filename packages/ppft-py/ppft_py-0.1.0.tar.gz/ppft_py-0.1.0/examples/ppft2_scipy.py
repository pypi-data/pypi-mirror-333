"""Example of the 2D Pseudo-Polar Fourier Transform with pyFFTW backend."""

import numpy as np

from ppftpy import ppft2

data = np.random.default_rng().random((128, 128))

transformed = ppft2(data, scipy_fft=True)
