# Development failure record

The first full saved-input run stopped at an overlapping recovery NPZ ID. The initial-output ZIP contains that ID despite its FAIL_QA CSV row. Exact array identity with the recovery member was confirmed; the verifier now accepts only this explicitly named overlap and fails any other duplicate. The original fatal JSON/log are preserved. No numerical comparison tolerance changed.

The initial PDF renderer also encountered a duplicate ReportLab invariant argument before producing final PDFs; this authoring-only error was corrected. It affected no scientific value. Final PDFs were rebuilt and visually reviewed.
