'''
C- automata declaration
'''

import typing

import tools.toolbox as tt

import finite_automaton.finite_automaton as fa

# NOTE - alphabets
lowerLettersAlphabet: frozenset[fa.Symbol] = tt.CharRange('a','z')
upperLettersAlphabet: frozenset[fa.Symbol] = tt.CharRange('A','Z')
lettersAlphabet: frozenset[fa.Symbol] = lowerLettersAlphabet | upperLettersAlphabet
digitsAlphabet: frozenset[fa.Symbol] = tt.CharRange('0','9')
symbolsAlphabet: frozenset[fa.Symbol] = frozenset(s for s in '+-*/=<>!;,()[]{}')
blanks: frozenset[fa.Symbol] = frozenset(s for s in ' \t\v\f\r\n')
alphabet: frozenset[fa.Symbol] = lettersAlphabet | digitsAlphabet | symbolsAlphabet | blanks


# NOTE - automata
def CreateDFAKeywords() -> fa.DFA:
    F: typing.Iterable[fa.State] = []
    F.extend( (f'f{i:02}' for i in range(1,7)) )

    Q: typing.Iterable[fa.Symbol] = []
    Q.extend( (f's{i:02}' for i in range(18)) )
    Q.append('empty')
    Q.extend(F)

    delta = {}

    delta.update(
        tt.ExpandDFATransitions(
            's00', (
                ('i', 's01'),
                ('e', 's03'),
                ('v', 's06'),
                ('w', 's09'),
                ('r', 's13'),
            ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions(
            's01', (
                ('f', 'f01'),
                ('n', 's02')
            ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s03', (('l', 's04'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s06', (('o', 's07'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s09', (('h', 's10'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s13', (('e', 's14'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f01', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s02', (('t', 'f02'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s04', (('s', 's05'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s07', (('i', 's08'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s10', (('i', 's11'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s14', (('t', 's15'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f02', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s05', (('e', 'f03'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s08', (('d', 'f04'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s11', (('l', 's12'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s15', (('u', 's16'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f03', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f04', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s12', (('e', 'f05'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s16', (('r', 's17'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f05', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s17', (('n', 'f06'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f06', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('empty', (), 'empty', alphabet))

    return fa.DFA(
        Q=Q,
        Sigma=alphabet,
        delta=delta,
        q0=Q[0],
        F=F)


def CreateDFAIdentifiersOverlapingKeywords() -> fa.DFA:
    F: typing.Iterable[fa.State] = []
    F.append('f01')

    Q: typing.Iterable[fa.Symbol] = []
    Q.extend(['s00', 'empty'])
    Q.extend(F)

    delta = {}
    delta.update(
        tt.ExpandDFATransitions(
            's00',
            tuple(((s, 'f01') for s in lettersAlphabet)),
            'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions(
            'f01',
            tuple(((s, 'f01') for s in lettersAlphabet)),
            'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('empty', (), 'empty', alphabet))

    return fa.DFA(
        Q=Q,
        Sigma=alphabet,
        delta=delta,
        q0=Q[0],
        F=F)


def CreateDFANumbers() -> fa.DFA:
    F: typing.Iterable[fa.State] = []
    F.append('f01')

    Q: typing.Iterable[fa.Symbol] = []
    Q.extend(['s00', 'empty'])
    Q.extend(F)

    delta = {}
    delta.update(
        tt.ExpandDFATransitions(
            's00',
            tuple(((s, 'f01') for s in digitsAlphabet)),
            'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions(
            'f01',
            tuple(((s, 'f01') for s in digitsAlphabet)),
            'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('empty', (), 'empty', alphabet))

    return fa.DFA(
        Q=Q,
        Sigma=alphabet,
        delta=delta,
        q0=Q[0],
        F=F)


def CreateDFAComments() -> fa.DFA:
    F: typing.Iterable[fa.State] = []
    F.append('f01')

    Q: typing.Iterable[fa.Symbol] = []
    Q.extend( (f's{i:02}' for i in range(5)) )
    Q.append('empty')
    Q.extend(F)

    delta = {}
    delta.update(
        tt.ExpandDFATransitions('s00', (('/', 's01'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s01', (('*', 's02'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s02', (('*', 's03'), ), 's02', alphabet))

    delta.update(
        tt.ExpandDFATransitions(
            's03', (
                ('*', 's03'),
                ('/', 'f01')
            ), 's04', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s04', (('*', 's03'), ), 's04', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f01', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('empty', (), 'empty', alphabet))

    return fa.DFA(
        Q=Q,
        Sigma=alphabet,
        delta=delta,
        q0=Q[0],
        F=F)


def CreateDFAOperators() -> fa.DFA:
    F: typing.Iterable[fa.State] = []
    F.extend( (f'f{i:02}' for i in range(1, 20)) )

    Q: typing.Iterable[fa.Symbol] = []
    Q.extend(['s00', 's01'])
    Q.append('empty')

    delta = {}
    delta.update(
        tt.ExpandDFATransitions(
            's00', (
                ('+', 'f01'),
                ('-', 'f02'),
                ('*', 'f03'),
                ('/', 'f04'),
                ('<', 'f05'),
                ('>', 'f07'),
                ('=', 'f09'),
                ('!', 's01'),
                (';', 'f12'),
                (',', 'f13'),
                ('(', 'f14'),
                (')', 'f15'),
                ('[', 'f16'),
                (']', 'f17'),
                ('{', 'f18'),
                ('}', 'f19'),
            ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f01', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f02', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f03', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f04', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f05', (('=', 'f06'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f07', (('=', 'f08'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f09', (('=', 'f10'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('s01', (('=', 'f11'), ), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f06', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f08', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f10', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f11', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f12', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f13', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f14', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f15', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f16', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f17', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f18', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('f19', (), 'empty', alphabet))

    delta.update(
        tt.ExpandDFATransitions('empty', (), 'empty', alphabet))

    return fa.DFA(
        Q=Q,
        Sigma=alphabet,
        delta=delta,
        q0=Q[0],
        F=F)
