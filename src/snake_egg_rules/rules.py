

from snake_egg_rules.operations import *

from snake_egg import EGraph, Rewrite, Var, vars

x, y, z, a, b, c, d = vars("x y z a b c d")


# We want only rules that are always true and safe.
#
# True rules are always equal.
# For instance sqrt(x*x) -> x works when x >= 0, but is not equal when x < 0.
#
# Safe rules mean that a valid domain on the left hand side is also valid on
# the right hand side.
# For instance (b*c)/a -> b/(a/c), the left hand side is valid when a != 0,
# but the right hand side is only valid when c != 0 and a/c != 0.
# So the left hand side is defined for a=1, b=1, and c=0, but then the right
# hand side is undefined.
#
# Rules can be marked as:
# * false: not always equal
# * unsafe: not safe
# * unknown: not fully analyzed
# * bad: impedes megalibm
# * skip: uses operations not used in megalibm
#
# For rules that contain operators with invalid domains there are boolean
# expressions that are true if the rule is safe.
# If the implication is true then "--->" is used for the implication, if false
# then "-/->" is used.
# The domain validity expressions are given in operations.py.

raw_rules = [

  # Commutativity
  # commutativity (arithmetic simplify fp-safe)
  ["+-commutative",  add(a, b),  add(b, a)],
  ["*-commutative",  mul(a, b),  mul(b, a)],

  # Associativity
  # associativity (arithmetic simplify)
  ["associate-+r+",          add(a, add(b, c)),  add(add(a, b), c)],
  ["associate-+l+",          add(add(a, b), c),  add(a, add(b, c))],
  ["associate-+r-",          add(a, sub(b, c)),  sub(add(a, b), c)],
  ["associate-+l-",          add(sub(a, b), c),  sub(a, sub(b, c))],
  ["associate--r+",          sub(a, add(b, c)),  sub(sub(a, b), c)],
  ["associate--l+",          sub(add(a, b), c),  add(a, sub(b, c))],
  ["associate--l-",          sub(sub(a, b), c),  sub(a, add(b, c))],
  ["associate--r-",          sub(a, sub(b, c)),  add(sub(a, b), c)],
  ["associate-*r*",          mul(a, mul(b, c)),  mul(mul(a, b), c)],
  ["associate-*l*",          mul(mul(a, b), c),  mul(a, mul(b, c))],
  ["associate-*r/",          mul(a, div(b, c)),  div(mul(a, b), c)],  #div c != 0 ---> c != 0
  ["associate-*l/",          mul(div(a, b), c),  div(mul(a, c), b)],
  ["associate-/r*",          div(a, mul(b, c)),  div(div(a, b), c)],  #div b*c != 0---> b != 0 && c != 0
  #unsafe ["associate-/l*",  div(mul(b, c), a),  div(b, div(a, c))],  #div a != 0 -/-> c != 0 && a/c != 0
  ["associate-/r/",          div(a, div(b, c)),  mul(div(a, b), c)],  #div c != 0 && b/c != 0 ---> b != 0
  ["associate-/l/",          div(div(b, c), a),  div(b, mul(a, c))],  #div c != 0 && a != 0---> a*c != 0

  # Counting
  # counting (arithmetic simplify)
  ["count-2",  add(x, x),  mul(2, x)],

  # Distributivity
  # distributivity (arithmetic simplify)
  ["distribute-lft-in",     mul(a, add(b, c)),          add(mul(a, b), mul(a, c))],
  ["distribute-rgt-in",     mul(a, add(b, c)),          add(mul(b, a), mul(c, a))],
  ["distribute-lft-out",    add(mul(a, b), mul(a, c)),  mul(a, add(b, c))],
  ["distribute-lft-out--",  sub(mul(a, b), mul(a, c)),  mul(a, sub(b, c))],
  ["distribute-rgt-out",    add(mul(b, a), mul(c, a)),  mul(a, add(b, c))],
  ["distribute-rgt-out--",  sub(mul(b, a), mul(c, a)),  mul(a, sub(b, c))],
  ["distribute-lft1-in",    add(mul(b, a), a),          mul(add(b, 1), a)],
  ["distribute-rgt1-in",    add(a, mul(c, a)),          mul(add(c, 1), a)],

  # Safe Distributivity
  # distributivity-fp-safe (arithmetic simplify fp-safe)
  ["distribute-lft-neg-in",   neg(mul(a, b)),       mul(neg(a), b)],
  ["distribute-rgt-neg-in",   neg(mul(a, b)),       mul(a, neg(b))],
  ["distribute-lft-neg-out",  mul(neg(a), b),       neg(mul(a, b))],
  ["distribute-rgt-neg-out",  mul(a, neg(b)),       neg(mul(a, b))],
  ["distribute-neg-in",       neg(add(a, b)),       add(neg(a), neg(b))],
  ["distribute-neg-out",      add(neg(a), neg(b)),  neg(add(a, b))],
  ["distribute-frac-neg",     div(neg(a), b),       neg(div(a, b))],  #div b != 0 ---> b != 0
  ["distribute-neg-frac",     neg(div(a, b)),       div(neg(a), b)],  #div b != 0 ---> b != 0

  # cancel-sign-fp-safe (arithmetic simplify fp-safe)
  ["cancel-sign-sub",      sub(a, mul(neg(b), c)),  add(a, mul(b, c))],
  ["cancel-sign-sub-inv",  sub(a, mul(b, c)),       add(a, mul(neg(b), c))],

  # Difference of squares
  # difference-of-squares-canonicalize (polynomials simplify)
  ["swap-sqr",               mul(mul(a, b), mul(a, b)),  mul(mul(a, a), mul(b, b))],
  ["un-swap-sqr",            mul(mul(a, a), mul(b, b)),  mul(mul(a, b), mul(a, b))],
  ["difference-of-squares",  sub(mul(a, a), mul(b, b)),  mul(add(a, b), sub(a, b))],
  ["difference-of-sqr-1",    sub(mul(a, a), 1),          mul(add(a, 1), sub(a, 1))],
  ["difference-of-sqr--1",   add(mul(a, a), neg(1)),     mul(add(a, 1), sub(a, 1))],
  #unknown ["sqr-pow",      pow(a, b),                  mul(pow(a, div(b, 2)), pow(a, div(b, 2)))],  #pow #div ???
  ["pow-sqr",                mul(pow(a, b), pow(a, b)),  pow(a, mul(2, b))],

  # difference-of-squares-flip (polynomials)
  #unsafe ["flip-+",  add(a, b),  div(sub(mul(a, a), mul(b, b)), sub(a, b))],  #div () -/-> a-b != 0
  #unsafe ["flip--",  sub(a, b),  div(sub(mul(a, a), mul(b, b)), add(a, b))],  #div () -/-> a+b != 0

  # Identity
  # id-reduce (arithmetic simplify)
  ["remove-double-div",  div(1, div(1, a)),  a],  #div a != 0 && 1/a != 0 ---> ()
  ["rgt-mult-inverse",   mul(a, div(1, a)),  1],  #div a != 0 && 1/a != 0 ---> ()
  ["lft-mult-inverse",   mul(div(1, a), a),  1],  #div a != 0 ---> ()

  # id-reduce-fp-safe-nan (arithmetic simplify fp-safe-nan)
  ["+-inverses",  sub(a, a),  0],
  ["*-inverses",  div(a, a),  1],  #div a != 0 ---> ()
  ["div0",        div(0, a),  0],  #div a != 0 ---> ()
  ["mul0-lft",    mul(0, a),  0],
  ["mul0-rgt",    mul(a, 0),  0],

  # id-reduce-fp-safe (arithmetic simplify fp-safe)
  ["+-lft-identity",     add(0, a),    a],
  ["+-rgt-identity",     add(a, 0),    a],
  ["--rgt-identity",     sub(a, 0),    a],
  ["sub0-neg",           sub(0, a),    neg(a)],
  ["remove-double-neg",  neg(neg(a)),  a],
  ["*-lft-identity",     mul(1, a),    a],
  ["*-rgt-identity",     mul(a, 1),    a],
  ["/-rgt-identity",     div(a, 1),    a],  #div 1 != 0 ---> ()
  ["mul-1-neg",          mul(neg(1), a),   neg(a)],

  # nan-transform-fp-safe (arithmetic simplify fp-safe)
  ["sub-neg",    sub(a, b),       add(a, neg(b))],
  ["unsub-neg",  add(a, neg(b)),  sub(a, b)],
  ["neg-sub0",   neg(b),          sub(0, b)],
  ["neg-mul-1",  neg(a),          mul(neg(1), a)],

  # id-transform (arithmetic)
  ["div-inv",            div(a, b),          mul(a, div(1, b))],  #div b != 0 ---> b != 0
  ["un-div-inv",         mul(a, div(1, b)),  div(a, b)],          #div b != 0 ---> b != 0
  #unsafe ["clear-num",  div(a, b),          div(1, div(b, a))],  #div b != 0 -/-> a != 0 && b/a != 0

  # id-transform-fp-safe (arithmetic fp-safe)
  ["*-un-lft-identity",  a,  mul(1, a)],

  # Difference of cubes
  # difference-of-cubes (polynomials)
  ["sum-cubes",         add(pow(a, 3), pow(b, 3)),  mul(add(mul(a, a), sub(mul(b, b), mul(a, b))), add(a, b))],
  ["difference-cubes",  sub(pow(a, 3), pow(b, 3)),  mul(add(mul(a, a), add(mul(b, b), mul(a, b))), sub(a, b))],
  #unknown ["flip3-+",  add(a, b),                  div(add(pow(a, 3), pow(b, 3)), add(mul(a, a), sub(mul(b, b), mul(a, b))))],  #pow #div ???
  #unknown ["flip3--",  sub(a, b),                  div(sub(pow(a, 3), pow(b, 3)), add(mul(a, a), add(mul(b, b), mul(a, b))))],  #pow #div ???

  # Dealing with fractions
  # fractions-distribute (fractions simplify)
  ["div-sub",     div(sub(a, b), c),          sub(div(a, c), div(b, c))],  #div c != 0 ---> c != 0
  ["times-frac",  div(mul(a, b), mul(c, d)),  mul(div(a, c), div(b, d))],  #div c*d !+ 0 ---> c != 0 && d != 0

  # fractions-transform (fractions)
  ["sub-div",     sub(div(a, c), div(b, c)),  div(sub(a, b), c)],                          #div c != 0 ---> c != 0
  ["frac-add",    add(div(a, b), div(c, d)),  div(add(mul(a, d), mul(b, c)), mul(b, d))],  #div b != 0 && d != 0 ---> b*d != 0
  ["frac-sub",    sub(div(a, b), div(c, d)),  div(sub(mul(a, d), mul(b, c)), mul(b, d))],  #div b != 0 && d != 0 ---> b*d != 0
  ["frac-times",  mul(div(a, b), div(c, d)),  div(mul(a, c), mul(b, d))],                  #div b != 0 && d != 0 ---> b*d != 0
  ["frac-2neg",   div(a, b),                  div(neg(a), neg(b))],                        #div b != 0 ---> -b != 0

  # Square root
  # squares-reduce (arithmetic simplify)
  ["rem-square-sqrt",  mul(sqrt(x), sqrt(x)),  x],        #sqrt x >= 0 ---> ()
  ["rem-sqrt-square",  sqrt(mul(x, x)),        fabs(x)],  #sqrt x*x >= 0 ---> ()

  # squares-reduce-fp-sound (arithmetic simplify fp-safe)
  ["sqr-neg",  mul(neg(x), neg(x)),    mul(x, x)],
  ["sqr-abs",  mul(fabs(x), fabs(x)),  mul(x, x)],

  # fabs-reduce (arithmetic simplify fp-safe)
  ["fabs-fabs",  fabs(fabs(x)),    fabs(x)],
  ["fabs-sub",   fabs(sub(a, b)),  fabs(sub(b, a))],
  ["fabs-neg",   fabs(neg(x)),     fabs(x)],
  ["fabs-sqr",   fabs(mul(x, x)),  mul(x, x)],
  ["fabs-mul",   fabs(mul(a, b)),  mul(fabs(a), fabs(b))],
  ["fabs-div",   fabs(div(a, b)),  div(fabs(a), fabs(b))],  #div b != 0 ---> |b| != 0

  # fabs-expand (arithmetic fp-safe)
  ["neg-fabs",  fabs(x),                fabs(neg(x))],
  ["mul-fabs",  mul(fabs(a), fabs(b)),  fabs(mul(a, b))],
  ["div-fabs",  div(fabs(a), fabs(b)),  fabs(div(a, b))],  #div |b| != 0 ---> b != 0

  # squares-transform (arithmetic)
  #unsafe ["sqrt-prod",     sqrt(mul(x, y)),        mul(sqrt(x), sqrt(y))],  #sqrt x*y >= 0 -/-> x >= 0 && y >= 0
  #unsafe ["sqrt-div",      sqrt(div(x, y)),        div(sqrt(x), sqrt(y))],  #sqrt #div y != 0 && x/y >= 0 -/-> x >= 0 && y >= 0 && sqrt(y) != 0
  #unknown ["sqrt-pow1",    sqrt(pow(x, y)),        pow(x, div(y, 2))],      #pow #sqrt #div ???
  ["sqrt-pow2",             pow(sqrt(x), y),        pow(x, div(y, 2))],
  ["sqrt-unprod",           mul(sqrt(x), sqrt(y)),  sqrt(mul(x, y))],        #sqrt x >= 0 && y >= 0 ---> x*y >= 0
  ["sqrt-undiv",            div(sqrt(x), sqrt(y)),  sqrt(div(x, y))],        #sqrt #div x >= 0 && y >= 0 && sqrt(y) != 0 ---> y != 0 && x/y >= 0
  #unsafe ["add-sqr-sqrt",  x,                      mul(sqrt(x), sqrt(x))],  #sqrt () -/-> x >= 0

  # Cube root
  # cubes-reduce (arithmetic simplify)
  ["rem-cube-cbrt",  pow(cbrt(x), 3),                      x],  #pow  <something> ---> ()
  ["rem-cbrt-cube",  cbrt(pow(x, 3)),                      x],  #pow  <something> ---> ()
  ["rem-3cbrt-lft",  mul(mul(cbrt(x), cbrt(x)), cbrt(x)),  x],
  ["rem-3cbrt-rft",  mul(cbrt(x), mul(cbrt(x), cbrt(x))),  x],
  ["cube-neg",       pow(neg(x), 3),                       neg(pow(x, 3))],

  # cubes-distribute (arithmetic simplify)
  ["cube-prod",  pow(mul(x, y), 3),  mul(pow(x, 3), pow(y, 3))],
  ["cube-div",   pow(div(x, y), 3),  div(pow(x, 3), pow(y, 3))],
  ["cube-mult",  pow(x, 3),          mul(x, mul(x, x))],

  # cubes-transform (arithmetic)
  ["cbrt-prod",           cbrt(mul(x, y)),        mul(cbrt(x), cbrt(y))],
  ["cbrt-div",            cbrt(div(x, y)),        div(cbrt(x), cbrt(y))],  #div y != 0 ---> cbrt(y) != 0
  ["cbrt-unprod",         mul(cbrt(x), cbrt(y)),  cbrt(mul(x, y))],
  ["cbrt-undiv",          div(cbrt(x), cbrt(y)),  cbrt(div(x, y))],        #div cbrt(y) != 0 ---> y != 0
  #bad ["add-cube-cbrt",  x,                      mul(mul(cbrt(x), cbrt(x)), cbrt(x))],
  #bad ["add-cbrt-cube",  x,                      cbrt(mul(mul(x, x), x))],

  # cubes-canonicalize (arithmetic simplify)
  ["cube-unmult",  mul(x, mul(x, x)),  pow(x, 3)],

  # Exponentials
  # exp-expand (exponents)
  #unsafe ["add-exp-log",  x,  exp(log(x))],  #log () -/-> x > 0
  ["add-log-exp",          x,  log(exp(x))],  #log () ---> exp(x) > 0

  # exp-reduce (exponents simplify)
  ["rem-exp-log",  exp(log(x)),  x],  #log x > 0 ---> ()
  ["rem-log-exp",  log(exp(x)),  x],  #log exp(x) > 0 ---> ()

  # exp-constants (exponents simplify fp-safe)
  ["exp-0",    exp(0),     1],
  ["exp-1-e",  exp(1),     CONST_E()],
  ["1-exp",    1,          exp(0)],
  ["e-exp-1",  CONST_E(),  exp(1)],

  # exp-distribute (exponents simplify)
  ["exp-sum",   exp(add(a, b)),  mul(exp(a), exp(b))],
  ["exp-neg",   exp(neg(a)),     div(1, exp(a))],       #div () ---> exp(a) != 0
  ["exp-diff",  exp(sub(a, b)),  div(exp(a), exp(b))],  #div () ---> exp(b) != 0

  # exp-factor (exponents simplify)
  ["prod-exp",      mul(exp(a), exp(b)),  exp(add(a, b))],
  ["rec-exp",       div(1, exp(a)),       exp(neg(a))],     #div exp(a) != 0 ---> ()
  ["div-exp",       div(exp(a), exp(b)),  exp(sub(a, b))],  #div exp(b) != 0 ---> ()
  ["exp-prod",      exp(mul(a, b)),       pow(exp(a), b)],
  ["exp-sqrt",      exp(div(a, 2)),       sqrt(exp(a))],    #sqrt #div 2 != 0 ---> exp(a) >= 0
  ["exp-cbrt",      exp(div(a, 3)),       cbrt(exp(a))],    #div 3 != 0 ---> ()
  ["exp-lft-sqr",   exp(mul(a, 2)),       mul(exp(a), exp(a))],
  ["exp-lft-cube",  exp(mul(a, 3)),       pow(exp(a), 3)],

  # Powers
  # pow-reduce (exponents simplify)
  #unknown ["unpow-1",  pow(a, neg(1)),  div(1, a)],  #pow #div ???

  # pow-reduce-fp-safe (exponents simplify fp-safe)
  #unknown ["unpow1",  pow(a, 1),  a],  #pow ???

  # pow-reduce-fp-safe-nan (exponents simplify fp-safe-nan)
  #unknown ["unpow0",      pow(a, 0),  1],  #pow ???
  #unknown ["pow-base-1",  pow(1, a),  1],  #pow ???

  # pow-expand-fp-safe (exponents fp-safe)
  #unknown ["pow1",  a,  pow(a, 1)],  #pow ???

  # pow-canonicalize (exponents simplify)
  #unknown ["exp-to-pow",  exp(mul(log(a), b)),  pow(a, b)],          #log #pow ???
  #unknown ["pow-plus",    mul(pow(a, b), a),    pow(a, add(b, 1))],  #pow ???
  #unknown ["unpow1/2",    pow(a, div(1, 2)),    sqrt(a)],            #pow #sqrt #div ???
  #unknown ["unpow2",      pow(a, 2),            mul(a, a)],          #pow ???
  #unknown ["unpow3",      pow(a, 3),            mul(mul(a, a), a)],  #pow ???
  #unknown ["unpow1/3",    pow(a, div(1, 3)),    cbrt(a)],            #pow #div ???

  # pow-transform (exponents)
  #unknown ["pow-exp",          pow(exp(a), b),             exp(mul(a, b))],             #pow ???
  #unknown ["pow-to-exp",       pow(a, b),                  exp(mul(log(a), b))],        #log #pow ???
  #unknown ["pow-prod-up",      mul(pow(a, b), pow(a, c)),  pow(a, add(b, c))],          #pow ???
  #unknown ["pow-prod-down",    mul(pow(b, a), pow(c, a)),  pow(mul(b, c), a)],          #pow ???
  #unknown ["pow-pow",          pow(pow(a, b), c),          pow(a, mul(b, c))],          #pow ???
  #unknown ["pow-neg",          pow(a, neg(b)),             div(1, pow(a, b))],          #pow #div ???
  #unknown ["pow-flip",         div(1, pow(a, b)),          pow(a, neg(b))],             #pow #div ???
  #unknown ["pow-div",          div(pow(a, b), pow(a, c)),  pow(a, sub(b, c))],          #pow #div ???
  #unknown ["pow-sub",          pow(a, sub(b, c)),          div(pow(a, b), pow(a, c))],  #pow #div ???
  #unknown ["pow-unpow",        pow(a, mul(b, c)),          pow(pow(a, b), c)],          #pow ???
  #unknown ["unpow-prod-up",    pow(a, add(b, c)),          mul(pow(a, b), pow(a, c))],  #pow ???
  #unknown ["unpow-prod-down",  pow(mul(b, c), a),          mul(pow(b, a), pow(c, a))],  #pow ???
  #unknown ["pow1/2",           sqrt(a),                    pow(a, div(1, 2))],          #pow #sqrt #div ???
  #unknown ["pow2",             mul(a, a),                  pow(a, 2)],                  #pow ???
  ["pow1/3",                    cbrt(a),                    pow(a, div(1, 3))], #pow (Pavel said)
  #unknown ["pow3",             mul(mul(a, a), a),          pow(a, 3)],                  #pow ???

  # pow-transform-fp-safe-nan (exponents simplify fp-safe-nan)
  #unknown ["pow-base-0",  pow(0, a),  0],  #pow ???

  # pow-transform-fp-safe (exponents fp-safe)
  #unknown ["inv-pow",  div(1, a),  pow(a, neg(1))],  #pow #div ???

  # Logarithms
  # log-distribute (exponents simplify)
  #unknown ["log-prod",  log(mul(a, b)),  add(log(a), log(b))],  #log ???
  #unknown ["log-div",   log(div(a, b)),  sub(log(a), log(b))],  #log #div ???
  #unknown ["log-rec",   log(div(1, a)),  neg(log(a))],          #log #div ???
  #unknown ["log-pow",   log(pow(a, b)),  mul(b, log(a))],       #log #pow ???
  #unknown ["log-E",     log(CONST_E()),  1],                    #log ???

  # log-factor (exponents)
  #unknown ["sum-log",   add(log(a),   log(b)),log(mul(a, b))],  #log ???
  #unknown ["diff-log",  sub(log(a),   log(b)),log(div(a, b))],  #log #div ???
  #unknown ["neg-log",   neg(log(a)),  log(div(1, a))],          #log #div ???

  # Trigonometry
  # trig-reduce (trigonometry simplify)
  ["cos-sin-sum",  add(mul(cos(a), cos(a)), mul(sin(a), sin(a))),  1],
  ["1-sub-cos",    sub(1, mul(cos(a), cos(a))),                    mul(sin(a), sin(a))],
  ["1-sub-sin",    sub(1, mul(sin(a), sin(a))),                    mul(cos(a), cos(a))],
  ["-1-add-cos",   add(mul(cos(a), cos(a)), neg(1)),               neg(mul(sin(a), sin(a)))],
  ["-1-add-sin",   add(mul(sin(a), sin(a)), neg(1)),               neg(mul(cos(a), cos(a)))],
  ["sub-1-cos",    sub(mul(cos(a), cos(a)), 1),                    neg(mul(sin(a), sin(a)))],
  ["sub-1-sin",    sub(mul(sin(a), sin(a)), 1),                    neg(mul(cos(a), cos(a)))],
  ["sin-PI/6",     sin(div(CONST_PI(), 6)),                        div(1, 2)],               #div 6 != 0 ---> 2 != 0
  ["sin-PI/4",     sin(div(CONST_PI(), 4)),                        div(sqrt(2), 2)],         #sqrt #div 4 != 0 ---> 2 >= 0 && 2 != 0
  ["sin-PI/3",     sin(div(CONST_PI(), 3)),                        div(sqrt(3), 2)],         #sqrt #div 3 != 0 ---> 3 >= 0 && 2 != 0
  ["sin-PI/2",     sin(div(CONST_PI(), 2)),                        1],                       #div 2 != 0 ---> ()
  ["sin-PI",       sin(CONST_PI()),                                0],
  ["sin-+PI",      sin(add(x, CONST_PI())),                        neg(sin(x))],
  ["sin+-PI",      sin(sub(x, CONST_PI())),                        neg(sin(x))],
  ["sin-+PI/2",    sin(add(x, div(CONST_PI(), 2))),                cos(x)],                  #div 2 != 0 ---> ()
  ["cos-PI/6",     cos(div(CONST_PI(), 6)),                        div(sqrt(3), 2)],         #sqrt #div 6 != 0 ---> 3 >= 0 && 2 != 0
  ["cos-PI/4",     cos(div(CONST_PI(), 4)),                        div(sqrt(2), 2)],         #sqrt #div 4 != 0 ---> 2 >= 0 && 2 != 0
  ["cos-PI/3",     cos(div(CONST_PI(), 3)),                        div(1, 2)],               #div 3 != 0 ---> 2 != 0
  ["cos-PI/2",     cos(div(CONST_PI(), 2)),                        0],                       #div 2 != 0 ---> ()
  ["cos-PI",       cos(CONST_PI()),                                neg(1)],
  ["cos-+PI",      cos(add(x, CONST_PI())),                        neg(cos(x))],
  ["cos-+PI/2",    cos(add(x, div(CONST_PI(), 2))),                neg(sin(x))],             #div 2 != 0 ---> ()
  ["tan-PI/6",     tan(div(CONST_PI(), 6)),                        div(1, sqrt(3))],         #sqrt #div 6 != 0 ---> 3 >= 0 && sqrt(3) != 0
  ["tan-PI/4",     tan(div(CONST_PI(), 4)),                        1],                       #div 4 != 0 ---> ()
  ["tan-PI/3",     tan(div(CONST_PI(), 3)),                        sqrt(3)],                 #sqrt #div 3 != 0 ---> 3 >= 0
  ["tan-PI",       tan(CONST_PI()),                                0],
  ["tan-+PI",      tan(add(x, CONST_PI())),                        tan(x)],
  #["tan-+PI/2",   tan(add(x, div(CONST_PI(), 2))),                div(neg(1), tan(x))],         #div 2 != 0 -/-> tan(x) != 0
  ["hang-0p-tan",  div(sin(a), add(1, cos(a))),                    tan(div(a, 2))],          #div 1+cos(a) != 0 ---> 2 != 0
  ["hang-0m-tan",  div(neg(sin(a)), add(1, cos(a))),               tan(div(neg(a), 2))],     #div 1+cos(a) != 0 ---> 2 != 0
  ["hang-p0-tan",  div(sub(1, cos(a)), sin(a)),                    tan(div(a, 2))],          #div sin(a) != 0 ---> 2 != 0
  ["hang-m0-tan",  div(sub(1, cos(a)), neg(sin(a))),               tan(div(neg(a), 2))],     #div -sin(a) != 0 ---> 2 != 0
  ["hang-p-tan",   div(add(sin(a), sin(b)), add(cos(a), cos(b))),  tan(div(add(a, b), 2))],  #div cos(a) + cos(b) != 0 ---> 2 != 0
  ["hang-m-tan",   div(sub(sin(a), sin(b)), add(cos(a), cos(b))),  tan(div(sub(a, b), 2))],  #div cos(a) + cos(b) != 0 ---> 2 != 0

  # trig-reduce-fp-sound (trigonometry simplify fp-safe)
  ["sin-0",  sin(0),  0],
  ["cos-0",  cos(0),  1],
  ["tan-0",  tan(0),  0],

  # trig-reduce-fp-sound-nan (trigonometry simplify fp-safe-nan)
  ["sin-neg",  sin(neg(x)),  neg(sin(x))],
  ["cos-neg",  cos(neg(x)),  cos(x)],
  ["tan-neg",  tan(neg(x)),  neg(tan(x))],

  # trig-expand (trigonometry)
  ["sin-sum",             sin(add(x, y)),                                    add(mul(sin(x), cos(y)), mul(cos(x), sin(y)))],
  ["cos-sum",             cos(add(x, y)),                                    sub(mul(cos(x), cos(y)), mul(sin(x), sin(y)))],
  #unsafe ["tan-sum",     tan(add(x, y)),                                    div(add(tan(x), tan(y)), sub(1, mul(tan(x), tan(y))))],         #div () -/-> 1-tan(x)*tan(x) != 0
  ["sin-diff",            sin(sub(x, y)),                                    sub(mul(sin(x), cos(y)), mul(cos(x), sin(y)))],
  ["cos-diff",            cos(sub(x, y)),                                    add(mul(cos(x), cos(y)), mul(sin(x), sin(y)))],
  ["sin-2",               sin(mul(2, x)),                                    mul(2, mul(sin(x), cos(x)))],
  #unknown ["sin-3",      sin(mul(3, x)),                                    sub(mul(3, sin(x)), mul(4, pow(sin(x), 3)))],                   #pow ???
  ["2-sin",               mul(2, mul(sin(x), cos(x))),                       sin(mul(2, x))],
  #unknown ["3-sin",      sub(mul(3, sin(x)), mul(4, pow(sin(x), 3))),       sin(mul(3, x))],                                                #pow ???
  ["cos-2",               cos(mul(2, x)),                                    sub(mul(cos(x), cos(x)), mul(sin(x), sin(x)))],
  #unknown ["cos-3",      cos(mul(3, x)),                                    sub(mul(4, pow(cos(x), 3)), mul(3, cos(x)))],                   #pow ???
  ["2-cos",               sub(mul(cos(x), cos(x)), mul(sin(x), sin(x))),     cos(mul(2, x))],
  #unknown ["3-cos",      sub(mul(4, pow(cos(x), 3)), mul(3, cos(x))),       cos(mul(3, x))],                                                #pow ???
  #unsafe ["tan-2",       tan(mul(2, x)),                                    div(mul(2, tan(x)), sub(1, mul(tan(x), tan(x))))],              #div () -/-> 1-tan(x)*tan(x) != 0
  ["2-tan",               div(mul(2, tan(x)), sub(1, mul(tan(x), tan(x)))),  tan(mul(2, x))],                                                #div 1-tan(x)*tan(x) != 0 ---> ()
  ["sqr-sin-a",           mul(sin(x), sin(x)),                               sub(div(1, 2), mul(div(1, 2), cos(mul(2, x))))],                #div () ---> 2 != 0
  ["sqr-cos-a",           mul(cos(x), cos(x)),                               add(div(1, 2), mul(div(1, 2), cos(mul(2, x))))],                #div () ---> 2 != 0
  ["diff-sin",            sub(sin(x), sin(y)),                               mul(2, mul(sin(div(sub(x, y), 2)), cos(div(add(x, y), 2))))],   #div () ---> 2 != 0
  ["diff-cos",            sub(cos(x), cos(y)),                               mul(neg(2), mul(sin(div(sub(x, y), 2)), sin(div(add(x, y), 2))))],  #div () ---> 2 != 0
  ["sum-sin",             add(sin(x), sin(y)),                               mul(2, mul(sin(div(add(x, y), 2)), cos(div(sub(x, y), 2))))],   #div () ---> 2 != 0
  ["sum-cos",             add(cos(x), cos(y)),                               mul(2, mul(cos(div(add(x, y), 2)), cos(div(sub(x, y), 2))))],   #div () ---> 2 != 0
  ["cos-mult",            mul(cos(x), cos(y)),                               div(add(cos(add(x, y)), cos(sub(x, y))), 2)],                   #div () ---> 2 != 0
  ["sin-mult",            mul(sin(x), sin(y)),                               div(sub(cos(sub(x, y)), cos(add(x, y))), 2)],                   #div () ---> 2 != 0
  ["sin-cos-mult",        mul(sin(x), cos(y)),                               div(add(sin(sub(x, y)), sin(add(x, y))), 2)],                   #div () ---> 2 != 0
  #unknown ["diff-atan",  sub(atan(x), atan(y)),                             atan2(sub(x, y), add(1, mul(x, y)))],                           #atan2 ???
  #unknown ["sum-atan",   add(atan(x), atan(y)),                             atan2(add(x, y), sub(1, mul(x, y)))],                           #atan2 ???
  ["tan-quot",            tan(x),                                            div(sin(x), cos(x))],                                           #div () ---> cos(x) != 0
  ["quot-tan",            div(sin(x), cos(x)),                               tan(x)],                                                        #div cos(x) != 0 ---> ()
  #unsafe ["tan-hang-p",  tan(div(add(a, b), 2)),                            div(add(sin(a), sin(b)), add(cos(a), cos(b)))],                 #div 2 != 0 -/-> cos(a)+cos(b) != 0
  #unsafe ["tan-hang-m",  tan(div(sub(a, b), 2)),                            div(sub(sin(a), sin(b)), add(cos(a), cos(b)))],                 #div 2 != 0 -/-> cos(a)+cos(b) != 0

  # trig-expand-fp-safe (trigonometry fp-safe)
  ["sqr-sin-b",  mul(sin(x), sin(x)),  sub(1, mul(cos(x), cos(x)))],
  ["sqr-cos-b",  mul(cos(x), cos(x)),  sub(1, mul(sin(x), sin(x)))],

  # trig-inverses (trigonometry)
  ["sin-asin",           sin(asin(x)),  x],                                                                                         #asin -1 <= x <= 1 --> ()
  ["cos-acos",           cos(acos(x)),  x],                                                                                         #acos -1 <= x <= 1 --> ()
  ["tan-atan",           tan(atan(x)),  x],
  #unknown ["atan-tan",  atan(tan(x)),  remainder(x, CONST_PI())],                                                                  #remainder ???
  #unknown ["asin-sin",  asin(sin(x)),  sub(fabs(remainder(add(x, div(CONST_PI(), 2)), mul(2, CONST_PI()))), div(CONST_PI(), 2))],  #remainder #asin #div ???
  #unknown ["acos-cos",  acos(cos(x)),  fabs(remainder(x, mul(2, CONST_PI())))],                                                    #remainder #acos ???

  # trig-inverses-simplified (trigonometry)
  ["atan-tan-s",           atan(tan(x)),  x],
  #false ["asin-sin-s",  asin(sin(x)),  x],  #asin counterexample x=2, asin(sin(x))~=1.14
  #false ["acos-cos-s",  acos(cos(x)),  x],  #acos counterexample x=4, acos(c0s(x))~=2.28

  # a trig-expand (trigonometry)
  #unknown ["cos-asin",  cos(asin(x)),  sqrt(sub(1, mul(x, x)))],           #asin #sqrt ???
  #unknown ["tan-asin",  tan(asin(x)),  div(x, sqrt(sub(1, mul(x, x))))],   #asin #sqrt #div ???
  #unknown ["sin-acos",  sin(acos(x)),  sqrt(sub(1, mul(x, x)))],           #acos #sqrt ???
  #unknown ["tan-acos",  tan(acos(x)),  div(sqrt(sub(1, mul(x, x))), x)],   #acos #sqrt #div ???
  #unknown ["sin-atan",  sin(atan(x)),  div(x, sqrt(add(1, mul(x, x))))],   #sqrt #div ???
  #unknown ["cos-atan",  cos(atan(x)),  div(1, sqrt(add(1, mul(x, x))))],   #sqrt #div ???
  ["asin-acos",          asin(x),       sub(div(CONST_PI(), 2), acos(x))],  #asin #acos #div -1 <= x <= 1 ---> 2 != 0 && -1 <= x <= 1
  ["acos-asin",          acos(x),       sub(div(CONST_PI(), 2), asin(x))],  #asin #acos #div -1 <= x <= 1 ---> 2 != 0 && -1 <= x <= 1
  ["asin-neg",           asin(neg(x)),  neg(asin(x))],                      #asin -1 <= -x <= 1 --> -1 <= x <= 1
  ["acos-neg",           acos(neg(x)),  sub(CONST_PI(), acos(x))],          #acos -1 <= -x <= 1 --> -1 <= x <= 1
  ["atan-neg",           atan(neg(x)),  neg(atan(x))],

  # Hyperbolic trigonometric functions
  # h trig-reduce (hyperbolic simplify)
  ["sinh-def",     sinh(x),                                            div(sub(exp(x), exp(neg(x))), 2)],                         #div () ---> 2 != 0
  ["cosh-def",     cosh(x),                                            div(add(exp(x), exp(neg(x))), 2)],                         #div () ---> 2 != 0
  ["tanh-def-a",   tanh(x),                                            div(sub(exp(x), exp(neg(x))), add(exp(x), exp(neg(x))))],  #div () ---> exp(x)+exp(-x) != 0
  ["tanh-def-b",   tanh(x),                                            div(sub(exp(mul(2, x)), 1), add(exp(mul(2, x)), 1))],      #div () ---> exp(2*x)+1 != 0
  ["tanh-def-c",   tanh(x),                                            div(sub(1, exp(mul(neg(2), x))), add(1, exp(mul(neg(2), x))))],    #div () ---> 1+exp(-2*x) != 0
  ["sinh-cosh",    sub(mul(cosh(x), cosh(x)), mul(sinh(x), sinh(x))),  1],
  ["sinh-+-cosh",  add(cosh(x), sinh(x)),                              exp(x)],
  ["sinh---cosh",  sub(cosh(x), sinh(x)),                              exp(neg(x))],

  # h trig-expand (hyperbolic)
  ["sinh-undef",         sub(exp(x), exp(neg(x))),                                 mul(2, sinh(x))],
  ["cosh-undef",         add(exp(x), exp(neg(x))),                                 mul(2, cosh(x))],
  ["tanh-undef",         div(sub(exp(x), exp(neg(x))), add(exp(x), exp(neg(x)))),  tanh(x)],                                                        #div exp(x)+exp(-x) != 0 ---> ()
  ["cosh-sum",           cosh(add(x, y)),                                          add(mul(cosh(x), cosh(y)), mul(sinh(x), sinh(y)))],
  ["cosh-diff",          cosh(sub(x, y)),                                          sub(mul(cosh(x), cosh(y)), mul(sinh(x), sinh(y)))],
  ["cosh-2",             cosh(mul(2, x)),                                          add(mul(sinh(x), sinh(x)), mul(cosh(x), cosh(x)))],
  #unsafe ["cosh-1/2",   cosh(div(x, 2)),                                          sqrt(div(add(cosh(x), 1), 2))],                                  #sqrt #div 2 != 0 -/-> 2 != 0 && (cosh(x)+1)/2 >= 0
  ["sinh-sum",           sinh(add(x, y)),                                          add(mul(sinh(x), cosh(y)), mul(cosh(x), sinh(y)))],
  ["sinh-diff",          sinh(sub(x, y)),                                          sub(mul(sinh(x), cosh(y)), mul(cosh(x), sinh(y)))],
  ["sinh-2",             sinh(mul(2, x)),                                          mul(2, mul(sinh(x), cosh(x)))],
  #unsafe ["sinh-1/2",   sinh(div(x, 2)),                                          div(sinh(x), sqrt(mul(2, add(cosh(x), 1))))],                    #sqrt #div 2 != 0 -/->  2*(cosh(x)+1) >= 0 && sqrt(2*(cosh(x)+1)) != 0
  #unsafe ["tanh-sum",   tanh(add(x, y)),                                          div(add(tanh(x), tanh(y)), add(1, mul(tanh(x), tanh(y))))],      #div () -/-> 1+tanh(x)*tanh(y) != 0
  ["tanh-2",             tanh(mul(2, x)),                                          div(mul(2, tanh(x)), add(1, mul(tanh(x), tanh(x))))],            #div () ---> 1+tanh(x)*tanh(x) != 0
  #unsafe ["tanh-1/2",   tanh(div(x, 2)),                                          div(sinh(x), add(cosh(x), 1))],                                  #div () -/-> cosh(x)+1 != 0
  #unsafe ["tanh-1/2*",  tanh(div(x, 2)),                                          div(sub(cosh(x), 1), sinh(x))],                                  #div () -/-> sinh(x) != 0
  ["sum-sinh",           add(sinh(x), sinh(y)),                                    mul(2, mul(sinh(div(add(x, y), 2)), cosh(div(sub(x, y), 2))))],  #div () ---> 2 != 0
  ["sum-cosh",           add(cosh(x), cosh(y)),                                    mul(2, mul(cosh(div(add(x, y), 2)), cosh(div(sub(x, y), 2))))],  #div () ---> 2 != 0
  ["diff-sinh",          sub(sinh(x), sinh(y)),                                    mul(2, mul(cosh(div(add(x, y), 2)), sinh(div(sub(x, y), 2))))],  #div () ---> 2 != 0
  ["diff-cosh",          sub(cosh(x), cosh(y)),                                    mul(2, mul(sinh(div(add(x, y), 2)), sinh(div(sub(x, y), 2))))],  #div () ---> 2 != 0

  # h trig-expand-fp-safe (hyperbolic fp-safe)
  ["sinh-neg",  sinh(neg(x)),  neg(sinh(x))],
  ["sinh-0",    sinh(0),       0],
  ["cosh-neg",  cosh(neg(x)),  cosh(x)],
  ["cosh-0",    cosh(0),       1],

  # ah trig-expand (hyperbolic)
  #unknown ["asinh-def",   asinh(x),                          log(add(x, sqrt(add(mul(x, x), 1))))],    #log #sqrt ???
  #unknown ["acosh-def",   acosh(x),                          log(add(x, sqrt(sub(mul(x, x), 1))))],    #acosh #log #sqrt ???
  #unknown ["atanh-def",   atanh(x),                          div(log(div(add(1, x), sub(1, x))), 2)],  #atanh #log #div ???
  #unknown ["acosh-2",     acosh(sub(mul(2, mul(x, x)), 1)),  mul(2, acosh(x))],                        #acosh ???
  #unknown ["asinh-2",     acosh(add(mul(2, mul(x, x)), 1)),  mul(2, asinh(x))],                        #acosh ???
  ["sinh-asinh",           sinh(asinh(x)),                    x],
  #unknown ["sinh-acosh",  sinh(acosh(x)),                    sqrt(sub(mul(x, x), 1))],                 #acosh #sqrt ???
  #unknown ["sinh-atanh",  sinh(atanh(x)),                    div(x, sqrt(sub(1, mul(x, x))))],         #atanh #sqrt #div ???
  #unsafe ["cosh-asinh",   cosh(asinh(x)),                    sqrt(add(mul(x, x), 1))],                 #sqrt () -/-> x*x+1 >= 0
  #unknown ["cosh-acosh",  cosh(acosh(x)),                    x],                                       #acosh ???
  #unknown ["cosh-atanh",  cosh(atanh(x)),                    div(1, sqrt(sub(1, mul(x, x))))],         #atanh #sqrt #div ???
  #unsafe ["tanh-asinh",   tanh(asinh(x)),                    div(x, sqrt(add(1, mul(x, x))))],         #sqrt #div () -/-> 1+x*x >= 0 && sqrt(1+x*x) != 0
  #unknown ["tanh-acosh",  tanh(acosh(x)),                    div(sqrt(sub(mul(x, x), 1)), x)],         #acosh #sqrt #div ???
  #unknown ["tanh-atanh",  tanh(atanh(x)),                    x],                                       #atanh ???

  # Specialized numerical functions
  # special-numerical-reduce (numerics simplify)
  #unknown ["expm1-def",    sub(exp(x), 1),                   expm1(x)],     #expm1 ???
  #unknown ["log1p-def",    log(add(1, x)),                   log1p(x)],     #log1p #log ???
  #unknown ["log1p-expm1",  log1p(expm1(x)),                  x],            #expm1 #log1p ???
  #unknown ["expm1-log1p",  expm1(log1p(x)),                  x],            #expm1 #log1p ???
  #unknown ["hypot-def",    sqrt(add(mul(x, x), mul(y, y))),  hypot(x, y)],  #hypot #sqrt ???
  #unknown ["hypot-1-def",  sqrt(add(1, mul(y, y))),          hypot(1, y)],  #hypot #sqrt ???
  #bad ["fma-def",          add(mul(x, y), z),                fma(x, y, z)],
  #bad ["fma-neg",          sub(mul(x, y), z),                fma(x, y, neg(z))],
  #bad ["fma-undef",         fma(x, y, z),                     add(mul(x, y), z)],

  # special-numerical-expand (numerics)
  #unknown ["expm1-undef",     expm1(x),     sub(exp(x), 1)],                   #expm1 ???
  #unknown ["log1p-undef",     log1p(x),     log(add(1, x))],                   #log1p #log ???
  #unknown ["log1p-expm1-u",  x,            log1p(expm1(x))],                  #expm1 #log1p ???
  #unknown ["expm1-log1p-u",  x,            expm1(log1p(x))],                  #expm1 #log1p ???
  #unknown ["hypot-undef",     hypot(x, y),  sqrt(add(mul(x, x), mul(y, y)))],  #hypot #sqrt ???

  # numerics-papers (numerics)
  #              "Further Analysis of Kahan's Algorithm for
  #              the Accurate Computation of 2x2 Determinants"
  #              Jeannerod et al., Mathematics of Computation, 2013
  #              a * b - c * d               ===> fma(a, b, -(d * c)) + fma(-d, c, d * c)
  #bad ["prod-diff",  sub(mul(a, b), mul(c, d)),  add(fma(a, b, neg(mul(d, c))), fma(neg(d), c, mul(d, c)))],

  # # compare-reduce (bools simplify fp-safe-nan)
  #skip ["lt-same",   (< x x),         (FALSE)],
  #skip ["gt-same",   (> x x),         (FALSE)],
  #skip ["lte-same",  (<= x x),        (TRUE)],
  #skip ["gte-same",  (>= x x),        (TRUE)],
  #skip ["not-lt",    (not (< x y)),   (>= x y)],
  #skip ["not-gt",    (not (> x y)),   (<= x y)],
  #skip ["not-lte",   (not (<= x y)),  (> x y)],
  #skip ["not-gte",   (not (>= x y)),  (< x y)],

  # # branch-reduce (branches simplify fp-safe)
  #skip ["if-true",        (if (TRUE), x y),    x],
  #skip ["if-false",       (if (FALSE), x y),   y],
  #skip ["if-same",        (if a x x),          x],
  #skip ["if-not",         (if (not a), x y),   (if a y x)],
  #skip ["if-if-or",       (if a x (if b x y))  (if (or a, b), x y)],
  #skip ["if-if-or-not",   (if a x (if b y x))  (if (or a (not b)), x y)],
  #skip ["if-if-and",      (if a (if b x y) y)  (if (and a, b), x y)],
  #skip ["if-if-and-not",  (if a (if b y x) y)  (if (and a (not b)), x y)],

  # erf-rules (special simplify)
  ["erf-odd",   erf(neg(x)),  neg(erf(x))],
  ["erf-erfc",  erfc(x),      sub(1, erf(x))],
  ["erfc-erf",  erf(x),       sub(1, erfc(x))],

  # new rules
  ["add-double-neg",  a,                  neg(neg(a))],
  ["rev-sin-+PI",     neg(sin(x)),        sin(add(x, CONST_PI()))],
  ["rev-sin-+PI/2",   cos(x),             sin(add(x, div(CONST_PI(), 2)))],  #div () ---> 2 != 0
  #["div-factor",      div(mul(a, b), a),  b],
  #["neg-div-factor",  div(neg(mul(a, b)), a),  neg(b)],
  ["inject_2pi", x, sub(add(x, mul(2, CONST_PI())), mul(2, CONST_PI()))],
  ["inject_neg_2pi", x, add(sub(x, mul(2, CONST_PI())), mul(2, CONST_PI()))],
  ["fraction_cancellation", add(sub(div(x, 2), x), div(x, 2)), 0 ],
]

rules = list()
for l in raw_rules:
    name = l[0]
    frm = l[1]
    to = l[2]
    rules.append(Rewrite(frm, to, name))

