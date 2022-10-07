

from utils import Logger, Timer

from sly import Lexer

import sys


logger = Logger(level=Logger.EXTRA, color=Logger.blue)
timer = Timer()


ADDED_OPERATIONS = dict()


class FPCoreLexError(Exception):
    def __init__(self, msg, tok):
        self.msg = msg
        self.tok = tok


class FPCoreLexer(Lexer):
    tokens = {
        # Delimiters
        LP,  # left paren
        RP,  # right paren
        LB,  # left square bracket
        RB,  # right square bracket
        COLON,
        BANG,
        HASH,  # Bill's syntactic sugar

        # Literals
        RATIONAL,
        HEXNUM,
        DECNUM,
        STRING,

        # Symbols
        SYMBOL,

        # Keywords
        FPCORE,
        IF,
        LET,
        LET_STAR,
        WHILE,
        WHILE_STAR,
        FOR,
        FOR_STAR,
        TENSOR,
        TENSOR_STAR,
        CAST,
        ARRAY,
        DIGITS,

        # Constants
        CONSTANT,

        # Operations
        OPERATION,
    }

    # Ignored input
    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
    ignore_space = r"\s"
    ignore_comment = r"\;.*"

    LP = r"\("
    RP = r"\)"
    LB = r"\["
    RB = r"\]"
    COLON = r":"
    HASH = r"#"

    # From https://fpbench.org/spec/fpcore-2.0.html
    RATIONAL = r"[+-]?[0-9]+/[0-9]*[1-9][0-9]*"

    # From https://fpbench.org/spec/fpcore-2.0.html
    #     modified to be used in a case sensitive environment
    HEXNUM = r"[+-]?0[xX]([0-9a-fA-F]+(\.[0-9a-fA-F]+)?|\.[0-9a-fA-F]+)([pP][-+]?[0-9]+)?"

    # From https://fpbench.org/spec/fpcore-2.0.html
    DECNUM = r"[-+]?([0-9]+(\.[0-9]+)?|\.[0-9]+)(e[-+]?[0-9]+)?"

    # From https://fpbench.org/spec/fpcore-2.0.html
    #   added general whitespace to catch newlines
    #   added α-ωΑ-Ω
    #   added ×
    @_(r'"([\sα-ωΑ-Ω×\x20-\x21\x23-\x5b\x5d-\x7e]|\\["\\])*"')
    def STRING(self, t):
        self.lineno += t.value.count('\n')
        return t

    # From https://fpbench.org/spec/fpcore-2.0.html
    #   added α-ωΑ-Ω
    SYMBOL = r"[α-ωΑ-Ωa-zA-Z~!@$%^&*_\-+=<>.?/:][α-ωΑ-Ωa-zA-Z0-9~!@$%^&*_\-+=<>.?/:]*"

    SYMBOL["FPCore"] = FPCORE
    FPCORE = "FPCore"

    SYMBOL["if"] = IF
    IF = "if"

    SYMBOL["let"] = LET
    LET = "let"

    SYMBOL["let*"] = LET_STAR
    LET_STAR = "let*"

    SYMBOL["while"] = WHILE
    WHILE = "while"

    SYMBOL["while*"] = WHILE_STAR
    WHILE_STAR = "while*"

    SYMBOL["for"] = FOR
    FOR = "for"

    SYMBOL["for*"] = FOR_STAR
    FOR_STAR = "for*"

    SYMBOL["tensor"] = TENSOR
    TENSOR = "tensor"

    SYMBOL["tensor*"] = TENSOR_STAR
    TENSOR_STAR = "tensor*"

    SYMBOL["cast"] = CAST
    CAST = "cast"

    SYMBOL["array"] = ARRAY
    ARRAY = "array"

    SYMBOL["digits"] = DIGITS
    DIGITS = "digits"

    CONSTANTS = sorted([
        "E", "LOG2E", "LOG10E", "LN2", "LN10",
        "PI", "PI_2", "PI_4", "M_1_PI", "M_2_PI",
        "M_2_SQRTPI", "SQRT2", "SQRT1_2", "INFINITY", "NAN",
        "TRUE", "FALSE",
    ], key=len)
    for i in range(len(CONSTANTS)):
        SYMBOL[CONSTANTS[i]] = CONSTANT
    CONSTANT = "({})".format(")|(".join(CONSTANTS))

    OPERATIONS = sorted([
        "+", "-", "*", "/", "fabs",
        "fma", "exp", "exp2", "expm1", "log",
        "log10", "log2", "log1p", "pow", "sqrt",
        "cbrt", "hypot", "sin", "cos", "tan",
        "asin", "acos", "atan", "atan2", "sinh",
        "cosh", "tanh", "asinh", "acosh", "atanh",
        "erf", "erfc", "tgamma", "lgamma", "ceil",
        "floor", "fmod", "remainder", "fmax", "fmin",
        "fdim", "copysign", "trunc", "round", "nearbyint",
        "<", ">", "<=", ">=", "==",
        "!=", "and", "or", "not", "isfinite",
        "isinf", "isnan", "isnormal", "signbit",
        "dim", "size", "ref",
        "thefunc",
    ], key=len)
    for i in range(len(OPERATIONS)):
        SYMBOL[OPERATIONS[i]] = OPERATION
    _not_regex = "({})".format(")|(".join(OPERATIONS))
    OPERATION = _not_regex.replace("+", "\\+").replace("*", "\\*")

    # here so '!=' gets precedence over '!'
    SYMBOL[r"!"] = BANG
    BANG = r"!"

    def error(self, t):
        msg = "Line {}: Bad character '{}'".format(self.lineno, t.value[0])
        raise FPCoreLexError(msg, t)


_lexer = FPCoreLexer()


def lex(text):
    timer.start()
    lexed = _lexer.tokenize(text)
    timer.stop()
    return lexed


def main(argv):
    logger.set_log_level(Logger.EXTRA)

    if len(argv) == 1:
        text = sys.stdin.read()
    elif len(argv) == 2:
        with open(argv[1], "r") as f:
            text = f.read()
    if text.strip() == "":
        text = "(FPCore (x) :pre (<= 1/100 x 1/2) (/ (- (exp x) 1) x))"

    logger.blog("Input text", text)

    for token in lex(text):
        logger("{:14} '{}'", token.type, token.value)

    logger("Lexing time: {:.6f} msec", timer.elapsed() * 1000)


if __name__ == "__main__":
    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
