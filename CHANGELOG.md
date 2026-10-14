# Changelog

All notable changes to this repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-10-14

### Added
- Public reproducibility package for the study on capacitated location-allocation applied to religious small-group formation.
- Corrected Python implementation of the optimization model using PuLP/CBC.
- Synthetic example dataset for public reproducibility without exposing confidential household-level data.
- Data dictionary describing the repository variables and expected schema.
- Data availability statement explaining why the original dataset is not publicly shared.
- Aggregate results reported in the thesis for reference.
- Reproducibility audit documenting methodological and implementation checks.
- Methodological corrections document describing changes made after review of the original thesis code and text.
- Citation metadata through `CITATION.cff`.
- MIT License and dependency specification through `requirements.txt`.

### Changed
- Standardized the leadership travel-cost weight to 0.7 to match the corrected manuscript and reported allocation.
- Clarified that leadership composition is enforced by explicit model constraints rather than by the objective-function weight.
- Clarified that reported travel distances are calculated at the household-unit level.
- Distinguished the optimization objective distance from the operational distance metric used for rotating host locations.
- Corrected references to geodesic distance so that the documentation consistently reflects the Haversine formulation.
- Clarified that the historical and optimized scenarios do not contain exactly the same set of allocated household units.
- Updated documentation to avoid overstating the elimination of extreme travel distances.

### Privacy
- Removed all direct identifiers, residential addresses, exact geocoded coordinates, and real household-level records from the public repository.
- Restricted the public data package to synthetic data and aggregate reported results.
- Added explicit guidance against committing confidential source data or maps generated from exact coordinates.

### Notes
- The synthetic dataset is intended to reproduce the workflow and data structure, not the exact numerical results reported in the article/thesis.
- The original confidential dataset remains unavailable publicly due to privacy and confidentiality constraints.
