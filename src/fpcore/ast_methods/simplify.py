from functools import cache
from fpcore.ast import ASTNode, Atom, FPCore, Operation
from utils import add_method
import snake_egg
import snake_egg_rules


@cache
def simplify_with_egraph(expr):
    egraph = snake_egg.EGraph(snake_egg_rules.eval)
    body = expr.to_snake_egg(to_rule=False)
    id = egraph.add(body)
    egraph.run(snake_egg_rules.rules,
               iter_limit=10,
               time_limit=600,
               node_limit=20_000,
               use_simple_scheduler=False)
    simplified = egraph.extract(id)
    return snake_egg_rules.egg_to_fpcore(simplified)


@add_method(ASTNode)
def simplify(self, *args, **kwargs):
    # Make sure calling simplify leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"simplify not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def simplify(self):
    return self


@add_method(Operation)
def simplify(self):
    return simplify_with_egraph(self)


@add_method(FPCore)
def simplify(self):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  self.body.simplify())
