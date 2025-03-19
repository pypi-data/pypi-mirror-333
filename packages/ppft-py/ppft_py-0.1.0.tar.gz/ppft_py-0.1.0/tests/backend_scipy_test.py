"""TODO."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Literal

import numpy as np
import pytest

from ppftpy import ppft2, ppft3, rppft2, rppft3

if TYPE_CHECKING:
    from collections.abc import Callable

    from ._helpers import RegressionTestPair, ScipyBackend


@pytest.mark.regression
def test_backend_regression_scipy_ppft2(
    scipy_backend: ScipyBackend, regression_test_2d: RegressionTestPair
) -> None:
    """Verify that PPFT2D results match the MATLAB implementation."""
    expected = regression_test_2d.out_data
    actual = scipy_backend.compute(regression_test_2d.in_data, ppft2)

    np.testing.assert_allclose(
        actual, expected, rtol=scipy_backend.rtol, atol=scipy_backend.atol
    )


@pytest.mark.regression
def test_backend_regression_scipy_ppft3(
    scipy_backend: ScipyBackend, regression_test_3d: RegressionTestPair
) -> None:
    """Verify that PPFT3D results match the MATLAB implementation."""
    expected = regression_test_3d.out_data
    actual = scipy_backend.compute(regression_test_3d.in_data, ppft3)

    np.testing.assert_allclose(
        actual, expected, rtol=scipy_backend.rtol, atol=scipy_backend.atol
    )


@pytest.mark.regression
@pytest.mark.parametrize("dtype", [int, float, complex], ids=lambda x: f"dtype={x}")
def test_backend_scipy_exceeding_tolerances_ppft2_raises(
    scipy_backend: ScipyBackend, dtype: type
) -> None:
    """Ensure that tolerances of test backends are applied correctly.

    This is a negative test to ensure that the set tolerances within the
    ``ScipyBackend`` class are applied as expected. A lambda function is passed
    as replacement for the actual PPFT2D function that simply adds +1 to all
    values. As the relative and absolute error are much smaller, the comparison
    must fail.
    """
    data = np.zeros((4, 4), dtype=dtype)

    expected = data.copy()
    actual = scipy_backend.compute(data, lambda x, **_kwargs: x + 1)

    with pytest.raises(AssertionError):
        # Raising an error is expected as the expected difference is 1.
        np.testing.assert_allclose(
            actual, expected, rtol=scipy_backend.rtol, atol=scipy_backend.atol
        )


@pytest.mark.parametrize("vectorized", [True, False])
@pytest.mark.parametrize(
    ("ppft_func", "dim"), [(ppft2, 2), (rppft2, 2), (ppft3, 3), (rppft3, 3)]
)
def test_ppft_get_fft_backend_scipy_unavailable(
    monkeypatch: pytest.MonkeyPatch,
    ppft_func: Callable,
    dim: Literal[2, 3],
    *,
    vectorized: bool,
) -> None:
    """TODO."""
    monkeypatch.setattr("ppftpy._utils.sc_fft", None)

    data = np.random.default_rng().random((4,) * dim)

    with pytest.raises(
        ModuleNotFoundError,
        match="SciPy FFT module is not available, install SciPy to use this feature",
    ):
        ppft_func(data, scipy_fft=True, vectorized=vectorized)


@pytest.mark.parametrize("vectorized", [True, False])
@pytest.mark.parametrize(
    ("ppft_func", "dim"), [(ppft2, 2), (rppft2, 2), (ppft3, 3), (rppft3, 3)]
)
@pytest.mark.usefixtures("no_scipy")
def test_ppft_get_fft_backend_scipy_not_installed(
    ppft_func: Callable, dim: Literal[2, 3], *, vectorized: bool
) -> None:
    """TODO."""
    import ppftpy._utils as ppft_utils_module

    importlib.reload(ppft_utils_module)

    assert ppft_utils_module.sc_fft is None

    data = np.random.default_rng().random((4,) * dim)

    with pytest.raises(
        ModuleNotFoundError,
        match="SciPy FFT module is not available, install SciPy to use this feature",
    ):
        ppft_func(data, scipy_fft=True, vectorized=vectorized)
