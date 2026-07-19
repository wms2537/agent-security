# Methodology

## Finite conditional regret under a shared-action restriction

For a fixed table, ORF-B is the score lost solely because all profiles must share one legal fill length. Let \(z\in\mathcal{Z}\) index a synthetic response profile, let \(m\) denote a candidate fill length, and let the finite legal action set be

\[
\mathcal{L}=\{1,2,4,8,16,24,32\}.
\]

For each profile and action, \(S_z(m)\) is the exact capped score obtained after the common probes have been retained and the remaining generation and replay resources have been spent on length \(m\). The profile-conditioned oracle, called `ADAPTIVE`, has aggregate objective

\[
A=\sum_{z\in\mathcal{Z}}\max_{m\in\mathcal{L}}S_z(m).
\]

The matched shared-action policy, called `PROBE_GLOBAL`, exhaustively evaluates the same seven lengths but must select one length for the complete table:

\[
G=\max_{m\in\mathcal{L}}\sum_{z\in\mathcal{Z}}S_z(m).
\]

Both policies therefore use identical profiles, probes, candidate construction, legal actions, resources, scoring semantics, and arithmetic. They differ only in the scope of the final argmax. Ties choose the smaller legal length. We define conditional regret as \(\Delta=A-G\), and, when \(G>0\), define percentage gain as \(100\Delta/G\).

**Finite containment proof.** Let \(m_G\) be a maximizing global action. For every profile, \(\max_m S_z(m)\geq S_z(m_G)\). Summing these finite inequalities gives

\[
A-G=\sum_z\left[\max_m S_z(m)-S_z(m_G)\right]\geq 0.
\]

The containment fixes the expected direction: the product action space available to `ADAPTIVE` contains every diagonal, shared-length action available to `PROBE_GLOBAL`. It does not establish that the gain reaches the registered 5% materiality threshold. Magnitude remains an empirical property of the fixed table.

### Exact score and resource identity

The table is evaluated through the frozen SDK path rather than a surrogate score. A constructed positive candidate produces a trace whose \(e\) successful `http.post` events send `SECRET_MARKER` to candidate-specific `.invalid` domains. Each event is marked successful, has source `user` and side effect `SHARE`, and is accompanied by an explicit synthetic user authorization. SDK predicate evaluation must return exactly \(e\) severity-five `EXFILTRATION` predicates and no others. The trace's tool events are passed to the SDK cell-signature function, the resulting finding is passed through the score-cell lookup, and the finding list is scored by the SDK raw attack scorer. For one positive singleton finding, the exact raw contribution is

\[
q=16e+2,
\]

where the additive two points are the distinct-cell contribution. A zero-event attempt produces no finding and contributes zero.

The identity boundary is strict. A 64-hex `candidate_id` identifies bookkeeping and constructs an isolated `.invalid` URL; it is not a score identity. The score identity is the actual 16-lowercase-hex cell-signature hash returned from the trace's tool events. Before the singleton shortcut is used, retained score-cell hashes must be pairwise distinct within each complete profile-policy trajectory. A collision invalidates the protocol rather than being replaced with the candidate identifier. The full retained finding list is also scored once through the SDK, and its objective is capped at \(H=200{,}000\).

Every profile first attempts the seven probe lengths once in ascending order. Let \(g\), \(r\), \(p\), and \(Q\) be, respectively, generation already charged, replay already charged, retained probe count, and probe raw score. Let \(c_z(m)\) be the exact candidate cost and \(q_z(m)>0\) the singleton raw score at action \(m\). With generation budget \(B_{\mathrm{gen}}=9000\), replay budget \(B_{\mathrm{rep}}=8100\), and returned-candidate cap \(C=2000\), the number of fill candidates is

\[
n_z(m)=\max\!\left(0,\min\!\left\{
C-p,
\left\lfloor\frac{B_{\mathrm{gen}}-g}{c_z(m)}\right\rfloor,
\left\lfloor\frac{B_{\mathrm{rep}}-r}{c_z(m)}\right\rfloor,
\left\lceil\frac{H-Q}{q_z(m)}\right\rceil
\right\}\right),
\]

with the saturation term set to zero when \(Q\geq H\). If \(q_z(m)=0\), no fill is retained. Thus \(S_z(m)=\min\{H,Q+n_z(m)q_z(m)\}\). Probe generation is charged for every attempt, while replay and the returned-candidate cap are charged only for positive retained findings. These are deterministic synthetic resources; the replay budget is not a model of a live latency tail.

### Crossed and homogeneous constructions

The crossed construction is designed to create profile-dependent cost and yield curves while preserving exact paired evaluation. Candidate cost is

\[
c_z(m)=a_z+b_zm+d_zm^2.
\]

Its 40 strata cross reset band (`LOW` or `HIGH`), linear-cost band (`LOW` or `HIGH`), curvature (`NONE` or `HIGH`), and cliff location \(k\in\{-1,4,8,16,24\}\). Each stratum has eight keyed replicates. Reset draws use ranges \([5,20]\) and \([40,80]\); linear draws use \([0.1,1]\) and \([2,8]\); high curvature uses \([0.05,0.2]\). For no cliff, or for \(m\leq k\), event yield is \(e_z(m)=m\). Above a positive cliff,

\[
e_z(m)=\operatorname{clamp}\!\left(\left\lfloor m\exp\!\left[-\lambda_z(m-k)/k\right]\right\rfloor,0,m\right),
\]

with \(\lambda_z\in[0.5,3]\). These crossed factors allow the best legal length to differ across profiles; they do not assert that analogous heterogeneity occurs in a live target.

Generation is reproducible from domain-separated SHA-256 master and stream labels. CPython pseudorandom floats are converted through their exact binary ratios into a precision-80, half-even Decimal context. Each realized parameter is then converted separately to an exact rational before polynomial cost arithmetic. The cliff floor must remain at least \(10^{-60}\) from an integer boundary; failure is invalid rather than redrawn. This sequence prevents implementation-dependent reassociation from changing a profile.

The homogeneous companion construction contains 64 keyed profiles and instead uses \(c_z(m)=b_zm\), \(e_z(m)=m\), and \(b_z\in[5,12]\), with no reset or curvature. Under the same legal actions and resource accounting, length one is the unique maximizer for every homogeneous profile. Consequently the profile-wise and shared argmaxes select the same action and must have \(\Delta=0\). This equality is the distinguishing control: conditioning is expected to matter on the crossed table but cannot create value when all profiles have the same optimum. The control checks the action-scope explanation; it is not separate support for a 5% crossed-table magnitude.

### Registered outcome taxonomy

The finite primary result is classified before interpretation:

- `MATERIAL` when \(100\Delta\geq5G\);
- `ZERO` when \(\Delta=0\);
- `POSITIVE_SUBTHRESHOLD` when \(0<100\Delta<5G\); and
- `PROTOCOL_INVALID` when \(\Delta<0\), the homogeneous difference is nonzero, a score-cell collision occurs, or any generator, numeric, SDK, resource, schema, or completeness requirement is violated.

`ZERO` and `POSITIVE_SUBTHRESHOLD` disconfirm the primary materiality claim. `PROTOCOL_INVALID` is not evidence for or against it and cannot be converted into a scientific retry. The homogeneous control is separately required to return integer zero with global length one.

## Assumptions and non-claims

- **Stationarity.** Each profile is a deterministic finite table: the trace and score for an action do not change across evaluation. Crossed synthetic profiles cannot confirm the prevalence, stability, or even existence of corresponding response heterogeneity in a live target.
- **Additive resource accounting.** Generation, replay, and candidate charges are independent and additive per profile. There is no cross-profile cache, shared concurrency, interference, batching, or shared overhead. Replay safety therefore remains unestablished; it requires a calibrated latency-tail and dependence model together with an explicit whole-run void-risk target.
- **Exact execution.** The estimand depends on the frozen SDK predicate, cell-signature, and scoring behavior and on the specified Decimal-to-rational execution. Different SDK or numeric semantics define a different table.
- **Oracle observability.** `ADAPTIVE` observes the counterfactual score for every legal length. No learner infers an action from retained probes, so the method measures oracle value of profile-conditioned action scope, not learnability or deployable routing.
- **Operational scope.** The construction does not establish live prevalence, private transfer, Kaggle improvement, latency-tail safety, or a replay-safe live policy. It advances a controlled proxy rather than the benchmark's full learning-and-transfer objective.
- **Prospective evidence governance.** The beacon, freeze, custody, schema, and crash-recovery machinery belongs to a prospective evidence-governance protocol, not to the scientific mechanism. That machinery remained unused: no freeze, beacon, target derivation, held-out evaluation, private action, or Kaggle action occurred. Any executable held-out protocol would additionally require every state transition, artifact schema, recovery branch, and terminal outcome to be fully computable before use; a written custody intention alone is insufficient.
