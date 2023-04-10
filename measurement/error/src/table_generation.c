
#include "table_generation.h"
#include "xmalloc.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static mpfr_t scratch;

static void
seperator_comma(size_t i, size_t bound)
{
  assert(i <= bound);

  if (i != bound)
  {
    printf(",");
  }
  printf("\n");
}

typedef double (*field)(error);

static void
print_errors_list(char *name, size_t len, error *errors, field get)
{
  printf("      \"%s\": [\n", name);
  for (size_t i = 0; i < len; i++)
  {
    if (isinf(get(errors[i]))) {
      printf("        1e400");
    } else if (isnan(get(errors[i]))) {
      printf("        \"nan\"");
    } else {
      printf("        %1.16e", get(errors[i]));
    }
    seperator_comma(i, len - 1);
  }
  printf("      ]");
}

static double get_val_max(error e) { return e.val_max; }
static double get_val_avg(error e) { return e.val_avg; }
static double get_val_min(error e) { return e.val_min; }
static double get_abs_max(error e) { return e.abs_max; }
static double get_abs_avg(error e) { return e.abs_avg; }
static double get_abs_med(error e) { return e.abs_med; }
static double get_rel_max(error e) { return e.rel_max; }
static double get_rel_avg(error e) { return e.rel_avg; }
static double get_rel_med(error e) { return e.rel_med; }

static int
qsort_cmp(const void *va, const void *vb)
{
  assert(va != NULL);
  assert(vb != NULL);

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
  assert(isfinite(low));
  assert(isfinite(high));
  assert(low < high);
  assert(samples > 0);
  assert(inputs != NULL);

  double span = high - low;

  for (size_t i = 0; i < samples; i++)
  {
    // TODO: this is a _really_ bad fp rng
    double dirty_rand = ((double)rand()) / ((double)RAND_MAX);
    inputs[i] = low + span * dirty_rand;
  }

  qsort(inputs, samples, sizeof(double), qsort_cmp);
}

static void
compare(mpfr_t expected, double actual, double *absolute, double *relative)
{
  assert(isfinite(actual));
  assert(absolute != NULL);
  assert(relative != NULL);

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
  assert(samples > 0);
  assert(reals != NULL);
  assert(values != NULL);
  assert(absolutes != NULL);
  assert(relatives != NULL);
  assert(ferror != NULL);

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
run_on_region(void *f, unop_type func_type, size_t samples, double *inputs, mpfr_t *reals,
              double *values, double *absolutes, double *relatives,
              error *ferror)
{
  assert(samples > 0);
  assert(inputs != NULL);
  assert(reals != NULL);
  assert(values != NULL);
  assert(absolutes != NULL);
  assert(relatives != NULL);
  assert(ferror != NULL);

  for (size_t i = 0; i < samples; i++)
  {
    double actual;
    switch (func_type){
      case UNOP_FP64:
      {
        unop_fp64 func = (unop_fp64)f;
        actual = func(inputs[i]);
        break;
      }
      case UNOP_FP32:
      {
        unop_fp32 func = (unop_fp32)f;
        actual = func(inputs[i]);
        break;
      }
      default:
      {
        break;
      }
    }
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

    for (size_t func_idx = 1; func_idx <= func_count; func_idx++)
    {
      void *f = funcs[func_idx - 1].func;
      unop_type func_type = funcs[func_idx - 1].func_type;
      error *ferror = &errorss[func_idx][region];
      run_on_region(f, func_type, samples, inputs, reals, values, absolutes, relatives,
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

void print_json(char *func_name,
                char *func_body,
                size_t generator_count, char **generators,
                size_t region_count, double *regions,
                size_t func_count, entry *funcs,
                error **errorss)
{
  assert(func_name != NULL);
  assert(func_body != NULL);
  assert(generator_count > 0);
  assert(generators != NULL);
  assert(region_count > 0);
  assert(regions != NULL);
  assert(func_count > 0);
  assert(funcs != NULL);
  assert(errorss != NULL);

  printf("{\n");

  // Name and body
  printf("  \"name\": \"%s\",\n", func_name);
  printf("  \"body\": \"%s\",\n", func_body);

  // Lambda expressions used to generate the generated funcs
  printf("  \"generators\": [\n");
  for (size_t i = 0; i < generator_count; i++)
  {
    printf("    \"%s\"", generators[i]);
    seperator_comma(i, generator_count - 1);
  }
  printf("  ],\n");

  // A list of fenceposts for the region under test
  printf("  \"regions\": [\n");
  for (size_t i = 0; i < region_count + 1; i++)
  {
    printf("    %1.16e", regions[i]);
    seperator_comma(i, region_count);
  }
  printf("  ],\n");

  // Then a dict from function name to a dict from
  printf("  \"functions\": {\n");
  for (size_t i = 0; i < func_count + 1; i++)
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

    // First the values seen per region
    print_errors_list("max_value", region_count, errorss[i], get_val_max);
    printf(",\n");
    print_errors_list("avg_value", region_count, errorss[i], get_val_avg);
    printf(",\n");
    print_errors_list("min_value", region_count, errorss[i], get_val_min);
    printf(",\n");

    // Then the absolute errors
    print_errors_list("abs_max_errors", region_count, errorss[i], get_abs_max);
    printf(",\n");
    print_errors_list("abs_avg_errors", region_count, errorss[i], get_abs_avg);
    printf(",\n");
    print_errors_list("abs_med_errors", region_count, errorss[i], get_abs_med);
    printf(",\n");

    // Then the relative errors
    print_errors_list("rel_max_errors", region_count, errorss[i], get_rel_max);
    printf(",\n");
    print_errors_list("rel_avg_errors", region_count, errorss[i], get_rel_avg);
    printf(",\n");
    print_errors_list("rel_med_errors", region_count, errorss[i], get_rel_med);
    printf("\n");

    printf("    }");
    seperator_comma(i, func_count);
  }
  printf("  }\n");
  printf("}\n");
}
