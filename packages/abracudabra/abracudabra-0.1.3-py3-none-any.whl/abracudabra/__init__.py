"""Convert dataframes, arrays, and tensors to CPU/CUDA."""

from importlib.metadata import version as _importlib_version

from .conversion.carray import to_array
from .conversion.cframe import to_dataframe, to_series
from .conversion.ctensor import to_tensor
from .device.base import Device
from .device.conversion import to_device
from .device.library import get_np_or_cp, get_pd_or_cudf
from .device.query import get_device

__all__ = [
    "Device",
    "get_device",
    "get_np_or_cp",
    "get_pd_or_cudf",
    "to_array",
    "to_dataframe",
    "to_device",
    "to_series",
    "to_tensor",
]


__version__ = _importlib_version(__name__)
