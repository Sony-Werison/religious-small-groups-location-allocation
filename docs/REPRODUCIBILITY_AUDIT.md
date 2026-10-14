# Reproducibility status

The main inconsistencies identified during the pre-publication audit have been resolved in the public code and in the corrected English translation of the thesis. See `METHODOLOGICAL_CORRECTIONS.md` for the full list.

## Public-release decisions

- The source spreadsheet is **not public**.
- The repository contains only synthetic row-level data and aggregate values reported in the study.
- Leader distance coefficient: **0.7**.
- Leadership coverage: enforced by explicit constraints.
- Distance method: **Haversine/geodesic**.
- Reported scenario means: household-unit operational distances.
- The baseline may contain unassigned household units; these are excluded from the historical operational mean and are disclosed in the output.
- A paired comparison is additionally reported for household units present in both scenarios.

Before final journal submission, execute the code with the confidential analysis dataset in a controlled environment, archive the resulting `summary.json`, and compare all manuscript tables against that run. Do not upload the confidential input file or exact-coordinate outputs to GitHub.
