

from .atom import Atom

from utils import Logger


logger = Logger()




class Variable(Atom):
    def __init__(self, source):
        super().__init__(source)
        self.dimention = None

    def set_dimention(self, *dimention):
        self.dimention = dimention
        return self

    def __str__(self):
        if self.dimention is None:
            return super().__str__()
        this_str = "({} {})".format(self.source, list_to_str(self.dimention))
        return super(Expr).__str__().format(this_str)

    def __repr__(self):
        if self.dimention is None:
            return super().__repr__()
        dims = list_to_repr(self.dimention)
        dims_repr = ".set_dimention({})".format(list_to_str(self.dimention))
        return super(Expr).__repr__().format(self.source) + dims_repr
    
    def __float__(self):
        msg = "could not convert Variable to float: '{}'".format(repr(self))
        raise ValueError(msg)

    def to_wolfram(self):
        return self.source

    def to_sollya(self):
        return self.source

