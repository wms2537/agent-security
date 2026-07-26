# DBER profile preregistration correction — index parser

Date: 2026-07-26  
Phase: 2  
Task: T088  
Status: frozen before any profile contract print or execution

During implementation inspection, before executing the harness, report 217's R1
fixture was found to name the wrong URL representation. It described parsing
`x<index>.example`, while immutable `experiments/attack.py::_url` actually maps:

```text
base_index = 26 * (first_letter - "a") + (second_letter - "a")
suffix = optional decimal suffix, default 0
index = 676 * suffix + base_index
url = http://<two letters><optional suffix>.co
```

The R1 fixture is corrected to parse that existing representation and apply the
already-frozen latency rule:

- decoded index `>= 900000`: `0.002 s` per agent action;
- decoded index `< 900000`, absent, or malformed: `0.020 s` per agent action.

Nothing else changes: the 12-unit population, seeds, budgets, caps, alpha,
policies, source/fresh-replay requirements, predictions, decision rule, and
scope remain exactly as frozen in report 217. This is an input-wiring correction,
not a result-driven adjustment; no profile result exists yet.
