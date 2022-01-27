

from snake_egg_rules.operations import *
import fpcore.ast as ast

import fractions


zero_arg = {
    CONST_PI: lambda: ast.Constant("PI"),
    CONST_E:  lambda: ast.Constant("E"),
}

one_arg = {
    thefunc: lambda x: ast.Operation("thefunc", x),
    acos:  lambda x: ast.Operation("acos",  x),
    acosh: lambda x: ast.Operation("acosh", x),
    asin:  lambda x: ast.Operation("asin",  x),
    asinh: lambda x: ast.Operation("asinh", x),
    atan:  lambda x: ast.Operation("atan",  x),
    atanh: lambda x: ast.Operation("atanh", x),
    cbrt:  lambda x: ast.Operation("cbrt",  x),
    cos:   lambda x: ast.Operation("cos",   x),
    cosh:  lambda x: ast.Operation("cosh",  x),
    erf:   lambda x: ast.Operation("erf",   x),
    erfc:  lambda x: ast.Operation("erfc",  x),
    exp:   lambda x: ast.Operation("exp",   x),
    expm1: lambda x: ast.Operation("expm1", x),
    fabs:  lambda x: ast.Operation("fabs",  x),
    inv:   lambda x: ast.Operation("inv",   x),
    log1p: lambda x: ast.Operation("log1p", x),
    log:   lambda x: ast.Operation("log",   x),
    neg:   lambda x: ast.Operation("-",     x),
    sin:   lambda x: ast.Operation("sin",   x),
    sinh:  lambda x: ast.Operation("sinh",  x),
    sqrt:  lambda x: ast.Operation("sqrt",  x),
    tan:   lambda x: ast.Operation("tan",   x),
    tanh:  lambda x: ast.Operation("tanh",  x),
}

two_arg = {
    add:       lambda x, y: ast.Operation("+", x, y),
    atan2:     lambda x, y: ast.Operation("atan2", x, y),
    div:       lambda x, y: ast.Operation("/", x, y),
    fmod:      lambda x, y: ast.Operation("fmod", x, y),
    hypot:     lambda x, y: ast.Operation("hypot", x, y),
    mul:       lambda x, y: ast.Operation("*", x, y),
    pow:       lambda x, y: ast.Operation("pow", x, y),
    remainder: lambda x, y: ast.Operation("remainder", x, y),
    sub:       lambda x, y: ast.Operation("-", x, y),
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
    #if T in zero_arg:
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
