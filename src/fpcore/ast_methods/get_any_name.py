

from fpcore.ast import ASTNode, FPCore
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def get_any_name(self, *args, **kwargs):
    # Make sure calling get_any_name leads to an error if not overridden
    class_name = type(self).__name__
    msg = "get_any_name not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)


@add_method(FPCore)
def get_any_name(self):
    if self.name != None:
        return self.name
    for p in self.properties:
        if p.name == "name":
            return p.value
    return None
