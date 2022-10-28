def CharRange(start: str, end: str) -> frozenset[str]:
    """
    Helper to get the characters between a range, like [a-z].
    """
    return frozenset( (chr(code) for code in range(ord(start), ord(end)+1)) )

