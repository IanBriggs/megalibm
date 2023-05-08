import snake_egg
import snake_egg_rules
from snake_egg_rules import operations
from fpcore.ast import Variable


def get_reconstruction(s_expr):
    """
    Construct 2 egraphs with k = 1 & 2 containing the s_expr (s reconstruction)
    applied k -> (1/2) times.
    Use e-graph intersection to find and return the generalized s_expr when
    applied k times
    """
    # Egraph 1
    egraph_1 = snake_egg.EGraph(snake_egg_rules.eval)
    egraph_1.enable_explanations()
    k = egraph_1.add("k")
    one = egraph_1.add(1)
    egraph_1.union(k, one)

    recons_1 = operations.recons('k')
    s_body = s_expr.to_snake_egg(to_rule=False)
    egraph_1.add(recons_1)
    egraph_1.add(s_body)
    egraph_1.union(recons_1, s_body)
    egraph_1.rebuild()

    # Egraph 2
    egraph_2 = snake_egg.EGraph(snake_egg_rules.eval)
    egraph_2.enable_explanations()
    k = egraph_2.add("k")
    two = egraph_2.add(2)
    egraph_2.union(k, two)

    recons_2 = operations.recons('k')
    sec_order_s_expr = s_expr.substitute(Variable("x"), s_expr)
    s_body2 = sec_order_s_expr.to_snake_egg(to_rule=False)
    egraph_2.add(recons_2)
    egraph_2.add(s_body2)
    egraph_2.union(recons_2, s_body2)
    egraph_2.rebuild()

    egraph_1.run(snake_egg_rules.rules,
               iter_limit=10,
               time_limit=60,
               node_limit=1000,
               use_simple_scheduler=True)

    egraph_2.run(snake_egg_rules.rules,
                iter_limit=10,
                time_limit=60,
                node_limit=1000,
                use_simple_scheduler=True)

    intersection = egraph_1.intersect(egraph_2)

    expr = intersection.extract(recons_1)

    return expr
