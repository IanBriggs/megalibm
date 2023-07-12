#include "table_generation.h"
#include "xmalloc.h"
#include "funcs.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

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
  print_json(ENTRY_COUNT, ENTRIES, timings, "core_function_sin", "<pre>\\n(FPCore \\\"core function sin\\\" (x)\\n    :name \\\"core function sin\\\"\\n    :pre (<= (- INFINITY) x INFINITY)\\n  (sin x))\\n</pre>");
  free_memory(timings);
  mpfr_free_cache();
  return 0;
}