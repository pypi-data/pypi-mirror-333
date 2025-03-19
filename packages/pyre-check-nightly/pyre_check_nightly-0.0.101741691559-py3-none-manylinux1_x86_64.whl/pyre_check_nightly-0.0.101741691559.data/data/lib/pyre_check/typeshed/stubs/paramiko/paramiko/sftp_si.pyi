from typing import Any

from paramiko.server import ServerInterface
from paramiko.sftp_attr import SFTPAttributes
from paramiko.sftp_handle import SFTPHandle

class SFTPServerInterface:
    def __init__(self, server: ServerInterface, *largs: Any, **kwargs: Any) -> None: ...
    def session_started(self) -> None: ...
    def session_ended(self) -> None: ...
    def open(self, path: str, flags: int, attr: SFTPAttributes) -> SFTPHandle | int: ...
    def list_folder(self, path: str) -> list[SFTPAttributes] | int: ...
    def stat(self, path: str) -> SFTPAttributes | int: ...
    def lstat(self, path: str) -> SFTPAttributes | int: ...
    def remove(self, path: str) -> int: ...
    def rename(self, oldpath: str, newpath: str) -> int: ...
    def posix_rename(self, oldpath: str, newpath: str) -> int: ...
    def mkdir(self, path: str, attr: SFTPAttributes) -> int: ...
    def rmdir(self, path: str) -> int: ...
    def chattr(self, path: str, attr: SFTPAttributes) -> int: ...
    def canonicalize(self, path: str) -> str: ...
    def readlink(self, path: str) -> str | int: ...
    def symlink(self, target_path: str, path: str) -> int: ...
