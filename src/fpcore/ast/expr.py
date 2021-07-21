

from .ast_node import ASTNode
from .ast_utils import list_to_str, list_to_repr

from utils import Logger


logger = Logger()




class Expr(ASTNode):
    def __init__(self):
        super().__init__()
        self.properties = list()

    def add_properties(self, properties):
        self.properties.extend(properties)
        return self

    def __str__(self):
        if len(self.properties) == 0:
            return "{}"
        return "(! {} {{}})".format(list_to_str(self.properties))

    def __repr__(self):
        format_repr = super().__repr__()
        if len(self.properties) == 0:
            return format_repr
        props = list_to_repr(self.properties)
        prop_repr = ".add_properites([{}])".format(props)
        return format_repr + prop_repr
