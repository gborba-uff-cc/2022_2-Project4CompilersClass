import io
import typing
import structures.token as st
import structures.parser_tree_node as sp


def SyntaxErrorText(
    msg: str,
    filename: str,
    currentToken: st.Token,
    previousToken: st.Token | None = None
) -> str:
    currentTokenText: str = f'the token \"{currentToken.value}\" @ {currentToken.lineNo}.{currentToken.columnNo} was not recognized'
    previousTokenText: str = ''
    if previousToken:
        previousTokenText = f', the last recognized token was \"{previousToken.value}\" @ {previousToken.lineNo}.{previousToken.columnNo}\n'
    hintText = f'Read the tokens as: (token) (@: at) (lineNo).(columnNo)'
    return f'{msg}\nOn the file {filename if filename else ""}{currentTokenText}{previousTokenText}{hintText}'

class ParserInvalidOptionError(SyntaxError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        if self.filename is None:
            self.filename: str = ''
        self.aToken: st.Token = st.Token()
        self.previousToken: st.Token | None = None

    def __str__(self) -> str:
        return SyntaxErrorText(self.msg, self.filename,self.aToken,self.previousToken)


class Parser():
    def __init__(
        self,
        sourceFile: io.TextIOWrapper,
        outTextFile: typing.TextIO,
        echoTrace: bool = False,
    ) -> None:
        self.__sourceFile = sourceFile
        self.__ouTextFile = outTextFile
        self.__echoTrace = echoTrace

        self.__tokens: typing.Sequence[st.Token] = []
        self.__currentTokenI: int = -1
        self.__furthestTokenReadI: int = -1
        self.__currentToken: st.Token = st.Token()

        # NOTE - load tokens
        self.__tokens = self.__ReadTokens()
        self.__currentToken = self.__GetNextToken()
        return None

    def __ReadTokens(self) -> typing.Sequence[st.Token]:
        """
        Return all tokens from the source file generated by the scanner.
        """
        tokens: typing.Sequence[st.Token] = []
        for line in self.__sourceFile.readlines():
            token = st.Token()
            token.FromStr(line)
            tokens.append(token)
        return tokens

    def Parse(self) -> sp.ParserTreeNode:
        """
        """
        n = sp.ParserTreeNode()
        try:
            n = self.__NT_Program()
        except EOFError:  # NOTE - reached the end of file
            print('Succesfully parsed the source file.',file=self.__ouTextFile)
        except ParserInvalidOptionError:
            # NOTE - capture parse error on the first declaration on program but
            # don't treat it
            pass
        finally:
            if self.__currentTokenI+1 != len(self.__tokens):
                print(SyntaxErrorText('Couldn\'t completely parse the source file.', '', self.__tokens[self.__furthestTokenReadI],  self.__tokens[self.__furthestTokenReadI-1]))
        return n

    def __Match(self, expected: st.TokenType):
        """
        """
        if (self.__currentToken.type is expected):
            self.__currentToken = self.__GetNextToken()
        else:
            furthestToken: st.Token = self.__tokens[self.__furthestTokenReadI]
            previousToken: st.Token | None = None
            if self.__furthestTokenReadI>0:
                previousToken = self.__tokens[self.__furthestTokenReadI-1]
            self.__UnexpectedTokenError('Couldn\'t match a token', furthestToken, previousToken)
        return None

    @staticmethod
    def __UnexpectedTokenError(
        msg: str,
        currentToken: st.Token,
        previousToken: st.Token | None
    ) -> typing.NoReturn:
        """
        Raise a syntatic error with message describing it.
        """
        error = ParserInvalidOptionError(msg)
        error.aToken = currentToken
        error.previousToken = previousToken
        raise error

    def __GetNextToken(self) -> st.Token:
        """
        Return the next token.
        """
        self.__currentTokenI += 1
        token = self.__currentToken = self.__tokens[self.__currentTokenI]
        if self.__furthestTokenReadI < self.__currentTokenI:
            self.__furthestTokenReadI = self.__currentTokenI
        if self.__currentToken.type is st.TokenType.EOF:
            raise EOFError()
        return token

    def __SetCurrentToken(self, tokenI: int) -> None:
        self.__currentTokenI = tokenI
        self.__currentToken = self.__tokens[self.__currentTokenI]
        return None
    # ------------------------------
    # NOTE - NON TERMINALS
    def __NT_Program(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_Declaration()
        self.__NT_DeclarationList()
        return n

    def __NT_DeclarationList(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Declaration()
            self.__NT_DeclarationList()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_Declaration(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Int()
            self.__T_Id()
            self.__NT_Declaration1()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_Void()
        self.__T_Id()
        self.__NT_Declaration1()
        return n

    def __NT_Declaration1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Semicolon()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_SquareBracketsOpen()
            self.__T_Num()
            self.__T_SquareBracketsClose()
            self.__T_Semicolon()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_ParenthesesOpen()
        self.__NT_Params()
        self.__T_ParenthesesClose()
        self.__NT_CompoundStmt()
        return n

    def __NT_Params(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Param()
            self.__NT_ParamList()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_Void()
        return n

    def __NT_ParamList(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Comma()
            self.__NT_Param()
            self.__NT_ParamList()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_Param(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Int()
            self.__T_Id()
            self.__NT_Param1()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_Void()
        self.__T_Id()
        self.__NT_Param1()
        return n

    def __NT_Param1(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_SquareBracketsOpen()
            self.__T_SquareBracketsClose()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_CompoundStmt(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__T_CurlyBracketsOpen()
        self.__NT_LocalDeclarations()
        self.__NT_StatementList()
        self.__T_CurlyBracketsClose()
        return n

    def __NT_LocalDeclarations(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Int()
            self.__T_Id()
            self.__NT_LocalDeclarations1()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_Void()
            self.__T_Id()
            self.__NT_LocalDeclarations1()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_LocalDeclarations1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Semicolon()
            self.__NT_LocalDeclarations()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_SquareBracketsOpen()
        self.__T_Num()
        self.__T_SquareBracketsClose()
        self.__T_Semicolon()
        self.__NT_LocalDeclarations()
        return n

    def __NT_StatementList(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Statement()
            self.__NT_StatementList()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_Statement(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Statement1()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_CurlyBracketsOpen()
            self.__NT_LocalDeclarations()
            self.__NT_StatementList()
            self.__T_CurlyBracketsClose()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_If()
            self.__T_ParenthesesOpen()
            self.__NT_Expression()
            self.__T_ParenthesesClose()
            self.__NT_Statement()
            self.__NT_Statement2()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_While()
            self.__T_ParenthesesOpen()
            self.__NT_Expression()
            self.__T_ParenthesesClose()
            self.__NT_Statement()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_Return()
        self.__NT_Statement1()
        return n

    def __NT_Statement1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Expression()
            self.__T_Semicolon()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_Semicolon()
        return n

    def __NT_Statement2(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Else()
            self.__NT_Statement()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_Expression(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Var()
            self.__T_Assignement()
            self.__NT_Expression()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__NT_SimpleExpression()
        return n

    def __NT_Var(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__T_Id()
        self.__NT_Factor1_OR_Var1()
        return n

    def __NT_SimpleExpression(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_AdditiveExpression()
        self.__NT_SimpleExpression1()
        return n

    def __NT_SimpleExpression1(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Relop()
            self.__NT_AdditiveExpression()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_Relop(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_LessEqual()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_Less()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_Greater()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_GreaterEqual()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_Equal()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_Different()
        return n

    def __NT_AdditiveExpression(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_Term()
        self.__NT_AdditiveExpression1()
        return n

    def __NT_AdditiveExpression1(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Addop()
            self.__NT_Term()
            self.__NT_AdditiveExpression1()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_Addop(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Plus()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_Minus()
        return n

    def __NT_Term(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_Factor()
        self.__NT_Term1()
        return n

    def __NT_Term1(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Mulop()
            self.__NT_Factor()
            self.__NT_Term1()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_Mulop(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Multiply()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_Divide()
        return n

    def __NT_Factor(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_ParenthesesOpen()
            self.__NT_Expression()
            self.__T_ParenthesesClose()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_Id()
            self.__NT_Factor2()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_Num()
        return n

    def __NT_Factor1_OR_Var1(self):
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_SquareBracketsOpen()
            self.__NT_Expression()
            self.__T_SquareBracketsClose()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_Factor2(self):
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_ParenthesesOpen()
            self.__NT_Args()
            self.__T_ParenthesesClose()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__NT_Factor1_OR_Var1()
        return n

    def __NT_Args(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Id()
            self.__NT_ArgList1()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_ParenthesesOpen()
            self.__NT_Expression()
            self.__T_ParenthesesClose()
            self.__NT_Term1()
            self.__NT_AdditiveExpression1()
            self.__NT_ArgList2()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_Num()
            self.__NT_Term1()
            self.__NT_AdditiveExpression1()
            self.__NT_ArgList2()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_ArgList(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Comma()
            self.__NT_Expression()
            self.__NT_ArgList()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        return n

    def __NT_ArgList1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Assignement()
            self.__NT_Expression()
            self.__NT_ArgList()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__T_SquareBracketsOpen()
            self.__NT_Expression()
            self.__T_SquareBracketsClose()
            self.__NT_ArgList3()
            return n
        except ParserInvalidOptionError:
            pass
        try:
            self.__SetCurrentToken(currentI)
            self.__NT_Term1()
            self.__NT_AdditiveExpression1()
            self.__NT_ArgList2()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__T_ParenthesesOpen()
        self.__NT_Args()
        self.__T_ParenthesesClose()
        self.__NT_Term1()
        self.__NT_AdditiveExpression1()
        self.__NT_ArgList2()
        return n

    def __NT_ArgList2(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Relop()
            self.__NT_AdditiveExpression()
            self.__NT_ArgList()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__NT_ArgList()
        return n

    def __NT_ArgList3(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Assignement()
            self.__NT_Expression()
            self.__NT_ArgList()
            return n
        except ParserInvalidOptionError:
            pass
        self.__SetCurrentToken(currentI)
        self.__NT_Term1()
        self.__NT_AdditiveExpression1()
        self.__NT_ArgList2()
        return n

    # NOTE - TERMINALS
    def __T_Id(self):
        return self.__Match(st.TokenType.ID)

    def __T_Num(self):
        return self.__Match(st.TokenType.NUM)

    def __T_Else(self):
        return self.__Match(st.TokenType.ELSE)

    def __T_If(self):
        return self.__Match(st.TokenType.IF)

    def __T_Int(self):
        return self.__Match(st.TokenType.INT)

    def __T_Return(self):
        return self.__Match(st.TokenType.RETURN)

    def __T_Void(self):
        return self.__Match(st.TokenType.VOID)

    def __T_While(self):
        return self.__Match(st.TokenType.WHILE)

    def __T_Plus(self):
        return self.__Match(st.TokenType.PLUS)

    def __T_Minus(self):
        return self.__Match(st.TokenType.MINUS)

    def __T_Multiply(self):
        return self.__Match(st.TokenType.MULTIPLY)

    def __T_Divide(self):
        return self.__Match(st.TokenType.DIVIDE)

    def __T_Less(self):
        return self.__Match(st.TokenType.LESS)

    def __T_LessEqual(self):
        return self.__Match(st.TokenType.LESS_EQUAL)

    def __T_Greater(self):
        return self.__Match(st.TokenType.GREATER)

    def __T_GreaterEqual(self):
        return self.__Match(st.TokenType.GREATER_EQUAL)

    def __T_Equal(self):
        return self.__Match(st.TokenType.EQUAL)

    def __T_Different(self):
        return self.__Match(st.TokenType.DIFFERENT)

    def __T_Assignement(self):
        return self.__Match(st.TokenType.ASSIGNEMENT)

    def __T_Semicolon(self):
        return self.__Match(st.TokenType.SEMICOLON)

    def __T_Comma(self):
        return self.__Match(st.TokenType.COMMA)

    def __T_ParenthesesOpen(self):
        return self.__Match(st.TokenType.PARENTHESES_OPEN)

    def __T_ParenthesesClose(self):
        return self.__Match(st.TokenType.PARENTHESES_CLOSE)

    def __T_SquareBracketsOpen(self):
        return self.__Match(st.TokenType.SQUARE_BRACKET_OPEN)

    def __T_SquareBracketsClose(self):
        return self.__Match(st.TokenType.SQUARE_BRACKET_CLOSE)

    def __T_CurlyBracketsOpen(self):
        return self.__Match(st.TokenType.CURLY_BRACKETS_OPEN)

    def __T_CurlyBracketsClose(self):
        return self.__Match(st.TokenType.CURLY_BRACKETS_CLOSE)

    # def T_CommentOpen(self):
    #     return self.__Match()

    # def T_CommentClose(self):
    #     return self.__Match()
