#!bin/bash

# for this one, we're running megalibm from pre-set renumo rules
# we want to generate the comparison between baseline and new here.
# so, we want to run the script with locally-generated.
# use make nightly, get all the relevant json, and run the script that generates
# comparison plots. 

cargo test --release --package ruler --test exponential -- test::run --exact --nocapture >> out/log.txt
cargo test --release --package ruler --test rational    -- test::run --exact --nocapture >> out/log.txt
cargo test --release --package ruler --test trig        -- test::run --exact --nocapture >> out/log.txt
cp ../../../nightly/data/output.json *

make
make nightly

# now run comparison 
python graph_against_baseline.py --directory=nightlies/run/

# also, write to results