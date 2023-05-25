from expect import expect_implemented
from fpcore.ast import ASTNode, Atom, FPCore, Operation, Variable
from utils import add_method


@add_method(ASTNode)
def cross(self, *args, **kwargs):
    expect_implemented("cross", self)


@add_method(Atom)
def cross(self, other):
    return self.copy()


@add_method(Operation)
def cross(self, other):
    if self.op == "thefunc":
        return other.substitute(Variable("x"), self.args[0])
    new_args = (arg.cross(other) for arg in self.args)
    return Operation(self.op, *new_args)


@add_method(FPCore)
def cross(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  self.body.cross(other))
