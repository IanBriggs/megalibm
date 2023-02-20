from fpcore.ast import ASTNode, Constant, FPCore, Number, Operation, Variable
from utils import add_method


@add_method(ASTNode)
def __float__(self, *args, **kwargs):
    # Make sure calling __float__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"__float__ not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


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
