

def assemble_header(decls):
    lines = ["#include <mpfr.h>", ""]
    lines.extend(decls)
    return lines


def assemble_functions(functions, header_fname):
    lines = ["#include \"{}\"".format(header_fname),
             "#include \"table_generation.h\"",
             "#include \"cody_waite_reduction.h\"",
             "#include <assert.h>",
             "#include <math.h>",
             ""]
    for func in functions:
        lines.extend(func)
        lines.append("")
    return lines


def assemble_error_main(func_name, func_body, mpfr_func, other_funcs,
                        generators, header_fname, domains, func_type="UNOP_FP64"):
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
        lines.append("  {{{}, \"{}\", {}}},".format(func, func, func_type))

    lines.extend([
        "};",
        "",
        "#define GENERATOR_COUNT ({})".format(len(generators)),
        "char* GENERATORS[GENERATOR_COUNT] = {"
    ])
    for gen in generators:
        lines.append("     \"{}\",".format(gen))

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
    for i, (low, high) in enumerate(domains):
        lines.extend(["  case {}:".format(i),
                      "    low = {};".format(low),
                      "    high = {};".format(high),
                      "    break;"])
    func_body = func_body.replace("\n", "\\\\n").replace('"', '\\\\\\"')
    lines.extend([
        "  default:",
        "    printf(\"Option not available\\n\");"
        "    exit(1);",
        "  }",
        "  size_t region_count = ((size_t) 1) << 8;",
        "  size_t samples = ((size_t) 1) << 12;",
        "  double* regions = generate_linear_regions(low, high, region_count);",
        "  error** errorss = generate_table(region_count, regions, samples,",
        "                                   {},".format(mpfr_func),
        "                                   ENTRY_COUNT, ENTRIES);",
        "  print_json(\"{}\",".format(func_name),
        "             \"{}\",".format(func_body),
        "             GENERATOR_COUNT, GENERATORS,",
        "             region_count, regions,",
        "             ENTRY_COUNT, ENTRIES,",
        "             errorss);",
        "  free_table(ENTRY_COUNT, errorss);",
        "  mpfr_free_cache();",
        "  return 0;",
        "}"])
    return lines

def assemble_timing_main(func_name, func_body, other_funcs, header_fname, domains):
    lines = ["#include \"table_generation.h\"",
             "#include \"xmalloc.h\"",
             "#include \"{}\"".format(header_fname),
             "#include <math.h>",
             "#include <stdlib.h>",
             "#include <stdio.h>",
             '#include <time.h>',
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
    for i, (low, high) in enumerate(domains):
        lines.extend(["  case {}:".format(i),
                      "    low = {};".format(low),
                      "    high = {};".format(high),
                      "    break;"])
    func_body = func_body.replace("\n", "\\\\n").replace('"', '\\\\\\"')
    lines.extend([
        "  default:",
        "    printf(\"Option not available\\n\");"
        "    exit(1);",
        "  }",
        "  size_t samples = ((size_t) 1) << 12;",
        "  size_t iters = 10000;",
        "  double* timings = time_functions(low, high, ENTRY_COUNT, ENTRIES, samples, iters);",
        "  print_json(ENTRY_COUNT, ENTRIES, timings, \"{}\", \"{}\");".format(
            func_name, func_body),
        "  free_memory(timings);" ,
        "  mpfr_free_cache();",
        "  return 0;",
        "}"])
    return lines