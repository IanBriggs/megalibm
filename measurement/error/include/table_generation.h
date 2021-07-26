#ifndef TABLE_GENERATION_H
#define TABLE_GENERATION_H

#include "oracle_functions.h"

typedef double(*unop_fp64)(double);

typedef struct {
  unop_fp64 func;
  char* name;
} entry;


void generate_table(double low, double high, double step,
                    oracle_func F, char* F_name, int len, entry* fs);

#endif
