from fpcore.ast import ASTNode, Atom, FPCore, Operation
from fpcore.ast_methods.mul import typecase_and_mul
from utils import add_method


@add_method(ASTNode)
def __rmul__(self, *args, **kwargs):
    # Make sure calling __rmul__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"__rmul__ not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def __rmul__(self, other):
    return typecase_and_mul(other, self)


@add_method(Operation)
def __rmul__(self, other):
    return typecase_and_mul(other, self)


@add_method(FPCore)
def __rmul__(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  typecase_and_mul(other, self))
