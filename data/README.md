# Data directory

## What is public

`synthetic_example.csv` is a **fully synthetic** dataset. No row corresponds to a real person, family, address, household, leader, host, or meeting site from the study.

It mirrors only the computational schema needed by the model:

- 38 household/site records;
- household demand;
- leadership category;
- host eligibility;
- baseline group label;
- one mandatory fixed site;
- artificial latitude/longitude values.

## What must remain private

The original research spreadsheet must not be uploaded to a public GitHub repository. It contains names, full residential addresses, exact coordinates, household-size information, group membership, and religious leadership/participation variables. Combining these fields creates a high re-identification risk and reveals sensitive information.

Recommended private storage layout (ignored by Git):

```text
data/private/original.xlsx
data/private/processed_confidential.csv
```

## Why a synthetic dataset is used

A public research repository should allow readers to inspect and execute the method without exposing study participants. The synthetic data support method-level reproducibility, whereas exact numerical replication of the case-study results requires the confidential dataset and should only be considered under an appropriate restricted-access mechanism and ethical/legal authorization.
