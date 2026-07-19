# Abstract

A fixed candidate length spends the same finite generation and replay budgets on
response profiles that may prefer different structures. We study this restriction
with Beacon-Held-Out Conditional Regret (ORF-B), which makes one action-scope
replacement: with identical retained probes, legal actions, resources, and
scores, it replaces one exhaustive global fill-length argmax with profile-wise
oracle argmaxes. On `n=3` fixed public synthetic masters, the profile-conditioned
oracle gained a mean **40.249%** over the exact global comparator, with a
measured-master s.d. of **1.855 percentage points**; `test: none; p: not
applicable`, because these masters form a deterministic finite census rather than
a population sample. Three separately derived homogeneous masters returned exact
zero regret, and both policies selected length one for every homogeneous profile.
In secondary public checks, three disjoint changed-construction masters averaged
**36.394%**, while paired one-at-a-time removals of cliff behavior and reset
overhead produced the largest decreases from the core gain. These results measure
public-synthetic oracle information value for the benchmark-shaped scorer. The
locked test was not run, and no Kaggle action occurred. Accordingly, the result
does not establish a learner, live response heterogeneity or transfer, replay
safety, private transfer, or held-out confirmation.
