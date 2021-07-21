

from .expr import Expr
from .ast_utils import list_to_str, list_to_repr

from utils import Logger


logger = Logger()




class For(Expr):
    def __init__(self, bindings, update_bindings, body):
        super().__init__()
        self.bindings = bindings
        self.update_bindings = update_bindings
        self.body = body

    def __str__(self):
        bindings_str = list_to_str(self.bindings)
        update_bindings_str = list_to_str(self.update_bindings)
        this_str = "(for ({}) ({}) {})".format(bindings_str,
                                               update_bindings_str,
                                               self.body)
        return super().__str__().format(this_str)

    def __repr__(self):
        bindings_repr = list_to_repr(self.bindings)
        update_bindings_repr = list_to_repr(self.update_bindings)
        this_repr = "[{}], [{}], {}".format(bindings_repr,
                                            update_bindings_repr,
                                            repr(self.body))
        return super().__repr__().format(this_repr)
