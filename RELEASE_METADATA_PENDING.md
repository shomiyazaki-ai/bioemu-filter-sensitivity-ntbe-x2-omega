# v1.1.0 release completion gate — NOT YET PUBLISHED

This package is a **release-preparation artifact**, not an issued version. Its science, code and tables remain the author-approved rc1 output. **Do not publish without closing each gate and regenerating both packages and manifests.**

## Required before GitHub/Zenodo public release

1. **AUTHOR-REPORTED COMPLETE:** A new version draft was created from published v1.0.0. Independently verify new-version lineage in the owner-controlled Zenodo UI before release.
2. **AUTHOR-REPORTED COMPLETE:** Reserved v1.1.0 version DOI `10.5281/zenodo.23660292` in the Zenodo draft. It is not yet publicly registered. Verify exact DOI in the owner-controlled draft before upload and confirm resolution after publication; it is distinct from previous v1.0.0 DOI `10.5281/zenodo.23615869` and any concept DOI.
3. Verify the author statements: current affiliation, funding, competing interests, AI assistance, acknowledgments, source attribution and whether author-owned figures/text/code can be assigned their documented licenses.
4. Resolve all per-file third-party dataset/code redistribution and Zenodo record-level license-selection issues. Retain original notices.
5. Confirm the GitHub integration/automatic Zenodo archiving setting is disabled or will not create a duplicate record. Preserve the existing **draft** v1.0.0 GitHub release without accidentally publishing it.
6. **DOI-only metadata binding complete:** README.md, VERSION.json, CITATION.cff preferred-citation, CHANGELOG.md, DISTRIBUTION.json and this checklist now carry reserved `10.5281/zenodo.23660292`. Final public release status/date and GitHub commit/tag remain pending. Do not insert hypothetical commit SHAs or tags.
7. If a final release commit SHA must be referenced by immutable archive data, determine the cycle-free sequence before packaging. A final commit SHA must not be embedded in the tree used to generate that same SHA. Use an external crosswalk or release metadata as necessary.
8. Rebuild FILE_MANIFEST.csv and SHA256SUMS.txt in both variants, reconstruct ZIP files deterministically and write **external** ZIP SHA-256 checksums. Verify the GitHub and Zenodo common files are byte-identical; the Zenodo archive has the additional large NPZ.
9. Re-run V0–V2 from clean copies and re-check PDF/table/figure integrity, including Table S3, after all changes.
10. Commit only the intended revision to the approved GitHub branch; verify tag v1.1.0 points to the intended commit. Create a GitHub release only with the correct archival integration setting. Publish the existing-version-lineage Zenodo draft after final file and metadata verification.
11. Post-release check all public links, DOI resolution, Zenodo version lineage, GitHub tag/commit, citation metadata and ZIP hashes. Preserve v1.0.0 unaltered.

## Version resolution fields

| Field | Status |
| --- | --- |
| Previous published record | 10.5281/zenodo.23615869 |
| Target version | 1.1.0 |
| New version DOI | `10.5281/zenodo.23660292` — RESERVED, author-reported, unpublished |
| Concept DOI | NOT VERIFIED IN THIS PACKAGE |
| New GitHub commit SHA | NOT CREATED IN THIS PACKAGE |
| New Git tag | PLANNED v1.1.0; NOT CREATED |
| Release date | NOT DETERMINED |
| GitHub release | NOT PUBLISHED |
| Zenodo new-version record | DRAFT CREATED (author-reported), NOT PUBLISHED |

**Release gate:** all above must be completed; do not interpret a local QC PASS as publication approval.
