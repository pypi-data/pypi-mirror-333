from _typeshed import StrOrBytesPath
from distutils.cmd import Command
from typing import ClassVar

class bdist_wininst(Command):
    description: ClassVar[str]
    user_options: ClassVar[list[tuple[str, str | None, str]]]
    boolean_options: ClassVar[list[str]]

    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    def run(self) -> None: ...
    def get_inidata(self) -> str: ...
    def create_exe(self, arcname: StrOrBytesPath, fullname: str, bitmap: StrOrBytesPath | None = None) -> None: ...
    def get_installer_filename(self, fullname: str) -> str: ...
    def get_exe_bytes(self) -> bytes: ...
