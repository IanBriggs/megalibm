#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import os.path as path
import shutil
import sys

from matplotlib import pyplot as plt
from error_function import error_function
from numeric_types import FP64

from time_function import time_function

BIN_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(BIN_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
REQ_DIR = path.join(GIT_DIR, "requirements")
EGG_DIR = path.join(REQ_DIR, "snake_egg", "target", "release")
AUTOGEN_DIR = path.join(GIT_DIR, 'autogen')

GEN_DIR = path.join(GIT_DIR, "generated")


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
                        help="Directory with the fpcore files")
    parser.add_argument("nightly_location", 
                        help="Nightly location")
    args = parser.parse_args(argv[1:])

    Logger.set_log_level(Logger.str_to_level(args.verbosity))

    if args.log_file is not None:
        Logger.set_log_filename(args.log_file)

    args.fnames = [path.join(AUTOGEN_DIR, fn)
                                for fn in os.listdir(args.dirname)
                                if fn.endswith(".fpcore")]
    # for fname in os.listdir(args.dirname):
    #     print("DNNN", fname)
    #     if os.path.isfile(fname) and fname.endswith(".fpcore"):
    #         args.fnames.append(fname)
    #     else:
    #         args.fnames.extend([path.join(fname, fn)
    #                             for fn in os.listdir(dn)
    #                             if fn.endswith(".fpcore")])

    args.fnames.sort()

    logger.dlog("Settings:")
    logger.dlog("    dirname: {}", args.dirname)
    logger.dlog("  verbosity: {}", args.verbosity)
    logger.dlog("   log-file: {}", args.log_file)

    return args

def c_ize_name(function):
    name = {p.name: p.value for p in function.properties}.get("name", "NoName")
    replace_chars = {
        '"': "",
        "'": "",
        "(": "",
        ")": "",
        ",": "_",
        " ": "_",
        ".": "_",
        "-": "_",
        ":": "_",
        "+": "plus",
    }
    for frm, to in replace_chars.items():
        name = name.replace(frm, to)
    while "__" in name:
        name = name.replace("__", "_")
    return name

def get_domains(domain):
    inf = str(domain[0])
    sup = str(domain[1])
    if inf == "(- PI_2)" and sup == "PI_2":
        domains = [Interval("-1.57079633", "1.57079633"),
                   Interval("-0.78539816", "0.78539816"),
                   Interval("-0.39269908", "0.39269908"),
                   Interval("-0.19634954", "0.19634954")]
    elif inf == "(- 20)" and sup == "20":
        domains = [Interval("-20", "20"),
                   Interval("-16", "16"),
                   Interval("-2", "2"),
                   Interval("-0.5", "0.5")]
    elif inf == "(- 0.577)" and sup == "0.577":
        domains = [Interval("-0.577", "0.577"),
                   Interval("-0.5", "0.5"),
                   Interval("-0.25", "0.25"),
                   Interval("-0.125", "0.125")]
    elif inf == "(- 1)" and sup == "1":
        domains = [Interval("-1", "1"),
                   Interval("-0.5", "0.5"),
                   Interval("-0.25", "0.25"),
                   Interval("-0.125", "0.125")]
    elif inf == "0" and sup == "2":
        domains = [Interval("0", "2"),
                   Interval("0", "1"),
                   Interval("0", "0.5"),
                   Interval("0", "0.25")]
    elif inf == "0" and sup == "1":
        domains = [Interval("0", "1"),
                   Interval("0", "0.5"),
                   Interval("0", "0.25"),
                   Interval("0", "0.125")]
    elif inf == "(- 1)" and sup == "INFINITY":
        domains = [Interval("-1", "64"),
                   Interval("-1", "16"),
                   Interval("-1", "4"),
                   Interval("-1", "-0.5")]
    elif inf == "0" and sup == "INFINITY":
        domains = [Interval("0", "64"),
                   Interval("0", "16"),
                   Interval("0", "4"),
                   Interval("0", "0.5")]
    elif inf == "1" and sup == "INFINITY":
        domains = [Interval("1", "64"),
                   Interval("1", "16"),
                   Interval("1", "4"),
                   Interval("1", "1.5")]
    elif inf == "(- INFINITY)" and sup == "INFINITY":
        domains = [Interval("-32", "32"),
                   Interval("-8", "8"),
                   Interval("-2", "2"),
                   Interval("-1", "1")]
    else:
        domains = [Interval("-32", "32"),
                   Interval("-8", "8"),
                   Interval("-2", "2"),
                   Interval("-1", "1")]
    return domains


def format_float(number):
    # Check if the number is smaller than 1 and has an exponent
    if abs(number) < 1 and 'e' in str(number):
        # Format the number with 2 digits after the decimal and the correct exponent
        return "{:.2e}".format(number)
    else:
        # Format the number with 2 digits after the decimal
        return "{:.2f}".format(number)
    

def save_domain_plot(left_data, right_data, left_name, right_name, fname, samples= 1 << 17):
    left_data["max_cr_abs_error"] = left_data["cr_abs_error"].rolling(
        window=samples//512).max()
    right_data["max_cr_abs_error"] = left_data["max_cr_abs_error"]

    y_min = 0
    y_max = max(left_data["f_abs_error"] + right_data["f_abs_error"])

    _, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

    left_data.plot.scatter(x="input", y="f_abs_error", s=2**-4, ax=axes[0])
    left_data.plot.line(x="input", y="max_cr_abs_error", color="black",
                        linewidth=2, legend=False, ax=axes[0])

    right_data.plot.scatter(x="input", y="f_abs_error", s=2**-4, ax=axes[1])
    right_data.plot.line(x="input", y="max_cr_abs_error", color="black",
                         linewidth=2, legend=False, ax=axes[1])

    if left_name is not None:
        axes[0].set_title(f"Absolute error for {left_name}")
    else:
        axes[0].set_title(f"Absolute error")

    if right_name is not None:
        axes[1].set_title(f"Absolute error for {right_name}")
    else:
        axes[1].set_title(f"Absolute error")

    axes[0].set_xlabel("Input")
    axes[1].set_xlabel("Input")
    axes[0].set_ylabel("Error")
    axes[1].set_ylabel("Error")

    left_y_min, left_y_max = axes[0].get_ylim()
    right_y_min, right_y_max = axes[1].get_ylim()
    y_min = min(left_y_min, right_y_min)
    y_max = min(left_y_max, right_y_max)
    axes[0].set_ylim(0, y_max)
    axes[1].set_ylim(0, y_max)

    plt.tight_layout()

# TODO NAME
    plt.savefig(fname)

    return axes


def generate_all_code(function, domain, location):
    name = c_ize_name(function)
    target = lambdas.types.Impl(function, domain)
    print("NAME", name)

    my_lambdas = synthesize(target)

    # TODO: handle numeric type current only impl FP64
    # CR and Libm source code
    libm_func_name = f"libm_{name}"
    libm_sig, libm_src = lambdas.generate_libm_c_code(target, libm_func_name)
    logger.blog("C libm function", "\n".join(libm_src))

    mpfr_func_name = f"mpfr_{name}"
    mpfr_sig, mpfr_src = lambdas.generate_mpfr_c_code(target, mpfr_func_name)
    logger.blog("C mpfr function", "\n".join(mpfr_src))

    OUT_DIR = location + f"{name}/" 
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR) 
    
    # Copy header files to run c code and generate data
    os.chdir(OUT_DIR)
    shutil.copytree(GIT_DIR + "/include", OUT_DIR + "/include",
                    dirs_exist_ok=True)
    
    domains = get_domains(domain)

    # Move to out dir to compile and link files
    os.chdir(OUT_DIR)

    json_dict = dict()
    best_lambda_ranges = None
    best_lambda_plot_data = dict()
    lambda_func_name = None
    least_err  = float("inf")
    for i, lam in enumerate(my_lambdas):
        try:
            func_name = f"my_{name}_{i}"
            sig, src = lambdas.generate_c_code(lam, func_name)
            lambda_code = "\n".join(src)
            libm_code = "\n".join(libm_src)
            oracle_code = "\n".join(mpfr_src)
            logger.blog("C function", "\n".join(src))
            # TODO : input numeric_type from args
            lambda_err_sum = 0
            json_ranges = dict()
            plot_data = dict()
            for domain in domains:
                domain_str = str(domain)
                lambda_time =  time_function(numeric_type=FP64,
                                            c_function_name=func_name,
                                            c_code=lambda_code,
                                            domain=domain)
                reference_time = time_function(numeric_type=FP64,
                                                    c_function_name=libm_func_name,
                                                    c_code=libm_code,
                                                    domain=domain)
                lambda_error = error_function(numeric_type=FP64,
                                                samples=2**17,
                                                c_function_name=func_name,
                                                c_code=lambda_code,
                                                oracle_function_name=mpfr_func_name,
                                                oracle_code=oracle_code,
                                                domain=domain)
                reference_error = error_function(numeric_type=FP64,
                                                samples=2**17,
                                                c_function_name=libm_func_name,
                                                c_code=libm_code,
                                                oracle_function_name=mpfr_func_name,
                                                oracle_code=oracle_code,
                                                domain=domain)
                
                if domain_str not in plot_data:
                    plot_data[domain_str] = dict()

                plot_data[domain_str]["lambda_error"] = lambda_error
                plot_data[domain_str]["reference_error"] = reference_error
                
                json_range = {
                    "MLM time": float(format_float(lambda_time)),
                    "Reference time": float(format_float(reference_time)),
                    "MLM error": float(format_float(lambda_error["f_abs_error"].max())),
                    "Reference error":float(format_float(reference_error["f_abs_error"].max())),
                }

                json_ranges[domain_str] = json_range
                
                lambda_err_sum += lambda_error["f_abs_error"].max()
            
            if lambda_err_sum < least_err:
                least_err = lambda_err_sum
                best_lambda_ranges = json_ranges
                lambda_func_name = func_name
                best_lambda_plot_data = plot_data

            # gen_sigs.append(sig)
            # gen_srcs.append(src)
            # gen_func_names.append(func_name)
            # gen_lams.append(lam)
        except cmd_sollya.FailedGenError:
            logger.warning("Unable to generate polynomial, skipping")

    if not best_lambda_ranges:
        return False
    
    json_dict["table_data"] = best_lambda_ranges
    json_dict["func_name"] = lambda_func_name

    # SAVE plots for the best performing lambda
    for idx, domain in enumerate(sorted(best_lambda_ranges.keys())):
        fname = OUT_DIR + f"/{lambda_func_name}_domain_{idx}_absolute_error_abs_max_errors.png"
        save_domain_plot(best_lambda_plot_data[str(domain)]["lambda_error"], best_lambda_plot_data[str(domain)]["reference_error"], lambda_func_name, libm_func_name, fname)
        
    with open( OUT_DIR + 'data.json' , 'w') as json_file:
        json.dump(json_dict, json_file)

    return True


def handle_work_item(func, nightly_info):
    logger("Working on: {}", c_ize_name(func))
    func.remove_let()

    var = "x"
    if func.arguments[0].source != "x":
        var = func.arguments[0]
        x = fpcore.ast.Variable("x")
        func.arguments[0] = x
        func = func.substitute(var, x)

   # Create gen dirs 
    THIS_GEN_DIR = GEN_DIR + f"/{nightly_info['nightly_timestamp']}/"
    if not os.path.exists(THIS_GEN_DIR):
        os.mkdir(THIS_GEN_DIR) 
    GEN_FOLDER = THIS_GEN_DIR + "generated/"
    if not os.path.exists(GEN_FOLDER):
        os.mkdir(GEN_FOLDER) 

    # func.extract_domain()
    domain = func.extract_domain()["x"] if  "x" in func.extract_domain() else func.extract_domain()
    did_generation = False
    try:
        # DEF something weird
        did_generation = generate_all_code(func, domain, GEN_FOLDER)
    except Exception as e:
        logger.warning("Caught exception {}", e)
    if not did_generation:
        # REMOVE generated fir for the function to make website
        shutil.rmtree(f"{GEN_FOLDER}{c_ize_name(func)}")
        logger.warning("Unable to generate for {}", c_ize_name(func))
    # os.chdir(start)
    return func

def main(argv):
    logger.warning("Currently unsound")

    args = parse_arguments(argv)
    print("ARGS", args)

    NIGHTLY_LOCATION = args.nightly_location
    NIGHTLY_TS = NIGHTLY_LOCATION.split("/")[-1]

    nightly_info = {
        "nightly_location": NIGHTLY_LOCATION,
        "nightly_timestamp": NIGHTLY_TS
    }


    # Read all the files, each file may have multiple functions
    work_items = list()
    for fname in args.fnames:
        logger("Reading: {}", fname)
        with open(fname, "r") as f:
            text = f.read()
            print("TEXT", text)

        some_funcs = fpcore.parse(text)
        print("SOMFUNC", some_funcs, type(some_funcs))
        work_items.append(some_funcs)
    print("WORK ITEMS", work_items)
    print("WORK ITEMS", work_items[0], type(work_items[0]))
    # Filter the functions
    old_work_items = work_items
    work_items = list()
    nag_shown = False
    for func in old_work_items:
        print("FUNC", func, type(func))
        if len(func.arguments) == 1:
            work_items.append(func)
            continue
        if not nag_shown:
            msg = "Currently only functions in a single variable are supported"
            logger.warning(msg)
            nag_shown = True
        name = func.get_any_name() or func
        logger.warning("Dropping {}", name)

    print("WORK ITEMS", work_items)
    print("WORK ITEMS", work_items[0], type(work_items[0]))

    # Run the identity finder
    tuples = [handle_work_item(func, nightly_info) for func in work_items]

    return 0



if __name__ == "__main__":
    timer.start()
    try:
        return_code = main(sys.argv)
        # return_code = main(ar)
    except KeyboardInterrupt:
        return_code = 130  # meaning "Script terminated by Control-C"
        print("")
        print("Goodbye")

    timer.stop()

    logger("Elapsed time: {:4f} sec", timer.elapsed())

    sys.exit(return_code)
2