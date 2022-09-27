# File Manifest

* __cmd_sollya__: A simple system to call out to the command line version of Sollya to get polynomial approximations to functions.
* __fpcore__: FPCore format parser and many ast niceties (exporters to other languages, integration with python syntax, etc)
* __lambdas__: The typed lambda language used to form implementations.
* __lego_blocks__: The underlying pieces that the lambda language uses to represent the computation and export C code.
* __snake_egg_rules__: EGraph related code
* __utils__: Simple logging, timing, and class modification code.
* __assemble_c_files.py__: Puts together the generated code to be used with the measurement system.
* __error.py__: unused
* __find_identities.py__: Code that attempts to find useful identites of a given function using EGraphs.
* __interval.py__: Barely used interval representation.
* __megalibm_generate.py__: Main script for function generation.
* __megalibm_identities.py__: Main script for function identity discovery.
* __nightly.sh__: Runner for the nightly system.
* __numeric_types.py__: unused
* __synthesize.py__: Code that generates implementations of a given function.
