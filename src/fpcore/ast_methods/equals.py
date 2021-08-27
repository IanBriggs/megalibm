

from fpcore.ast import ASTNode, Atom, Operation, FPCore
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def __eq__(self, obj):
    # Make sure calling __eq__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = "__eq__ not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(Atom)
def __eq__(self, other):
    return type(self) == type(other) and self.source == other.source

@add_method(FPCore)
def __eq__(self, other):
    return (type(other) == FPCore
            and all(s_arg == o_arg for a_arg, o_arg
                    in zip(self.arguments, other.arguments))
            and all(s_prop == o_prop for a_prop, o_prop
                    in zip(self.properties, other.properties))
            and self.body == other.body)

@add_method(Operation)
def __eq__(self, other):
    return (type(other) == Operation
            and self.op == other.op
            and all(a_arg == o_arg for a_arg, o_arg
                    in zip(self.args, other.args)))
