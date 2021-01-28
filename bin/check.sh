#!/bin/bash

set -e -x

export SCRIPT_LOCATION=$(readlink -f $(dirname $0))

export check_date=$(date +%s)

export MEGALIBM="${SCRIPT_LOCATION}/megalibm"

mkdir ${check_date}
cat <<EOF > ${check_date}/index.html
<!doctype html>
<title>Megalibm Results for $(date +%Y-%m-%d)</title>
<pre>
EOF

"${MEGALIBM}" |& tee ${check_date}/log.txt
cat optuner_sins.c >> ${check_date}/index.html

cat <<EOF >> ${check_date}/index.html
</pre>
EOF

cp optuner_sins.c optuner_sins.h ${check_date}

if [ "$(hostname)" = "warfa" ]; then
    scp -r ${check_date} uwplse.org:/var/www/megalibm/
fi

