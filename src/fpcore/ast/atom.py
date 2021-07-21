

from .expr import Expr
from .operation import Operation

from utils import Logger


logger = Logger()




class Atom(Expr):
    def __init__(self, source):
        super().__init__()
        self.source = source

    def __str__(self):
        format_str = super().__str__()
        return format_str.format(self.source)

    def __repr__(self):
        format_repr = super().__repr__()
        return format_repr.format(repr(self.source))

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.source == other.source)

    def __add__(self, other):
        return Operation("+", self, other)

    def __sub__(self, other):
        return Operation("-", self, other)

    def __neg__(self):
        return Operation("-", self)

    def substitute(self, old, new):
        if self == old:
            return new
        return self
