from .node import *
import sys

class Interpreter:
    def __init__(self):
        self.tag_heads = dict()
        self.defult_tag_head = None

        self.tag_tails = dict()
        self.defult_tag_tail = None

        self.text_handler = None

        self.params = dict()
        self.default_params = dict()
        self.defaultest_param = None

    def process(self, root):
        self.process_chunk(root)

    def process_chunk(self, chunk):
        for child in chunk.children:
            if type(child) == TextNode:
                self.process_text(child)
            else: # Assuming the interpretter is not broken, this must be a tag
                assert type(child) == TagNode
                self.process_tag(child)

    def process_text(self, node):
        if self.text_handler == None:
            print(f'No handler for text nodes.', sys.stderr)
            return
        self.text_handler(node.value, node.raw)

    def process_tag(self, node):
        if node.name in self.tag_heads:
            self.tag_heads[node.name](node.name)
        elif self.defult_tag_head != None:
            self.defult_tag_head(node.name)
        else:
            print(f'Unhandled tag head {node.name}.', sys.stderr)

        for param in node.params:
            is_chunk = type(param.value) == ChunkNode

            if (node.name, param.name) in self.params:
                self.params[(node.name, param.name)](node.name, param.name, is_chunk)
            elif node.name in self.default_params:
                self.default_params(node.name, param.name, is_chunk)
            elif self.defaultest_param != None:
                self.defaultest_param(node.name, param.name, is_chunk)
            else:
                print(f'Unhandled tag param {param.name} of {node.name}.', sys.stderr)

            if type(param.value) == TextNode:
                self.process_text(param.value)
            else:
                assert type(param.value) == ChunkNode
                self.process_chunk(param.value)


        if node.name in self.tag_tails:
            self.tag_tails[node.name](node.name)
        elif self.defult_tag_tail != None:
            self.defult_tag_tail(node.name)
        else:
            print(f'Unhandled tag tail {node.name}.', sys.stderr)

    def tag_head(self, param):
        if type(param) != str:
            self.defult_tag_head = param
            return param

        def apply(callable):
            self.tag_heads[param] = callable
            return callable
        return apply

    def tag_tail(self, param):
        if type(param) != str:
            self.defult_tag_tail = param
            return param

        def apply(callable):
            self.tag_tails[param] = callable
            return callable
        return apply

    def text(self, callback):
        self.text_handler = callback
        return callback

    # Very scuffed, but the API will be kinda nice.
    def param(self, first, second = False):
        if type(first != str):
            self.defaultest_param = first
            return first

        def apply(callable):
            if second == False:
                self.default_params[first] = callable
            else:
                self.default_params[(first, second)] = callable

            return callable

        return apply
