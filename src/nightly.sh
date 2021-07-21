#!/bin/bash

set -x
set -e

export SCRIPT_LOCATION=$(readlink -f $(dirname $0))

export check_date=$(date +%s)

export MEGALIBM="${SCRIPT_LOCATION}/megalibm"

mkdir "${check_date}"
cat <<EOF > "${check_date}/index.html"
<!doctype html>
<title>Megalibm Results for $(date +%Y-%m-%d)</title>
<pre>
EOF

# Run megalibm

cat <<EOF >> "${check_date}/index.html"
</pre>
EOF

# Gather output files


if [ "$(hostname)" = "warfa" && "${USER}" = "p92" ]; then
    scp -r "${check_date}" uwplse.org:/var/www/megalibm/
fi

