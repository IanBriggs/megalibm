
#include "table_generation.h"
#include "xmalloc.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static mpfr_t scratch;

static int
qsort_cmp(const void *va, const void *vb)
{
  const double a = *(const double *)va;
  const double b = *(const double *)vb;

  assert(isfinite(a));
  assert(isfinite(b));

  if (a > b)
  {
    return 1;
  }
  if (a < b)
  {
    return -1;
  }
  return 0;
}

static void
fill_inputs(double low, double high, size_t samples, double *inputs)
{
  double span = high - low;

  for (size_t i = 0; i < samples; i++)
  {
    double dirty_rand = ((double)rand()) / ((double)RAND_MAX);
    inputs[i] = low + span * dirty_rand;
  }

  qsort(inputs, samples, sizeof(double), qsort_cmp);
}

static void
compare(mpfr_t expected, double actual, double *absolute, double *relative)
{
  mpfr_d_sub(scratch, actual, expected, MPFR_RNDN);
  *absolute = fabs(mpfr_get_d(scratch, MPFR_RNDN));

  mpfr_div(scratch, scratch, expected, MPFR_RNDN);
  *relative = fabs(mpfr_get_d(scratch, MPFR_RNDN));
}

static void
reference_on_region(size_t samples, mpfr_t *reals,
                    double *values, double *absolutes, double *relatives,
                    error *ferror)
{
  for (size_t i = 0; i < samples; i++)
  {
    double actual = mpfr_get_d(reals[i], MPFR_RNDN);
    compare(reals[i], actual, &absolutes[i], &relatives[i]);
    values[i] = actual;
  }

  qsort(values, samples, sizeof(double), qsort_cmp);
  qsort(absolutes, samples, sizeof(double), qsort_cmp);
  qsort(relatives, samples, sizeof(double), qsort_cmp);

  double val_sum = 0.0;
  double abs_sum = 0.0;
  double rel_sum = 0.0;
  for (size_t i = 0; i < samples; i++)
  {
    val_sum += values[i];
    abs_sum += absolutes[i];
    rel_sum += relatives[i];
  }

  ferror->val_max = values[samples - 1];
  ferror->val_avg = val_sum / ((double)samples);
  ferror->val_min = values[0];

  ferror->abs_max = absolutes[samples - 1];
  ferror->abs_avg = abs_sum / ((double)samples);
  ferror->abs_med = absolutes[((size_t)samples / 2)];

  ferror->rel_max = relatives[samples - 1];
  ferror->rel_avg = rel_sum / ((double)samples);
  ferror->rel_med = relatives[((size_t)samples / 2)];
}

static void
run_on_region(unop_fp64 f, size_t samples, double *inputs, mpfr_t *reals,
              double *values, double *absolutes, double *relatives,
              error *ferror)
{
  for (size_t i = 0; i < samples; i++)
  {
    double actual = f(inputs[i]);
    compare(reals[i], actual, &absolutes[i], &relatives[i]);
    values[i] = actual;
  }

  qsort(values, samples, sizeof(double), qsort_cmp);
  qsort(absolutes, samples, sizeof(double), qsort_cmp);
  qsort(relatives, samples, sizeof(double), qsort_cmp);

  double val_sum = 0.0;
  double abs_sum = 0.0;
  double rel_sum = 0.0;
  for (size_t i = 0; i < samples; i++)
  {
    val_sum += values[i];
    abs_sum += absolutes[i];
    rel_sum += relatives[i];
  }

  ferror->val_max = values[samples - 1];
  ferror->val_avg = val_sum / ((double)samples);
  ferror->val_min = values[0];

  ferror->abs_max = absolutes[samples - 1];
  ferror->abs_avg = abs_sum / ((double)samples);
  ferror->abs_med = absolutes[((size_t)samples / 2)];

  ferror->rel_max = relatives[samples - 1];
  ferror->rel_avg = rel_sum / ((double)samples);
  ferror->rel_med = relatives[((size_t)samples / 2)];
}

double *
generate_linear_regions(double low, double high, size_t region_count)
{
  assert(finite(low));
  assert(finite(high));
  assert(low < high);
  assert(region_count > 0);

  double *retval = (double *)xmalloc(sizeof(double) * (region_count + 1));

  double step = (high - low) / ((double)region_count);
  for (size_t i = 0; i < region_count; i++)
  {
    retval[i] = low + ((double)i) * step;
  }
  retval[region_count] = high;

  return retval;
}

void free_regions(double *regions)
{
  assert(regions != NULL);

  xfree(regions);
}

error **
generate_table(size_t region_count, double *regions, size_t samples,
               unop_mpfr oracle,
               size_t func_count, entry *funcs)
{
  assert(region_count > 0);
  assert(regions != NULL);
  assert(samples > 0);
  assert(oracle != NULL);
  assert(func_count > 0);
  assert(funcs != NULL);

  error **errorss = (error **)xmalloc(sizeof(error *) * (func_count + 1));
  for (size_t i = 0; i <= func_count; i++)
  {
    errorss[i] = (error *)xmalloc(sizeof(error) * region_count);
  }

  mpfr_init2(scratch, ORACLE_PREC);

  mpfr_t *reals = (mpfr_t *)xmalloc(sizeof(mpfr_t) * samples);
  for (size_t i = 0; i < samples; i++)
  {
    mpfr_init2(reals[i], ORACLE_PREC);
  }

  double *inputs = (double *)xmalloc(sizeof(double) * samples);
  double *values = (double *)xmalloc(sizeof(double) * samples);
  double *absolutes = (double *)xmalloc(sizeof(double) * samples);
  double *relatives = (double *)xmalloc(sizeof(double) * samples);

  for (size_t region = 0; region < region_count; region++)
  {
    fill_inputs(regions[region], regions[region + 1], samples, inputs);
    for (size_t i = 0; i < samples; i++)
    {
      oracle(reals[i], inputs[i]);
    }

    reference_on_region(samples, reals, values, absolutes, relatives,
                        &errorss[0][region]);

    for (size_t fidx = 1; fidx <= func_count; fidx++)
    {
      unop_fp64 f = funcs[fidx - 1].func;
      error *ferror = &errorss[fidx][region];
      run_on_region(f, samples, inputs, reals, values, absolutes, relatives,
                    ferror);
    }
  }

  xfree(relatives);
  xfree(absolutes);
  xfree(values);
  xfree(inputs);

  for (size_t i = 0; i < samples; i++)
  {
    mpfr_clear(reals[i]);
  }

  xfree(reals);

  mpfr_clear(scratch);

  return errorss;
}

void free_table(size_t func_count, error **errorss)
{
  assert(errorss != NULL);

  for (size_t i = 0; i < func_count; i++)
  {
    assert(errorss[i] != NULL);
    xfree(errorss[i]);
    errorss[i] = NULL;
  }

  xfree(errorss);
}

void print_json(size_t region_count, double *regions,
                size_t func_count, entry *funcs,
                error **errorss,
                char *func_name, char *func_body)
{
  // Due to how picky JSON is with commas everything here has the form:
  //  for thing in things[:-1]:
  //    output thing + ,
  //  output things[-1]

  printf("{\n");

  // Name and body
  printf("  \"name\": \"%s\",\n", func_name);
  printf("  \"body\": \"%s\",\n", func_body);

  // First a list of fenceposts for the region under test
  printf("  \"regions\": [\n");
  for (size_t i = 0; i < region_count; i++)
  {
    printf("    %1.16e,\n", regions[i]);
  }
  printf("    %1.16e\n", regions[region_count]);
  printf("  ],\n");

  // Then a dict from function name to a dict from
  printf("  \"functions\": {\n");
  for (size_t i = 0; i < func_count; i++)
  {
    // The zero-th dataset is the reference (mpfr) values, others are named
    if (i == 0)
    {
      printf("    \"reference\": {\n");
    }
    else
    {
      printf("    \"%s\": {\n", funcs[i - 1].name);
    }

    // First the maximum value seen per region
    printf("      \"max_value\": [\n");
    for (size_t j = 0; j < region_count - 1; j++)
    {
      printf("        %1.16e,\n", errorss[i][j].val_max);
    }
    printf("        %1.16e\n", errorss[i][region_count - 1].val_max);
    printf("      ],\n");

    // Then the average value
    printf("      \"avg_value\": [\n");
    for (size_t j = 0; j < region_count - 1; j++)
    {
      printf("        %1.16e,\n", errorss[i][j].val_avg);
    }
    printf("        %1.16e\n", errorss[i][region_count - 1].val_avg);
    printf("      ],\n");

    // Then the min vlue
    printf("      \"min_value\": [\n");
    for (size_t j = 0; j < region_count - 1; j++)
    {
      printf("        %1.16e,\n", errorss[i][j].val_min);
    }
    printf("        %1.16e\n", errorss[i][region_count - 1].val_min);
    printf("      ],\n");

    // Then the maximum of the absolute error
    printf("      \"abs_max_errors\": [\n");
    for (size_t j = 0; j < region_count - 1; j++)
    {
      printf("        %1.16e,\n", errorss[i][j].abs_max);
    }
    printf("        %1.16e\n", errorss[i][region_count - 1].abs_max);
    printf("      ],\n");

    // Then the average of the absolute error
    printf("      \"abs_avg_errors\": [\n");
    for (size_t j = 0; j < region_count - 1; j++)
    {
      printf("        %1.16e,\n", errorss[i][j].abs_avg);
    }
    printf("        %1.16e\n", errorss[i][region_count - 1].abs_avg);
    printf("      ],\n");

    // Then the median of the absolute error
    printf("      \"abs_med_errors\": [\n");
    for (size_t j = 0; j < region_count - 1; j++)
    {
      printf("        %1.16e,\n", errorss[i][j].abs_med);
    }
    printf("        %1.16e\n", errorss[i][region_count - 1].abs_med);
    printf("      ],\n");

    // Then the maximum of the relative error
    printf("      \"rel_max_errors\": [\n");
    for (size_t j = 0; j < region_count - 1; j++)
    {
      printf("        %1.16e,\n", errorss[i][j].rel_max);
    }
    printf("        %1.16e\n", errorss[i][region_count - 1].rel_max);
    printf("      ],\n");

    // Then the average of the relative error
    printf("      \"rel_avg_errors\": [\n");
    for (size_t j = 0; j < region_count - 1; j++)
    {
      printf("        %1.16e,\n", errorss[i][j].rel_avg);
    }
    printf("        %1.16e\n", errorss[i][region_count - 1].rel_avg);
    printf("      ],\n");

    // Then the median of the relative error
    printf("      \"rel_med_errors\": [\n");
    for (size_t j = 0; j < region_count - 1; j++)
    {
      printf("        %1.16e,\n", errorss[i][j].rel_med);
    }
    printf("        %1.16e\n", errorss[i][region_count - 1].rel_med);
    printf("      ]\n");

    printf("    },\n");
  }

  printf("    \"%s\": {\n", funcs[func_count - 1].name);

  printf("      \"max_value\": [\n");
  for (size_t j = 0; j < region_count - 1; j++)
  {
    printf("        %1.16e,\n", errorss[func_count][j].val_max);
  }
  printf("        %1.16e\n", errorss[func_count][region_count - 1].val_max);
  printf("      ],\n");

  printf("      \"avg_value\": [\n");
  for (size_t j = 0; j < region_count - 1; j++)
  {
    printf("        %1.16e,\n", errorss[func_count][j].val_avg);
  }
  printf("        %1.16e\n", errorss[func_count][region_count - 1].val_avg);
  printf("      ],\n");

  printf("      \"min_value\": [\n");
  for (size_t j = 0; j < region_count - 1; j++)
  {
    printf("        %1.16e,\n", errorss[func_count][j].val_min);
  }
  printf("        %1.16e\n", errorss[func_count][region_count - 1].val_min);
  printf("      ],\n");

  printf("      \"abs_max_errors\": [\n");
  for (size_t j = 0; j < region_count - 1; j++)
  {
    printf("        %1.16e,\n", errorss[func_count][j].abs_max);
  }
  printf("        %1.16e\n", errorss[func_count][region_count - 1].abs_max);
  printf("      ],\n");

  printf("      \"abs_avg_errors\": [\n");
  for (size_t j = 0; j < region_count - 1; j++)
  {
    printf("        %1.16e,\n", errorss[func_count][j].abs_avg);
  }
  printf("        %1.16e\n", errorss[func_count][region_count - 1].abs_avg);
  printf("      ],\n");

  printf("      \"abs_med_errors\": [\n");
  for (size_t j = 0; j < region_count - 1; j++)
  {
    printf("        %1.16e,\n", errorss[func_count][j].abs_med);
  }
  printf("        %1.16e\n", errorss[func_count][region_count - 1].abs_med);
  printf("      ],\n");

  printf("      \"rel_max_errors\": [\n");
  for (size_t j = 0; j < region_count - 1; j++)
  {
    printf("        %1.16e,\n", errorss[func_count][j].rel_max);
  }
  printf("        %1.16e\n", errorss[func_count][region_count - 1].rel_max);
  printf("      ],\n");

  printf("      \"rel_avg_errors\": [\n");
  for (size_t j = 0; j < region_count - 1; j++)
  {
    printf("        %1.16e,\n", errorss[func_count][j].rel_avg);
  }
  printf("        %1.16e\n", errorss[func_count][region_count - 1].rel_avg);
  printf("      ],\n");

  printf("      \"rel_med_errors\": [\n");
  for (size_t j = 0; j < region_count - 1; j++)
  {
    printf("        %1.16e,\n", errorss[func_count][j].rel_med);
  }
  printf("        %1.16e\n", errorss[func_count][region_count - 1].rel_med);
  printf("      ]\n");

  printf("    }\n");

  printf("  }\n");

  printf("}\n");
}
