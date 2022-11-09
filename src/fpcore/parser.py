

from utils import Logger, Timer

import fpcore.ast as ast
import fpcore.lexer as fpcore_lexer

from sly import Parser

import sys


logger = Logger(level=Logger.EXTRA, color=Logger.cyan)
timer = Timer()


class FPCoreParseError(Exception):
    def __init__(self, msg, p=None):
        self.msg = msg
        self.p = p


class FPCoreParser(Parser):
    tokens = fpcore_lexer.FPCoreLexer.tokens | {"ADDED_OPERATION"}

    # fpcores :=
    #     | <fpcore>+
    @_("fpcore { fpcore }")
    def fpcores(self, p):
        return (p.fpcore0, *p.fpcore1)

    # fpcore :=
    #     | ( FPCore <signature> <property>* <expr> )
    @_("LP FPCORE signature { property } expr RP")
    def fpcore(self, p):
        name = p.signature[0]
        args = p.signature[1]
        fpc = ast.FPCore(name, args, p.property, p.expr)
        if name is not None:
            fpcore_lexer.ADDED_OPERATIONS[name] = fpc
        return fpc

    # signature :=
    #      | {symbol}? (<argument>*)
    @_("[ SYMBOL ] LP { argument } RP")
    def signature(self, p):
        name = p[0][0]
        args = p.argument
        return (name, args)

    # dimension :=
    #     | <variable>
    #     | <number>
    @_("variable",
       "number")
    def dimension(self, p):
        return p[0]

    # argument :=
    #     | <variable>
    @_("variable")
    def argument(self, p):
        return p[0]

    #     | ( <variable> <dimension>+ )
    @_("LP variable dimension { dimension } RP")
    def argument(self, p):
        return p.variable.set_dimension((p.dimension0, *p.dimension1))

    #     | ( ! <property>* <variable> <dimension>* )
    @_("LP BANG { property } variable { dimension } RP")
    def argument(self, p):
        if len(p.property) > 0:
            p.variable.add_properties(p.property)
        if len(p.dimension) > 0:
            p.variable.set_dimension(p.dimension)
        return p.variable

    # expr :=
    #     | <number>
    #     | <variable>
    #     | <operation>
    #     | <if_expr>
    #     | <let>
    #     | <while_expr>
    #     | <for_expr>
    #     | <tensor>
    @_("number",
       "variable",
       "operation",
       "if_expr",
       "let",
       "while_expr",
       "for_expr",
       "tensor")
    def expr(self, p):
        return p[0]

    #     | {constant}
    @_("CONSTANT")
    def expr(self, p):
        return ast.Constant(p[0])

    #     | ( cast <expr> )
    @_("LP CAST expr RP")
    def expr(self, p):
        return ast.Cast(p.expr)

    #     | ( array <expr>* )
    @_("LP ARRAY { expr } RP")
    def expr(self, p):
        return ast.Array(p.expr)

    #     | ( ! <property>* <expr> )
    @_("LP BANG { property } expr RP")
    def expr(self, p):
        if len(p.property) > 0:
            p.expr.add_properties(p.property)
        return p.expr

    #     | ( # <expr> )
    @_("LP HASH expr RP")
    def expr(self, p):
        prop = ast.Property("precision", "integer")
        p.expr.add_properties([prop])
        return p.expr

    # number :=
    #     | {rational}
    @_("RATIONAL")
    def number(self, p):
        return ast.Number(p[0])
        # return ast.Rational(p[0])

    #     | {decnum}
    @_("DECNUM")
    def number(self, p):
        source = p[0]
        if source[0] == "-":
            return ast.Operation("-", ast.Number(source[1:]))
        return ast.Number(source)
        # return ast.Decnum(p[0])

    #     | {hexnum}
    @_("HEXNUM")
    def number(self, p):
        return ast.Number(p[0])
        # return ast.Hexnum(p[0])

    #     | ( digits {decnum} {decnum} {decnum} )
    @_("LP DIGITS DECNUM DECNUM DECNUM RP")
    def number(self, p):
        assert (0)
        return None
        # return ast.Digits(p[2], p[3], p[4])

    # property :=
    #     | : {symbol} <data>
    #     | : {operation} <data>
    @_("COLON SYMBOL data",
       "COLON OPERATION data")
    def property(self, p):
        return ast.Property(p[1], p[2])

    # data :=
    #     | {symbol}
    #     | <number>
    #     | {string}
    #     | <operation>
    #     | <let>
    #     | <binding>
    #     | <if>
    @_("SYMBOL",
       "number",
       "STRING",
       "operation",
       "let",
       "binding",
       "if_expr")
    def data(self, p):
        return p[0]

    #     | ( <data>* )
    @_("LP { data } RP")
    def data(self, p):
        return p.data

    # operation :=
    #     | ( {operation} <expr>* )
    @_("LP OPERATION { expr } RP",
       "LP ADDED_OPERATION { expr } RP")
    def operation(self, p):
        return ast.Operation(p[1], *p.expr)

    # if_expr :=
    #     | ( if <expr> <expr> <expr> )
    @_("LP IF expr expr expr RP")
    def if_expr(self, p):
        return ast.If(p.expr0, p.expr1, p.expr2)

    # let :=
    #     | ( let ( <binding>* ) <expr> )
    @_("LP LET LP { binding } RP expr RP")
    def let(self, p):
        return ast.Let(p.binding, p.expr)

    #     | ( let* ( <binding>* ) <expr> )
    @_("LP LET_STAR LP { binding } RP expr RP")
    def let(self, p):
        return ast.LetStar(p.binding, p.expr)

    # while_expr :=
    #     | ( while <expr> ( <update_binding>* ) <expr> )
    @_("LP WHILE expr LP { update_binding } RP expr RP")
    def while_expr(self, p):
        return ast.While(p.expr0, p.update_binding, p.expr1)

    #     | ( while* <expr> ( <update_binding>* ) <expr> )
    @_("LP WHILE_STAR expr LP { update_binding } RP expr RP")
    def while_expr(self, p):
        return ast.WhileStar(p.expr0, p.update_binding, p.expr1)

    # for_expr :=
    #     | ( for ( <binding>* ) ( <update_binding>* ) <expr> )
    @_("LP FOR LP { binding } RP LP { update_binding } RP expr RP")
    def for_expr(self, p):
        return ast.For(p.binding, p.update_binding, p.expr)

    #     | ( for* ( <binding>* ) ( <update_binding>* ) <expr> )
    @_("LP FOR_STAR LP { binding } RP LP { update_binding } RP expr RP")
    def for_expr(self, p):
        return ast.ForStar(p.binding, p.update_binding, p.expr)

    # tensor :=
    #     | ( tensor ( <binding>* ) <expr> )
    @_("LP TENSOR LP { binding } RP expr RP")
    def tensor(self, p):
        return ast.Tensor(p.binding, p.expr)

    #     | ( tensor* ( <binding>* ) ( <update_binding>* ) <expr> )
    @_("LP TENSOR_STAR LP { binding } RP LP { update_binding } RP expr RP")
    def tensor(self, p):
        return ast.TensorStar(p.binding, p.update_binding, p.expr)

    # binding :=
    #     | [ <variable> <expr> ]
    @_("LB variable expr RB")
    def binding(self, p):
        return ast.Binding(p.variable, p.expr)

    # update_binding :=
    #     | [ <variable> <expr> <expr> ]
    @_("LB variable expr expr RB")
    def update_binding(self, p):
        return ast.UpdateBinding(p.variable, p.expr0, p.expr1)

    # variable :=
    #     | {symbol}
    @_("SYMBOL")
    def variable(self, p):
        return ast.Variable(p[0])

    # errors
    def error(self, p):
        if p is None:
            raise FPCoreParseError("Unexpected end of FPCore")

        if (p.type == "SYMBOL"):
            # and p.value in fpcore_lexer.ADDED_OPERATIONS):
            p.type = "ADDED_OPERATION"
            self.errok()
            return p

        msg = "Line {}: Syntax error at '{}'".format(p.lineno, p)
        raise FPCoreParseError(msg, p)


_parser = FPCoreParser()


def parse(text):
    tokens = fpcore_lexer.lex(text)
    timer.start()
    parsed = _parser.parse(tokens)
    timer.stop()
    return parsed


def main(argv):
    logger.set_log_level(Logger.EXTRA)

    if len(argv) == 1:
        text = sys.stdin.read()
    elif len(argv) == 2:
        with open(argv[1], "r") as f:
            text = f.read()
    if text.strip() == "":
        text = "(FPCore test () 1) (FPCore () 1)"

    logger.blog("Input text", text)

    for fpc in parse(text):
        logger.blog("repr", repr(fpc))
        logger.blog("str", str(fpc))

    logger(" Lexing time: {:.6f} msec", fpcore_lexer.timer.elapsed() * 1000)
    logger("Parsing time: {:.6f} msec", timer.elapsed() * 1000)


if __name__ == "__main__":
    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
