

from sexpdata import loads, dumps, car, cdr
from dataclasses import dataclass
import sys
from urllib.request import urlopen
from urllib.request import HTTPError
from functools import reduce
import re
import json

# from operations import *
from snake_egg_rules.operations import *
# from operations import *
from snake_egg import EGraph, Rewrite, Var, vars


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
sound_div_rules = """(+ ?b ?a) ==> (+ ?a ?b)
(* ?b ?a) ==> (* ?a ?b)
(- ?a ?a) ==> 0
(+ ?a 0) ==> ?a
?a ==> (+ ?a 0)
?a ==> (- ?a 0)
(- ?a 0) ==> ?a
?a ==> (* 1 ?a)
(* 1 ?a) ==> ?a
?a ==> (/ ?a 1)
(/ ?a 1) ==> ?a
(~ ?a) ==> (* ?a -1)
(* ?a -1) ==> (~ ?a)
(~ ?a) ==> (/ ?a -1)
(/ ?a -1) ==> (~ ?a)
(~ ?a) ==> (- 0 ?a)
(- 0 ?a) ==> (~ ?a)
(* ?a 0) ==> 0
(+ ?a -1) ==> (- ?a 1)
(- ?a 1) ==> (+ ?a -1)
(+ 1 ?a) ==> (- ?a -1)
(- ?a -1) ==> (+ 1 ?a)
(/ (+ ?a 1) (- -1 ?a)) ==> (/ (- -1 ?a) (+ ?a 1))
(/ (- -1 ?a) (+ ?a 1)) ==> (/ (+ ?a 1) (- -1 ?a))
(* (- 1 ?a) (/ -1 ?a)) ==> (/ (+ ?a -1) ?a)
(/ (+ ?a -1) ?a) ==> (* (- 1 ?a) (/ -1 ?a))
(* (+ ?a 1) (/ -1 ?a)) ==> (/ (- -1 ?a) ?a)
(/ (- -1 ?a) ?a) ==> (* (+ ?a 1) (/ -1 ?a))
(* ?a (/ -1 ?a)) ==> (- (/ 0 ?a) (/ ?a ?a))
(- (/ 0 ?a) (/ ?a ?a)) ==> (* ?a (/ -1 ?a))
(/ (+ ?a 1) ?a) ==> (* (+ ?a 1) (/ 1 ?a))
(* (+ ?a 1) (/ 1 ?a)) ==> (/ (+ ?a 1) ?a)
(/ (- 1 ?a) ?a) ==> (* (- 1 ?a) (/ 1 ?a))
(* (- 1 ?a) (/ 1 ?a)) ==> (/ (- 1 ?a) ?a)
(/ (/ 0 ?a) (+ ?a ?a)) ==> (/ (/ 0 ?a) ?a)
(/ (/ 0 ?a) ?a) ==> (/ (/ 0 ?a) (+ ?a ?a))
(/ (/ 0 ?a) (* ?a ?a)) ==> (/ (/ 0 ?a) ?a)
(/ (/ 0 ?a) ?a) ==> (/ (/ 0 ?a) (* ?a ?a))
(* ?a (/ 1 ?a)) ==> (* (~ ?a) (/ -1 ?a))
(* (~ ?a) (/ -1 ?a)) ==> (* ?a (/ 1 ?a))
(/ (/ 0 ?a) (~ ?a)) ==> (/ (/ 0 ?a) ?a)
(/ (/ 0 ?a) ?a) ==> (/ (/ 0 ?a) (~ ?a))
(/ (/ 0 ?a) (fabs ?a)) ==> (/ (/ 0 ?a) ?a)
(/ (/ 0 ?a) ?a) ==> (/ (/ 0 ?a) (fabs ?a))
(+ ?c (+ ?b ?a)) ==> (+ ?b (+ ?a ?c))
(* (* ?c ?b) ?a) ==> (* ?b (* ?c ?a))
(- (- ?c ?b) ?a) ==> (- (- ?c ?a) ?b)
(- ?c (- ?b ?a)) ==> (- ?a (- ?b ?c))
(- (- ?c ?b) ?a) ==> (- ?c (+ ?a ?b))
(- (+ ?c ?b) ?a) ==> (+ ?c (- ?b ?a))
(* (- ?c ?b) (~ ?a)) ==> (* (- ?b ?c) ?a)
(+ (~ ?c) (- ?b ?a)) ==> (- ?b (+ ?a ?c))
(+ (- ?a ?c) (- ?b ?a)) ==> (- ?b ?c)
(+ (* ?a ?c) (* ?b ?a)) ==> (* ?a (+ ?b ?c))
(- (* ?a ?c) (* ?b ?a)) ==> (* ?a (- ?c ?b))
(* (+ ?c ?c) (* ?b ?a)) ==> (* (+ ?a ?a) (* ?b ?c))
(* (- ?a ?c) (- ?b ?a)) ==> (* (- ?a ?b) (- ?c ?a))
(* (- ?c ?a) (- ?b ?a)) ==> (* (- ?a ?c) (- ?a ?b))
(* (* ?a ?c) (/ ?b ?a)) ==> (* (* ?a ?b) (/ ?c ?a))
(- (- 1 ?c) (- ?b ?a)) ==> (+ (- ?a ?c) (- 1 ?b))
(+ (- ?c ?b) (- -1 ?a)) ==> (+ (- ?c ?a) (- -1 ?b))
(fabs (- ?b ?a)) ==> (fabs (- ?a ?b))
(fabs (* ?b ?a)) ==> (* (fabs ?b) (fabs ?a))
(* (fabs ?b) (fabs ?a)) ==> (fabs (* ?b ?a))
(- ?b ?a) ==> (- (+ ?a ?b) (+ ?a ?a))
(/ (- ?b ?a) (- ?b ?a)) ==> (/ (- ?a ?b) (- ?a ?b))
(/ (- ?a ?b) (- ?b ?a)) ==> (/ (- ?b ?a) (- ?a ?b))
(/ (* ?a ?b) (/ ?a ?a)) ==> (* (* ?a ?a) (/ ?b ?a))
(* (* ?a ?a) (/ ?b ?a)) ==> (/ (* ?a ?b) (/ ?a ?a))
(- (* ?b ?b) (* ?a ?a)) ==> (* (+ ?a ?b) (- ?b ?a))
(* (+ ?a ?b) (- ?b ?a)) ==> (- (* ?b ?b) (* ?a ?a))
(* ?b (- 1 ?a)) ==> (- ?b (* ?a ?b))
(/ 0 (- ?b ?a)) ==> (/ 0 (- ?a ?b))
(* (* ?a ?b) (/ 0 ?a)) ==> 0
(- ?b ?a) ==> (+ (+ ?b 1) (- -1 ?a))
(* ?b (/ 0 ?a)) ==> (* (+ ?a ?b) (/ 0 ?a))
(* (+ ?a ?b) (/ 0 ?a)) ==> (* ?b (/ 0 ?a))
(* (/ 0 ?b) (/ 0 ?a)) ==> (* (/ ?b ?a) (/ 0 ?b))
(fabs (fabs ?a)) ==> (fabs ?a)
(fabs ?a) ==> (fabs (fabs ?a))
(fabs (* ?a ?a)) ==> (* ?a ?a)
(* ?a ?a) ==> (fabs (* ?a ?a))
(/ ?a (fabs ?a)) ==> (/ (fabs ?a) ?a)
(/ (fabs ?a) ?a) ==> (/ ?a (fabs ?a))
(/ ?a ?a) ==> (/ (fabs ?a) (fabs ?a))
(/ (fabs ?a) (fabs ?a)) ==> (/ ?a ?a)
(+ (fabs ?a) (fabs ?a)) ==> (fabs (+ ?a ?a))
(fabs (+ ?a ?a)) ==> (+ (fabs ?a) (fabs ?a))
(/ ?a (/ ?a ?a)) ==> (* ?a (/ ?a ?a))
(* ?a (/ ?a ?a)) ==> (/ ?a (/ ?a ?a))
(/ (~ ?a) (fabs ?a)) ==> (/ (fabs ?a) (~ ?a))
(/ (fabs ?a) (~ ?a)) ==> (/ (~ ?a) (fabs ?a))
(/ (* ?a ?a) (* ?a ?a)) ==> (/ ?a ?a)
(/ ?a ?a) ==> (/ (* ?a ?a) (* ?a ?a))
(/ ?a ?a) ==> (/ (+ ?a ?a) (+ ?a ?a))
(/ (+ ?a ?a) (+ ?a ?a)) ==> (/ ?a ?a)
(/ (* ?a ?a) ?a) ==> (+ ?a (/ 0 ?a))
(+ ?a (/ 0 ?a)) ==> (/ (* ?a ?a) ?a)
(/ (* ?a ?a) (~ ?a)) ==> (- (/ 0 ?a) ?a)
(- (/ 0 ?a) ?a) ==> (/ (* ?a ?a) (~ ?a))
(/ (* ?a ?a) (fabs ?a)) ==> (+ (fabs ?a) (/ 0 ?a))
(+ (fabs ?a) (/ 0 ?a)) ==> (/ (* ?a ?a) (fabs ?a))
(+ ?a (/ ?a ?a)) ==> (* (+ ?a 1) (/ ?a ?a))
(* (+ ?a 1) (/ ?a ?a)) ==> (+ ?a (/ ?a ?a))
(* (- 1 ?a) (/ ?a ?a)) ==> (- (/ ?a ?a) ?a)
(- (/ ?a ?a) ?a) ==> (* (- 1 ?a) (/ ?a ?a))
(- ?a (/ ?a ?a)) ==> (* (+ ?a -1) (/ ?a ?a))
(* (+ ?a -1) (/ ?a ?a)) ==> (- ?a (/ ?a ?a))
(- (~ ?a) (/ ?a ?a)) ==> (* (- -1 ?a) (/ ?a ?a))
(* (- -1 ?a) (/ ?a ?a)) ==> (- (~ ?a) (/ ?a ?a))
(/ 0 (fabs ?a)) ==> (/ 0 ?a)
(/ 0 ?a) ==> (/ 0 (fabs ?a))
(/ 0 (/ ?a ?a)) ==> 0
(* ?a (/ 0 ?a)) ==> 0
(/ 0 ?a) ==> (/ 0 (* ?a ?a))
(/ 0 (* ?a ?a)) ==> (/ 0 ?a)
(/ 0 ?a) ==> (/ 0 (+ ?a ?a))
(/ 0 (+ ?a ?a)) ==> (/ 0 ?a)"""


trig_no_div = """(+ ?b ?a) ==> (+ ?a ?b)
(* ?b ?a) ==> (* ?a ?b)
(- ?a ?a) ==> 0
(+ ?a 0) ==> ?a
?a ==> (+ ?a 0)
?a ==> (- ?a 0)
(- ?a 0) ==> ?a
?a ==> (* 1 ?a)
(* 1 ?a) ==> ?a
(~ ?a) ==> (* ?a -1)
(* ?a -1) ==> (~ ?a)
(~ ?a) ==> (- 0 ?a)
(- 0 ?a) ==> (~ ?a)
(* ?a 0) ==> 0
(+ ?a -1) ==> (- ?a 1)
(- ?a 1) ==> (+ ?a -1)
(+ 1 ?a) ==> (- ?a -1)
(- ?a -1) ==> (+ 1 ?a)
(+ ?c (+ ?b ?a)) ==> (+ ?b (+ ?a ?c))
(* (* ?c ?b) ?a) ==> (* ?b (* ?c ?a))
(- (- ?c ?b) ?a) ==> (- (- ?c ?a) ?b)
(- ?c (- ?b ?a)) ==> (- ?a (- ?b ?c))
(- (- ?c ?b) ?a) ==> (- ?c (+ ?a ?b))
(- (+ ?c ?b) ?a) ==> (+ ?c (- ?b ?a))
(* (- ?c ?b) (~ ?a)) ==> (* (- ?b ?c) ?a)
(+ (~ ?c) (- ?b ?a)) ==> (- ?b (+ ?a ?c))
(+ (- ?a ?c) (- ?b ?a)) ==> (- ?b ?c)
(+ (* ?a ?c) (* ?b ?a)) ==> (* ?a (+ ?b ?c))
(- (* ?a ?c) (* ?b ?a)) ==> (* ?a (- ?c ?b))
(* (+ ?c ?c) (* ?b ?a)) ==> (* (+ ?a ?a) (* ?b ?c))
(* (- ?a ?c) (- ?b ?a)) ==> (* (- ?a ?b) (- ?c ?a))
(* (- ?c ?a) (- ?b ?a)) ==> (* (- ?a ?c) (- ?a ?b))
(- (- 1 ?c) (- ?b ?a)) ==> (+ (- ?a ?c) (- 1 ?b))
(+ (- ?c ?b) (- -1 ?a)) ==> (+ (- ?c ?a) (- -1 ?b))
(fabs (- ?b ?a)) ==> (fabs (- ?a ?b))
(fabs (* ?b ?a)) ==> (* (fabs ?b) (fabs ?a))
(* (fabs ?b) (fabs ?a)) ==> (fabs (* ?b ?a))
(- ?b ?a) ==> (- (+ ?a ?b) (+ ?a ?a))
(- (* ?b ?b) (* ?a ?a)) ==> (* (+ ?a ?b) (- ?b ?a))
(* (+ ?a ?b) (- ?b ?a)) ==> (- (* ?b ?b) (* ?a ?a))
(* ?b (- 1 ?a)) ==> (- ?b (* ?a ?b))
(- ?b ?a) ==> (+ (+ ?b 1) (- -1 ?a))
(fabs (fabs ?a)) ==> (fabs ?a)
(fabs ?a) ==> (fabs (fabs ?a))
(fabs (* ?a ?a)) ==> (* ?a ?a)
(* ?a ?a) ==> (fabs (* ?a ?a))
(+ (fabs ?a) (fabs ?a)) ==> (fabs (+ ?a ?a))
(fabs (+ ?a ?a)) ==> (+ (fabs ?a) (fabs ?a))"""

trig_div_safe = """?a ==> (/ ?a 1)
(/ ?a 1) ==> ?a
(~ ?a) ==> (/ ?a -1)
(/ ?a -1) ==> (~ ?a)
(/ (+ ?a 1) (- -1 ?a)) ==> (/ (- -1 ?a) (+ ?a 1))
(/ (- -1 ?a) (+ ?a 1)) ==> (/ (+ ?a 1) (- -1 ?a))
(* (- 1 ?a) (/ -1 ?a)) ==> (/ (+ ?a -1) ?a)
(/ (+ ?a -1) ?a) ==> (* (- 1 ?a) (/ -1 ?a))
(* (+ ?a 1) (/ -1 ?a)) ==> (/ (- -1 ?a) ?a)
(/ (- -1 ?a) ?a) ==> (* (+ ?a 1) (/ -1 ?a))
(* ?a (/ -1 ?a)) ==> (- (/ 0 ?a) (/ ?a ?a))
(- (/ 0 ?a) (/ ?a ?a)) ==> (* ?a (/ -1 ?a))
(/ (+ ?a 1) ?a) ==> (* (+ ?a 1) (/ 1 ?a))
(* (+ ?a 1) (/ 1 ?a)) ==> (/ (+ ?a 1) ?a)
(/ (- 1 ?a) ?a) ==> (* (- 1 ?a) (/ 1 ?a))
(* (- 1 ?a) (/ 1 ?a)) ==> (/ (- 1 ?a) ?a)
(/ (/ 0 ?a) (+ ?a ?a)) ==> (/ (/ 0 ?a) ?a)
(/ (/ 0 ?a) ?a) ==> (/ (/ 0 ?a) (+ ?a ?a))
(/ (/ 0 ?a) (* ?a ?a)) ==> (/ (/ 0 ?a) ?a)
(/ (/ 0 ?a) ?a) ==> (/ (/ 0 ?a) (* ?a ?a))
(* ?a (/ 1 ?a)) ==> (* (~ ?a) (/ -1 ?a))
(* (~ ?a) (/ -1 ?a)) ==> (* ?a (/ 1 ?a))
(/ (/ 0 ?a) (~ ?a)) ==> (/ (/ 0 ?a) ?a)
(/ (/ 0 ?a) ?a) ==> (/ (/ 0 ?a) (~ ?a))
(/ (/ 0 ?a) (fabs ?a)) ==> (/ (/ 0 ?a) ?a)
(/ (/ 0 ?a) ?a) ==> (/ (/ 0 ?a) (fabs ?a))
(* (* ?a ?c) (/ ?b ?a)) ==> (* (* ?a ?b) (/ ?c ?a))
(/ (- ?b ?a) (- ?b ?a)) ==> (/ (- ?a ?b) (- ?a ?b))
(/ (- ?a ?b) (- ?b ?a)) ==> (/ (- ?b ?a) (- ?a ?b))
(/ (* ?a ?b) (/ ?a ?a)) ==> (* (* ?a ?a) (/ ?b ?a))
(* (* ?a ?a) (/ ?b ?a)) ==> (/ (* ?a ?b) (/ ?a ?a))
(/ 0 (- ?b ?a)) ==> (/ 0 (- ?a ?b))
(* (* ?a ?b) (/ 0 ?a)) ==> 0
(* ?b (/ 0 ?a)) ==> (* (+ ?a ?b) (/ 0 ?a))
(* (+ ?a ?b) (/ 0 ?a)) ==> (* ?b (/ 0 ?a))
(* (/ 0 ?b) (/ 0 ?a)) ==> (* (/ ?b ?a) (/ 0 ?b))
(/ ?a (fabs ?a)) ==> (/ (fabs ?a) ?a)
(/ (fabs ?a) ?a) ==> (/ ?a (fabs ?a))
(/ ?a ?a) ==> (/ (fabs ?a) (fabs ?a))
(/ (fabs ?a) (fabs ?a)) ==> (/ ?a ?a)
(/ ?a (/ ?a ?a)) ==> (* ?a (/ ?a ?a))
(* ?a (/ ?a ?a)) ==> (/ ?a (/ ?a ?a))
(/ (~ ?a) (fabs ?a)) ==> (/ (fabs ?a) (~ ?a))
(/ (fabs ?a) (~ ?a)) ==> (/ (~ ?a) (fabs ?a))
(/ (* ?a ?a) (* ?a ?a)) ==> (/ ?a ?a)
(/ ?a ?a) ==> (/ (* ?a ?a) (* ?a ?a))
(/ ?a ?a) ==> (/ (+ ?a ?a) (+ ?a ?a))
(/ (+ ?a ?a) (+ ?a ?a)) ==> (/ ?a ?a)
(/ (* ?a ?a) ?a) ==> (+ ?a (/ 0 ?a))"""

# up to and including line 241 succeeded last time 

trig_div = """(+ ?a (/ 0 ?a)) ==> (/ (* ?a ?a) ?a)
(/ (* ?a ?a) (~ ?a)) ==> (- (/ 0 ?a) ?a)
(- (/ 0 ?a) ?a) ==> (/ (* ?a ?a) (~ ?a))
(/ (* ?a ?a) (fabs ?a)) ==> (+ (fabs ?a) (/ 0 ?a))
(+ (fabs ?a) (/ 0 ?a)) ==> (/ (* ?a ?a) (fabs ?a))
(+ ?a (/ ?a ?a)) ==> (* (+ ?a 1) (/ ?a ?a))
(* (+ ?a 1) (/ ?a ?a)) ==> (+ ?a (/ ?a ?a))
(* (- 1 ?a) (/ ?a ?a)) ==> (- (/ ?a ?a) ?a)
(- (/ ?a ?a) ?a) ==> (* (- 1 ?a) (/ ?a ?a))
(- ?a (/ ?a ?a)) ==> (* (+ ?a -1) (/ ?a ?a))
(* (+ ?a -1) (/ ?a ?a)) ==> (- ?a (/ ?a ?a))
(- (~ ?a) (/ ?a ?a)) ==> (* (- -1 ?a) (/ ?a ?a))
(* (- -1 ?a) (/ ?a ?a)) ==> (- (~ ?a) (/ ?a ?a))
(/ 0 (fabs ?a)) ==> (/ 0 ?a)
(/ 0 ?a) ==> (/ 0 (fabs ?a))
(/ 0 (/ ?a ?a)) ==> 0
(* ?a (/ 0 ?a)) ==> 0
(/ 0 ?a) ==> (/ 0 (* ?a ?a))
(/ 0 (* ?a ?a)) ==> (/ 0 ?a)
(/ 0 ?a) ==> (/ 0 (+ ?a ?a))
(/ 0 (+ ?a ?a)) ==> (/ 0 ?a)"""



# Get raw rules from txt
x, y, z, a, b, c, d = vars("x y z a b c d")

operator_map = {
  "+ ": "add ",
  "~ ": "neg ",
  "- ": "sub ",
  "* ": "mul ",
  "/ ": "div ",
  "fabs ": "fabs ",
  "tan ": "tan ",
  "cos ": "cos ",
  "sin ": "sin ",
}


def is_operator(s):
  ops = [op.strip() for op in operator_map.values()]
  return (s in ops)


def lisp_to_c_style(sexpr):
  if not isinstance(sexpr, list):
    return dumps(sexpr, str_as='symbol')
  elif isinstance(sexpr, list):
    if sexpr == []:
      return ""
    elif len(sexpr) == 1:
      return dumps(car(sexpr[0]), str_as='symbol')
    else:
      hd = car(sexpr)
      args = cdr(sexpr)
      hd_s = dumps(lisp_to_c_style(hd), str_as='symbol')
      args_s = [dumps(lisp_to_c_style(a), str_as='symbol') for a in args]
      return hd_s + "(" + ", ".join(args_s) + ")"


def replace_all(sexpr, operator_map):
    for old, new in operator_map.items():
        sexpr = sexpr.replace(old, new)
    return sexpr


def cleanup(expr):
    expr = expr.replace("?", "")
    expr = replace_all(expr, operator_map)
    return str(lisp_to_c_style(loads(expr))).replace("PI", "CONST_PI()")


@dataclass(repr=False)
class RulerRule:
    name: str
    lhs: str
    rhs: str

    def __repr__(self):
        return f'["{self.name}", {cleanup(self.lhs)}, {cleanup(self.rhs)}]'


def mk_rules(rules, f):
    # first rule
    f += "[" + repr(rules[0]) + ",\n"
    for i in range(1, len(rules) - 1):
        f += repr(rules[i]) + ",\n"
    # last rule
    f += (repr(rules[len(rules) - 1])) + "]"
    return f


def process_rules(content):
    # with open(output, 'w+') as f:
    #     f.write(prelude)

    string_rules = ""
    count = 0
    rules = []
    # content = open(input, 'r').readlines()
    for c in content:
        print(c)
        (lhs, rhs) = c.split("==>")
        if ("cis " in lhs) or ("cis " in rhs):
            continue
        else:
            r = RulerRule(str(count), lhs, rhs)
            count += 1
            rules.append(r)
    rules = mk_rules(rules, string_rules)
    # print(rules)
    return rules

all_rules = (sound_div_rules + "\n" + trig_no_div + "\n" + trig_div_safe).split("\n")
rule_str = process_rules(all_rules)

rules = list()
evaled_rules = eval(rule_str)
# print(rules)
for l in evaled_rules:
  name = l[0]
  frm = l[1]
  to = l[2]
  rules.append(Rewrite(frm, to, name))

print(rules)