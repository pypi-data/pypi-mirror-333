"""Query the device of a NumPy/CuPy array, series or Torch tensor."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, overload

from .._import import get_library_name
from .._validate import Library, validate_obj_type
from .base import Device, DeviceType

if TYPE_CHECKING:
    from torch import Tensor

    from .._annotations import Array, DataFrame, Series


def _cupy_get_device(array: object, /) -> Device:
    """Get the device of a cupy array.

    Args:
        array: The array to check.

    Returns:
        The device of the array.

    """
    return Device("cuda", array.device.id)  # type: ignore[attr-defined]


@overload
def frame_get_device_type(
    frame: Series | DataFrame, /, *, raise_if_unknown: Literal[True] = ...
) -> DeviceType: ...


@overload
def frame_get_device_type(
    frame: Series | DataFrame, /, *, raise_if_unknown: bool = ...
) -> DeviceType | None: ...


def frame_get_device_type(
    frame: Series | DataFrame, /, *, raise_if_unknown: bool = True
) -> DeviceType | None:
    """Get the device type of a pandas or cudf series or dataframe.

    Args:
        frame: The frame to check.
        raise_if_unknown: Whether to raise an error if the frame is not
            a series or dataframe.

    Returns:
        The device type of the frame.
        If  ``raise_if_unknown`` is ``False`` and the frame is not a series or
        dataframe, return ``None``.

    Raises:
        TypeError: If the frame is not a series or dataframe and
            ``raise_if_unknown`` is ``True``.

    """
    library = get_library_name(frame)

    if library == "pandas" and validate_obj_type(frame, Library.pandas):
        return "cpu"

    if library == "cudf" and validate_obj_type(frame, Library.cudf):
        return "cuda"

    if raise_if_unknown:
        msg = (
            "Expected a Pandas/cuDF index, series or dataframe, "
            f"but got '{type(frame).__name__}'."
        )
        raise TypeError(msg)

    return None


def _torch_get_device(tensor: Tensor, /) -> Device:
    """Get the device of a Torch tensor.

    Args:
        tensor: The tensor to check.

    Returns:
        The device of the tensor.

    """
    device = tensor.device
    return Device.validate(device.type, device.index)


@overload
def get_device(
    element: Array | Tensor, /, *, raise_if_unknown: Literal[True] = ...
) -> Device: ...


@overload
def get_device(
    element: Array | Tensor, /, *, raise_if_unknown: bool = ...
) -> Device | None: ...


def get_device(
    element: Array | Tensor, /, *, raise_if_unknown: bool = True
) -> Device | None:
    """Get the device of a NumPy/CuPy array or series.

    Args:
        element: The element to check.
        raise_if_unknown: Whether to raise an error if the element is not a known
            array or tensor.

    Returns:
        The device of the element.

    Examples:
        >>> import numpy as np
        >>> array = np.random.rand(3)
        >>> get_device(array)
        Device(type="cpu", idx=None)
        >>> import torch
        >>> tensor = torch.rand(3, device="cuda")
        >>> get_device(tensor)
        Device(type="cuda", idx=0)

    """
    library = get_library_name(element)

    if library == "numpy" and validate_obj_type(element, Library.numpy):
        return Device("cpu")

    if library == "cupy" and validate_obj_type(element, Library.cupy):
        return _cupy_get_device(element)

    if library == "torch" and validate_obj_type(element, Library.torch):
        return _torch_get_device(element)

    if raise_if_unknown:
        msg = (
            "Expected a NumPy/CuPy array or torch array or tensor, "
            f"but got '{type(element).__name__}'."
        )
        raise TypeError(msg)

    return None


def guess_device(*elements: Array | Tensor, skip_unknown: bool = True) -> Device:
    """Guess the device of a sequence of arrays or tensors.

    This function checks the device of the elements and returns the device if all
    elements are on the same device.
    Otherwise, it raises an error.

    Args:
        *elements: The elements to check.
        skip_unknown: Whether to skip elements that are not known arrays or tensors
            (e.g., lists, tuples, etc.).

    Returns:
        The device of the elements.

    Raises:
        ValueError: If no elements are given.
        ValueError: If the device cannot be inferred from any of the elements
            (if ``skip_unknown`` is ``True``).
        ValueError: If the elements are on different devices.

    """
    if not elements:
        msg = "Expected at least one element, but got none."
        raise ValueError(msg)

    devices = {
        device
        for element in elements
        if (device := get_device(element, raise_if_unknown=not skip_unknown))
        is not None
    }

    if len(devices) == 0:
        msg = "Could not infer the device from any of the elements."
        raise ValueError(msg)

    if len(devices) > 1:
        msg = (
            f"Expected all elements to be on the same device, "
            f"but found {len(devices)} different devices:"
            + ", ".join(map(repr, devices))
        )
        raise ValueError(msg)

    return devices.pop()
