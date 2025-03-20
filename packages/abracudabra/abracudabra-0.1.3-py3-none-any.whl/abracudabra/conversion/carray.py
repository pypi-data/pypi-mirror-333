"""Convert to numpy or cupy arrays."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._import import get_library_name, raise_library_not_found
from .._validate import Library, validate_obj_type
from ..device.base import Device, _raise_invalid_device_type
from ..device.conversion import array_to_device, tensor_to_device, to_cupy_array
from ..device.query import _torch_get_device
from ._cdtype import from_torch_to_numpy_dtype

if TYPE_CHECKING:
    import cudf
    import pandas as pd
    from torch import Tensor

    from .._annotations import Array, DataFrame, Series


def _torch_to_array(tensor: Tensor, /, device: str | Device | None = None) -> Array:
    """Convert a Torch tensor to a numpy array."""
    # Get the device of the tensor and convert it to the desired device
    if device is not None:
        device = Device.parse(device)
        tensor = tensor_to_device(tensor, device)
    else:
        device = _torch_get_device(tensor)

    # Convert the tensor to the desired array
    match device.type:
        case "cpu":
            return tensor.numpy(force=True)
        case "cuda":
            try:
                import cupy as cp
            except ImportError:  # pragma: no cover
                raise_library_not_found("cupy")

            return cp.asarray(tensor, dtype=from_torch_to_numpy_dtype(tensor.dtype))
        case _:  # pragma: no cover
            # this should never happen, since the error is caught
            # by either `tensor_to_device` or `Device.parse`
            _raise_invalid_device_type(device.type)


def _array_to_array(array: Array, /, device: str | Device | None = None) -> Array:
    """Convert a NumPy/CuPy array to a NumPy/CuPy array.

    The array is converted to the desired device if specified.
    """
    if device is None:
        return array  # passthrough

    device = Device.parse(device)
    return array_to_device(array, device)


def _pandas_frame_to_array(
    frame: pd.Index | pd.Series[Any] | pd.DataFrame,
    /,
    device: str | Device | None = None,
) -> Array:
    numpy_array = frame.to_numpy()
    if device is None:
        return numpy_array

    return array_to_device(numpy_array, device)


def _cudf_frame_to_array(
    frame: cudf.Index | cudf.Series | cudf.DataFrame,
    /,
    device: str | Device | None = None,
) -> Array:
    """Convert a cuDF index, series or dataframe to a CuPy array."""
    if device is None:
        return frame.to_cupy()

    device = Device.parse(device)
    match device.type:
        case "cpu":
            return frame.to_numpy()
        case "cuda":
            try:
                import cupy as cp
            except ImportError:  # pragma: no cover
                raise_library_not_found("cupy")

            with cp.cuda.Device(device.idx):
                return frame.to_cupy()
        case _:
            _raise_invalid_device_type(device.type)


def _any_to_array(sequence: object, /, device: str | Device | None) -> Array:
    """Convert a sequence to a NumPy/CuPy array."""
    device = Device.parse(device) if device is not None else Device("cpu")

    match device.type:
        case "cpu":
            try:
                import numpy as np
            except ImportError:  # pragma: no cover
                raise_library_not_found("numpy")

            return np.asarray(sequence)
        case "cuda":
            return to_cupy_array(sequence, device.idx)
        case _:
            _raise_invalid_device_type(device.type)


def to_array(
    sequence: Array | Series | DataFrame | Tensor,
    /,
    device: str | Device | None = None,
    *,
    strict: bool = False,
) -> Array:
    """Convert an array, series, or dataframe to a NumPy or CuPy array.

    Args:
        sequence: The sequence to convert.
        device: The device to convert the sequence to. If None, the sequence stays
            on the same device.
        strict: Whether to raise an error if the sequence is not a valid type.
            A NumPy/CuPy array, Pandas/cuDF series or dataframe, or Torch tensor
            are valid types.
            If False, the sequence is converted to a NumPy/CuPy array if possible,
            but it might raise an error if the conversion is not possible.

    Returns:
        A NumPy/CuPy array.

    Raises:
        TypeError: If the sequence is not a valid type and ``strict`` is True.

    Examples:
        Build a CuPy array from a sequence

        >>> import cupy as cp
        >>> cupy_array = to_array([1, 2, 3], "cuda:0")
        >>> print(type(cupy_array))
        <class 'cupy.ndarray'>

        Build a NumPy array from a cuDF series

        >>> import cudf
        >>> cudf_series = cudf.Series([1, 2, 3])
        >>> numpy_array = to_array(cudf_series)
        >>> print(type(numpy_array))
        <class 'numpy.ndarray'>

    """
    library = get_library_name(sequence)
    device = Device.parse(device) if device is not None else None

    if (library == "numpy" and validate_obj_type(sequence, Library.numpy)) or (
        library == "cupy" and validate_obj_type(sequence, Library.cupy)
    ):
        return _array_to_array(sequence, device)
    elif library == "pandas" and validate_obj_type(sequence, Library.pandas):
        return _pandas_frame_to_array(sequence, device)
    elif library == "cudf" and validate_obj_type(sequence, Library.cudf):
        return _cudf_frame_to_array(sequence, device)
    elif library == "torch" and validate_obj_type(sequence, Library.torch):
        return _torch_to_array(sequence, device)

    if strict:
        msg = (
            "Expected a NumPy/CuPy array, Pandas/cuDF series or dataframe, "
            f"or Torch tensor, but got '{type(sequence)!r}'."
        )
        raise TypeError(msg)

    # hope for the best
    return _any_to_array(sequence, device)
