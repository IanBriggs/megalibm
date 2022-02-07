#!/usr/bin/env python3

import argparse
import os
import os.path as path
import multiprocessing
import sys

BIN_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(BIN_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
REQ_DIR = path.join(GIT_DIR, "requirements")
EGG_DIR = path.join(REQ_DIR, "snake_egg", "target", "release")
sys.path.append(SRC_DIR)
sys.path.append(EGG_DIR)

import fpcore
import snake_egg
import snake_egg_rules

import datetime

from collections import namedtuple

from utils import Logger, Timer

logger = Logger(Logger.LOW, color=Logger.blue, def_color=Logger.cyan)
timer = Timer()


ITERS = [
    10,  # Main iters for finding identities
    11, # Iters for backoff dedup
    5,  # Iters for simple dedup
    1,  # Iters for definition finding I(x) - f(x) = 0
    1,  # Iters for definition finding I(x) / f(x) = 1
]





def parse_arguments(argv):
    num_cpus = 1 #multiprocessing.cpu_count() // 2
    parser = argparse.ArgumentParser(description='Default script description')
    parser.add_argument("-v", "--verbosity",
                        nargs="?",
                        default="high",#"low",
                        const="medium",
                        choices=list(Logger.CONSTANT_DICT),
                        help="Set output verbosity")
    parser.add_argument("-l", "--log-file",
                        nargs="?",
                        type=str,
                        help="Redirect logging to given file.")
    parser.add_argument("-p", "--procs",
                        help="Execute using the selected number of processes",
                        type=int,
                        default=num_cpus,
                        action="store")
    parser.add_argument("dirname",
                        help="Directory with the fpcore files")
    args = parser.parse_args(argv[1:])

    Logger.set_log_level(Logger.str_to_level(args.verbosity))

    if args.log_file is not None:
        Logger.set_log_filename(args.log_file)

    if os.path.isfile(args.dirname) and args.dirname.endswith(".fpcore"):
        args.fnames = [args.dirname]
    else:
        args.fnames = [path.join(args.dirname, fname)
                       for fname in os.listdir(args.dirname)
                       if fname.endswith(".fpcore")]
    args.fnames.sort()

    args.procs = min(len(args.fnames), args.procs)

    logger.dlog("Settings:")
    logger.dlog("    dirname: {}", args.dirname)
    logger.dlog("  verbosity: {}", args.verbosity)
    logger.dlog("   log-file: {}", args.log_file)
    logger.dlog("      procs: {}", args.procs)

    return args

def run_egraph(egraph, rules, iters, gen_output, use_simple):
    output = None
    iteration = 0
    for iteration in range(1, iters+1):
        try:
            egraph.run(rules,
                       iter_limit=1,
                       time_limit=600,
                       node_limit=10000000,
                       use_simple_scheduler=use_simple)
        except:
            logger.warning("Egg ran into an issue on iteration {}", iteration)
            break
    output = gen_output(egraph)
    return iteration, output


def generate_all_identities(func, max_iters):
    timer = Timer()
    timer.start()

    therules = snake_egg_rules.rules.copy()
    thevar = snake_egg.Var(func.arguments[0].source)
    thefunc = snake_egg_rules.thefunc

    from_def = thefunc(thevar)
    to_def = func.to_snake_egg(to_rule=True)
    rw = snake_egg.Rewrite

    # Add def and undef to ruleset
    therules.append(rw(from_def, to_def, "def"))
    try:
        therules.append(rw(to_def, from_def, "undef"))
    except:
        logger.warning("unable to undef function")

    # Create our egraph and add thefunc
    egraph = snake_egg.EGraph(snake_egg_rules.eval)
    se_func = thefunc("x")
    egraph.add(se_func)

    # Run for up to max_iters one at a time so we have output in the case of
    #   errors
    iteration, exprs = run_egraph(egraph, therules, max_iters,
                                  lambda eg: eg.node_extract(se_func),
                                  False)
    exprs = list(exprs)
    exprs.sort(key=lambda e: str(e), reverse=True)
    exprs.sort(key=lambda e: len(str(e)))
    elapsed = timer.stop()

    logger.dlog("Generated {} identities in {:4f} seconds",
                len(exprs), elapsed)

    return iteration, exprs


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

    logger.dlog("Removed {} identities in {:4f} seconds",
                len(exprs)-len(new_exprs), elapsed)

    return new_exprs


def filter_dedup(exprs, max_iters, use_simple):
    timer = Timer()
    timer.start()

    # Filter the results by:
    #  1. Adding all exprs to an egraph
    #  3. Churn egraph
    #  4. Now expressions will share ids, dedup groups by them
    egraph = snake_egg.EGraph(snake_egg_rules.eval)

    iteration, expr_ids = run_egraph(egraph, snake_egg_rules.rules, max_iters,
                                     lambda eg: {e:str(eg.add(e))
                                                 for e in exprs},
                                     use_simple)

    deduped = dict()
    for expr, id_num in expr_ids.items():
        if id_num in deduped:
            old = deduped[id_num]
            old_str = str(snake_egg_rules.egg_to_fpcore(old))
            expr_str = str(snake_egg_rules.egg_to_fpcore(expr))
            if (expr_size(old) > expr_size(expr)
                or (expr_size(old) == expr_size(expr) and old_str < expr_str)):
                deduped[id_num] = expr
                logger.llog(Logger.HIGH, "replaced: {}", old_str)
                logger.llog(Logger.HIGH, "    with: {}", expr_str)
                continue
            logger.llog(Logger.HIGH, "expression: {}", old_str)
            logger.llog(Logger.HIGH, "  equal to: {}", expr_str)
            continue
        deduped[id_num] = expr
    new_exprs = deduped.values()
    elapsed = timer.stop()

    logger.dlog("Removed {} identities in {:4f} seconds",
                len(exprs)-len(new_exprs), elapsed)

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
    fx = snake_egg_rules.thefunc("x")
    sub = snake_egg_rules.sub

    new_exprs = list()
    for Ix in exprs:
        egraph = snake_egg.EGraph(snake_egg_rules.eval)
        Ix_sub_fx = sub(Ix, fx)
        egraph.add(Ix_sub_fx)
        egraph.add(0)
        egraph.union(Ix_sub_fx, 0)
        egraph.rebuild()
        iteration, _ = run_egraph(egraph, snake_egg_rules.rules, max_iters,
                                  lambda eg: None,
                                  True)

        body_sub_fx = sub(func.to_snake_egg(to_rule=False), fx)

        if egraph.equiv(0, body_sub_fx):
            logger.llog(Logger.HIGH, "definition identity sub: {}", Ix)
            continue
        new_exprs.append(Ix)
    elapsed = timer.stop()

    logger.dlog("Removed {} identities in {:4f} seconds",
                len(exprs)-len(new_exprs), elapsed)

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
    fx = snake_egg_rules.thefunc("x")
    div = snake_egg_rules.div

    new_exprs = list()
    for Ix in exprs:
        egraph = snake_egg.EGraph(snake_egg_rules.eval)
        Ix_div_fx = div(Ix, fx)
        egraph.add(Ix_div_fx)
        egraph.add(1)
        egraph.union(Ix_div_fx, 1)
        egraph.rebuild()
        iteration, _ = run_egraph(egraph, snake_egg_rules.rules, max_iters,
                                  lambda eg: None,
                                  True)

        body_div_fx = div(func.to_snake_egg(to_rule=False), fx)

        if egraph.equiv(1, body_div_fx):
            logger.llog(Logger.HIGH, "definition identity div: {}", Ix)
            continue
        new_exprs.append(Ix)
    elapsed = timer.stop()

    logger.dlog("Removed {} identities in {:4f} seconds",
                len(exprs)-len(new_exprs), elapsed)

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
    logger.dlog("f(x): {}", func.body)

    iteration, exprs = generate_all_identities(func, ITERS[0])

    exprs = filter_keep_thefunc(exprs)
    exprs = filter_dedup(exprs, ITERS[1], False)
    exprs = filter_dedup(exprs, ITERS[2], True)
    exprs = filter_defs_sub(exprs, func, ITERS[3])
    exprs = filter_defs_div(exprs, func, ITERS[4])

    lines = [str(snake_egg_rules.egg_to_fpcore(expr)) for expr in exprs]
    lines.sort(reverse=True)
    lines.sort(key=len)

    logger.blog("After filtering",
                "  " + "\n  ".join(lines))

    return lines


def write_per_func_webpage(filename, func_to_identities):
    today = datetime.date.today()
    y = today.year
    m = today.month
    d = today.day
    lines = [
        "<!doctype html>",
        "<html>",
        "<head>",
        f"<title>Per Function Identities for {y}-{m}-{d}</title>",
        "<style>",
        "pre { font-size: 20px; }",
        "</style>",
        "</head>",
        "<body>",
    ]

    info = [({p.name: p.value for p in func.properties}.get("name", "NoName"),
             func,
             ids)
            for func, ids in func_to_identities.items()]
    info.sort(key=lambda t:t[0])
    for name, func, ids in info:
        name = name.strip('"')
        lines.append(func.to_html())

        lines.append("<ul>")

        ids.sort(key=lambda id:expr_size(id))
        for id in ids:
            lines.append(f"<li>{str(id)}</li>")

        lines.append("</ul>")

    lines.extend([
        "</body>",
        "</html>"
        ])

    text = "\n".join(lines)

    with open(filename, "w") as f:
        f.write(text)


def write_identity_webpage(filename, identities):
    today = datetime.date.today()
    y = today.year
    m = today.month
    d = today.day
    lines = [
        "<!doctype html>",
        "<html>",
        "<head>",
        f"<title>Megalibm Identities for {y}-{m}-{d}</title>",
        "</head>",
        "<body>",
        "<a href=per_func.html>Per Function Breakdown</a>",
        f"<h1>All {len(identities)} Identities:</h1>",
        "<table>",
        "<tr>",
        "<th>Count</th>",
        "<th>Expr</th>",
        "</tr>",
    ]

    identities = [(expr, count) for expr, count in identities.items()]
    identities.sort(key=lambda t: t[0])
    identities.sort(key=lambda t: -t[1])

    lines.extend([f"<tr><td>{count}</td><td>{expr}</td><tr>"
                  for expr, count in identities])

    lines.extend([
        "</table>",
        "</body>",
        "</html>"
        ])

    text = "\n".join(lines)

    with open(filename, "w") as f:
        f.write(text)


def handle_work_item(fname):
    try:
        with open(fname, "r") as f:
            text = f.read()

        func = fpcore.parse(text)
        func.remove_let()

        expr_lines = extract_identities(func)

        return func, expr_lines
    except Exception as e:
        return None, e


def main(argv):
    logger.warning("Currently unsound")

    args = parse_arguments(argv)

    with multiprocessing.Pool(processes=args.procs) as pool:
        tuples = pool.map(handle_work_item, args.fnames, chunksize=1)

    per_func_identities = dict(tuples)
    counts = dict()
    for func, ids in per_func_identities.items():
        if func == None:
            raise e
        for i in ids:
            counts[i] = counts.get(i, 0) + 1

    tups = [(c, e) for e, c in counts.items()]
    tups.sort(key=lambda t: t[1], reverse=True)
    tups.sort(key=lambda t: t[0], reverse=True)

    logger.blog(f"All identites",
                "Count\tExpr\n" + "\n".join(f"{c}\t{e}"
                                            for c, e in tups))

    write_per_func_webpage("per_func.html", per_func_identities)
    write_identity_webpage("index.html", counts)

    return 0




if __name__ == "__main__":
    timer.start()

    retcode = 130  # meaning "Script terminated by Control-C"

    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("")
        print("Goodbye")

    timer.stop()

    logger("Elapsed time: {:4f} sec", timer.elapsed())

    sys.exit(retcode)
