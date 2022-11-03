from fpcore.ast import ASTNode, Atom, FPCore, Number, Operation
from fpcore.ast_methods.truediv import typecase_and_divide
from utils import add_method


@add_method(ASTNode)
def __rtruediv__(self, *args, **kwargs):
    # Make sure calling __rtruediv__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"__rtruediv__ not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def __rtruediv__(self, other):
    return typecase_and_divide(other, self)


@add_method(Operation)
def __rtruediv__(self, other):
    return typecase_and_divide(other, self)


@add_method(FPCore)
def __rtruediv__(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  typecase_and_divide(other, self))
