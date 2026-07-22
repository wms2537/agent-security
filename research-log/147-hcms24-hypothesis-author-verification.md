# HCMS-24 hypothesis author verification

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Status:** PASS before independent review

Exact command:

```bash
comp/.venv/bin/python -I experiments/poc/hcms24_phase2_reference_v1.py --config experiments/configs/hcms24-c3-v1.json
```

Output:

```text
hcms24_phase2_author_check_v1=PASS
source_bindings=6
evidence_bindings=7
antecedent_status=FAIL_disclosed
selector_status=retired_zero_value
shared_kernel_methods=4
exact_prefix_coverage=1.000000
contribution_components=2
correctness_controls=2
primary_profiles=3
safety_profiles_excluded=1
williams_orders=4
directed_predecessor_pairs=12
position_balance=1_each
predecessor_balance=1_each
minimum_primary_ratio=1.100000
replay_removal=end_to_end_hcms_scalar
official_score_claim=withheld
attack_unchanged=true
review=not_dispatched
```

Additional static checks:

- config JSON parses;
- checker source compiles without execution;
- competition attack SHA-256 equals the committed incumbent;
- the Phase-3 runner and attempt directory are absent;
- the rejected v6 hypothesis remains unchanged;
- no Kaggle action occurred.

The author check verifies internal consistency and bound antecedent evidence. It
does not substitute for independent theory review or fresh execution.
