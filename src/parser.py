import abc
import copy

from .node import *

class Parser(abc.ABC):

    def __init__(self, source_name = None):
        self.position = SourcePosition(source_name)

    @abc.abstractmethod
    def get_impl(self):
        """
        Get the next character or `None` if at the end of the file.
        This method is to be overriden by implementations.
        """
        pass

    @abc.abstractmethod
    def peek(self, n):
        pass

    def get(self):
        result = self.get_impl()
        if result != None:
            self.position.advance(result)
        return result

    def parse(self):
        return self.parse_chunk()

    def parse_chunk(self):
        children = []
        begining = copy.copy(self.position)
        begining.advance(self.peek(0))

        while True:
            next = self.peek(0)

            if next == None:
                return ChunkNode(begining, self.position, children)
            elif next == '[':
                next2 = self.peek(1)
                if next2 == '[':
                    children.append(self.parse_text())
                elif next2 in [ '"', ';', ':' ]:
                    return ChunkNode(begining, self.position, children)
                else:
                    children.append(self.parse_tag())
            else:
                children.append(self.parse_text())

    def parse_text(self):
        begining = copy.copy(self.position)
        begining.advance(self.peek(0))
        value = ""
        raw = ""

        while True:
            next = self.peek(0)
            next2 = self.peek(1)

            if (next == '[' and next2 != '[') or next == None:
                return TextNode(begining, self.position, value, raw)
            elif next in ['\\', '['] and next2 == '[':
                value += '['
                raw += next + '['
                self.get()
                self.get()
            else:
                v = self.get()
                value += v
                raw += v

    def parse_tag(self):
        begining = copy.copy(self.position)
        begining.advance(self.peek(0))
        name = ""
        params = []

        tmp = self.get() # just in case someone uses -O
        assert tmp == '[' # Chunk should take care of that...

        while self.peek(0) not in [':', '"', ';']:
            name += self.get()

        while True:
            kind = self.get()

            if kind == ';':
                self.get()
                return TagNode(begining, self.position, name, params)
            else:
                param_name = ''
                while self.peek(0) != ']':
                    param_name += self.get()
                self.get()
                if param_name == '':
                    param_name = None

                if kind == ':':
                    params.append(Param(param_name, self.parse_chunk()))
                else: # "
                    params.append(Param(param_name, self.parse_text()))

            if self.get() == None:
                return TagNode(begining, self.position, name, params)


class StringParser(Parser):

    def __init__(self, source):
        super().__init__('<string>')
        self.str_index = 0
        self.source = source

    def get_impl(self):
        if self.str_index >= len(self.source):
            return None

        result = self.source[self.str_index]
        self.str_index += 1
        return result

    def peek(self, n):
        if self.str_index + n >= len(self.source):
            return None

        return self.source[self.str_index + n]

from collections import deque
class FileParser(Parser):
    def __init__(self, path):
        super().__init__(path)
        self.file = open(path, 'r')
        self.done = False
        self.queue = deque()

    def read(self):
        if self.done:
            return False

        chunk = self.file.read(512)
        if len(chunk) < 512:
            self.file.close()
            self.done = True

        self.queue.extend(chunk)
        return True

    def get_impl(self):
        if len(self.queue) == 0:
            if not self.read():
                return None

        return self.queue.popleft()

    def peek(self, n):
        while len(self.queue) < n + 1:
            if not self.read():
                return None

        return self.queue[n]

