

from .expr import Expr
from .ast_utils import list_to_str, list_to_repr

from utils import Logger


logger = Logger()




class While(Expr):
    def __init__(self, cond, update_bindings, body):
        super().__init__()
        self.cond = cond
        self.update_bindings = update_bindings
        self.body = body

    def __str__(self):
        format_str = super().__str__()
        bindings_str = list_to_str(self.update_bindings)
        this_str = "(while {} ({}) {})".format(self.cond,
                                               bindings_str,
                                               self.body)
        return format_str.format(this_str)

    def __repr__(self):
        format_repr = super().__repr__()
        this_repr = "{}, [{}], {}".format(repr(self.cond),
                                          list_to_repr(self.update_bindings),
                                          repr(self.body))
        return format_repr.format(this_repr)
