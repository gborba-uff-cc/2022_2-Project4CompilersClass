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
