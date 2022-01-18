#!/usr/bin/env python3

import argparse
import os
import os.path as path
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

logger = Logger(Logger.LOW, color=Logger.blue)
timer = Timer()





def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Default script description')
    parser.add_argument("-v", "--verbosity",
                        nargs="?",
                        default="low",
                        const="medium",
                        choices=list(Logger.CONSTANT_DICT),
                        help="Set output verbosity")
    parser.add_argument("-l", "--log-file",
                        nargs="?",
                        type=str,
                        help="Redirect logging to given file.")
    parser.add_argument("dirname",
                        help="Directory with the fpcore files")
    args = parser.parse_args(argv[1:])

    Logger.set_log_level(Logger.str_to_level(args.verbosity))

    if args.log_file is not None:
        Logger.set_log_filename(args.log_file)

    logger.dlog("Settings:")
    logger.dlog("    dirname: {}", args.dirname)
    logger.dlog("  verbosity: {}", args.verbosity)
    logger.dlog("   log-file: {}", args.log_file)

    return args

def run_egraph(egraph, rules, iters, gen_output):
    output = None
    iteration = 0
    for iteration in range(1, iters+1):
        try:
            egraph.run(rules, iter_limit=1, time_limit=600, node_limit=10000000)
        except:
            logger.warning("Egg ran into an issue on iteration {}", iteration)
            break
        output = gen_output(egraph)
    return iteration, output


def generate_all_identities(func, max_iters):
    therules = snake_egg_rules.rules.copy()
    thevar = snake_egg.Var(func.arguments[0].source)
    thefunc = namedtuple("thefunc", "x")

    # Add def and undef to ruleset
    therules.append(snake_egg.Rewrite(thefunc(thevar),
                                      func.to_snake_egg(to_rule=True),
                                      "def"))
    try:
        therules.append(snake_egg.Rewrite(func.to_snake_egg(to_rule=True),
                                          thefunc(thevar),
                                          "undef"))
    except:
        logger.warning("unable to undef function")

    # Add thefunc to the snake_egg --> fpcore parser
    parse_thefunc = lambda x: fpcore.ast.Operation("thefunc", x)
    snake_egg_rules.one_arg[thefunc] = parse_thefunc

    # Create our egraph and add thefunc
    egraph = snake_egg.EGraph(snake_egg_rules.eval)
    se_func = thefunc("x")
    egraph.add(se_func)

    # Run for up to max_iters one at a time so we have output in the case of
    #   errors
    iteration, exprs = run_egraph(egraph, therules, max_iters,
                                  lambda eg: eg.node_extract(se_func))

    # If there was no issue the run a few extra iters to find unreduced output
    _, extra_exprs = run_egraph(egraph, therules, 2,
                                lambda eg: eg.node_extract(se_func))

    # Intersect the two expr sets
    # The idea is that some expressions are redundant, but were generated later
    #   in the egraph iterations, so give it a few more and intersect to exclude
    #   those expressions.
    exprs = set(exprs)
    extra_exprs = set(extra_exprs)
    intersection = set()
    for expr in exprs:
        exstr = str(snake_egg_rules.egg_to_fpcore(expr))
        if expr not in extra_exprs:
            logger.log("extra iters removed: {}", exstr)
            continue
        if "thefunc" not in exstr:
            logger.log("thefunc not present: {}", exstr)
            continue
        intersection.add(expr)

    return iteration, intersection

def expr_size(expr, _cache=dict()):
    if expr in _cache:
        return _cache[expr]

    size = 1
    if isinstance(expr, tuple):
        size += sum(expr_size(arg) for arg in expr)

    _cache[expr] = size
    return size

def extract_identities(func, max_iters=15):
    iteration, exprs = generate_all_identities(func, max_iters)

    # Filter the results by:
    #  1. Adding all exprs to an egraph
    #  3. Churn egraph
    #  4. Now expressions will share ids, dedup groups by them

    egraph = snake_egg.EGraph(snake_egg_rules.eval)
    expr_ids = dict()
    for expr in exprs:
        id_num = egraph.add(expr)
        expr_ids[expr] = str(id_num)

    for churn in range(3):
        try:
            egraph.run(snake_egg_rules.rules, iter_limit=1, time_limit=600, node_limit=10000000)
        except:
            logger.warning("Egg ran into an issue")
            break

        for expr in exprs:
            id_num = egraph.add(expr)
            expr_ids[expr] = str(id_num)

    deduped = dict()
    for expr, id_num in expr_ids.items():
        if id_num in deduped:
            old = deduped[id_num]
            old_str = str(snake_egg_rules.egg_to_fpcore(old))
            expr_str = str(snake_egg_rules.egg_to_fpcore(expr))
            if expr_size(old) > expr_size(expr) or old_str < expr_str:
                deduped[id_num] = expr
                logger("replaced {} with {}", old_str, expr_str)
                continue
            logger("equivalent expressions {} == {}", old_str, expr_str)
            continue
        deduped[id_num] = expr

    exprs = deduped.values()

    lines = [str(snake_egg_rules.egg_to_fpcore(expr)) for expr in exprs]

    logger.blog(f"After {iteration} iterations",
                "per_func: " + "\nper_func: ".join(lines))

    return lines


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
        f"<h1>All {len(identities)} Identities:</h1>",
        "<table>",
        "<tr>",
        "<th>Count</th>",
        "<th>Expr</th>",
        "</tr>",
    ]

    identities = [(expr, count) for expr, count in identities.items()]
    identities.sort(key=lambda t: -t[1])

    lines.extend([f"<tr><td>{count}</td><td>{expr}</td><tr>"
                  for expr, count in identities])

    lines.extend([
        "</table>",
        "</boy>",
        "</html>"
        ])

    text = "\n".join(lines)

    with open(filename, "w") as f:
        f.write(text)


def main(argv):
    logger.warning("Currently unsound")

    args = parse_arguments(argv)

    if os.path.isfile(args.dirname) and args.dirname.endswith(".fpcore"):
        fnames = [args.dirname]
    else:
        fnames = [path.join(args.dirname, fname)
                  for fname in os.listdir(args.dirname)
                  if fname.endswith(".fpcore")]

    counts = dict()
    for fname in fnames:
        with open(fname, "r") as f:
            text = f.read()

        func = fpcore.parse(text)
        logger("Input function: {}", func)

        func.remove_let()

        expr_lines = extract_identities(func)

        for line in expr_lines:
            if line in counts:
                counts[line] += 1
            else:
                counts[line] = 1


    logger.blog(f"All identites",
                "Count\tExpr\n" + "\n".join(f"{c}\t{e}"
                                            for e, c in counts.items()))

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
