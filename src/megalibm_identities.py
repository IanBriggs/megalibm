#!/usr/bin/env python3

import argparse
import datetime
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

import find_identities
import fpcore
from utils import Logger, Timer

logger = Logger(Logger.LOW, color=Logger.blue, def_color=Logger.cyan)
timer = Timer()


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Default script description')
    parser.add_argument("-v", "--verbosity",
                        nargs="?",
                        default="high",  # "low",
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

    if os.path.isfile(args.dirname) and args.dirname.endswith(".fpcore"):
        args.fnames = [args.dirname]
    else:
        args.fnames = [path.join(args.dirname, fname)
                       for fname in os.listdir(args.dirname)
                       if fname.endswith(".fpcore")]
    args.fnames.sort()

    logger.dlog("Settings:")
    logger.dlog("    dirname: {}", args.dirname)
    logger.dlog("  verbosity: {}", args.verbosity)
    logger.dlog("   log-file: {}", args.log_file)

    return args


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
    info.sort(key=lambda t: t[0])
    for name, func, ids in info:
        name = name.strip('"')
        lines.append(func.to_html())

        lines.append("<ul>")

        ids.sort(key=lambda id: find_identities.expr_size(id))
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


def handle_work_item(func):
    func.remove_let()

    if func.arguments[0].source != "x":
        var = func.arguments[0]
        x = fpcore.ast.Variable("x")
        func.arguments[0] = x
        func = func.substitute(var, x)

    expr_lines = find_identities.extract_identities(func)

    return func, expr_lines


def main(argv):
    logger.warning("Currently unsound")

    args = parse_arguments(argv)

    # Read all the files, each file may have mutiple functions
    work_items = list()
    for fname in args.fnames:
        with open(fname, "r") as f:
            text = f.read()

        some_funcs = fpcore.parse(text)
        work_items.extend(some_funcs)

    # Filter the functions
    old_work_items = work_items
    work_items = list()
    nag_shown = True
    for func in old_work_items:
        if len(func.arguments) == 1:
            work_items.append(func)
            continue
        if nag_shown:
            msg = "Currently only functions in a single variable are supported"
            logger.warning(msg)
            nag_shown = False
        name = func.get_any_name() or func
        logger.warning("Dropping {}", name)

    # Run the identity finder
    tuples = [handle_work_item(func) for func in work_items]

    # Get some statistics
    per_func_identities = dict(tuples)
    counts = dict()
    for func, ids in per_func_identities.items():
        if func == None:
            raise ids
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

    logger("{} unique identities", len(counts))

    return 0


if __name__ == "__main__":
    timer.start()

    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        retcode = 130  # meaning "Script terminated by Control-C"
        print("")
        print("Goodbye")

    timer.stop()

    logger("Elapsed time: {:4f} sec", timer.elapsed())

    sys.exit(retcode)
