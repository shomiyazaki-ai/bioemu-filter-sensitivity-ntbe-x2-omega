# Sequential post-hoc structural filtering of a fixed BioEmu stability benchmark

**Status: RELEASE CANDIDATE — not yet authorized for public deposit.**

This repository accompanies **one** Technical Note covering two related fixed-archive research questions: NT-BE (saved A to official geometry-screened B0) and X2-omega (B0 to additional peptide-omega-screened Bomega). They are not two publications or independent datasets.

## Key results
- 154 systems (42 WT, 112 mutants), 112 shared-WT mutant comparisons.
- A = 302,800 frames; B0 = 298,188; Bomega = 272,381.
- |DDG shift| >= 0.1 kcal/mol: 19/112 for A-to-B0; 40/112 for B0-to-Bomega; intersection 12, union 47; 44/112 for cumulative A-to-Bomega.
- MAE A/B0/Bomega: 0.702595 / 0.696142 / 0.707681 kcal/mol.

The analyses measure sensitivity of *predicted* foldedness/DG/DDG to post-hoc filtering of an already saved ensemble; they do not imply a more accurate equilibrium distribution, an improved free-energy model or independent biological replication.

## Files
- `manuscript/Technical_Note_RELEASE_CANDIDATE.pdf` — English Technical Note.
- `supplement/Supplementary_Information_RELEASE_CANDIDATE.pdf` — 7-section supplementary explanation.
- `supplement/Table_S2_S3_system_foldedness_dG.csv` — system-level complete response.
- `supplement/Table_S4_cross_stage_112_pairs.csv` — paired DDG/cross-stage table.
- `supplement/Table_S5_boundary_and_omega.csv` — omega boundary and sample-size information.
- `data/*.csv`, `data/report_omega.json`, `data/all_npz.zip` — original fixed analysis outputs.
- `code/` — original code and independent read-only release checks.
- `provenance/` — complete fixed publication gate and validation report.
- `SHA256SUMS.txt` — file hashes; excludes itself.

## Verification
Install NumPy and pandas, then run `python code/verify_release.py`. This is a **read-only package consistency check** and does not regenerate raw trajectories or rerun all original-coordinate calculations.

Upstream source: BioEmu original research and official benchmark archive (https://zenodo.org/records/15672282). Original FNC settings: `contact_lambda=1.2`, `contact_delta=0.0` explicitly, fixed sigmoid and 295-K conversion. A is the **saved** archive, not unscreened generating-model output.

## Evidence boundaries
The October 19 independent gate audited all 154 saved NPZ and targeted 10 original-coordinate systems/2,700 frames. It did **not** reproduce 154 original-coordinate systems. The original historical environment is not completely reconstructed. The original 153+1 dataset restoration should be described only to the extent surviving logs support it. Boundary diagnostics yield 39 instead of primary 40 in two specified alternate treatments; 'under70' is relative to requested sample targets.

## Rights and attribution — MUST REVIEW BEFORE PUBLICATION
The package contains code and data derived from upstream sources. Microsoft BioEmu software may require original MIT notices; redistributed structure/derived inputs may require CDLA-Permissive-2.0 plus third-party attributions described in the official NOTICE. A blanket original-MIT assertion is inappropriate. Obtain and include verbatim license/notice files as required after reviewing each included artifact. Human author identity, affiliation, funding, conflicts, acknowledgments, licensing choices and AI-assistance disclosure must be explicitly confirmed.

## Citation / release management
One repository plus one Zenodo DOI version series for the same integrated work. DOI not yet assigned. Do not publish until release blockers in `provenance/RELEASE_BLOCKERS.md` are cleared.

## Editorial revision (2026-10-24)

The technical note explicitly includes Section 6 (Discussion) and Section 8 (Conclusions). The fixed dataset, all tables and results remain unchanged. This is still a release candidate pending author and license review.


## Licensing, declarations, citation — 2026-10-24 administrative package

The approved scope is specified in `licenses/LICENSE_SCOPE.md` (NTBE) or `LICENSES/LICENSE_SCOPE.md` (X4). Author-owned prose and original figures are CC BY 4.0; original author-owned code is MIT. Upstream benchmark data and other third-party-derived assets are not covered by a blanket license. `AUTHOR_DECLARATIONS_FOR_APPROVAL.md`, `REFERENCES_VERIFIED.md` and `CITATION.cff` provide author-confirmation metadata. **Not yet published: final human approval and owner-rights confirmation outstanding.**

## Editorial revision (24 October 2026)
The manuscript now reports a system-level median/range of B0-to-Bomega foldedness changes and illustrates the paired WT cancellation/amplification using the original matched 1TG0 pair. Full system and paired outputs remain in the CSV files.


## Consolidated editorial release (24 October 2026)
Technical Note and SI were typeset anew with explicit Discussion/Conclusions, substantive Results and correctly formatted SI tables. See `provenance/FINAL_EDITORIAL_CHANGELOG.md`. For X4, recorded mask/lag intervention rules and fixed BioEmu Phase C AMBER99SB/TIP3P, 300 K/1 bar protocol are described. No new scientific execution or unverified Phase 2B causal certificate is claimed. Publication URLs remain to be assigned.

## Final document QC
The manuscript has complete numbered references, figure captions and author/AI declarations. Science data and SI are unchanged in this administrative update. Source A is an already-saved archive, not a raw unfiltered generative distribution.
