from fpcore.ast import ASTNode, Atom, FPCore, Operation, Variable
from utils import add_method


@add_method(ASTNode)
def get_variables(self, *args, **kwargs) -> set[str]:
    # Make sure calling get_variables leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"get_variables not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def get_variables(self):
    return set()


@add_method(Variable)
def get_variables(self):
    return {self.source}


@add_method(Operation)
def get_variables(self):
    arg_sets = (a.get_variables() for a in self.args)
    return set.union(*arg_sets)


@add_method(FPCore)
def get_variables(self):
    return self.body.get_variables(target_op)
