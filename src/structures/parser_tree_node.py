import io
import structures.token as st


class ParserTreeNode():
    def __init__(self, value: str|st.Token) -> None:
        self.nodes: list['ParserTreeNode'] = []
        self.value: str|st.Token = value
        return None

    def AddNode(self, aNode: 'ParserTreeNode') -> None:
        # NOTE - production rule (function)
        if (isinstance(aNode.value, str) and (not aNode.nodes)):
            return None

        self.nodes.append(aNode)
        return None

    def NodeText(self) -> str:
        content = self.__NodeText(0)
        return content

    def __NodeText(self, indentLevel: int):
        buffer: io.StringIO = io.StringIO()
        text: str = ''

        if isinstance(self.value, str):
            text = self.value
        else:
            text = f'{self.value.type.name}: {self.value.value}'
        buffer.write(f'{"":<{indentLevel}}{text}\n')

        for childs in self.nodes:
            childNode = childs.__NodeText(indentLevel+1)
            buffer.write(childNode)
        content = buffer.getvalue()

        buffer.close()
        return content

    def ClearNode(self) -> None:
        self.nodes.clear()
        return None
