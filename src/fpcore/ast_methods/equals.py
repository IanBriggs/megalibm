from expect import expect_implemented
from fpcore.ast import ASTNode, Atom, FPCore, Operation
from utils import add_method


@add_method(ASTNode)
def __eq__(self, *args, **kwargs):
    expect_implemented("__eq__", self)


@add_method(Atom)
def __eq__(self, other):
    return type(self) == type(other) and self.source == other.source


@add_method(Operation)
def __eq__(self, other):
    return (type(other) == Operation
            and self.op == other.op
            and all(a_arg == o_arg for a_arg, o_arg
                    in zip(self.args, other.args)))


@add_method(FPCore)
def __eq__(self, other):
    return (type(other) == FPCore
            and all(s_arg == o_arg for s_arg, o_arg
                    in zip(self.arguments, other.arguments))
            and all(s_prop == o_prop for s_prop, o_prop
                    in zip(self.properties, other.properties))
            and self.body == other.body)
