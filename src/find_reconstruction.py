import snake_egg
import snake_egg_rules
from snake_egg_rules import operations, egg_to_fpcore
from fpcore.ast import Variable


def get_reconstruction(s_expr):
    """
        Construct 2 egraphs with k = 1 & 2 containing the s_expr (s reconstruction) applied k -> (1/2) times.
        Use e-graph intersection to find and return the generalised s_expr when applied k times
    """
    #Egraph 1
    egraph = snake_egg.EGraph(snake_egg_rules.eval)
    egraph.enable_explanations()
    k = egraph.add("k")
    one = egraph.add(1)
    egraph.union(k, one)

    recons_1 = operations.recons('k')
    s_body = s_expr.to_snake_egg(to_rule=False)
    egraph.add(recons_1)
    egraph.add(s_body)
    egraph.union(recons_1, s_body)
    egraph.rebuild()

    #Egraph 2
    egraph2 = snake_egg.EGraph(snake_egg_rules.eval)
    egraph2.enable_explanations()
    k = egraph2.add("k")
    two = egraph2.add(2)
    egraph2.union(k, two)
    sec_order_s_expr = s_expr.substitute(Variable("x"), s_expr) 

    recons_2 = operations.recons('k')
    s_body2 = sec_order_s_expr.to_snake_egg(to_rule=False)
    egraph2.add(recons_2)
    egraph2.add(s_body2)
    egraph2.union(recons_2, s_body2)
    egraph2.rebuild()

    egraph.run(snake_egg_rules.rules,
                iter_limit=10,
                time_limit=60,
                node_limit=1000,
                use_simple_scheduler=True)
    
    egraph2.run(snake_egg_rules.rules,
                iter_limit=60,
                time_limit=10,
                node_limit=1000,
                use_simple_scheduler=True)

    intersection = egraph.intersect(egraph2)
    
    expr = intersection.extract(recons_1)

    return expr