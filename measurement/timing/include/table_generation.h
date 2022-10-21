#ifndef TABLE_GENERATION_H
#define TABLE_GENERATION_H

#include <stddef.h>
#include <stdint.h>

typedef double (*unop_fp64)(double);

typedef struct
{
  unop_fp64 func;
  char *name;
} entry;

// Returns how long it takes to run each function on the domain
double* time_functions(double low, double high,
                       size_t func_count, entry *funcs);

void print_json(size_t func_count, entry *funcs,
                double *times,
                char *func_name, char *func_body);

#endif
