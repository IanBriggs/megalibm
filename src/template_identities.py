# Experimentation on the idea that we can use rewrite rules to capture patterns
# in an egraph.
import snake_egg
import snake_egg_rules
from snake_egg import Rewrite
from utils import Logger, Timer
from collections import namedtuple

logger = Logger(Logger.LOW, color=Logger.blue, def_color=Logger.cyan)
timer = Timer()

x, p = snake_egg.vars("x p")
from snake_egg_rules.operations import *
mirror_right = namedTuple("mirror-right", "p")
mirror_left = namedTuple("mirror-left", "p")
negate_right = namedTuple("negate-right", "p")
negate_left = namedTuple("negate-left", "p")

raw_template_rules = [
    ["capture-mirror-right", thefunc(add(mul(2, p), x)),      mirror_right(p)],
    ["capture-mirror-left",  thefunc(sub(p, x)),              mirror_left(p)],
    ["capture-negate-right", neg(thefunc(add(mul(2, p), x))), negate_right(p)],
    ["capture-negate-left",  neg(thefunc(sub(p, x))),         negate_left(p)],
]


def generate_all_identities(func, max_iters):
    timer = Timer()
    timer.start()

    # Create our egraph and add the function body
    egraph = snake_egg.EGraph(snake_egg_rules.eval)
    body = func.to_snake_egg(to_rule=False)
    egraph.add(body)

    # Run with mathematical rules
    egraph.run(snake_egg_rules.rules,
               iter_limit=max_iters,
               time_limit=600,
               node_limit=100_000,
               use_simple_scheduler=False)

    # Make rewrite for <body>(var) to f(var)
    pattern_var = snake_egg.Var(func.arguments[0].source)
    pattern_func = snake_egg_rules.thefunc(pattern_var)
    pattern_body = func.to_snake_egg(to_rule=True)
    rewrite_body_to_func = Rewrite(pattern_body, pattern_func)

    # Run with undef rule
    egraph.run([rewrite_body_to_func],
               iter_limit=1,
               time_limit=600,
               node_limit=100_000 + 10_000,
               use_simple_scheduler=True)

    # Create the template rules

    # Run with template rules

    # Extract and sort the identities
    exprs = egraph.node_extract(body)
    exprs = list(exprs)
    exprs.sort(key=lambda e: str(e), reverse=True)
    exprs.sort(key=lambda e: len(str(e)))

    elapsed = timer.stop()
    logger.dlog("Generated {} identities in {:4f} seconds",
                len(exprs), elapsed)

    return exprs