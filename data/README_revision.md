# Revision data dictionary

`frozen/` holds unchanged original research output CSVs and published display tables. Original published paths under data/ and supplement/ remain for continuity. `inputs/all_npz.zip` is the exact published 154-member saved-array archive. The two original geometry/recovery ZIPs and L1/L2 records are preserved input evidence. `results/` contains the new independent replay, not a replacement primary result.

## systems_recomputed.csv (154 rows)

`system`, `matched_baseline`, `is_mutant` use the official metadata. `target_frames` is official num_samples. Suffixes `_A`, `_B0`, `_Bomega` denote all saved frames, official geometry pass, and additional omega pass.

- `n_*`: retained frames, integers.
- `p_*`: mean frame-level soft foldedness (dimensionless), after f(q)=1/[1+exp(-20(q-0.5))].
- `dg_*`: operational folded-minus-unfolded estimate (kcal/mol), clipped logit at 295 K.
- `clipped_*`: whether either original probability or odds clipping changed a value.
- `delta_p_a_to_b`, `delta_dg_a_to_b`: later minus earlier; three edges A_to_B0, B0_to_Bomega, A_to_Bomega.
- `removed_n_a_to_b`: frame count removed along that edge.
- `twisted_bond_frames`, `evaluable_bond_frames`: B0 bond-frame counts, not frame counts.
- `unknown_frames`: B0 frames with any unknown omega.
- `near_A`, `near_B0`: frames with any known |d-30|<=0.02 degree bond, with the stated denominator.
- `near_bonds_B0`: B0 bond-frame near count.
- `min_omega_threshold_gap_deg`: nearest saved known angular deviation's absolute distance to 30 degrees.
- `dg_boundary_permissive`, `dg_boundary_conservative`: the two pre-existing diagnostic selection scenarios (kcal/mol), not bounds.

## pairs_recomputed.csv (112 rows)

`mutant`, `matched_baseline`, `ddg_exp` define the fixed pair and official reference (kcal/mol). `ddg_S` is mutant dg_S minus baseline dg_S; `ae_S` is abs(ddg_S-ddg_exp). `delta_ddg_edge` and `delta_ae_edge` are later minus earlier (kcal/mol). `mutant_dg_shift_edge` and `baseline_dg_shift_edge` decompose the paired shift by subtraction. `opposite_system_signs_edge` flags the signs of those two system shifts. `opposite_stage_signs` instead compares the two sequential pair shifts. Neither flag removes data. `boundary_D_*` is scenario DDG minus primary B0 DDG, in kcal/mol.

## Verification records

`comparison_details.csv` contains each computed/saved value, absolute error, fixed tolerance and pass flag. `classification_diagnostics.csv` contains one row per pair per edge (336), exact threshold flags and AE signs plus tolerance-near warnings. `nonlinear_intervals.csv` has 462 p-interval propagation records. Its intervals quantify an acceptance allowance only. `npz_member_manifest.csv` hashes all 154 saved members. `summary.json` contains complete stage summaries, counts, MAE and changes. `verification.json` records code version/hash, input hashes, all checks, coverage, maxima and FAILs.

All finite numeric values are written without display rounding. The PDFs use six-decimal display for energy/foldedness summaries; no calculation uses those rounded displays. A positive delta AE is worse, a negative delta AE better, and exact zero unchanged. `pass_` is a Boolean output field; an empty failures list and complete required coverage, not a single label in isolation, establish a full V0-V2 success.
