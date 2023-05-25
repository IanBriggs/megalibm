from expect import expect_implemented
from fpcore.ast import ASTNode, Constant, FPCore, Number, Operation, Variable
from utils import add_method


@add_method(ASTNode)
def __float__(self, *args, **kwargs):
    expect_implemented("__float__", self)


@add_method(Constant)
def __float__(self):
    return float(self.eval({}))


@add_method(Variable)
def __float__(self):
    msg = f"can not convert Variable to float: '{repr(self)}'"
    raise ValueError(msg)


@add_method(Number)
def __float__(self):
    return float(self.eval({}))


@add_method(Operation)
def __float__(self):
    return float(self.eval({}))


@add_method(FPCore)
def __float__(self):
    return float(self.eval({}))
