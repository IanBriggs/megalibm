# Experimentation on the idea that we can use rewrite rules to capture patterns
# in an egraph.
from snake_egg_rules.operations import *
from collections import namedtuple

import snake_egg
from snake_egg import Rewrite

import snake_egg_rules
from utils import Logger, Timer

from fpcore.ast import Number, Variable

logger = Logger(Logger.LOW, color=Logger.blue, def_color=Logger.cyan)
timer = Timer()

ITERS = [
    10,  # Main iters for finding identities
    6,  # Iters for backoff deduplication
    5,  # Iters for simple deduplication
    3,  # Iters for definition finding I(x) - f(x) = 0
    3,  # Iters for definition finding I(x) / f(x) = 1
    5,  # Iters for generator deduplication
]

period, inflection = snake_egg.vars("period inflection")

raw_template_rules = [
     ["capture-mirror",    thefunc(sub(inflection, "x")),      mirror(inflection)],
     ["capture-periodic",  thefunc(sub("x", period)),          periodic(period)],
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

    # Make rewrite for <body>(var) to f(var)
    pattern_var = snake_egg.Var(func.arguments[0].source)
    pattern_func = snake_egg_rules.thefunc(pattern_var)
    pattern_body = func.to_snake_egg(to_rule=True)
    rewrite_body_to_func = Rewrite(pattern_body, pattern_func)

    # Run with mathematical rules
    egraph.run(snake_egg_rules.rules,
               iter_limit=max_iters,
               time_limit=600,
               node_limit=20_000,
               use_simple_scheduler=False)

    # Run with undef rule
    egraph.run([rewrite_body_to_func],
               iter_limit=max_iters,
               time_limit=600,
               node_limit=20_000 + 10_000,
               use_simple_scheduler=True)

    # Run with template rules
    egraph.run(template_rules,
               iter_limit=max_iters,
               time_limit=600,
               node_limit=20_000 + 10_000 + 10_000,
               use_simple_scheduler=True)

    # Extract and sort the identities
    extracted = egraph.node_extract(body)
    exprs = list(extracted)
    exprs.sort(key=lambda e: str(e), reverse=True)
    exprs.sort(key=lambda e: len(str(e)))

    elapsed = timer.stop()
    logger.dlog("Generated {} identities in {:4f} seconds",
                len(exprs), elapsed)

    return exprs


def expr_size(expr, _cache=dict()):
    if expr in _cache:
        return _cache[expr]

    size = 1
    if isinstance(expr, tuple):
        size += sum(expr_size(arg) for arg in expr)

    _cache[expr] = size
    return size


def filter_deduplication(exprs, max_iters, use_simple):
    timer = Timer()
    timer.start()

    # Add all expressions to a fresh EGraph
    egraph = snake_egg.EGraph(snake_egg_rules.eval)
    for expr in exprs:
        egraph.add(expr)

    # Run with standard mathematical rules
    egraph.run(snake_egg_rules.rules+template_rules,
               iter_limit=max_iters,
               time_limit=600,
               node_limit=10_000,
               use_simple_scheduler=use_simple)
    expr_ids = {expr: str(egraph.add(expr)) for expr in exprs}

    # Get a mapping from EGraph Id to set of expressions
    groups = dict()
    for expr, id_num in expr_ids.items():
        groups.setdefault(id_num, set()).add(expr)

    # For each set in the mapping pick a representative
    new_exprs = list()
    for id, group in groups.items():
        if len(group) == 1:
            new_exprs.append(group.pop())
            continue
        logger.blog("all equal", "\n".join(
            str(snake_egg_rules.egg_to_fpcore(g)) for g in group))
        best_size = min(expr_size(e) for e in group)
        best_in_group = {e for e in group if expr_size(e) == best_size}
        best = min(best_in_group, key=lambda e: str(e))
        logger("Picked representative {}", snake_egg_rules.egg_to_fpcore(best))
        new_exprs.append(best)

    elapsed = timer.stop()
    logger.dlog("{} to {} identities in {:4f} seconds",
                len(exprs), len(new_exprs), elapsed)

    return new_exprs


def filter_keep_thefunc_and_templates(exprs):
    timer = Timer()
    timer.start()

    new_exprs = list()
    for expr in exprs:
        expr_str = str(snake_egg_rules.egg_to_fpcore(expr))
        if all(s not in expr_str for s in {"thefunc", "mirror", "negate", "periodic", "exp_recons"}):
            logger.llog(
                Logger.HIGH, "missing \"thefunc\" and templates: {}", expr_str)
            continue
        new_exprs.append(expr)

    elapsed = timer.stop()
    logger.dlog("{} to {} identities in {:4f} seconds",
                len(exprs), len(new_exprs), elapsed)

    return new_exprs

def filter_defs_sub(exprs, func, max_iters):
    timer = Timer()
    timer.start()

    # We can have exprs for the form
    #  I(x) = 2*<body> - f(x)
    # where <body> is the body of f(x).
    # So if we:
    #  1. Add I(x)-f(x) and 0 to a new egraph
    #  2. Union the two
    #  3. Run with rules that do not define f(x)
    #  4. Check if <body> - f(x) is in the egraph and it equals 0
    # Then we know that I(x) doe not give us new information
    var = func.arguments[0].source
    fx = snake_egg_rules.thefunc(var)
    sub = snake_egg_rules.sub
    body_sub_fx = sub(func.to_snake_egg(to_rule=False), fx)

    new_exprs = list()
    for Ix in exprs:
        egraph = snake_egg.EGraph(snake_egg_rules.eval)
        Ix_sub_fx = sub(Ix, fx)
        egraph.add(Ix_sub_fx)
        egraph.add(0)
        egraph.union(Ix_sub_fx, 0)
        egraph.rebuild()
        egraph.run(snake_egg_rules.rules,
                   iter_limit=max_iters,
                   time_limit=600,
                   node_limit=100_000,
                   use_simple_scheduler=True)
        if egraph.equiv(0, body_sub_fx):
            logger.llog(Logger.HIGH, "definition identity sub: {}", Ix)
            continue
        new_exprs.append(Ix)

    elapsed = timer.stop()
    logger.dlog("{} to {} identities in {:4f} seconds",
                len(exprs), len(new_exprs), elapsed)

    return new_exprs


def filter_defs_div(exprs, func, max_iters):
    timer = Timer()
    timer.start()

    # We can have exprs for the form
    #  I(x) = 2*<body> - f(x)
    # where <body> is the body of f(x).
    # So if we:
    #  1. Add I(x)/f(x) and 1 to a new egraph
    #  2. Union the two
    #  3. Run with rules that do not define f(x)
    #  4. Check if <body> / f(x) is in the egraph and it equals 1
    # Then we know that I(x) doe not give us new information
    var = func.arguments[0].source
    fx = snake_egg_rules.thefunc(var)
    div = snake_egg_rules.div
    body_div_fx = div(func.to_snake_egg(to_rule=False), fx)

    new_exprs = list()
    for Ix in exprs:
        egraph = snake_egg.EGraph(snake_egg_rules.eval)
        Ix_div_fx = div(Ix, fx)
        egraph.add(Ix_div_fx)
        egraph.add(1)
        egraph.union(Ix_div_fx, 1)
        egraph.rebuild()
        egraph.run(snake_egg_rules.rules,
                   iter_limit=max_iters,
                   time_limit=600,
                   node_limit=100_000,
                   use_simple_scheduler=True)
        if egraph.equiv(1, body_div_fx):
            logger.llog(Logger.HIGH, "definition identity div: {}", Ix)
            continue
        new_exprs.append(Ix)

    elapsed = timer.stop()
    logger.dlog("{} to {} identities in {:4f} seconds",
                len(exprs), len(new_exprs), elapsed)

    return new_exprs


def expr_size(expr, _cache=dict()):
    if expr in _cache:
        return _cache[expr]

    size = 1
    if isinstance(expr, tuple):
        size += sum(expr_size(arg) for arg in expr)

    _cache[expr] = size
    return size

def extract_identities(func):
    logger.dlog("Name: {}", func.get_any_name())
    logger.dlog("f(x): {}", func.body)

    exprs = generate_all_identities(func, ITERS[0])

    exprs = filter_keep_thefunc_and_templates(exprs)

    old_len = len(exprs) + 1
    while len(exprs) < old_len:
        old_len = len(exprs)
        exprs = filter_deduplication(
            exprs, ITERS[1], False)

    exprs = filter_defs_sub(exprs, func, ITERS[3])
    exprs = filter_defs_div(exprs, func, ITERS[4])

    exprs = [snake_egg_rules.egg_to_fpcore(expr) for expr in exprs]
    exprs = [expr.substitute(periodic(Number("0")), thefunc(Variable("x"))) for expr in exprs]
    exprs = list({expr.simplity() for expr in exprs})
    # exprs = deduplication_generators(exprs, ITERS[5])

    lines = [str(expr) for expr in exprs]
    lines.sort(reverse=True)
    lines.sort(key=len)

    logger.blog("After filtering",
                "  " + "\n  ".join(lines))

    return exprs
