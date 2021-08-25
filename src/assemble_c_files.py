

def assemble_header(decls):
    lines = ["#include <mpfr.h>", ""]
    lines.extend(decls)
    return lines

def assemble_functions(functions, header_fname):
    lines = ["#include \"{}\"".format(header_fname),
             "#include \"table_generation.h\"",
             "#include <assert.h>",
             "#include <math.h>",
             ""]
    for func in functions:
        lines.extend(func)
        lines.append("")
    return lines

def assemble_error_main(mpfr_func, other_funcs, header_fname, domains):
    lines = ["#include \"table_generation.h\"",
             "#include \"xmalloc.h\"",
             "#include \"{}\"".format(header_fname),
             "#include <math.h>",
             "#include <stdlib.h>",
             "#include <stdio.h>",
             "",
             "#define ENTRY_COUNT ({})".format(len(other_funcs)),
             "entry ENTRIES[ENTRY_COUNT] = {"]
    for func in other_funcs:
        lines.append("  {{{}, \"{}\"}},".format(func, func))

    lines.extend(["};",
                  "",
                  "int main(int argc, char** argv)",
                  "{",
                  "  long int choice = 0;",
                  "  if (argc == 2) {",
                  "    choice = strtol(argv[1], NULL, 10);",
                  "  }",
                  "  double low,high;",
                  "  switch (choice) {"])
    for i,(low,high) in enumerate(domains):
        lines.extend(["  case {}:".format(i),
                      "    low = {};".format(low),
                      "    high = {};".format(high),
                      "    break;"])
    lines.extend(["  default:",
                  "    printf(\"Option not available\\n\");"
                  "    exit(1);",
                  "  }",
                  "  size_t region_count = ((size_t) 1) << 10;",
                  "  size_t samples = ((size_t) 1) << 14;",
                  "  double* regions = generate_linear_regions(low, high, region_count);",
                  "  error** errorss = generate_table(region_count, regions, samples,",
                  "                                   {},".format(mpfr_func),
                  "                                   ENTRY_COUNT, ENTRIES);",
                  "  print_json(region_count, regions, ENTRY_COUNT, ENTRIES, errorss);",
                  "  free_table(ENTRY_COUNT, errorss);",
                  "  mpfr_free_cache();",
                  "  return 0;",
                  "}"])
    return lines
