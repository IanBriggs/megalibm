

from fpcore.ast import ASTNode, Atom, Operation, FPCore
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def substitute(self, *args, **kwargs):
    # Make sure calling substitute leads to an error if not overridden
    class_name = type(self).__name__
    msg = "substitute not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)


@add_method(Atom)
def substitute(self, old, new):
    if self == old:
        return new
    return self


@add_method(FPCore)
def substitute(self, old, new):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  self.body.substitute(old, new))


@add_method(Operation)
def substitute(self, old, new):
    if self == old:
        return new
    new_args = [arg.substitute(old, new) for arg in self.args]
    return Operation(self.op, *new_args)
