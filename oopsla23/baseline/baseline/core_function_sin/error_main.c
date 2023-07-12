#include "table_generation.h"
#include "xmalloc.h"
#include "funcs.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#define ENTRY_COUNT (67)
entry ENTRIES[ENTRY_COUNT] = {
  {libm_core_function_sin, "libm_core_function_sin"},
  {my_core_function_sin_0, "my_core_function_sin_0"},
  {my_core_function_sin_1, "my_core_function_sin_1"},
  {my_core_function_sin_2, "my_core_function_sin_2"},
  {my_core_function_sin_3, "my_core_function_sin_3"},
  {my_core_function_sin_4, "my_core_function_sin_4"},
  {my_core_function_sin_5, "my_core_function_sin_5"},
  {my_core_function_sin_6, "my_core_function_sin_6"},
  {my_core_function_sin_7, "my_core_function_sin_7"},
  {my_core_function_sin_8, "my_core_function_sin_8"},
  {my_core_function_sin_9, "my_core_function_sin_9"},
  {my_core_function_sin_10, "my_core_function_sin_10"},
  {my_core_function_sin_11, "my_core_function_sin_11"},
  {my_core_function_sin_12, "my_core_function_sin_12"},
  {my_core_function_sin_13, "my_core_function_sin_13"},
  {my_core_function_sin_14, "my_core_function_sin_14"},
  {my_core_function_sin_15, "my_core_function_sin_15"},
  {my_core_function_sin_16, "my_core_function_sin_16"},
  {my_core_function_sin_17, "my_core_function_sin_17"},
  {my_core_function_sin_18, "my_core_function_sin_18"},
  {my_core_function_sin_19, "my_core_function_sin_19"},
  {my_core_function_sin_20, "my_core_function_sin_20"},
  {my_core_function_sin_21, "my_core_function_sin_21"},
  {my_core_function_sin_22, "my_core_function_sin_22"},
  {my_core_function_sin_23, "my_core_function_sin_23"},
  {my_core_function_sin_24, "my_core_function_sin_24"},
  {my_core_function_sin_25, "my_core_function_sin_25"},
  {my_core_function_sin_26, "my_core_function_sin_26"},
  {my_core_function_sin_27, "my_core_function_sin_27"},
  {my_core_function_sin_28, "my_core_function_sin_28"},
  {my_core_function_sin_29, "my_core_function_sin_29"},
  {my_core_function_sin_30, "my_core_function_sin_30"},
  {my_core_function_sin_31, "my_core_function_sin_31"},
  {my_core_function_sin_32, "my_core_function_sin_32"},
  {my_core_function_sin_33, "my_core_function_sin_33"},
  {my_core_function_sin_34, "my_core_function_sin_34"},
  {my_core_function_sin_35, "my_core_function_sin_35"},
  {my_core_function_sin_36, "my_core_function_sin_36"},
  {my_core_function_sin_37, "my_core_function_sin_37"},
  {my_core_function_sin_38, "my_core_function_sin_38"},
  {my_core_function_sin_39, "my_core_function_sin_39"},
  {my_core_function_sin_40, "my_core_function_sin_40"},
  {my_core_function_sin_41, "my_core_function_sin_41"},
  {my_core_function_sin_42, "my_core_function_sin_42"},
  {my_core_function_sin_43, "my_core_function_sin_43"},
  {my_core_function_sin_44, "my_core_function_sin_44"},
  {my_core_function_sin_45, "my_core_function_sin_45"},
  {my_core_function_sin_46, "my_core_function_sin_46"},
  {my_core_function_sin_47, "my_core_function_sin_47"},
  {my_core_function_sin_48, "my_core_function_sin_48"},
  {my_core_function_sin_49, "my_core_function_sin_49"},
  {my_core_function_sin_50, "my_core_function_sin_50"},
  {my_core_function_sin_51, "my_core_function_sin_51"},
  {my_core_function_sin_52, "my_core_function_sin_52"},
  {my_core_function_sin_53, "my_core_function_sin_53"},
  {my_core_function_sin_54, "my_core_function_sin_54"},
  {my_core_function_sin_55, "my_core_function_sin_55"},
  {my_core_function_sin_56, "my_core_function_sin_56"},
  {my_core_function_sin_57, "my_core_function_sin_57"},
  {my_core_function_sin_58, "my_core_function_sin_58"},
  {my_core_function_sin_59, "my_core_function_sin_59"},
  {my_core_function_sin_60, "my_core_function_sin_60"},
  {my_core_function_sin_61, "my_core_function_sin_61"},
  {my_core_function_sin_62, "my_core_function_sin_62"},
  {my_core_function_sin_63, "my_core_function_sin_63"},
  {my_core_function_sin_64, "my_core_function_sin_64"},
  {my_core_function_sin_65, "my_core_function_sin_65"},
};

#define GENERATOR_COUNT (66)
char* GENERATORS[GENERATOR_COUNT] = {
     "(periodic (* PI 6) (Horner (MinimaxPolynomial (sin x) [0.0 (* PI 6)])))",
     "(periodic (* PI 6) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) (* PI 3)])))",
     "(periodic (* PI 4) (Horner (MinimaxPolynomial (sin x) [0.0 (* PI 4)])))",
     "(periodic (* PI 4) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) (+ PI PI)])))",
     "(periodic (+ PI PI) (Horner (MinimaxPolynomial (sin x) [0.0 (+ PI PI)])))",
     "(periodic (+ PI PI) (Horner (MinimaxPolynomial (sin x) [(- PI) PI])))",
     "(periodic (* PI 6) (MirrorLeft (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))",
     "(periodic (* PI 6) (MirrorLeft (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))",
     "(periodic (* PI 6) (MirrorLeft (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))",
     "(periodic (* PI 6) (MirrorLeft (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))",
     "(periodic (* PI 6) (MirrorLeft (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))",
     "(periodic (* PI 6) (MirrorLeft (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))",
     "(periodic (* PI 6) (MirrorLeft (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))",
     "(periodic (* PI 6) (MirrorLeft (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))",
     "(periodic (* PI 6) (MirrorLeft (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))",
     "(periodic (* PI 6) (MirrorLeft (- x) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))",
     "(periodic (* PI 6) (MirrorRight (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))",
     "(periodic (* PI 6) (MirrorRight (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))",
     "(periodic (* PI 6) (MirrorRight (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))",
     "(periodic (* PI 6) (MirrorRight (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))",
     "(periodic (* PI 6) (MirrorRight (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))",
     "(periodic (* PI 6) (MirrorRight (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))",
     "(periodic (* PI 6) (MirrorRight (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))",
     "(periodic (* PI 6) (MirrorRight (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))",
     "(periodic (* PI 6) (MirrorRight (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))",
     "(periodic (* PI 6) (MirrorRight (- x) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))",
     "(periodic (* PI 4) (MirrorLeft (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorLeft (- x) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))",
     "(periodic (* PI 4) (MirrorRight (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))",
     "(periodic (* PI 4) (MirrorRight (- x) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))",
     "(periodic (+ PI PI) (MirrorLeft (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorLeft (- x) (Horner (MinimaxPolynomial (sin x) [0 PI]))))",
     "(periodic (+ PI PI) (MirrorRight (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))",
     "(periodic (+ PI PI) (MirrorRight (- x) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))",
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
                                   mpfr_core_function_sin,
                                   ENTRY_COUNT, ENTRIES);
  print_json("core_function_sin",
             "<pre>\\n(FPCore \\\"core function sin\\\" (x)\\n    :name \\\"core function sin\\\"\\n    :pre (<= (- INFINITY) x INFINITY)\\n  (sin x))\\n</pre>",
             GENERATOR_COUNT, GENERATORS,
             region_count, regions,
             ENTRY_COUNT, ENTRIES,
             errorss);
  free_table(ENTRY_COUNT, errorss);
  mpfr_free_cache();
  return 0;
}