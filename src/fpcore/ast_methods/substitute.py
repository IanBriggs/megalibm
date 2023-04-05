from fpcore.ast import ASTNode, Atom, FPCore, Operation
from utils import add_method

@add_method(ASTNode)
def substitute(self, *args, **kwargs):
    # Make sure calling substitute leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"substitute not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def substitute(self, old, new):
    if self == old:
        return new
    return self


@add_method(Operation)
def substitute(self, old, new):
    if self == old:
        return new
    new_args = [arg.substitute(old, new) for arg in self.args]
    return Operation(self.op, *new_args)


@add_method(FPCore)
def substitute(self, old, new):
    if self == old:
        return new
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  self.body.substitute(old, new))


