#!/bin/bash

set -x
set -e

SCRIPT_DIR=$(dirname "${0}")
SCRIPT_LOCATION=$(readlink -f "${SCRIPT_DIR}")

GIT_LOCATION=$(cd "${SCRIPT_LOCATION}" && cd .. && pwd)


"${GIT_LOCATION}/examples/lambda_exp.py"

rm -rf "${GIT_LOCATION}/measurement/error/generated"
mkdir "${GIT_LOCATION}/measurement/error/generated"
mv "${GIT_LOCATION}/generated_exp" "${GIT_LOCATION}/measurement/error/generated"

export C_INCLUDE_PATH="/opt/homebrew/include"
export LIBRARY_PATH="/opt/homebrew/lib"

cd "${GIT_LOCATION}/measurement/error/"
make build
make -j2 generated/generated_exp/data_0.json generated/generated_exp/data_1.json
./scripts/plot_error.py generated

echo "View output images located at ${GIT_LOCATION}/measurement/error/generated/generated_exp"