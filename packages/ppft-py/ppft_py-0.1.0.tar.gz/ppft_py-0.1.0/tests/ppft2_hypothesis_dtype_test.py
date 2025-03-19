"""TODO."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays

from ppftpy import ppft2, rppft2

if TYPE_CHECKING:
    from collections.abc import Callable

    from numpy.typing import DTypeLike, NDArray

MAX_SHAPE_SIZE: Final = 32
VALID_SHAPE_2D: Final = (
    st.integers(2, MAX_SHAPE_SIZE).filter(lambda x: x % 2 == 0).map(lambda n: (n, n))
)

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


@pytest.mark.parametrize("dtype", SUPPORTED_DTYPES_NON_COMPLEX)
@pytest.mark.parametrize("ppft_func", [ppft2, rppft2])
@given(
    data=arrays(
        dtype=np.float64,
        shape=VALID_SHAPE_2D,
        elements=st.floats(-1.0, 1.0, allow_nan=False, allow_infinity=False),
    )
)
@settings(deadline=None)
def test_ppft2_dtype_handling_non_complex(
    dtype: DTypeLike, ppft_func: Callable, data: NDArray
) -> None:
    """Ensure all valid NumPy dtypes produce valid complex128 output."""
    data = data.astype(dtype)
    output = ppft_func(data)

    assert np.issubdtype(output.dtype, np.complexfloating), (
        "Output is not of a complex type"
    )
    assert not np.isnan(output).any(), "Output contains NaN values"


@given(
    data=arrays(
        dtype=st.sampled_from(SUPPORTED_DTYPES_COMPLEX),
        shape=VALID_SHAPE_2D,
        elements=st.complex_numbers(
            min_magnitude=0.0,
            max_magnitude=1.0,
            allow_nan=False,
            allow_infinity=False,
            width=64,
        ),
    )
)
@settings(deadline=None)
def test_ppft2_dtype_handling_complex(data: NDArray) -> None:
    """Ensure all complex NumPy dtypes produce valid complex128 output."""
    output = ppft2(data)

    assert np.issubdtype(output.dtype, np.complexfloating), (
        "Output is not of a complex type"
    )
    assert not np.isnan(output).any(), "Output contains NaN values"


@given(
    data=arrays(dtype=st.sampled_from(SUPPORTED_DTYPES_COMPLEX), shape=VALID_SHAPE_2D)
)
def test_ppft2_dtype_handling_real_mode_complex_raises(data: NDArray) -> None:
    """Ensure real PPFT2D only allows non-complex data input."""
    with pytest.raises(
        TypeError,
        match="Complex data is not supported, please provide real-valued input",
    ):
        rppft2(data)
