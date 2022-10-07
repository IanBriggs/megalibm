import z3
import snake_egg
import fpcore
import snake_egg_rules
from pprint import pprint
from utils import Logger, Timer

logger = Logger(Logger.LOW, color=Logger.blue, def_color=Logger.cyan)
timer = Timer()

# This is where we find "useful" identities of a function.
# To do so we start with a function `f(x) = <body>(x)`
# This `<body>(x)` is placed in an EGraph and ran with a standard set of
# mathematical rules to generate many equivalent expressions.
# Then a single iteration is ran in that EGraph to rewrite `<body>(?x)` to
# `f(?x)`, this allows us to identify things containing `f(<something>)`
# To finish generation we take this EGraph and extract a representative
# expression for each E_Node_ in the main E_Class_ while giving `f` a weight of
# 0 to cause it to occur if possible.
# Now we need to filter this set of expressions down to a reasonable number.
# 1. __Pre__: Only keep expressions containing `f`
# 2. __Dedup__: Put all expressions in an EGraph and run with standard
#               mathematical rules. If two expressions are equal without
#               knowing what `f` means, then it is not interesting. This is
#               done two times, once with the backoff scheduler and once with
#               the simple scheduler. The first version removes a bulk of
#               identities, to allow the second to be more thorough.
# 3. __DefSub__: Attempts to remove "definitional" identities that basically
#                encode the definition of `f` in the expression (e.g.
#                `f(x) = sin(x)` with the identity `I(x) = 2*sin(x) - f(x)`)
#                To do this we start with `f(x) = <body>(x)` and
#                `I(x) = <i-body>(x)`. We add `<i-body>(x) - f(x)` and `0` to
#                the EGraph and union them before running with standard
#                mathematical rules. At the end, if `<body>(x) - f(x)` is in
#                the EGraph and equal to `0`, then the identity was encoding
#                a definition.
# 4. __DefDiv__: This does the same as above by inserting `<i-body>(x) / f(x)`
#                and `1` into the EGraph.
# 5. __Gen__: Attempts to remove "generator" identities. These are identities
#             such as, for `f(x) = sin(x)`, `I_0(x) = sin(x + pi)` and
#             `I_1(x) = sin(x + 2*pi)`. You can generate `I_1(x)` by taking
#             `I_0(I_0(x))`.
# Hopefully what comes out the other end is a small set of identities that give
# us new information about the function

ITERS = [
    10,  # Main iters for finding identities
    6,  # Iters for backoff dedup
    5,  # Iters for simple dedup
    3,  # Iters for definition finding I(x) - f(x) = 0
    3,  # Iters for definition finding I(x) / f(x) = 1
    5,  # Iters for generator dedup
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
    rewrite_body_to_func = snake_egg.Rewrite(pattern_body, pattern_func)

    # Run with undef rule
    egraph.run([rewrite_body_to_func],
               iter_limit=1,
               time_limit=600,
               node_limit=100_000 + 10_000,
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


def filter_keep_thefunc(exprs):
    timer = Timer()
    timer.start()

    new_exprs = list()
    for expr in exprs:
        exstr = str(snake_egg_rules.egg_to_fpcore(expr))
        if "thefunc" not in exstr:
            logger.llog(Logger.HIGH, "missing \"thefunc\": {}", exstr)
            continue
        new_exprs.append(expr)

    elapsed = timer.stop()
    logger.dlog("{} to {} identities in {:4f} seconds",
                len(exprs), len(new_exprs), elapsed)

    return new_exprs


def filter_reject_thefunc_of_x(exprs):
    timer = Timer()
    timer.start()

    new_exprs = list()
    for expr in exprs:
        exstr = str(snake_egg_rules.egg_to_fpcore(expr))
        exstr.replace("(thefunc x)", "")
        if "thefunc" not in exstr:
            logger.llog(Logger.HIGH, "only has \"thefunc(x)\": {}", exstr)
            continue
        new_exprs.append(expr)

    elapsed = timer.stop()
    logger.dlog("{} to {} identities in {:4f} seconds",
                len(exprs), len(new_exprs), elapsed)

    return new_exprs


def filter_dedup(exprs, max_iters, use_simple):
    timer = Timer()
    timer.start()

    # Add all expressions to a fresh EGraph
    egraph = snake_egg.EGraph(snake_egg_rules.eval)
    for expr in exprs:
        egraph.add(expr)

    # Run with standard mathematical rules
    egraph.run(snake_egg_rules.rules,
               iter_limit=max_iters,
               time_limit=600,
               node_limit=100_000,
               use_simple_scheduler=use_simple)
    expr_ids = {expr: str(egraph.add(expr)) for expr in exprs}

    # Get a mapping from EGraph Id to set of expressions
    groups = dict()
    for expr, id_num in expr_ids.items():
        groups.setdefault(id_num, set()).add(expr)

    # For each set in the mapping pick a representative
    new_exprs = list()
    for id, group in groups.items():
        best = group.pop()
        best_size = expr_size(best)
        best_str = str(best)
        while len(group) > 0:
            new = group.pop()
            new_size = expr_size(new)
            new_str = str(new)
            if new_size > best_size:
                continue
            if new_size < best_size:
                best = new
                best_size = new_size
                best_str = new_str
                continue
            if new_str > best_str:
                continue
            best = new
            best_size = new_size
            best_str = new_str
        new_exprs.append(best)

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


def cross_identity(A, B):
    # A = (ta (f (sa x)))
    # B = (tb (f (sb x)))
    # A*B = (ta (tb (f (sb (sa x)))))
    x = fpcore.ast.Variable("x")
    f = fpcore.ast.Operation("thefunc", x)
    ta = A.extract_t()
    tb = B.extract_t()
    sa = A.extract_s()
    sb = B.extract_s()

    ta_tb = ta.substitute(x, tb)
    ta_tb_f = ta_tb.substitute(x, f)
    ta_tb_f_sb = ta_tb_f.substitute(x, sb)
    ta_tb_f_sb_sa = ta_tb_f_sb.substitute(x, sa)

    return ta_tb_f_sb_sa


def dedup_generators(identities, iters):
    timer = Timer()
    timer.start()

    query = [
        "(define-fun btoi ((b Bool)) Int",
        "  (ite b 1 0))",
    ]

    query.extend([f"(declare-const core_I_{I} Bool) ; {iden}"
                  for I, iden in enumerate(identities)])

    query.extend([f"(declare-const I_{I} Bool)"
                  for I, iden in enumerate(identities)])

    query.extend([f"(declare-const len_I_{I} Int)"
                  for I, iden in enumerate(identities)])

    query.extend([f"(assert (< 0 len_I_{I} 5))"
                  for I, iden in enumerate(identities)])

    cross_products = dict()
    I = 0
    for first in identities:
        first.sat_expr = None
        logger("Crossing: {}", first)
        crossed = list()
        J = 0
        for second in identities:
            logger("  with: {}", second)
            cross = first.cross(second)
            cross.sat_expr = (
                f"(and I_{I} I_{J} (= len_I_{{}} (+ len_I_{I} len_I_{J})))")
            logger("    becomes: {}", cross)
            crossed.append(cross)
            J += 1
        cross_products[first] = crossed
        I += 1

    egraph = snake_egg.EGraph(snake_egg_rules.eval)

    flat_cross_products = list()
    for key, value in cross_products.items():
        egraph.add(key.to_snake_egg(to_rule=False))
        flat_cross_products.append(key)
        for cross in value:
            egraph.add(cross.to_snake_egg(to_rule=False))
            flat_cross_products.append(cross)

    egraph.run(snake_egg_rules.rules,
               iter_limit=iters,
               time_limit=600,
               node_limit=100_000,
               use_simple_scheduler=True)
    ids = {e: str(egraph.add(e.to_snake_egg(to_rule=False)))
           for e in flat_cross_products}

    groups = list(set(ids.values()))

    for I, iden in enumerate(identities):
        gid = ids[iden]
        query.append(f"(assert (= I_{I} (or (and core_I_{I} (= len_I_{I} 1))")
        for e in flat_cross_products:
            if ids[e] != gid or e.sat_expr == None:
                continue
            query.append("  " + e.sat_expr.format(I))
        query[-1] += ")))"

    line = "(assert (and "
    line += " ".join([f"I_{I}" for I in range(len(identities))]) + "))"
    query.append(line)

    query.append("(declare-const cost Int)")

    line = "(assert (= cost (+ "
    line += " ".join([f"(btoi core_I_{I})" for I in
                      range(len(identities))]) + ")))"
    query.append(line)

    query.append("(minimize cost)")
    query.append("(check-sat)")

    query = "\n".join(query)

    logger.blog("Z3 query", query)

    ctx = z3.Context("model_validate", "true")
    optimizer = z3.Optimize(ctx=ctx)
    optimizer.from_string(query)
    state = optimizer.check()
    if str(state) != "sat":
        assert False, "Impossible!"
    z3_model = optimizer.model()
    model = {d.name(): z3_model[d] for d in z3_model}
    for I, iden in enumerate(identities):
        name = f"I_{I}"
        logger("{}: {}", model[name], iden)

    new_identities = [iden for I, iden in enumerate(identities)
                      if model[f"core_I_{I}"]]

    elapsed = timer.stop()
    logger.dlog("{} to {} identities in {:4f} seconds",
                len(identities), len(new_identities), elapsed)

    return new_identities


def extract_identities(func):
    logger.dlog("Name: {}", func.get_any_name())
    logger.dlog("f(x): {}", func.body)

    exprs = generate_all_identities(func, ITERS[0])

    exprs = filter_keep_thefunc(exprs)
    exprs = filter_dedup(exprs, ITERS[1], False)
    exprs = filter_dedup(exprs, ITERS[2], True)
    exprs = filter_defs_sub(exprs, func, ITERS[3])
    exprs = filter_defs_div(exprs, func, ITERS[4])

    exprs = [snake_egg_rules.egg_to_fpcore(expr) for expr in exprs]
    exprs = dedup_generators(exprs, ITERS[5])

    lines = [str(expr) for expr in exprs]
    lines.sort(reverse=True)
    lines.sort(key=len)

    logger.blog("After filtering",
                "  " + "\n  ".join(lines))

    return lines
