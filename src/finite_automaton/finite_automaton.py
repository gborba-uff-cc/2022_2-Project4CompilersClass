'''
DFA definition and some DFA operations
'''

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

    def Accept(self, word: str) -> bool:
        cur_state = self.q0
        i_char = 0
        len_w = len(word)
        while i_char < len_w:
            cur_state = self.delta[cur_state, word[i_char]]
            i_char += 1
        # acceptance condition
        return (i_char == len(word)) and (cur_state in self.F)

    def Complement(self) -> 'DFA':
        return DFA(
            Q=self.Q,
            Sigma=self.alphabet,
            delta=self.delta,
            q0=self.q0,
            F=self.Q - self.F
        )

    def Intersection(self, other: 'DFA'):
        """
        both FA should have the same alphabet.
        """
        if len(self.alphabet ^ other.alphabet) != 0:
            RuntimeError("can't do intersection, alphabets are different")

        newQ, newDelta = self.__IntersectionAndUnionCommon(other)
        Q = frozenset(map(str, newQ))
        q0=str((self.q0,other.q0))
        F = frozenset(
            (str(pair) for pair in itertools.product(self.F, other.F)))
        return DFA(
            Q=Q,
            Sigma=self.alphabet,
            delta=newDelta,
            q0=q0,
            F=F
        )

    def Union(self, other: 'DFA'):
        """
        both FA should have the same alphabet.
        """
        if len(self.alphabet ^ other.alphabet) != 0:
            RuntimeError("can't do union, alphabets are different")

        newQ, newDelta = self.__IntersectionAndUnionCommon(other)
        Q = frozenset(map(str, newQ))
        q0=str((self.q0,other.q0))
        aux = []
        aux.extend([str(pair) for pair in itertools.product(self.F, other.Q)])
        aux.extend([str(pair) for pair in itertools.product(self.Q, other.F)])
        F = frozenset(aux)
        return DFA(
            Q=Q,
            Sigma=self.alphabet,
            delta=newDelta,
            q0=q0,
            F=F
        )

    def __IntersectionAndUnionCommon(
            self,
            other: 'DFA'
        ) -> tuple[typing.Iterable[tuple[State,State]], DFATransitionFunction]:
        Q = list((
            pair for pair in itertools.product(self.Q, other.Q)))
        delta: DFATransitionFunction = {}
        for ((m1q, m2q), symbol) in itertools.product(Q, self.alphabet):
            v = (
                self.delta[m1q, symbol],
                other.delta[m2q, symbol]
            )
            k = (m1q, m2q)
            delta[(str(k), symbol)] = str(v)
        return (Q, delta)


if __name__ == '__main__':
    def CreateDFA2aExactly():
        return DFA(
            Q=set('q1 q2 q3 q4'.split()),
            Sigma=set('a b'.split()),
            delta={
                ('q1', 'a'): 'q2',
                ('q1', 'b'): 'q1',
                ('q2', 'a'): 'q3',
                ('q2', 'b'): 'q2',
                ('q3', 'a'): 'q4',
                ('q3', 'b'): 'q3',
                ('q4', 'a'): 'q4',
                ('q4', 'b'): 'q4',
            },
            q0='q1',
            F={'q3'}
        )

    def CreateDFA2bAtLeast():
        return DFA(
            Q=set('s1 s2 s3'.split()),
            Sigma=set('a b'.split()),
            delta={
                ('s1', 'a'): 's1',
                ('s1', 'b'): 's2',
                ('s2', 'a'): 's2',
                ('s2', 'b'): 's3',
                ('s3', 'a'): 's3',
                ('s3', 'b'): 's3',
            },
            q0='s1',
            F={'s3'}
        )

    M1 = CreateDFA2aExactly()
    M2 = CreateDFA2bAtLeast()
    M3 = M2.Complement()
    M4 = M1.Union(M2)
    M5 = M1.Intersection(M2)

    for i, M in enumerate((M1, M2, M3, M4, M5), start=1):
        print()
        for w in ('a aa b bb bbb abba aab bbba babab abbbbaa'.split()+['']):
            print(f'''M{i}.Accept('{w}')={M.Accept(w)}''')
