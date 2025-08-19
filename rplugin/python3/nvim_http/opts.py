from enum import Enum
from typing import Optional


class ResponseBufferMode(Enum):
    """
    Enum for the different modes of the response buffer.
    """

    VERITCAL = "vsplit"
    HORIZONTAL = "split"
    TAB = "tabnew"

    @classmethod
    def from_args(cls, *args: str) -> "ResponseBufferMode":
        """
        Get the response buffer mode from the given arguments.
        """
        if "-t" in args or "--tab" in args:
            return ResponseBufferMode.TAB
        if "-h" in args or "--horizontal" in args:
            return ResponseBufferMode.HORIZONTAL
        return ResponseBufferMode.VERITCAL


class HttpRequestOptions:
    """
    Options for the HTTP request.
    """

    _default_timeout = 10
    _default_buffer_name= "/private/tmp/response.http" if __import__("platform").system() == "Darwin" else "/tmp/response.http"

    def __init__(self, *args: str):
        self.response_buffer_mode = ResponseBufferMode.from_args(*args)
        self.timeout = self._timeout_from_args(*args)
        self.disable_redirects = "--no-redirects" in args
        self.buffer_name = self._buffer_name_from_args(*args)
 
    @classmethod
    def _timeout_from_args(cls, *args: str) -> Optional[float]:
        """
        Get the timeout from the given arguments.
        """
        for i, arg in enumerate(args):
            if arg in ("-T", "--timeout") and i + 1 < len(args):
                return float(args[i + 1])

        return cls._default_timeout

    @classmethod
    def _buffer_name_from_args(cls, *args: str) -> str:
        """
        Get the buffer name from the given arguments.
        """
        for i, arg in enumerate(args):
            if arg == "--buffer-name" and i + 1 < len(args):
                return args[i + 1]

        return cls._default_buffer_name
