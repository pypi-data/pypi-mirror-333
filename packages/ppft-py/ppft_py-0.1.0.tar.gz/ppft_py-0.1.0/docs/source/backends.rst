##########
 Backends
##########

The following implementations of the `Array API Standard
<https://data-apis.org/array-api/latest/>`_ have been tested to work:

.. list-table::
   :header-rows: 1

   -  -  Backend
      -  Devices
      -  Minimum Version

   -  -  `NumPy <https://github.com/numpy/numpy>`_
      -  CPU
      -  1.23.0

   -  -  `CuPy <https://github.com/cupy/cupy>`_
      -  GPU
      -  10.0.0

   -  -  `DPNP <https://github.com/IntelPython/dpnp/>`_
      -  GPU
      -  0.17.0

   -  -  `Dask <https://github.com/dask/dask>`_
      -  CPU / GPU
      -  2024.8.1

   -  -  `PyTorch <https://github.com/pytorch/pytorch>`_
      -  CPU / GPU
      -  1.13.0

   -  -  `JAX <https://github.com/jax-ml/jax>`_
      -  CPU / GPU
      -  0.4.32

The following implementations of the `SciPy
<https://github.com/scipy/scipy>`_ FFT interface have been tested to
work:

.. list-table::
   :header-rows: 1

   -  -  Backend
      -  Supports
      -  Minimum Version

   -  -  `SciPy <https://github.com/scipy/scipy>`_
      -  NumPy *(incl. Dask/JAX with NumPy arrays)*
      -  1.8.0

   -  -  `mkl_fft <https://github.com/IntelPython/mkl_fft>`_
      -  NumPy *(incl. Dask/JAX with NumPy arrays)*
      -  1.3.6

   -  -  `pyFFTW <https://github.com/pyFFTW/pyFFTW>`_
      -  NumPy *(incl. Dask/JAX with NumPy arrays)*
      -  0.13.0

   -  -  `CuPy <https://github.com/cupy/cupy>`_
      -  CuPy *(incl. Dask with CuPy arrays)*
      -  10.0.0
