#!bin/bash

make

make nightly

# kick the tires
python graph_against_baseline_local.py