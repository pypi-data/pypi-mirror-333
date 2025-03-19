from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Final

from ._utils import _get_config, _get_pq_pz, _get_rpq_rpz, _verify_dtype_non_complex

if TYPE_CHECKING:
    from types import EllipsisType, ModuleType

    import numpy as np
    from numpy.typing import NDArray

__MULTI_MODE_2D: Final = 3


def ppft2(
    data: NDArray, /, *, vectorized: bool = False, scipy_fft: bool = False
) -> NDArray[np.complex128 | np.complex256]:
    """Compute the 2D Pseudo-Polar Fourier Transform.

    This function computes the 2-dimensional Pseudo-Polar Fourier
    Transform [Averbuch2001]_.

    Parameters
    ----------
    data
        The input data, either a single 2D matrix (shape ``(N, N)``) or a batch
        of 2D matrices (shape ``(V, N, N)``). Each matrix must be square with
        even length. The data can be either real or complex.
    scipy_fft
        If ``True``, uses SciPy's FFT backend (``scipy.fft``) or a registered
        backend via SciPy's backend control instead of the native array's FFT
        implementation (e.g., ``numpy.fft``). This may improve performance but
        requires SciPy to be installed.
    vectorized
        If ``True``, computes the transform using a fully vectorized approach.
        This is significantly faster but requires more memory. Use with caution
        for large datasets.

    Returns
    -------
        The computed 2D Pseudo-Polar Fourier Transform. The output shape
        depends on the input:

        - If `data` has shape ``(N, N)``, the output has shape ``(2, 2N+1, N+1)``.
        - If `data` has shape ``(V, N, N)``, the output has shape ``(V, 2, 2N+1, N+1)``.

    Raises
    ------
    ValueError
        If the input shape is not ``(N, N)`` (single 2D matrix) or
        ``(V, N, N)`` (multiple 2D matrices) with even ``N`` and arbitrary ``V``.
    ModuleNotFoundError
        If `scipy_fft=True` but SciPy is not installed.

    See Also
    --------
    rppft2 : The 2D Pseudo-Polar Fourier Transform of real input.
    ppft3 : The 3D Pseudo-Polar Fourier Transform.

    References
    ----------
    .. [Averbuch2001] A. Averbuch, R. Coifman, D. Donoho, M. Israeli, and J.
       Waldén, "Fast Slant Stack: A notion of Radon Transform for Data in a
       Cartesian Grid which is Rapidly Computible, Algebraically Exact,
       Geometrically Faithful and Invertible," 2001.

    Examples
    --------
    >>> from ppftpy import ppft2
    >>> import numpy as np
    >>> arr = np.random.default_rng().random((4, 4))
    >>> ppft2(arr).shape
    (2, 9, 5)

    Compute PPFT2D for 3 arrays.

    >>> from ppftpy import ppft2
    >>> import numpy as np
    >>> arr = np.random.default_rng().random((3, 4, 4))
    >>> ppft2(arr).shape
    (3, 2, 9, 5)
    """
    __verify_data_shape(data)

    ppft_func = __ppft2_vectorized if vectorized else __ppft2_sequential
    return ppft_func(data, scipy_fft=scipy_fft, real_mode=False)


def rppft2(
    data: NDArray, /, *, vectorized: bool = False, scipy_fft: bool = False
) -> NDArray[np.complex128 | np.complex256]:
    """Compute the 2D Pseudo-Polar Fourier Transform for real input.

    This function computes the 2-dimensional Pseudo-Polar Fourier Transform
    [Averbuch2001]_ for real input. The real PPFT2D computes only the non-redundant half
    of the spectrum.

    Parameters
    ----------
    data
        The input data, either a single 2D matrix (shape ``(N, N)``) or a batch
        of 2D matrices (shape ``(V, N, N)``). Each matrix must be square with
        even length. The data can be either real or complex.
    scipy_fft
        If ``True``, uses SciPy's FFT backend (``scipy.fft``) or a registered
        backend via SciPy's backend control instead of the native array's FFT
        implementation (e.g., ``numpy.fft``). This may improve performance but
        requires SciPy to be installed.
    vectorized
        If ``True``, computes the transform using a fully vectorized approach.
        This is significantly faster but requires more memory. Use with caution
        for large datasets.

    Returns
    -------
        The computed 2D Pseudo-Polar Fourier Transform. The output shape
        depends on the input:

        - If `data` has shape ``(N, N)``, the output has shape ``(2, N+1, N+1)``.
        - If `data` has shape ``(V, N, N)``, the output has shape ``(V, 2, N+1, N+1)``.

    Raises
    ------
    ValueError
        If the input shape is not ``(N, N)`` (single 2D matrix) or
        ``(V, N, N)`` (multiple 2D matrices) with even ``N`` and arbitrary ``V``.
    ModuleNotFoundError
        If `scipy_fft=True` but SciPy is not installed.
    TypeError
        If the input data is complex.

    See Also
    --------
    ppft2 : The 2D Pseudo-Polar Fourier Transform.
    rppft3 : The 3D Pseudo-Polar Fourier Transform of real input.

    References
    ----------
    .. [Averbuch2001] A. Averbuch, R. Coifman, D. Donoho, M. Israeli, and J.
       Waldén, "Fast Slant Stack: A notion of Radon Transform for Data in a
       Cartesian Grid which is Rapidly Computible, Algebraically Exact,
       Geometrically Faithful and Invertible," 2001.

    Examples
    --------
    >>> from ppftpy import rppft2
    >>> import numpy as np
    >>> arr = np.random.default_rng().random((4, 4))
    >>> rppft2(arr).shape
    (2, 5, 5)

    Compute PPFT2D for 3 arrays.

    >>> from ppftpy import rppft2
    >>> import numpy as np
    >>> arr = np.random.default_rng().random((3, 4, 4))
    >>> rppft2(arr).shape
    (3, 2, 5, 5)
    """
    __verify_data_shape(data)
    _verify_dtype_non_complex(data)

    ppft_func = __ppft2_vectorized if vectorized else __ppft2_sequential
    return ppft_func(data, scipy_fft=scipy_fft, real_mode=True)


def __ppft2_vectorized(
    data: NDArray, *, scipy_fft: bool, real_mode: bool
) -> NDArray[np.complex128 | np.complex256]:
    xp, xp_inner, fft, device, rechunk, compute = _get_config(data, scipy_fft=scipy_fft)

    n = len(data[-1])
    nh = n // 2
    np = n + 1
    np3 = np * 3
    m = 2 * n + 1
    mx = np if real_mode else m
    md = m - nh
    idx = (..., slice(md, md + np))
    multi = data.ndim == __MULTI_MODE_2D
    amount = len(data) if multi else 1
    sectors = amount * 2

    pq_pz_func = _get_rpq_rpz if real_mode else _get_pq_pz
    pq, pz = pq_pz_func(
        n, dim=2, xp=xp, xp_inner=xp_inner, scipy_fft=scipy_fft, device=device
    )

    data_flipped = xp.flip(data, axis=-2)
    out = xp.stack([data_flipped, xp.moveaxis(data_flipped, -2, -1)])
    out = xp.reshape(out, (-1, n, n))

    zeros = xp_inner.zeros((sectors, nh + 1, n), device=device)
    out = xp.concatenate([zeros[:, :-1], out, zeros], axis=1)
    out = fft.ifftshift(out, axes=1)

    if rechunk:
        out = out.rechunk({1: -1})

    out = (
        fft.rfft(out, axis=1)
        if real_mode
        else fft.fftshift(fft.fft(out, axis=1), axes=1)
    )

    if compute:
        out = out.compute()

    zeros = xp_inner.zeros((sectors, mx, 1), device=device)
    out = xp.concatenate([out, zeros], axis=2) * pq

    if rechunk:
        out = out.rechunk({-1: -1})

    out = fft.ifft(fft.fft(out, n=np3) * pz)[idx] * pq

    if multi:
        out = xp.moveaxis(xp.reshape(out, (2, amount, mx, np)), 0, 1)

    return xp.flip(out, axis=-1)


def __ppft2_sequential(
    data: NDArray, *, scipy_fft: bool, real_mode: bool
) -> NDArray[np.complex128 | np.complex256]:
    xp, xp_inner, fft, device, rechunk, compute = _get_config(data, scipy_fft=scipy_fft)

    n = len(data[-1])
    nh = n // 2
    np = n + 1
    np3 = np * 3
    m = 2 * n + 1
    mx = np if real_mode else m
    md = m - nh
    idx = (..., slice(md, md + np))
    multi = data.ndim == __MULTI_MODE_2D
    amount = len(data) if multi else 1

    pq_pz_func = _get_rpq_rpz if real_mode else _get_pq_pz
    pq, pz = pq_pz_func(
        n, dim=2, xp=xp, xp_inner=xp_inner, scipy_fft=scipy_fft, device=device
    )

    data_flipped = xp.flip(data, axis=-2)
    data_stacked = data_flipped if multi else (data_flipped,)
    zeros_1 = xp_inner.zeros((nh + 1, n), device=device)

    ops = (xp.moveaxis(x, i, 0) for x, i in itertools.product(data_stacked, range(2)))
    ops = (xp.concatenate([zeros_1[:-1], x, zeros_1]) for x in ops)
    ops = (fft.ifftshift(x, axes=0) for x in ops)

    if rechunk:
        ops = (x.rechunk({0: -1}) for x in ops)

    ops = (
        fft.rfft(x, axis=0) if real_mode else fft.fftshift(fft.fft(x, axis=0), axes=0)
        for x in ops
    )

    if compute:
        ops = (x.compute() for x in ops)

    zeros_2 = xp_inner.zeros((mx, 1), device=device)
    out = xp.stack(
        [
            __apply_qz(x, pq, pz, zeros_2, np3, idx, xp, fft, rechunk=rechunk)
            for x in ops
        ]
    )

    if multi:
        out = xp.reshape(out, (amount, 2, mx, np))

    return xp.flip(out, axis=-1)


def __apply_qz(  # noqa: PLR0913
    x: NDArray,
    q: NDArray,
    z: NDArray,
    zeros: NDArray,
    np3: int,
    idx: tuple[EllipsisType | slice, ...],
    xp: ModuleType,
    fft: ModuleType,
    *,
    rechunk: bool,
) -> NDArray[np.complex128 | np.complex256]:
    x = xp.concatenate([x, zeros], axis=1) * q

    if rechunk:
        x = x.rechunk({-1: -1})

    return fft.ifft(fft.fft(x, n=np3) * z)[idx] * q


def __verify_data_shape(data: NDArray) -> None:
    if data.ndim not in (2, 3):
        msg = "Input data must a single NxN matrix or an array of NxN matrices"
        raise ValueError(msg)

    inner = data[0] if data.ndim == __MULTI_MODE_2D else data

    if len(set(inner.shape)) != 1:
        msg = "Input data must have sides with same lengths"
        raise ValueError(msg)

    if len(inner) % 2 != 0:
        msg = "Input data must have even sides"
        raise ValueError(msg)
