

from .expr import Expr

from utils import Logger


logger = Logger()




class If(Expr):
    def __init__(self, cond, true, false):
        super().__init__()
        self.cond = cond
        self.true = true
        self.false = false

    def __str__(self):
        format_str = super().__str__()
        this_str = "(if {} {} {})".format(self.cond, self.true, self.false)
        return format_str.format(this_str)

    def __repr__(self):
        format_repr = super().__repr__()
        this_repr = "{}, {}, {}".format(repr(self.cond),
                                        repr(self.true),
                                        repr(self.false))
        return format_repr.format(this_repr)
