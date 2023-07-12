#include "table_generation.h"
#include "xmalloc.h"
#include "funcs.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

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

#define GENERATOR_COUNT (8)
char* GENERATORS[GENERATOR_COUNT] = {
     "(periodic PI (Horner (MinimaxPolynomial (tan x) [0.0 PI])))",
     "(periodic PI (Horner (MinimaxPolynomial (tan x) [(/ (- PI) 2) (/ PI 2)])))",
     "(periodic (- (* PI (- 2))) (Horner (MinimaxPolynomial (tan x) [0.0 (+ PI PI)])))",
     "(periodic (- (* PI (- 2))) (Horner (MinimaxPolynomial (tan x) [(/ (* PI (- 2)) 2) (/ (+ PI PI) 2)])))",
     "(periodic PI (MirrorLeft (- x) (Horner (MinimaxPolynomial (tan x) [0 (/ PI 2)]))))",
     "(periodic PI (MirrorRight (- x) (Horner (MinimaxPolynomial (tan x) [(/ (- PI) 2) 0]))))",
     "(periodic (- (* PI (- 2))) (MirrorLeft (- x) (Horner (MinimaxPolynomial (tan x) [0 (/ (+ PI PI) 2)]))))",
     "(periodic (- (* PI (- 2))) (MirrorRight (- x) (Horner (MinimaxPolynomial (tan x) [(/ (* PI (- 2)) 2) 0]))))",
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
  size_t region_count = ((size_t) 1) << 8;
  size_t samples = ((size_t) 1) << 12;
  double* regions = generate_linear_regions(low, high, region_count);
  error** errorss = generate_table(region_count, regions, samples,
                                   mpfr_core_function_tan,
                                   ENTRY_COUNT, ENTRIES);
  print_json("core_function_tan",
             "<pre>\\n(FPCore \\\"core function tan\\\" (x)\\n    :name \\\"core function tan\\\"\\n    :pre (<= (- INFINITY) x INFINITY)\\n  (tan x))\\n</pre>",
             GENERATOR_COUNT, GENERATORS,
             region_count, regions,
             ENTRY_COUNT, ENTRIES,
             errorss);
  free_table(ENTRY_COUNT, errorss);
  mpfr_free_cache();
  return 0;
}