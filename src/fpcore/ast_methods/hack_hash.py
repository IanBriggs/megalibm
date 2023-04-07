from fpcore.ast import ASTNode, Atom, FPCore, Operation
from utils import add_method

# please forgive me
@add_method(ASTNode)
def __hash__(self):
    return str(self).__hash__()