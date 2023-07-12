#include "table_generation.h"
#include "xmalloc.h"
#include "funcs.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#define ENTRY_COUNT (4)
entry ENTRIES[ENTRY_COUNT] = {
  {libm_core_function_asin, "libm_core_function_asin"},
  {my_core_function_asin_0, "my_core_function_asin_0"},
  {my_core_function_asin_1, "my_core_function_asin_1"},
  {my_core_function_asin_2, "my_core_function_asin_2"},
};

#define GENERATOR_COUNT (3)
char* GENERATORS[GENERATOR_COUNT] = {
     "(Horner (MinimaxPolynomial (asin x) [(- 1) 1]))",
     "(MirrorLeft (- x) (Horner (MinimaxPolynomial (asin x) [0 1])))",
     "(MirrorRight (- x) (Horner (MinimaxPolynomial (asin x) [(- 1) 0])))",
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
  size_t region_count = ((size_t) 1) << 8;
  size_t samples = ((size_t) 1) << 12;
  double* regions = generate_linear_regions(low, high, region_count);
  error** errorss = generate_table(region_count, regions, samples,
                                   mpfr_core_function_asin,
                                   ENTRY_COUNT, ENTRIES);
  print_json("core_function_asin",
             "<pre>\\n(FPCore \\\"core function asin\\\" (x)\\n    :name \\\"core function asin\\\"\\n    :pre (<= (- 1) x 1)\\n  (asin x))\\n</pre>",
             GENERATOR_COUNT, GENERATORS,
             region_count, regions,
             ENTRY_COUNT, ENTRIES,
             errorss);
  free_table(ENTRY_COUNT, errorss);
  mpfr_free_cache();
  return 0;
}