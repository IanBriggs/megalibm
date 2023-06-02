
import subprocess

import mpmath
import pandas
from compile import compile_file, link_files
from interval import Interval
from numeric_types import FP32, FP64, NumericType


def error_function(numeric_type: NumericType,
                   samples: int,
                   c_function_name: str,
                   c_code: str,
                   oracle_function_name: str,
                   oracle_code: str,
                   range: Interval) -> dict:
    if c_function_name is None:
        return None

    data = oracle_values(numeric_type,
                                samples,
                                oracle_function_name,
                                oracle_code,
                                range)

    data["oracle"] = (
        data["correctly_rounded"].map(lambda d: mpmath.mpf(d))
        + data["diff"].map(lambda d: mpmath.mpf(d))
        )

    function_data = function_values(numeric_type,
                                    samples,
                                    c_function_name,
                                    c_code,
                                    range)

    assert data["input"] == function_data["input"]

    data["function"] = function_data["function"]

    data["f_error"] = data["oracle"] - data["function"]
    data["f_error"] = data["f_error"].map(lambda mp: abs(float(mp)))

    data["cr_error"] = data["oracle"] - data["correctly_rounded"]
    data["cr_error"] = data["cr_error"].map(lambda mp: abs(float(mp)))

    return data


def any_values(is_oracle: bool,
              numeric_type: NumericType,
                  samples: int,
                  function_name: str,
                  code: str,
                  range: Interval):
    low = numeric_type.num_to_str(range.inf)
    high = numeric_type.num_to_str(range.sup)

    value_type = "oracle" if is_oracle else "function"

    if numeric_type == FP64:
        gen = f"generate_{value_type}_values_f64"
    elif numeric_type == FP32:
        gen = f"generate_{value_type}_values_f32"

    lines = [
        '#include "error_measurement.h"',
        '',
        code,
        '',
        'int main(int argc, char** argv) {',
        f'  {gen}({function_name}, {low}, {high}, {samples});',
        '}'
    ]
    c_source = "\n".join(lines)

    fname = f"{function_name}.c"
    with open(fname, "w") as f:
        f.write(c_source)

    run_name = f"{function_name}_runner"
    obj = compile_file(fname, main=True)
    runner = link_files([obj], run_name)

    tsv_name = f"{function_name}.tsv"
    subprocess.run(f"./{runner} > {tsv_name}")

    data = pandas.read_csv(tsv_name, sep='\t')

    for c in data.columns:
        data[c] = data[c].map(lambda s: float.fromhex(s))

    return data

def function_values(numeric_type: NumericType,
                  samples: int,
                  function_name: str,
                  code: str,
                  range: Interval):
    return any_values(False,
                      numeric_type,
                      samples,
                      function_name,
                      code,
                      range)

def oracle_values(numeric_type: NumericType,
                  samples: int,
                  function_name: str,
                  code: str,
                  range: Interval):
    return any_values(True,
                      numeric_type,
                      samples,
                      function_name,
                      code,
                      range)