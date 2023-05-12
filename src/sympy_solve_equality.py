
import sympy

import fpcore


def sympy_solve_equality(lhs, rhs, var):
    eq = sympy.Eq(lhs.to_sympy(), rhs.to_sympy())
    ans = sympy.solve(eq, var.to_sympy())[0]
    return sympy_to_fpcore(ans)


SYMPY_TO_FPCORE_OPERATIONS = {
    sympy.core.add.Add: "+",
    sympy.core.mul.Mul: "*",
    sympy.core.power.Pow: "pow",
}


def sympy_to_fpcore(sym):
    # TODO: This only supports the parts of the sympy language needed for
    # our examples. The rest of the language needs to be added

    # Catch Mul with items in it that are Pow(x, NegativeOne)
    if (sym.func == sympy.core.mul.Mul
        and any((a.func == sympy.core.power.Pow
                 and a.args[1].func == sympy.core.numbers.NegativeOne)
                 for a in sym.args)):
        num, den = sympy.fraction(sym)
        a = sympy_to_fpcore(num)
        b = sympy_to_fpcore(den)
        return fpcore.ast.Operation("/", a, b)

    # Catch Add(a, Mul(NegativeOne, b)) as (- a b)
    if (sym.func == sympy.core.add.Add
        and len(sym.args) == 2
        and sym.args[1].func == sympy.core.mul.Mul
            and sym.args[1].args[0].func == sympy.core.numbers.NegativeOne):
        a = sympy_to_fpcore(sym.args[0])
        b = sympy_to_fpcore(sym.args[1].args[1])
        return fpcore.ast.Operation("-", a, b)

    # Catch Add(Mul(NegativeOne, a), b) as (- b a)
    if (sym.func == sympy.core.add.Add
        and len(sym.args) == 2
        and sym.args[0].func == sympy.core.mul.Mul
            and sym.args[0].args[0].func == sympy.core.numbers.NegativeOne):
        a = sympy_to_fpcore(sym.args[0].args[1])
        b = sympy_to_fpcore(sym.args[1])
        return fpcore.ast.Operation("-", b, a)

    # Catch Add(NegativeOne, a) as (- a 1)
    if (sym.func == sympy.core.add.Add
        and len(sym.args) == 2
            and sym.args[0].func == sympy.core.numbers.NegativeOne):
        a = sympy_to_fpcore(sym.args[1])
        return fpcore.ast.Operation("-", a, fpcore.ast.Number("1"))

    # Catch Add(a, NegativeOne) as (- a 1)
    if (sym.func == sympy.core.add.Add
        and len(sym.args) == 2
            and sym.args[1].func == sympy.core.numbers.NegativeOne):
        a = sympy_to_fpcore(sym.args[0])
        return fpcore.ast.Operation("-", a, fpcore.ast.Number("1"))

    # Variables
    if sym.func == sympy.core.symbol.Symbol:
        return fpcore.ast.Variable(sym.name)

    # Integers
    if sym.func == sympy.core.numbers.Integer:
        num = fpcore.ast.Number(str(abs(sym.numerator)))
        if sym.numerator < 0:
            num = fpcore.ast.Operation("-", num)
        return num

    # Rational
    if sym.func == sympy.core.numbers.Rational:
        num = fpcore.ast.Number(str(abs(sym.numerator)))
        den = fpcore.ast.Number(str(sym.denominator))
        rat = fpcore.ast.Operation("/", num, den)
        if sym.numerator < 0:
            rat = fpcore.ast.Operation("-", rat)
        return rat

    # The constant 1 ??
    if sym.func == sympy.core.numbers.One:
        return fpcore.ast.Number("1")

    # The constant -1 ??
    if sym.func == sympy.core.numbers.NegativeOne:
        return fpcore.ast.Operation("-", fpcore.ast.Number("1"))

    # The constant 1/2 ??
    if sym.func == sympy.core.numbers.Half:
        return fpcore.ast.Operation("/",
                                    fpcore.ast.Number("1"),
                                    fpcore.ast.Number("2"))

    # Others get translated directly
    try:
        op = SYMPY_TO_FPCORE_OPERATIONS[sym.func]
        args = [sympy_to_fpcore(a) for a in reversed(sym.args)]
        while len(args) > 1:
            lhs = args.pop()
            rhs = args.pop()
            bin = fpcore.ast.Operation(op, lhs, rhs)
            args.append(bin)
        return args[0]
    except KeyError:
        msg = f"Conversion to FPCore not yet supported for: {sym.func}"
        raise NotImplementedError(msg)


if __name__ == "__main__":
    lhs = fpcore.parse_expr("s")
    rhs = fpcore.parse_expr("(/ (- x 1) (+ x 1))")
    var = fpcore.ast.Variable("x")

    ans = sympy_solve_equality(lhs, rhs, var)

    print(ans)

    lhs = fpcore.parse_expr("s")
    rhs = fpcore.parse_expr("(- x 1)")
    var = fpcore.ast.Variable("x")

    ans = sympy_solve_equality(lhs, rhs, var)

    print(ans)

    lhs = fpcore.parse_expr("s")
    rhs = fpcore.parse_expr("(/ x (+ 2 x))")
    var = fpcore.ast.Variable("x")

    ans = sympy_solve_equality(lhs, rhs, var)

    print(ans)

    lhs = fpcore.parse_expr("s")
    rhs = fpcore.parse_expr("(+ (/ 1 2) x)")
    var = fpcore.ast.Variable("x")

    ans = sympy_solve_equality(lhs, rhs, var)

    print(ans)