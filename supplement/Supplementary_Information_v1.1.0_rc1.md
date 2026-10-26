# Supplementary Information

## Sensitivity of BioEmu Stability Benchmark Estimates to Sequential Geometry and Peptide-ω Screening

Sho Miyazaki

Independent researcher, Tokyo, Japan

26 October 2026 | Version 1.1.0-rc1 | Unpublished revision candidate

This supplement connects methods, sources, computation, results and verification. The historical CSVs and NPZs remain unchanged. Full new replay tables are verification outputs, not replacements for the fixed research data. No new sampling, threshold optimization, uncertainty estimation or statistical test is introduced.

## S1. Source, system mapping and provenance

The official archived benchmark v0.1 metadata, `system_info.csv`, define 154 unique system IDs and the `name_wt` pairing. Boolean `mutant=True` identifies 112 mutants; the other 42 entries are matched baselines. All 112 mutant-to-baseline links resolve to one of the 42 baseline entries, and baselines map to themselves. A baseline can itself be an altered sequence or designed protein. The larger `samples_delta_G.zip` contains additional non-benchmark systems, which are outside this study.

Experimental ΔΔG values come from the official `ddg_exp` column, in kcal/mol with mutant-minus-baseline sign. They are not reconstructed from rounded values in the article. The underlying experiments are credited in the official dataset card to [4]. The reference ΔΔG values and mappings are held fixed at all three stages; no uncertainty-weighting, experimental reinterpretation, or re-extraction from the original experimental dataset is performed. `dg_exp`, `wt_only_reference` and target sample counts are preserved as provenance. The 112-pair secondary analysis does not silently exclude pairs because of a system-level reference-only flag.

**Table S1. Principal sources and roles.** Exact paths, byte sizes, hashes, URLs and acquisition status appear in provenance/source_manifest.csv and verification/input_manifest.json.

| Source | Version / identity | Use |
| --- | --- | --- |
| Official benchmark code/data release [3] | Zenodo 15672282; code ZIP SHA-256 prefix b1ed5564f5c57506 | Metadata, FNC, geometry code, reference provenance |
| Official BioEmu code release [3] | ZIP SHA-256 prefix 66748f93aa7f3c22 | Generation/code context, separate from benchmark evaluation |
| Original research publication | Zenodo 23615869, v1.0.0, 24 October 2026 | Unchanged primary CSVs, 154-member NPZ, historical documents |
| Current study repository | Read at commit 7681674d5ec80545239e80214de1bd164c07eff8 | Current published reader guidance and frozen output comparison |
| L1/L2 | Executed on 26 October 2026, subsequent to original publication | Historical source-coordinate verification records |
| This candidate | v1.1.0-rc1, unpublished | New arithmetic verifier, editorial revision and self-QC |

The two supplied Primary ZIPs differ. The complete code ZIP has SHA-256 a543c6d46c9a820f0407c13a3fb8f1fb71fb4702e2341be6b50e99c28ae7be6e; the other ZIP is a different container with compiled cache members and fewer source files. Names or download suffixes are not identity evidence. The NPZ ZIP is byte-identical to the v1.0.0 publication (SHA-256 569a09744787d2c6c9b35e9e0cc80ce2ef4dd40d6a3f494cd45fe33bed8584b7). Archive ZIP comments provide no authenticated upstream commit; archived bytes define the official version used here.

### S1.1 The 153+1 recovery

The initial system CSV has 153 PASS rows and one FAIL_QA for `1TG0__D45C_N47P`, caused by a broad reference-file lookup finding two same-named PDBs. The recovery code changes only reference selection to the exact official `reference_mutants` or `reference_wildtypes` path. It does not change the systems, settings, estimators or filters. The recovered system has A=200 and B0=199.

Combining 153 successful rows and the one recovery row recovers all 154 IDs. Comparing their common fields with the reconciled table found no change above 1e-9 and 619 numeric reserialization differences with maximum 4.44×10⁻¹⁶. The initial-output ZIP also contains a 154th NPZ for the recovery ID even though its CSV records FAIL_QA. That NPZ and the recovery NPZ have identical arrays. This is documented overlap, not an additional independent run or proof of its exact file chronology. The verifier rejects all other duplicate IDs. Available files reconstruct the executed rules; complete contemporaneous author approval and dependency history are not asserted.

## S2. Official geometry screening

The saved original geometry NPZs contain float32 `fnc` and Boolean `pass_ca`, `pass_cn`, `pass_clash`, `pass_all`. The original gate is `pass_all=pass_ca & pass_cn & pass_clash`. The additional ω diagnostic NPZs preserve the same FNC and mask as `fnc` and `b0_mask`. Those arrays are compared exactly across all 154 systems, including the documented recovery overlap.

The archived official `filter_unphysical_traj_masks` tests consecutive Cα-Cα <4.5 Å and C-N <2.0 Å. For clashes, `_compute_filtered_contacts` selects residue pairs with sequence-index difference >2 and at least one Cα distance <6 Å within the trajectory chunk, then computes closest-heavy contacts; a frame passes only if all considered contacts are >1.0 Å. Exactly 4.5, 2.0 or 1.0 Å therefore fails the relevant inequality. Distances are converted from MDTraj nm to Å and evaluated nonperiodically in the relevant sample routines. This code includes assumptions about residue geometry in its candidate prefilter and is not exhaustive certification of all atoms at arbitrary distortion.

V0 verifies the saved masks and their conjunction. It does not infer geometry from FNC values. L2 reports reapplication to coordinates; its use of chunk=100 can change the candidate union relative to a whole-trajectory call in pathological cases. Agreement in the recorded execution is not proof of chunk invariance for arbitrary ensembles.

## S3. FNC and foldedness calculation

The reference and sample are reduced to Cα atoms, with contacts drawn from reference residue pairs separated by >3 sequence positions and at reference distance ≤10 Å. The official implementation stores symmetric pairs; their duplication does not change the contact mean. Sample-reference sequence alignment maps the contact indices. The study checks complete mapping rather than accepting unmapped contacts. In this benchmark the reference and metadata sequences agree; sample sequence checks in L2 are inherited coordinate evidence.

The executable score is q(x)=mean_C{1/[1+exp(β(d(x)−λ(d_ref+δ)))]}, with β=5 Å⁻¹, λ=1.2 and δ=0.0 Å. The explicit settings matter: the archived bare `get_fnc_from_samples_trajectory` defaults are λ=0.0 and δ=1.2, whereas `FNCSettings` and the official evaluator pass λ=1.2 and δ=0.0. Calling the bare function without explicit settings would calculate a different quantity. The retained official function bodies and settings in the historical snapshots match the archived source by AST comparison, excluding their adapted logger import.

Frame contributions are f(q)=1/[1+exp(-20(q−0.5))], and p_S is their arithmetic mean over S. The calculation converts saved FNC to float64 before this transform. The source paper's PPFT/evaluation sections [1] describe soft foldedness; its S12 notation includes a signed steepness parameter. The archived executable increasing sigmoid and its explicit settings specify the transform reproduced here. Neither a hard q≥0.5 population nor f(mean q) is substituted.

For valid q∈[0,1], f lies approximately in [0.0000454,0.9999546]. With a nonempty finite set, the mean remains in this interval. This explains why no clipping occurs under these inputs; it is not a demonstration of robustness to arbitrary invalid inputs. The fixed saved FNC precision is not evidence about accuracy relative to unknown structures.

## S4. Operational ΔG and paired ΔΔG estimators

For each nonempty set, clip p to [1e-10,1−1e-10], then clip p/(1−p) to [1e-10,1e10] and compute ΔG=−RT ln(odds) at 295 K. R=0.001987203599772605 kcal mol⁻¹ K⁻¹. Empty sets are noncomputable, not assigned zero. Nonfinite or out-of-range FNC is rejected. There is no pseudocount, temperature fit, refit of the state definition or new force-field calculation.

The paired estimator is ΔΔG=ΔG_mutant−ΔG_matched_baseline. For any stage edge its change equals mutant system change minus baseline system change. Large same-signed system shifts can largely cancel; opposite-signed system shifts reinforce the paired magnitude. Across-stage reinforcement instead compares the signs of the two pair changes. Figure 2 addresses the latter; data/results/pairs_recomputed.csv separately records both system contributions.

The estimator is operational: selection changes the conditional empirical ensemble, and ΔG is a nonlinear transformation of its soft mean. No transformation here restores unknown equilibrium weights or corrects a thermodynamic bias. The deterministic numerical tolerances below are reproducibility criteria, not experimental uncertainty.

## S5. Peptide-ω screening and boundary cases

The four-atom order is Cα(i), C(i), N(i+1), Cα(i+1). Circular distance to the nearest multiple of 180° gives d(ω), ranging from 0° to 90°. Twisted means finite d>30°, with strict inequality; angles at ±30° or ±150° are not twisted. The original computation uses a vector-projection dihedral formula and checks it against MDTraj. Unknown covers missing atoms, degenerate geometry and nonfinite angles. The primary Bω rule is B0 & ~any(known twisted), retaining Unknown-only frames. Pro status belongs to the following residue and is descriptive. Cis non-Pro is counted without automatic rejection.

The saved float32 angles reproduce every Bω mask. The nearest saved angular deviation is 0.0000305176° away from the 30° boundary; none equals it. The already-defined near diagnostic is |d−30°|≤0.02°. There are 302 frames with any near bond in A and 292 in B0, explaining the different L2 and primary counts. No Unknown frames are present. In B0 there are 14,922,082 evaluable bond-frames, 27,329 twisted bond-frames, and 25,807 frames rejected for at least one twist.

The historical “permissive” scenario disregards twisted bonds within the near band; the “conservative” scenario rejects every near bond and Unknown frame in addition to known twists. These pre-existing scenarios yield 39/112 descriptive |D|≥0.1 counts, versus primary 40/112. They are not newly optimized cutoffs or statistical uncertainty bounds. Primary D falls outside the interval spanned by the two scenario values in 29/112 pairs (the historical non-bracketing diagnostic uses 1e-12 to avoid floating-point equalities). For `1EM7_V54S__D47W`, primary D is -0.1003079005 kcal/mol, conservative -0.0989172631 and permissive -0.0994791297. The primary result remains unchanged. All 29 IDs are in data/results/summary.json, and all scenario values in pairs_recomputed.csv.

## S6. Full numerical sensitivity results

Machine-readable complete tables are authoritative for unrounded values. `data/frozen/` preserves the original CSV bytes; `data/results/` holds independent replay values that agree within the frozen tolerances. Differences at the last floating-point digits are reported, never overwritten in the historical tables.

**Table S2. Soft-foldedness signed changes over 154 systems.** p is dimensionless; +/−/0 counts use strict signs. The five unchanged geometry responses are retained in all summaries.

| Edge | Median | Range | Positive / negative / zero |
| --- | ---: | --- | --- |
| A→B0 | +0.002133 | -0.000798 to +0.069137 | 135 / 14 / 5 |
| B0→Bω | +0.001850 | -0.011552 to +0.045725 | 131 / 23 / 0 |
| A→Bω | +0.004721 | -0.000855 to +0.108705 | 147 / 7 / 0 |

Full system results: data/results/systems_recomputed.csv (154 rows) contains each stage's retained n, p, ΔG, clipping flag, all three changes, removed counts and ω diagnostics. Full pair results: data/results/pairs_recomputed.csv (112 rows) contains matched baseline, fixed reference, all three ΔΔG and AE values, every stage/cumulative change, both system contributions and the two historical boundary scenarios. Legacy complete tables retain their original names in supplement/ and data/frozen/ for continuity. An original column named WT identifies the metadata baseline only.

**Table S3. Retention and descriptive flags.** Counts refer to retained frames, not evaluated peptide bond–frames. The Bω low-retention flag is descriptive only; its denominator is the official requested `num_samples`, not n_B0. It does not remove any systems or pairs from analysis.

| Diagnostic | Result |
| --- | ---: |
| A frames retained | 302,800 |
| B0 frames retained | 298,188 |
| Bω frames retained | 272,381 |
| Removed at A→B0 | 4,612 |
| Removed at B0→Bω | 25,807 |
| Minimum retained Bω frames per system | 128 |
| Bω systems below 70% of requested frames | 3 / 154 |
| Systems with ΔG clipping at any stage | 0 / 154 |

The three flagged systems are `2RRT__A48P` (128/200, 64%), `2RRT__F9P_F61V` (134/200, 67%), and `4C26__S6N_H43H` (136/200, 68%). These counts and percentages are descriptive and have no exclusion effect.

The primary continuous pair ranges and medians are in Technical Note Table 1. At the supplementary 0.1 kcal/mol threshold, edge counts are 19 and 40, with intersection 12 and union 47; the cumulative count is 44. No pair lies within 4e-9 kcal/mol of the reporting boundary in this replay. The primary conclusion depends on the full continuous results.

## S7. Secondary experimental-reference comparison

All 336 AE values are computed from the independently reconstructed pair estimates and the official reference metadata, before comparing historical AE columns. No historical AE/MAE is used as a calculation input. Every pair has three finite estimates and the same fixed experimental reference. MAE is an equal-weight arithmetic mean over 112 pairs, even though some share a baseline.

**Table S4. Secondary reference error, in kcal/mol.** Changes and counts are later stage minus earlier stage. “Unchanged” is exact equality under the fixed rule, without introducing a new tie tolerance.

| Stage | MAE |
| --- | ---: |
| A | 0.702595 |
| B0 | 0.696142 |
| Bω | 0.707681 |

| Edge | Change in MAE | AE improved / worsened / unchanged |
| --- | ---: | --- |
| A→B0 | -0.006453 | 59 / 52 / 1 |
| B0→Bω | +0.011539 | 54 / 58 / 0 |
| A→Bω | +0.005086 | 54 / 58 / 0 |

The sole exact AE tie is `6FVC__L24V` for A→B0. classification_diagnostics.csv records it as a tolerance-near sign boundary, without changing its historical tie classification. Small aggregate MAE differences, a mixed pair response and shared baselines do not establish superiority of a filter or gate. No confidence interval or significance label is attached to these descriptive differences.

## S8. Verification tiers, L1/L2 and reproducibility limits

### S8.1 Lightweight reproducibility (V0-V2)

`verification/numerics.py` and `verify.py` are new code, with no import of the original analysis or official estimator. The replay uses saved arrays, official metadata and Python/NumPy, with `math.fsum` for mean reductions. It computes all values from NPZ before loading historical result CSVs for comparison. It checks original geometry NPZ continuity, mask nesting, saved-angle classification, 154 unique systems, 112 unique pairs and every required numerical value. Input SHA-256 checks precede computation. The full original code is retained separately and is not executed by this route.

Twenty-two synthetic tests cover mask inclusion/type/shape, sigmoid and order of averaging, logit sign, clipping, empty sets, nonfinite and invalid values, paired sign and baseline, AE and MAE, stage differences, missing/duplicate IDs, ω/threshold boundaries and nonlinear intervals. The first full run stopped on the documented duplicate recovery NPZ; the corrected verifier explicitly requires the expected ID and array identity. Its original FAIL and rationale are preserved. No numeric acceptance tolerance was changed.

**Table S5. Direct absolute acceptance tolerances, fixed before full-study comparison.** Energy units are kcal/mol.

| Quantity | Stage value | Stage difference |
| --- | ---: | ---: |
| Mean soft foldedness | 1e-10 | 2e-10 |
| System ΔG | 1e-9 | 2e-9 |
| Paired ΔΔG | 2e-9 | 4e-9 |
| Pair AE | 2e-9 | 4e-9 |
| MAE | 2e-9 | 4e-9 |
| Hash, ID, count, mask | Exact | Exact |

All 462 p and 462 ΔG values, 336 ΔΔG and 336 AE values, 462 system changes for each system quantity and 336 pair changes for each pair quantity pass. The three MAEs and all three MAE differences pass. Maximum direct errors are 3.33e-16 for p, 6.59e-13 kcal/mol for system energy changes, 6.58e-13 for ΔG/ΔΔG/AE, and 7.42e-13 for pair/AE changes. Full per-cell comparisons, maxima, tolerances, failures, environment, code version and input hashes are in data/results/verification.json and comparison_details.csv.

Direct agreement is not inferred from the p tolerance. For all 462 system-stage values, evaluate the decreasing clipped ΔG transform at max(0,p−1e-10) and min(1,p+1e-10), with outward floating-point rounding. Every historical ΔG lies in its independently constructed interval; the largest interval width is 8.22e-7 kcal/mol. These intervals describe propagation of an acceptance allowance, not physical uncertainty. Exact classification rules are replayed and tolerance-near cases separately recorded. The acceptance file's SHA-256 is 1afb2ffa28b5250b516a63f64e8162ac1524f8ee5cc413d7ca5ffab782e0c2cf.

### S8.2 Coordinate-dependent route (V3)

V3 requires the official `samples_delta_G.zip` (1,959,113,732 bytes) plus the official benchmark release, MDTraj, SciPy and Biopython. The archive's official MD5 is 30c285d2a503fb3436cefda86c75a5c6; the L1 recorded SHA-256 is 81fa710c667d29f664e378e551ee1f180975a62d8e37d859646be8b2fa9469c7. These archive-level identities are inherited records; this Work did not download the 1.96 GB file or recompute its whole-file hash. The official public metadata expose its size and MD5. V3 is separate from the lightweight NPZ arithmetic route.

L1, executed 26 October, records archive identity, metadata/inventory and selected coordinate QA. L2 provides 154 individual coordinate results and 112 pair records. Its vector-normal ω expression and direct Cα/C-N distances are independent of the primary formulas, but it reuses official FNC and clash functions and MDTraj input loading. Recorded maximum ω difference against saved float32 angles is 7.63e-6°; maximum FNC difference is zero. Neither is a measure of structural truth or pre-compression coordinate accuracy. This Work directly checks IDs, all recorded source hashes, counts and all three ΔG/ΔΔG stages against the new replay, rather than relying on aggregate PASS.

The historical L2 fingerprint omits the two dynamically imported snapshot hashes, the pair CSV and some dependency versions. Its aggregate `all_pass` condition could be true without pair checking; the actual supplied records do contain exactly 112 pairs. Present-day hashes do not retrospectively prove which unrecorded imports were used. L2's recorded environment is Python 3.13.1, MDTraj 1.10.2, NumPy 2.2.1 on Windows; it is not substituted for the incompletely documented original Primary environment. Existing scripts and execution records are retained without rewriting their historical claims.

### S8.3 Claim-to-output index and release integrity

The full Claim-Source-Computation-Output matrix is provenance/claim_source_computation_output.csv. It links retention, foldedness, ΔG, paired ΔΔG, AE, MAE and changes, boundary diagnostics and verification scope to inputs and code. README.md provides executed lightweight commands, expected coverage and FAIL conditions, and labels the V3 coordinate procedure as not rerun in this Work. Hashes for the final distribution are in FILE_MANIFEST.csv and SHA256SUMS.txt; archive hashes are outside the archives to avoid circular identity claims.

Original publication material is retained at its original paths and clearly identified as v1.0.0. Revised files have versioned names. The legacy provenance files may contain preparation-time “release candidate” or pending-DOI statements; those are historical, and README.md supplies the current status. No new public DOI, GitHub tag or commit is asserted for this candidate. P3 is a separately structured review pass within this Work and cannot provide independence equivalent to another reviewer or model.

## References

[1] Lewis, S., Hempel, T., Jiménez-Luna, J., et al. Scalable emulation of protein equilibrium ensembles with generative deep learning. Science 389 (2025), eadv9817. https://doi.org/10.1126/science.adv9817

[2] Williams, C. J., Headd, J. J., Moriarty, N. W., et al. MolProbity: More and better reference data for improved all-atom structure validation. Protein Science 27 (2018), 293-315. https://doi.org/10.1002/pro.3330

[3] Microsoft Research. Supplementary data for scalable emulation of protein equilibrium ensembles with generative deep learning. Zenodo record 15672282 (2025), including bioemu-benchmarks_code_release.zip and samples_delta_G.zip. https://doi.org/10.5281/zenodo.15672282. Software: https://github.com/microsoft/bioemu-benchmarks and https://github.com/microsoft/bioemu. The archived bytes, rather than current main branches, define this study.

[4] Tsuboyama, K., et al. Mega-scale experimental analysis of protein folding stability in biology and design. Nature 620 (2023), 434-444. https://doi.org/10.1038/s41586-023-06328-6. Upstream experimental source identified by the official benchmark dataset card; reference values here are taken directly from the benchmark metadata, without reanalysis of the experiments.