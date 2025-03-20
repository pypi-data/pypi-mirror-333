"""Convert data types between NumPy and Torch.

Note that NumPy and CuPy dtypes are the same.
"""

from __future__ import annotations

import warnings
from collections.abc import Iterable
from functools import lru_cache
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import numpy as np
    import torch as t

    from .._annotations import DataFrame, Index, Series


@lru_cache
def _get_numpy_to_torch_dtype_dict() -> dict[np.dtype[Any], t.dtype]:
    """Get the dictionary mapping NumPy dtypes to Torch dtypes."""
    import numpy as np
    import torch as t

    return {
        np.dtype("bool"): t.bool,
        np.dtype("uint8"): t.uint8,
        np.dtype("uint16"): t.uint16,
        np.dtype("uint32"): t.uint32,
        np.dtype("uint64"): t.uint64,
        np.dtype("int8"): t.int8,
        np.dtype("int16"): t.int16,
        np.dtype("int32"): t.int32,
        np.dtype("int64"): t.int64,
        np.dtype("float16"): t.float16,
        np.dtype("float32"): t.float32,
        np.dtype("float64"): t.float64,
        np.dtype("complex64"): t.complex64,
        np.dtype("complex128"): t.complex128,
    }


@lru_cache
def _get_torch_to_numpy_dtype_dict() -> dict[t.dtype, Any]:
    """Get the dictionary mapping Torch dtypes to NumPy dtypes."""
    numpy_to_torch_dtype_dict = _get_numpy_to_torch_dtype_dict()
    return {v: k for k, v in numpy_to_torch_dtype_dict.items()}


def from_torch_to_numpy_dtype(torch_dtype: t.dtype, /) -> np.dtype | None:
    """Convert a Torch dtype to a NumPy dtype.

    Args:
        torch_dtype: The Torch dtype to convert.

    Returns:
        The NumPy dtype equivalent of the Torch dtype.

    Warns:
        If the Torch dtype does not have a NumPy equivalent.

    """
    torch_to_numpy_dtype = _get_torch_to_numpy_dtype_dict()
    numpy_dtype = torch_to_numpy_dtype.get(torch_dtype)

    if numpy_dtype is None:
        warnings.warn(
            f"Torch dtype '{torch_dtype}' does not have a NumPy equivalent. ",
            stacklevel=2,
        )

    return numpy_dtype


def from_numpy_to_torch_dtype(numpy_dtype: np.dtype, /) -> t.dtype | None:
    """Convert a NumPy dtype to a Torch dtype.

    Args:
        numpy_dtype: The NumPy dtype to convert.

    Returns:
        The Torch dtype equivalent of the NumPy dtype.

    Warns:
        If the NumPy dtype does not have a Torch equivalent.

    """
    torch_to_numpy_dtype_dict = _get_numpy_to_torch_dtype_dict()

    torch_dtype = torch_to_numpy_dtype_dict.get(numpy_dtype)

    if torch_dtype is None:
        warnings.warn(
            f"NumPy dtype '{numpy_dtype}' does not have a Torch equivalent. ",
            stacklevel=2,
        )

    return torch_dtype


def get_frame_result_dtype(frame: Index | Series | DataFrame) -> np.dtype[Any]:
    """Get the dtype of a Pandas/cuDF frame."""
    # Try to get `dtypes` attribute: shound work for series and dataframes
    dtypes = getattr(frame, "dtypes", None)
    # if it does not exist, try to get the `dtype`: should work for indexes
    if dtypes is None:
        dtypes = getattr(frame, "dtype", None)

    if isinstance(dtypes, Iterable):
        from numpy import result_type

        return result_type(*dtypes)
    else:
        return dtypes  # type: ignore[return-value]
