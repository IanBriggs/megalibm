

from .expr import Expr
from .ast_utils import list_to_str, list_to_repr

from utils import Logger


logger = Logger()




class Let(Expr):
    def __init__(self, bindings, body):
        super().__init__()
        self.bindings = bindings
        self.body = body

    def __str__(self):
        format_str = super().__str__()
        this_str = "(let ({}) {})".format(list_to_str(self.bindings),
                                          self.body)
        return format_str.format(this_str)

    def __repr__(self):
        format_repr = super().__repr__()
        this_repr = "[{}], {}".format(list_to_repr(self.bindings),
                                      repr(self.body))
        return format_repr.format(this_repr)
