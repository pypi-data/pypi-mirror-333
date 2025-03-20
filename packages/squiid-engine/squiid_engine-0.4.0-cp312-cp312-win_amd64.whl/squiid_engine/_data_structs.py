from __future__ import annotations

from ctypes import Structure, c_bool, c_char_p, c_int
from dataclasses import dataclass
from enum import IntEnum
from typing import final


class BucketTypes(IntEnum):
    """An enum defining types of data stored in a Bucket.

    Attributes:
        FLOAT: A floating point value
        STRING: A string value
        CONSTANT: A constant value. See ConstantTypes
        UNDEFINED: An undefined value
    """

    FLOAT = 1
    STRING = 2
    CONSTANT = 3
    UNDEFINED = 4


class ConstantTypes(IntEnum):
    """An enum defining types of constants if a Bucket's BucketTypes value is CONSTANT.

    Attributes:
        PI: Pi
        HALF_PI: Pi/2
        THIRD_PI: Pi/3
        QUARTER_PI: Pi/4
        SIXTH_PI: Pi/6
        EIGHTH_PI: Pi/8
        TWO_PI: 2*Pi
        E: Euler's number
        C: Speed of light
        G: Gravitational constant
        PHI: Golden Ratio
    """

    PI = 1
    HALF_PI = 2
    THIRD_PI = 3
    QUARTER_PI = 4
    SIXTH_PI = 5
    EIGHTH_PI = 6
    TWO_PI = 7
    E = 8
    C = 10
    G = 11
    PHI = 12


@final
@dataclass
class Bucket_FFI(Structure):
    """Struct containing FFI representation of a Bucket."""

    _fields_ = [
        ("value", c_char_p),
        ("bucket_type", c_int),
        (
            "constant_type",
            c_int,
        ),
    ]

    value: bytes
    bucket_type: c_int
    constant_type: c_int


@final
@dataclass
class EngineSignalSet_FFI(Structure):
    """Struct containing FFI representation of a EngineSignalSet."""

    _fields_ = [
        ("stack_updated", c_bool),
        ("quit", c_bool),
        ("error", c_char_p),  # Will be None if no error
    ]

    stack_updated: bool
    quit: bool
    error: bytes


@dataclass
class Bucket:
    """A Bucket contains an item that can be on the stack.

    Attributes:
        value (str | None): String representation of a value
        bucket_type (BucketTypes): The type of value
        constant_type (ConstantTypes): Defines the constant if `bucket_type` is CONSTANT
    """

    value: str | None = None
    bucket_type: BucketTypes = BucketTypes.UNDEFINED
    constant_type: ConstantTypes = ConstantTypes.PI

    @classmethod
    def from_ffi(cls, ffi_bucket: Bucket_FFI) -> Bucket:
        """Create a Bucket from a Bucket_FFI.

        Args:
            ffi_bucket (Bucket_FFI): The Bucket_FFI to use in the conversion

        Returns:
            Bucket: A new Bucket containing the deserialized information
        """
        value: str | None = None
        if ffi_bucket.value:  # pragma: no branch
            value = ffi_bucket.value.decode("utf-8")

        return cls(
            value=value,
            bucket_type=BucketTypes(ffi_bucket.bucket_type),
            constant_type=ConstantTypes(ffi_bucket.constant_type),
        )


@dataclass
class EngineSignalSet:
    """Identifies EngineSignals triggered during submission of commands to the engine."""

    _stack_updated: bool
    _quit: bool
    _error: str | None

    @classmethod
    def from_ffi(cls, ffi_signal: EngineSignalSet_FFI) -> EngineSignalSet:
        """Construct a new EngineSignalSet from a EngineSignalSet_FFI object.

        Args:
            ffi_signal (EngineSignalSet_FFI): The EngineSignalSet_FFI object

        Returns:
            EngineSignalSet: The new EngineSignalSet
        """
        error_value: str | None = None
        if ffi_signal.error:
            error_value = ffi_signal.error.decode("utf-8")

        return cls(
            _stack_updated=ffi_signal.stack_updated,
            _quit=ffi_signal.quit,
            _error=error_value,
        )

    def stack_updated(self) -> bool:
        """Check if the stack has been updated and should be retrieved.

        Returns:
            bool: whether or not the stack is updated
        """
        return self._stack_updated

    def should_quit(self) -> bool:
        """Check if a quit was requested.

        This means that the user requested that the engine quit, and thus the frontend
        should also quit.

        Returns:
            bool: whether or not a quit was requested.
        """
        return self._quit

    def has_error(self) -> bool:
        """Check whether or not there is an error present.

        Returns:
            bool: whether or not there is an error
        """
        return self._error is not None

    def get_error(self) -> str:
        """Get the error that is present, if applicable.

        Returns:
            str: The error if it exists, or an empty string
        """
        return self._error or ""
