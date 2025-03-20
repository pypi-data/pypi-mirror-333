"""Import utilities for Abracudabra."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from types import ModuleType


def import_library(library: str, /) -> ModuleType:
    """Import a library.

    Args:
        library: The name of the library to import.

    Raises:
        ImportError: If the library could not be found.

    """
    try:
        return import_module(library)
    except ImportError as e:
        raise_library_not_found(library, cause=e)


def raise_library_not_found(library: str, cause: Exception | None = None) -> NoReturn:
    """Raise an error for a missing library.

    Args:
        library: The name of the missing library.
        cause: The optional original exception.

    Raises:
        ImportError: Always.

    """
    msg = f"Library '{library}' could not be found."
    raise ImportError(msg) from cause


def get_library_name(obj: object, /) -> str:
    """Get the dependency of an object.

    Args:
        obj: The object to check.

    Returns:
        The dependency of the object.

    """
    return type(obj).__module__.split(".")[0]
