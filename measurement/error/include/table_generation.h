#ifndef TABLE_GENERATION_H
#define TABLE_GENERATION_H

#include <mpfr.h>
#include <stdint.h>

#define ORACLE_PREC ((mpfr_prec_t)512)

typedef double (*unop_fp64)(double);

typedef int (*unop_mpfr)(mpfr_t, double);

typedef struct
{
  unop_fp64 func;
  char *name;
} entry;

typedef struct
{
  double val_max;
  double val_avg;
  double val_min;
  double abs_max;
  double abs_avg;
  double abs_med;
  double rel_max;
  double rel_avg;
  double rel_med;
} error;

double *generate_linear_regions(double low, double high, size_t regions);

void free_regions(double *regions);

error **generate_table(size_t region_count, double *regions, size_t samples,
                       unop_mpfr oracle,
                       size_t func_count, entry *funcs);

void free_table(size_t func_count, error **errorss);

void print_json(char* func_name,
                char* func_body,
                size_t generator_count, char** generators,
                size_t region_count, double *regions,
                size_t func_count, entry *funcs,
                error **errorss);


#endif
