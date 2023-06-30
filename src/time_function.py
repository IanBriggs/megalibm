
import subprocess
from compile import compile_file, link_files
from interval import Interval
from numeric_types import FP32, FP64, NumericType


def time_function(numeric_type: NumericType,
                  c_function_name: str,
                  c_code: str,
                  domain: Interval,
                  samples: int = 1 << 17,
                  iters: int = 100) -> float:
    
    if not c_function_name:
        return None
    

    low = domain.inf.to_libm_c(numeric_type=numeric_type)
    high = domain.sup.to_libm_c(numeric_type=numeric_type)


    if numeric_type == FP64:
        gen = f"time_function_fp64"
    elif numeric_type == FP32:
        gen = f"time_function_fp32"

    lines = [
        '#include "timing_measurement.h"',
        '#include "double_double.h"',
        '#include "cody_waite_reduction.h"',
        '',
        c_code,
        '',
        'int main(int argc, char** argv) {',
        f'  {gen}({c_function_name}, {low}, {high}, {samples}, {iters});',
        '}'
    ]
    c_source = "\n".join(lines)

    fname = f"{c_function_name}.c"
    with open(fname, "w") as f:
        f.write(c_source)

    run_name = f"{c_function_name}_runner"
    obj = compile_file(fname)
    runner = link_files([obj], run_name)
    
    p = subprocess.run(f"./{runner}", capture_output=True)

    return float.fromhex(p.stdout.decode("utf-8"))