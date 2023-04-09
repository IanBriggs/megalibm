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
    DOMS_TO_COMBINE = ['rational_best', 'exponential', 'trig']
    # OPTIONAL_DOMS = ['trig']

    # rule_save_path = "ruler_rules/"
    url = "http://nightly.cs.washington.edu/reports/ruler/"
    json_folder = "json/"
    # baseline_names = ["herbie", "oopsla"]
    branches_usable = ["main"]
    sep = "%3A"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    links_to_runs = re.findall("<a href=\"(.*)\">", html)
    # print(links_to_runs)

    runs_split = [run.split(sep) for run in links_to_runs]
    runs_split = list(filter(lambda run: len(run) > 1, runs_split))
    # print(runs_split)
    runs_split.sort(key=lambda run1: int(run1[0]))

    # branches = ['nightlies-tests']
    branches = list(set([run[2] for run in runs_split]))
    # branches = runs_split[-1][2]
    # print(branches)

    # timestamp, "nightly", branch, commit
    runs_split_by_branches = reduce(assign_to_branch, runs_split, dict.fromkeys(branches, []))
    # print(runs_split_by_branches)

    all_rules = [] 
    # for branch_name in branches:   
    #     relevant_runs = runs_split_by_branches[branch_name]
    #     latest = relevant_runs[-1]    
    #     print(f"For branch {branch_name}, found {len(relevant_runs)} runs. Latest at time {latest[0]} with commit {latest[3]}.")    
    
    runs_split = list(filter(lambda run: run[2] in branches_usable, runs_split))
    latest = runs_split[-1]

    print(f"Using latest from branch {latest[2]}, at time {latest[0]} with commit {latest[3]}.")
    current_attempt = 1
    while True:
        try:
            # ensures that all domains are taken from the same commit
            # TODO: just scrape the json instead 
            page_to_scrape = page_to_scrape = url + \
                    sep.join(latest) + "/data/output.js"

            page = urlopen(page_to_scrape).read().decode("utf-8")
            # remove the first line because it's a js file because wtf?
            page = page.removeprefix('var data =')
            
            json_file = json.loads(page)
            # json_file = json.load(urlopen(page_to_scrape))
            # rules = []
            for domain in DOMS_TO_COMBINE:
                print(f"Parsing rules from {domain}, using json at {page_to_scrape}")    

                for item in json_file:
                    if item["enumo_spec_name"] == domain: #and item["baseline_name"] == baseline_name:
                        rules_from_domain = item["rules"]["rules"]
                        all_rules.extend(rules_from_domain)
                
            # print(json_file)
            # all_rules.extend(rules)
            break
        except KeyError as err:
            # if err.code == 404:
            if current_attempt >= len(runs_split):
                raise Exception(
                    f"No json appear to be available for any commits on this branch ({latest[2]}).")
            current_attempt += 1
            print(current_attempt)
            latest = runs_split[-current_attempt]
            print(
                f"This commit failed. Trying again with commit {latest[3]} at time {latest[0]}")
            # else:
                # raise err    
            
    # we got the right run, let's see if we can get the other optional domains
    # for domain in OPTIONAL_DOMS:
    #     try:
    #         page_to_scrape = url + \
    #             sep.join(latest) + json_folder + domain + ".json"
    #         print(f"Scraping json from {domain}, using {page_to_scrape}")    
    #         json_file = json.load(urlopen(page_to_scrape))
    #         # print(json_file)
    #         all_rules.extend(json_file["rules"])
    #     except HTTPError as err:
    #         if err.code == 404:
    #             print(f"Optional domain {domain} was not available for commit {latest[3]} on branch {branch_name}.")
    #         else:
    #             raise err 
    
    # filename = f'{rule_save_path}{branch_name}-{latest[0]}.txt'
    # with open(filename, 'w') as f:
    #     f.write("\n".join(all_rules))
    #     print(f"Saved collated rules into {filename}.")
    all_rules = list(set(all_rules))
    print("Collated rules are:")
    print("\n".join(all_rules))
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

