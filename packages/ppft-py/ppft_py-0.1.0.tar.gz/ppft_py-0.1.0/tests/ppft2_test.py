"""TODO."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

import numpy as np
import pytest

from ppftpy import ppft2, rppft2

if TYPE_CHECKING:
    from collections.abc import Callable

    from numpy.typing import DTypeLike, NDArray


RTOL: Final = 1e-12
ATOL: Final = 1e-12

SUPPORTED_DTYPES: Final = [
    dtype
    for dtype in set(np.sctypeDict.values())
    if np.issubdtype(dtype, np.number) and not np.issubdtype(dtype, np.timedelta64)
]
SUPPORTED_DTYPES_COMPLEX: Final = [
    dtype for dtype in SUPPORTED_DTYPES if np.issubdtype(dtype, np.complexfloating)
]
SUPPORTED_DTYPES_NON_COMPLEX: Final = [
    dtype for dtype in SUPPORTED_DTYPES if not np.issubdtype(dtype, np.complexfloating)
]


@pytest.mark.parametrize("func", [ppft2, rppft2], ids=lambda x: f"func={x.__name__}")
def test_ppft2_zeros_return_zero_only(zeros_data_2d: NDArray, func: Callable) -> None:
    """TODO."""
    output = func(zeros_data_2d)
    assert np.all(output == 0.0 + 0.0j), "Not all values are complex 0.0"


@pytest.mark.parametrize("func", [ppft2, rppft2], ids=lambda x: f"func={x.__name__}")
def test_ppft2_returns_complex_dtype(data_2d: NDArray, func: Callable) -> None:
    """TODO."""
    output = func(data_2d)
    assert np.issubdtype(output.dtype, np.complexfloating), (
        "Output is not of a complex type"
    )


@pytest.mark.parametrize("func", [ppft2, rppft2], ids=lambda x: f"func={x.__name__}")
def test_ppft2_sequential_equals_vectorized(data_2d: NDArray, func: Callable) -> None:
    """TODO."""
    output_vectorized = func(data_2d, vectorized=True)
    output_sequential = func(data_2d, vectorized=False)

    np.testing.assert_equal(output_vectorized, output_sequential)


@pytest.mark.parametrize(
    "dtype",
    [*SUPPORTED_DTYPES_NON_COMPLEX, *SUPPORTED_DTYPES_COMPLEX],
    ids=lambda x: f"dtype={x}",
)
def test_ppft2_supports_data_types(dtype: DTypeLike) -> None:
    """TODO."""
    data = np.ones((4, 4), dtype=dtype)
    out = ppft2(data)

    assert not np.isnan(out).any()
    assert np.issubdtype(out.dtype, np.complexfloating)


@pytest.mark.parametrize(
    "dtype", [*SUPPORTED_DTYPES_NON_COMPLEX], ids=lambda x: f"dtype={x}"
)
@pytest.mark.parametrize("func", [ppft2, rppft2], ids=lambda x: f"func={x.__name__}")
def test_rppft2_supports_non_complex_data_types(
    func: Callable, dtype: DTypeLike
) -> None:
    """TODO."""
    data = np.ones((4, 4), dtype=dtype)
    out = func(data)

    assert not np.isnan(out).any()
    assert np.issubdtype(out.dtype, np.complexfloating)


def test_ppft2_returns_correct_shape(data_2d: NDArray) -> None:
    """Verify that all PPFT2 generates two "Pseudo-Polar" outputs.

    PPFT2 generates two "Pseudo-Polar" outputs.
    Each has a shape of (2xN+1, N+1).
    All outputs are then combined into a single 3D matrix with the shape
    of (2, 2xN+1, N+1).
    """
    data = data_2d

    n = len(data)

    # We expect 2 sectors with each element having a shape of (2*n+1, n+1).
    # For n=4, the expected shape is (2, 9, 5).
    expected_shape = (2, 2 * n + 1, n + 1)

    assert ppft2(data).shape == expected_shape


def test_ppft2_sectors_symmetric_data(data_2d: NDArray) -> None:
    """TODO."""
    data = data_2d

    # We only care for the magnitude of the data.
    result = np.abs(ppft2(data))

    # The returned PPFT2D has two fourier-transformed sectors,
    # therefore we need to compare both parts.
    np.testing.assert_allclose(np.flipud(result[0]), result[0], atol=ATOL)
    np.testing.assert_allclose(np.flipud(result[1]), result[1], atol=ATOL)


@pytest.mark.parametrize("vectorized", [True, False])
@pytest.mark.parametrize("ppft_func", [ppft2, rppft2])
def test_ppft2_single_equals_multi_mode(
    data_2d: NDArray, ppft_func: Callable, *, vectorized: bool
) -> None:
    """TODO."""
    data = data_2d

    # We add arbitrary data as vectorized input.
    expanded_data = np.stack([data, data * 0.5, data * 0.3, data * 0.1])

    actual = ppft_func(expanded_data, vectorized=vectorized)
    expected = np.array([ppft_func(d, vectorized=vectorized) for d in expanded_data])

    np.testing.assert_equal(actual, expected)


@pytest.mark.parametrize("func", [ppft2, rppft2])
@pytest.mark.parametrize("dimension", [1, 4, 5])
@pytest.mark.parametrize("size", [2, 4, 8, 16])
def test_ppft2_fails_for_non_2d_data(func: Callable, size: int, dimension: int) -> None:
    """TODO."""
    data = np.zeros((size,) * dimension)

    with pytest.raises(
        ValueError,
        match="Input data must a single NxN matrix or an array of NxN matrices",
    ):
        func(data)


@pytest.mark.parametrize("size", [1, 2, 3, 5, 6, 7, 8])
def test_ppft2_fails_for_non_square_data(size: int) -> None:
    """TODO."""
    data = np.zeros((4, size))

    with pytest.raises(
        ValueError, match="Input data must have sides with same lengths"
    ):
        ppft2(data)


@pytest.mark.parametrize("size", [1, 3, 5, 7, 9, 11, 13, 15, 17, 19])
def test_ppft2_fails_for_odd_sized_data(size: int) -> None:
    """TODO."""
    data = np.zeros((size,) * 2)

    with pytest.raises(ValueError, match="Input data must have even sides"):
        ppft2(data)


@pytest.mark.parametrize("vectorized", [True, False], ids=lambda x: f"vectorized={x}")
@pytest.mark.parametrize("scipy_fft", [True, False], ids=lambda x: f"scipy_fft={x}")
def test_rppft2_equals_ppft2(
    data_2d: NDArray, *, vectorized: bool, scipy_fft: bool
) -> None:
    """TODO."""
    data = data_2d

    if scipy_fft:
        pytest.importorskip("scipy", reason="SciPy is not installed")

    n = len(data)

    actual = rppft2(data, vectorized=vectorized, scipy_fft=scipy_fft)
    expected = ppft2(data, vectorized=vectorized, scipy_fft=scipy_fft)[:, n:]

    if scipy_fft:
        np.testing.assert_equal(actual, expected)
    else:
        np.testing.assert_allclose(actual, expected, rtol=1e-15, atol=1e-12)


@pytest.mark.parametrize("ppft_func", [ppft2, rppft2])
def test_ppft2_vectorized_equals_sequential(
    data_2d: NDArray, ppft_func: Callable
) -> None:
    """TODO."""
    data = data_2d

    expected = ppft_func(data, vectorized=True)
    actual = ppft_func(data, vectorized=False)

    np.testing.assert_equal(actual, expected)
