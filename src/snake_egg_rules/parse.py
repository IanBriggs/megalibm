

from operator import attrgetter
from snake_egg_rules.operations import *
import fpcore.ast as ast

import fractions


zero_arg = {
    CONST_PI: lambda: ast.Constant("PI"),
    CONST_E: lambda: ast.Constant("E"),
}


def mk_one(operation):
    return lambda x: ast.Operation(operation, x)


one_arg = {
    thefunc: mk_one("thefunc"),
    acos: mk_one("acos"),
    acosh: mk_one("acosh"),
    asin: mk_one("asin"),
    asinh: mk_one("asinh"),
    atan: mk_one("atan"),
    atanh: mk_one("atanh"),
    cbrt: mk_one("cbrt"),
    cos: mk_one("cos"),
    cosh: mk_one("cosh"),
    erf: mk_one("erf"),
    erfc: mk_one("erfc"),
    exp: mk_one("exp"),
    exp2: mk_one("exp"),
    expm1: mk_one("expm1"),
    fabs: mk_one("fabs"),
    inv: mk_one("inv"),
    tgamma: mk_one("tgamma"),
    lgamma: mk_one("lgamma"),
    log1p: mk_one("log1p"),
    log10: mk_one("log10"),
    log: mk_one("log"),
    log2: mk_one("log2"),
    neg: mk_one("-"),
    sin: mk_one("sin"),
    sinh: mk_one("sinh"),
    sqrt: mk_one("sqrt"),
    tan: mk_one("tan"),
    tanh: mk_one("tanh"),
}


def mk_two(operation):
    return lambda a, b: ast.Operation(operation, a, b)


two_arg = {
    add: mk_two("+"),
    atan2: mk_two("atan2"),
    div: mk_two("/"),
    fmod: mk_two("fmod"),
    hypot: mk_two("hypot"),
    mul: mk_two("*"),
    pow: mk_two("pow"),
    remainder: mk_two("remainder"),
    sub: mk_two("-"),
}

three_arg = {
    fma: lambda x, y, z: ast.Operation("fma", x, y, z,),
}


def egg_to_fpcore(expr):
    T = type(expr)

    if T == str:
        return ast.Variable(expr)

    if T == int:
        return ast.Number(str(expr))

    if T == float:
        return ast.Number(str(expr))

    if T == fractions.Fraction:
        if expr.denominator == 1:
            return ast.Number(str(expr.numerator))
        return ast.Operation("/",
                             ast.Number(str(expr.numerator)),
                             ast.Number(str(expr.denominator)))

    # TODO: Definitely a bug, why are zero arg tuples weird?
    #print(f"expr: '{expr}' of type: '{T}'")
    # if T in zero_arg:
    #    return zero_arg[T]()

    if expr in zero_arg:
        return zero_arg[expr]()

    if T not in one_arg and T not in two_arg and T not in three_arg:
        arg = egg_to_fpcore(expr[0])
        s = str(expr)
        op = s[:s.index("(")]
        return ast.Operation(op, arg)

    x = egg_to_fpcore(expr.x)
    if T in one_arg:
        return one_arg[T](x)

    y = egg_to_fpcore(expr.y)
    if T in two_arg:
        return two_arg[T](x, y)

    z = egg_to_fpcore(expr.z)
    if T in three_arg:
        return three_arg[T](x, y, z)

    assert False, f"Unsupported operation: {T}"
