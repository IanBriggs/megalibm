
from interval import Interval
from numeric_types import NumericType


def error_function(numeric_type: NumericType,
                   samples: int,
                   c_function_name: str,
                   c_code: str,
                   oracle_function_name: str,
                   oracle_code: str,
                   range: Interval) -> dict:
    if c_function_name is None:
        return None

    cdecl = numeric_type.c_type
    low = numeric_type.num_to_str(range.inf)
    high = numeric_type.num_to_str(range.sup)

    lines = [
        '#include "error_measurement.h"',
        '',
        'int main(int argc, char** argv) {',
        f'  {cdecl} low = {low};'
        f'  {cdecl} high = {high};'
        f'  size_t samples = {samples};'
        '    ',
    ]
    pass

def oracle_values(numeric_type: NumericType,
                   samples: int,
                   oracle_function_name: str,
                   oracle_code: str,
                   range: Interval):
    cdecl = numeric_type.c_type
    low = numeric_type.num_to_str(range.inf)
    high = numeric_type.num_to_str(range.sup)

    lines = [
        '#include "error_measurement.h"',
        '',
        'int main(int argc, char** argv) {',
        f'  {cdecl} low = {low};'
        f'  {cdecl} high = {high};'
        f'  size_t samples = {samples};'
        '   generate_oracle_values_f64()',
    ]