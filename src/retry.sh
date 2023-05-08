#!/bin/bash

set -x
set -e

# Locations
SCRIPT_DIR=$(dirname "${0}")
SCRIPT_LOCATION=$(readlink -f "${SCRIPT_DIR}")
GIT_LOCATION=$(cd "${SCRIPT_LOCATION}" && cd .. && pwd)
NIGHTLIES_LOCATION=${GIT_LOCATION}/nightlies

CORES="$(getconf _NPROCESSORS_ONLN)"

# check args
if [ $# != 1 ]; then
    echo "retry must be given a nightly directory"
    exit 1
fi

THIS_NIGHTLY_LOCATION="${PWD}/${1}"

# Clean possible remenants
rm -rf "${GIT_LOCATION}/measurement/timing/generated"
rm -rf "${GIT_LOCATION}/measurement/error/generated"

# Clean data to force a regen
find "${THIS_NIGHTLY_LOCATION}/generated/" -name "*.json" -delete
find "${THIS_NIGHTLY_LOCATION}/generated/" -name "*.o" -delete
find "${THIS_NIGHTLY_LOCATION}/generated/" -name "*.png" -delete
find "${THIS_NIGHTLY_LOCATION}/generated/" -name "error_main" -delete
find "${THIS_NIGHTLY_LOCATION}/generated/" -name "timing_main" -delete

# Move generated to timing dir
cp -r "${THIS_NIGHTLY_LOCATION}/generated" "${GIT_LOCATION}/measurement/timing"

# Time functions
cd "${GIT_LOCATION}/measurement/timing"
make -j"${CORES}" build
make -j1 run

# Move generated to error dir
mv "${GIT_LOCATION}/measurement/timing/generated" "${GIT_LOCATION}/measurement/error"

# Error measurement
cd "${GIT_LOCATION}/measurement/error"
make -j"${CORES}" build
make -j"${CORES}" run

# Move generated to final directory
rm -r "${THIS_NIGHTLY_LOCATION}/generated"
mv "${GIT_LOCATION}/measurement/error/generated" "${THIS_NIGHTLY_LOCATION}/generated"

# Generate website
cd "${THIS_NIGHTLY_LOCATION}"
"${SCRIPT_LOCATION}"/make_website generated
