# megalibm

## Getting started

Here are some instructions on how to get started.

### On Mac:
 - Requirements
    * python
    * pip

- Installation
   * Clone the repo `git clone git@github.com:IanBriggs/megalibm.git`
   * Run `make`.
   This will install dependencies like `rust` and [snake-egg](https://github.com/egraphs-good/snake-egg).
   * Install z3: `python3 -m pip install sly z3-solver`

- Running the tool
  - You can run megalibm on any of the fpcores: `python3 bin/script benchmarks/1_argument/BENCHMARK.fpcore`
  - This will produce two html pages: `per_func.html` and `index.html`.
