from expect import expect_implemented
from fpcore.ast import ASTNode, Atom, FPCore, Operation
from utils import add_method

@add_method(ASTNode)
def substitute(self, *args, **kwargs):
    expect_implemented("substitute", self)


@add_method(Atom)
def substitute(self, old, new):
    if self == old:
        return new
    return self


@add_method(Operation)
def substitute(self, old, new):
    if self == old:
        return new
    new_args = [arg.substitute(old, new) for arg in self.args]
    return Operation(self.op, *new_args)


@add_method(FPCore)
def substitute(self, old, new):
    if self == old:
        return new
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  self.body.substitute(old, new))


