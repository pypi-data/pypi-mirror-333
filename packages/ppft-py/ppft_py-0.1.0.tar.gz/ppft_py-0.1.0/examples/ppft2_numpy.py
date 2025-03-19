"""Example of the 2D Pseudo-Polar Fourier Transform with default backend."""

import numpy as np

from ppftpy import ppft2

data = np.random.default_rng().random((128, 128))

transformed = ppft2(data)
