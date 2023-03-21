#!/bin/bash

set -x
set -e

# Locations
SCRIPT_DIR=$(dirname "${0}")
SCRIPT_LOCATION=$(readlink -f "${SCRIPT_DIR}")
GIT_LOCATION=$(cd "${SCRIPT_LOCATION}" && cd .. && pwd)
NIGHTLIES_LOCATION=${GIT_LOCATION}/nightlies

# check args
if [ $# != 1 ] ; then
echo "retry must be given a nightly directory"
exit 1
fi

THIS_NIGHTLY_LOCATION="${PWD}/${1}"

# Clean possible remenants
rm -rf "${GIT_LOCATION}/measurement/timing/generated"
rm -rf "${GIT_LOCATION}/measurement/error/generated"

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