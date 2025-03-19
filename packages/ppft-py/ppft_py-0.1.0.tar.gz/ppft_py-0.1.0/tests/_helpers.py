"""TODO."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Protocol

import numpy as np
import pytest
from array_api_compat import is_cupy_array
from lark import Lark, Token, Transformer
from scipy import fft
from scipy.fft._backend import _named_backends as known_scipy_backends
from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import ModuleType

    from numpy.typing import NDArray


BACKEND_SELECTION_GRAMMAR: Final = r"""
    start: backend_list
    backend_list: backend (";" backend)*
    backend: NAME (":" device_list)?
    device_list: DEVICE ("," DEVICE)*

    NAME: /[a-zA-Z0-9_]+/
    DEVICE: /[a-zA-Z0-9_]+/

    %import common.WS
    %ignore WS
"""


class BackendSelectionTransformer(Transformer):
    """TODO."""

    def start(self, items: list[dict[str, list[str]]]) -> dict[str, list[str]]:
        """Ensure the root node returns only the dictionary."""
        return items[0]

    def backend_list(self, items: list[tuple[str, list[str]]]) -> dict[str, list[str]]:
        return dict(items)

    def device_list(self, items: list[str]) -> list[str]:
        return list(items)

    def backend(self, items: list[str]) -> tuple[str, list[str]]:
        name = items[0]
        devices = items[1:] if len(items) > 1 else []
        devices = devices[0] if devices and isinstance(devices[0], list) else devices
        return name, devices

    def name(self, token: Token) -> str:
        return str(token)

    def device(self, token: Token) -> str:
        return str(token)


@dataclass(frozen=True, slots=True, kw_only=True)
class ArrayBackendParseResult:
    """TODO."""

    name: str
    clazz: type[ArrayBackend]
    device: str

    def instantiate(self) -> Backend:
        """TODO."""
        return self.clazz(self.device)


@dataclass(frozen=True, slots=True, kw_only=True)
class ScipyBackendParseResult:
    """TODO."""

    name: str
    clazz: type[ScipyBackend]
    array_backend: ArrayBackendParseResult

    def instantiate(self) -> ScipyBackend:
        """TODO."""
        return self.clazz(self.array_backend.instantiate())


def __enabled_scipy_backends(
    scipy_test_backends: str, array_test_backends: str
) -> list[ScipyBackendParseResult]:
    selected_array_backends = __enabled_array_backends(array_test_backends)
    if not selected_array_backends:
        return []

    scipy_test_backends = scipy_test_backends.strip().lower()
    if not scipy_test_backends:
        return []

    selected_scipy_backends = SCIPY_BACKENDS.keys()
    if scipy_test_backends != "all":
        parser = Lark(BACKEND_SELECTION_GRAMMAR, parser="lalr")
        transformer = BackendSelectionTransformer()
        parsed_backends = transformer.transform(parser.parse(scipy_test_backends))
        selected_scipy_backends &= parsed_backends

    enabled_backend_combinations = []
    for scipy_backend in selected_scipy_backends:
        supported_array_backends = __enabled_array_backends(
            ";".join(SCIPY_BACKENDS[scipy_backend]["array_backends"])
        )
        enabled_array_backends = set(selected_array_backends) & set(
            supported_array_backends
        )

        enabled_backend_combinations.extend(
            ScipyBackendParseResult(
                name=scipy_backend,
                clazz=SCIPY_BACKENDS[scipy_backend]["class"],
                array_backend=array_backend,
            )
            for array_backend in enabled_array_backends
        )

    return enabled_backend_combinations


def __enabled_array_backends(test_backends: str) -> list[ArrayBackendParseResult]:
    test_backends = test_backends.strip().lower()

    if not test_backends:
        return []

    selected_backends = ARRAY_BACKENDS.keys()
    if test_backends == "all":
        parsed_backends = None
    else:
        parser = Lark(BACKEND_SELECTION_GRAMMAR, parser="lalr")
        transformer = BackendSelectionTransformer()
        parsed_backends = transformer.transform(parser.parse(test_backends))
        selected_backends &= parsed_backends

    enabled_backends = []
    for backend in selected_backends:
        supported_devices = ARRAY_BACKENDS[backend]["devices"]
        selected_devices = set(parsed_backends[backend]) if parsed_backends else None
        enabled_devices = (
            supported_devices & selected_devices
            if selected_devices
            else supported_devices
        )

        enabled_backends.extend(
            ArrayBackendParseResult(
                name=backend, clazz=ARRAY_BACKENDS[backend]["class"], device=device
            )
            for device in enabled_devices
        )

    return enabled_backends


class Backend(Protocol):
    """TODO."""

    @property
    def rtol(self) -> float:
        """TODO."""
        return 1e-15

    @property
    def atol(self) -> float:
        """TODO."""
        return 0.0

    def compute(self, data: NDArray, func: Callable, **kwargs: Any) -> NDArray:
        """TODO."""
        ...


class ArrayBackend(Backend):
    """TODO."""

    _NAMESPACE: str
    _MIN_VERSION: str | None = None
    _RTOL: float | None = None
    _ATOL: float | None = None

    def __init__(self, device: str) -> None:
        self._namespace: ModuleType = pytest.importorskip(
            self._NAMESPACE, minversion=self._MIN_VERSION
        )
        self._device: str = device

    @property
    @override
    def rtol(self) -> float:
        return self._RTOL if self._RTOL is not None else super().rtol

    @property
    @override
    def atol(self) -> float:
        return self._ATOL if self._ATOL is not None else super().atol

    @property
    def _namespace_kwargs(self) -> dict[str, Any]:
        return {}

    @override
    def compute(self, data: NDArray, func: Callable, **kwargs: Any) -> NDArray:
        return self._to_numpy(func(self._to_namespace(data), **kwargs))

    def _to_namespace(self, data: NDArray) -> NDArray:
        return self._namespace.asarray(data, **self._namespace_kwargs)

    def _to_numpy(self, data: NDArray) -> NDArray:
        return data


class NumpyArrayBackend(ArrayBackend):
    """TODO."""

    _NAMESPACE = "numpy"
    _RTOL = 1e-11


class CupyArrayBackend(ArrayBackend):
    """TODO."""

    _NAMESPACE = "cupy"
    _RTOL = 1e-11

    @override
    def _to_numpy(self, data: NDArray) -> NDArray:
        return data.get()


class DpnpArrayBackend(ArrayBackend):
    """TODO."""

    _NAMESPACE = "dpnp"
    _MIN_VERSION = "0.17.0"

    @property
    @override
    def _namespace_kwargs(self) -> dict[str, Any]:
        import dpctl

        if self._device not in ("cpu", "gpu"):
            pytest.skip(f"Unknown dpnp device '{self._device}'")

        if not getattr(dpctl, f"has_{self._device}_devices")():
            pytest.skip(f"dpnp device '{self._device}' is not available")

        return {"device": getattr(dpctl, f"select_{self._device}_device")()}


class DaskArrayBackend(ArrayBackend):
    """TODO."""

    _NAMESPACE = "dask.array"
    _ATOL = 1e-10

    __DEVICE_BACKEND_MAPPING: Final = {"cpu": "numpy", "gpu": "cupy"}

    @property
    @override
    def _namespace_kwargs(self) -> dict[str, Any]:
        if self._device not in self.__DEVICE_BACKEND_MAPPING:
            pytest.skip(f"Unknown Dask device '{self._device}'")

        internal_backend = self.__DEVICE_BACKEND_MAPPING[self._device]

        return {"like": pytest.importorskip(internal_backend).array(())}

    @override
    def _to_numpy(self, data: NDArray) -> NDArray:
        out_data = data.compute()

        return out_data.get() if is_cupy_array(out_data) else out_data


class JaxArrayBackend(ArrayBackend):
    """TODO."""

    _NAMESPACE = "jax.numpy"
    _RTOL = 1e-11

    @property
    @override
    def _namespace_kwargs(self) -> dict[str, Any]:
        jax = pytest.importorskip("jax")
        jax_extend = pytest.importorskip("jax.extend")

        if self._device not in jax_extend.backend.backends():
            pytest.skip(f"JAX device backend '{self._device}' is not available")

        devices = jax.devices(self._device)
        if not devices:
            pytest.skip(f"No devices for JAX device backend '{self._device}' available")

        return {"device": devices[0]}


class TorchArrayBackend(ArrayBackend):
    """TODO."""

    _NAMESPACE = "torch"
    _RTOL = 1e-11

    def __init__(self, device: str) -> None:
        super().__init__(device)

        # Setting float precision to 'float64' allows PyTorch to return
        # results with 'complex128' dtype (instead of 'complex64' for
        # default 'float32'). This is set to make the actual precision
        # more comparable to other backends and to allow higher
        # precision on regression tests.
        torch = pytest.importorskip("torch")
        torch.set_default_dtype(torch.float64)

    @property
    @override
    def _namespace_kwargs(self) -> dict[str, Any]:
        try:
            torch_device = getattr(self._namespace, self._device)
        except AttributeError:
            pytest.skip(f"PyTorch device '{self._device}' cannot be accessed")

        if not torch_device.is_available():
            pytest.skip(f"PyTorch device '{self._device}' is not available")

        if not torch_device.device_count():
            pytest.skip(f"No devices for PyTorch device '{self._device}' available")

        return {"device": self._device}

    @override
    def _to_numpy(self, data: NDArray) -> NDArray:
        return data.cpu()


class ScipyBackend(Backend):
    """TODO."""

    _MODULE: str
    _MIN_VERSION: str | None = None

    def __init__(self, array_backend: Backend) -> None:
        self._fft_backend: ModuleType | str = (
            self._MODULE
            if self._MODULE in known_scipy_backends
            else pytest.importorskip(self._MODULE, minversion=self._MIN_VERSION)
        )
        self._array_backend: Backend = array_backend

    @property
    @override
    def rtol(self) -> float:
        """TODO."""
        return self._array_backend.rtol

    @property
    @override
    def atol(self) -> float:
        """TODO."""
        return self._array_backend.atol

    @override
    def compute(self, data: NDArray, func: Callable, **kwargs: Any) -> NDArray:
        """TODO."""
        with fft.set_backend(self._fft_backend):
            return self._array_backend.compute(data, func, scipy_fft=True, **kwargs)


class ScipyScipyBackend(ScipyBackend):
    """TODO."""

    _MODULE = "scipy"


class MklScipyBackend(ScipyBackend):
    """TODO."""

    _MODULE = "mkl_fft._scipy_fft_backend"


class PyfftwScipyBackend(ScipyBackend):
    """TODO."""

    _MODULE = "pyfftw.interfaces.scipy_fft"


class CupyScipyBackend(ScipyBackend):
    """TODO."""

    _MODULE = "cupyx.scipy.fft"


@dataclass(frozen=True, slots=True, kw_only=True)
class RegressionTestPair:
    """TODO."""

    n: int
    dim: int
    matrix_type: str
    function_name: str
    in_path: Path
    out_path: Path

    @property
    def in_data(self) -> NDArray:
        return np.load(self.in_path)

    @property
    def out_data(self) -> NDArray:
        return np.load(self.out_path)


def __get_all_test_file_pairs(
    test_dir: Path, *, extension: str = "npy"
) -> list[RegressionTestPair]:
    # In file format: '{dim}d_{matrix-type}_{n}_in.{extension}'
    input_files = test_dir.glob(f"*_in.{extension}")

    test_pairs = []
    for in_path in input_files:
        file_id = str(in_path.stem.removesuffix("_in"))
        filename_split = file_id.split("_")
        dim = int(filename_split[0][0])
        matrix_type = filename_split[1]
        n = int(filename_split[2])

        test_pairs.extend(
            RegressionTestPair(
                n=n,
                dim=dim,
                matrix_type=matrix_type,
                function_name=out_path.stem.split("_out_")[1],
                in_path=in_path,
                out_path=out_path,
            )
            for out_path in test_dir.glob(f"{file_id}_out_*.{extension}")
        )

    return test_pairs


DEVICES_NUMPY: Final = {"cpu"}
DEVICES_CUPY: Final = {"gpu"}
DEVICES_DPNP: Final = {"cpu", "gpu"}
DEVICES_DASK: Final = {"cpu", "gpu"}
DEVICES_JAX: Final = {"cpu", "tpu", "cuda", "rocm"}
DEVICES_TORCH: Final = {
    # Source: https://pytorch.org/docs/stable/backends.html
    "cpu",
    "cuda",
    "cudnn",
    "cusparselt",
    "mha",
    "mps",
    "mkl",
    "mkldnn",
    "nnpack",
    "openmp",
    "opt_einsum",
    "xeon",
}

ARRAY_BACKENDS: Final[dict[str, dict[str, Any]]] = {
    "numpy": {"class": NumpyArrayBackend, "devices": DEVICES_NUMPY},
    "cupy": {"class": CupyArrayBackend, "devices": DEVICES_CUPY},
    "dpnp": {"class": DpnpArrayBackend, "devices": DEVICES_DPNP},
    "dask": {"class": DaskArrayBackend, "devices": DEVICES_DASK},
    "jax": {"class": JaxArrayBackend, "devices": DEVICES_JAX},
    "torch": {"class": TorchArrayBackend, "devices": DEVICES_TORCH},
}

ARRAY_BACKENDS_NUMPY = {"numpy", "jax:cpu", "dask:cpu"}
ARRAY_BACKENDS_CUPY = {"cupy"}

SCIPY_BACKENDS: Final[dict[str, dict[str, Any]]] = {
    "scipy": {"class": ScipyScipyBackend, "array_backends": ARRAY_BACKENDS_NUMPY},
    "mkl": {"class": MklScipyBackend, "array_backends": ARRAY_BACKENDS_NUMPY},
    "pyfftw": {"class": PyfftwScipyBackend, "array_backends": ARRAY_BACKENDS_NUMPY},
    "cupy": {"class": CupyScipyBackend, "array_backends": ARRAY_BACKENDS_CUPY},
}

USER_ENABLED_ARRAY_BACKENDS: Final = __enabled_array_backends(
    os.getenv("TEST_BACKENDS_ARRAY", "")
)

USER_ENABLED_SCIPY_BACKENDS: Final = __enabled_scipy_backends(
    os.getenv("TEST_BACKENDS_SCIPY", ""), os.getenv("TEST_BACKENDS_ARRAY", "")
)

EXISTING_PPFT3_REGRESSION_TEST_PAIRS = __get_all_test_file_pairs(
    Path("tests/test_data/ppft3")
)
EXISTING_PPFT2_REGRESSION_TEST_PAIRS = __get_all_test_file_pairs(
    Path("tests/test_data/ppft2")
)
