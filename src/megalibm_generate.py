#!/usr/bin/env python3

import argparse
import datetime
from genericpath import isdir
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
import lambdas
import cmd_sollya

from synthesize import synthesize
from assemble_c_files import *
from interval import Interval

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


def c_ize_name(function):
    name = {p.name: p.value for p in function.properties}.get("name", "NoName")
    replace_chars = {
        '"' : "",
        "'" : "",
        "(" : "",
        ")" : "",
        "," : "_",
        " " : "_",
        "." : "_",
        "-" : "_",
        ":" : "_",
        "+" : "plus",
    }
    for frm, to in replace_chars.items():
        name = name.replace(frm, to)
    while "__" in name:
        name = name.replace("__", "_")
    return name

def generate_all_code(function, domain):
    name = c_ize_name(function)
    target = lambdas.types.Impl(function, domain)

    start = os.getcwd()
    if not path.isdir(name):
        os.mkdir(name)
    os.chdir(name)

    my_lambdas = synthesize(target)

    libm_funcname = f"libm_{name}"
    libm_sig, libm_src = lambdas.generate_libm_c_code(target, libm_funcname)
    logger.blog("C libm function", "\n".join(libm_src))

    mpfr_funcname = f"mpfr_{name}"
    mpfr_sig, mpfr_src = lambdas.generate_mpfr_c_code(target, mpfr_funcname)
    logger.blog("C mpfr function", "\n".join(mpfr_src))

    gen_sigs = list()
    gen_srcs = list()
    gen_funcnames = list()
    for i, lam in enumerate(my_lambdas):
        try:
            funcname = f"my_{name}_{i}"
            sig, src = lambdas.generate_c_code(lam, funcname)
            logger.blog("C function", "\n".join(src))
            gen_sigs.append(sig)
            gen_srcs.append(src)
            gen_funcnames.append(funcname)
        except cmd_sollya.FailedGenError:
            logger("Unable to generate polynomial, skipping")

    header_lines = assemble_header([libm_sig, mpfr_sig] + gen_sigs)
    header_fname = "funcs.h"
    with open(header_fname, "w") as f:
        f.write("\n".join(header_lines))

    func_lines = assemble_functions(
        [libm_src, mpfr_src] + gen_srcs, header_fname)
    func_fname = "funcs.c"
    with open(func_fname, "w") as f:
        f.write("\n".join(func_lines))

    fstr = str(function)
    if any(f in fstr for f in {"sin", "cos", "tan"}):
        domains = [("-M_PI/4", "M_PI/4"),
                   ("-M_PI", "M_PI"),
                   ("-10*M_PI", "10*M_PI"),
                   ("-100*M_PI", "100*M_PI"), ]
    elif float(domain.inf) == 0:
        domains = [("0.0", "0.175"),
                   ("0.0", "0.7"),
                   ("0.0", "7"),
                   ("0.0", "70"), ]
    else:
        domains = [("-0.1", "0.1"),
                   ("-1", "1"),
                   ("-10", "10"),
                   ("-100", "100"), ]

    main_lines = assemble_error_main(mpfr_funcname,
                                     [libm_funcname] + gen_funcnames,
                                     header_fname, domains)
    main_fname = "main.c"
    with open(main_fname, "w") as f:
        f.write("\n".join(main_lines))

    os.chdir(start)


def handle_work_item(func):
    func.remove_let()

    if func.arguments[0].source != "x":
        var = func.arguments[0]
        x = fpcore.ast.Variable("x")
        func.arguments[0] = x
        func = func.substitute(var, x)

    # TODO: figure out valid domain
    domain = Interval("(- INFINITY)", "INFINITY")
    start = os.getcwd()
    if not path.isdir("generated"):
        os.mkdir("generated")
    os.chdir("generated")
    generate_all_code(func, domain)
    os.chdir(start)
    return func


def main(argv):
    logger.warning("Currently unsound")

    args = parse_arguments(argv)

    # Read all the files, each file may have multiple functions
    work_items = list()
    for fname in args.fnames:
        with open(fname, "r") as f:
            text = f.read()

        some_funcs = fpcore.parse(text)
        work_items.extend(some_funcs)

    # Filter the functions
    old_work_items = work_items
    work_items = list()
    nag_shown = False
    for func in old_work_items:
        if len(func.arguments) == 1:
            work_items.append(func)
            continue
        if not nag_shown:
            msg = "Currently only functions in a single variable are supported"
            logger.warning(msg)
            nag_shown = True
        name = func.get_any_name() or func
        logger.warning("Dropping {}", name)

    # Run the identity finder
    tuples = [handle_work_item(func) for func in work_items]

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
