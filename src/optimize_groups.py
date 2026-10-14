"""Capacitated location-allocation model used in the case study.

Public-release notes
--------------------
* The script expects an already de-identified or synthetic model table.
* It never requires participant names or street addresses.
* The original research dataset must not be committed to a public repository.
* Leadership coverage is enforced by hard constraints. The leader-distance
  coefficient (default 0.7) only discounts leaders' travel cost in the
  objective, giving the solver more flexibility to place them where coverage
  is operationally required.

The optimization objective and the operational evaluation metric are distinct:
the objective uses distance to one selected center, whereas the operational
metric used in the study averages a household unit's distance to all eligible
rotating hosts in its assigned group (or to the fixed institutional site for
the fixed group).
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import pulp

DEFAULT_NUM_GROUPS = 4
DEFAULT_MAX_CAPACITY = 25
DEFAULT_LEADER_DISTANCE_WEIGHT = 0.7
EARTH_RADIUS_KM = 6371.0

REQUIRED_COLUMNS = {
    "ID",
    "Latitude",
    "Longitude",
    "Household_Size",
    "Leader_Level",
    "Host_Eligible",
    "Current_Group",
    "Fixed_Site",
}

UNASSIGNED_LABELS = {"-", "Unassigned", "unassigned", "nan", "None", "", "New"}


def load_data(path: Path) -> pd.DataFrame:
    """Load a de-identified/synthetic model table and validate its schema."""
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.copy()
    df["ID"] = df["ID"].astype(str)
    df["Current_Group"] = df["Current_Group"].fillna("Unassigned").astype(str)

    for col in ["Latitude", "Longitude"]:
        df[col] = pd.to_numeric(df[col], errors="raise")
    for col in ["Household_Size", "Leader_Level", "Host_Eligible", "Fixed_Site"]:
        df[col] = pd.to_numeric(df[col], errors="raise").astype(int)

    if (df["Fixed_Site"] == 1).sum() != 1:
        raise ValueError("Exactly one row must have Fixed_Site = 1.")
    if not set(df["Leader_Level"]).issubset({0, 1, 2}):
        raise ValueError("Leader_Level must be 0 (member), 1 (trainee), or 2 (experienced).")
    if not set(df["Host_Eligible"]).issubset({0, 1}):
        raise ValueError("Host_Eligible must be binary (0/1).")
    if not set(df["Fixed_Site"]).issubset({0, 1}):
        raise ValueError("Fixed_Site must be binary (0/1).")
    return df


def haversine_matrix(df: pd.DataFrame) -> tuple[dict[str, dict[str, float]], np.ndarray]:
    """Return pairwise geodesic distances (km) using the Haversine formula."""
    ids = df["ID"].tolist()
    coords = np.radians(df[["Latitude", "Longitude"]].to_numpy(float))
    lat = coords[:, 0]
    lon = coords[:, 1]
    dlat = lat[:, None] - lat[None, :]
    dlon = lon[:, None] - lon[None, :]
    a = np.sin(dlat / 2) ** 2 + np.cos(lat[:, None]) * np.cos(lat[None, :]) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
    matrix = EARTH_RADIUS_KM * c
    nested = {
        id_i: {id_j: float(matrix[i, j]) for j, id_j in enumerate(ids)}
        for i, id_i in enumerate(ids)
    }
    return nested, matrix


def optimize(
    df: pd.DataFrame,
    distances: dict[str, dict[str, float]],
    num_groups: int,
    max_capacity: int,
    leader_distance_weight: float,
) -> dict:
    """Solve the binary capacitated location-allocation problem."""
    if not 0 < leader_distance_weight <= 1:
        raise ValueError("leader_distance_weight must be in the interval (0, 1].")

    ids = df["ID"].tolist()
    demand = df.set_index("ID")["Household_Size"].to_dict()
    host = df.set_index("ID")["Host_Eligible"].to_dict()
    experienced = df.set_index("ID")["Leader_Level"].apply(lambda v: 1 if v == 2 else 0).to_dict()
    trainee = df.set_index("ID")["Leader_Level"].apply(lambda v: 1 if v == 1 else 0).to_dict()
    fixed_site = df.loc[df["Fixed_Site"] == 1, "ID"].iloc[0]

    if int(sum(demand.values())) > num_groups * max_capacity:
        raise ValueError("Total participant demand exceeds total configured group capacity.")
    if sum(experienced.values()) < num_groups:
        raise ValueError("Not enough experienced leaders to cover all active groups.")
    if sum(trainee.values()) < num_groups:
        raise ValueError("Not enough trainee leaders to cover all active groups.")

    model = pulp.LpProblem("Religious_Group_Allocation", pulp.LpMinimize)
    y = pulp.LpVariable.dicts("Center", ids, cat="Binary")
    x = pulp.LpVariable.dicts("Assign", (ids, ids), cat="Binary")

    # Leaders receive a lower distance coefficient. This does NOT guarantee
    # leader coverage; coverage is guaranteed by the explicit constraints below.
    costs = {}
    for i in ids:
        row_weight = leader_distance_weight if (experienced[i] or trainee[i]) else 1.0
        for j in ids:
            costs[(i, j)] = distances[i][j] * row_weight

    model += pulp.lpSum(costs[(i, j)] * x[i][j] for i in ids for j in ids)

    # Each household unit is assigned exactly once, and only to an open center.
    for i in ids:
        model += pulp.lpSum(x[i][j] for j in ids) == 1
        for j in ids:
            model += x[i][j] <= y[j]

    # Only eligible host locations may be activated.
    for j in ids:
        if host[j] == 0:
            model += y[j] == 0

    # Exactly p groups are opened, including the mandatory fixed site.
    model += pulp.lpSum(y[j] for j in ids) == num_groups
    model += y[fixed_site] == 1

    # Participant capacity (household size is used here).
    for j in ids:
        model += pulp.lpSum(demand[i] * x[i][j] for i in ids) <= max_capacity * y[j]

    # Hard coverage constraints for experienced and trainee leaders.
    for j in ids:
        model += pulp.lpSum(experienced[i] * x[i][j] for i in ids) >= y[j]
        model += pulp.lpSum(trainee[i] * x[i][j] for i in ids) >= y[j]

    model.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=60))
    status = pulp.LpStatus[model.status]
    if status != "Optimal":
        raise RuntimeError(f"Solver status: {status}")

    centers = [j for j in ids if pulp.value(y[j]) > 0.5]
    center_to_group = {center: f"Group {idx}" for idx, center in enumerate(centers, start=1)}
    assignment: dict[str, str] = {}
    assigned_center: dict[str, str] = {}
    for i in ids:
        for j in ids:
            if pulp.value(x[i][j]) > 0.5:
                assignment[i] = center_to_group[j]
                assigned_center[i] = j
                break

    return {
        "status": status,
        "objective_value": float(pulp.value(model.objective)),
        "centers": centers,
        "assignment": assignment,
        "assigned_center": assigned_center,
        "fixed_site": fixed_site,
    }


def operational_distances(
    df: pd.DataFrame,
    group_map: dict[str, str],
    distances: dict[str, dict[str, float]],
) -> dict[str, float]:
    """Distance per household unit under the study's operational metric.

    Rotating groups: mean distance to all host-eligible homes in that group.
    Fixed group: distance only to the mandatory institutional site.
    Unassigned baseline household units are omitted.
    """
    indexed = df.set_index("ID")
    fixed_site = indexed.index[indexed["Fixed_Site"] == 1][0]
    groups: dict[str, list[str]] = {}
    for uid, group in group_map.items():
        if str(group) in UNASSIGNED_LABELS:
            continue
        groups.setdefault(str(group), []).append(uid)

    per_id: dict[str, float] = {}
    for _, members in groups.items():
        if fixed_site in members:
            meeting_locations = [fixed_site]
        else:
            meeting_locations = [uid for uid in members if int(indexed.loc[uid, "Host_Eligible"]) == 1]
        if not meeting_locations:
            raise ValueError("A non-fixed active group contains no host-eligible meeting location.")
        for uid in members:
            per_id[uid] = float(np.mean([distances[uid][host_id] for host_id in meeting_locations]))
    return per_id


def operational_metrics(
    df: pd.DataFrame,
    group_map: dict[str, str],
    distances: dict[str, dict[str, float]],
) -> dict:
    """Summarize the operational scenario at the household-unit level."""
    indexed = df.set_index("ID")
    per_id = operational_distances(df, group_map, distances)

    groups: dict[str, list[str]] = {}
    for uid, group in group_map.items():
        if uid in per_id:
            groups.setdefault(str(group), []).append(uid)

    rows = []
    for group, members in sorted(groups.items()):
        member_distances = [per_id[uid] for uid in members]
        rows.append({
            "Group": group,
            "Participants": int(indexed.loc[members, "Household_Size"].sum()),
            "Experienced_Leaders": int((indexed.loc[members, "Leader_Level"] == 2).sum()),
            "Trainee_Leaders": int((indexed.loc[members, "Leader_Level"] == 1).sum()),
            "Mean_Household_Distance_km": float(np.mean(member_distances)),
            "Min_Household_Distance_km": float(np.min(member_distances)),
            "Max_Household_Distance_km": float(np.max(member_distances)),
            "Household_Units": len(members),
        })

    values = list(per_id.values())
    return {
        "mean_household_distance_km": float(np.mean(values)) if values else 0.0,
        "groups": rows,
        "n_household_units_evaluated": len(values),
        "distance_by_id": per_id,
    }


def paired_comparison(baseline: dict, optimized: dict) -> dict:
    """Compare only household units present in both scenarios."""
    before = baseline["distance_by_id"]
    after = optimized["distance_by_id"]
    common = sorted(set(before) & set(after))
    if not common:
        return {"n": 0}
    b = np.array([before[i] for i in common], dtype=float)
    a = np.array([after[i] for i in common], dtype=float)
    reduction = (b.mean() - a.mean()) / b.mean() * 100 if b.mean() else 0.0
    return {
        "n": len(common),
        "baseline_mean_household_distance_km": float(b.mean()),
        "optimized_mean_household_distance_km": float(a.mean()),
        "percent_reduction": float(reduction),
        "households_shorter": int(np.sum(a < b - 1e-9)),
        "households_longer": int(np.sum(a > b + 1e-9)),
        "households_unchanged": int(np.sum(np.isclose(a, b, atol=1e-9))),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("results/run"))
    parser.add_argument("--num-groups", type=int, default=DEFAULT_NUM_GROUPS)
    parser.add_argument("--max-capacity", type=int, default=DEFAULT_MAX_CAPACITY)
    parser.add_argument("--leader-weight", type=float, default=DEFAULT_LEADER_DISTANCE_WEIGHT)
    args = parser.parse_args()

    df = load_data(args.input)
    distances, _ = haversine_matrix(df)

    baseline_map = dict(zip(df["ID"], df["Current_Group"]))
    baseline = operational_metrics(df, baseline_map, distances)

    solution = optimize(
        df,
        distances,
        num_groups=args.num_groups,
        max_capacity=args.max_capacity,
        leader_distance_weight=args.leader_weight,
    )
    optimized = operational_metrics(df, solution["assignment"], distances)
    paired = paired_comparison(baseline, optimized)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "parameters": {
            "num_groups": args.num_groups,
            "max_capacity": args.max_capacity,
            "leader_distance_weight": args.leader_weight,
        },
        "metric_definition": (
            "Household-unit operational distance: mean distance to all host-eligible locations "
            "within a rotating group; fixed-site group uses the institutional site only."
        ),
        "baseline": {k: v for k, v in baseline.items() if k != "distance_by_id"},
        "optimized": {k: v for k, v in optimized.items() if k != "distance_by_id"},
        "paired_common_households": paired,
        "solution": {
            "status": solution["status"],
            "objective_value": solution["objective_value"],
            "centers": solution["centers"],
            "fixed_site": solution["fixed_site"],
        },
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    assignment_df = df[["ID", "Household_Size", "Leader_Level", "Host_Eligible"]].copy()
    assignment_df["Optimized_Group"] = assignment_df["ID"].map(solution["assignment"])
    assignment_df["Assigned_Center"] = assignment_df["ID"].map(solution["assigned_center"])
    assignment_df["Operational_Distance_km"] = assignment_df["ID"].map(optimized["distance_by_id"])
    assignment_df.to_csv(args.output_dir / "assignments.csv", index=False)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
