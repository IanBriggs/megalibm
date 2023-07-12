# megalibm
This document walks you through generating and interpreting 
Figure 8's graphs and table. 

## Kick the tires
To re-generate plots from Figure 8, you should run 
`./kick-tires.sh`. The script should complete in less than a minute.
From there, you can go to `results/` and open
`pareto.html` in browser, which should display 
a number of plots.
The plots generated compare the performance of 
libm, megalibm using the baseline rules,
and megalibm using the Renumo rules.

The table in Figure 8 was generated manually.
To generate the numbers in the table,
you can then open the files `results/baseline.html` and 
`results/renumo.html` in browser.

To recreate the table, you will click on each 
benchmark name to be taken to a page with new graphs
pertaining to that benchmark. We looked at the graph
of relative error over each domain, and counted the number
of clusters or groupings from each implementation,
which gave rise to the unique implementations. (We found that
the number of unique implementations was constant across domains.)
For the unique identities, we took the list of identities at the 
top of the page, and checked to see which could derive the others
via multiple applications.

## Lite
In the lite version of the artifact, we re-run the results of megalibm
given some pre-generated rules from Renumo. To get started,
run `./lite.sh`. The script should complete in the order of 5-10 minutes.
The script will generate a fresh `renumo_run.html` file,
which will appear in the `results/` folder.
The script will also re-generate the `pareto.html` file,
also found in `results/`.
The script will copy over the baseline results that were pre-generated.

## Full
In the full version of the artifact, we re-run Renumo to get new rules,
collate these rules, and then run Megalibm using the new rules.
The results of the megalibm run will be reflected in `renumo_run.html`,
and the comparison of this with the given baseline will be 
freshly generated and available in `pareto.html`, 
again both located in the `results/` folder.

