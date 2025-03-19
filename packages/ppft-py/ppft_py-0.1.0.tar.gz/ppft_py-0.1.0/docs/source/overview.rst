Overview
========

Welcome to the documentation for **ppft-py**.

**ppft-py** provides a Python implementation of the Pseudo-Polar Fourier
Transform (PPFT) in both 2D (PPFT2D) and 3D (PPFT3D), based on the methods
introduced in [Averbuch2001]_ and [Averbuch2003]_.

The module :mod:`~ppftpy` provides the following functions:

.. list-table:: Key Functions
   :header-rows: 1

   * - Function
   * - :func:`~ppftpy.ppft2`
   * - :func:`~ppftpy.rppft2`
   * - :func:`~ppftpy.ppft3`
   * - :func:`~ppftpy.rppft3`

For detailed API documentation, see :doc:`reference`.

.. rubric:: Contents

.. toctree::

   backends

.. rubric:: Package

:Version: |version|
:Release: |release|

.. rubric:: References

.. [Averbuch2003] A. Averbuch and Y. Shkolnisky, "3D Fourier based discrete
   Radon transform," Applied and Computational Harmonic Analysis, vol. 15, no.
   1, pp. 33-69, Jul. 2003, issn: 1063-5203. `doi:10.1016/s1063-5203(03)00030-7
   <https://doi.org/10.1016/s1063-5203(03)00030-7>`_.

.. [Averbuch2001] A. Averbuch, R. Coifman, D. Donoho, M. Israeli, and J.
   Waldén, "Fast Slant Stack: A notion of Radon Transform for Data in a
   Cartesian Grid which is Rapidly Computible, Algebraically Exact,
   Geometrically Faithful and Invertible," 2001.

.. autosummary::
   :toctree: _autosummary
   :recursive:
