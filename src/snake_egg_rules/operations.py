

from collections import namedtuple


nt = namedtuple

thefunc   = nt("thefunc",    "x")

CONST_PI  = nt("CONST_PI",   "")
CONST_E   = nt("CONST_E",    "")
CONST_INFINITY   = nt("CONST_INFINITY",    "")

neg       = nt("neg",        "x")
inv       = nt("inv",        "x")   # x != 0

add       = nt("add",        "x y")
sub       = nt("sub",        "x y")
mul       = nt("mul",        "x y")
div       = nt("div",        "x y") # y != 0

acos      = nt("acos",       "x")   # -1 <= x <= 1
acosh     = nt("acosh",      "x")   #  1 <= x
asin      = nt("asin",       "x")   # -1 <= x <= 1
asinh     = nt("asinh",      "x")
atan      = nt("atan",       "x")
atanh     = nt("atanh",      "x")
cbrt      = nt("cbrt",       "x")
cos       = nt("cos",        "x")
cosh      = nt("cosh",       "x")
erf       = nt("erf",        "x")
erfc      = nt("erfc",       "x")
exp       = nt("exp",        "x")
expm1     = nt("expm1",      "x")
fabs      = nt("fabs",       "x")
log       = nt("log",        "x")   #  0 < x
log10     = nt("log10",      "x")   #  0 < x
log1p     = nt("log1p",      "x")   # -1 < x
log2      = nt("log2",       "x")   #  0 < x
sin       = nt("sin",        "x")
sinh      = nt("sinh",       "x")
sqrt      = nt("sqrt",       "x")   #  0 <= x
tan       = nt("tan",        "x")
tanh      = nt("tanh",       "x")

atan2     = nt("atan2",      "x y") # x != 0 && y != 0
pow       = nt("pow",        "x y") # (x < 0 && (int(y) == y || something something odd den)) || (x == 0 && 0 <= y) || (0 < x)
hypot     = nt("hypot",      "x y") # 0 <= x && 0 <= y
remainder = nt("remainder",  "x y") # y != 0

fma       = nt("fma",        "x y z")

# Not in rewrite rules
uadd      = nt("uadd",       "x")
ceil      = nt("ceil",       "x")
exp2      = nt("exp2",       "x")
fdim      = nt("fdim",       "x y")
floor     = nt("floor",      "x")
isnormal  = nt("isnormal",   "x")
lgamma    = nt("lgamma",     "x")   # complicated
log10     = nt("log10",      "x")   #  0 < x
log2      = nt("log2",       "x")   #  0 < x
nearbyint = nt("nearbyint",  "x")
round     = nt("round",      "x")
signbit   = nt("signbit",    "x")
tgamma    = nt("tgamma",     "x")   # complicated

fmax      = nt("fmax",       "x y")
fmin      = nt("fmin",       "x y")
fmod      = nt("fmod",       "x y") # y != 0

