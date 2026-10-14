# Combinatorial Optimization for Religious Study-Group Allocation

This repository is a publication-oriented reproducibility package for the case study **“Combinatorial Optimization and Geoprocessing for Allocating Members to Religious Study Groups.”**

## Scope

The study formulates the allocation of household units to small religious study groups as a capacitated p-median/location-allocation problem with additional operational constraints for host eligibility, group capacity, experienced leadership, leadership in training, and a mandatory fixed meeting site.

The repository is intentionally designed **not to publish the original individual-level dataset**. The original data contain direct identifiers, residential addresses, exact geocoordinates, and variables that reveal participation and roles in a religious organization. The public `data/synthetic_example.csv` is fully synthetic and is provided only to demonstrate the workflow and code interface.

## Repository structure

```text
.
├── data/
│   ├── README.md
│   └── synthetic_example.csv
├── docs/
│   ├── DATA_AVAILABILITY.md
│   ├── DATA_DICTIONARY.md
│   ├── REPRODUCIBILITY_AUDIT.md
│   └── METHODOLOGICAL_CORRECTIONS.md
├── results/
│   └── reported_aggregate_results.csv
├── src/
│   ├── generate_synthetic_data.py
│   └── optimize_groups.py
├── .gitignore
├── CITATION.cff
├── LICENSE
└── requirements.txt
```

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/optimize_groups.py --input data/synthetic_example.csv --output-dir results/synthetic_run
```

The synthetic dataset will not reproduce the article's numerical results. The article results were obtained from the confidential research dataset. Aggregate values reported in the thesis are preserved in `results/reported_aggregate_results.csv` for reference.

## Model implemented

The code uses binary decision variables for (i) opening candidate meeting centers and (ii) assigning each household unit to one opened center. It enforces:

- exactly one assignment per household unit;
- assignment only to an opened center;
- candidate-center eligibility restricted to host-capable locations;
- exactly four active groups;
- mandatory activation of the fixed institutional site;
- a maximum capacity of 25 participants per group;
- at least one experienced leader and one leader in training per active group.

The public implementation uses a leader travel-cost coefficient of **0.7**, consistent with the corrected manuscript and the allocation reported in the thesis. This coefficient discounts leader travel in the objective; it does **not** create the leadership coverage requirement, which is enforced by explicit constraints. The code also reports a paired robustness comparison when the historical scenario contains unassigned household units. See `docs/METHODOLOGICAL_CORRECTIONS.md`.

## Privacy and research-data statement

Do **not** commit the original spreadsheet, geocoded addresses, raw maps, interactive HTML maps, or any export that contains exact coordinates. See `docs/DATA_AVAILABILITY.md` for a recommended journal data-availability statement and `data/README.md` for the public/private split.

## Citation

If this code is used in a publication, update `CITATION.cff` with the final article title, journal, DOI, and repository release version.
