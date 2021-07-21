

from .ast_node import ASTNode
from .operation import Operation
from .ast_utils import list_to_str, list_to_repr

from utils import Logger


logger = Logger()




class FPCore(ASTNode):
    def __init__(self, name, arguments, properties, body):
        super().__init__()
        self.name = name
        self.arguments = arguments
        self.properties = properties
        self.body = body

    def __str__(self):
        name_str = "" if self.name is None else self.name + " "
        arguments_str = list_to_str(self.arguments)
        properties_str = list_to_str(self.properties)
        return "(FPCore {}({}) {} {})".format(name_str,
                                              arguments_str,
                                              properties_str,
                                              self.body)

    def __repr__(self):
        arguments_repr = list_to_repr(self.arguments)
        properties_repr = list_to_repr(self.properties)
        this_repr = "{}, [{}], [{}], {}".format(repr(self.name),
                                                arguments_repr,
                                                properties_repr,
                                                repr(self.body))
        return super().__repr__().format(this_repr)

    def __eq__(self, other):
        return (type(other) == FPCore
                and all(s_arg == o_arg for a_arg, o_arg
                    in zip(self.arguments, other.arguments))
                and all(s_prop == o_prop for a_prop, o_prop
                    in zip(self.properties, other.properties))
                and self.body == other.body)

    def __sub__(self, other):
        return FPCore(self.name,
                      self.arguments,
                      self.properties,
                      Operation("-", self.body, other.body))

    def __add__(self, other):
        return FPCore(self.name,
                      self.arguments,
                      self.properties,
                      Operation("+", self.body, other.body))

    def __neg__(self):
        return FPCore(self.name,
                      self.arguments,
                      self.properties,
                      Operation("-", self.body))

    def __float__(self):
        return float(self.body)

    def substitute(self, old, new):
        return FPCore(self.name,
                      self.arguments,
                      self.properties,
                      self.body.substitute(old, new))

    def to_wolfram(self):
        return self.body.to_wolfram()

    def to_sollya(self):
        return self.body.to_sollya()
