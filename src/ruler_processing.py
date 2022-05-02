from ctypes.wintypes import HDC
import sys
import json
from dataclasses import dataclass

from numpy import isin
from sexpdata import loads, dumps, car, cdr

prelude = """
from snake_egg_rules.operations import *

from snake_egg import EGraph, Rewrite, Var, vars

x, y, z, a, b, c, d = vars("x y z a b c d")

raw_rules = ["""

epilogue = """]

rules = list()
for l in raw_rules:
    name = l[0]
    frm = l[1]
    to = l[2]
    rules.append(Rewrite(frm, to, name))
"""

usage = """USAGE: python ruler_processing.py <input> <output>
    <input>  ruler rules json file
    <output> megalibm rules python file
  """

operator_map = {
  "+ " : "add ",
  "~ " : "neg ",
  "- " : "sub ",
  "* " : "mul ",
  "/ " : "div ",
  "tan " : "tan ",
  "cos " : "cos ",
  "sin " : "sin ",
}

def is_operator(s):
  ops = [op.strip() for op in operator_map.values()]
  return (s in ops)

def lisp_to_c_style(sexpr):
  if not isinstance(sexpr, list):
    return sexpr
  elif isinstance(sexpr, list):
    if sexpr == []:
      return ""
    elif len(sexpr) == 1:
      return dumps(car(sexpr[0]), str_as='symbol') 
    else:
      hd = car(sexpr)
      args = cdr(sexpr)
      hd_s = dumps(lisp_to_c_style (hd), str_as='symbol')
      args_s = [dumps(lisp_to_c_style(a), str_as='symbol') for a in args]
      return hd_s + "(" + ", ".join(args_s) + ")"

def replace_all(sexpr, operator_map):
  for old, new in operator_map.items() :
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
  f.write("\n\t" + repr(rules[0]) + ",\n")
  for i in range(1, len(rules) - 1):
    f.write("\t" + repr(rules[i]) + ",\n")
  # last rule
  f.write("\t" + repr(rules[len(rules) - 1]))  

def process_rules(input, output):
  with open(output, 'w+') as f:
    f.write(prelude)
    count = 0
    rules = []
    content = json.loads(open(input, 'r').read())['new_eqs']
    for c in content:
      if c['bidirectional']:
        r1 = RulerRule(str(count), c['lhs'], c['rhs'])
        count += 1
        rules.append(r1)
        r2 = RulerRule(str(count), c['rhs'], c['lhs'])
        count += 1
        rules.append(r2)
      else:
        r = RulerRule(str(count), c['lhs'], c['rhs'])
        count += 1
        rules.append(r)
    mk_rules(rules, f)
    f.write(epilogue)

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print(usage)
    else:
        process_rules(sys.argv[1], sys.argv[2])