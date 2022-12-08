import dataclasses
import enum
import structures.token as st
import typing

@enum.unique
class _IdType(enum.Enum):
    ARRAY = enum.auto()
    VARIABLE = enum.auto()
    FUNCTION = enum.auto()

_IdName: typing.TypeAlias = str
_IdDataType: typing.TypeAlias = str


class IdInUse(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class IdNotInUse(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)



class SymbolTableEntry():
    def __init__(self, idType: _IdType, idDataType: _IdDataType) -> None:
        self.idType: _IdType
        self.idDataType: _IdDataType
        return None


class SymbolTable():
    def __init__(self) -> None:
        self.__table: dict[_IdName, SymbolTableEntry] = {}
        self.__outterTable: typing.Union['SymbolTable', None] = None
        return None

# to implement nested scopes and the most closely nested scopes and the most
# closely nested rule the symbol table insert operation must not overwrite
# previous declarations, but temporaly hide them, so that the lookup operation
# only finds the most recently inserted declaration for the name
    def __Insert(
        self,
        IdType: _IdType,
        IdDataType: _IdDataType,
        id: str
    ) -> None:
        """
        Can raise IdInUse
        """
        try:
            self.LookupThisScope(id)
            raise IdInUse()
        except IdNotInUse:
            self.__table[id] = SymbolTableEntry(IdType, IdDataType)
        return None

    def InsertVariable(
        self,
        IdDataType: str,
        id: str
    ) -> None:
        return self.__Insert(_IdType.VARIABLE, IdDataType, id)

    def InsertArray(
        self,
        IdDataType: str,
        id: str
    ) -> None:
        return self.__Insert(_IdType.ARRAY, IdDataType, id)

    def InsertFunction(
        self,
        IdDataType: str,
        id: str
    ) -> None:
        return self.__Insert(_IdType.FUNCTION, IdDataType, id)

    # def Delete(self, id: str):
    #     return None

    def LookupThisScope(self, id: str):
        """
        Can raise IdNotInUse
        """
        try:
            return self.__table[id]
        except KeyError:
            raise IdNotInUse()

    def LookupAllScopes(self, id: str):
        """
        Can raise IdNotInUse
        """
        scope = self
        while scope:
            try:
                return scope.__table[id]
            except KeyError:
                scope = scope.__outterTable
        raise IdNotInUse()

    def InitInnerScope(self):
        """
        Set a symbol table to the inner scope of this symbol table and return it
        """
        inner = SymbolTable()
        inner.__outterTable = self
        return inner

    def DropThisScope(self) -> 'SymbolTable':
        """
        Drop this symbol table and return the outter scope table of self or
        self if an outter scope table don't exists
        """
        outter = self.__outterTable

        if outter is None:
            return self

        del self
        return outter

