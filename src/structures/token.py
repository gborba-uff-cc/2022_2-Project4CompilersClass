import enum
import typing


@enum.unique
class TokenType(enum.Enum):
    ERROR = enum.auto()
    EOF = enum.auto()
    ID = enum.auto()
    NUM = enum.auto()
    KEYWORD = enum.auto()
    SYMBOL = enum.auto()
    COMMENT = enum.auto()


class Token(typing.NamedTuple):
    type: TokenType
    value: str

    def __str__(self) -> str:
        return f'<{self.type.name},"{self.value}">'

