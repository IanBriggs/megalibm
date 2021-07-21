

from .expr import Expr

from utils import Logger


logger = Logger()




class Array(Expr):
    def __init__(self, items):
        super().__init__()
        self.items = items

    def __str__(self):
        items_str = list_to_str(self.items)
        this_str = "(array {})".format(items_str)
        return super().__str__().format(this_str)

    def __repr__(self):
        items_repr = list_to_repr(self.items)
        this_repr = "[{}]".format(items_repr)
        return super().__repr__().format(this_repr)
