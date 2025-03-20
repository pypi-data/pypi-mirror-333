"""Define the base device class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, NamedTuple, NoReturn, TypeGuard

if TYPE_CHECKING:
    from torch import device as torch_device

DeviceType = Literal["cpu", "cuda"]
"""The device type, e.g., ``"cpu"`` or ``"cuda"``."""

DEVICE_TYPES: frozenset[DeviceType] = frozenset(["cpu", "cuda"])
"""The supported device types."""


def _is_valid_device_type(device_type: str, /) -> TypeGuard[DeviceType]:
    """Check if a device name is valid."""
    return device_type in DEVICE_TYPES


def _raise_invalid_device_type(device_type: str, /) -> NoReturn:
    """Raise an error for an invalid device type."""
    msg = (
        f"Unsupported device type: {device_type!r}. Supported types are: "
        + ", ".join(map(repr, DEVICE_TYPES))
    )
    raise ValueError(msg)


class Device(NamedTuple):
    """A device with a name and index."""

    type: DeviceType
    """The device type, e.g., ``"cpu"`` or ``"cuda"``."""

    idx: int | None = None
    """The device index, e.g., ``0`` or ``None``."""

    def __str__(self) -> str:
        """Return the device name."""
        type_ = self.type
        return f"{type_}:{idx}" if (idx := self.idx) is not None else type_

    @staticmethod
    def _validate_type(device_type: object, /) -> DeviceType:
        """Validate a device type."""
        device_type = str(device_type)
        if not _is_valid_device_type(device_type):
            _raise_invalid_device_type(device_type)
        return device_type

    @staticmethod
    def _validate_idx(idx: object | None, /) -> int | None:
        """Validate a device index."""
        if idx is None:
            return None

        try:
            return int(idx)  # type: ignore[call-overload]
        except ValueError as e:
            msg = (
                "Expected an integer index or None, but got "
                f"{idx!r} of type {type(idx).__name__}."
            )
            raise TypeError(msg) from e

    @classmethod
    def validate(cls, device: object, idx: object | None = None) -> Device:
        """Return a device, validating the device type and index.

        Args:
            device: The device type.
            idx: The optional device index.

        Returns:
            The device.

        """
        device = cls._validate_type(device)
        idx = cls._validate_idx(idx)
        return cls(device, idx)

    @classmethod
    def from_str(cls, device: str, /) -> Device:
        """Return a device from a string.

        The string should be in the format ``"device[:idx]"``.

        Examples:
            >>> Device.from_str("cpu")
            Device(type="cpu", idx=None)
            >>> Device.from_str("cuda:1")
            Device(type="cuda", idx=1)

        """
        if ":" in device:
            name, idx = device.split(":", 1)

            return cls.validate(name, idx)
        return cls.validate(device)

    @classmethod
    def parse(cls, device: str | Device | torch_device, /) -> Device:
        """Return a device from a string or device.

        If the input is already a device, it is returned as is.
        Otherwise, the input is parsed as a string.

        Args:
            device: The device or device string (e.g., ``"cpu"`` or ``"cuda:1"``).

        Returns:
            The device.

        """
        if isinstance(device, cls):
            return device

        # This works with strings and torch.device objects
        return cls.from_str(str(device))

    def to_torch(self) -> torch_device:
        """Return a torch device.

        Examples:
            >>> Device("cpu", None).to_torch()
            device(type='cpu')
            >>> Device("cuda", 1).to_torch()
            device(type='cuda', index=1)

        """
        from torch import device as torch_device

        return torch_device(*self)  # type: ignore[arg-type]
