

from collections import namedtuple




PI = namedtuple("PI", "")
E = namedtuple("E", "")

neg = namedtuple("neg", "x")

add = namedtuple("add", "x y")
sub = namedtuple("sub", "x y")
mul = namedtuple("mul", "x y")
div = namedtuple("div", "x y")


acos = namedtuple("acos", "x")
acosh = namedtuple("acosh", "x")
asin = namedtuple("asin", "x")
asinh = namedtuple("asinh", "x")
atan = namedtuple("atan", "x")
atanh = namedtuple("atanh", "x")
cbrt = namedtuple("cbrt", "x")
cos = namedtuple("cos", "x")
cosh = namedtuple("cosh", "x")
erf = namedtuple("erf", "x")
erfc = namedtuple("erfc", "x")
exp = namedtuple("exp", "x")
expm1 = namedtuple("expm1", "x")
fabs = namedtuple("fabs", "x")
log = namedtuple("log", "x")
log1p = namedtuple("log1p", "x")
sin = namedtuple("sin", "x")
sinh = namedtuple("sinh", "x")
sqrt = namedtuple("sqrt", "x")
tan = namedtuple("tan", "x")
tanh = namedtuple("tanh", "x")

atan2 = namedtuple("atan2", "x y")
pow = namedtuple("pow", "x y")
hypot = namedtuple("hypot", "x y")
remainder = namedtuple("remainder", "x y")

fma = namedtuple("fma", "x y z")

# Not in rewrite rules
uadd = namedtuple("uadd", "x")
ceil = namedtuple("ceil", "x")
exp2 = namedtuple("exp2", "x")
fdim = namedtuple("fdim", "x y")
floor = namedtuple("floor", "x")
isnormal = namedtuple("isnormal", "x")
lgamma = namedtuple("lgamma", "x")
log10 = namedtuple("log10", "x")
log2 = namedtuple("log2", "x")
nearbyint = namedtuple("nearbyint", "x")
round = namedtuple("round", "x")
signbit = namedtuple("signbit", "x")
tgamma = namedtuple("tgamma", "x")

fmax = namedtuple("fmax", "x y")
fmin = namedtuple("fmin", "x y")
fmod = namedtuple("fmod", "x y")

