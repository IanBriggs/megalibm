#!bin/bash

make

make nightly

# kick the tires
mkdir plots
python graph_against_baseline_local.py