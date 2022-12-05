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

import fpcore
import lambdas
import cmd_sollya
import find_identities

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
                        default="medium",
                        const="medium",
                        choices=list(Logger.CONSTANT_DICT),
                        help="Set output verbosity")
    parser.add_argument("-l", "--log-file",
                        nargs="?",
                        type=str,
                        help="Redirect logging to given file.")
    parser.add_argument("dirname",
                        help="Directory with the fpcore files",
                        nargs="+")
    args = parser.parse_args(argv[1:])

    Logger.set_log_level(Logger.str_to_level(args.verbosity))

    if args.log_file is not None:
        Logger.set_log_filename(args.log_file)

    args.fnames = list()
    for dn in args.dirname:
        if os.path.isfile(dn) and dn.endswith(".fpcore"):
            args.fnames.append(dn)
        else:
            args.fnames.extend([path.join(dn, fn)
            for fn in os.listdir(dn)
            if fn.endswith(".fpcore")])

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

    my_lambdas = synthesize(target)

    gen_lams = list()
    gen_sigs = list()
    gen_srcs = list()
    gen_func_names = list()
    for i, lam in enumerate(my_lambdas):
        try:
            func_name = f"my_{name}_{i}"
            sig, src = lambdas.generate_c_code(lam, func_name)
            logger.blog("C function", "\n".join(src))
            gen_sigs.append(sig)
            gen_srcs.append(src)
            gen_func_names.append(func_name)
            gen_lams.append(lam)
        except cmd_sollya.FailedGenError:
            logger.warning("Unable to generate polynomial, skipping")

    if len(gen_func_names) == 0:
        return False

    libm_func_name = f"libm_{name}"
    libm_sig, libm_src = lambdas.generate_libm_c_code(target, libm_func_name)
    logger.blog("C libm function", "\n".join(libm_src))

    mpfr_func_name = f"mpfr_{name}"
    mpfr_sig, mpfr_src = lambdas.generate_mpfr_c_code(target, mpfr_func_name)
    logger.blog("C mpfr function", "\n".join(mpfr_src))

    start = os.getcwd()
    if not path.isdir(name):
        os.mkdir(name)
    os.chdir(name)

    header_lines = assemble_header([libm_sig, mpfr_sig] + gen_sigs)
    header_fname = "funcs.h"
    with open(header_fname, "w") as f:
        f.write("\n".join(header_lines))

    func_lines = assemble_functions(
        [libm_src, mpfr_src] + gen_srcs, header_fname)
    func_fname = "funcs.c"
    with open(func_fname, "w") as f:
        f.write("\n".join(func_lines))

    inf = str(domain[0])
    sup = str(domain[1])
    if inf == "(- PI_2)" and sup == "PI_2":
        domains = [("-1.57079633", "1.57079633"),
                   ("-0.78539816", "0.78539816"),
                   ("-0.39269908", "0.39269908"),
                   ("-0.19634954", "0.19634954")]
    elif inf == "(- 20)" and sup == "20":
        domains = [("-20", "20"),
                   ("-16", "16"),
                   ("-2", "2"),
                   ("-0.5", "0.5")]
    elif inf == "(- 0.577)" and sup == "0.577":
        domains = [("-0.577", "0.577"),
                   ("-0.5", "0.5"),
                   ("-0.25", "0.25"),
                   ("-0.125", "0.125")]
    elif inf == "(- 1)" and sup == "1":
        domains = [("-1", "1"),
                   ("-0.5", "0.5"),
                   ("-0.25", "0.25"),
                   ("-0.125", "0.125")]
    elif inf == "0" and sup == "2":
        domains = [("0", "2"),
                   ("0", "1"),
                   ("0", "0.5"),
                   ("0", "0.25")]
    elif inf == "0" and sup == "1":
        domains = [("0", "1"),
                   ("0", "0.5"),
                   ("0", "0.25"),
                   ("0", "0.125")]
    elif inf == "(- 1)" and sup == "INFINITY":
        domains = [("-1", "64"),
                   ("-1", "16"),
                   ("-1", "4"),
                   ("-1", "-0.5")]
    elif inf == "0" and sup == "INFINITY":
        domains = [("0", "64"),
                   ("0", "16"),
                   ("0", "4"),
                   ("0", "0.5")]
    elif inf == "1" and sup == "INFINITY":
        domains = [("1", "64"),
                   ("1", "16"),
                   ("1", "4"),
                   ("1", "1.5")]
    elif inf == "(- INFINITY)" and sup == "INFINITY":
        domains = [("-32", "32"),
                   ("-8", "8"),
                   ("-2", "2"),
                   ("-1", "1")]
    else:
        print(f"domain: ({inf}, {sup})")
        assert False

    func_body = function.to_html()

    generators = [str(lam) for lam in gen_lams]

    # Error measurement
    main_lines = assemble_error_main(name, func_body,
                                     mpfr_func_name,
                                     [libm_func_name] + gen_func_names,
                                     generators,
                                     header_fname, domains)
    main_fname = "error_main.c"
    with open(main_fname, "w") as f:
        f.write("\n".join(main_lines))

    # Timing measurement
    main_lines = assemble_timing_main(name, func_body,
                                     [libm_func_name] + gen_func_names,
                                     header_fname, domains)
    main_fname = "timing_main.c"
    with open(main_fname, "w") as f:
        f.write("\n".join(main_lines))


    os.chdir(start)
    return True

def handle_work_item(func):
    logger("Working on: {}", c_ize_name(func))
    func.remove_let()

    var = "x"
    if func.arguments[0].source != "x":
        var = func.arguments[0]
        x = fpcore.ast.Variable("x")
        func.arguments[0] = x
        func = func.substitute(var, x)

    func.extract_domain()
    domain = func.domains[var]
    start = os.getcwd()
    if not path.isdir("generated"):
        os.mkdir("generated")
    os.chdir("generated")
    if not generate_all_code(func, domain):
        logger.warning("Unable to generate for {}", c_ize_name(func))
    os.chdir(start)
    return func


def main(argv):
    logger.warning("Currently unsound")

    args = parse_arguments(argv)

    # Read all the files, each file may have multiple functions
    work_items = list()
    for fname in args.fnames:
        logger("Reading: {}", fname)
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
        return_code = main(sys.argv)
    except KeyboardInterrupt:
        return_code = 130  # meaning "Script terminated by Control-C"
        print("")
        print("Goodbye")

    timer.stop()

    logger("Elapsed time: {:4f} sec", timer.elapsed())

    sys.exit(return_code)
