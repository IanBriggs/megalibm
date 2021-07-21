#!/usr/bin/env python3

import argparse
import os.path as path
import sys

BIN_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(BIN_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
sys.path.append(SRC_DIR)

from utils import Logger, Timer

logger = Logger(Logger.HIGH, color=Logger.blue)
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
    args = parser.parse_args(argv[1:])

    Logger.set_log_level(Logger.str_to_level(args.verbosity))

    if args.log_file is not None:
        Logger.set_log_filename(args.log_file)

    logger.dlog("Settings:")
    logger.dlog("  verbosity: {}", args.verbosity)
    logger.dlog("   log-file: {}", args.log_file)

    return args


def main(argv):
    args = parse_arguments(argv)
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
