'''
C- automata declaration
'''

import enum
import typing

import automata.fa.dfa as afd
import tools.toolbox as tt

# NOTE - alphabets
lowerLettersAlphabet: frozenset[str] = tt.CharRange('a','z')
upperLettersAlphabet: frozenset[str] = tt.CharRange('A','Z')
lettersAlphabet: frozenset[str] = lowerLettersAlphabet | upperLettersAlphabet
digitsAlphabet: frozenset[str] = tt.CharRange('0','9')
symbolsAlphabet: frozenset[str] = frozenset(s for s in '+-*/=<>!;,()[]{}')
blanks: frozenset[str] = frozenset(s for s in ' \t\v\f\r\n')
alphabet: frozenset[str] = lettersAlphabet | digitsAlphabet | symbolsAlphabet | blanks

@enum.unique
class CMinusDFAs(enum.Enum):
    Keywords = enum.auto()
    IdsOverlapingKeywords = enum.auto()
    Identifiers = enum.auto()
    Numbers = enum.auto()
    Comments = enum.auto()
    Operators = enum.auto()
    CMinus = enum.auto()


# NOTE - automata
def CreateDFAKeywords(MPrefix: str='MK_', errorState:str = 'error') -> afd.DFA:
    F: typing.Iterable[str] = []
    F.extend( (f'{MPrefix}f{i:02}' for i in range(1,7)) )

    Q: typing.Iterable[str] = []
    Q.extend( (f'{MPrefix}s{i:02}' for i in range(18)) )
    Q.append(f'{MPrefix}{errorState}')
    Q.extend(F)

    delta: dict[str, dict[str, str]] = {}
    delta.update(
        tt.ExpandDFATransitions(
            f'{MPrefix}s00', (
                ('i', f'{MPrefix}s01'),
                ('e', f'{MPrefix}s03'),
                ('v', f'{MPrefix}s06'),
                ('w', f'{MPrefix}s09'),
                ('r', f'{MPrefix}s13'),
            ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(
            f'{MPrefix}s01', (
                ('f', f'{MPrefix}f01'),
                ('n', f'{MPrefix}s02')
            ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s03', (('l', f'{MPrefix}s04'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s06', (('o', f'{MPrefix}s07'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s09', (('h', f'{MPrefix}s10'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s13', (('e', f'{MPrefix}s14'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f01', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s02', (('t', f'{MPrefix}f02'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s04', (('s', f'{MPrefix}s05'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s07', (('i', f'{MPrefix}s08'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s10', (('i', f'{MPrefix}s11'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s14', (('t', f'{MPrefix}s15'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f02', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s05', (('e', f'{MPrefix}f03'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s08', (('d', f'{MPrefix}f04'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s11', (('l', f'{MPrefix}s12'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s15', (('u', f'{MPrefix}s16'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f03', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f04', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s12', (('e', f'{MPrefix}f05'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s16', (('r', f'{MPrefix}s17'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f05', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s17', (('n', f'{MPrefix}f06'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f06', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}{errorState}', (), f'{MPrefix}{errorState}', alphabet))

    return afd.DFA(
        states=set(Q),
        input_symbols=set(map(tt.TranslateSymbols,alphabet)),
        transitions={qi:{tt.TranslateSymbols(si):qo for si,qo in d.items()} for qi,d in delta.items()},
        initial_state=Q[0],
        final_states=set(F))


def CreateDFAIdentifiersOverlapingKeywords(MPrefix: str='MI_', errorState:str = 'error') -> afd.DFA:
    F: typing.Iterable[str] = []
    F.append(f'{MPrefix}f01')

    Q: typing.Iterable[str] = []
    Q.extend([f'{MPrefix}s00', f'{MPrefix}{errorState}'])
    Q.extend(F)

    delta: dict[str, dict[str, str]] = {}
    delta.update(
        tt.ExpandDFATransitions(
            f'{MPrefix}s00',
            tuple(((s, f'{MPrefix}f01') for s in lettersAlphabet)),
            f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(
            f'{MPrefix}f01',
            tuple(((s, f'{MPrefix}f01') for s in lettersAlphabet)),
            f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}{errorState}', (), f'{MPrefix}{errorState}', alphabet))

    return afd.DFA(
        states=set(Q),
        input_symbols=set(map(tt.TranslateSymbols,alphabet)),
        transitions={qi:{tt.TranslateSymbols(si):qo for si,qo in d.items()} for qi,d in delta.items()},
        initial_state=Q[0],
        final_states=set(F))


def CreateDFAIdentifiers(
    MIOKPrefix: str='MI_',
    MIOKerrorState:str = 'error',
    MKPrefix: str='MK_',
    MKerrorState:str = 'error'
) -> afd.DFA:
    # (whi(l(e[A-Za-z]|[A-Za-df-z])|[A-Za-km-z])|(el(s(e[A-Za-z]|[A-Za-df-z])|[A-Za-rt-z])|((return|(i(nt|f)|void))[A-Za-z]|(re(t(ur[A-Za-mo-z]|(u[A-Za-qs-z]|[A-Za-tv-z]))|[A-Za-su-z])|(i(n[A-Za-su-z]|[A-Za-eg-mo-z])|(e[A-Za-km-z]|(r[A-Za-df-z]|(voi[A-Za-ce-z]|(v(o[A-Za-hj-z]|[A-Za-np-z])|(wh[A-Za-hj-z]|(w[A-Za-gi-z]|[A-Za-df-hj-qs-ux-z])))))))))))[A-Za-z]*|(whil?|(els?|(re(t(ur|u?))?|(in?|(e|(r|(voi|(vo?|(wh|w)))))))))
    ids = CreateDFAIdentifiersOverlapingKeywords(MIOKPrefix, MIOKerrorState).minify()
    compKw = CreateDFAKeywords(MKPrefix, MKerrorState).minify()
    return ids.intersection(~compKw,retain_names=True)


def CreateDFANumbers(MPrefix: str='MN_', errorState:str = 'error') -> afd.DFA:
    F: typing.Iterable[str] = []
    F.append(f'{MPrefix}f01')

    Q: typing.Iterable[str] = []
    Q.extend([f'{MPrefix}s00', f'{MPrefix}{errorState}'])
    Q.extend(F)

    delta: dict[str, dict[str, str]] = {}
    delta.update(
        tt.ExpandDFATransitions(
            f'{MPrefix}s00',
            tuple(((s, f'{MPrefix}f01') for s in digitsAlphabet)),
            f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(
            f'{MPrefix}f01',
            tuple(((s, f'{MPrefix}f01') for s in digitsAlphabet)),
            f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}{errorState}', (), f'{MPrefix}{errorState}', alphabet))

    return afd.DFA(
        states=set(Q),
        input_symbols=set(map(tt.TranslateSymbols,alphabet)),
        transitions={qi:{tt.TranslateSymbols(si):qo for si,qo in d.items()} for qi,d in delta.items()},
        initial_state=Q[0],
        final_states=set(F))


def CreateDFAComments(MPrefix: str='MC_', errorState:str = 'error') -> afd.DFA:
    F: typing.Iterable[str] = []
    F.append(f'{MPrefix}f01')

    Q: typing.Iterable[str] = []
    Q.extend( (f'{MPrefix}s{i:02}' for i in range(5)) )
    Q.append(f'{MPrefix}{errorState}')
    Q.extend(F)

    delta: dict[str, dict[str, str]] = {}
    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s00', (('/', f'{MPrefix}s01'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s01', (('*', f'{MPrefix}s02'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s02', (('*', f'{MPrefix}s03'), ), f'{MPrefix}s02', alphabet))

    delta.update(
        tt.ExpandDFATransitions(
            f'{MPrefix}s03', (
                ('*', f'{MPrefix}s03'),
                ('/', f'{MPrefix}f01')
            ), f'{MPrefix}s04', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s04', (('*', f'{MPrefix}s03'), ), f'{MPrefix}s04', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f01', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}{errorState}', (), f'{MPrefix}{errorState}', alphabet))

    return afd.DFA(
        states=set(Q),
        input_symbols=set(map(tt.TranslateSymbols,alphabet)),
        transitions={qi:{tt.TranslateSymbols(si):qo for si,qo in d.items()} for qi,d in delta.items()},
        initial_state=Q[0],
        final_states=set(F))


def CreateDFAOperators(MPrefix: str='MO_', errorState:str = 'error') -> afd.DFA:
    F: typing.Iterable[str] = []
    F.extend( (f'{MPrefix}f{i:02}' for i in range(1, 20)) )

    Q: typing.Iterable[str] = []
    Q.extend([f'{MPrefix}s00', f'{MPrefix}s01'])
    Q.append(f'{MPrefix}{errorState}')
    Q.extend(F)

    delta: dict[str, dict[str, str]] = {}
    delta.update(
        tt.ExpandDFATransitions(
            f'{MPrefix}s00', (
                ('+', f'{MPrefix}f01'),
                ('-', f'{MPrefix}f02'),
                ('*', f'{MPrefix}f03'),
                ('/', f'{MPrefix}f04'),
                ('<', f'{MPrefix}f05'),
                ('>', f'{MPrefix}f07'),
                ('=', f'{MPrefix}f09'),
                ('!', f'{MPrefix}s01'),
                (';', f'{MPrefix}f12'),
                (',', f'{MPrefix}f13'),
                ('(', f'{MPrefix}f14'),
                (')', f'{MPrefix}f15'),
                ('[', f'{MPrefix}f16'),
                (']', f'{MPrefix}f17'),
                ('{', f'{MPrefix}f18'),
                ('}', f'{MPrefix}f19'),
            ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f01', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f02', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f03', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f04', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f05', (('=', f'{MPrefix}f06'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f07', (('=', f'{MPrefix}f08'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f09', (('=', f'{MPrefix}f10'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}s01', (('=', f'{MPrefix}f11'), ), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f06', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f08', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f10', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f11', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f12', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f13', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f14', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f15', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f16', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f17', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f18', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}f19', (), f'{MPrefix}{errorState}', alphabet))

    delta.update(
        tt.ExpandDFATransitions(f'{MPrefix}{errorState}', (), f'{MPrefix}{errorState}', alphabet))

    return afd.DFA(
        states=set(Q),
        input_symbols=set(map(tt.TranslateSymbols,alphabet)),
        transitions={qi:{tt.TranslateSymbols(si):qo for si,qo in d.items()} for qi,d in delta.items()},
        initial_state=Q[0],
        final_states=set(F))


def AllErrorsStatesIn(state: str) -> bool:
    res = True
    old = state
    for q in errorsStates:
        new = old.replace(q,'')
        if new == old:
            res &= False
        old=new
    return res


prefixAndErrors: dict[CMinusDFAs, tuple[str, str]] = {
    CMinusDFAs.Keywords:('MK_','error'),
    CMinusDFAs.IdsOverlapingKeywords:('MIK_','error'),
    CMinusDFAs.Numbers:('MN_','error'),
    CMinusDFAs.Comments:('MC_','error'),
    CMinusDFAs.Operators:('MO_','error')}

errorsStates: frozenset[str] = frozenset(tuple(
    ''.join(v) for _,v in prefixAndErrors.items()))

dictCMinusDfas: dict[CMinusDFAs, afd.DFA] = {
    CMinusDFAs.Keywords: CreateDFAKeywords(
        *prefixAndErrors[CMinusDFAs.Keywords]),
    CMinusDFAs.Identifiers: CreateDFAIdentifiers(
        *prefixAndErrors[CMinusDFAs.IdsOverlapingKeywords],
        *prefixAndErrors[CMinusDFAs.Keywords]),
    CMinusDFAs.Numbers: CreateDFANumbers(
        *prefixAndErrors[CMinusDFAs.Numbers]),
    CMinusDFAs.Comments: CreateDFAComments(
        *prefixAndErrors[CMinusDFAs.Comments]),
    CMinusDFAs.Operators: CreateDFAOperators(
        *prefixAndErrors[CMinusDFAs.Operators])
}
dictCMinusDfas[CMinusDFAs.CMinus] = \
    dictCMinusDfas[CMinusDFAs.Keywords]\
    .union(dictCMinusDfas[CMinusDFAs.Identifiers], retain_names=True)\
    .union(dictCMinusDfas[CMinusDFAs.Numbers], retain_names= True)\
    .union(dictCMinusDfas[CMinusDFAs.Comments], retain_names= True)\
    .union(dictCMinusDfas[CMinusDFAs.Operators], retain_names= True)
