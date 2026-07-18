2026-07-18 | P1-4 | recon + strong baseline | done | compliant norm=100.68, refuse_exfil norm=11.04 (fallback ok), notebook builds
2026-07-18 | P4 | harden: multi-post-8 + 22pct private reserve | done | compliant norm 100.7->198.6, refuse_exfil 11.28; REVIEW.md + MEMO_AUDIT.md written
2026-07-18 | P4 | enrich bank (harmony/authority/sequential multi-post + 2nd CD) + gateway facts | done | compliant 198.6 held, refuse_exfil 11.28; notebook rebuilt
2026-07-18 | P4 | submit setup: T4 accelerator + placeholder submission.csv; docs verified | done | v3 pushed, commit polling; earlier 400s were P100 then missing-output-file
2026-07-18 | P4 | SUBMITTED v3 (ref 54799835) | done | real rerun queued; awaiting 4-cell leaderboard scores
2026-07-18 | P4 | ROOTCAUSE LB=36: 4-cell mean (not 1 cell), multi-post backwards (latency-bound N), 28pct dead budget, gemma≠gpt-oss | done
2026-07-18 | P4 | REBUILD v2: single-post exfil, per-model raw/s selection, verified fill, void-safe 0.90, gemma JSON template | done | mock selection+fill+sizing validated
