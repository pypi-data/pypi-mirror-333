"""TODO."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

from ppftpy import ppft2, ppft3

if TYPE_CHECKING:
    from ._helpers import ArrayBackend, RegressionTestPair


@pytest.mark.regression
def test_backend_regression_array_ppft2(
    array_backend: ArrayBackend, regression_test_2d: RegressionTestPair
) -> None:
    """Verify that PPFT2D results match the MATLAB implementation."""
    expected = regression_test_2d.out_data
    actual = array_backend.compute(regression_test_2d.in_data, ppft2)

    np.testing.assert_allclose(
        actual, expected, rtol=array_backend.rtol, atol=array_backend.atol
    )


@pytest.mark.regression
def test_backend_regression_array_ppft3(
    array_backend: ArrayBackend, regression_test_3d: RegressionTestPair
) -> None:
    """Verify that PPFT3D results match the MATLAB implementation."""
    expected = regression_test_3d.out_data
    actual = array_backend.compute(regression_test_3d.in_data, ppft3)

    np.testing.assert_allclose(
        actual, expected, rtol=array_backend.rtol, atol=array_backend.atol
    )


@pytest.mark.regression
@pytest.mark.parametrize("dtype", [int, float, complex], ids=lambda x: f"dtype={x}")
def test_backend_array_exceeding_tolerances_ppft2_raises(
    array_backend: ArrayBackend, dtype: type
) -> None:
    """Ensure that tolerances of test backends are applied correctly.

    This is a negative test to ensure that the set tolerances within the
    ``ArrayBackend`` class are applied as expected. A lambda function is passed
    as replacement for the actual PPFT2D function that simply adds +1 to all
    values. As the relative and absolute error are much smaller, the comparison
    must fail.
    """
    data = np.zeros((4, 4), dtype=dtype)

    expected = data.copy()
    actual = array_backend.compute(data, lambda x, **_kwargs: x + 1)

    with pytest.raises(AssertionError):
        # Raising an error is expected as the expected difference is 1.
        np.testing.assert_allclose(
            actual, expected, rtol=array_backend.rtol, atol=array_backend.atol
        )
