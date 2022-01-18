#!/bin/bash

set -x
set -e

SCRIPT_DIR=$(dirname "${0}")
SCRIPT_LOCATION=$(readlink -f "${SCRIPT_DIR}")


check_date=$(date +%s)
GIT_LOCATION=$(cd "${SCRIPT_LOCATION}" && cd .. && pwd)
NIGHTLIES_LOCATION=${GIT_LOCATION}/nightlies
THIS_NIGHTLY_LOCATION=${NIGHTLIES_LOCATION}/${check_date}

mkdir -p "${NIGHTLIES_LOCATION}"
mkdir "${THIS_NIGHTLY_LOCATION}"


cd "${THIS_NIGHTLY_LOCATION}"
"${SCRIPT_LOCATION}"/script "${GIT_LOCATION}/benchmarks/1_argument"


# Gather output files

if [ "$(hostname)" = "warfa" ] && [ "${USER}" = "p92" ] ; then
    scp -r "${THIS_NIGHTLY_LOCATION}" uwplse.org:/var/www/megalibm/
fi

if command -v nightly-results &>/dev/null; then
    nightly-results url https://megalibm.uwplse.org/"${check_date}/"
fi

