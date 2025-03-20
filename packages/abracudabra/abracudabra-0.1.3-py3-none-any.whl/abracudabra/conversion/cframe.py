"""Convert to a Pandas/cuDF series or dataframe."""

from __future__ import annotations

import contextlib
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from ..device.base import Device
from ..device.conversion import to_device
from ..device.library import get_pd_or_cudf
from ..device.query import guess_device
from .carray import to_array

if TYPE_CHECKING:
    from collections.abc import Iterable

    from torch import Tensor

    from .._annotations import Array, DataFrame, Series


def _guess_dataframe_device(
    sequences: Iterable[Tensor | Array],
    /,
    device: str | Device | None = None,
) -> Device:
    """Guess the device of a dataframe."""
    if device is not None:
        return Device.parse(device)

    return guess_device(*sequences, skip_unknown=True)


def to_series(
    sequence: object,
    /,
    index: Array | Tensor | None = None,
    device: str | Device | None = None,
    *,
    strict: bool = False,
    **kwargs: Any,
) -> Series:
    r"""Convert an array or tensor to a Pandas/cuDF series.

    Args:
        sequence: The array or tensor to convert.
        index: The optional index for the series.
        device: The device to use for the series. If not provided, the array stays
            on the same device.
        strict: Whether to raise an error if the sequence is not
            a NumPy/CuPy array or Torch tensor.
        **kwargs: Additional keyword arguments for the series.

    Returns:
        The converted series.

    Examples:
        Convert a list to a CuPy series

        >>> series = to_series([10, 20, 30], device="cuda")
        >>> print(type(series))
        <class 'cudf.core.series.Series'>

        Convert a CuPy array to a cuDF series

        >>> import cupy as cp
        >>> cupy_array = cp.array([40, 50, 60])
        >>> series = to_series(cupy_array)
        >>> print(type(series))
        <class 'cudf.core.series.Series'>

    """
    device = _guess_dataframe_device([sequence], device=device)
    array = to_array(sequence, device=device, strict=strict)

    if index is not None:
        # Try to move the index to the same device as the array
        # If it fails, just pass it as is, and let Pandas/cuDF handle it
        with contextlib.suppress(TypeError):
            index = to_device(index, device=device)

    pdf_or_cudf = get_pd_or_cudf(device.type)
    return pdf_or_cudf.Series(array, index=index, **kwargs)  # type: ignore[arg-type]


def to_dataframe(
    data: Mapping[str, Array | Tensor] | Tensor | Array,
    /,
    index: Array | Tensor | None = None,
    device: str | Device | None = None,
    *,
    strict: bool = False,
    **kwargs: Any,
) -> DataFrame:
    r"""Convert to a Pandas/cuDF dataframe.

    Args:
        data: The data to convert. If a mapping, the keys will be used as column names.
        index: The optional index for the dataframe.
        device: The device to use for the dataframe. If not provided,
            the type is guessed from the data.
        strict: Whether to raise an error if the provided data does not consist of
            NumPy/CuPy arrays or Torch tensors.
        **kwargs: Additional keyword arguments for the dataframe.

    Returns:
        The converted dataframe.

    Examples:
        Build a dataframe from mixed data types

        >>> import cupy as cp
        >>> import numpy as np
        >>> import torch

        >>> numpy_array = np.full((5,), 1, dtype=np.float32)
        >>> cupy_array = cp.full((5,), 2, dtype=cp.int8)
        >>> torch_tensor = torch.full((5,), 3, dtype=torch.float32, device="cuda:0")
        >>> dataframe = to_dataframe(
        ...     {"numpy": numpy_array, "cupy": cupy_array, "torch": torch_tensor},
        ...     device="cuda:0",
        ... )
        >>> print(dataframe)
        numpy  cupy  torch
        0    1.0     2    3.0
        1    1.0     2    3.0
        2    1.0     2    3.0
        3    1.0     2    3.0
        4    1.0     2    3.0
        >>> print(type(dataframe))
        <class 'cudf.core.dataframe.DataFrame'>

    """
    device = _guess_dataframe_device(
        data.values() if isinstance(data, Mapping) else [data],
        device=device,
    )

    if isinstance(data, Mapping):
        data = {
            key: to_array(value, device=device, strict=strict)
            for key, value in data.items()
        }
    else:
        data = to_array(data, device=device, strict=strict)

    if index is not None:
        with contextlib.suppress(TypeError):
            index = to_device(index, device=device)

    df_or_cudf = get_pd_or_cudf(device.type)
    return df_or_cudf.DataFrame(data, index=index, **kwargs)
