import abc
import copy

class SourcePosition:
    def __init__(self, source_name = None):
        self.character = -1
        self.line = 0
        self.source_name = source_name

    def advance(self, result):
        if result != None:
            if result == '\n':
                self.line += 1
                self.character = 0
            else:
                self.character += 1

    def represent(self, hl = None):
        hl_punct = hl['punct'] if (hl != None and 'punct' in hl) else ''
        hl_number = hl['number'] if (hl != None and 'number' in hl) else ''
        hl_string = hl['string'] if (hl != None and 'string' in hl) else ''
        hl_clear = hl['clear'] if (hl != None and 'clear' in hl) else ''

        sn = ''
        if self.source_name != None:
            sn = self.source_name + f'{hl_string}{hl_punct}:'
        return f'{sn}{hl_number}{self.line + 1}{hl_punct}:{hl_number}{self.character + 1}{hl_clear}'

    def __repr__(self):
        self.represent()

class Node:
    def __init__(self, begining, end):
        self.begining = copy.copy(begining)
        self.end = copy.copy(end)
        self.end.source_name = None

    def represent(self, indent, name = 'Node', hl = None):
        hl_punct = hl['punct'] if (hl != None and 'punct' in hl) else ''
        hl_number = hl['number'] if (hl != None and 'number' in hl) else ''
        hl_name = hl['name'] if (hl != None and 'name' in hl) else ''
        hl_clear = hl['clear'] if (hl != None and 'clear' in hl) else ''

        b = self.begining.represent(hl)
        e = self.end.represent(hl)

        return ('    ' * indent) + f'{b} {hl_punct}-{hl_clear} {e}{hl_punct}: {hl_name}{name}{hl_clear}\n'

    def __repr__(self):
        return self.represent(0)

class ChunkNode(Node):
    def __init__(self, begining, end, children = []):
        super().__init__(begining, end)
        self.children = children

    def represent(self, indent = 0, hl = None):
        result = super().represent(indent, 'Chunk', hl)
        for child in self.children:
            result += child.represent(indent + 1, hl)
        return result

class TagNode(Node):
    def __init__(self, begining, end, name, params = []):
        super().__init__(begining, end)
        self.name = name
        self.params = params

    def represent(self, indent = 0, hl = None):
        hl_punct = hl['punct'] if (hl != None and 'punct' in hl) else ''
        hl_string = hl['string'] if (hl != None and 'string' in hl) else ''
        hl_clear = hl['clear'] if (hl != None and 'clear' in hl) else ''

        result = super().represent(indent,
            f'Tag{hl_punct}({hl_string}{self.name}{hl_punct}){hl_clear}', hl
        )

        for param in self.params:
            result += '    ' * (indent + 1)
            if param.name != None:
                result += f'{hl_string}"{param.name}"{hl_clear}'
            else:
                result += f'{hl_punct}None{hl_clear}'
            result += '\n'
            result += param.value.represent(indent + 2, hl)
        return result


class Param():
    def __init__(self, name, value):
        self.name = name
        self.value = value

class TextNode(Node):
    def __init__(self, begining, end, value, raw):
        super().__init__(begining, end)
        self.value = value
        self.raw = raw

    def represent(self, indent = 0, hl = None):
        hl_punct = hl['punct'] if (hl != None and 'punct' in hl) else ''
        hl_string = hl['string'] if (hl != None and 'string' in hl) else ''
        hl_clear = hl['clear'] if (hl != None and 'clear' in hl) else ''

        return super().represent(indent,
            f'Text{hl_punct}({hl_string}{repr(self.value)}{hl_punct}){hl_clear}',
        hl)
