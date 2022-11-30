import typing
import structures.token as st
import structures.parser_tree_node as sp


class ParserSyntaxError(SyntaxError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Parser():
    def __init__(self) -> None:
        self.__tokens: typing.Sequence[st.Token] = []
        self.__currentTokenI: int = 0
        self.__currentToken: st.Token = self.__GetNextToken()
        return None

    def Parse(self) -> None:
        """
        """
        try:
            self.__NT_Program()
        except ParserSyntaxError:
            ...
        return None

    def __Match(self, expected: st.TokenType):
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
        raise ParserSyntaxError(message)

    def __GetNextToken(self) -> st.Token:
        """
        Return the next token.
        """
        token = self.__currentToken = self.__tokens[self.__currentTokenI]
        self.__currentTokenI += 1
        return token

