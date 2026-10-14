"""Generate a fully synthetic example dataset for the public repository.

No value in this file is derived from an individual participant record.
The generator mirrors only the dimensions and broad constraints needed to
exercise the optimization workflow.
"""
from __future__ import annotations

import csv
import math
import random
from pathlib import Path

SEED = 20261014
N_RECORDS = 38
OUT = Path(__file__).resolve().parents[1] / "data" / "synthetic_example.csv"


def main() -> None:
    rng = random.Random(SEED)

    # 37 household units + one fixed institutional site.
    household_sizes = [2] * 25 + [3] * 6 + [4] * 6
    # This yields 92; adjust two artificial records to obtain a total of 90.
    household_sizes[0] = 1
    household_sizes[1] = 1
    rng.shuffle(household_sizes)

    experienced = set(rng.sample(range(1, 38), 6))
    remaining = [i for i in range(1, 38) if i not in experienced]
    trainees = set(rng.sample(remaining, 6))

    host_candidates = set(rng.sample(range(1, 38), 7))

    rows = []
    center_lat, center_lon = -10.0, -50.0  # fictional synthetic study region
    for i in range(1, 38):
        angle = rng.uniform(0, 2 * math.pi)
        radius_km = min(rng.expovariate(1 / 5.0), 18.0)
        dlat = (radius_km / 111.0) * math.sin(angle)
        dlon = (radius_km / (111.0 * math.cos(math.radians(center_lat)))) * math.cos(angle)
        leader = 2 if i in experienced else (1 if i in trainees else 0)
        current_group = rng.choice(["A", "B", "C"])
        if i == 28:
            current_group = "Unassigned"
        rows.append([
            f"F{i:03d}",
            round(center_lat + dlat, 6),
            round(center_lon + dlon, 6),
            household_sizes[i - 1],
            leader,
            1 if i in host_candidates else 0,
            current_group,
            0,
        ])

    # Mandatory fixed institutional site, deliberately synthetic.
    rows.append(["SITE", center_lat + 0.002, center_lon - 0.002, 0, 0, 1, "C", 1])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Latitude", "Longitude", "Household_Size", "Leader_Level",
            "Host_Eligible", "Current_Group", "Fixed_Site"
        ])
        writer.writerows(rows)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
