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

./${GIT_LOCATION}/examples/lambda_versin.py | tee "${THIS_NIGHTLY_LOCATION}/index.html"

cd ${GIT_LOCATION}/measurement/error
make
mkdir -p data
for i in 0 1 2 3 4 5
do
    ./bin/versin_error $i > data/versin_error_$i.tsv
done

./scripts/plot_error.py data/*.tsv | tee "${THIS_NIGHTLY_LOCATION}/index.html"

mv *.png "${THIS_NIGHTLY_LOCATION}"


cat <<EOF >> "${THIS_NIGHTLY_LOCATION}/index.html"
</pre>
EOF

# Gather output files


if [ "$(hostname)" = "warfa" ] && [ "${USER}" = "p92" ] ; then
    scp -r "${THIS_NIGHTLY_LOCATION}" uwplse.org:/var/www/megalibm/
fi

