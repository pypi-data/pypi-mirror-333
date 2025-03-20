"""Type aliases for NumPy, CuPy, Pandas, and cuDF objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeAlias

if TYPE_CHECKING:
    import cudf
    import numpy.typing as npt
    import pandas as pd

    # NB: cupy typing not available
    Array: TypeAlias = npt.NDArray[Any] | Any
    """Type alias for NumPy/CuPy array."""

    Series: TypeAlias = pd.Series[Any] | cudf.Series
    """Type alias for Pandas/cuDF series."""

    DataFrame: TypeAlias = pd.DataFrame | cudf.DataFrame
    """Type alias for Pandas/cuDF dataframe."""

    Index: TypeAlias = pd.Index | cudf.Index
    """Type alias for Pandas/cuDF index."""

    __all__ = ["Array", "DataFrame", "Index", "Series"]
