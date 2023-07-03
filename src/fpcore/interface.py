from expect import expect_subclass
import fpcore

def var(s: str):
    return fpcore.ast.Variable(s)

def num(s: str):
    if s[0] == "-":
        return fpcore.ast.Operation("-",
                                    fpcore.ast.Number(s[1:]))
    return fpcore.ast.Number(s)


def make_function(args, body):
    return fpcore.ast.FPCore(None, args, list(), body)

E = fpcore.ast.Constant("E")
LOG2E = fpcore.ast.Constant("LOG2E")
LOG10E = fpcore.ast.Constant("LOG10E")
LN2 = fpcore.ast.Constant("LN2")
LN10 = fpcore.ast.Constant("LN10")
PI = fpcore.ast.Constant("PI")
PI_2 = fpcore.ast.Constant("PI_2")
PI_4 = fpcore.ast.Constant("PI_4")
M_1_PI = fpcore.ast.Constant("M_1_PI")
M_2_PI = fpcore.ast.Constant("M_2_PI")
M_2_SQRTPI = fpcore.ast.Constant("M_2_SQRTPI")
SQRT2 = fpcore.ast.Constant("SQRT2")
SQRT1_2 = fpcore.ast.Constant("SQRT1_2")
INFINITY = fpcore.ast.Constant("INFINITY")
NAN = fpcore.ast.Constant("NAN")
TRUE = fpcore.ast.Constant("TRUE")
FALSE = fpcore.ast.Constant("FALSE",)


def _make_unop(op, x):
    expect_subclass("x", x, fpcore.ast.ASTNode)
    return fpcore.ast.Operation(op, x)


def acos(x): return _make_unop("acos", x)
def acosh(x): return _make_unop("acosh", x)
def asin(x): return _make_unop("asin", x)
def asinh(x): return _make_unop("asinh", x)
def atan(x): return _make_unop("atan", x)
def atanh(x): return _make_unop("atanh", x)
def cbrt(x): return _make_unop("cbrt", x)
def ceil(x): return _make_unop("ceil", x)
def cos(x): return _make_unop("cos", x)
def cosh(x): return _make_unop("cosh", x)
def erf(x): return _make_unop("erf", x)
def erfc(x): return _make_unop("erfc", x)
def exp(x): return _make_unop("exp", x)
def exp2(x): return _make_unop("exp2", x)
def expm1(x): return _make_unop("expm1", x)
def fabs(x): return _make_unop("fabs", x)
def floor(x): return _make_unop("floor", x)
def lgamma(x): return _make_unop("lgamma", x)
def log(x): return _make_unop("log", x)
def log10(x): return _make_unop("log10", x)
def log1p(x): return _make_unop("log1p", x)
def log2(x): return _make_unop("log2", x)
def sin(x): return _make_unop("sin", x)
def sinh(x): return _make_unop("sinh", x)
def sqrt(x): return _make_unop("sqrt", x)
def tan(x): return _make_unop("tan", x)
def tanh(x): return _make_unop("tanh", x)
def tgamma(x): return _make_unop("tgamma", x)


def _make_binop(op, x, y):
    expect_subclass("x", x, fpcore.ast.ASTNode)
    expect_subclass("y", y, fpcore.ast.ASTNode)
    return fpcore.ast.Operation(op, x, y)


def atan2(x, y): return _make_binop("atan2", x, y)
def fdim(x, y): return _make_binop("fdim", x, y)
def fmax(x, y): return _make_binop("fmax", x, y)
def fmin(x, y): return _make_binop("fmin", x, y)
def fmod(x, y): return _make_binop("fmod", x, y)
def hypot(x, y): return _make_binop("hypot", x, y)
def pow(x, y): return _make_binop("pow", x, y)


def _make_triop(op, x, y,z):
    expect_subclass("x", x, fpcore.ast.ASTNode)
    expect_subclass("y", y, fpcore.ast.ASTNode)
    expect_subclass("z", z, fpcore.ast.ASTNode)
    return fpcore.ast.Operation(op, x, y, z)


def fma(x, y, z): return _make_triop("fma", z, y, z)
