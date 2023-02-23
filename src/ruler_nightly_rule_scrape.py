from urllib.request import urlopen
from urllib.request import HTTPError
from functools import reduce
import re 
import json
import subprocess

DOMS_TO_COMBINE = ['bool', 'bv4', 'bv32']

rule_save_path = "ruler-rules/"
megalibm_rule_save_path = "src/snake_egg_rules/"
rule_processing_script_path = "src/ruler_processing.py"
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
runs_split.sort(key = lambda run1: int(run1[0]))

branches = list(set([run[2] for run in runs_split]))
print(branches)

# timestamp, "nightly", branch, commit
def assign_to_branch(acc, x):
    acc[x[2]].append(x)
    return acc
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
                page_to_scrape = url + sep.join(latest) + json_folder + domain + ".json"
                print(f"Scraping json from {domain}, using {page_to_scrape}")
        
                json_file = json.load(urlopen(page_to_scrape))
                # print(json_file)
                all_rules.extend(json_file["rules"])
            break
        except HTTPError as err:
            if err.code == 404:
                if current_attempt >= len(relevant_runs):
                    raise Exception(f"No json appear to be available for any commits on this branch ({branch_name}).")
                current_attempt += 1
                print(current_attempt)
                latest = relevant_runs[-current_attempt]
                print(f"This commit failed. Trying again with commit {latest[3]} at time {latest[0]}")
            else:
                raise err
                     
    filename = f'{rule_save_path}{branch_name}-{latest[0]}.txt'
    with open(filename, 'w') as f:
        f.write("\n".join(all_rules))
        print(f"Saved collated rules into {filename}.")
    
    # make sure to render them and associate them with the same name 
    
    try:
        megalibm_filename = f"{megalibm_rule_save_path}ruler_rules.py"
        # megalibm_filename = f"{megalibm_rule_save_path}{branch_name}-{latest[0]}.py"
        subprocess.check_output(["python", rule_processing_script_path, filename, megalibm_filename])
        print(f"Successfully converted rules in {filename} into megalibm rules at {megalibm_filename}")
    except subprocess.CalledProcessError as e:
        print(e.output)

    try:
        subprocess.check_output(["git", "add", megalibm_filename])
        print("Added rule python file.")
        subprocess.check_output(["git", "commit", "-m", f"Running nightlies with rules from {branch_name}-{latest[0]}"])
        print("Committed.")
        # no way this will work lol
        subprocess.check_output(["git", "push"])
    except subprocess.CalledProcessError as e:
        print(e.output)
