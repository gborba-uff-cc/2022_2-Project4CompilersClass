import copy
import io
import typing

import automata.base.exceptions as abe
import automata.fa.dfa as afd
import finite_automaton.automaton_language_cminus as fa_alc
import tools.toolbox as tt
import structures.token as st


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
        self.__lineNum: int = -1
        self.__linePos: int = -1
        self.__lineBuff: str = ''
        self.__wordRead:str = ''
        self.__wordLine = 0
        self.__wordColumn = 0
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

    def GetToken(self) -> st.Token:
        """
        Return the position (line, column) and the next token read from the
        file, one token per call.

        Echoing the positions and raws read tokens if echoTrace if needed.
        """
        self.__wordRead = ''
        tokenType: st.TokenType = st.TokenType.ERROR
        tokenValue: str = ''

        # NOTE - run automaton
        try:
            self.__ScanInputStepwise()
            tokenValue = self.__wordRead
            tokenType = self.IdentifyTokenTypeByValue(tokenValue)
        except EOFError:
            tokenType = st.TokenType.EOF
            tokenValue = ''
        except abe.RejectionException:
            tokenType = st.TokenType.ERROR
            tokenValue = self.__wordRead

        token: st.Token = st.Token(tokenType, tokenValue, self.__wordLine+1, self.__wordColumn+1)
        if self.__echoTrace:
            self.__EchoToken(token)
        return token

    def IdentifyTokenTypeByValue(self, value: str) -> st.TokenType:
        tokenType = st.TokenType.ERROR
        for dfaType, M in fa_alc.dictCMinusDfas.items():
            if dfaType in {fa_alc.CMinusDFAs.Identifiers, fa_alc.CMinusDFAs.Numbers} and \
                M.accepts_input(value):
                    if dfaType is fa_alc.CMinusDFAs.Identifiers:
                        return st.TokenType.ID
                    else:
                        return st.TokenType.NUM
        for tt in st.TokenType:
            if value == tt.value:
                return tt
        return tokenType

    def __ScanInputStepwise(self) -> None:
        """
        Read character by character from the file until the word read is valid.
        """
        word = []
        self.__lastFinalStateReached = ''
        current_state = self.initial_state
        inError = False
        emptyWordAndEOF = False
        wordLine = -1
        wordColumn = -1

        while True:
            try:
                c = self.__GetNextChar()
                if wordLine == -1 and wordColumn == -1:
                    wordLine = self.__lineNum
                    wordColumn = self.__linePos

                input_symbol = tt.TranslateSymbols(c)
                current_state = self._get_next_current_state(current_state, input_symbol)

                # NOTE - 'recognize' c
                word.append(c)

                if current_state in self.final_states:
                    self.__lastFinalStateReached = current_state
                else:
                    # NOTE - in error estate if current state represents the
                    # error states of all DFAs
                    inError = fa_alc.AllErrorsStatesIn(current_state)

                if inError:
                    current_state = self.__lastFinalStateReached
                    if len(word) > 1:
                        self.__UngetNextChar()
                        word.pop()
                    break
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

        self.__wordRead = ''.join(word)
        self.__wordLine = wordLine
        self.__wordColumn = wordColumn

        if emptyWordAndEOF:
            raise EOFError()
        else:
            self._check_for_input_rejection(current_state)
        return None

    def __GetNextChar(self) -> str:
        """
        Read next character from file.
        """
        while True:
            if self.__lineBuff and self.__linePos+1 < len(self.__lineBuff):
                self.__linePos += 1
                return self.__lineBuff[self.__linePos]
            self.__GetNextLine()

    def __GetNextLine(self) -> None:
        """
        Read next line from file when the line buffer is empty.

        Print the line read if the scanner should echoLines.
        """
        # NOTE - read a chunk of text
        self.__lineBuff = self.__sourceFile.readline()
        # NOTE - chunk not empty (not EOF)
        if self.__lineBuff:
            self.__lineNum += 1
            # NOTE - restart buffer pointer
            self.__linePos = -1
            # NOTE - print if needed
            if self.__echoLines:
                self.__EchoLine(self.__lineNum+1, self.__lineBuff)
            return None
        else:
            raise EOFError()

    def __UngetNextChar(self) -> None:
        if self.__linePos < 0:
            return
        self.__linePos -= 1
        return None

    def __EchoLine(self, lineno: int, line: str) -> None:
        return print(f'{lineno:>4}: {line}', end='' if line[-1:]=='\n' else '\n', file=self.__outTextFile)

    def __EchoToken(self, token: st.Token) -> None:
        return print(f'{token.lineNo:>6}.{token.columnNo:>02}: {token}', file=self.__outTextFile)
