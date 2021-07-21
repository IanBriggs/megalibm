

import datetime
import inspect
import os.path as path
import sys


class Logger():
    # +-----------------------------------------------------------------------+
    # | Level Constants                                                       |
    # +-----------------------------------------------------------------------+
    NONE = -10
    QUIET = 0
    LOW = 10
    MEDIUM = 20
    HIGH = 30
    EXTRA = 40
    CONSTANT_DICT = {"none":   NONE,
                     "quiet":  QUIET,
                     "low":    LOW,
                     "medium": MEDIUM,
                     "high":   HIGH,
                     "extra":  EXTRA}

    @classmethod
    def str_to_level(self_class, string):
        try:
            return int(string)
        except ValueError:
            pass

        norm = string.lower()
        return self_class.CONSTANT_DICT[norm]

    # +-----------------------------------------------------------------------+
    # | Color printing using ANSI escape codes                                |
    # +-----------------------------------------------------------------------+
    COLOR_CODES = {
        "black":   "\x1b[30m",
        "red":     "\x1b[31m",
        "green":   "\x1b[32m",
        "yellow":  "\x1b[33m",
        "blue":    "\x1b[34m",
        "magenta": "\x1b[35m",
        "cyan":    "\x1b[36m",
        "white":   "\x1b[37m",
        "none":    "\x1b[0m",
    }

    @classmethod
    def color_text(self_class, color, text):
        color_code = self_class.COLOR_CODES[color.lower()]
        none = self_class.COLOR_CODES["none"]
        return "{}{}{}".format(color_code, text, none)

    @classmethod
    def strip_color(self_class, text):
        for code in self_class.COLOR_CODES.values():
            text = text.replace(code, "")
        return text

    @classmethod
    def black(self_class, text):
        return self_class.color_text("black", text)

    @classmethod
    def red(self_class, text):
        return self_class.color_text("red", text)

    @classmethod
    def green(self_class, text):
        return self_class.color_text("green", text)

    @classmethod
    def yellow(self_class, text):
        return self_class.color_text("yellow", text)

    @classmethod
    def blue(self_class, text):
        return self_class.color_text("blue", text)

    @classmethod
    def magenta(self_class, text):
        return self_class.color_text("magenta", text)

    @classmethod
    def cyan(self_class, text):
        return self_class.color_text("cyan", text)

    @classmethod
    def white(self_class, text):
        return self_class.color_text("white", text)

    # +-----------------------------------------------------------------------+
    # | Class variables                                                       |
    # +-----------------------------------------------------------------------+

    # Current level
    LOG_LEVEL = LOW

    # Current output
    LOG_FILE = sys.stdout

    # Number of registered loggers
    LOGGER_COUNT = 0

    @classmethod
    def set_log_level(self_class, level):
        # Check level
        if type(level) != int:
            msg = "level must be an int, found '{}'".format(type(level))
            raise TypeError(msg)

        # Set class variable
        self_class.LOG_LEVEL = level

    @classmethod
    def send_log_to_stderr(self_class):
        # This should only be called once during the runtime
        if self_class.LOG_FILE != sys.stdout:
            msg = "Attempted to redirect log output twice"
            raise RuntimeError(msg)
        self_class.LOG_FILE = sys.stderr

    @classmethod
    def set_log_filename(self_class, filename):
        # This should only be called once during the runtime
        if self_class.LOG_FILE != sys.stdout:
            msg = "Attempted to redirect log output twice"
            raise RuntimeError(msg)

        # Open the indicated logfile
        # todo: What should be done if this fails or there are issues
        #       during the lifetime?
        self_class.LOG_FILE = open(filename, "w")

    # +-----------------------------------------------------------------------+
    # | Member functions                                                      |
    # +-----------------------------------------------------------------------+
    def __init__(self, level=None, color=None, def_color=None):
        # Use defaults if arguments aren't set
        #     Note: ternary has to be used for level since a level of 0 is
        #           valid (ie '0 if 0 is not None else 40' == 0 vs
        #                                        '0 or 40' == 40)
        self.level = level if level is not None else Logger.EXTRA
        self.color = color or Logger.white
        self.def_color = def_color or Logger.white

        # Figure out the module for this Logger
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])

        # Sometimes it can't be found
        if module is None:
            self.module = "Unknown"

        # When it can be found get the filename
        else:
            filename = module.__file__
            base = path.basename(filename)
            self.module = path.splitext(base)[0]

        # Keep track of the number of Loggers
        Logger.LOGGER_COUNT += 1

    def __del__(self):
        # If this was the last logger and the log had been sent to a file close
        #     the file
        # todo: This is only called when the object is garbage collected
        #       and so has no guarantee that it will ever be called
        #       This means we will most likely leave an open file handle on
        #       exit, but I don't know of a better way to do this
        #       Context managers won't help since a logger is meant to be
        #       made at the beginning of a module
        Logger.LOGGER_COUNT -= 1
        if Logger.LOGGER_COUNT == 0 and (Logger.LOG_FILE != sys.stdout
                                         and Logger.LOG_FILE != sys.stderr):
            Logger.LOG_FILE.close()
            Logger.LOG_FILE = None

    def __call__(self, message, *args):
        # Convenience alias for log
        self.log(message, *args)

    def should_log(self, level=None):
        # With no level check against the member variable
        level = self.level if level is None else level
        return level <= Logger.LOG_LEVEL

    def _log(self, formatted_message, pre=None, out=None):
        # If out is not set then use the member output
        out = out or Logger.LOG_FILE

        # Add beginning parts to message and finish all formatting
        pre = pre or ""
        mod = self.color(self.module)
        full_message = "{} {}:{} {}".format(datetime.datetime.now(),
                                            mod,
                                            pre,
                                            formatted_message)

        # If redirecting then remove color information
        if not out.isatty():
            full_message = Logger.strip_color(full_message)

        # Finally print the message
        print(full_message, file=out)

        # Return for possible reuse of the message
        return full_message

    def format_message(self, message, *args):
        # Don't try to format if args aren't given
        # This allows logging of an object without the caller using an
        # explicit string conversion
        if len(args) == 0:
            return str(message)
        return message.format(*args)

    def log(self, message, *args):
        # Log message based on current level and member log level
        if self.should_log():
            formatted_message = self.format_message(message, *args)
            self._log(formatted_message)

    def llog(self, level, message, *args):
        # Log message based on current level and argument log level
        if self.should_log(level):
            formatted_message = self.format_message(message, *args)
            self._log(formatted_message)

    def dlog(self, message, *args):
        # Log while using the current function name
        if self.should_log():
            frame = inspect.stack()[1]
            funcname = self.def_color(frame.function)
            formatted_funcname = " {}:".format(funcname)
            formatted_message = self.format_message(message, *args)
            self._log(formatted_message, pre=formatted_funcname)

    def blog(self, description, text, level=None):
        # Log a block of text
        if self.should_log(level):
            self._log("{}:\n\n{}\n".format(description, text))

    def warning(self, message, *args):
        # Warning print at level quiet or above
        if self.should_log(Logger.QUIET):

            # Warnings go to stderr
            warn = " {}:".format(Logger.yellow("WARNING"))
            formatted_message = self.format_message(message, *args)
            full_message = self._log(formatted_message, warn, sys.stderr)

            # If logging has been sent to a file also send message to that file
            if Logger.LOG_FILE != sys.stdout and Logger.LOG_FILE != sys.stderr:
                print(Logger.strip_color(full_message), file=Logger.LOG_FILE)

    def error(self, message, *args):
        # Errors always go to stderr
        err = " {}:".format(Logger.red("ERROR"))
        formatted_message = self.format_message(message, *args)
        full_message = self._log(formatted_message, err, sys.stderr)

        # If logging has been sent to a file also send message to that file
        if Logger.LOG_FILE != sys.stdout and Logger.LOG_FILE != sys.stderr:
            print(Logger.strip_color(full_message), file=Logger.LOG_FILE)


def main(argv):
    logger.set_log_level(Logger.EXTRA)

    logger("Logging has multiple levels: {}", " ".join(Logger.CONSTANT_DICT))
    logger("These turn into numbers:")
    for name in Logger.CONSTANT_DICT:
        logger("  {} -> {}", name, Logger.str_to_level(name))

    logger("Logging can print in color:")
    logger(Logger.black("  black"))
    logger(Logger.red("  red"))
    logger(Logger.green("  green"))
    logger(Logger.yellow("  yellow"))
    logger(Logger.blue("  blue"))
    logger(Logger.magenta("  magenta"))
    logger(Logger.cyan("  cyan"))
    logger(Logger.white("  white"))

    logger("Logging can be done multiple ways:")
    print()
    print("> logger.log(\"hello world\")")
    logger.log("hello world")
    print()
    print("> logger.log(\"formatting is {}\", \"great\")")
    logger.log("formatting is {}", "great")
    print()
    print("> logger(\"Can be called directly\")")
    logger("Can be called directly")
    print()
    print("> logger.llog(Logger.QUIET, \"Can specify a logging level\")")
    logger.llog(Logger.QUIET, "Can specify a logging level")
    print()
    print("> logger.dlog(\"Can automatically include the def name\")")
    logger.dlog("Can automatically include the def name")
    print()
    print("> logger.blog(\"Can\", \"log blocks\\nof\\ntext\")")
    logger.blog("Can", "log blocks\nof\ntext")
    print()
    print("> logger.warning(\"Can warn\")")
    logger.warning("Can warn")
    print()
    print("> logger.error(\"or error\")")
    logger.error("or error")

    return 0


if __name__ == "__main__":
    logger = Logger(color=Logger.cyan, def_color=Logger.green)

    retcode = 130  # meaning "Script terminated by Control-C"

    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("")
        print("Goodbye")

    sys.exit(retcode)
