

from fpcore.ast import ASTNode, Atom, Operation, FPCore, Variable
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)




@add_method(ASTNode)
def cross(self, other):
    # Make sure calling cross leads to an error if not overridden
    class_name = type(self).__name__
    msg = "cross not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(Atom)
def cross(self, other):
    return self.copy()

@add_method(Operation)
def cross(self, other):
    if self.op == "thefunc":
        return other.substitute(Variable("x"), self.args[0])
    new_args = (arg.cross(other) for arg in self.args)
    return Operation(self.op, *new_args)

@add_method(FPCore)
def cross(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  self.body.cross(other))
