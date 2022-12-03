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
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    # NOTE - symbols
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

    def FromStr(self, s: str) -> None:
        _, _, s = s.partition('<')
        s, _, _ = s.partition('>')
        lineNoStr, _, s = s.partition(',')
        lineNo = int(lineNoStr)

        columnNoStr, _, s = s.partition(',')
        columnNo = int(columnNoStr)

        typeName, _, s = s.partition(',')
        type = self.__GetTypeByTypeName(typeName)

        value = s.strip('"')

        self.type = type
        self.value = value
        self.lineNo = lineNo
        self.columnNo = columnNo
        return None

    @staticmethod
    def __GetTypeByTypeName(name: str) -> TokenType:
        """
        Return the token type by its name.
        """
        tokenType: TokenType = TokenType.ERROR
        for tt in TokenType:
            if name == tt.name:
                return tt
        return tokenType
