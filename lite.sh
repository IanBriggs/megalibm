#!/bin/bash

# for this one, we're running megalibm from pre-set renumo rules
# we want to generate the comparison between baseline and new here.
# so, we want to run the script with locally-generated.
# use make nightly, get all the relevant json, and run the script that generates
# comparison plots. 

rm -rf results/run
rm -rf results/plots
mkdir plots

# run the rules locally. 
cp oopsla23/precomputed.json output.json

make
make nightly

# now run comparison 
python graph_against_baseline.py --directory=results/run/generated/

cp -r results/run/generated results/generated
cp results/run/index.html results/renumo_run.html
cp results/run/style.css results/style.css

cp -r oopsla23/baseline/baseline results/baseline
cp oopsla23/baseline/index.html results/baseline.html
