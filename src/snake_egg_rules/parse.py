

from snake_egg_rules.operations import *
import fpcore.ast as ast

import fractions


zero_arg = {
    CONST_PI: lambda: ast.Constant("PI"),
    CONST_E: lambda: ast.Constant("E"),
}


def mkone(operation):
    return lambda x: ast.Operation(operation, x)


one_arg = {
    thefunc: mkone("thefunc"),
    acos: mkone("acos"),
    acosh: mkone("acosh"),
    asin: mkone("asin"),
    asinh: mkone("asinh"),
    atan: mkone("atan"),
    atanh: mkone("atanh"),
    cbrt: mkone("cbrt"),
    cos: mkone("cos"),
    cosh: mkone("cosh"),
    erf: mkone("erf"),
    erfc: mkone("erfc"),
    exp: mkone("exp"),
    exp2: mkone("exp"),
    expm1: mkone("expm1"),
    fabs: mkone("fabs"),
    inv: mkone("inv"),
    lgamma: mkone("lgamma"),
    log1p: mkone("log1p"),
    log10: mkone("log10"),
    log: mkone("log"),
    log2: mkone("log2"),
    neg: mkone("-"),
    sin: mkone("sin"),
    sinh: mkone("sinh"),
    sqrt: mkone("sqrt"),
    tan: mkone("tan"),
    tanh: mkone("tanh"),
}


def mktwo(operation):
    return lambda a, b: ast.Operation(operation, a, b)


two_arg = {
    add: mktwo("+"),
    atan2: mktwo("atan2"),
    div: mktwo("/"),
    fmod: mktwo("fmod"),
    hypot: mktwo("hypot"),
    mul: mktwo("*"),
    pow: mktwo("pow"),
    remainder: mktwo("remainder"),
    sub: mktwo("-"),
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
