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

    # NOTE - NON TERMINALS
    def __NT_Program(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_DeclarationList()
        return n

    def __NT_DeclarationList(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_Declaration()
        self.__NT_DeclarationList1()
        return n

    def __NT_DeclarationList1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Declaration()
            self.__NT_DeclarationList1()
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_Declaration(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_VarDeclaration()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__NT_FunDeclaration()
        return n

    def __NT_VarDeclaration(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_TypeSpecifier()
        self.__T_Id()
        self.__NT_VarDeclaration1()
        return n

    def __NT_VarDeclaration1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Semicolon()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_SquareBracketsOpen()
        self.__T_Num()
        self.__T_SquareBracketsClose()
        self.__T_Semicolon()
        return n

    def __NT_TypeSpecifier(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Int()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_Void()
        return n

    def __NT_FunDeclaration(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Int()
            self.__T_Id()
            self.__T_ParenthesesOpen()
            self.__NT_Params()
            self.__T_ParenthesesClose()
            self.__NT_CompoundStmt()
            return n
        except:
            pass
        self.__currentTokenI = currentI
        self.__T_Void()
        self.__T_Id()
        self.__T_ParenthesesOpen()
        self.__NT_Params()
        self.__T_ParenthesesClose()
        self.__NT_CompoundStmt()
        return n

    def __NT_Params(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_ParamList()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_Void()
        return n

    def __NT_ParamList(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_Param()
        self.__NT_ParamList1()
        return n

    def __NT_ParamList1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Comma()
            self.__NT_Param()
            self.__NT_ParamList1()
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_Param(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Int()
            self.__T_Id()
            self.__NT_Param1()
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_Void()
        self.__T_Id()
        self.__NT_Param1()
        return n

    def __NT_Param1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_SquareBracketsOpen()
            self.__T_SquareBracketsClose()
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_CompoundStmt(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__T_CurlyBracketsOpen()
        self.__NT_LocalDeclarations()
        self.__NT_StatementList()
        self.__T_CurlyBracketsClose()
        return n

    def __NT_LocalDeclarations(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_LocalDeclarations1()
        return n

    def __NT_LocalDeclarations1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Int()
            self.__T_Id()
            self.__NT_LocalDeclarations2()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__T_Void()
            self.__T_Id()
            self.__NT_LocalDeclarations2()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_LocalDeclarations2(self):
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Semicolon()
            self.__NT_LocalDeclarations1()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_SquareBracketsOpen()
        self.__T_Num()
        self.__T_SquareBracketsClose()
        self.__T_Semicolon()
        self.__NT_LocalDeclarations1()
        return n

    def __NT_StatementList(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_StatementList1()
        return n

    def __NT_StatementList1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Statement()
            self.__NT_StatementList1()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_Statement(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_ExpressionStmt()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__T_CurlyBracketsOpen()
            self.__NT_LocalDeclarations()
            self.__NT_StatementList()
            self.__T_CurlyBracketsClose()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__NT_SelectionStmt()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__NT_IterationStmt()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__NT_ReturnStmt()
        return n

    def __NT_ExpressionStmt(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Expression()
            self.__T_Semicolon()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_Semicolon()
        return n

    def __NT_SelectionStmt(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__T_If()
        self.__T_ParenthesesOpen()
        self.__NT_Expression()
        self.__T_ParenthesesClose()
        self.__NT_Statement()
        self.__NT_SelectionStmt1()
        return n

    def __NT_SelectionStmt1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Else()
            self.__NT_Statement()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_IterationStmt(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__T_While()
        self.__T_ParenthesesOpen()
        self.__NT_Expression()
        self.__T_ParenthesesClose()
        self.__NT_Statement()
        return n

    def __NT_ReturnStmt(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__T_Return()
        self.__NT_ReturnStmt1()
        return n

    def __NT_ReturnStmt1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Semicolon()
            return n
        except:
            pass
        self.__currentTokenI = currentI
        self.__NT_Expression()
        self.__T_Semicolon()
        return n

    def __NT_Expression(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Var()
            self.__T_Assignement()
            self.__NT_Expression()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__NT_SimpleExpression()
        return n

    def __NT_Var(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__T_Id()
        self.__NT_Var1()
        return n

    def __NT_Var1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_SquareBracketsOpen()
            self.__NT_Expression()
            self.__T_SquareBracketsClose()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_SimpleExpression(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_AdditiveExpression()
        self.__NT_SimpleExpression1()
        return n

    def __NT_SimpleExpression1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Relop()
            self.__NT_AdditiveExpression()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_Relop(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_LessEqual()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__T_Less()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__T_Greater()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__T_GreaterEqual()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__T_Equal()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_Different()
        return n

    def __NT_AdditiveExpression(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_Term()
        self.__NT_AdditiveExpression1()
        return n

    def __NT_AdditiveExpression1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Addop()
            self.__NT_Term()
            self.__NT_AdditiveExpression1()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_Addop(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Plus()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_Minus()
        return n

    def __NT_Term(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__NT_Factor()
        self.__NT_Term1()
        return n

    def __NT_Term1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Mulop()
            self.__NT_Factor()
            self.__NT_Term1()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_Mulop(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Multiply()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
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
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__T_Id()
            self.__NT_Factor1()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__NT_Call()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_Num()
        return n

    def __NT_Factor1(self):
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_SquareBracketsOpen()
            self.__NT_Expression()
            self.__T_SquareBracketsClose()
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_Call(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        self.__T_Id()
        self.__T_ParenthesesOpen()
        self.__NT_Args()
        self.__T_ParenthesesClose()
        return n

    def __NT_Args(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_ArgList()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_ArgList(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Id()
            self.__NT_ArgList2()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__T_ParenthesesOpen()
            self.__NT_Expression()
            self.__T_ParenthesesClose()
            self.__NT_Term1()
            self.__NT_AdditiveExpression1()
            self.__NT_ArgList3()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_Num()
        self.__NT_Term1()
        self.__NT_AdditiveExpression1()
        self.__NT_ArgList3()
        return n

    def __NT_ArgList1(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Comma()
            self.__NT_Expression()
            self.__NT_ArgList1()
            return n
        except:
            pass
        self.__currentTokenI = currentI
        return n

    def __NT_ArgList2(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Assignement()
            self.__NT_Expression()
            self.__NT_ArgList1()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__T_SquareBracketsOpen()
            self.__NT_Expression()
            self.__T_SquareBracketsClose()
            self.__NT_ArgList4()
            return n
        except ParserSyntaxError:
            pass
        try:
            self.__currentTokenI = currentI
            self.__NT_Term1()
            self.__NT_AdditiveExpression1()
            self.__NT_ArgList3()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__T_ParenthesesOpen()
        self.__NT_Args()
        self.__T_ParenthesesClose()
        self.__NT_Term1()
        self.__NT_AdditiveExpression1()
        self.__NT_ArgList3()
        return n

    def __NT_ArgList3(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__NT_Relop()
            self.__NT_AdditiveExpression()
            self.__NT_ArgList1()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__NT_ArgList1()
        return n

    def __NT_ArgList4(self) -> sp.ParserTreeNode:
        n = sp.ParserTreeNode()
        currentI = self.__currentTokenI
        try:
            self.__T_Assignement()
            self.__NT_Expression()
            self.__NT_ArgList1()
            return n
        except ParserSyntaxError:
            pass
        self.__currentTokenI = currentI
        self.__NT_Term1()
        self.__NT_AdditiveExpression1()
        self.__NT_ArgList3()
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
