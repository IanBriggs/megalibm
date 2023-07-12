#include "table_generation.h"
#include "xmalloc.h"
#include "funcs.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define ENTRY_COUNT (4)
entry ENTRIES[ENTRY_COUNT] = {
  {libm_core_function_acos, "libm_core_function_acos"},
  {my_core_function_acos_0, "my_core_function_acos_0"},
  {my_core_function_acos_1, "my_core_function_acos_1"},
  {my_core_function_acos_2, "my_core_function_acos_2"},
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
    low = -1;
    high = 1;
    break;
  case 1:
    low = -0.5;
    high = 0.5;
    break;
  case 2:
    low = -0.25;
    high = 0.25;
    break;
  case 3:
    low = -0.125;
    high = 0.125;
    break;
  default:
    printf("Option not available\n");    exit(1);
  }
  size_t samples = ((size_t) 1) << 12;
  size_t iters = 10000;
  double* timings = time_functions(low, high, ENTRY_COUNT, ENTRIES, samples, iters);
  print_json(ENTRY_COUNT, ENTRIES, timings, "core_function_acos", "<pre>\\n(FPCore \\\"core function acos\\\" (x)\\n    :name \\\"core function acos\\\"\\n    :pre (<= (- 1) x 1)\\n  (acos x))\\n</pre>");
  free_memory(timings);
  mpfr_free_cache();
  return 0;
}