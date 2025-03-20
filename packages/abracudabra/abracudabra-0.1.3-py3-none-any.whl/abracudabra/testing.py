"""Assertions for testing purposes.

These functions are used in the unitary tests. The equality checks assume no
floating-point errors.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._import import raise_library_not_found

if TYPE_CHECKING:
    from torch import Tensor

    from ._annotations import Array, DataFrame, Series


def assert_tensors_equal(tensor1: Tensor, tensor2: Tensor, /) -> None:
    """Assert that two Torch tensors are equal."""
    try:
        import torch
    except ImportError:  # pragma: no cover
        raise_library_not_found("torch")

    # Type
    for tensor in (tensor1, tensor2):
        if not isinstance(tensor, torch.Tensor):
            msg = f"Expected a Torch tensor, but got {type(tensor)!r}."
            raise TypeError(msg)

    # Device
    if tensor1.device != tensor2.device:
        msg = (
            "The two tensors are on different devices: "
            f"{tensor1.device} and {tensor2.device}."
        )
        raise AssertionError(msg)

    # dtype
    if tensor1.dtype != tensor2.dtype:
        msg = (
            "The two tensors have different data types: "
            f"{tensor1.dtype} and {tensor2.dtype}."
        )
        raise AssertionError(msg)

    # Values
    if not tensor1.equal(tensor2):
        msg = "The two tensors are not equal."
        raise AssertionError(msg)


def assert_arrays_equal(array1: Array, array2: Array, /) -> None:
    """Assert that two arrays are equal."""
    # Type
    if type(array1) is not type(array2):
        msg = (
            "Expected arrays of the same type, "
            f"but got {type(array1)!r} and {type(array2)!r}."
        )
        raise AssertionError(msg)

    # Shape
    if array1.shape != array2.shape:
        msg = (
            "Expected arrays of the same shape, "
            f"but got {array1.shape} and {array2.shape}."
        )
        raise AssertionError(msg)

    # dtype
    if array1.dtype != array2.dtype:
        msg = (
            "The two arrays have different data types: "
            f"{array1.dtype} and {array2.dtype}."
        )
        raise AssertionError(msg)

    # Values
    if not (array1 == array2).all():
        msg = "The two arrays are not equal."
        raise AssertionError(msg)


def assert_frames_equal(frame1: Series | DataFrame, frame2: Series | DataFrame) -> None:
    """Assert that two Pandas/cuDF series or dataframes are equal."""
    # Type
    if type(frame1) is not type(frame2):
        msg = (
            "Expected frames of the same type, "
            f"but got {type(frame1)!r} and {type(frame2)!r}."
        )
        raise AssertionError(msg)

    # dtypes
    dtypes_equal = frame1.dtypes == frame2.dtypes
    if not isinstance(dtypes_equal, bool):
        dtypes_equal = dtypes_equal.all()

    if not dtypes_equal:
        msg = "The two frames have different data types."
        raise AssertionError(msg)

    # Values
    if not frame1.equals(frame2):  # type: ignore[arg-type]
        msg = "The two frames are not equal."
        raise AssertionError(msg)
