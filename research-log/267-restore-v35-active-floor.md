# Restore retained v35 active floor

Date: 2026-08-03

## Reason

After v37 completed with public score `84.735`, the measured dense replacement branch was refuted. Leaving it active by default would make future submissions start from a discarded configuration.

The active attack path is restored to the retained v35-style public-control validation-fill floor:

- single user message per candidate;
- one `http.post`;
- one URL;
- live keep-only-if-fired fill;
- refuted dense branches removed from active source and notebooks.

This is not a new leaderboard claim. It is a control restore before opening a fresh above-100 mechanism.

## Changes

- Removed the measured dense replacement branch from `experiments/attack.py`.
- Restored the attack docstring and class description to the public-control validation-fill control.
- Rebuilt all notebook copies with `submission/build_notebook.py`.

## Verification

Compilation and notebook rebuild:

```text
comp/.venv/bin/python -m py_compile experiments/attack.py submission/build_notebook.py
comp/.venv/bin/python submission/build_notebook.py
```

returned:

```text
wrote /home/soh/agent-security/ai-agent-security-attack.ipynb (16026 bytes)
wrote /home/soh/agent-security/submission/kaggle_notebook.ipynb (16026 bytes)
wrote /home/soh/agent-security/submission/kernel/kaggle_notebook.ipynb (16026 bytes)
attack.py parses OK
```

Dense-marker absence:

```text
rg -n "MEASURED_DENSE|DENSE_ENABLED|_dense_msg|_measured_dense|Measured dense replacement" experiments/attack.py ai-agent-security-attack.ipynb submission/kaggle_notebook.ipynb submission/kernel/kaggle_notebook.ipynb || true
```

returned no matches.

Notebook contract markers:

```text
rg -n "Public-control validation-fill|Single-hop SECRET_MARKER|JEDAttackInferenceServer\\(\\)\\.serve\\(\\)|Id,Score" experiments/attack.py ai-agent-security-attack.ipynb submission/kaggle_notebook.ipynb submission/kernel/kaggle_notebook.ipynb submission/build_notebook.py
```

returned the public-control docstring, single-hop class description, placeholder `Id,Score`, and direct `JEDAttackInferenceServer().serve()` markers.

None-env serialization smoke:

```text
PYTHONPATH=comp/sdk:experiments comp/.venv/bin/python <none-env smoke>
```

returned:

```text
override_count 5
messages_per_candidate 1
max_http_post_mentions 1
max_url_mentions 1
empty_messages 0
```

Fake-live fill smoke:

```text
PYTHONPATH=comp/sdk:experiments comp/.venv/bin/python <fake-live fill smoke>
```

returned:

```text
fake_live_count 7
env_calls 8
max_http_post_mentions 1
max_url_mentions 1
has_dense_wording False
```

## Decision

The repository's active attack path is again the retained v35 floor. Do not submit this restore as a new claim unless a later confidence checklist explicitly selects it. Use it as the fallback/control for the next above-100 mechanism.
