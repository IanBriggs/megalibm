
#include "table_generation.h"
#include "xmalloc.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>



static mpfr_t scratch;

static int
qsort_cmp(const void * va, const void * vb)
{
  const double a = *(const double*)va;
  const double b = *(const double*)vb;

  assert(isfinite(a));
  assert(isfinite(b));

  if (a > b) { return  1; }
  if (a < b) { return -1; }
  return 0;
}

static void
fill_inputs(double low, double high, size_t samples, double* inputs)
{
  double span = high - low;

  for (size_t i=0; i<samples; i++) {
    double dirty_rand = ((double) rand()) / ((double) RAND_MAX);
    inputs[i] = low + span * dirty_rand;
  }

  qsort(inputs, samples, sizeof(double), qsort_cmp);
}


static void
compare(mpfr_t expected, double actual, double* absolute, double* relative)
{
  mpfr_d_sub(scratch, actual, expected, MPFR_RNDN);
  *absolute = fabs(mpfr_get_d(scratch, MPFR_RNDN));

  mpfr_div(scratch, scratch, expected, MPFR_RNDN);
  *relative = fabs(mpfr_get_d(scratch, MPFR_RNDN));
}

static void
run_on_region(unop_fp64 f, size_t samples, double* inputs, mpfr_t* reals,
              double* absolutes, double* relatives, error* ferror)
{
  for (size_t i=0; i<samples; i++) {
    double actual = f(inputs[i]);
    compare(reals[i], actual, &absolutes[i], &relatives[i]);
  }

  qsort(absolutes, samples, sizeof(double), qsort_cmp);
  qsort(relatives, samples, sizeof(double), qsort_cmp);

  double absum = 0.0;
  double relsum = 0.0;
  for (size_t i=0; i<samples; i++) {
    absum += absolutes[i];
    relsum += relatives[i];
  }
  
  ferror->abs_max = absolutes[samples-1];
  ferror->abs_avg = absum/((double) samples);
  ferror->abs_med = absolutes[((size_t) samples/2)];

  ferror->rel_max = relatives[samples-1];
  ferror->rel_avg = relsum/((double) samples);
  ferror->rel_med = relatives[((size_t) samples/2)];
}


double*
generate_linear_regions(double low, double high, size_t region_count)
{
  assert(finite(low));
  assert(finite(high));
  assert(low < high);
  assert(region_count > 0);

  double* retval = (double*) xmalloc(sizeof(double) * (region_count+1));

  double step = (high - low) / ((double) region_count);
  for (size_t i=0; i<region_count; i++) {
    retval[i] = low + ((double) i)*step;
  }
  retval[region_count] = high;

  return retval;
}

void
free_regions(double* regions) {
  assert(regions != NULL);

  xfree(regions);
}


error**
generate_table(size_t region_count, double* regions, size_t samples,
               unop_mpfr oracle,
               size_t func_count, entry* funcs)
{
  assert(region_count > 0);
  assert(regions != NULL);
  assert(samples > 0);
  assert(oracle != NULL);
  assert(func_count > 0);
  assert(funcs != NULL);

  error** errorss = (error**) xmalloc(sizeof(error*) * func_count);
  for (size_t i=0; i<func_count; i++) {
    errorss[i] = (error*) xmalloc(sizeof(error) * region_count);
  }

  mpfr_init2(scratch, ORACLE_PREC);

  mpfr_t* reals = (mpfr_t*) xmalloc(sizeof(mpfr_t) * samples);  
  for (size_t i=0; i<samples; i++) {
    mpfr_init2(reals[i], ORACLE_PREC);
  }
  
  double* inputs = (double*) xmalloc(sizeof(double) * samples);
  double* absolutes = (double*) xmalloc(sizeof(double) * samples);
  double* relatives = (double*) xmalloc(sizeof(double) * samples);

  for (size_t region=0; region<region_count; region++) {
    fill_inputs(regions[region], regions[region+1], samples, inputs);
    for (size_t i=0; i<samples; i++) {
      oracle(reals[i], inputs[i]);
    }

    for (size_t fidx=0; fidx<func_count; fidx++) {
      unop_fp64 f = funcs[fidx].func;
      error* ferror = &errorss[fidx][region];
      run_on_region(f, samples, inputs, reals, absolutes, relatives, ferror);
    }
  }

  xfree(relatives);
  xfree(absolutes);
  xfree(inputs);
  
  for (size_t i=0; i<samples; i++) {
    mpfr_clear(reals[i]);
  }

  xfree(reals);

  mpfr_clear(scratch);

  return errorss;
}

void
free_table(size_t func_count, error** errorss)
{
  assert(errorss != NULL);

  for (size_t i=0; i<func_count; i++) {
    assert(errorss[i] != NULL);
    xfree(errorss[i]);
    errorss[i] = NULL;
  }

  xfree(errorss);
}


void
print_json(size_t region_count, double* regions,
           size_t func_count, entry* funcs,
           error** errorss)
{
  printf("{\n");

  printf("  \"regions\": [\n");
  for (size_t i=0; i<region_count; i++) {
    printf("    %1.16e,\n", regions[i]);
  }
  printf("    %1.16e\n", regions[region_count]);
  printf("  ],\n");

  printf("  \"functions\": {\n");
  for (size_t i=0; i<func_count-1; i++) {
    printf("    \"%s\": {\n", funcs[i].name);

    printf("      \"abs_max_errors\": [\n");
    for (size_t j=0; j<region_count-1; j++) {
      printf("        %1.16e,\n", errorss[i][j].abs_max);
    }
    printf("        %1.16e\n", errorss[i][region_count-1].abs_max);
    printf("      ],\n");

    printf("      \"abs_avg_errors\": [\n");
    for (size_t j=0; j<region_count-1; j++) {
      printf("        %1.16e,\n", errorss[i][j].abs_avg);
    }
    printf("        %1.16e\n", errorss[i][region_count-1].abs_avg);
    printf("      ],\n");

    printf("      \"abs_med_errors\": [\n");
    for (size_t j=0; j<region_count-1; j++) {
      printf("        %1.16e,\n", errorss[i][j].abs_med);
    }
    printf("        %1.16e\n", errorss[i][region_count-1].abs_med);
    printf("      ],\n");

    printf("      \"rel_max_errors\": [\n");
    for (size_t j=0; j<region_count-1; j++) {
      printf("        %1.16e,\n", errorss[i][j].rel_max);
    }
    printf("        %1.16e\n", errorss[i][region_count-1].rel_max);
    printf("      ],\n");

    printf("      \"rel_avg_errors\": [\n");
    for (size_t j=0; j<region_count-1; j++) {
      printf("        %1.16e,\n", errorss[i][j].rel_avg);
    }
    printf("        %1.16e\n", errorss[i][region_count-1].rel_avg);
    printf("      ],\n");

    printf("      \"rel_med_errors\": [\n");
    for (size_t j=0; j<region_count-1; j++) {
      printf("        %1.16e,\n", errorss[i][j].rel_med);
    }
    printf("        %1.16e\n", errorss[i][region_count-1].rel_med);
    printf("      ]\n");

    
    printf("    },\n");
  }

  printf("    \"%s\": {\n", funcs[func_count-1].name);

  printf("      \"abs_max_errors\": [\n");
  for (size_t j=0; j<region_count-1; j++) {
    printf("        %1.16e,\n", errorss[func_count-1][j].abs_max);
  }
  printf("        %1.16e\n", errorss[func_count-1][region_count-1].abs_max);
  printf("      ],\n");

  printf("      \"abs_avg_errors\": [\n");
  for (size_t j=0; j<region_count-1; j++) {
    printf("        %1.16e,\n", errorss[func_count-1][j].abs_avg);
  }
  printf("        %1.16e\n", errorss[func_count-1][region_count-1].abs_avg);
  printf("      ],\n");

  printf("      \"abs_med_errors\": [\n");
  for (size_t j=0; j<region_count-1; j++) {
    printf("        %1.16e,\n", errorss[func_count-1][j].abs_med);
  }
  printf("        %1.16e\n", errorss[func_count-1][region_count-1].abs_med);
  printf("      ],\n");

  printf("      \"rel_max_errors\": [\n");
  for (size_t j=0; j<region_count-1; j++) {
    printf("        %1.16e,\n", errorss[func_count-1][j].rel_max);
  }
  printf("        %1.16e\n", errorss[func_count-1][region_count-1].rel_max);
  printf("      ],\n");

  printf("      \"rel_avg_errors\": [\n");
  for (size_t j=0; j<region_count-1; j++) {
    printf("        %1.16e,\n", errorss[func_count-1][j].rel_avg);
  }
  printf("        %1.16e\n", errorss[func_count-1][region_count-1].rel_avg);
  printf("      ],\n");

  printf("      \"rel_med_errors\": [\n");
  for (size_t j=0; j<region_count-1; j++) {
    printf("        %1.16e,\n", errorss[func_count-1][j].rel_med);
  }
  printf("        %1.16e\n", errorss[func_count-1][region_count-1].rel_med);
  printf("      ]\n");

  printf("    }\n");

  printf("  }\n");

  printf("}\n");
}

