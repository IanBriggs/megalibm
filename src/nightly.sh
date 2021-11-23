#!/bin/bash

set -x
#set -e

SCRIPT_DIR=$(dirname "${0}")
SCRIPT_LOCATION=$(readlink -f "${SCRIPT_DIR}")


check_date=$(date +%s)
GIT_LOCATION=$(cd "${SCRIPT_LOCATION}" && cd .. && pwd)
NIGHTLIES_LOCATION=${GIT_LOCATION}/nightlies
THIS_NIGHTLY_LOCATION=${NIGHTLIES_LOCATION}/${check_date}

mkdir -p "${NIGHTLIES_LOCATION}"
mkdir "${THIS_NIGHTLY_LOCATION}"

do_one() {
    fname="${1}"
    fstr="${2}"
    low="${3}"
    high="${4}"
    cat <<EOF > "${THIS_NIGHTLY_LOCATION}/${fname}.html"
    <!doctype html>
    <html>
    <head>
    <title>${fname}: Megalibm Results for $(date +%Y-%m-%d)</title>
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: auto auto auto auto;
    }
    .func {
          font-size: 300%;
    }
    </style>
    </head>
    <body>
    <h1>${fname}</h1>
    <div class="func">${fstr}</div>
EOF

    # Run megalibm
    cd "${GIT_LOCATION}/measurement/error"
    mkdir -p generated
    cd generated
    echo "<pre>" >> "${THIS_NIGHTLY_LOCATION}/${fname}.html"
    ../../../examples/synthesize_many.py "${fname}" "${fstr}" "${low}" "${high}"
    cat "${fname}.c"
    echo "</pre>" >> "${THIS_NIGHTLY_LOCATION}/${fname}.html"

    cd "${GIT_LOCATION}/measurement/error"
    make
    mkdir -p data

    cat <<EOF >> "${THIS_NIGHTLY_LOCATION}/${fname}.html"
    <div class="grid-container">
    <div class="grid-item"> <center> Input Set </center> </div>
    <div class="grid-item"> <center> Epsilon vs Delta </center> </div>
    <div class="grid-item"> <center> Absolute Error </center> </div>
    <div class="grid-item"> <center> Relative Error</center> </div>
EOF

    echo "" >> "${THIS_NIGHTLY_LOCATION}/${fname}.html"
    for i in 0 1 2 3
    do
        ./bin/main_"${fname}" $i > data/"${fname}_error_$i.json"
        cat <<EOF >> "${THIS_NIGHTLY_LOCATION}/${fname}.html"
        <div class="grid-item"> Set ${i} </div>
        <div class="grid-item">
        <img src="${fname}_Absolute_vs_Relative_Error_Domain_${i}.png" style="width:100%">
        </div>
        <div class="grid-item">
        <img src="${fname}_Absolute_Error_Domain_${i}.png" style="width:100%">
        </div>
        <div class="grid-item">
        <img src="${fname}_Relative_Error_Domain_${i}.png" style="width:100%">
        </div>
EOF

        ./scripts/plot_error.py "data/${fname}_error_${i}.json"
        mv ./data/*.png "${THIS_NIGHTLY_LOCATION}"
    done

    cat <<EOF >> "${THIS_NIGHTLY_LOCATION}/${fname}.html"
    </div>
    </body>
    </html>
EOF

    echo "<li><a href=${fname}.html>${fname}</a></li>" >> "${THIS_NIGHTLY_LOCATION}/index.html"

}


cat <<EOF > "${THIS_NIGHTLY_LOCATION}/index.html"
<!doctype html>
<html>
<head>
<title>Megalibm Results for $(date +%Y-%m-%d)</title>
</head>
<body>
<h1>Generation Suported:</h1>
<ul>
EOF

do_one "NMSE_example_3_4" "(FPCore (x) (/ (- 1 (cos x)) (sin x)))" "(- INFINITY)" "INFINITY"
do_one "cosine" "(FPCore (x) (cos x))" "(- INFINITY)" "INFINITY"
do_one "exsec" "(FPCore (x) (- (/ 1 (cos x)) 1))" "(- INFINITY)" "INFINITY"
do_one "logarithm" "(FPCore (x) (log x))" "0.0" "INFINITY"
do_one "sine" "(FPCore (x) (sin x))" "(- INFINITY)" "INFINITY"
do_one "tangent" "(FPCore (x) (tan x))" "(- INFINITY)" "INFINITY"
do_one "tanhf" "(FPCore (x) (/ (- 1 (cos x)) (sin x)))" "(- INFINITY)" "INFINITY"
do_one "vercosin" "(FPCore (x) (+ 1 (cos x)))" "(- INFINITY)" "INFINITY"
do_one "versin" "(FPCore (x) (- 1 (cos x)))" "(- INFINITY)" "INFINITY"




cat <<EOF >> "${THIS_NIGHTLY_LOCATION}/index.html"
</ul>
<h1>Generation Not Suported:</h1>
<ul>
EOF

do_one "NMSE_example_3_1" "(FPCore (x) (- (sqrt (+ x 1)) (sqrt x)))" "0.0" "INFINITY"
do_one "NMSE_example_3_10" "(FPCore (x) (/ (log (- 1 x)) (log (+ 1 x))))" "(- INFINITY)" "INFINITY"
do_one "NMSE_example_3_5" "(FPCore (N) (- (atan (+ N 1)) (atan N)))" "(- INFINITY)" "INFINITY"
do_one "NMSE_example_3_7" "(FPCore (x) (- (exp x) 1))" "(- INFINITY)" "INFINITY"
do_one "NMSE_example_3_8" "(FPCore (N) (- (- (* (+ N 1) (log (+ N 1))) (* N (log N))) 1))" "0.0" "INFINITY"
do_one "NMSE_example_3_9" "(FPCore (x) (- (/ 1 x) (/ 1 (tan x))))" "(- INFINITY)" "INFINITY"
do_one "NMSE_problem_3_3_4" "(FPCore (x) (- (pow (+ x 1) (/ 1 3)) (pow x (/ 1 3))))" "0.0" "INFINITY"
do_one "NMSE_problem_3_3_6" "(FPCore (N) (- (log (+ N 1)) (log N)))" "0.0" "INFINITY"
do_one "NMSE_problem_3_3_7" "(FPCore (x) (+ (- (exp x) 2) (exp (- x))))" "(- INFINITY)" "INFINITY"
do_one "NMSE_problem_3_4_1" "(FPCore (x) (/ (- 1 (cos x)) (* x x)))" "(- INFINITY)" "INFINITY"
do_one "covercosin" "(FPCore (x) (+ 1 (sin x)))" "(- INFINITY)" "INFINITY"
do_one "coversin" "(FPCore (x) (- 1 (sin x)))" "(- INFINITY)" "INFINITY"
do_one "exosec" "(FPCore (x) (- (/ 1 (sin x)) 1))" "(- INFINITY)" "INFINITY"
do_one "exponential" "(FPCore (x) (exp x))" "(- INFINITY)" "INFINITY"
do_one "exponential_minus_one" "(FPCore (x) (- (exp x) 1))" "(- INFINITY)" "INFINITY"
do_one "hacovercosin" "(FPCore (x) (/ (+ 1 (sin x)) 2))" "(- INFINITY)" "INFINITY"
do_one "hacoversin" "(FPCore (x) (/ (- 1 (sin x)) 2))" "(- INFINITY)" "INFINITY"
do_one "havercosin" "(FPCore (x) (/ (+ 1 (cos x)) 2))" "(- INFINITY)" "INFINITY"
do_one "haversin" "(FPCore (x) (/ (- 1 (cos x)) 2))" "(- INFINITY)" "INFINITY"
do_one "logarithm_one_plus" "(FPCore (x) (log (+ x 1)))" "0" "INFINITY"

cat <<EOF >> "${THIS_NIGHTLY_LOCATION}/index.html"
</ul>
</body>
</html>
EOF

# Domain issues
# do_one "NMSE_example_3_6" "(FPCore (x) (- (/ 1 (sqrt x)) (/ 1 (sqrt (+ x 1)))))" "0.0" "INFINITY"

# Requires adding let
# do_one "logexp" "(FPCore (x) (let ([e (exp x)]) (log (+ 1 e))))"
# do_one "verhulst" "(FPCore (x) (let ([r 4.0] [K 1.11]) (/ (* r x) (+ 1 (/ x K)))))"
# do_one "predatorPrey" "(FPCore (x) (let ([r 4.0] [K 1.11]) (/ (* (* r x) x) (+ 1 (* (/ x K) (/ x K))))))"
# do_one "carbonGas" "(FPCore (x) (let ([p 3.5e7] [a 0.401] [b 42.7e-6] [t 300] [n 1000] [k 1.3806503e-23]) (- (* (+ p (* (* a (/ n v)) (/ n v))) (- v (* n b))) (* (* k n) t))))"







# Gather output files

if [ "$(hostname)" = "warfa" ] && [ "${USER}" = "p92" ] ; then
    scp -r "${THIS_NIGHTLY_LOCATION}" uwplse.org:/var/www/megalibm/
fi

if command -v nightly-results &>/dev/null; then
    nightly-results url https://megalibm.uwplse.org/"${check_date}/"
fi

