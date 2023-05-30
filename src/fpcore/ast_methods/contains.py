from expect import expect_implemented
from fpcore.ast import ASTNode, Atom, FPCore, Operation
from utils import add_method


@add_method(ASTNode)
def contains(self, *args, **kwargs):
    expect_implemented("contains", self)


@add_method(Atom)
def contains(self, target):
    return self == target


@add_method(Operation)
def contains(self, target):
    if self == target:
        return True
    return any(arg.contains(target) for arg in self.args)


@add_method(FPCore)
def contains(self, target):
    return self.body.contains(target)


