from _typeshed import FileDescriptorOrPath, ReadableBuffer, WriteableBuffer
from collections.abc import Iterable
from io import FileIO

from ..base import AsyncBase, AsyncIndirectBase

# This class does not exist at runtime and instead these methods are
# all dynamically patched in.
class _UnknownAsyncBinaryIO(AsyncBase[bytes]):
    async def close(self) -> None: ...
    async def flush(self) -> None: ...
    async def isatty(self) -> bool: ...
    async def read(self, size: int = ..., /) -> bytes: ...
    async def readinto(self, buffer: WriteableBuffer, /) -> int | None: ...
    async def readline(self, size: int | None = ..., /) -> bytes: ...
    async def readlines(self, hint: int = ..., /) -> list[bytes]: ...
    async def seek(self, offset: int, whence: int = ..., /) -> int: ...
    async def seekable(self) -> bool: ...
    async def tell(self) -> int: ...
    async def truncate(self, size: int | None = ..., /) -> int: ...
    async def writable(self) -> bool: ...
    async def write(self, b: ReadableBuffer, /) -> int: ...
    async def writelines(self, lines: Iterable[ReadableBuffer], /) -> None: ...
    def fileno(self) -> int: ...
    def readable(self) -> bool: ...
    @property
    def closed(self) -> bool: ...
    @property
    def mode(self) -> str: ...
    @property
    def name(self) -> FileDescriptorOrPath: ...

class AsyncBufferedIOBase(_UnknownAsyncBinaryIO):
    async def read1(self, size: int = ..., /) -> bytes: ...
    def detach(self) -> FileIO: ...
    @property
    def raw(self) -> FileIO: ...

class AsyncIndirectBufferedIOBase(AsyncIndirectBase[bytes], _UnknownAsyncBinaryIO):
    async def read1(self, size: int = ..., /) -> bytes: ...
    def detach(self) -> FileIO: ...
    @property
    def raw(self) -> FileIO: ...

class AsyncBufferedReader(AsyncBufferedIOBase):
    async def peek(self, size: int = ..., /) -> bytes: ...

class AsyncIndirectBufferedReader(AsyncIndirectBufferedIOBase):
    async def peek(self, size: int = ..., /) -> bytes: ...

class AsyncFileIO(_UnknownAsyncBinaryIO):
    async def readall(self) -> bytes: ...

class AsyncIndirectFileIO(AsyncIndirectBase[bytes], _UnknownAsyncBinaryIO):
    async def readall(self) -> bytes: ...
