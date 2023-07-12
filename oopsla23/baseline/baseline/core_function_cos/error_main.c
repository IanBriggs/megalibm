#include "table_generation.h"
#include "xmalloc.h"
#include "funcs.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

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

#define GENERATOR_COUNT (16)
char* GENERATORS[GENERATOR_COUNT] = {
     "(periodic (* PI 4) (Horner (MinimaxPolynomial (cos x) [0.0 (* PI 4)])))",
     "(periodic (* PI 4) (Horner (MinimaxPolynomial (cos x) [(- (+ PI PI)) (+ PI PI)])))",
     "(periodic (+ PI PI) (Horner (MinimaxPolynomial (cos x) [0.0 (+ PI PI)])))",
     "(periodic (+ PI PI) (Horner (MinimaxPolynomial (cos x) [(- PI) PI])))",
     "(periodic (* PI 4) (MirrorLeft (- (+ PI PI) (- (+ PI PI) x)) (Horner (MinimaxPolynomial (cos x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (/ (+ 0 (* 2 (* 2 x))) 4) (Horner (MinimaxPolynomial (cos x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (/ (* 2 x) 2) (Horner (MinimaxPolynomial (cos x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorRight (- (+ PI PI) (- (+ PI PI) x)) (Horner (MinimaxPolynomial (cos x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (/ (+ 0 (* 2 (* 2 x))) 4) (Horner (MinimaxPolynomial (cos x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (/ (* 2 x) 2) (Horner (MinimaxPolynomial (cos x) [(- (+ PI PI)) 0]))))",
     "(periodic (+ PI PI) (MirrorLeft (- (+ PI PI) (- (+ PI PI) x)) (Horner (MinimaxPolynomial (cos x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (/ (+ 0 (* 2 (* 2 x))) 4) (Horner (MinimaxPolynomial (cos x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (/ (* 2 x) 2) (Horner (MinimaxPolynomial (cos x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorRight (- (+ PI PI) (- (+ PI PI) x)) (Horner (MinimaxPolynomial (cos x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (/ (+ 0 (* 2 (* 2 x))) 4) (Horner (MinimaxPolynomial (cos x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (/ (* 2 x) 2) (Horner (MinimaxPolynomial (cos x) [(- PI) 0]))))",
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
                                   mpfr_core_function_cos,
                                   ENTRY_COUNT, ENTRIES);
  print_json("core_function_cos",
             "<pre>\\n(FPCore \\\"core function cos\\\" (x)\\n    :name \\\"core function cos\\\"\\n    :pre (<= (- INFINITY) x INFINITY)\\n  (cos x))\\n</pre>",
             GENERATOR_COUNT, GENERATORS,
             region_count, regions,
             ENTRY_COUNT, ENTRIES,
             errorss);
  free_table(ENTRY_COUNT, errorss);
  mpfr_free_cache();
  return 0;
}