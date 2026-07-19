2026-07-18 | P1-4 | recon + strong baseline | done | compliant norm=100.68, refuse_exfil norm=11.04 (fallback ok), notebook builds
2026-07-18 | P4 | harden: multi-post-8 + 22pct private reserve | done | compliant norm 100.7->198.6, refuse_exfil 11.28; REVIEW.md + MEMO_AUDIT.md written
2026-07-18 | P4 | enrich bank (harmony/authority/sequential multi-post + 2nd CD) + gateway facts | done | compliant 198.6 held, refuse_exfil 11.28; notebook rebuilt
2026-07-18 | P4 | submit setup: T4 accelerator + placeholder submission.csv; docs verified | done | v3 pushed, commit polling; earlier 400s were P100 then missing-output-file
2026-07-18 | P4 | SUBMITTED v3 (ref 54799835) | done | real rerun queued; awaiting 4-cell leaderboard scores
2026-07-18 | P4 | ROOTCAUSE LB=36: 4-cell mean (not 1 cell), multi-post backwards (latency-bound N), 28pct dead budget, gemma≠gpt-oss | done
2026-07-18 | P4 | REBUILD v2: single-post exfil, per-model raw/s selection, verified fill, void-safe 0.90, gemma JSON template | done | mock selection+fill+sizing validated
2026-07-18 | P4 | REAL LB v2 = 69.570 (was 36.705, +89%) | done | root-cause fix confirmed; mid-pack, top ~103.67; next=read v2 kernel log for real per-model selection (T002)
2026-07-19 | P4 | ORIENT + close stale T004 private-diversity branch | failed | `rg -n` confirms v1 actual 36.705 vs ~85 predicted and 28% dead reserve; mechanics smoke passed on four mocks
2026-07-19 | P4 | T002 live leaderboard + Kaggle strong-baseline audit | done | v2 telemetry unavailable; leader=105.635; 0.99/direct-cost predicts ~84.2; multi-message amortization is the only credible 2x lever
2026-07-19 | P4 | SELECT T005 replay-safe baseline parity | in_progress | prediction 82-89 real LB; mechanics first, no Kaggle submission without checkpoint
2026-07-19 | P4 | T005 replay-safe baseline parity | done | controlled SDK run 39->47 findings = 1.205x vs predicted 1.210x; expected real band ~84, not enough to lead
2026-07-19 | P4 | SELECT T006 adaptive multi-message amortization | in_progress | predict fixed-overhead mock selects multi, zero-overhead mock falls back; live gate requires >1.10x raw/s and >=75% messages firing
2026-07-19 | P4 | T006 adaptive multi-message amortization | done | negative routes single; fixed-overhead routes multi and exact raw=390; full-context failure falls back with exact raw=54; M24 smoke exact raw=19300
2026-07-19 | P4 | USER CHECKPOINT T007 real Kaggle experiment | open | submission-ready notebook; approve push+submit to measure >=106 lead / >=125 strong / 82-89 fallback / <78 failure
2026-07-19 | P2 | T008 proprietary-moat problem reframing | done | user redirected away from copied recipes; PROBLEM.md now anchors online system identification, constrained chain-length optimization, and a distinguishing-prediction moat
2026-07-19 | P2 | SELECT T009 Online Replay Frontier hypothesis | in_progress | varies=candidate-structure-policy; fixed-M replacement must pass Phase-2 anti-stacking and independent theory review before implementation
2026-07-19 | P2 | T009 theory review round 1 | blocked-no-verdict | reviewer returned `Agent errored: Request blocked.`; logged verbatim, hypothesis remains frozen, final review round dispatched methodology-only
2026-07-19 | P2 | T009 theory-review recovery | blocked-user-checkpoint | review budget 2/2 consumed; no recoverable round-2 verdict; Phase-2 gate remains closed and no experiment is authorized
2026-07-19 | P2 | T009 replacement-review authorization | approved | user replied verbatim “yes, go on” to the proposed one-round extension; hypothesis-review limit 2→3 only
2026-07-19 | P2 | T009 replacement theory review round 3 | in_progress | sterile independent review dispatched against unchanged 232-line hypothesis; review budget now 3/3
2026-07-19 | P2 | T009 replacement theory review round 3 | needs_revision | reviewer verified 232 lines; ORF is salvageable but 8 required fixes remain; review budget 3/3 exhausted and Phase-2 gate stays closed
2026-07-19 | P2 | T009 final scientific re-review authorization | approved | user said verbatim “yes, go on, I approve it”; hypothesis-review limit 3→4 only
2026-07-19 | P2 | T009 superseding ORF hypothesis v2 | ready_review | deterministic verification PASS: picks=[1,32,8,4], mean=69591, +34.05% vs best static, 3.15% oracle regret; no experiment run
