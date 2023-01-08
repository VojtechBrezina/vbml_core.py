from . import parser
from . import node
from . import interpreter


def parse_string(source):
    return parser.StringParser(source).parse()

def parse_file(path):
    return parser.FileParser(path).parse()

if __name__ == '__main__':
    from .tests import *
    import unittest
    unittest.main()
