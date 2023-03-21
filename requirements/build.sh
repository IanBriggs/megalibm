#!/bin/bash

set -e

SCRIPT_LOCATION="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LOG="${SCRIPT_LOCATION}/log.txt"
rm -f "${LOG}"

DONE_MARKER="${SCRIPT_LOCATION}/done"
rm -f "${DONE_MARKER}"

DEBUG_ENV="${SCRIPT_LOCATION}/debug_env.sh"
rm -f "${DEBUG_ENV}"

SUCCESS=0
function finish {
    if [ "$SUCCESS" == 0 ]; then
        echo "requirements failed to build."
        echo "See ${LOG} for details."
        echo ""
        tail "${LOG}"
        rm -f "${DONE_MARKER}"
    else
        echo "Success"
        touch "${DONE_MARKER}"
    fi
}
trap finish EXIT

function in_path {
    command -v "$1" &>/dev/null
}


# python libraries
echo "Installing python dependencies"
python3 -m pip install --upgrade --quiet pip
python3 -m pip install --upgrade --quiet maturin mpmath sly matplotlib z3-solver
echo "  Done"

# snake_egg
echo "Installing snake_egg (IanBriggs fork)"
SNAKE_EGG_HOME="${SCRIPT_LOCATION}/snake_egg"
DONE_SNAKE_EGG_MARKER="${SNAKE_EGG_HOME}/done"
if [ -f "${DONE_SNAKE_EGG_MARKER}" ]; then
    echo "  snake_egg already installed"
else
    cd "${SCRIPT_LOCATION}"

    echo "  Cleaning build location"
    rm -rf snake_egg

    echo "  Cloning snake_egg"
    git clone https://github.com/IanBriggs/snake-egg.git snake_egg \
        >>"${LOG}" 2>&1

    echo "  Building snake_egg"
    cd snake_egg
    make >>"${LOG}" 2>&1

    echo "  Done"
    touch "${DONE_SNAKE_EGG_MARKER}"
fi

export PYTHONPATH="${SNAKE_EGG_HOME}/target/release:${PYTHONPATH}"

echo "export PYTHONPATH=\"${SNAKE_EGG_HOME}/target/release:\$PYTHONPATH"\" \
    >>"${DEBUG_ENV}"

# Indicate success
SUCCESS=1
