# Capped Measured Dense Replacement PoC notes

Implemented the Phase-3 local PoC as a self-contained harness under
`experiments/poc/`. It imports the frozen attack message helpers without editing
`experiments/attack.py`, builds local sandbox environments through
`build_attack_env(..., env_selection=EnvSelection.SANDBOX, guardrail=OptimalGuardrail())`,
and uses local mock agents only.

The positive fixture retains only exact four-endpoint dense candidates that
produce at least four observed local exfiltration events. The no-fire fixture
uses the same measured-retention path and then falls back to a v35-style
single-post, one-URL candidate when dense retention is below the frozen
minimum. The capped-unmeasured comparator emits the same capped dense stack
without candidate-level measurement, demonstrating the no-fire control
difference.

The score-rate-stop ablation is deliberately a deterministic pure-controller
case: dense firing is held fixed at four events while local elapsed times make
the dense score-rate fail the enabled stop but pass when the stop is disabled.
This isolates admission logic without using a slow target model.

This PoC validates local implementation mechanics only. It is not Kaggle
evidence, target-model dense prevalence evidence, replay-safety evidence, or
authorization to change active attack code.
