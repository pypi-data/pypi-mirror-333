from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Literal, TypeGuard, overload

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Mapping

    import cudf
    import numpy as np
    import pandas as pd
    from torch import Tensor


def _get_numpy_type() -> dict[str, type]:
    import numpy as np

    return {"array": np.ndarray}


def _get_cupy_type() -> dict[str, type]:
    import cupy as cp

    return {"array": cp.ndarray}


def _get_torch_type() -> dict[str, type]:
    import torch

    return {"tensor": torch.Tensor}


def _get_pandas_type() -> dict[str, type]:
    import pandas as pd

    return {"series": pd.Series, "dataframe": pd.DataFrame, "index": pd.Index}


def _get_cudf_type() -> dict[str, type]:
    import cudf

    return {"series": cudf.Series, "dataframe": cudf.DataFrame, "index": cudf.Index}


class Library(Enum):
    """Library names."""

    numpy = "numpy"
    cupy = "cupy"
    torch = "torch"
    pandas = "pandas"
    cudf = "cudf"


LIBRARY_TO_CONCRETE_TYPES: dict[Library, Callable[[], Mapping[str, type]]] = {
    Library.numpy: _get_numpy_type,
    Library.cupy: _get_cupy_type,
    Library.torch: _get_torch_type,
    Library.pandas: _get_pandas_type,
    Library.cudf: _get_cudf_type,
}
"""Mapping from library names to functions that return a mapping of concrete types."""


def _get_concrete_types(
    library: Library, types: str | Iterable[str] | None = None
) -> type | tuple[type, ...]:
    get_types = LIBRARY_TO_CONCRETE_TYPES[library]

    concrete_types = get_types()
    if types is None:
        return tuple(concrete_types.values())
    elif isinstance(types, str):
        return concrete_types[types]
    else:
        return tuple(concrete_types[t] for t in types)


@overload
def validate_obj_type(
    obj: object,
    /,
    library: Literal[Library.numpy],
    types: str | Iterable[str] | None = ...,
) -> TypeGuard[np.ndarray]: ...


@overload
def validate_obj_type(
    obj: object,
    /,
    library: Literal[Library.cupy],
    types: str | Iterable[str] | None = ...,
) -> TypeGuard[Any]: ...


@overload
def validate_obj_type(
    obj: object,
    /,
    library: Literal[Library.torch],
    types: str | Iterable[str] | None = ...,
) -> TypeGuard[Tensor]: ...


@overload
def validate_obj_type(
    obj: object,
    /,
    library: Literal[Library.pandas],
    types: str | Iterable[str] | None = ...,
) -> TypeGuard[pd.Index | pd.Series[Any] | pd.DataFrame]: ...


@overload
def validate_obj_type(
    obj: object,
    /,
    library: Literal[Library.cudf],
    types: str | Iterable[str] | None = ...,
) -> TypeGuard[cudf.Index | cudf.Series | cudf.DataFrame]: ...


@overload
def validate_obj_type(
    obj: object, /, library: Library, types: str | Iterable[str] | None = ...
) -> bool: ...


def validate_obj_type(
    obj: object, /, library: Library, types: str | Iterable[str] | None = None
) -> bool:
    """Validate an object ensuring it matches the type from a specified library.

    Args:
        obj: The object to validate.
        library: Library name from Enum 'Library'.
        types: The type(s) to validate against.
            For example, ``'array'``, ``'index'``, ``'series'``,
            ``'dataframe'``, ``'tensor'``.

    Returns:
        The input object, if validation succeeds.

    Raises:
        ValueError: If an unsupported library is provided.
        TypeError: If the object type doesn't match the expected type.

    """
    concrete_types = _get_concrete_types(library, types)
    return isinstance(obj, concrete_types)
