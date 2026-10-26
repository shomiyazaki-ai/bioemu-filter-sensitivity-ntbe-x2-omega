# NT-BE / X2-ω: sequential screening sensitivity in a fixed BioEmu benchmark

**Version 1.1.0 release-ready snapshot, prepared 26 October 2026; Zenodo publication pending.** It preserves the scientific results of [published v1.0.0](https://doi.org/10.5281/zenodo.23615869). The version-specific Zenodo DOI **10.5281/zenodo.23660292** has been reserved by the author in the unpublished new-version Draft; GitHub release commit and tag are recorded externally after they exist; this snapshot alone does **not** establish publication of v1.1.0. The previously observed public baseline commit was `7681674d5ec80545239e80214de1bd164c07eff8`, **not** the new release commit. See [release completion checklist](RELEASE_METADATA_PENDING.md).

## Read the study

| Purpose | File |
| --- | --- |
| Revised English Technical Note | [PDF](manuscript/Technical_Note_v1.1.0_rc1.pdf) · [editable Markdown](manuscript/Technical_Note_v1.1.0_rc1.md) |
| Revised Supplementary Information | [PDF](supplement/Supplementary_Information_v1.1.0_rc1.pdf) · [editable Markdown](supplement/Supplementary_Information_v1.1.0_rc1.md) |
| Revised figures | [Figure 1](figures/Figure_1_retention_v1.1.0_rc1.png) · [Figure 2](figures/Figure_2_signed_shifts_v1.1.0_rc1.png), with PDF, SVG and generating source in figures/ |
| Complete independently reconstructed results | [154 systems](data/results/systems_recomputed.csv) · [112 matched pairs](data/results/pairs_recomputed.csv) · [summary](data/results/summary.json) |
| Fixed historical numerical outputs | [data/frozen/](data/frozen/) and unchanged original data/ and supplement/ CSV paths |
| Verification evidence | [machine-readable report](data/results/verification.json) · [all comparisons](data/results/comparison_details.csv) · [nonlinear intervals](data/results/nonlinear_intervals.csv) |
| Claim-to-source index | [matrix](provenance/claim_source_computation_output.csv) · [source manifest](provenance/source_manifest.csv) |
| Production and release judgment | [P2 report](provenance/P2_Production_Report_JA.md) · [P3 self-QC report](provenance/P3_Independent_QC_Report_JA.md) |

The primary question concerns sensitivity of FNC-derived soft foldedness and operational stability estimates to sequential geometry and peptide-ω screening, at system and matched-pair levels. The fixed 154-system ensemble has 42 matched baselines and 112 mutants, forming 112 comparisons. “Matched baseline” follows official `name_wt`; not every baseline is an unmodified natural wild type.

A ⊇ B0 ⊇ Bω retain 302,800, 298,188 and 272,381 frames. Continuous system and pair changes are heterogeneous; mutant-minus-baseline subtraction can amplify or cancel system shifts. The minimum contribution is a traceable fixed-archive case record using existing rules. The conclusion does not depend on the arbitrary descriptive 0.1 kcal/mol count. Experimental-reference errors are a separate secondary analysis (MAE A/B0/Bω = 0.702595/0.696142/0.707681 kcal/mol).

These operational estimates do not demonstrate recovered equilibrium populations, experimental thermodynamic correction, complete all-atom validity, general predictive improvement, or a recommendation to adopt either gate. Shared baselines make pairs dependent.

## What changed from v1.0.0

The revision supplies self-contained Methods, both foldedness-screening responses, all three signed energy-change paths, secondary AE/MAE calculations, clearer figures, source-to-output links and a complete independent saved-array verifier. It adds the 26 October L1/L2 evidence as subsequent verification with explicit limits. It changes no original research CSV, NPZ, primary script, filter cutoff or estimator.

Original PDFs, images, code and provenance retain their published paths and bytes. The revised documents/figures have versioned names. `provenance/README_SOURCE_ARCHIVE.md`, `provenance/README_JA.md`, the old `SOURCE_AND_QA.md` and `VALIDATION_REPORT.json`, and `provenance/history/` describe earlier stages. Their old pending-DOI or release-candidate language is historical, not the status of this candidate or of published v1.0.0. Historical scripts under code/ and code/historical/ are preserved records, not the standard verification entrypoint.

## Execute the standard lightweight route: V0-V2

Requirements: Python 3.12 and NumPy 2.3.5. A fresh isolated Linux environment with Python 3.12.14 and NumPy 2.3.5 was used successfully; the installation, 22 artificial tests and whole-study verification logs are in provenance/. Windows/other Python versions were not freshly tested in this Work. No GPU, MDTraj, SciPy or Biopython is needed for V0-V2.

From the root of the **complete candidate** directory:

```bash
python -m venv .venv
# Activate .venv using the command appropriate to your operating system.
python -m pip install -r requirements-verification.txt
python verification/test_numerics.py
python verification/verify.py --out verification-run
```

The two Python verification commands and NumPy installation were executed in a fresh venv. The exact environment-specific command log is `provenance/clean_environment_commands.txt`. Choose an unused output directory: the verifier deliberately refuses to overwrite a prior run. It writes only the selected output directory, never the inputs. The calculations import no original analysis code. Run synthetic tests before full-study verification.

**Inputs:** `data/inputs/all_npz.zip` (51,612,943 bytes), the original geometry-output and recovery ZIPs, official `sources/official/system_info.csv`, historical result CSVs in data/frozen/, and the hash-pinned source/acceptance files identified by verification/input_manifest.json. The full Zenodo candidate includes them. The smaller GitHub staging ZIP omits only all_npz.zip; obtain the identical saved NPZ from the original publication as described below.

**Expected output:** `verification.json` with status PASS, coverage p=462, dg=462, ddg=336, ae=336, an empty failures list, per-group maxima and tolerances; 154-row systems and 112-row pairs CSVs; 336-row classification diagnostics; 462 nonlinear intervals; NPZ member hashes; summary.json. Preserved outputs are under data/results/. Small differences at floating-point last digits are allowed only by the frozen acceptance specification.

V0 verifies hashes, exact IDs, target mapping, counts and Boolean masks. V1 reconstructs frame-level soft foldedness, means, ΔG, ΔΔG and all changes. V2 independently uses official experimental references for every AE/MAE and all changes. Historical numerical result columns are not calculation inputs; they are opened after reconstruction for comparison. The nonlinear ΔG interval test is separate from direct value agreement. Exact historical threshold/tie rules are retained and near-boundary classifications are listed separately.

FAIL conditions include a missing/changed input, unexpected duplicate/missing ID, wrong mask type/shape/nesting, nonfinite/out-of-range FNC, noncomputable set, missing pair, count/mask disagreement, or any direct/interval/classification mismatch. Hash or schema failures stop the run and are not silently skipped. Exit code is nonzero. See acceptance_spec.json for the unchanged numerical tolerances.

### Obtain the NPZ for the GitHub staging directory

Download the published [Supporting_Data_and_Code_v1.0.0.zip](https://zenodo.org/records/23615869/files/Supporting_Data_and_Code_v1.0.0.zip?download=1) (SHA-256 `91753d9a9fb2494e2619a03d9f9f1db38ac5e999f1a9661a8e592467e35c4c31`). Extract **only** its member `data/all_npz.zip` to the new candidate's `data/inputs/all_npz.zip`. Its SHA-256 must be `569a09744787d2c6c9b35e9e0cc80ce2ef4dd40d6a3f494cd45fe33bed8584b7`.

The publication archive was actually downloaded, its MD5 checked against Zenodo, and the supplied NPZ byte-matched in this Work. To perform the extraction after saving the downloaded ZIP in the current directory:

```bash
python verification/install_npz_from_v1.py Supporting_Data_and_Code_v1.0.0.zip
```

This extraction command was executed on a clean copy of the GitHub staging structure. It verifies both archive and member hashes and refuses to overwrite a different file. It does not generate replacement FNC or coordinates.

## Separate coordinate route: V3

V3 is not a lightweight alternative to V1. It needs the official [benchmark archive record](https://zenodo.org/records/15672282), in particular `samples_delta_G.zip` (1,959,113,732 bytes) and `bioemu-benchmarks_code_release.zip`, plus MDTraj, SciPy, Biopython and NumPy. The exact archived releases, not latest pip defaults, are the source. Current upstream dependency behavior may differ. No new structures need to be generated.

The original-coordinate archive was not downloaded or rerun in this Work. Historical L1/L2 records in data/inputs/ were acquired and directly checked. L2 has 154 individual system and 112 pair records. It shares official FNC/clash functions and MDTraj loading, while ω and adjacent Cα/C-N distances have separately written formulas. Its fingerprint omits both imported snapshots, the pair CSV and some dependency versions. Its aggregate `all_pass` alone does not enforce 112 pairs. These limits remain; today's hashes do not repair historical fingerprints.

For a future replay, create an external input directory holding exactly one each of `samples_delta_G.zip`, `bioemu-benchmarks_code_release.zip`, `all_npz.zip`, `NTBE_systems_154_reconciled.csv` and `NTBE_pairs_112_reconciled.csv` (the latter two from data/frozen/). The saved NPZ is copied from data/inputs/. The historical L2 script and both snapshots are together in code/historical/. The following procedure is a **documented template, not executed in this Work**:

```bash
python code/historical/ntbe_l2_verify_L2_v1_0_1.py --root /absolute/path/to/v3_inputs --mode pilot --out replay_new
python code/historical/ntbe_l2_verify_L2_v1_0_1.py --root /absolute/path/to/v3_inputs --mode full --out replay_new
python code/historical/ntbe_l2_verify_L2_v1_0_1.py --root /absolute/path/to/v3_inputs --mode aggregate --out replay_new
```

Its historical observed environment was Python 3.13.1, MDTraj 1.10.2, NumPy 2.2.1, with additional SciPy/Biopython versions unrecorded. Before any future replay, hash all inputs and both imported snapshots, record all dependency versions, and independently require 154 unique system and 112 unique pair results. This guidance does not change or certify the historical script. Its original tolerances differ from the new V0-V2 specification; do not substitute its aggregate PASS for the saved-array verification. The old L1/L2 kits and actual executed L2 v1.0.1 source are retained separately.

## Rebuild documents and figures

Install requirements-production.txt in a suitable Python environment. The renderer uses DejaVu TTF fonts at `/usr/share/fonts/truetype/dejavu`; adjust the documented FONTS directory in the script for another OS. Then run:

```bash
python figures/make_revision_figures.py
python manuscript/build_revision_pdfs.py
```

Both commands were executed here. ReportLab generates PDFs from the versioned Markdown; equation images are generated by mathtext. The figure source reads independent result tables. Review rendered PDFs after any source change. Figure PNGs are 400 dpi, with PDF/SVG alternatives.

## Rights and citation

Original author text and figures: CC BY 4.0. Eligible original author code, including verification/ and the revision figure/PDF builders: MIT. Official benchmark software: Microsoft MIT. Dataset material: CDLA-Permissive-2.0, with the official NOTICE crediting PDB (CC0) and MegaScale (CC BY 4.0). Full upstream notices accompany source/data; inclusion does not relicense them as author-owned. See licenses/REVISION_LICENSE_SCOPE.md. Raw XTC, model weights and the accepted-paper PDF are not distributed in this candidate.

**v1.1.0 version DOI reserved (not yet registered/published): `10.5281/zenodo.23660292`.** Until that Draft is published, the citable public record is [v1.0.0](https://doi.org/10.5281/zenodo.23615869). Root CITATION.cff now identifies the forthcoming report version with the reserved DOI; **do not interpret DOI reservation as publication**. Confirm the DOI after publishing. The prior candidate CFF remains at CITATION_v1.1.0_rc1.cff as historical evidence and must not be used as the public citation. Original v1.0.0 CFF is retained under provenance/history/v1.0.0/. See RELEASE_METADATA_PENDING.md for exact release blockers. Final distribution SHA-256 and inventory are SHA256SUMS.txt and FILE_MANIFEST.csv; external delivery checksums identify the two ZIPs. The GitHub staging ZIP differs from the full Zenodo candidate by omission of the large NPZ member and by distribution-specific manifests; no scientific output is omitted.

## Author review and release

The author approved the scientific and editorial candidate; this does not mean the public release has occurred. Verify declarations, per-file rights, version DOI, GitHub revision commit/tag, release metadata and distributions using RELEASE_METADATA_PENDING.md before publication. The existing v1.0.0 draft GitHub release must not be published accidentally. The Zenodo GitHub automatic archive setting must be checked to avoid duplicate deposits. No public commit, tag, Zenodo version creation or upload was performed in this metadata-preparation step. P3 is the same Work's structured self-review, not a separate human/model audit.
