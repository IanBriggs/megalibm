from fpcore.ast import ASTNode, Constant, FPCore, Number, Operation, Variable
from utils import add_method


@add_method(ASTNode)
def copy(self, *args, **kwargs):
    # Make sure calling copy leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"copy not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Constant)
def copy(self):
    return Constant(self.source)


@add_method(Variable)
def copy(self):
    return Variable(self.source)


@add_method(Number)
def copy(self):
    return Number(self.source)


@add_method(Operation)
def copy(self):
    new_args = [arg.copy() for arg in self.args]
    return Operation(self.op, *new_args)


@add_method(FPCore)
def copy(self):
    return FPCore(self.name,
                  [a.copy() for a in self.arguments],
                  [p.copy() for p in self.properties],
                  self.body.copy())
