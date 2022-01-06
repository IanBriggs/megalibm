

from fpcore.ast import (ASTNode, Atom, FPCore, Let, LetStar, Operation,
                               Variable)
from utils import add_method, Logger

import copy

logger = Logger(level=Logger.EXTRA)


class FPCoreNameError(Exception):
    def __init__(self, name):
        logger.error("No definition for variable: {}", name)
        self.name = name


@add_method(ASTNode)
def remove_let(self, environment_stack):
    # Make sure calling remove_let leads to an error if not overridden
    class_name = type(self).__name__
    msg = "remove_let not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)


@add_method(Atom)
def remove_let(self, environment_stack):
    return self


@add_method(Variable)
def remove_let(self, environment_stack):
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
    new_environment = {str(b.name): b.value.remove_let(environment_stack)
                       for b in self.bindings}
    environment_stack.append(new_environment)
    expr = self.body.remove_let(environment_stack)
    environment_stack.pop()
    return expr


@add_method(LetStar)
def remove_let(self, environment_stack):
    for b in self.bindings:
        new_environment = {str(b.name): b.value.remove_let(environment_stack)}
        environment_stack.append(new_environment)

    expr = self.body.remove_let(environment_stack)
    for _ in self.bindings:
        environment_stack.pop()

    return expr


@add_method(FPCore)
def remove_let(self):
    inputs = {str(a):a for a in self.arguments}
    environment_stack = [inputs,]
    new_body = self.body.remove_let(environment_stack)
    self.body = new_body
    assert(len(environment_stack) == 1)




def main(argv):
    logger.set_log_level(Logger.EXTRA)

    if len(argv) == 1:
        text = sys.stdin.read()
    elif len(argv) == 2:
        with open(argv[1], "r") as f:
            text = f.read()
    if text.strip() == "":
        text = "(FPCore (x) :pre (<= 1/100 x 1/2) (/ (- (exp x) 1) x))"

    logger.blog("Input text", text)

    parsed = parse(text)[0]
    parsed.remove_let()

    logger.blog("Removed lets", parsed)


if __name__ == "__main__":
    from fpcore.parser import parse
    import sys

    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
