from expect import expect_implemented
from fpcore.ast import ASTNode, Atom, FPCore, Operation, Variable
from utils import add_method


@add_method(ASTNode)
def is_constant(self, *args, **kwargs):
    expect_implemented("is_constant", self)


@add_method(Atom)
def is_constant(self):
    return True


@add_method(Variable)
def is_constant(self):
    return False


@add_method(Operation)
def is_constant(self):
    return all([arg.is_constant() for arg in self.args])


@add_method(FPCore)
def is_constant(self):
    return float(self.eval({}))
