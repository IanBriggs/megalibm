#!/bin/bash

set -x
set -e

export SCRIPT_LOCATION=$(readlink -f $(dirname $0))


export check_date=$(date +%s)
export GIT_LOCATION=$(cd ${SCRIPT_LOCATION} && cd .. && pwd)
export NIGHTLIES_LOCATION=${GIT_LOCATION}/nightlies
export THIS_NIGHTLY_LOCATION=${NIGHTLIES_LOCATION}/${check_date}

mkdir -p ${NIGHTLIES_LOCATION}
mkdir ${THIS_NIGHTLY_LOCATION}

cat <<EOF > "${THIS_NIGHTLY_LOCATION}/index.html"
<!doctype html>
<title>Megalibm Results for $(date +%Y-%m-%d)</title>
<pre>
EOF

# Run megalibm
cd ${GIT_LOCATION}
for e in ${GIT_LOCATION}/examples/*.py
do
    $e | tee "${THIS_NIGHTLY_LOCATION}/index.html"
done

cat <<EOF >> "${THIS_NIGHTLY_LOCATION}/index.html"
</pre>
EOF

# Gather output files


if [ "$(hostname)" = "warfa" ] && [ "${USER}" = "p92" ] ; then
    scp -r "${check_date}" uwplse.org:/var/www/megalibm/
fi

