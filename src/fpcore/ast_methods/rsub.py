from fpcore.ast import ASTNode, Atom, FPCore, Operation
from fpcore.ast_methods.sub import typecase_and_sub
from utils import add_method


@add_method(ASTNode)
def __rsub__(self, *args, **kwargs):
    # Make sure calling __rsub__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"__rsub__ not implemented for class '{class_name}'".format(
        class_name)
    raise NotImplementedError(msg)


@add_method(Atom)
def __rsub__(self, other):
    return typecase_and_sub(other, self)


@add_method(Operation)
def __rsub__(self, other):
    return typecase_and_sub(other, self)


@add_method(FPCore)
def __rsub__(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  typecase_and_sub(other, self))
