#!/bin/bash

set -x
set -e

SCRIPT_DIR=$(dirname "${0}")
SCRIPT_LOCATION=$(readlink -f "${SCRIPT_DIR}")

check_date=$(date +%s)
GIT_LOCATION=$(cd "${SCRIPT_LOCATION}" && cd .. && pwd)
NIGHTLIES_LOCATION=${GIT_LOCATION}/nightlies
THIS_NIGHTLY_LOCATION=${NIGHTLIES_LOCATION}/mini_${check_date}

mkdir -p "${NIGHTLIES_LOCATION}"
mkdir "${THIS_NIGHTLY_LOCATION}"

# Make temporary splash page for two nightlies
cd "${THIS_NIGHTLY_LOCATION}"

cat <<EOF >index.html
<!doctype html>
<head>
  <meta http-equiv="refresh" content="1; URL=generated/index.html" />
</head>
<body>
  <p>If you are not redirected in five seconds, <a href="generated/index.html">click here</a>.</p>
</body>
EOF

# Run the generation of just cos
time "${SCRIPT_LOCATION}"/megalibm_generate "${GIT_LOCATION}/benchmarks/core_function_cos.fpcore"

# Error
rm -rf "${GIT_LOCATION}/measurement/error/generated"
mv "${THIS_NIGHTLY_LOCATION}/generated/" "${GIT_LOCATION}/measurement/error/"
cd "${GIT_LOCATION}/measurement/error/"
make -j6 build
# make -j6 run
# ./scripts/plot_error.py generated
# rm -r "${GIT_LOCATION}/measurement/timing/generated"
mv generated "${GIT_LOCATION}/measurement/timing/"

# Timing
cd "${GIT_LOCATION}/measurement/timing/"
make -j6 build
make -j1 run
