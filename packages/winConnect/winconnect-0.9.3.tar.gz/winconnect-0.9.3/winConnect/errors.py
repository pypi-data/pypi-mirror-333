from dataclasses import dataclass
from enum import Enum


class WinConnectErrors(Enum):
    NO_ERROR = 0

    INIT_FIRST = 10

    UNKNOWN_DATA_TYPE = 30
    UNKNOWN_COMMAND = 31
    UNKNOWN_ACTION = 32

    BAD_DATA = 50
    BAD_VERSION = 51
    BAD_HEADER = 52
    BAD_SETTINGS = 53
    BAD_CRYPTO = 54

    BODY_TOO_BIG = 60


@dataclass
class WinConnectError:
    code: WinConnectErrors
    message: str
