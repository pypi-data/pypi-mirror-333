# ppft-py

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ppft-py?pypiBaseUrl=https%3A%2F%2Ftest.pypi.org)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/ppft-py?pypiBaseUrl=https%3A%2F%2Ftest.pypi.org)
[![ci](https://github.com/jnk22/ppft-py/actions/workflows/ci.yml/badge.svg)](https://github.com/jnk22/ppft-py/actions/workflows/ci.yml)
[![ReadtheDocs](https://readthedocs.org/projects/ppft-py/badge/?version=latest)](https://ppft-py.readthedocs.io)
[![codecov](https://codecov.io/github/jnk22/ppft-py/graph/badge.svg?token=5EJL318F1D)](https://codecov.io/github/jnk22/ppft-py)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Highly optimized Pseudo-Polar Fourier Transform in Python.

This repository provides a Python implementation of the **Pseudo-Polar Fourier
Transform (PPFT)** in both **2D (PPFT2D) and 3D (PPFT3D)**, based on the
methods presented in the following papers:

- Averbuch et al., 2001 — _Fast Slant Stack: A notion of Radon Transform for
  Data in a Cartesian Grid which is Rapidly Computable, Algebraically Exact,
  Geometrically Faithful and Invertible_.
- [Averbuch & Shkolnisky, 2003](https://doi.org/10.1016/s1063-5203(03)00030-7)
  — _3D Fourier based discrete Radon transform_, Applied and Computational
  Harmonic Analysis, Vol. 15, No. 1, pp. 33–69.

## Features

- GPU-accelerated computation for enhanced performance.
- Backend-agnostic implementation using the [Array API Standard](https://data-apis.org/array-api/latest/) with no direct dependencies.
- Memory-efficient and fully vectorized modes available.
- Optimized handling of real-valued input data for improved efficiency.
- Supports additional FFT backends using SciPy for extended flexibility and
  performance.

## Usage

To transform data with the Pseudo-Polar Fourier Transform, import the function
from `ppftpy` and apply it to the input data:

**2D Pseudo-Polar Fourier Transform:**

```python
import numpy as np

from ppftpy import ppft2

data = np.random.default_rng().random((128, 128))

transformed = ppft2(data)
```

**3D Pseudo-Polar Fourier Transform:**

```python
import numpy as np

from ppftpy import ppft3

data = np.random.default_rng().random((32, 32, 32))

transformed = ppft3(data)
```

**Note:** _The example uses NumPy arrays for the Pseudo-Polar Fourier
Transform. However, this library supports all backends that implement the
[Array API Standard](https://data-apis.org/array-api/latest/) and its
[FFT extension](https://data-apis.org/array-api/latest/extensions/fourier_transform_functions.html)
(via the [array-api-compat](https://github.com/data-apis/array-api-compat)
compatibility layer). See [backends](#backends) for a list of tested backends._

### SciPy FFT Backends

Additionally, implementations of the [SciPy](https://github.com/scipy/scipy)
FFT interface can be used as backends for the underlying FFT:

**2D Pseudo-Polar Fourier Transform with SciPy backend:**

```python
import numpy as np

from ppftpy import ppft2

data = np.random.default_rng().random((128, 128))

transformed = ppft2(data, scipy_fft=True)
```

**2D Pseudo-Polar Fourier Transform with pyFFTW backend:**

```python
import numpy as np
import pyfftw.interfaces.scipy_fft as pyfftw
from scipy import fft

from ppftpy import ppft2

data = np.random.default_rng().random((128, 128))

with fft.set_backend(pyfftw):
    transformed = ppft2(data, scipy_fft=True)
```

**Note:** _For more information on using custom FFT backends with SciPy, check
out the [backend control section](https://docs.scipy.org/doc/scipy/reference/fft.html#backend-control)
of the SciPy documentation. See [backends](#backends) for a list of tested
backends._

## Backends

The following implementations of the [Array API Standard](https://data-apis.org/array-api/latest/)
have been tested to work:

| Backend                                       |  Devices  | Minimum Version |
| --------------------------------------------- | :-------: | --------------- |
| [NumPy](https://github.com/numpy/numpy)       |    CPU    | 1.23.0          |
| [CuPy](https://github.com/cupy/cupy)          |    GPU    | 10.0.0          |
| [DPNP](https://github.com/IntelPython/dpnp/)  | CPU / GPU | 0.17.0[^1]      |
| [Dask](https://github.com/dask/dask)          | CPU / GPU | 2024.8.1        |
| [PyTorch](https://github.com/pytorch/pytorch) | CPU / GPU | 1.13.0          |
| [JAX](https://github.com/jax-ml/jax)          | CPU / GPU | 0.4.32          |

[^1]: [Released](https://github.com/IntelPython/dpnp/releases/tag/0.17.0), but not yet available on [PyPI](https://pypi.org/project/dpnp/).

The following implementations of the [SciPy](https://github.com/scipy/scipy)
FFT interface have been tested to work:

| Backend                                           | Supports                                   | Minimum Version |
| ------------------------------------------------- | ------------------------------------------ | --------------- |
| [SciPy](https://github.com/scipy/scipy)           | NumPy _(incl. Dask/JAX with NumPy arrays)_ | 1.8.0           |
| [mkl_fft](https://github.com/IntelPython/mkl_fft) | NumPy _(incl. Dask/JAX with NumPy arrays)_ | 1.3.6           |
| [pyFFTW](https://github.com/pyFFTW/pyFFTW)        | NumPy _(incl. Dask/JAX with NumPy arrays)_ | 0.13.0          |
| [CuPy](https://github.com/cupy/cupy)              | CuPy _(incl. Dask with CuPy arrays)_       | 10.0.0          |

## Acknowledgments

This project utilizes concepts from the reference implementations and for
generating test data for regression tests:

- **PPFT2D**: [ShkolniskyLab/PPFT2D](https://github.com/ShkolniskyLab/PPFT2D)
- **PPFT3D**: [ShkolniskyLab/PPFT3D](https://github.com/ShkolniskyLab/PPFT3D)
  and its associated [MATLAB Central resource](https://www.mathworks.com/matlabcentral/fileexchange/61815-3d-pseudo-polar-fourier-and-radon-transforms)
