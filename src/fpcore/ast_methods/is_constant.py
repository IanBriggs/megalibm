from fpcore.ast import ASTNode, Atom, FPCore, Operation, Variable
from utils import add_method


@add_method(ASTNode)
def is_constant(self, *args, **kwargs):
    # Make sure calling is_constant leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"is_constant not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


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
