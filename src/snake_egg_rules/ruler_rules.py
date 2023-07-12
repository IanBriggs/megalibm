from sexpdata import loads, dumps, car, cdr, Symbol
from dataclasses import dataclass
import sys
from urllib.request import urlopen
from urllib.request import HTTPError
from functools import reduce
import re
import json

# from operations import *
from snake_egg_rules.operations import *
from snake_egg import EGraph, Rewrite, Var, vars

rules = list() 

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
  "if": "if",
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

def is_if_expr_str(sexpr_str):
    if len(sexpr_str) < 1:
        return False
    sexpr = loads(sexpr_str)
    return is_if_expr(sexpr)

def is_if_expr(sexpr):
    if isinstance(sexpr, str) or isinstance(sexpr, int) or len(sexpr) == 1:
        return False
    if dumps(car(sexpr)) == "if":
        return True
    return any([is_if_expr(x) for x in sexpr]) 
    
#TODO: div by exp(a) should be allowed though 
def is_unsafe_div(sexpr, was_div_present=False):
    # print(sexpr)
    if was_div_present:
        # is there a variable present anywhere left?
        # todo - this needs to be changed to allow div by exp(a)
        # maybe we make another recursive call and only deal with single items 
        # return any(c in dumps(sexpr) for c in ["a", "b", "c"])
        # print(f"sexpr is {sexpr}")
        if (isinstance(sexpr, str) and sexpr in ["a", "b", "c"]) or isinstance(sexpr, Symbol):
            # print("uh oh!")
            # print(sexpr)
            return True 
        elif type(sexpr) is list and dumps(car(sexpr)) == "exp":
            # print("it's exp")
            # print(sexpr)
            return False
        elif type(sexpr) is list:
            # print(dumps(sexpr))
            return any(is_unsafe_div(c, True) for c in dumps(sexpr))
        else:
            # print(f"hmm: {type(sexpr)}")
            return False
        
    if isinstance(sexpr, str) or isinstance(sexpr, int) or len(sexpr) == 1:
        # we know div was not involved, so return False
        # could also be a thunk I guess.. but I assume that won't do anything here... that would be crazy
        return False
    if dumps(car(sexpr)) == "/":
        # if dumps(sexpr[-1]) in ["a", "b", "c"]:
        #     print("yay")
        #     return True
        if dumps(sexpr[-1]).isdigit() or isinstance(sexpr[-1], int):
            return is_unsafe_div(sexpr[1], False)
        elif type(sexpr[-1]) is list:
            return is_unsafe_div(sexpr[-1], True) or is_unsafe_div(sexpr[1], False)
        else:
            # print("huh?")
            # print(dumps(sexpr[-1]))
            # print(type(dumps(sexpr[-1])))
            # print("found pteontially bad")
            return is_unsafe_div(sexpr[-1], True)
    
    return any([is_unsafe_div(x, False) for x in sexpr]) 

def is_unsafe_div_str(sexpr_str):
    # print(sexpr_str)
    if len(sexpr_str) < 1:
        return False
    sexpr = loads(sexpr_str)
    return is_unsafe_div(sexpr, False)

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
        (lhs, rhs) = c.split("==>")
        if ("cis " in lhs) or ("cis " in rhs):
            continue
        else:
            if is_unsafe_div_str(lhs) or is_unsafe_div_str(rhs): # check no unsafe div
                continue
            if is_if_expr_str(lhs) or is_if_expr_str(rhs):
                continue 
            r = RulerRule(str(count), lhs, rhs)
            count += 1
            rules.append(r)
    rules = mk_rules(rules, string_rules)
    # print(rules)
    return rules


def assign_to_branch(acc, x):
    acc[x[2]].append(x)
    return acc


def scrape_and_grab_json():
    DOMS_TO_COMBINE = ['rational_replicate', 'exponential', 'trig']
    TYPE_NAME = "baseline"
    # OPTIONAL_DOMS = ['trig']
    all_rules = []
    # rule_save_path = "ruler_rules/"
    with open("../../output.json", "r") as f:
        page = f.read()
        json_file = json.loads(page)
        # json_file = json.load(urlopen(page_to_scrape))
        # rules = []
        for domain in DOMS_TO_COMBINE:
            print(f"Parsing rules from {domain}, using json at output.json")  
            print(len(json_file)) 
            for item in json_file:
                # print(item)
                if item["TYPE"] == TYPE_NAME: #and item["baseline_name"] == baseline_name:
                    if item["spec_name"] == domain:
                        rules_from_domain = item["rules"]
                        # no_div = list(filter(lambda rule: not is_unsafe_div_str(rule), rules_from_domain))
                        # all_rules.extend(no_div) # todo: need to check if div is safe 
                        all_rules.extend(rules_from_domain)
        
    # print(json_file)
    # all_rules.extend(rules)
            
    all_rules = list(set(all_rules))
    # print("Collated rules before filtering are:")
    # print("\n".join(all_rules))
    rule_str = process_rules(all_rules)
    evaled_rules = eval(rule_str)
    # print(all_rules)
    print(rule_str)
    for l in evaled_rules:
        name = l[0]
        frm = l[1]
        to = l[2]
        global rules
        rules.append(Rewrite(frm, to, name))
    


        # make sure to render them and associate them with the same name

scrape_and_grab_json()
