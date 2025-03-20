from __future__ import annotations

import ctypes
import pathlib
import platform
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from os import PathLike

from ._data_structs import Bucket, Bucket_FFI, EngineSignalSet, EngineSignalSet_FFI

COMPATIBLE_ENGINE_VERSION: Final[bytes] = b">=2.1.0,<3.0"


class SquiidEngine:
    """Class used to access the Squiid engine."""

    def __init__(self, library_path: str | PathLike[str] | None = None) -> None:
        """Construct a new Squiid engine class.

        Args:
            library_path (str | PathLike[str] | None): path to `libsquiid_engine.so`
        """
        if library_path is None:
            file_directory = pathlib.Path(__file__).parent.resolve()

            prefix = "lib"
            extension = ".so"
            if platform.system() == "Windows":  # pragma: no cover
                prefix = ""
                extension = ".dll"
            elif platform.system() == "Darwin":  # pragma: no cover
                extension = ".dylib"

            resolved_library_path = (
                file_directory / f"{prefix}squiid_engine{extension}"
            ).resolve()
        else:
            resolved_library_path = pathlib.Path(library_path).resolve()

        # check if library exists before loading
        if not resolved_library_path.is_file():
            exception_message = f"Shared library not found at {resolved_library_path}"
            raise FileNotFoundError(exception_message)

        self._lib: ctypes.CDLL = ctypes.CDLL(str(resolved_library_path))

        # define function argument and result types
        self._lib.execute_multiple_rpn_exposed.argtypes = [
            ctypes.POINTER(ctypes.c_char_p),
            ctypes.c_size_t,
        ]
        self._lib.execute_multiple_rpn_exposed.restype = EngineSignalSet_FFI

        self._lib.get_stack_exposed.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self._lib.get_stack_exposed.restype = ctypes.POINTER(ctypes.POINTER(Bucket_FFI))

        self._lib.get_commands_exposed.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self._lib.get_commands_exposed.restype = ctypes.POINTER(ctypes.c_char_p)

        self._lib.get_previous_answer_exposed.argtypes = []
        self._lib.get_previous_answer_exposed.restype = ctypes.POINTER(Bucket_FFI)

        self._lib.update_previous_answer_exposed.argtypes = []
        self._lib.update_previous_answer_exposed.restype = EngineSignalSet_FFI

        # Version check function
        self._lib.check_compatible.argtypes = [
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.POINTER(ctypes.c_char)),
        ]
        self._lib.check_compatible.restype = ctypes.c_bool

        # Add cleanup functions
        self._lib.free_engine_signal_set.argtypes = [EngineSignalSet_FFI]
        self._lib.free_engine_signal_set.restype = None

        self._lib.free_string_array.argtypes = [
            ctypes.POINTER(ctypes.c_char_p),
            ctypes.c_int,
        ]
        self._lib.free_string_array.restype = None

        self._lib.free_string.argtypes = [ctypes.c_char_p]
        self._lib.free_string.restype = None

        self._lib.free_bucket_array.argtypes = [
            ctypes.POINTER(ctypes.POINTER(Bucket_FFI)),  # array pointer
            ctypes.c_int,  # length
        ]
        self._lib.free_bucket_array.restype = None

        self._lib.free_bucket.argtypes = [ctypes.POINTER(Bucket_FFI)]
        self._lib.free_bucket.restype = None

        # check version compatibility with loaded library
        self._check_compatible()

    def _check_compatible(self) -> None:
        """Check version compatibility with the library.

        Raises:
            RuntimeError: If the versions are incompatible
        """
        error = ctypes.POINTER(ctypes.c_char)()
        if not self._lib.check_compatible(
            ctypes.c_char_p(COMPATIBLE_ENGINE_VERSION),
            ctypes.byref(error),
        ):
            # copy the error and free the original
            error_copy = b""
            if error:  # pragma: no branch
                error_copy = ctypes.cast(error, ctypes.c_char_p).value or b""
                self._lib.free_string(error)

            raise RuntimeError(error_copy.decode())

        if error:
            self._lib.free_string(error)  # pragma: no cover

    def execute_multiple_rpn(self, data: list[str]) -> EngineSignalSet:
        """Execute multiple RPN commands in the engine at once.

        Args:
            data (list[str]): list of RPN commands as strings. Example: ["3", "3", "add"]

        Returns:
            EngineSignalSet: Which Engine Signals were triggered from the commands
        """
        encoded_data = [item.encode("utf-8") for item in data]

        # get pointer to data
        data_ptr = (ctypes.c_char_p * len(encoded_data))(*encoded_data)

        # submit data to engine
        result: EngineSignalSet_FFI = self._lib.execute_multiple_rpn_exposed(
            data_ptr,
            len(encoded_data),
        )

        messages = EngineSignalSet.from_ffi(result)

        self._lib.free_engine_signal_set(result)

        return messages

    def execute_single_rpn(self, data: str) -> EngineSignalSet:
        """Execute a single RPN statement.

        Args:
            data (str): the single command to execute

        Returns:
            EngineSignalSet: Which Engine Signals were triggered from the commands
        """
        return self.execute_multiple_rpn([data])

    def get_stack(self) -> list[Bucket]:
        """Get the current stack from the engine.

        Returns:
            list[Bucket]: The stack
        """
        # define variable to store stack length
        out_len = ctypes.c_int(0)

        # get stack from engine
        stack: list[Any] = self._lib.get_stack_exposed(ctypes.byref(out_len))  # pyright: ignore[reportExplicitAny]

        try:
            stack_items: list[Bucket] = []
            # iterate over the given array and convert the Bucket_FFI elements to Bucket
            for i in range(out_len.value):
                if stack[i]:  # pragma: no branch
                    curr_value: Bucket_FFI = stack[i].contents  # pyright: ignore[reportAny]
                    stack_items.append(Bucket.from_ffi(curr_value))

            return stack_items

        finally:
            # cleanup in case of error
            self._lib.free_bucket_array(stack, out_len)

    def get_commands(self) -> list[str]:
        """Get a list of valid commands that the engine accepts.

        Returns:
            list[str]: list of commands from the engine

        Raises:
            RuntimeError: Raises if no commands are returned, though this shouldn't happen
        """
        # define variable to store stack length
        out_len = ctypes.c_int(0)

        result_ptr = None

        try:
            # try to get the commands
            result_ptr: list[bytes] | None = self._lib.get_commands_exposed(
                ctypes.byref(out_len),
            )

            # return none on failure
            if not result_ptr or out_len.value == 0:  # pragma: no cover
                error_msg = "no commands were returned from the engine"
                raise RuntimeError(error_msg)

            command_list: list[str] = []
            # iterate over the array of results
            for i in range(out_len.value):
                # get the current result value
                curr_value = ctypes.c_char_p(result_ptr[i]).value

                if curr_value is not None:  # pragma: no branch
                    # append it to the result list if not None
                    command_list.append(curr_value.decode("utf-8"))

            return command_list

        finally:
            # free the unneeded bytes once finished
            if result_ptr and out_len.value > 0:
                self._lib.free_string_array(result_ptr, out_len)

    def get_previous_answer(self) -> Bucket:
        """Get the current previous answer variable from the engine.

        Returns:
            Bucket: Bucket containing the value of the previous answer
        """
        bucket_ffi_ptr = self._lib.get_previous_answer_exposed()  # pyright: ignore[reportAny]

        try:
            return Bucket.from_ffi(bucket_ffi_ptr.contents)  # pyright: ignore[reportAny]
        finally:
            # cleanup in case of error
            self._lib.free_bucket(bucket_ffi_ptr)

    def update_previous_answer(self) -> EngineSignalSet:
        """Update the previous answer variable in the engine.

        This should be called after a full algebraic statement in algebraic mode,
        or after each RPN command if in RPN mode.

        Returns:
            EngineSignalSet: Holds errors encountered while updating the previous answer
        """
        signals_ffi: EngineSignalSet_FFI = self._lib.update_previous_answer_exposed()

        try:
            return EngineSignalSet.from_ffi(signals_ffi)
        finally:
            # free signals in case of error
            self._lib.free_engine_signal_set(signals_ffi)
