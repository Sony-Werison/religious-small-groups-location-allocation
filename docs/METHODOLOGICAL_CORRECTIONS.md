# Methodological corrections incorporated in the public release

This repository incorporates corrections identified during the conversion of the thesis into a journal manuscript. They are corrections of reporting, terminology, and reproducibility; they do not change the principal allocation reported in the thesis.

1. **Leader coefficient:** the public code uses `0.7`, consistent with the thesis narrative and with the allocation reported in the results. The appendix version containing `0.9` was a stale script version.
2. **Meaning of the coefficient:** the coefficient does not enforce leadership coverage. Because it is below 1.0, it discounts leader travel in the objective and gives the solver greater flexibility to place leaders farther away. Minimum experienced/trainee coverage is guaranteed by hard constraints.
3. **Exactly four groups:** the public formulation explicitly documents the constraint `sum(y_j) = p`, with `p = 4` in the case study.
4. **Distance terminology:** all spatial distances are described as geodesic/Haversine distances, not Euclidean distances.
5. **Unit of the reported mean:** 4.74 km and 3.46 km are household-unit operational means, not participant-weighted means. Participant counts are used in the capacity constraint.
6. **Operational metric vs. objective:** the optimizer assigns each household unit to one selected center, whereas the evaluation metric for rotating groups averages distance to all eligible hosts in that group. The manuscript now states this distinction explicitly.
7. **Baseline Group C:** the fixed institutional site was the active meeting location in the historical scenario. Under the same fixed-site-only rule used to obtain the 4.74 km overall mean, Group C's mean is approximately **4.07 km**. The earlier 3.88 km value mixed a host-eligibility rule with the fixed-site rule.
8. **Different scenario sample sizes:** one household unit was unassigned historically and enters the optimized configuration. The reported 26.93% is therefore an operational scenario comparison (37 historical household units versus 38 optimized household units), not a strictly paired estimate.
9. **Paired robustness check:** when the comparison is restricted to the 37 household units observed in both scenarios, the mean operational distance changes from approximately **4.74 km to 3.37 km**, a reduction of approximately **28.91%**.
10. **Extreme-distance claim:** the optimized scenario still contains a high-distance household-level outlier (about 16.09 km). The corrected text states that the global mean was reduced while some individual households experienced longer travel.
11. **Scale terminology:** the dataset comprises 38 consolidated household units representing 90 participants; references to “38 members” have been corrected.
12. **Privacy:** the raw spreadsheet contains direct identifiers, addresses, exact geocoordinates, and variables revealing religious participation/roles. It is explicitly excluded from the public repository. The public example is synthetic.
13. **Reference correction:** the thesis citation to ABNT NBR 5411 as a personal-data-protection standard was removed from the manuscript because it is not an appropriate source for that claim. Privacy statements are grounded in the applicable ethical/data-protection framework instead.
