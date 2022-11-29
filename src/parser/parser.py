import typing
import structures.token as ts


class Parser():
    def __init__(self) -> None:
        self.__tokens: typing.Sequence[ts.Token] = []
        self.__tokensI: int = 0
        self.__currentToken: ts.Token = self.__GetNextToken()
        return None

    def Parse(self) -> None:
        """
        """
        try:
            self.__NT_Program()
        except SyntaxError:
            ...
        return None

    def __Match(self, expected: ts.TokenType):
        """
        """
        if (self.__currentToken.type is expected):
            self.__currentToken = self.__GetNextToken()
        else:
            self.__Error(f'Could not match the actual token "{self.__currentToken}" at line {""}.{""} ')
        return None

    @staticmethod
    def __Error(message: str):
        """
        Raise a syntatic error with message describing it.
        """
        raise SyntaxError(message)

    def __GetNextToken(self) -> ts.Token:
        """
        Return the next token.
        """
        token = self.__currentToken = self.__tokens[self.__tokensI]
        self.__tokensI += 1
        return token

