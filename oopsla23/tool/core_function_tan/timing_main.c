#include "table_generation.h"
#include "xmalloc.h"
#include "funcs.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define ENTRY_COUNT (9)
entry ENTRIES[ENTRY_COUNT] = {
  {libm_core_function_tan, "libm_core_function_tan"},
  {my_core_function_tan_0, "my_core_function_tan_0"},
  {my_core_function_tan_1, "my_core_function_tan_1"},
  {my_core_function_tan_2, "my_core_function_tan_2"},
  {my_core_function_tan_3, "my_core_function_tan_3"},
  {my_core_function_tan_4, "my_core_function_tan_4"},
  {my_core_function_tan_5, "my_core_function_tan_5"},
  {my_core_function_tan_6, "my_core_function_tan_6"},
  {my_core_function_tan_7, "my_core_function_tan_7"},
};

int main(int argc, char** argv)
{
  long int choice = 0;
  if (argc == 2) {
    choice = strtol(argv[1], NULL, 10);
  }
  double low,high;
  switch (choice) {
  case 0:
    low = -32;
    high = 32;
    break;
  case 1:
    low = -8;
    high = 8;
    break;
  case 2:
    low = -2;
    high = 2;
    break;
  case 3:
    low = -1;
    high = 1;
    break;
  default:
    printf("Option not available\n");    exit(1);
  }
  size_t samples = ((size_t) 1) << 12;
  size_t iters = 10000;
  double* timings = time_functions(low, high, ENTRY_COUNT, ENTRIES, samples, iters);
  print_json(ENTRY_COUNT, ENTRIES, timings, "core_function_tan", "<pre>\\n(FPCore \\\"core function tan\\\" (x)\\n    :name \\\"core function tan\\\"\\n    :pre (<= (- INFINITY) x INFINITY)\\n  (tan x))\\n</pre>");
  free_memory(timings);
  mpfr_free_cache();
  return 0;
}