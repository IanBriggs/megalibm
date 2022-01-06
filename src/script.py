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


def extract_identities(func, max_iters=10):
    thevar = snake_egg.Var(func.arguments[0].source)
    thefunc = namedtuple("thefunc", "x")

    thefunc_rule_do = snake_egg.Rewrite(thefunc(thevar),
                                     func.to_snake_egg(to_rule=True),
                                     "smeagol")
    snake_egg_rules.rules.append(thefunc_rule_do)

    thefunc_rule_undo = snake_egg.Rewrite(func.to_snake_egg(to_rule=True),
                                     thefunc(thevar),
                                     "gollum")
    snake_egg_rules.rules.append(thefunc_rule_undo)

    parse_thefunc = lambda x: fpcore.ast.Operation("thefunc", x)
    snake_egg_rules.one_arg[thefunc] = parse_thefunc

    egraph = snake_egg.EGraph(snake_egg_rules.eval)
    se_func = thefunc("x")
    eg_func = egraph.add(se_func)

    old_expr_lines = set()
    expr_lines = set()
    iter = 0
    for iter in range(1, max_iters+1):
        try:
            egraph.run(snake_egg_rules.rules, iter_limit=1)
        except:
            logger.warning("Egg ran into an issue")
            break

        exprs = egraph.node_extract(se_func)

        old_expr_lines = expr_lines
        expr_lines = {str(snake_egg_rules.egg_to_fpcore(expr))
                      for expr in exprs}

        if old_expr_lines == expr_lines:
            logger.log("Halted early")
            break

    logger.blog(f"After {iter} iterations", "\n".join(expr_lines))

    snake_egg_rules.rules.pop() # remove gollum
    snake_egg_rules.rules.pop() # remove smeagol

    return expr_lines


def write_identity_webpage(filename, identities):
    today = datetime.date.today()
    y = today.year
    m = today.month
    d = today.day
    lines = [
        "<!doctype html>",
        "<html>",
        "<head>",
        "<title>Megalibm Identities for {y}-{m}-{d}</title>",
        "</head>",
        "<body>",
        "<h1>Identities:</h1>",
        "<ul>",
    ]

    lines.extend([f"<li>{iden}</li>" for iden in identities])

    lines.extend([
        "</ul>",
        "</boy>",
        "</html>"
        ])

    text = "\n".join(lines)

    with open(filename, "w") as f:
        f.write(text)


def main(argv):
    logger.warning("Currently unsound")

    args = parse_arguments(argv)

    union = set()
    for fname in os.listdir(args.dirname):
        if not fname.endswith(".fpcore"):
            continue

        fname = path.join(args.dirname, fname)
        with open(fname, "r") as f:
            text = f.read()

        func = fpcore.parse(text)
        logger("Input function: {}", func)

        func.remove_let()

        expr_lines = extract_identities(func)

        union.update(expr_lines)

    union = {u for u in union if "thefunc" in u}
    logger.blog(f"All identites", "\n".join(union))

    write_identity_webpage("index.html", union)

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
