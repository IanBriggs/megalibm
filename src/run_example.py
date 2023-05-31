#!/usr/bin/env python3

import argparse
import os
import os.path as path
import sys
from error_function import error_function

import fpcore
import lambdas
from time_function import time_function

EXAMPLE_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
sys.path.append(SRC_DIR)

from assemble_c_files import *
from utils import Logger, Timer

logger = Logger(color=Logger.green, level=Logger.LOW)
timer = Timer()


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
    logger.dlog("      dirname: {}", args.dirname)
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
        with open(reference_filename, "r") as f:
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


def main(argv):
    args = parse_arguments(argv)

    # BAD! Do not load arbitrary python code and run it.
    with open(args.example_file, "r") as f:
        example = f.read()
    example_globals = dict()
    exec(example, globals=example_globals)

    # Get the lambda
    lambda_expression = example_globals.get("lambda_expression")
    if lambda_expression is None:
        logger.error("File '{}' must define the variable `lambda_expression`",
                     args.example_file)
        sys.exit(1)

    # And name
    lambda_function_name = example_globals.get("lambda_function_name")
    if lambda_function_name is None:
        lambda_function_name = "lambda"

    # Generate the code
    lambda_expression.type_check()
    lambda_signature, lines = lambdas.generate_c_code(lambda_expression,
                                                      lambda_function_name)
    lambda_code = "\n".join(lines)

    precision = oracle_impl_type.numeric_type

    # Use the function and type to create an oracle
    oracle_impl_type = lambda_expression.out_type
    oracle_function_name = "oracle"
    oracle_signature, lines = lambdas.generate_mpfr_c_code(oracle_impl_type,
                                                           oracle_function_name,
                                                           numeric_type=precision)
    oracle_code = "\n".join(lines)

    # Get the reference, if present
    reference_function_name, reference_code = determine_reference(
        example_globals)

    # Get some configuration values
    regions_per_range = example_globals.get("regions_per_range", 256)
    samples_per_region = example_globals.get("samples_per_region", 4096)
    points_per_pad = example_globals.get("points_per_pad", 4096)
    repeats_per_time = example_globals.get("repeats_per_time", 100000)

    # Prepare output json structure
    json_dict = {
        "example_filename": args.example_filename,
        "precision": precision,
        "lambda_code": lambda_code,
        "lambda_function_name": lambda_function_name,
        "oracle_code": oracle_code,
        "oracle_function_name": oracle_function_name,
        "reference_code": reference_code,
        "reference_function_name": reference_function_name,
        "regions_per_range": regions_per_range,
        "samples_per_region": samples_per_region,
        "points_per_pad": points_per_pad,
        "repeats_per_time": repeats_per_time,
    }

    # Get input ranges
    input_ranges = example_globals.get("input_ranges")
    if input_ranges is None:
        logger.error("File '{}' must define the variable `input_ranges`",
                     args.example_file)
        sys.exit(1)

    # Run on all of them and add the data to our `json_dict`
    json_ranges = dict()
    for range in input_ranges:
        json_range = {
            "lambda_time": time_function(numeric_type=precision,
                                         points_per_pad=points_per_pad,
                                         repeats_per_time=repeats_per_time,
                                         c_function_name=lambda_function_name,
                                         c_code=lambda_code,
                                         rang=range),
            "reference_time": time_function(numeric_type=precision,
                                            points_per_pad=points_per_pad,
                                            repeats_per_time=repeats_per_time,
                                            c_function_name=reference_function_name,
                                            c_code=reference_code,
                                            rang=range),
            "lambda_error": error_function(numeric_type=precision,
                                           regions_per_range=regions_per_range,
                                           samples_per_region=samples_per_region,
                                           c_function_name=lambda_function_name,
                                           c_code=lambda_code,
                                           oracle_function_name=oracle_function_name,
                                           oracle_code=oracle_code,
                                           rang=range),
            "reference_error": error_function(numeric_type=precision,
                                              regions_per_range=regions_per_range,
                                              samples_per_region=samples_per_region,
                                              c_function_name=reference_function_name,
                                              c_code=reference_code,
                                              oracle_function_name=oracle_function_name,
                                              oracle_code=oracle_code,
                                              rang=range),
        }
        json_ranges[range] = json_range
    json_dict["range_data"] = json_ranges

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
