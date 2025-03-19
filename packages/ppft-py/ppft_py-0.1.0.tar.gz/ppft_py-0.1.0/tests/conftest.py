"""TODO."""

from __future__ import annotations

import importlib
import sys
from typing import TYPE_CHECKING, Final
from unittest import mock

import numpy as np
import pytest
from _pytest.compat import NotSetType

from ._helpers import (
    EXISTING_PPFT2_REGRESSION_TEST_PAIRS,
    EXISTING_PPFT3_REGRESSION_TEST_PAIRS,
    USER_ENABLED_ARRAY_BACKENDS,
    USER_ENABLED_SCIPY_BACKENDS,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from numpy.typing import NDArray

    from ._helpers import ArrayBackend, RegressionTestPair, ScipyBackend

DATA_2D: Final = ["gradient_data_2d", "ones_data_2d", "random_data_2d"]
DATA_3D: Final = ["gradient_data_3d", "ones_data_3d", "random_data_3d"]

DATA_SIZE_2D: Final = [2, 4, 8, 16, 32, 64]
DATA_SIZE_3D: Final = [2, 4, 8, 16]

DEFAULT_SEED: Final = 0
DEFAULT_RNG: Final = np.random.default_rng(DEFAULT_SEED)


@pytest.fixture
def zeros_data_2d(data_size_2d: int) -> NDArray:
    """Return data with only zeros (i.e., black) data."""
    return np.zeros((data_size_2d,) * 2)


@pytest.fixture
def ones_data_2d(data_size_2d: int) -> NDArray:
    """Return data with only ones (i.e., white) data."""
    return np.ones((data_size_2d,) * 2)


@pytest.fixture
def gradient_data_2d(data_size_2d: int) -> NDArray:
    """Return gradient data data."""
    gradient_matrix = np.linspace(0, 1, data_size_2d)
    return np.meshgrid(gradient_matrix, gradient_matrix)[0]


@pytest.fixture
def random_data_2d(data_size_2d: int) -> NDArray:
    """Return random data."""
    return DEFAULT_RNG.random((data_size_2d,) * 2)


@pytest.fixture
def zeros_data_3d(data_size_3d: int) -> NDArray:
    """Return data with only zeros (i.e., black) data."""
    return np.zeros((data_size_3d,) * 3)


@pytest.fixture
def ones_data_3d(data_size_3d: int) -> NDArray:
    """Return data with only ones (i.e., white) data."""
    return np.ones((data_size_3d,) * 3)


@pytest.fixture
def gradient_data_3d(data_size_3d: int) -> NDArray:
    """Return gradient data data."""
    gradient_matrix = np.linspace(0, 1, data_size_3d)
    return np.meshgrid(gradient_matrix, gradient_matrix, gradient_matrix)[0]


@pytest.fixture
def random_data_3d(data_size_3d: int) -> NDArray:
    """Return random data."""
    return DEFAULT_RNG.random((data_size_3d,) * 3)


@pytest.fixture(params=DATA_SIZE_2D)
def data_size_2d(request: pytest.FixtureRequest) -> int:
    """Fixture to provide different data sizes."""
    return request.param


@pytest.fixture(params=DATA_SIZE_3D)
def data_size_3d(request: pytest.FixtureRequest) -> int:
    """Fixture to provide different data sizes."""
    return request.param


@pytest.fixture(params=DATA_2D)
def data_2d(request: pytest.FixtureRequest, data_size_2d: int) -> NDArray:  # noqa: ARG001
    """Fixture to provide different types of data."""
    return request.getfixturevalue(request.param)


@pytest.fixture(params=DATA_3D)
def data_3d(request: pytest.FixtureRequest, data_size_3d: int) -> NDArray:  # noqa: ARG001
    """Fixture to provide different types of data."""
    return request.getfixturevalue(request.param)


@pytest.fixture(
    params=EXISTING_PPFT2_REGRESSION_TEST_PAIRS,
    ids=lambda x: f"dim={x.dim}-data={x.matrix_type}-n={x.n}-func={x.function_name}",
)
def regression_test_2d(request: pytest.FixtureRequest) -> RegressionTestPair:
    """TODO."""
    return request.param


@pytest.fixture(
    params=EXISTING_PPFT3_REGRESSION_TEST_PAIRS,
    ids=lambda x: f"dim={x.dim}-data={x.matrix_type}-n={x.n}-func={x.function_name}",
)
def regression_test_3d(request: pytest.FixtureRequest) -> RegressionTestPair:
    """TODO."""
    return request.param


@pytest.fixture(
    params=USER_ENABLED_ARRAY_BACKENDS,
    ids=lambda x: ""
    if isinstance(x, NotSetType)
    else f"array_backend={x.name}-device={x.device}",
)
def array_backend(request: pytest.FixtureRequest) -> ArrayBackend:
    """TODO."""
    return request.param.instantiate()


@pytest.fixture(
    params=USER_ENABLED_SCIPY_BACKENDS,
    ids=lambda x: "-".join(
        ""
        if isinstance(x, NotSetType)
        else (
            f"scipy_backend={x.name}",
            f"array_backend={x.array_backend.name}",
            f"device={x.array_backend.device}",
        )
    ),
)
def scipy_backend(request: pytest.FixtureRequest) -> Generator[ScipyBackend]:
    """TODO."""
    yield request.param.instantiate()

    # pyFFTW saves plans for FFT computations called 'wisdom'.
    # With mkl_fft present, this leads to errors during runtime.
    # We therefore delete the state after each test run with pyFFTW.
    # See https://pyfftw.readthedocs.io/en/latest/source/pyfftw/pyfftw.html#wisdom-functions.
    if request.param.name == "pyfftw":
        import pyfftw

        pyfftw.forget_wisdom()


@pytest.fixture
def no_scipy() -> Generator:
    """Temporarily remove scipy and restore sys.modules after the test."""
    import ppftpy._utils as ppft_utils_module

    with mock.patch.dict(sys.modules, {"scipy": None}):
        yield

    importlib.reload(ppft_utils_module)
