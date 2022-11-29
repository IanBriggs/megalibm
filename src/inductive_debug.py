import snake_egg
import snake_egg_rules
from snake_egg_rules import operations
from fpcore.ast import Operation, Variable, Number

if __name__ == "__main__":

    #E1
    recons = operations.recons('k')
    s_expr = Operation("+", Variable("x"), Number("1"))
    e1 = snake_egg.EGraph(snake_egg_rules.eval)
    e1.enable_explanations()
    e1.add("k")
    e1.add(1)
    e1.union("k", 1)

    e1.add(recons)
    s_body = s_expr.to_snake_egg(to_rule=False)
    e1.add(s_body)
    e1.union(recons, s_body)
    print(e1.dot())


    #E2
    e2 = snake_egg.EGraph(snake_egg_rules.eval)
    e2.enable_explanations()
    e2.add("k")
    e2.add(1)
    e2.union("k", 2)

    e2.add(recons)
    s_body2 = s_expr.substitute(Variable("x"), s_expr)
    e2.add(s_body2)
    e2.union(recons, s_body2)


    e1.run(snake_egg_rules.rules,
                   iter_limit=1,
                   time_limit=600,
                   node_limit=100_000,
                   use_simple_scheduler=True)


    e2.run(snake_egg_rules.rules,
                   iter_limit=1,
                   time_limit=600,
                   node_limit=100_000,
                   use_simple_scheduler=True)

    print(e1.dot())
    print(e2.dot())
    inters = e1.intersect(e2)
    ext = inters.extract(recons)    


