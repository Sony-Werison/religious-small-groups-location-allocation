# Public model data dictionary

| Column | Type | Description |
|---|---|---|
| `ID` | string | Artificial record identifier. |
| `Latitude` | float | Synthetic latitude in decimal degrees. |
| `Longitude` | float | Synthetic longitude in decimal degrees. |
| `Household_Size` | integer | Number of participants represented by the household unit; 0 for the fixed institutional site. |
| `Leader_Level` | integer | 0 = no preaching/leadership role, 1 = leader in training, 2 = experienced leader. |
| `Host_Eligible` | integer | 1 if the location can host meetings, otherwise 0. |
| `Current_Group` | string | Baseline group label (`A`, `B`, `C`) or `Unassigned`. |
| `Fixed_Site` | integer | 1 only for the mandatory institutional meeting site. |

The public file contains synthetic values only.
