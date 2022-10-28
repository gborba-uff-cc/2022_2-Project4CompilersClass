import typing

def CharRange(start: str, end: str) -> frozenset[str]:
    """
    Helper to get the characters between a range, like [a-z].
    """
    return frozenset( (chr(code) for code in range(ord(start), ord(end)+1)) )

def ExpandDFATransitions(
        qOrigin: str,
        symbol_qNext: typing.Sequence[tuple[str,str]],
        qDefault: str,
        alphabet: set[str]|frozenset[str]) -> dict[tuple[str,str],str]:
    """
    Automate the creation of transitions (qOrigin,symbol)->qNext.

    `qOrigin` is the root state where transitions are leaving.

    `symbol_qNext` is a sequence with tuple dictating the transitions
    (qOrigin,symbol)->qNext.

    `qDefault` is the state where symbols outside `symbol_qNext` but in the
    `alphabet`, resulting in transitions (qOrigin,s)->qNext for every s not in
    the symbols of `symbol_qNext`.
    """
    aux: dict[tuple[str,str],str] = {}
    symbolsIn: set[str] = set()
    for s, t in symbol_qNext:
        aux[qOrigin, s] = t
        symbolsIn.add(s)
    symbolsOut = alphabet - symbolsIn
    for s in symbolsOut:
        aux[qOrigin, s] = qDefault
    return aux
