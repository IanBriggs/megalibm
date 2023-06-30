#!/bin/bash

set -x
set -e

# Locations
SCRIPT_DIR=$(dirname "${0}")
SCRIPT_LOCATION=$(readlink -f "${SCRIPT_DIR}")
GIT_LOCATION=$(cd "${SCRIPT_LOCATION}" && cd .. && pwd)
NIGHTLIES_LOCATION=${GIT_LOCATION}/nightlies
GENERATED_LOCATION=${GIT_LOCATION}/generated

# Used for generative benchmarks
# # Benchmarks
# BENCH_CORE=${GIT_LOCATION}/benchmarks/core_*.fpcore
# BENCH_FUNC=${GIT_LOCATION}/benchmarks/function_*.fpcore
# BENCH_FPBE=${GIT_LOCATION}/benchmarks/fpbench_*.fpcore
# BENCH_HERB=${GIT_LOCATION}/benchmarks/herbie_*.fpcore
# BENCHMARKS=("${BENCH_CORE[@]}" "${BENCH_FUNC[@]}" "${BENCH_FPBE[@]}")
# if [ $# -gt 0 ]; then
#   case $1 in
#   "all")
#     BENCHMARKS="${GIT_LOCATION}/benchmarks"
#     ;;
#   "debug")
#     BENCHMARKS=${GIT_LOCATION}/benchmarks/core_function_sin.fpcore
#     ;;
#   "core")
#     BENCHMARKS="${BENCH_CORE[@]}"
#     ;;
#   "function")
#     BENCHMARKS="${BENCH_FUNC[@]}"
#     ;;
#   "fpbench")
#     BENCHMARKS="${BENCH_FPBE[@]}"
#     ;;
#   "herbie")
#     BENCHMARKS="${BENCH_HERB[@]}"
#     ;;
#   *)
#     echo "Unknown selection: $1"
#     exit 1
#     ;;
#   esac
# fi

# Data
NIGHTLY_TIMESTAMP=$(date +%s)
CORES="$(getconf _NPROCESSORS_ONLN)"
THIS_NIGHTLY_LOCATION=${NIGHTLIES_LOCATION}/${NIGHTLY_TIMESTAMP}

# Make the final directory
mkdir -p "${NIGHTLIES_LOCATION}"
mkdir "${THIS_NIGHTLY_LOCATION}"
mkdir "${GENERATED_LOCATION}"

# # Clean possible remenants
# rm -rf "${GIT_LOCATION}/measurement/timing/generated"
# rm -rf "${GIT_LOCATION}/measurement/error/generated"

# Run the generation in the final directory
cd "${SCRIPT_LOCATION}"
for e in "${GIT_LOCATION}"/mlms/*.py ; do
  time python3 "run_example" "${e}" "$THIS_NIGHTLY_LOCATION"
done

mv "${GIT_LOCATION}/generated/${NIGHTLY_TIMESTAMP}/generated" "${THIS_NIGHTLY_LOCATION}"

cd "${THIS_NIGHTLY_LOCATION}"
"${SCRIPT_LOCATION}"/make_table generated


# Copy data and send notification if on the nightly runner
if [ "$(hostname)" = "nightly" ]; then
  nightly-results publish "${THIS_NIGHTLY_LOCATION}"
fi