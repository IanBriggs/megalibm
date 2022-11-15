from fpcore.ast import ASTNode, Atom, FPCore, Operation
from utils import add_method


@add_method(ASTNode)
def contains_op(self, *args, **kwargs):
    # Make sure calling contains_op leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"contains_op not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def contains_op(self, target_op):
    return False


@add_method(Operation)
def contains_op(self, target_op):
    if self.op == target_op:
        return True
    return any(arg.contains_op(target_op) for arg in self.args)


@add_method(FPCore)
def contains_op(self, target_op):
    return self.body.contains_op(target_op)


