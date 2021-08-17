
#include "table_generation.h"
#include "versin.h"
#include "xmalloc.h"

#include <math.h>
#include <stdlib.h>

#define ENTRY_COUNT (2)

entry ENTRIES[ENTRY_COUNT] = {
  {libm_versin, "libm_versin"},
  {my_versin_26, "my_versin_26"},
};


int main(int argc, char** argv)
{
  long int choice = 0;
  if (argc == 2) {
    choice = strtol(argv[1], NULL, 10);
  }

  double low, high;
  switch (choice) {
  case 0:
    low = -M_PI/8;
    high = M_PI/8;
    break;

  case 1:
    low = -M_PI/4;
    high = M_PI/4;
    break;

  case 2:
    low = -M_PI/2;
    high = M_PI/2;
    break;

  case 3:
    low = -M_PI;
    high = M_PI;
    break;

  case 4:
    low = -20*M_PI;
    high = 20*M_PI;
    break;

  case 5:
    low = -200*M_PI;
    high = 200*M_PI;
    break;

  default:
    exit(1);
  }

  size_t region_count = ((size_t) 1) << 10;
  size_t samples = ((size_t) 1) << 14;
  double* regions = generate_linear_regions(low, high, region_count);
  error** errorss = generate_table(region_count, regions, samples,
                                   oracle_versin,
                                   ENTRY_COUNT, ENTRIES);
  print_json(region_count, regions, ENTRY_COUNT, ENTRIES, errorss);
  free_table(ENTRY_COUNT, errorss);
  mpfr_free_cache();
}
