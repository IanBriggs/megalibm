import copy

from fpcore.ast import ASTNode, Atom, FPCore, Let, LetStar, Operation, Variable
from utils import add_method


class FPCoreNameError(Exception):
    """ variable is never defined in the FPCore """

    def __init__(self, name):
        self.name = name
        msg = f"name '{name}' is note defined in the FPCore"
        super(FPCoreNameError, self).__init__(msg)


@add_method(ASTNode)
def remove_let(self, *args, **kwargs):
    # Make sure calling remove_let leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"remove_let not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def remove_let(self, environment_stack):
    return self


@add_method(Variable)
def remove_let(self, environment_stack):
    # Lookup the variable starting with the innermost scope
    for environment in reversed(environment_stack[1:]):
        if self.source in environment:
            return copy.deepcopy(environment[self.source])
    if self.source in environment_stack[0]:
        return self
    raise FPCoreNameError(self.source)


@add_method(Operation)
def remove_let(self, environment_stack):
    self.args = [a.remove_let(environment_stack) for a in self.args]
    return self


@add_method(Let)
def remove_let(self, environment_stack):
    # let gives us a new scope and we can map all the bindings at the same time
    new_environment = {str(b.name): b.value.remove_let(environment_stack)
                       for b in self.bindings}
    environment_stack.append(new_environment)

    expr = self.body.remove_let(environment_stack)
    environment_stack.pop()

    return expr


@add_method(LetStar)
def remove_let(self, environment_stack):
    # let* gives us a new scope for each new binding
    for b in self.bindings:
        new_environment = {str(b.name): b.value.remove_let(environment_stack)}
        environment_stack.append(new_environment)

    expr = self.body.remove_let(environment_stack)
    for _ in self.bindings:
        environment_stack.pop()

    return expr


@add_method(FPCore)
def remove_let(self):
    inputs = {str(a): a for a in self.arguments}
    environment_stack = [inputs, ]
    new_body = self.body.remove_let(environment_stack)
    self.body = new_body
    assert (len(environment_stack) == 1)
