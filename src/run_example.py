#!/usr/bin/env python3

import argparse
import json
import os
import os.path as path
import shutil
import sys
from error_function import error_function

import fpcore
import lambdas
from numeric_types import FP64
from time_function import time_function
import pandas as pd
import matplotlib.pyplot as plt

EXAMPLE_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
GEN_DIR = path.join(GIT_DIR, "generated")
sys.path.append(SRC_DIR)

from assemble_c_files import *
from utils import Logger, Timer

logger = Logger(color=Logger.green, level=Logger.LOW)
timer = Timer()

import pprint 
pp = pprint.PrettyPrinter(indent=4)

def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Example runner')
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
    parser.add_argument("example_file",
                        help="File to run")
    parser.add_argument("nightly_location",
                        help="Nightly Location")
    
    args = parser.parse_args(argv[1:])

    Logger.set_log_level(Logger.str_to_level(args.verbosity))

    if args.log_file is not None:
        Logger.set_log_filename(args.log_file)

    if not os.path.exists(args.example_file):
        logger.error("Given `example_file` does not exist: '{}'",
                     args.example_file)
    if not os.path.isfile(args.example_file):
        logger.error("Given `example_file` is not a file: '{}'",
                     args.example_file)
        sys.exit(1)

    logger.dlog("Settings:")
    # logger.dlog("      dirname: {}", args.dirname)
    logger.dlog("    verbosity: {}", args.verbosity)
    logger.dlog("     log-file: {}", args.log_file)
    logger.dlog(" example_file: {}", args.example_file)
    return args


def determine_reference(environment):
    # Allow multiple ways of giving a reference code and function name:
    # 1. Just a filename, we will read it for the code and guess the function
    #    name
    # 2. A filename and a function name, we will read the file for the code
    # 3. Code and a function name
    # 4. Nothing, there is no reference
    reference_filename = environment.get("reference_filename", None)
    reference_function_name = environment.get("reference_function_name", None)
    reference_code = environment.get("reference_code", None)
    if (reference_filename is not None
        and reference_code is None
            and reference_function_name is None):
        with open( GIT_DIR + "/examples/" + reference_filename, "r") as f:
            reference_code = f.read()
        reference_function_name = reference_filename.rstrip(".c")
    elif (reference_filename is not None
          and reference_code is not None
          and reference_function_name is None):
        with open(reference_filename, "r") as f:
            reference_code = f.read()
    elif (reference_filename is None
          and reference_code is not None
          and reference_function_name is not None):
        pass
    else:
        logger.error("Invalid reference configuration:")
        logger.error("      `reference_filename`: {}", reference_filename)
        logger.error(" `reference_function_name`: {}", reference_function_name)
        logger.error("          `reference_code`: {}", reference_code)
        sys.exit(1)

    return reference_function_name, reference_code

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
    axes[0].set_ylim(y_min, y_max)
    axes[1].set_ylim(y_min, y_max)

    plt.tight_layout()

# TODO NAME
    plt.savefig(fname)

    return axes

def format_float(number):
    # Check if the number is smaller than 1 and has an exponent
    if abs(number) < 1 and 'e' in str(number):
        # Format the number with 2 digits after the decimal and the correct exponent
        return "{:.2e}".format(number)
    else:
        # Format the number with 2 digits after the decimal
        return "{:.2f}".format(number)

def main(argv):
    args = parse_arguments(argv)

    print(args)
    NIGHTLY_LOCATION = args.nightly_location
    NIGHTLY_TS = NIGHTLY_LOCATION.split("/")[-1]

    # BAD! Do not load arbitrary python code and run it.
    with open(args.example_file, "r") as f:
        example = f.read()
    example_globals = dict()
    exec(example, example_globals)

    # Get the lambda and type check
    lambda_expression = example_globals.get("lambda_expression")
    lambda_expression.type_check()

    if lambda_expression is None:
        logger.error("File '{}' must define the variable `lambda_expression`",
                     args.example_file)
        sys.exit(1)

    # And name
    lambda_function_name = example_globals.get("lambda_function_name")
    if lambda_function_name is None:
        lambda_function_name = "lambda"

    # Precision and impl
    oracle_impl_type = lambda_expression.out_type
    precision = example_globals.get("numeric_type", FP64)
    func_type = example_globals.get("func_type", FP64)

    # Generate the code
    lambda_signature, lines = lambdas.generate_c_code(lambda_expression,
                                                      lambda_function_name, numeric_type=precision, func_type=func_type)
    lambda_code = "\n".join(lines)

    print(lambda_code)

    # Use the function and type to create an oracle
    oracle_function_name = "oracle"
    oracle_signature, lines = lambdas.generate_mpfr_c_code(oracle_impl_type,
                                                           oracle_function_name,
                                                           numeric_type=func_type)
    oracle_code = "\n".join(lines)

    # Get the reference, if present
    reference_function_name, reference_code = determine_reference(
        example_globals)
    

    # Get some configuration values
    # regions_per_range = example_globals.get("regions_per_range", 256)
    # samples_per_region = example_globals.get("samples_per_region", 4096)
    # points_per_pad = example_globals.get("points_per_pad", 4096)
    # repeats_per_time = example_globals.get("repeats_per_time", 100000)

    # # Prepare output json structure
    # json_dict = {
    #     "example_filename": args.example_file,
    #     "precision": precision,
    #     "lambda_code": lambda_code,
    #     "lambda_function_name": lambda_function_name,
    #     "oracle_code": oracle_code,
    #     "oracle_function_name": oracle_function_name,
    #     "reference_code": reference_code,
    #     "reference_function_name": reference_function_name,
    #     "regions_per_range": regions_per_range,
    #     "samples_per_region": samples_per_region,
    #     "points_per_pad": points_per_pad,
    #     "repeats_per_time": repeats_per_time,
    # }

    # Get input ranges
    input_ranges = example_globals.get("input_ranges")
    if input_ranges is None:
        logger.error("File '{}' must define the variable `input_ranges`",
                     args.example_file)
        sys.exit(1)

    # Create gen dirs 
    THIS_GEN_DIR = GEN_DIR + f"/{NIGHTLY_TS}/"
    if not os.path.exists(THIS_GEN_DIR):
        os.mkdir(THIS_GEN_DIR) 
    GEN_FOLDER = THIS_GEN_DIR + "generated/"
    if not os.path.exists(GEN_FOLDER):
        os.mkdir(GEN_FOLDER) 
    OUT_DIR = GEN_FOLDER + f"{lambda_function_name}/" 
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR) 
    
    # Copy header files to run c code and generate data
    os.chdir(OUT_DIR)
    shutil.copytree(GIT_DIR + "/include", OUT_DIR + "/include")


    # Run on all of them and add the data to our `json_dict`

    json_ranges = dict()
    json_dict = dict()

    for idx, domain in enumerate(input_ranges):
        lambda_time =  time_function(numeric_type=func_type,
                                         c_function_name=lambda_function_name,
                                         c_code=lambda_code,
                                         domain=domain)
        reference_time = time_function(numeric_type=func_type,
                                            c_function_name=reference_function_name,
                                            c_code=reference_code,
                                            domain=domain)
        lambda_error = error_function(numeric_type=func_type,
                                           samples=2**17,
                                           c_function_name=lambda_function_name,
                                           c_code=lambda_code,
                                           oracle_function_name=oracle_function_name,
                                           oracle_code=oracle_code,
                                           domain=domain)
        reference_error = error_function(numeric_type=func_type,
                                           samples=2**17,
                                           c_function_name=reference_function_name,
                                           c_code=reference_code,
                                           oracle_function_name=oracle_function_name,
                                           oracle_code=oracle_code,
                                           domain=domain)
        
        fname = OUT_DIR + f"/{lambda_function_name}_domain_{idx}_absolute_error_abs_max_errors.png"
        
        save_domain_plot(lambda_error, reference_error, lambda_function_name, reference_function_name, fname)
        
        json_range = {
            "MLM time": float(format_float(lambda_time)),
            "Reference time": float(format_float(reference_time)),
            "MLM error": float(format_float(lambda_error["f_abs_error"].max())),
            "Reference error":float(format_float(reference_error["f_abs_error"].max())),
        }
        dom_str = str(domain)
        json_ranges[dom_str] = json_range
    pp.pprint(json_ranges)

    json_dict["table_data"] = json_ranges
    json_dict["func_name"] = lambda_function_name

    with open( OUT_DIR + 'data.json' , 'w') as json_file:
        json.dump(json_dict, json_file)
    # 

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
