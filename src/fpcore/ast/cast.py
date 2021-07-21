

from .expr import Expr

from utils import Logger


logger = Logger()




class Cast(Expr):
    def __init__(self, body):
        super().__init__()
        self.body = body

    def __str__(self):
        format_str = super().__str__()
        this_str = "(cast {})".format(self.body)
        return format_str.format(this_str)

    def __repr__(self):
        format_repr = super().__repr__()
        this_repr = "{}".format(repr(self.body))
        return format_repr.format(this_repr)
