from fpcore.ast import ASTNode, Atom, FPCore, Number, Operation
from utils import add_method


def typecase_and_lt(a, b):
    # Extract body expressions of FPCores
    if type(a) == FPCore:
        a = a.body
    if type(b) == FPCore:
        b = b.body

    # Force number types into AST nodes
    if type(a) in {int, float}:
        a = Number(str(a))
    if type(b) in {int, float}:
        b = Number(str(b))

    # This will fail for non-numeric expressions
    return float(a) < float(b)


@add_method(ASTNode)
def __lt__(self, *args, **kwargs):
    # Make sure calling __lt__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"__lt__ not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def __lt__(self, other):
    return typecase_and_lt(self, other)


@add_method(Operation)
def __lt__(self, other):
    return typecase_and_lt(self, other)


@add_method(FPCore)
def __lt__(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  typecase_and_lt(self, other))
