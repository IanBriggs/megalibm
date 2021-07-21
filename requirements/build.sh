#!/bin/bash


set -e

SCRIPT_LOCATION="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

LOG="${SCRIPT_LOCATION}/log.txt"
rm -f "${LOG}"

DONE_MARKER="${SCRIPT_LOCATION}/done"
rm -f "${DONE_MARKER}"

DEBUG_ENV="${SCRIPT_LOCATION}/debug_env.sh"
rm -f "${DEBUG_ENV}"

SUCCESS=0
function finish {
    if [ "$SUCCESS" == 0 ]
    then
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




# something
echo "Installing something"
DONE_SOMETHING_MARKER="${SCRIPT_LOCATION}/something/done"
if [ -f "${DONE_SOMETHING_MARKER}" ]; then
    echo "  something already installed"
else
    cd "${SCRIPT_LOCATION}"

    echo "  Cleaning build location"
    rm -rf something

    echo "  Building something"
    mkdir something
    echo "something was made" >> "${LOG}" 2>&1

    echo "  Done"
    touch "${DONE_SOMETHING_MARKER}"
fi


# Debug environment source file
cd "${SCRIPT_LOCATION}"
echo "export PATH=${SCRIPT_LOCATION}/something:\$PATH" >> "${DEBUG_ENV}"


# Indicate success
SUCCESS=1
