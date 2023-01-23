#!/bin/bash

set -x
set -e

# Locations
SCRIPT_DIR=$(dirname "${0}")
SCRIPT_LOCATION=$(readlink -f "${SCRIPT_DIR}")
GIT_LOCATION=$(cd "${SCRIPT_LOCATION}" && cd .. && pwd)
NIGHTLIES_LOCATION=${GIT_LOCATION}/nightlies

# Benchmarks
BENCHMARKS="${GIT_LOCATION}/benchmarks"
if [ $# -gt 0 ]; then
  case $1 in
  "debug")
    BENCHMARKS=${GIT_LOCATION}/benchmarks/core_function_sin.fpcore
    ;;
  "core")
    BENCHMARKS=${GIT_LOCATION}/benchmarks/core_*.fpcore
    ;;
  "function")
    BENCHMARKS=${GIT_LOCATION}/benchmarks/function_*.fpcore
    ;;
  "fpbench")
    BENCHMARKS=${GIT_LOCATION}/benchmarks/fpbench_*.fpcore
    ;;
  "herbie")
    BENCHMARKS=${GIT_LOCATION}/benchmarks/herbie_*.fpcore
    ;;
  *)
    echo "Unknown selection: $1"
    exit 1
    ;;
  esac
fi

# Data
NIGHTLY_TIMESTAMP=$(date +%s)
CORES="$(getconf _NPROCESSORS_ONLN)"
THIS_NIGHTLY_LOCATION=${NIGHTLIES_LOCATION}/${NIGHTLY_TIMESTAMP}

# Make the final directory
mkdir -p "${NIGHTLIES_LOCATION}"
mkdir "${THIS_NIGHTLY_LOCATION}"

# Clean possible remenants
rm -rf "${GIT_LOCATION}/measurement/timing/generated"
rm -rf "${GIT_LOCATION}/measurement/error/generated"

# Run the generation in the final directory
cd "${THIS_NIGHTLY_LOCATION}"
time "${SCRIPT_LOCATION}"/megalibm_generate ${BENCHMARKS}

# Move generated to timing dir
mv "${THIS_NIGHTLY_LOCATION}/generated" "${GIT_LOCATION}/measurement/timing/"

# Time functions
cd "${GIT_LOCATION}/measurement/timing/"
make -j"${CORES}" build
make -j1 run

# Move generated to error dir
mv "${GIT_LOCATION}/measurement/timing/generated" "${GIT_LOCATION}/measurement/error/"

# Error measurement
cd "${GIT_LOCATION}/measurement/error/"
make -j"${CORES}" build
make -j"${CORES}" run

# Move generated to final directory
mv "${GIT_LOCATION}/measurement/error/generated" "${THIS_NIGHTLY_LOCATION}/generated/"

# Generate website
cd "${THIS_NIGHTLY_LOCATION}"
"${SCRIPT_LOCATION}"/make_website generated

# Copy data and send notification if on the nightly runner
if [ "$(hostname)" = "nightly" ]; then
  nightly-results publish "${THIS_NIGHTLY_LOCATION}"
fi
