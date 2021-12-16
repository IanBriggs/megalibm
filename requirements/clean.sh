#!/bin/bash


set -e

SCRIPT_LOCATION="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

LOG="${SCRIPT_LOCATION}/log.txt"
rm -f "${LOG}"

DONE_MARKER="${SCRIPT_LOCATION}/done"
rm -f "${DONE_MARKER}"

DEBUG_ENV="${SCRIPT_LOCATION}/debug_env.sh"
rm -f "${DEBUG_ENV}"




# rust
echo "Cleaning rust"
rm -rf "${SCRIPT_LOCATION}/rust"

# # egg
# echo "Cleaning egg"
# rm -rf "${SCRIPT_LOCATION}/egg"

# snake_egg
echo "Cleaning snake_egg"
rm -rf "${SCRIPT_LOCATION}/snake_egg"

# remove various files
echo "Cleaning build.sh"
rm -f "${LOG}"
rm -f "${DONE_MARKER}"
rm -f "${DEBUG_ENV}"
