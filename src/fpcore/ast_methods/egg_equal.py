from fpcore.ast import ASTNode, Atom, FPCore, Number, Operation
from utils import add_method
import snake_egg
import snake_egg_rules


def typecast_and_check_equality(a, b):
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

    # Error if no AST Nodes
    if not issubclass(type(a), ASTNode):
        msg = "FPCore does not support equality by type '{}' (value = {})"
        raise TypeError(msg.format(type(a), a))
    if not issubclass(type(b), ASTNode):
        msg = "FPCore does not support equality by type '{}' (value = {})"
        raise TypeError(msg.format(type(b), a))

    egraph = snake_egg.EGraph(snake_egg_rules.eval)
    a = a.to_snake_egg(to_rule=False)
    b = b.to_snake_egg(to_rule=False)
    egraph.add(a)
    egraph.add(b)
    egraph.run(snake_egg_rules.rules,
               iter_limit=20,
               time_limit=600,
               node_limit=2_000_000_000,
               use_simple_scheduler=False)
    id_a = egraph.add(a)
    id_b = egraph.add(b)

    return id_a == id_b


@add_method(ASTNode)
def egg_equal(self, *args, **kwargs):
    # Make sure calling egg_equal leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"egg_equal not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def egg_equal(self, other):
    return typecast_and_check_equality(self, other)


@add_method(Operation)
def egg_equal(self, other):
    return typecast_and_check_equality(self, other)


@add_method(FPCore)
def egg_equal(self, other):
    return typecast_and_check_equality(self, other)
