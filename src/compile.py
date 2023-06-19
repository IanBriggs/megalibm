
from os import path
import shlex
import sys
import subprocess
from utils import Logger

logger = Logger(level=Logger.HIGH, color=Logger.green)

EXAMPLE_DIR = path.abspath("")
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")

def compile_file(filename: str,
                 compiler: str = None,
                 flags: list = None):
    # Defaults
    if compiler is None:
        compiler = "gcc"
    if flags is None:
        flags = ["-O3", "-mtune=native", "-fno-builtin", "-DNDEBUG"]

    # brew puts things in weird places
    if path.exists("/opt/homebrew/include"):
        flags.insert(0, "-I/opt/homebrew/include")

    # add our local dir
    if "GIT_DIR" in globals():
        flags.insert(0, f"-I{GIT_DIR}/include")
    else:
        flags.insert(0, "-Iinclude")

    objectname = filename.replace(".c", ".o")
    command = "{} {} {} -c -o {}".format(compiler,
                                         " ".join(flags),
                                         filename,
                                         objectname)

    p = subprocess.run(shlex.split(command), capture_output=True)

    if p.returncode != 0:
        logger.error("Compile command failed")
        logger.error("command: '{}'", command)
        logger.error("stdout:\n{}", p.stdout.decode("utf8"))
        logger.error("stderr:\n{}", p.stderr.decode("utf8"))
        sys.exit(1)

    return objectname


def link_files(filenames: list,
               binary_name: str,
               compiler: str = None,
               link_flags: list = None,
               ):
    # Defaults
    if compiler is None:
        compiler = "gcc"
    if link_flags is None:
        link_flags = ["-lmpfr", "-lgmp", "-lm"]

    # brew puts things in weird places
    if path.exists("/opt/homebrew/lib"):
        link_flags.insert(0, "-L/opt/homebrew/lib")

    command = "{} {} {} -o {}".format(compiler,
                                      " ".join(filenames),
                                      " ".join(link_flags),
                                      binary_name)

    p = subprocess.run(shlex.split(command), capture_output=True)

    if p.returncode != 0:
        logger.error("Link command failed")
        logger.error("command: '{}'", command)
        logger.error("stdout:\n{}", p.stdout.decode("utf8"))
        logger.error("stderr:\n{}", p.stderr.decode("utf8"))
        sys.exit(1)

    return binary_name
