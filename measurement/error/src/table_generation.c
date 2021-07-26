
#include "table_generation.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>




void
generate_table(double low, double high, double step,
               oracle_func F, char* F_name, int len, entry* fs)
{
  assert(finite(low));
  assert(finite(high));
  assert(finite(step));
  assert(low < high);
  assert(high-low > step);
  assert(F_name != NULL);
  assert(len > 0);
  assert(fs != NULL);

  printf("Input %s abs_err_%s rel_err_%s ", F_name, F_name, F_name);
  for (int i=0; i<len; i++) {
    char*f_name = fs[i].name;
    assert(f_name != NULL);
    printf("%s abs_err_%s rel_err_%s ", f_name, f_name, f_name);
  }
  printf("\n");

  mpfr_t real;
  init_oracle(&real);
  for (double x=low; x<=high; x+=step) {
    F(x, &real);
    double rounded = mpfr_get_d(real, MPFR_RNDN);
    double absdiff, reldiff;
    compare_oracle(rounded, &real, &absdiff, &reldiff);
    printf("%1.16e %1.16e %1.16e %1.16e ", x, rounded, absdiff, reldiff);

    for (int i=0; i<len; i++) {
      double actual = fs[i].func(x);
      compare_oracle(actual, &real, &absdiff, &reldiff);
      printf("%1.16e %1.16e %1.16e ", actual, absdiff, reldiff);
    }
    printf("\n");
  }
  clear_oracle(&real);
}
