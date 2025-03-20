"""Library import functions for device types.

This module provides functions to import the appropriate library based on the
device type.
Since the NumPy/CuPy and Pandas/cuDF libraries share similar interfaces,
being able to switch between them based on the device type is useful.
"""

from types import ModuleType

from .._import import import_library
from .base import DeviceType

_DEVICE_TO_LIBRARY: dict[str, dict[DeviceType, str]] = {
    "array": {"cpu": "numpy", "cuda": "cupy"},
    "frame": {"cpu": "pandas", "cuda": "cudf"},
}
"""A collection of mappings from device types to library names."""

_DEFAULT_DEVICE_TYPE: DeviceType = "cpu"
"""The default device type, if the device type is not specified."""


def _import_library(obj_name: str, device_type: DeviceType | None = None) -> ModuleType:
    """Import the library for the given object and device type."""
    if device_type is None:
        device_type = _DEFAULT_DEVICE_TYPE
    library_name = _DEVICE_TO_LIBRARY[obj_name][device_type]
    return import_library(library_name)


def get_np_or_cp(device_type: DeviceType | None = None) -> ModuleType:
    """Get the numpy or cupy library based on the device type.

    * if ``device_type`` is ``"cpu"``, return the numpy library
    * if ``device_type`` is ``"cuda"``, return the cupy library

    If ``device_type`` is not specified, return the numpy library (default).

    Examples:
        >>> device_type = "cuda"  # in some configuration for example
        >>> np_or_cp = get_np_or_cp(device_type)
        >>> np_or_cp.random.choice([1, 2, 3], size=1)  # returns a cupy array
        array([3])

    """
    return _import_library("array", device_type)


def get_pd_or_cudf(device_type: DeviceType | None = None) -> ModuleType:
    """Get the pandas or cudf library based on the device type.

    * if ``device_type`` is ``"cpu"``, return the pandas library
    * if ``device_type`` is ``"cuda"``, return the cudf library

    If ``device_type`` is not specified, return the pandas library (default).

    Examples:
        >>> pd_or_cudf = get_pd_or_cudf("cpu")
        >>> pd_or_cudf.Series([1, 2, 3])  # returns a pandas series
        0    1
        1    2
        2    3
        dtype: int64

    """
    return _import_library("frame", device_type)
