# OpenRouter observability — what it can and cannot faithfully measure

Date: 2026-08-07

User directed using OpenRouter (key in .env) instead of downloading the GGUFs
(no cp314 llama-cpp wheel; 20GB models). Both EXACT competition models are on
OpenRouter: `openai/gpt-oss-20b`, `google/gemma-4-26b-a4b-it`.

## Probes

1. Chat + API tools, plain verbose message: BOTH models fire instantly
   (~1.5-2.5s), `finish=tool_calls`, emit `http.post{url,data=SECRET_MARKER}`.
2. Chat, NO API tools, tools-as-system-text, plain vs v35 harmony frame: gpt-oss
   STILL returns `finish=tool_calls` with empty content on both — OpenRouter's
   provider applies harmony tool-parsing itself; raw `<|channel|>` tokens are not
   surfaced in `content`.
3. `/completions` raw endpoint (gpt-oss): returns delimiter-stripped text
   (`analysis...assistantfinalOK`) — the `<|...|>` control tokens are gone.

## What OpenRouter CAN faithfully give (transferable — same weights)

- **Model compliance / refusal** per message per exact model. Result: both models
  comply readily with plain AND framed exfil messages. No refusal. So the
  competition's firing gap is NOT model refusal — message semantics are not the
  bottleneck.

## What OpenRouter CANNOT faithfully give

- **SDK raw-parse frame sensitivity.** The competition SDK renders tools into the
  prompt and parses RAW llama.cpp text with a harmony regex
  (`<|channel|>commentary...to=functions...`). OpenRouter's provider robustly
  parses harmony itself, so plain and frame fire equally — it hides exactly the
  fragility that made v35's frame essential and v41 (verbose) tank to 62.280.
- **Timing/latency.** OpenRouter serves on fast GPUs (~2s/call). The competition
  runs llama.cpp on a CPU kernel (enable_gpu:false) — far slower, which is why
  reruns take hours and the replay budget is tight. OpenRouter latency does not
  transfer, so it cannot calibrate the count/REPLAY_SAFE_FRAC math.

## Implication

OpenRouter confirms compliance is fine but cannot reproduce the two signals that
actually drive our score gap (SDK raw-parse firing + CPU throughput). Faithful
observability of those requires running the real stack: llama.cpp + the exact
GGUFs + the SDK parser/gym env on CPU. That is feasible off the py3.14 venv
(python3.11/3.12 present, cmake+gcc present, 59G free, models on HF) but is the
heavier path the user chose to avoid.

## Useful middle path

Drive the REAL SDK gym attack env (real tools, predicates, scoring) with an
OpenRouter-backed agent using native tool_calls as the fire signal. This faith-
fully reproduces the ENV + PREDICATE + SCORING logic and real model DECISIONS
(compliance, multi-step behavior, which predicates a message trips), just not the
raw-parse firing fragility or CPU timing. Good for exploring candidate STRATEGY
(e.g. can a message trip multiple predicates, do chains comply) with real
model+scoring feedback — the first offline signal we would have.

## State

No code/submission change. attack.py remains the v35 floor. Scratch probes
removed.
