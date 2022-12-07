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
    return f'{msg}\nOn the file{f" {filename}" if filename else ""}, {currentTokenText}{previousTokenText}{hintText}'

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
        self.__traceStack: list[str] = []

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
        if self.__echoTrace:
            print("\n\nParsing the souce file", file=self.__ouTextFile)

        n = sp.ParserTreeNode('')
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

    def __Match(self, expected: st.TokenType) -> sp.ParserTreeNode:
        """
        """
        ruleName = f'T_{expected.name.capitalize()}'
        self.__traceStack.append(ruleName)
        self.__PrintTrace()
        self.__traceStack.pop()

        n = sp.ParserTreeNode(self.__currentToken)

        if (self.__currentToken.type is expected):
            self.__currentToken = self.__GetNextToken()
        else:
            furthestToken: st.Token = self.__tokens[self.__furthestTokenReadI]
            previousToken: st.Token | None = None
            if self.__furthestTokenReadI>0:
                previousToken = self.__tokens[self.__furthestTokenReadI-1]
            self.__UnexpectedTokenError('Couldn\'t match a token', furthestToken, previousToken)
        return n

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
        if self.__currentToken.type is st.TokenType.EOF and self.__furthestTokenReadI == len(self.__tokens)-2:
            raise EOFError()
        return token

    def __SetCurrentToken(self, tokenI: int) -> None:
        self.__currentTokenI = tokenI
        self.__currentToken = self.__tokens[self.__currentTokenI]
        return None

    def __PrintTrace(self) -> None:
        if not self.__echoTrace:
            return None
        lenTraceStack: int = len(self.__traceStack)
        print('current trace stack: ', end='', file=self.__ouTextFile)
        for i in range(lenTraceStack):
            productionRule = self.__traceStack[i]
            endStr = '->' if i != lenTraceStack-1 else '\n'
            print(f'{productionRule}',end=endStr,file=self.__ouTextFile)
        return None

    def __ProductionRuleName(self, productionRule: typing.Callable) -> str:
        return productionRule.__qualname__.split(".__")[-1]

    # ------------------------------
    # NOTE - NON TERMINALS
    def __NT_Program(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Program)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        try:
            tmp = self.__NT_Declaration()
            n.AddNode(tmp)
            tmp = self.__NT_DeclarationList()
            n.AddNode(tmp)
        except EOFError:
            pass

        self.__traceStack.pop()
        return n

    def __NT_DeclarationList(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_DeclarationList)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__NT_Declaration()
            n.AddNode(tmp)
            tmp = self.__NT_DeclarationList()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_Declaration(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Declaration)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Int()
            n.AddNode(tmp)
            tmp = self.__T_Id()
            n.AddNode(tmp)
            tmp = self.__NT_Declaration1()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__T_Void()
        n.AddNode(tmp)
        tmp = self.__T_Id()
        n.AddNode(tmp)
        tmp = self.__NT_Declaration1()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Declaration1(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Declaration1)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Semicolon()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_SquareBracketsOpen()
            n.AddNode(tmp)
            tmp = self.__T_Num()
            n.AddNode(tmp)
            tmp = self.__T_SquareBracketsClose()
            n.AddNode(tmp)
            tmp = self.__T_Semicolon()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__T_ParenthesesOpen()
        n.AddNode(tmp)
        tmp = self.__NT_Params()
        n.AddNode(tmp)
        tmp = self.__T_ParenthesesClose()
        n.AddNode(tmp)
        tmp = self.__NT_CompoundStmt()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Params(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Params)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Void()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__NT_Param()
        n.AddNode(tmp)
        tmp = self.__NT_ParamList()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_ParamList(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_ParamList)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Comma()
            n.AddNode(tmp)
            tmp = self.__NT_Param()
            n.AddNode(tmp)
            tmp = self.__NT_ParamList()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_Param(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Param)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Int()
            n.AddNode(tmp)
            tmp = self.__T_Id()
            n.AddNode(tmp)
            tmp = self.__NT_Param1()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__T_Void()
        n.AddNode(tmp)
        tmp = self.__T_Id()
        n.AddNode(tmp)
        tmp = self.__NT_Param1()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Param1(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_Param1)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_SquareBracketsOpen()
            n.AddNode(tmp)
            tmp = self.__T_SquareBracketsClose()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_CompoundStmt(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_CompoundStmt)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        tmp = self.__T_CurlyBracketsOpen()
        n.AddNode(tmp)
        tmp = self.__NT_LocalDeclarations()
        n.AddNode(tmp)
        tmp = self.__NT_StatementList()
        n.AddNode(tmp)
        tmp = self.__T_CurlyBracketsClose()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_LocalDeclarations(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_LocalDeclarations)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Int()
            n.AddNode(tmp)
            tmp = self.__T_Id()
            n.AddNode(tmp)
            tmp = self.__NT_LocalDeclarations1()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_Void()
            n.AddNode(tmp)
            tmp = self.__T_Id()
            n.AddNode(tmp)
            tmp = self.__NT_LocalDeclarations1()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_LocalDeclarations1(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_LocalDeclarations1)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Semicolon()
            n.AddNode(tmp)
            tmp = self.__NT_LocalDeclarations()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__T_SquareBracketsOpen()
        n.AddNode(tmp)
        tmp = self.__T_Num()
        n.AddNode(tmp)
        tmp = self.__T_SquareBracketsClose()
        n.AddNode(tmp)
        tmp = self.__T_Semicolon()
        n.AddNode(tmp)
        tmp = self.__NT_LocalDeclarations()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_StatementList(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_StatementList)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__NT_Statement()
            n.AddNode(tmp)
            tmp = self.__NT_StatementList()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_Statement(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Statement)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_CurlyBracketsOpen()
            n.AddNode(tmp)
            tmp = self.__NT_LocalDeclarations()
            n.AddNode(tmp)
            tmp = self.__NT_StatementList()
            n.AddNode(tmp)
            tmp = self.__T_CurlyBracketsClose()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_If()
            n.AddNode(tmp)
            tmp = self.__T_ParenthesesOpen()
            n.AddNode(tmp)
            tmp = self.__NT_Expression()
            n.AddNode(tmp)
            tmp = self.__T_ParenthesesClose()
            n.AddNode(tmp)
            tmp = self.__NT_Statement()
            n.AddNode(tmp)
            tmp = self.__NT_Statement2()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_While()
            n.AddNode(tmp)
            tmp = self.__T_ParenthesesOpen()
            n.AddNode(tmp)
            tmp = self.__NT_Expression()
            n.AddNode(tmp)
            tmp = self.__T_ParenthesesClose()
            n.AddNode(tmp)
            tmp = self.__NT_Statement()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_Return()
            n.AddNode(tmp)
            tmp = self.__NT_Statement1()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__NT_Statement1()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Statement1(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Statement1)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Semicolon()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__NT_Expression()
        n.AddNode(tmp)
        tmp = self.__T_Semicolon()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Statement2(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_Statement2)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Else()
            n.AddNode(tmp)
            tmp = self.__NT_Statement()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_Expression(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Expression)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__NT_Var()
            n.AddNode(tmp)
            tmp = self.__T_Assignement()
            n.AddNode(tmp)
            tmp = self.__NT_Expression()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__NT_SimpleExpression()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Var(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Var)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        tmp = self.__T_Id()
        n.AddNode(tmp)
        tmp = self.__NT_Factor1_OR_Var1()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_SimpleExpression(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_SimpleExpression)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        tmp = self.__NT_AdditiveExpression()
        n.AddNode(tmp)
        tmp = self.__NT_SimpleExpression1()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_SimpleExpression1(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_SimpleExpression1)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__NT_Relop()
            n.AddNode(tmp)
            tmp = self.__NT_AdditiveExpression()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_Relop(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Relop)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_LessEqual()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_Less()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_Greater()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_GreaterEqual()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_Equal()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__T_Different()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_AdditiveExpression(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_AdditiveExpression)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        tmp = self.__NT_Term()
        n.AddNode(tmp)
        tmp = self.__NT_AdditiveExpression1()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_AdditiveExpression1(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_AdditiveExpression1)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__NT_Addop()
            n.AddNode(tmp)
            tmp = self.__NT_Term()
            n.AddNode(tmp)
            tmp = self.__NT_AdditiveExpression1()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_Addop(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Addop)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Plus()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__T_Minus()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Term(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Term)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        tmp = self.__NT_Factor()
        n.AddNode(tmp)
        tmp = self.__NT_Term1()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Term1(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_Term1)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__NT_Mulop()
            n.AddNode(tmp)
            tmp = self.__NT_Factor()
            n.AddNode(tmp)
            tmp = self.__NT_Term1()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_Mulop(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Mulop)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Multiply()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__T_Divide()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Factor(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_Factor)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_ParenthesesOpen()
            n.AddNode(tmp)
            tmp = self.__NT_Expression()
            n.AddNode(tmp)
            tmp = self.__T_ParenthesesClose()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_Id()
            n.AddNode(tmp)
            tmp = self.__NT_Factor2()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__T_Num()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Factor1_OR_Var1(self):
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_Factor1_OR_Var1)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_SquareBracketsOpen()
            n.AddNode(tmp)
            tmp = self.__NT_Expression()
            n.AddNode(tmp)
            tmp = self.__T_SquareBracketsClose()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_Factor2(self):
        ruleName: str = self.__ProductionRuleName(self.__NT_Factor2)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_ParenthesesOpen()
            n.AddNode(tmp)
            tmp = self.__NT_Args()
            n.AddNode(tmp)
            tmp = self.__T_ParenthesesClose()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__NT_Factor1_OR_Var1()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_Args(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_Args)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Id()
            n.AddNode(tmp)
            tmp = self.__NT_ArgList1()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_ParenthesesOpen()
            n.AddNode(tmp)
            tmp = self.__NT_Expression()
            n.AddNode(tmp)
            tmp = self.__T_ParenthesesClose()
            n.AddNode(tmp)
            tmp = self.__NT_Term1()
            n.AddNode(tmp)
            tmp = self.__NT_AdditiveExpression1()
            n.AddNode(tmp)
            tmp = self.__NT_ArgList2()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_Num()
            n.AddNode(tmp)
            tmp = self.__NT_Term1()
            n.AddNode(tmp)
            tmp = self.__NT_AdditiveExpression1()
            n.AddNode(tmp)
            tmp = self.__NT_ArgList2()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_ArgList(self) -> sp.ParserTreeNode:
        #NOTE - optional production
        ruleName: str = self.__ProductionRuleName(self.__NT_ArgList)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Comma()
            n.AddNode(tmp)
            tmp = self.__NT_Expression()
            n.AddNode(tmp)
            tmp = self.__NT_ArgList()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)

        self.__traceStack.pop()
        return n

    def __NT_ArgList1(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_ArgList1)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Assignement()
            n.AddNode(tmp)
            tmp = self.__NT_Expression()
            n.AddNode(tmp)
            tmp = self.__NT_ArgList()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_SquareBracketsOpen()
            n.AddNode(tmp)
            tmp = self.__NT_Expression()
            n.AddNode(tmp)
            tmp = self.__T_SquareBracketsClose()
            n.AddNode(tmp)
            tmp = self.__NT_ArgList3()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        try:
            self.__SetCurrentToken(currentI)
            tmp = self.__T_ParenthesesOpen()
            n.AddNode(tmp)
            tmp = self.__NT_Args()
            n.AddNode(tmp)
            tmp = self.__T_ParenthesesClose()
            n.AddNode(tmp)
            tmp = self.__NT_Term1()
            n.AddNode(tmp)
            tmp = self.__NT_AdditiveExpression1()
            n.AddNode(tmp)
            tmp = self.__NT_ArgList2()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__NT_Term1()
        n.AddNode(tmp)
        tmp = self.__NT_AdditiveExpression1()
        n.AddNode(tmp)
        tmp = self.__NT_ArgList2()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_ArgList2(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_ArgList2)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__NT_Relop()
            n.AddNode(tmp)
            tmp = self.__NT_AdditiveExpression()
            n.AddNode(tmp)
            tmp = self.__NT_ArgList()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__NT_ArgList()
        n.AddNode(tmp)

        self.__traceStack.pop()
        return n

    def __NT_ArgList3(self) -> sp.ParserTreeNode:
        ruleName: str = self.__ProductionRuleName(self.__NT_ArgList3)
        self.__traceStack.append(ruleName)
        self.__PrintTrace()

        n = sp.ParserTreeNode(ruleName)
        currentI = self.__currentTokenI
        try:
            tmp = self.__T_Assignement()
            n.AddNode(tmp)
            tmp = self.__NT_Expression()
            n.AddNode(tmp)
            tmp = self.__NT_ArgList()
            n.AddNode(tmp)

            self.__traceStack.pop()
            return n
        except ParserInvalidOptionError:
            n.ClearNode()
        self.__SetCurrentToken(currentI)
        tmp = self.__NT_Term1()
        n.AddNode(tmp)
        tmp = self.__NT_AdditiveExpression1()
        n.AddNode(tmp)
        tmp = self.__NT_ArgList2()
        n.AddNode(tmp)

        self.__traceStack.pop()
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
