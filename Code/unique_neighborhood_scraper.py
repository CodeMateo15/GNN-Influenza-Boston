import pandas as pd
from pathlib import Path

def read_csv_with_dynamic_header(path):
    # Detect header row automatically
    with open(path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    header_row = None
    for i, line in enumerate(lines):
        if "GEOID" in line and "YEAR" in line:
            header_row = i
            break

    if header_row is None:
        raise ValueError(f"No valid header found in {path}")

    df = pd.read_csv(
        path,
        skiprows=header_row,
        encoding='utf-8-sig'
    )

    df.columns = df.columns.str.strip()
    return df


# -------------------------
# GROUP 1: Multiple CSVs
# -------------------------

group1_folder = Path("/Users/mateobiggs/GNN-Influenza-Boston/Data/Neighborhood Data")  # change this
group1_files = list(group1_folder.glob("*.csv"))

if not group1_files:
    raise ValueError("No CSV files found in Group 1 folder.")

reference_neighborhoods = None
file_neighborhood_map = {}

for file in group1_files:
    df = read_csv_with_dynamic_header(file)

    if "GEOID" not in df.columns:
        raise ValueError(f"GEOID column missing in {file}")

    neighborhoods = set(
        df["GEOID"].dropna().astype(str).str.strip().unique()
    )

    file_neighborhood_map[file.name] = neighborhoods

    if reference_neighborhoods is None:
        reference_neighborhoods = neighborhoods
    else:
        if neighborhoods != reference_neighborhoods:
            missing = reference_neighborhoods - neighborhoods
            extra = neighborhoods - reference_neighborhoods

            print(f"\nMismatch detected in: {file.name}")
            if missing:
                print(f"  Missing neighborhoods: {sorted(missing)}")
            if extra:
                print(f"  Extra neighborhoods: {sorted(extra)}")

            raise ValueError("Group 1 CSVs do not contain identical neighborhood sets.")


print("All Group 1 CSVs contain identical neighborhoods.")
group1_neighborhoods = sorted(reference_neighborhoods)


# -------------------------
# GROUP 2: Single CSV
# -------------------------

group2_path = "/Users/mateobiggs/GNN-Influenza-Boston/Data/BPHC Flu Data/BPHC Dashboard Influenza Neighborhood.csv"  # <-- change this
df2 = pd.read_csv(group2_path)

group2_neighborhoods = sorted(
    df2["description"].dropna().astype(str).unique()
)


# -------------------------
# GROUP 3: Single CSV
# -------------------------

group3_path = "/Users/mateobiggs/GNN-Influenza-Boston/Data/BPHC Flu Data/BPHC Dashboard Influenza Wastewater.csv"  # <-- change this
df3 = pd.read_csv(group3_path)

group3_neighborhoods = sorted(
    df3["demographic_value"].dropna().astype(str).unique()
)


# -------------------------
# OUTPUT
# -------------------------

print("Group 1 Unique Neighborhoods:", group1_neighborhoods)
print("Group 2 Unique Neighborhoods:", group2_neighborhoods)
print("Group 3 Unique Neighborhoods:", group3_neighborhoods)
