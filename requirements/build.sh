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

# rust
echo "Installing rust"
RUST_HOME="${SCRIPT_LOCATION}/rust"
DONE_RUST_MARKER="${RUST_HOME}/done"
export RUSTUP_HOME="${RUST_HOME}"      # needed since rustup doesn't have --prefix
export CARGO_HOME="${RUST_HOME}/cargo" # ditto
if [ -f "${DONE_RUST_MARKER}" ]; then
    echo "  rust already installed"
else
    cd "${SCRIPT_LOCATION}"

    echo "  Cleaning build location"
    rm -rf rust

    echo "  Dowloading and running rustup script"
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
        >>"${LOG}" 2>&1

    echo "  Done"
    touch "${DONE_RUST_MARKER}"
fi

export PATH="${CARGO_HOME}/bin:${PATH}"

echo "export RUSTUP_HOME=\"${RUST_HOME}\"" >>"${DEBUG_ENV}"
echo "export CARGO_HOME=\"${RUST_HOME}/cargo\"" >>"${DEBUG_ENV}"
echo "export PATH=\"${CARGO_HOME}/bin:\$PATH"\" >>"${DEBUG_ENV}"

# python libraries
python3 -m pip install --upgrade maturin mpmath sly matplotlib z3-solver

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
