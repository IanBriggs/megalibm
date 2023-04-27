#ifndef TABLE_GENERATION_H
#define TABLE_GENERATION_H

#include <stddef.h>
#include <stdint.h>

#define ORACLE_PREC ((mpfr_prec_t)512)

typedef double (*unop_fp64)(double);

typedef float (*unop_fp32)(float);

typedef enum {
  UNOP_FP64,
  UNOP_FP32
} unop_type;


typedef struct
{
  void *func;
  char *name;
  unop_type func_type;
} entry;

// Returns how long it takes to run each function on the domain
double *time_functions(double low, double high,
                       size_t func_count, entry *funcs, size_t samples, size_t iters);

void print_json(size_t func_count, entry *funcs,
                double *times,
                char *func_name, char *func_body);

void free_memory(double *timings);

#endif
