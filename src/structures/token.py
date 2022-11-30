import enum
import typing


@enum.unique
class TokenType(enum.Enum):
    ERROR = enum.auto()
    EOF = enum.auto()
    ID = enum.auto()
    NUM = enum.auto()
    COMMENT = enum.auto()
    # NOTE - keyword
    KEYWORD = enum.auto()
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    # NOTE - symbols
    SYMBOL = enum.auto()
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    LESS = '<'
    LESS_EQUAL = '<='
    GREATER = '>'
    GREATER_EQUAL = '>='
    EQUAL = '=='
    DIFFERENT = '!='
    ASSIGNEMENT = '='
    SEMICOLON = ';'
    COMMA = ','
    PARENTHESES_OPEN = '('
    PARENTHESES_CLOSE = ')'
    SQUARE_BRACKET_OPEN = '['
    SQUARE_BRACKET_CLOSE = ']'
    CURLY_BRACKETS_OPEN = '{'
    CURLY_BRACKETS_CLOSE = '}'


class Token():
    def __init__(
        self,
        type: TokenType = TokenType.ERROR,
        value: str = '',
        lineNo: int = -1,
        columnNo: int = -1
    ) -> None:
        self.type = type
        self.value = value
        self.lineNo = lineNo
        self.columnNo = columnNo
        return None

    def __str__(self) -> str:
        return f'<{self.lineNo},{self.columnNo},{self.type.name},"{self.value}">'


