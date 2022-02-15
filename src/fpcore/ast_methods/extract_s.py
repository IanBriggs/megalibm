

from fpcore.ast import ASTNode, Atom, Operation, FPCore
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def extract_s(self):
    # Make sure calling extract_s leads to an error if not overridden
    class_name = type(self).__name__
    msg = "extract_s not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(Atom)
def extract_s(self):
    return None

@add_method(Operation)
def extract_s(self):
    if self.op == "thefunc":
        return self.args[0].copy()
    for arg in self.args:
        inner = arg.extract_s()
        if inner != None:
            return inner
    assert False, "Unable to find 'thefunc'"

@add_method(FPCore)
def extract_s(self):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  self.body.extract_s())
