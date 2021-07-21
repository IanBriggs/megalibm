

from .expr import Expr

from utils import Logger


logger = Logger()




class Tensor(Expr):
    def __init__(self, bindings, body):
        super().__init__()
        self.bindings = bindings
        self.body = body

    def __str__(self):
        bindings_str = list_to_str(self.bindings)
        this_str = "(tensor ({}) {})".format(bindings_str,
                                            self.body)
        return super().__str__().format(this_str)

    def __repr__(self):
        bindings_repr = list_to_repr(self.bindings)
        this_repr = "[{}], {}".format(bindings_repr,
                                      repr(self.body))
        return super().__repr__().format(this_repr)


