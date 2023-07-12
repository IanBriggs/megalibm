#include "table_generation.h"
#include "xmalloc.h"
#include "funcs.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define ENTRY_COUNT (17)
entry ENTRIES[ENTRY_COUNT] = {
  {libm_core_function_cos, "libm_core_function_cos"},
  {my_core_function_cos_0, "my_core_function_cos_0"},
  {my_core_function_cos_1, "my_core_function_cos_1"},
  {my_core_function_cos_2, "my_core_function_cos_2"},
  {my_core_function_cos_3, "my_core_function_cos_3"},
  {my_core_function_cos_4, "my_core_function_cos_4"},
  {my_core_function_cos_5, "my_core_function_cos_5"},
  {my_core_function_cos_6, "my_core_function_cos_6"},
  {my_core_function_cos_7, "my_core_function_cos_7"},
  {my_core_function_cos_8, "my_core_function_cos_8"},
  {my_core_function_cos_9, "my_core_function_cos_9"},
  {my_core_function_cos_10, "my_core_function_cos_10"},
  {my_core_function_cos_11, "my_core_function_cos_11"},
  {my_core_function_cos_12, "my_core_function_cos_12"},
  {my_core_function_cos_13, "my_core_function_cos_13"},
  {my_core_function_cos_14, "my_core_function_cos_14"},
  {my_core_function_cos_15, "my_core_function_cos_15"},
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
  print_json(ENTRY_COUNT, ENTRIES, timings, "core_function_cos", "<pre>\\n(FPCore \\\"core function cos\\\" (x)\\n    :name \\\"core function cos\\\"\\n    :pre (<= (- INFINITY) x INFINITY)\\n  (cos x))\\n</pre>");
  free_memory(timings);
  mpfr_free_cache();
  return 0;
}