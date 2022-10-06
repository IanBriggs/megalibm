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
mirror_right = namedtuple("mirror-right", "p")
mirror_left = namedtuple("mirror-left", "p")
negate_right = namedtuple("negate-right", "p")
negate_left = namedtuple("negate-left", "p")
periodic = namedtuple("periodic", "p")
exp_recons = namedtuple("exp_recons", "p")
raw_template_rules = [
    ["capture-mirror-right", thefunc(add(mul(2, p), x)),      mirror_right(p)],
    ["capture-mirror-left",  thefunc(sub(p, x)),              mirror_left(p)],
    ["capture-negate-right", neg(thefunc(add(mul(2, p), x))), negate_right(p)],
    ["capture-negate-left",  neg(thefunc(sub(p, x))),         negate_left(p)],
    ["capture-periodic",     thefunc(add(p, x)),              periodic(p)],
    ["capture-exp-recons",   div(thefunc(add(p, x)), 2),      exp_recons(p)],
]
template_rules = list()
for l in raw_template_rules:
    name = l[0]
    frm = l[1]
    to = l[2]
    template_rules.append(Rewrite(frm, to, name))


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

    # Run with template rules
    egraph.run(template_rules,
               iter_limit=1,
               time_limit=600,
               node_limit=100_000 + 10_000 + 10_000,
               use_simple_scheduler=True)


    # Extract and sort the identities
    exprs = egraph.node_extract(body)
    exprs = list(exprs)
    exprs.sort(key=lambda e: str(e), reverse=True)
    exprs.sort(key=lambda e: len(str(e)))

    elapsed = timer.stop()
    logger.dlog("Generated {} identities in {:4f} seconds",
                len(exprs), elapsed)

    return exprs

def extract_identities(func):
    logger.dlog("Name: {}", func.get_any_name())
    logger.dlog("f(x): {}", func.body)

    exprs = generate_all_identities(func, ITERS[0])

    # exprs = filter_keep_thefunc(exprs)
    # exprs = filter_dedup(exprs, ITERS[1], False)
    # exprs = filter_dedup(exprs, ITERS[2], True)
    # exprs = filter_defs_sub(exprs, func, ITERS[3])
    # exprs = filter_defs_div(exprs, func, ITERS[4])

    exprs = [snake_egg_rules.egg_to_fpcore(expr) for expr in exprs]
    # exprs = dedup_generators(exprs, ITERS[5])

    lines = [str(expr) for expr in exprs]
    lines.sort(reverse=True)
    lines.sort(key=len)

    logger.blog("After filtering",
                "  " + "\n  ".join(lines))

    return lines