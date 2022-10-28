import itertools
import typing


State: typing.TypeAlias = str
Symbol: typing.TypeAlias = str
DFATransitionFunction: typing.TypeAlias = dict[tuple[State, Symbol], State]
NFATransitionFunction: typing.TypeAlias = dict[tuple[State,Symbol], frozenset[State]]


class FA():
    def __init__(
        self,
        Q: typing.Iterable[State],
        Sigma: typing.Iterable[Symbol],
        q0: State,
        F: typing.Iterable[Symbol]
    ) -> None:
        self.Q: frozenset[State] = frozenset(Q)
        self.alphabet: frozenset[Symbol] = frozenset(Sigma)
        self.q0: State = q0
        self.F: frozenset[State] = frozenset(F)


class DFA(FA):
    def __init__(
        self,
        Q: typing.Iterable[State],
        Sigma: typing.Iterable[Symbol],
        delta: DFATransitionFunction,
        q0: State,
        F: typing.Iterable[Symbol]
    ) -> None:
        super().__init__(Q, Sigma, q0, F)
        self.delta: DFATransitionFunction = delta

    def accept(self, word: str) -> bool:
        cur_state = self.q0
        i_char = 0
        len_w = len(word)
        while i_char < len_w:
            cur_state = self.delta[cur_state, word[i_char]]
            i_char += 1
        # acceptance condition
        return (i_char == len(word)) and (cur_state in self.F)

