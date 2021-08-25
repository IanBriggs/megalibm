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
<html>
<head>
<title>Megalibm Results for $(date +%Y-%m-%d)</title>
<style>
.grid-container {
    display: grid;
    grid-template-columns: auto auto auto auto;
}
</style>
</head>
<body>
<h1>Versin</h1>
EOF

# Run megalibm
cd ${GIT_LOCATION}/measurement/error
mkdir -p generated
cd generated
echo "<pre>" >> "${THIS_NIGHTLY_LOCATION}/index.html"
../../../examples/lambda_versin.py | tee -a "${THIS_NIGHTLY_LOCATION}/index.html"
echo "</pre>" >> "${THIS_NIGHTLY_LOCATION}/index.html"

cd ${GIT_LOCATION}/measurement/error
make
mkdir -p data

cat <<EOF >> "${THIS_NIGHTLY_LOCATION}/index.html"
<div class="grid-container">
    <div class="grid-item"> <center> Input Set </center> </div>
    <div class="grid-item"> <center> Epsilon vs Delta </center> </div>
    <div class="grid-item"> <center> Absolute Error </center> </div>
    <div class="grid-item"> <center> Relative Error</center> </div>

EOF
echo "" >> "${THIS_NIGHTLY_LOCATION}/index.html"
for i in 0 1 2 3
do
    ./bin/main_versin $i > data/versin_error_$i.json
    cat <<EOF >> "${THIS_NIGHTLY_LOCATION}/index.html"
    <div class="grid-item"> Set ${i} </div>
    <div class="grid-item">
         <img src="Absolute_vs_Relative_Error_Domain_${i}.png" style="width:100%">
    </div>
    <div class="grid-item">
         <img src="Absolute_Error_Domain_${i}.png" style="width:100%">
    </div>
    <div class="grid-item">
         <img src="Relative_Error_Domain_${i}.png" style="width:100%">
    </div>

EOF
done

echo "</div>" >> "${THIS_NIGHTLY_LOCATION}/index.html"

./scripts/plot_error.py data/*.json
mv *.png "${THIS_NIGHTLY_LOCATION}"


echo "</body>" >> "${THIS_NIGHTLY_LOCATION}/index.html"
echo "</html>" >> "${THIS_NIGHTLY_LOCATION}/index.html"

# Gather output files

if [ "$(hostname)" = "warfa" ] && [ "${USER}" = "p92" ] ; then
    scp -r "${THIS_NIGHTLY_LOCATION}" uwplse.org:/var/www/megalibm/
fi

if command -v nightly-results &>/dev/null; then
    nightly-results url https://megalibm.uwplse.org/${check_date}/
fi

