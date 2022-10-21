
#include "table_generation.h"
#include "xmalloc.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>


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


static void
time_function_using_inputs(unop_fp64 f, size_t samples, double *inputs)
{
  // TODO: Yash
}

double*
time_functions(double low, double high,
                       size_t func_count, entry *funcs)
{
  double* function_times = (double*) xmalloc(sizeof(double)*func_count);

  // TODO: Yash

  return function_times;
}

void
print_json(size_t func_count, entry *funcs,
                double *times,
                char *func_name, char *func_body)
{
  // TODO: Yash
}
