from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Final

from ._utils import _get_config, _get_pq_pz, _get_rpq_rpz, _verify_dtype_non_complex

if TYPE_CHECKING:
    from types import ModuleType

    import numpy as np
    from numpy.typing import NDArray

__MULTI_MODE_3D: Final = 4


def ppft3(
    data: NDArray, /, *, vectorized: bool = False, scipy_fft: bool = False
) -> NDArray[np.complex128 | np.complex256]:
    """Compute the 3D Pseudo-Polar Fourier Transform.

    This function computes the 3-dimensional Pseudo-Polar Fourier
    Transform [Averbuch2003]_.

    Parameters
    ----------
    data
        The input data, either a single 3D matrix (shape ``(N, N, N)``) or a
        batch of 3D matrices (shape ``(V, N, N, N)``). Each matrix must be
        cubical with even length. The data can be either real or complex.
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
        The computed 3D Pseudo-Polar Fourier Transform. The output shape
        depends on the input:

        - If `data` has shape ``(N, N, N)``, the output has shape
          ``(3, 3N+1, N+1, N+1)``.
        - If `data` has shape ``(V, N, N, N)``, the output has shape
          ``(V, 3, 3N+1, N+1, N+1)``.

    Raises
    ------
    ValueError
        If the input shape is not ``(N, N, N)`` or ``(V, N, N, N)`` with even
        ``N`` and arbitrary ``V``.
    ModuleNotFoundError
        If `scipy_fft=True` but SciPy is not installed.

    See Also
    --------
    rppft3 : The 3D Pseudo-Polar Fourier Transform of real input.
    ppft2 : The 2D Pseudo-Polar Fourier Transform.

    References
    ----------
    .. [Averbuch2003] A. Averbuch and Y. Shkolnisky, "3D Fourier based discrete
       Radon transform," Applied and Computational Harmonic Analysis, vol. 15,
       no. 1, pp. 33-69, Jul. 2003, issn: 1063-5203.
       `doi:10.1016/s1063-5203(03)00030-7
       <https://doi.org/10.1016/s1063-5203(03)00030-7>`_.

    Examples
    --------
    >>> from ppftpy import ppft3
    >>> import numpy as np
    >>> arr = np.random.default_rng().random((4, 4, 4))
    >>> ppft3(arr).shape
    (3, 13, 5, 5)

    Compute PPFT3D for 2 arrays.

    >>> from ppftpy import ppft3
    >>> import numpy as np
    >>> arr = np.random.default_rng().random((2, 4, 4, 4))
    >>> ppft3(arr).shape
    (2, 3, 13, 5, 5)
    """
    __verify_data_shape(data)

    ppft_func = __ppft3_vectorized if vectorized else __ppft3_sequential
    return ppft_func(data, scipy_fft=scipy_fft, real_mode=False)


def rppft3(
    data: NDArray, /, *, vectorized: bool = False, scipy_fft: bool = False
) -> NDArray[np.complex128 | np.complex256]:
    """Compute the 3D Pseudo-Polar Fourier Transform for real input.

    This function computes the 3-dimensional Pseudo-Polar Fourier Transform
    [Averbuch2003]_ for real input. The real PPFT3D computes only the non-redundant half
    of the spectrum.

    Parameters
    ----------
    data
        The input data, either a single 3D matrix (shape ``(N, N, N)``) or a
        batch of 3D matrices (shape ``(V, N, N, N)``). Each matrix must be
        cubical with even length. The data can be either real or complex.
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
        The computed 3D Pseudo-Polar Fourier Transform. The output shape
        depends on the input:

        - If `data` has shape ``(N, N, N)``, the output has shape
          ``(3, 3N+1, N+1, N+1)``.
        - If `data` has shape ``(V, N, N, N)``, the output has shape
          ``(V, 3, 3N+1, N+1, N+1)``.

    Raises
    ------
    ValueError
        If the input shape is not ``(N, N, N)`` (single 3D matrix) or ``(V, N, N, N)``
        (multiple 3D matrices) with even ``N`` and arbitrary ``V``.
    ModuleNotFoundError
        If `scipy_fft=True` but SciPy is not installed.
    TypeError
        If the input data is complex.

    See Also
    --------
    ppft3 : The 3D Pseudo-Polar Fourier Transform.
    rppft2 : The 2D Pseudo-Polar Fourier Transform of real input.

    References
    ----------
    .. [Averbuch2003] A. Averbuch and Y. Shkolnisky, "3D Fourier based discrete
       Radon transform," Applied and Computational Harmonic Analysis, vol. 15,
       no. 1, pp. 33-69, Jul. 2003, issn: 1063-5203.
       `doi:10.1016/s1063-5203(03)00030-7
       <https://doi.org/10.1016/s1063-5203(03)00030-7>`_.

    Examples
    --------
    >>> from ppftpy import rppft3
    >>> import numpy as np
    >>> arr = np.random.default_rng().random((4, 4, 4))
    >>> rppft3(arr).shape
    (3, 7, 5, 5)

    Compute PPFT3D for 2 arrays.

    >>> from ppftpy import rppft3
    >>> import numpy as np
    >>> arr = np.random.default_rng().random((2, 4, 4, 4))
    >>> rppft3(arr).shape
    (2, 3, 7, 5, 5)
    """
    __verify_data_shape(data)
    _verify_dtype_non_complex(data)

    ppft_func = __ppft3_vectorized if vectorized else __ppft3_sequential
    return ppft_func(data, scipy_fft=scipy_fft, real_mode=True)


def __ppft3_vectorized(
    data: NDArray, *, scipy_fft: bool, real_mode: bool
) -> NDArray[np.complex128 | np.complex256]:
    xp, xp_inner, fft, device, rechunk, compute = _get_config(data, scipy_fft=scipy_fft)

    n = len(data[-1])
    np = n + 1
    np3 = np * 3
    m = 3 * n + 1
    mx = m // 2 + 1 if real_mode else m
    md = (2 * n + 1) - n // 2
    idx = (..., slice(md, md + np), slice(None))
    multi = data.ndim == __MULTI_MODE_3D
    amount = len(data) if multi else 1
    sectors = amount * 3

    pq_pz_func = _get_rpq_rpz if real_mode else _get_pq_pz
    pq, pz = pq_pz_func(
        n, dim=3, xp=xp, xp_inner=xp_inner, scipy_fft=scipy_fft, device=device
    )
    pq = pq[None, :, :, None]
    pz = pz[None, :, :, None]

    out = xp.stack([data, xp.moveaxis(data, -2, -3), xp.moveaxis(data, -1, -3)])
    out = xp.reshape(out, (-1, n, n, n))

    zeros = xp_inner.zeros((sectors, n + 1, n, n), device=device)
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

    zeros = xp_inner.zeros((sectors, mx, 1, np), device=device)
    out = xp.concatenate([xp.moveaxis(out, -2, -1), zeros[..., :-1]], axis=2) * pq

    if rechunk:
        out = out.rechunk({2: -1})

    out = fft.ifft(fft.fft(out, n=np3, axis=2) * pz, axis=2)[idx] * pq

    if compute:
        out = out.compute()

    out = xp.concatenate([xp.moveaxis(out, -2, -1), zeros], axis=2) * pq

    if rechunk:
        out = out.rechunk({2: -1})

    out = fft.ifft(fft.fft(out, n=np3, axis=2) * pz, axis=2)[idx] * pq

    if multi:
        out = xp.moveaxis(xp.reshape(out, (3, amount, mx, np, np)), 0, 1)

    return xp.flip(xp.flip(out, axis=-1), axis=-2)


def __ppft3_sequential(
    data: NDArray, *, scipy_fft: bool, real_mode: bool
) -> NDArray[np.complex128 | np.complex256]:
    xp, xp_inner, fft, device, rechunk, compute = _get_config(data, scipy_fft=scipy_fft)

    n = len(data[-1])
    np = n + 1
    np3 = np * 3
    m = 3 * n + 1
    mx = m // 2 + 1 if real_mode else m
    md = (2 * n + 1) - n // 2
    idx = slice(md, md + np)
    multi = data.ndim == __MULTI_MODE_3D
    amount = len(data) if multi else 1

    pq_pz_func = _get_rpq_rpz if real_mode else _get_pq_pz
    pq, pz = pq_pz_func(
        n, dim=3, xp=xp, xp_inner=xp_inner, scipy_fft=scipy_fft, device=device
    )
    pq = pq[..., None]
    pz = pz[..., None]

    data_stacked = data if multi else (data,)
    zeros_1 = xp_inner.zeros((n + 1, n, n), device=device)

    ops = (xp.moveaxis(x, i, 0) for x, i in itertools.product(data_stacked, range(3)))
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

    zeros_2 = xp_inner.zeros((1, np), device=device)
    params = zeros_2, np3, idx, xp, fft
    out = xp.stack(
        [
            __pp_sector(x, params, pq, pz, xp=xp, compute=compute, rechunk=rechunk)
            for x in ops
        ]
    )

    if multi:
        out = xp.reshape(out, (amount, 3, mx, np, np))

    return xp.flip(xp.flip(out, axis=-1), axis=-2)


def __pp_sector(  # noqa: PLR0913
    x: NDArray,
    params: tuple[NDArray, int, slice, ModuleType, ModuleType],
    pq: NDArray,
    pz: NDArray,
    *,
    xp: ModuleType,
    compute: bool,
    rechunk: bool,
) -> NDArray[np.complex128 | np.complex256]:
    return xp.stack(
        [
            __apply_qz(
                __apply_qz(_x, q, z, *params, compute=compute, rechunk=rechunk),
                q,
                z,
                *params,
                compute=False,
                rechunk=rechunk,
            )
            for _x, q, z in zip(x, pq, pz, strict=False)
        ]
    )


def __apply_qz(  # noqa: PLR0913
    x: NDArray,
    q: NDArray,
    z: NDArray,
    zeros: NDArray,
    np3: int,
    idx: slice,
    xp: ModuleType,
    fft: ModuleType,
    *,
    rechunk: bool,
    compute: bool,
) -> NDArray[np.complex128 | np.complex256]:
    x = xp.concatenate([x.T, zeros[:, : len(x)]]) * q

    if rechunk:
        x = x.rechunk({0: -1})

    x = fft.ifft(fft.fft(x, n=np3, axis=0) * z, axis=0)[idx] * q

    if compute:
        x = x.compute()

    return x


def __verify_data_shape(data: NDArray) -> None:
    if data.ndim not in (3, 4):
        msg = "Input data must a single NxNxN matrix or an array of NxNxN matrices"
        raise ValueError(msg)

    inner = data[0] if data.ndim == __MULTI_MODE_3D else data

    if len(set(inner.shape)) != 1:
        msg = "Input data must have sides with same lengths"
        raise ValueError(msg)

    if len(inner) % 2 != 0:
        msg = "Input data must have even sides"
        raise ValueError(msg)
