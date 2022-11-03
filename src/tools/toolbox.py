import typing


def CharRange(start: str, end: str) -> frozenset[str]:
    """
    Helper to get the characters between a range, like [a-z].
    """
    return frozenset( (chr(code) for code in range(ord(start), ord(end)+1)) )


def ExpandDFATransitions(
        qOrigin: str,
        # typing.Sequence[tuple[Symbol,State]]
        symbol_qNext: typing.Sequence[tuple[str,str]],
        qDefault: str,
        alphabet: set[str]|frozenset[str]
    # dict[tuple[State,Symbol]State]
    ) -> dict[str, dict[str,str]]:
    """
    Automate the creation of transitions (qOrigin,symbol)->qNext.

    `qOrigin` is the root state where transitions are leaving.

    `symbol_qNext` is a sequence with tuple dictating the transitions
    (qOrigin,symbol)->qNext.

    `qDefault` is the state where symbols outside `symbol_qNext` but in the
    `alphabet`, resulting in transitions (qOrigin,s)->qNext for every s not in
    the symbols of `symbol_qNext`.
    """
    # dict[tuple[State,Symbol],State]
    aux: dict[str, dict[str,str]] = {qOrigin: {}}
    symbolsIn: set[str] = set()
    for k, v in symbol_qNext:
        aux[qOrigin][k] = v
        symbolsIn.add(k)
    symbolsOut = alphabet - symbolsIn
    for k in symbolsOut:
        aux[qOrigin][k] = qDefault
    return aux


def SetNotation(iter: typing.Iterable[str]) -> str:
    return f'''{{'{"','".join(map(str,sorted(iter)))}'}}'''


# FIXME -
def TranslateSymbols(input: str, aToB_bToA: bool = True):
    return input
    __translationTable = ('*()','ΑΒΓ')
    relation = __translationTable if aToB_bToA else __translationTable[::-1]
    return input.translate(str.maketrans(*relation))
