import copy
import enum
import io
import typing

import automata.base.exceptions as abe
import automata.fa.dfa as afd
import finite_automaton.automaton_language_cminus as fa_alc
import tools.toolbox as tt


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
        return f'<{self.type.name},\'{self.value}\'>'


class Scanner(afd.DFA):
    def __init__(
        self,
        sourceFile: io.TextIOWrapper,
        outTextFile: typing.TextIO,
        echoLines: bool = False,
        echoTrace: bool = False
    ) -> None:
        self.__sourceFile = sourceFile
        self.__outTextFile = outTextFile
        self.__echoLines = echoLines
        self.__echoTrace = echoTrace
        self.__lineNum: int = 0
        self.__linePos: int = 0
        self.__lineBuff: str = ''
        self.__wordRead:str = ''
        self.__lastFinalStateReached: str = ''
        # ----------
        cMinus = fa_alc.dictCMinusDfas[fa_alc.CMinusDFAs.CMinus]
        self.states = cMinus.states.copy()
        self.input_symbols = cMinus.input_symbols.copy()
        self.transitions = copy.deepcopy(cMinus.transitions)
        self.initial_state = cMinus.initial_state
        self.final_states = cMinus.final_states.copy()
        self.allow_partial = False
        self.validate()

    def GetToken(self) -> Token:
        """
        Return one token read from the file one token per call.

        Echo the raws read tokens if echoTrace if needed.
        """
        self.__wordRead = ''
        tokenType: TokenType = TokenType.ERROR
        tokenValue: str = ''
        # NOTE - run automaton
        try:
            self.__ScanInputStepwise()
            tokenValue = self.__wordRead
            tokenType = self.IdentifyTokenTypeByValue(tokenValue)
        except EOFError:
            tokenType = TokenType.EOF
            tokenValue = ''
        except abe.RejectionException:
            tokenType = TokenType.ERROR
            tokenValue = self.__wordRead
        token = Token(tokenType, tokenValue)
        if self.__echoTrace:
            self.__EchoToken(token)
        return token

    def IdentifyTokenTypeByValue(self, value: str) -> TokenType:
        tokenType = TokenType.ERROR
        for dfaType, M in fa_alc.dictCMinusDfas.items():
            if M.accepts_input(value):
                if dfaType is fa_alc.CMinusDFAs.Keywords:
                    tokenType = TokenType.KEYWORD
                elif dfaType is fa_alc.CMinusDFAs.Identifiers:
                    tokenType = TokenType.ID
                elif dfaType is fa_alc.CMinusDFAs.Numbers:
                    tokenType = TokenType.NUM
                elif dfaType is fa_alc.CMinusDFAs.Operators:
                    tokenType = TokenType.SYMBOL
                elif dfaType is fa_alc.CMinusDFAs.Comments:
                    tokenType = TokenType.COMMENT
        return tokenType

    def __ScanInputStepwise(self) -> None:
        """
        Read character by character from the file until the word read is valid.
        """
        word = []
        self.__lastFinalStateReached = ''
        emptyWordAndEOF = False
        inError = False
        current_state = self.initial_state

        while True:
            try:
                c = self.__GetNextChar()
                input_symbol = tt.TranslateSymbols(c)

                current_state = self._get_next_current_state(current_state, input_symbol)

                if current_state in self.final_states:
                    self.__lastFinalStateReached = current_state
                else:
                    # NOTE - in error estate if current state represents the
                    # error states of all DFAs
                    inError = fa_alc.AllErrorsStatesIn(current_state)
                if inError:
                    current_state = self.__lastFinalStateReached
                    if len(word) > 0:
                        self.__UngetNextChar()
                    else:
                        # NOTE - capture one character wide errors (whitespaces)
                        word.append(c)
                        self.__wordRead = ''.join(word)
                    break
                if not inError or (inError and len(word)==0):
                    # NOTE - 'recognize' c if not in error
                    word.append(c)
                    self.__wordRead = ''.join(word)
            except EOFError as e:
                # NOTE - EOF and do not started reading a word. lineBuff='<EOF>'
                if len(word)==0:
                    emptyWordAndEOF = True
                # NOTE - finish reading the word right before EOF. lineBuff='mno<EOF>'
                # needed?
                # else:
                #     self.__UngetNextChar()
                # NOTE - abort while loop to check the state currently in
                break
        if emptyWordAndEOF:
            raise EOFError()
        else:
            self._check_for_input_rejection(current_state)
        return None

    def __GetNextChar(self) -> str:
        """
        Read next character from file.
        """
        # NOTE -  there is a character in buffer
        if self.__linePos < len(self.__lineBuff):
            self.__linePos += 1
            return self.__lineBuff[self.__linePos-1]
        else:
            return self.__GetNextLine()

    def __GetNextLine(self) -> str:
        """
        Read next line from file when the line buffer is empty.

        Print the line read if the scanner should echoLines.
        """
        # NOTE - read a chunk of text
        self.__lineBuff = self.__sourceFile.readline()
        # NOTE - chunk not empty (not EOF)
        if self.__lineBuff:
            self.__linePos = 1
            self.__lineNum += 1
            # NOTE - print if needed
            if self.__echoLines:
                self.__EchoLine()
            # NOTE - restart buffer pointer
            return self.__lineBuff[self.__linePos-1]
        else:
            raise EOFError()

    def __UngetNextChar(self) -> None:
        self.__linePos -= 1
        return

    def __EchoLine(self) -> None:
        return print(f'{self.__lineNum:>4}: {self.__lineBuff}', end='' if self.__lineBuff[-1:]=='\n' else '\n', file=self.__outTextFile)

    def __EchoToken(self, token: Token) -> None:
        return print(f'{self.__lineNum:>6}: {token}', file=self.__outTextFile)
