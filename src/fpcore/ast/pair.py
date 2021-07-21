

from .ast_node import ASTNode

from utils import Logger


logger = Logger()




class Pair(ASTNode):
    def __init__(self, name, value):
        assert(type(name) == Variable)
        self.name = name
        self.value = value

    def __repr__(self):
        format_repr = super().__repr__()
        this_repr = list_to_repr((self.name, self.value))
        return format_repr.format(this_repr)
