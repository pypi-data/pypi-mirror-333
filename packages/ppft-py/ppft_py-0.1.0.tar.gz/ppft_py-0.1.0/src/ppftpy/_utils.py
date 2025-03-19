from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any, Literal

from array_api_compat import (
    get_namespace,
    is_cupy_namespace,
    is_dask_namespace,
    is_torch_namespace,
)

try:
    import scipy.fft as sc_fft
except ImportError:
    sc_fft = None

if TYPE_CHECKING:
    from types import ModuleType

    import numpy as np
    from numpy.typing import NDArray

    TorchDeviceOrNone = Any | None


def _get_config(
    data: NDArray, *, scipy_fft: bool
) -> tuple[ModuleType, ModuleType, ModuleType, TorchDeviceOrNone, bool, bool]:
    xp = get_namespace(data)
    xp_inner = xp
    fft = _get_fft_backend(xp, scipy_fft=scipy_fft)
    device = data.device if is_torch_namespace(xp) else None
    rechunk = False
    compute = False

    if is_dask_namespace(xp):
        # For operating on Dask arrays, we need the actual underlying
        # namespace if it is CuPy (i.e., data is on GPUs). We also do
        # this for NumPy arrays on CPU for consistency. Accessing
        # '_meta' is considered safe to get the underlying array type:
        # https://github.com/dask/dask/issues/6442
        xp_inner = get_namespace(data._meta)
        rechunk = True

        if is_cupy_namespace(xp_inner):
            compute = True

    return xp, xp_inner, fft, device, rechunk, compute


def _get_fft_backend(xp: ModuleType, *, scipy_fft: bool) -> ModuleType:
    if not scipy_fft:
        return xp.fft

    if sc_fft is None:
        msg = "SciPy FFT module is not available, install SciPy to use this feature"
        raise ModuleNotFoundError(msg)

    return sc_fft


def _verify_dtype_non_complex(data: NDArray) -> None:
    if get_namespace(data).isdtype(data.dtype, "complex floating"):
        msg = "Complex data is not supported, please provide real-valued input"
        raise TypeError(msg)


@functools.cache
def _get_pq_pz(
    n: int,
    *,
    dim: Literal[2, 3],
    xp: ModuleType,
    xp_inner: ModuleType,
    scipy_fft: bool,
    device: TorchDeviceOrNone = None,
) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
    fft = _get_fft_backend(xp, scipy_fft=scipy_fft)

    np = n + 1
    nh = n // 2
    nhp = nh + 1
    m = n * dim + 1
    mh = m // 2

    arange_mh = xp_inner.arange(-mh, mh + 1, device=device)
    arange_np = xp_inner.arange(-np, np + 1, device=device)
    px = 2j * xp.pi / (n * m) * arange_mh[:, None] * arange_np**2

    pq = xp.exp(-px[:, nhp:-nhp])

    zeros = xp_inner.zeros((m, nh), device=device)
    padded = xp.concatenate((zeros, xp.exp(px), zeros), axis=1)

    if is_dask_namespace(xp):
        padded = padded.rechunk({-1: -1})

    pz = fft.fft(padded)

    return pq, pz


@functools.cache
def _get_rpq_rpz(
    n: int, *, dim: Literal[2, 3], **kwargs: Any
) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
    pq, pz = _get_pq_pz(n, dim=dim, **kwargs)
    x = (dim * n) // 2

    return pq[x:], pz[x:]
