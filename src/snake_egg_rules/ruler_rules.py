from sexpdata import loads, dumps, car, cdr
from dataclasses import dataclass
import sys
from urllib.request import urlopen
from urllib.request import HTTPError
from functools import reduce
import re
import json

from operations import *
# from snake_egg_rules.operations import *
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


def assign_to_branch(acc, x):
    acc[x[2]].append(x)
    return acc


def scrape_and_grab_json():
    DOMS_TO_COMBINE = ['rational']

    rule_save_path = "../ruler_rules/"
    url = "http://nightly.cs.washington.edu/reports/ruler/"
    json_folder = "json/"
    sep = "%3A"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    links_to_runs = re.findall("<a href=\"(.*)\">", html)
    print(links_to_runs)

    runs_split = [run.split(sep) for run in links_to_runs]
    runs_split = list(filter(lambda run: len(run) > 1, runs_split))
    print(runs_split)
    runs_split.sort(key=lambda run1: int(run1[0]))

    branches = ['nightlies-tests']
    # branches = list(set([run[2] for run in runs_split]))
    # print(branches)

    # timestamp, "nightly", branch, commit
    runs_split_by_branches = reduce(assign_to_branch, runs_split, dict.fromkeys(branches, []))
    print(runs_split_by_branches)

    for branch_name in branches:
        all_rules = []    
        relevant_runs = runs_split_by_branches[branch_name]
        latest = relevant_runs[-1]    
        print(f"For branch {branch_name}, found {len(relevant_runs)} runs. Latest at time {latest[0]} with commit {latest[3]}.")    
        current_attempt = 1
        while True:
            try:
                # ensures that all domains are taken from the same commit
                for domain in DOMS_TO_COMBINE:
                    page_to_scrape = url + \
                        sep.join(latest) + json_folder + domain + ".json"
                    print(f"Scraping json from {domain}, using {page_to_scrape}")    
                    json_file = json.load(urlopen(page_to_scrape))
                    # print(json_file)
                    all_rules.extend(json_file["rules"])
                break
            except HTTPError as err:
                if err.code == 404:
                    if current_attempt >= len(relevant_runs):
                        raise Exception(
                            f"No json appear to be available for any commits on this branch ({branch_name}).")
                    current_attempt += 1
                    print(current_attempt)
                    latest = relevant_runs[-current_attempt]
                    print(
                        f"This commit failed. Trying again with commit {latest[3]} at time {latest[0]}")
                else:
                    raise err    
        filename = f'{rule_save_path}{branch_name}-{latest[0]}.txt'
        with open(filename, 'w') as f:
            f.write("\n".join(all_rules))
            print(f"Saved collated rules into {filename}.")

        rule_str = process_rules(all_rules)
        evaled_rules = eval(rule_str)
        # print(rules)
        for l in evaled_rules:
            name = l[0]
            frm = l[1]
            to = l[2]
            global rules
            rules.append(Rewrite(frm, to, name))



        # make sure to render them and associate them with the same name

scrape_and_grab_json()


# raw_rules = [
#     ["0", &(b, a), &(a, b)],
#     ["1", ^(b, a), ^(a, b)],
#     ["2", |(b, a), |(a, b)],
#     ["3", &(a, a), a],
#     ["4", a, |(a, a)],
#     ["5", |(a, neg(a)), ^(a, neg(a))],
#     ["6", neg(neg(a)), a],
#     ["7", ^(b, |(b, a)), &(neg(b), a)],
#     ["8", &(b, neg(a)), &(b, ^(b, a))],
#     ["9", ^(b, &(b, a)), &(b, neg(a))],
#     ["10", ^(c, ^(b, a)), ^(a, ^(c, b))],
#     ["11", |(|(c, b), a), |(c, |(b, a))],
#     ["12", &(c, &(b, a)), &(b, &(c, a))],
#     ["13", neg(^(b, a)), ^(b, neg(a))],
#     ["14", ^(b, ^(b, a)), a],
#     ["15", |(b, ^(a, a)), b],
#     ["16", &(a, |(b, a)), a],
#     ["17", |(b, &(b, a)), b],
#     ["18", &(^(b, b), a), ^(b, b)],
#     ["19", |(a, ^(b, a)), |(b, a)],
#     ["20", |(b, neg(a)), |(&(a, b), neg(a))],
#     ["21", |(b, neg(|(b, a))), |(b, neg(a))],
#     ["22", neg(|(b, neg(a))), &(a, neg(b))],
#     ["23", neg(&(b, a)), |(neg(b), neg(a))],
#     ["24", ^(a, &(c, |(b, a))), &(^(c, a), |(b, a))],
#     ["25", ^(b, |(^(c, b), a)), ^(&(b, a), |(c, a))],
#     ["26", ^(|(c, b), |(b, a)), &(neg(b), ^(c, a))],
#     ["27", |(&(c, b), a), |(a, &(b, ^(c, a)))],
#     ["28", &(b, ^(c, &(b, a))), &(b, ^(c, a))],
#     ["29", |(&(c, b), a), &(|(b, a), |(c, a))],
#     ["30", &(c, |(b, a)), &(c, |(b, &(c, a)))],
#     ["31", ^(&(b, c), &(b, a)), &(b, ^(c, a))],
#     ["32", |(&(c, b), &(b, a)), &(b, |(c, a))],
#     ["33", &(b, a), &(a, b)],
#     ["34", |(b, a), |(a, b)],
#     ["35", add(b, a), add(a, b)],
#     ["36", mul(b, a), mul(a, b)],
#     ["37", |(a, a), a],
#     ["38", a, &(a, a)],
#     ["39", |(a, neg(a)), add(a, neg(a))],
#     ["40", a, neg(neg(a))],
#     ["41", mul(b, add(a, a)), mul(a, add(b, b))],
#     ["42", &(neg(b), a), -sub(|(b, a), b)],
#     ["43", -sub(a, &(b, a)), &(neg(b), a)],
#     ["44", mul(b, -sub(a, a)), -sub(a, a)],
#     ["45", |(c, |(b, a)), |(a, |(c, b))],
#     ["46", -sub(c, -sub(b, a)), -sub(a, -sub(b, c))],
#     ["47", -sub(-sub(c, b), a), -sub(-sub(c, a), b)],
#     ["48", add(add(c, b), a), add(b, add(c, a))],
#     ["49", &(c, &(b, a)), &(&(c, b), a)],
#     ["50", mul(mul(c, b), a), mul(b, mul(c, a))],
#     ["51", -sub(c, -sub(b, a)), -sub(add(c, a), b)],
#     ["52", -sub(c, -sub(b, a)), add(-sub(a, b), c)],
#     ["53", -sub(-sub(c, b), a), -sub(c, add(a, b))],
#     ["54", -sub(b, a), sub(-sub(a, b))],
#     ["55", -sub(b, a), add(sub(a), b)],
#     ["56", -sub(b, sub(a)), add(a, b)],
#     ["57", -sub(neg(b), a), -sub(neg(a), b)],
#     ["58", sub(mul(b, a)), mul(sub(b), a)],
#     ["59", -sub(neg(b), a), neg(add(b, a))],
#     ["60", neg(-sub(b, a)), add(a, neg(b))],
#     ["61", add(b, -sub(a, a)), b],
#     ["62", |(-sub(b, b), a), a],
#     ["63", &(a, |(b, a)), a],
#     ["64", |(b, &(b, a)), b],
#     ["65", &(b, -sub(a, a)), -sub(b, b)],
#     ["66", |(add(a, a), sub(a)), sub(&(a, neg(add(a, a))))],
#     ["67", &(add(a, a), neg(a)), &(add(a, a), sub(a))],
#     ["68", |(a, sub(a)), sub(&(a, sub(a)))],
#     ["69", -sub(mul(b, b), mul(a, a)), mul(add(a, b), -sub(b, a))],
#     ["70", add(&(b, a), &(b, a)), &(add(b, b), add(a, a))],
#     ["71", add(|(b, a), |(b, a)), |(add(b, b), add(a, a))],
#     ["72", -sub(b, |(a, -sub(b, a))), &(a, -sub(b, a))],
#     ["73", -sub(b, &(a, -sub(b, a))), |(a, -sub(b, a))],
#     ["74", add(b, a), add(|(b, a), &(b, a))],
#     ["75", add(b, &(a, sub(a))), -sub(b, |(a, sub(a)))],
#     ["76", -sub(b, &(a, sub(a))), add(|(a, sub(a)), b)],
#     ["77", add(a, &(b, sub(a))), -sub(b, |(b, sub(a)))],
#     ["78", sub(&(sub(b), neg(a))), add(b, &(a, sub(b)))],
#     ["79", neg(sub(&(b, a))), add(a, |(b, neg(a)))],
#     ["80", mul(neg(b), a), -sub(sub(a), mul(b, a))],
#     ["81", mul(b, neg(sub(a))), -sub(mul(b, a), b)],
#     ["82", mul(sub(neg(b)), a), add(a, mul(b, a))],
#     ["83", add(a, mul(b, a)), mul(neg(b), sub(a))],
#     ["84", neg(|(b, a)), &(neg(b), neg(a))],
#     ["85", mul(c, -sub(b, neg(a))), add(c, mul(add(b, a), c))],
#     ["86", add(mul(neg(c), b), a), -sub(a, add(b, mul(c, b)))],
#     ["87", -sub(-sub(c, b), mul(b, a)), add(mul(b, neg(a)), c)],
#     ["88", add(b, add(mul(c, b), a)), -sub(a, mul(neg(c), b))],
#     ["89", mul(c, add(b, neg(a))), -sub(mul(c, -sub(b, a)), c)],
#     ["90", |(&(c, b), a), |(a, &(c, |(b, a)))],
#     ["91", &(c, |(b, a)), |(&(c, b), &(c, a))],
#     ["92", &(|(c, b), |(b, a)), |(b, &(c, a))],
#     ["93", mul(c, add(b, a)), add(mul(a, c), mul(b, c))],
#     ["94", &(b, a), &(a, b)],
#     ["95", |(b, a), |(a, b)],
#     ["96", add(b, a), add(a, b)],
#     ["97", mul(b, a), mul(a, b)],
#     ["98", |(a, a), a],
#     ["99", a, &(a, a)],
#     ["100", |(a, neg(a)), add(a, neg(a))],
#     ["101", a, neg(neg(a))],
#     ["102", mul(b, add(a, a)), mul(a, add(b, b))],
#     ["103", &(neg(b), a), -sub(|(b, a), b)],
#     ["104", -sub(a, &(b, a)), &(neg(b), a)],
#     ["105", mul(b, -sub(a, a)), -sub(a, a)],
#     ["106", |(c, |(b, a)), |(a, |(c, b))],
#     ["107", -sub(c, -sub(b, a)), -sub(a, -sub(b, c))],
#     ["108", -sub(-sub(c, b), a), -sub(-sub(c, a), b)],
#     ["109", add(add(c, b), a), add(b, add(c, a))],
#     ["110", &(c, &(b, a)), &(&(c, b), a)],
#     ["111", mul(mul(c, b), a), mul(b, mul(c, a))],
#     ["112", -sub(c, -sub(b, a)), -sub(add(c, a), b)],
#     ["113", -sub(c, -sub(b, a)), add(-sub(a, b), c)],
#     ["114", -sub(-sub(c, b), a), -sub(c, add(a, b))],
#     ["115", -sub(b, a), sub(-sub(a, b))],
#     ["116", -sub(b, a), add(sub(a), b)],
#     ["117", -sub(b, sub(a)), add(a, b)],
#     ["118", -sub(neg(b), a), -sub(neg(a), b)],
#     ["119", sub(mul(b, a)), mul(sub(b), a)],
#     ["120", -sub(neg(b), a), neg(add(b, a))],
#     ["121", neg(-sub(b, a)), add(a, neg(b))],
#     ["122", add(b, -sub(a, a)), b],
#     ["123", |(-sub(b, b), a), a],
#     ["124", &(a, |(b, a)), a],
#     ["125", |(b, &(b, a)), b],
#     ["126", &(b, -sub(a, a)), -sub(b, b)],
#     ["127", |(add(a, a), sub(a)), -sub(&(a, add(a, a)), a)],
#     ["128", &(add(a, a), neg(a)), &(add(a, a), sub(a))],
#     ["129", sub(|(a, sub(a))), &(a, sub(a))],
#     ["130", |(a, sub(a)), sub(&(a, sub(a)))],
#     ["131", -sub(mul(b, b), mul(a, a)), mul(add(a, b), -sub(b, a))],
#     ["132", add(&(b, a), &(b, a)), &(add(b, b), add(a, a))],
#     ["133", add(|(b, a), |(b, a)), |(add(b, b), add(a, a))],
#     ["134", mul(-sub(b, neg(b)), a), add(a, mul(b, add(a, a)))],
#     ["135", -sub(b, |(a, -sub(b, a))), &(a, -sub(b, a))],
#     ["136", -sub(b, &(a, -sub(b, a))), |(a, -sub(b, a))],
#     ["137", add(b, a), add(&(b, a), |(b, a))],
#     ["138", -sub(mul(b, a), mul(b, a)), -sub(b, b)],
#     ["139", add(b, &(a, sub(a))), -sub(b, |(a, sub(a)))],
#     ["140", -sub(b, &(a, sub(a))), add(|(a, sub(a)), b)],
#     ["141", add(a, &(b, sub(a))), sub(&(neg(b), sub(a)))],
#     ["142", neg(sub(&(b, a))), add(b, |(neg(b), a))],
#     ["143", mul(b, add(a, neg(a))), sub(b)],
#     ["144", mul(neg(sub(b)), a), -sub(mul(b, a), a)],
#     ["145", neg(|(b, a)), &(neg(b), neg(a))],
#     ["146", |(&(c, b), a), |(a, &(c, |(b, a)))],
#     ["147", &(c, |(b, a)), |(&(c, b), &(c, a))],
#     ["148", &(|(c, b), |(b, a)), |(b, &(c, a))],
#     ["149", mul(c, add(b, a)), add(mul(a, c), mul(b, c))]]

# rules = list()
# for l in raw_rules:
#     name = l[0]
#     frm = l[1]
#     to = l[2]
#     rules.append(Rewrite(frm, to, name))
