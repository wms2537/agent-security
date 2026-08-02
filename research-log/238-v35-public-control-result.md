# V35 Public-Control Result

**Date:** 2026-08-02 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 8 · **Status:** completed

## Context

Report 237 restored the public high-score validation-fill single-post control after the guarded two-call rc650 path completed with a blank score. The goal of v35 was recovery: prove the direct runner, GPU metadata, validation-fill kernel, and submitted artifact could still produce a visible target score.

## Content

The public-control submission completed with a visible score:

- Submission ref: `55158967`
- Description: `Public-control validation-fill GPU recovery v35`
- Status: `SubmissionStatus.COMPLETE`
- Public score: `86.670`
- Source SHA: `1e18beda6589f43dbbd2bcc500a876aeb6cef272579894c828bd31289a7aa87e`

This is a valid recovery result, not a format failure. It improves over the previous live incumbent `81.225` by `5.445` public points, but it misses the preregistered public-control expectation of `88.5-89.2`.

The same leaderboard poll showed the current public leader at `112.865`, so the single-post control is not enough for the competition objective. It should remain the fallback floor while the next hypothesis tests multi-event score density in an exact final shape.

## Gate Check

- Submission status evidence: `comp/.venv/bin/kaggle competitions submissions ai-agent-security-multi-step-tool-attacks -v` -> `55158967,submission.csv,2026-08-01 09:25:20.083000,Public-control validation-fill GPU recovery v35,SubmissionStatus.COMPLETE,86.670,`
- Leaderboard state evidence: `comp/.venv/bin/kaggle competitions leaderboard -c ai-agent-security-multi-step-tool-attacks -s` -> `ADARSH REDDY B ... 112.865`
- Source identity evidence: `sha256sum experiments/attack.py` -> `1e18beda6589f43dbbd2bcc500a876aeb6cef272579894c828bd31289a7aa87e  experiments/attack.py`

## Problem alignment

This result restores a visible, source-compliant control floor and shows that exceeding the current leaderboard frontier requires a higher-density candidate structure, not another single-post count sweep.

## Decision

Keep v35 as the live fallback floor. Move the active competition search to an exact single-message multi-event density hypothesis with the v35 fill path preserved as fallback.

## Next Steps

Preregister one narrow Stage B density experiment: a single user message that requests four independent `http.post` calls to four unique destinations, admitted only after exact-shape local mechanics and online probe evidence, otherwise falling back to v35.
