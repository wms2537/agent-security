# DBER four-policy profile — pre-execution implementation check

Date: 2026-07-26  
Phase: 2  
Task: T088  
Status: implemented, unexecuted

## Frozen implementation

- controller with behavior-neutral terminal instrumentation:
  `experiments/attack.py`,
  SHA-256 `2fd5a59350a655981ea6b3812bea8855bd776dcfc3e27ee842cb49655403c570`;
- controlled latency fixture:
  `experiments/mock_agents.py`,
  SHA-256 `90293f2b5bb340f06f81858441a67d288c44229ef898ff133844ee00f0eddc06`;
- factorial profile and independent artifact verifier:
  `experiments/dber_factorial_profile.py`,
  SHA-256 `ee2eaac6f426f43df1eeb6d639fe9cd56ed79e489df962c8062e82990fb12906`;
- deterministic pre-execution tests:
  `experiments/test_dber_factorial_profile.py`,
  SHA-256 `a2361de5e349d52ed4c5b75d630d62c48b7fe462a4eba93ed96fed95a4b71d3a`.

The implementation is bound to preregistration report 217
(`e2897108166089ab2d1d0ecd59202fc7bb05b718e8bebbe5933ade91f8297e56`)
and its sole pre-execution parser correction report 218
(`f6bc94d27a1ef3b6ab733d407b362576368f92498caa501ce2b92478d62f8e57`).

## Checks run before scientific execution

Compilation:

```text
python -m py_compile:
  experiments/attack.py
  experiments/mock_agents.py
  experiments/dber_factorial_profile.py
  experiments/test_dber_factorial_profile.py
result: PASS
```

The project virtual environment does not contain `pytest`; that invocation
returned `No module named pytest` and is not counted as a test result. The same
three deterministic test functions were then invoked directly under the project
interpreter:

```text
dber_factorial_tests=PASS tests=3
```

Those tests establish:

1. exact candidate-message identity between the pre-instrumentation attack at
   commit `86a64c1` and the instrumented module under a deterministic clock/env;
2. direct terminal reason `candidate` and zero clamp removals in that fixture;
3. correct inverse decoding on ordinary and `>=900000` `.co` indices;
4. bounded packing admits the positive-marginal cheap item and rejects the
   expensive item.

The machine-readable contract check returned:

```text
dber_factorial_contract=PASS units=12 policies=4 sources=8
```

The contract fixes the exact 12-unit order, four policies, alpha, configs,
preregistration paths, and SHA-256 of attack, mock, harness, tests, replay ops,
scorer, predicates, and cell-signature sources.

`git diff --check` also passes.

## Auditability properties

- generation and fresh replay traces are both retained and hashed;
- each fresh replay constructs its own environment before reset/interactions;
- predicates and both signature types are recomputed from traces;
- official `score_attack_raw` is the only scoring path;
- every candidate has messages, source phase, timings, isolated score, and four
  admission decisions;
- the independent verifier reloads artifacts, checks source contract and unit
  order, recomputes trace hashes/predicates/signatures/raw/cost/overflow, and
  reconciles admissions against each portfolio;
- all frozen prediction failures make a unit invalid and return process status 2.

No profile unit has run. No attack-mechanism admission code, Kaggle push, commit
run, or submission has occurred.
