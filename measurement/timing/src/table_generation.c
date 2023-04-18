
#include "table_generation.h"
#include "xmalloc.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MULT_ROUNDING_FACTOR 1e9

static void
fill_inputs(double low, double high, size_t samples, double *inputs)
{
  double span = high - low;

  for (size_t i = 0; i < samples; i++)
  {
    double dirty_rand = ((double)rand()) / ((double)RAND_MAX);
    inputs[i] = low + span * dirty_rand;
  }
}

static double time_function_using_inputs(void *f, unop_type func_type, size_t samples, double *inputs, size_t iters)
{
  clock_t start, end;
  double cpu_time_used, avg_time_per_sample;

  start = clock();
  for (size_t iter = 0; iter < iters; iter++)
  {
    for (size_t i = 0; i < samples; i++)
    {
      double value;
      switch (func_type){
        case UNOP_FP64:
        {
          unop_fp64 func = (unop_fp64)f;
          value = func(inputs[i]);
          break;
        }
        case UNOP_FP32:
        {
          unop_fp32 func = (unop_fp32)f;
          value = func(inputs[i]);
          break;
        }
        default:
        {
          break;
        }
      }
    }
  }
  end = clock();
  cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
  avg_time_per_sample = (double)(cpu_time_used / (iters * samples) * MULT_ROUNDING_FACTOR);
  return avg_time_per_sample;
}



double *
time_functions(double low, double high,
               size_t func_count, entry *funcs, size_t samples, size_t iters)
{
  double *function_times = (double *)xmalloc(sizeof(double) * func_count);

  double *inputs = (double *)xmalloc(sizeof(double) * samples);
  fill_inputs(low, high, samples, inputs);

  for (size_t fidx = 0; fidx < func_count; fidx++)
  {
    void *f = funcs[fidx].func;
    unop_type func_type = funcs[fidx - 1].func_type;
    function_times[fidx] = time_function_using_inputs(f, func_type, samples, inputs, iters);
  }

  xfree(inputs);

  return function_times;
}

void free_memory(double *function_times)
{
  assert(function_times != NULL);
  xfree(function_times);
}

void print_json(size_t func_count, entry *funcs,
                double *times,
                char *func_name, char *func_body)
{
  printf("{\n");

  // Name and body
  printf("  \"name\": \"%s\",\n", func_name);
  printf("  \"body\": \"%s\",\n", func_body);

  // Dict from function name to a timing
  printf("  \"functions\": {\n");
  for (size_t i = 0; i < func_count; i++)
  {
    printf("    \"%s\": {\n", funcs[i].name);
    printf("      \"avg_time_per_sample\": %1.8e", times[i]);
    printf("\n    }");
    if (i != func_count - 1)
    {
      printf(",");
    }
    printf("\n");
  }
  printf("  }\n");
  printf("}\n");
}
