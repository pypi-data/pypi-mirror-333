"""TODO."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

import numpy as np
import pytest

from ppftpy import ppft3, rppft3

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


@pytest.mark.parametrize("func", [ppft3, rppft3], ids=lambda x: f"func={x.__name__}")
def test_ppft3_zeros_return_zero_only(zeros_data_3d: NDArray, func: Callable) -> None:
    """TODO."""
    output = func(zeros_data_3d)
    assert np.all(output == 0.0 + 0.0j), "Not all values are complex 0.0"


@pytest.mark.parametrize("func", [ppft3, rppft3], ids=lambda x: f"func={x.__name__}")
def test_ppft3_returns_complex_dtype(data_3d: NDArray, func: Callable) -> None:
    """TODO."""
    output = func(data_3d)
    assert np.issubdtype(output.dtype, np.complexfloating), (
        "Output is not of a complex type"
    )


@pytest.mark.parametrize("func", [ppft3, rppft3], ids=lambda x: f"func={x.__name__}")
def test_ppft2_sequential_equals_vectorized(data_3d: NDArray, func: Callable) -> None:
    """TODO."""
    output_vectorized = func(data_3d, vectorized=True)
    output_sequential = func(data_3d, vectorized=False)

    np.testing.assert_equal(output_vectorized, output_sequential)


@pytest.mark.parametrize(
    "dtype",
    [*SUPPORTED_DTYPES_NON_COMPLEX, *SUPPORTED_DTYPES_COMPLEX],
    ids=lambda x: f"dtype={x}",
)
def test_ppft3_supports_data_types(dtype: DTypeLike) -> None:
    """TODO."""
    data = np.ones((4, 4, 4), dtype=dtype)
    out = ppft3(data)

    assert not np.isnan(out).any()
    assert np.issubdtype(out.dtype, np.complexfloating)


@pytest.mark.parametrize(
    "dtype", [*SUPPORTED_DTYPES_NON_COMPLEX], ids=lambda x: f"dtype={x}"
)
@pytest.mark.parametrize("func", [ppft3, rppft3], ids=lambda x: f"func={x.__name__}")
def test_rppft3_supports_non_complex_data_types(
    func: Callable, dtype: DTypeLike
) -> None:
    """TODO."""
    data = np.ones((4, 4, 4), dtype=dtype)
    out = func(data)

    assert not np.isnan(out).any()
    assert np.issubdtype(out.dtype, np.complexfloating)


def test_ppft3_returns_correct_shape(data_3d: NDArray) -> None:
    """Verify that all PPFT3 generates two "Pseudo-Polar" outputs.

    PPFT3 generates two "Pseudo-Polar" outputs.
    Each has a shape of (3xN+1, N+1, N+1).
    All outputs are then combined into a single 3D matrix with the shape
    of (3, 3xN+1, N+1, N+1).
    """
    data = data_3d

    n = len(data)

    # We expect 2 sectors with each element having a shape of (3*n+1, n+1, n+1).
    # For n=4, the expected shape is (3, 13, 5, 5).
    expected_shape = (3, 3 * n + 1, n + 1, n + 1)

    assert ppft3(data).shape == expected_shape


def test_ppft3_sectors_symmetric_data(data_3d: NDArray) -> None:
    """Verfiy that all values in a fourier image are equal at its mirrored position."""
    data = data_3d

    # We only care for the magnitude of the data.
    sec1, sec2, sec3 = np.abs(ppft3(data))

    # The returned ppft3D has two fourier-transformed sectors,
    # therefore we need to compare both parts.
    assert sec1.shape == sec2.shape == sec3.shape

    np.testing.assert_allclose(np.flipud(sec1), sec1, rtol=RTOL, atol=ATOL)
    np.testing.assert_allclose(np.flipud(sec2), sec2, rtol=RTOL, atol=ATOL)
    np.testing.assert_allclose(np.flipud(sec3), sec3, rtol=RTOL, atol=ATOL)


@pytest.mark.parametrize("vectorized", [True, False], ids=lambda x: f"vectorized={x}")
@pytest.mark.parametrize("scipy_fft", [True, False], ids=lambda x: f"scipy_fft={x}")
def test_rppft3_equals_ppft3(
    data_3d: NDArray, *, vectorized: bool, scipy_fft: bool
) -> None:
    """TODO."""
    data = data_3d

    if scipy_fft:
        pytest.importorskip("scipy", reason="SciPy is not installed")

    n = len(data)
    x = n + n // 2

    actual = rppft3(data, vectorized=vectorized, scipy_fft=scipy_fft)
    expected = ppft3(data, vectorized=vectorized, scipy_fft=scipy_fft)[:, x:]

    if scipy_fft:
        np.testing.assert_equal(actual, expected)
    else:
        np.testing.assert_allclose(actual, expected, rtol=1e-15, atol=1e-11)


@pytest.mark.parametrize("vectorized", [True, False])
@pytest.mark.parametrize("ppft_func", [ppft3, rppft3])
def test_ppft3_single_equals_multi_mode(
    data_3d: NDArray, ppft_func: Callable, *, vectorized: bool
) -> None:
    """TODO."""
    data = data_3d

    # We add arbitrary data as vectorized input.
    expanded_data = np.stack([data, data * 0.5, data * 0.3, data * 0.1])

    actual = ppft_func(expanded_data, vectorized=vectorized)
    expected = np.array([ppft_func(d, vectorized=vectorized) for d in expanded_data])

    np.testing.assert_equal(actual, expected)


@pytest.mark.parametrize("ppft_func", [ppft3, rppft3])
def test_ppft3_vectorized_equals_sequential(
    data_3d: NDArray, ppft_func: Callable
) -> None:
    """TODO."""
    data = data_3d

    expected = ppft_func(data, vectorized=True)
    actual = ppft_func(data, vectorized=False)

    np.testing.assert_equal(actual, expected)


@pytest.mark.parametrize("func", [ppft3, rppft3])
@pytest.mark.parametrize("dimension", [1, 2, 5])
@pytest.mark.parametrize("size", [2, 4, 8])
def test_ppft3_fails_for_non_3d_data(func: Callable, size: int, dimension: int) -> None:
    """TODO."""
    data = np.zeros((size,) * dimension)

    with pytest.raises(
        ValueError,
        match="Input data must a single NxNxN matrix or an array of NxNxN matrices",
    ):
        func(data)


@pytest.mark.parametrize("size", [1, 2, 5, 6, 7, 8])
def test_ppft3_fails_for_non_cube_data(size: int) -> None:
    """TODO."""
    data = np.zeros((4, 4, size))

    with pytest.raises(
        ValueError, match="Input data must have sides with same lengths"
    ):
        ppft3(data)


@pytest.mark.parametrize("size", [1, 3, 5, 7, 9, 11, 13, 15, 17, 19])
def test_ppft3_fails_for_odd_sized_data(size: int) -> None:
    """TODO."""
    data = np.zeros((size,) * 3)

    with pytest.raises(ValueError, match="Input data must have even sides"):
        ppft3(data)


@pytest.mark.parametrize("ppft3_func", [ppft3])
def test_ppft3_original_example_im2(ppft3_func: Callable) -> None:
    """Verify example input to be converted to proper output shape.

    This example is a test for a single test input for PPFT3 that has
    been manually compared to the output of the original MATLAB code.
    """
    data = np.ones((4, 4, 4)) * np.array([0.1, 0.2, 0.3, 0.4]).reshape(1, 1, 4)

    assert data.shape == (4, 4, 4)
    assert data.ndim == 3  # noqa: PLR2004
    assert data.dtype == np.float64
    result = ppft3_func(data)

    assert result.shape == (3, 13, 5, 5)

    assert result[0, 0, 0, 0] == pytest.approx(0.0462 - 0.0099j, rel=1e-3)
    np.testing.assert_allclose(
        result[0, :, 0, 0],
        np.array(
            [
                0.0462 - 0.0099j,
                0.2890 - 0.0932j,
                0.1509 - 0.0658j,
                0.0269 - 0.0328j,
                1.6290 - 1.8533j,
                9.3580 - 4.7693j,
                16.0000 + 0.0000j,
                9.3580 + 4.7693j,
                1.6290 + 1.8533j,
                0.0269 + 0.0328j,
                0.1509 + 0.0658j,
                0.2890 + 0.0932j,
                0.0462 + 0.0099j,
            ]
        ),
        rtol=1e-2,
    )

    np.testing.assert_allclose(
        result[0, 0, :, 0],
        np.array(
            [
                0.0462 - 0.0099j,
                -0.0317 - 0.0179j,
                -0.1316 - 0.3820j,
                0.0140 - 0.0337j,
                -0.0425 + 0.0207j,
            ]
        ),
        rtol=1e-2,
    )


@pytest.mark.parametrize("ppft3_func", [ppft3])
def test_ppft3_original_example_im2_ones(ppft3_func: Callable) -> None:
    """Verify example input to be converted to proper output shape.

    This example is a test for a single test input for PPFT3 that has
    been manually compared to the output of the original MATLAB code.
    """
    # Define the array in Python using NumPy
    data = np.ones((4,) * 3) * np.ones(4).reshape(1, 1, 4)
    assert data.shape == (4, 4, 4)
    assert data.ndim == 3  # noqa: PLR2004
    assert data.dtype == np.float64

    result = ppft3_func(data)
    assert result.shape == (3, 13, 5, 5)

    np.testing.assert_allclose(
        result[0, :, 0, 0],
        np.array(
            [
                0.0364 - 0.0959j,
                1.0597 - 0.5562j,
                0.5079 + 0.1252j,
                -0.0267 - 0.0387j,
                0.9817 - 8.0853j,
                30.4410 - 26.9684j,
                64.0000 + 0.0000j,
                30.4410 + 26.9684j,
                0.9817 + 8.0853j,
                -0.0267 + 0.0387j,
                0.5079 - 0.1252j,
                1.0597 + 0.5562j,
                0.0364 + 0.0959j,
            ]
        ),
        rtol=1e-3,
    )

    np.testing.assert_allclose(
        result[0, 0, :, 0],
        np.array(
            [
                0.0364 - 0.0959j,
                -0.0700 + 0.0368j,
                -0.8511 - 0.2098j,
                -0.0449 - 0.0651j,
                -0.0124 + 0.1018j,
            ]
        ),
        rtol=1e-3,
    )
