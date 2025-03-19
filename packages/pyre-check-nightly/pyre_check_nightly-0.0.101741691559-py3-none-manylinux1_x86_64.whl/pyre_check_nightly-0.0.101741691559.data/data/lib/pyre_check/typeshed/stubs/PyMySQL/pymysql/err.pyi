import builtins
from typing import NoReturn

from .constants import ER as ER

class MySQLError(Exception): ...
class Warning(builtins.Warning, MySQLError): ...
class Error(MySQLError): ...
class InterfaceError(Error): ...
class DatabaseError(Error): ...
class DataError(DatabaseError): ...
class OperationalError(DatabaseError): ...
class IntegrityError(DatabaseError): ...
class InternalError(DatabaseError): ...
class ProgrammingError(DatabaseError): ...
class NotSupportedError(DatabaseError): ...

error_map: dict[int, type[DatabaseError]]

def raise_mysql_exception(data) -> NoReturn: ...
