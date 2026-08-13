"""
Scrape MBTA GTFS schedule data and build a weighted transit adjacency matrix
for 14 Boston neighborhoods used in the GNN-Influenza model.

Edge weight = normalized weekly cross-boundary trip frequency between
consecutive stops on MBTA routes.

Outputs (to Data/MBTA/):
  - mbta_edges.csv           : edge list with weights
  - mbta_adjacency_matrix.csv: 14×14 symmetric matrix
"""

import os
import zipfile
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data" / "MBTA"

GTFS_URL = "https://cdn.mbta.com/MBTA_GTFS.zip"
GTFS_ZIP = DATA_DIR / "MBTA_GTFS.zip"
GTFS_DIR = DATA_DIR / "gtfs"

BOUNDARIES_URL = (
    "https://data.boston.gov/dataset/e11a621a-6561-4da6-a715-6edd2fa217a4/"
    "resource/c9663e7a-84c2-435c-91c0-91cdce1ee5ac/download/"
    "boston_neighborhood_boundaries_approximated_by_2020_census_block_groups.geojson"
)
BOUNDARIES_FILE = DATA_DIR / "boston_neighborhoods.geojson"

# 14 canonical GNN neighborhood names (indices 0-13)
NEIGHBORHOODS = [
    "Allston/Brighton",
    "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Charlestown",
    "Dorchester",
    "East Boston",
    "Fenway",
    "Hyde Park",
    "Jamaica Plain",
    "Mattapan",
    "Roslindale",
    "Roxbury",
    "South Boston",
    "South End",
    "West Roxbury",
]

# Map boundary GeoJSON neighborhood names → canonical GNN node name
BOUNDARY_TO_GNN = {
    "Allston": "Allston/Brighton",
    "Brighton": "Allston/Brighton",
    "Back Bay": "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Beacon Hill": "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Downtown": "Back Bay/Beacon Hill/Downtown/North End/West End",
    "North End": "Back Bay/Beacon Hill/Downtown/North End/West End",
    "West End": "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Bay Village": "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Chinatown": "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Leather District": "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Charlestown": "Charlestown",
    "Dorchester": "Dorchester",
    "East Boston": "East Boston",
    "Fenway": "Fenway",
    "Longwood": "Fenway",
    "Hyde Park": "Hyde Park",
    "Jamaica Plain": "Jamaica Plain",
    "Mattapan": "Mattapan",
    "Roslindale": "Roslindale",
    "Mission Hill": "Roxbury",
    "Roxbury": "Roxbury",
    "South Boston": "South Boston",
    "South Boston Waterfront": "South Boston",
    "South End": "South End",
    "West Roxbury": "West Roxbury",
}

# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------


def download_gtfs():
    """Download and extract MBTA GTFS feed."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if GTFS_DIR.exists() and (GTFS_DIR / "stops.txt").exists():
        print("GTFS already extracted, skipping download.")
        return

    if not GTFS_ZIP.exists():
        print("Downloading MBTA GTFS feed …")
        resp = requests.get(GTFS_URL, timeout=120)
        resp.raise_for_status()
        GTFS_ZIP.write_bytes(resp.content)
        print(f"  saved {GTFS_ZIP} ({len(resp.content) / 1e6:.1f} MB)")

    print("Extracting GTFS …")
    GTFS_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(GTFS_ZIP, "r") as zf:
        zf.extractall(GTFS_DIR)
    print("  done.")


def download_boundaries():
    """Download Boston neighborhood boundary GeoJSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if BOUNDARIES_FILE.exists():
        print("Boundary GeoJSON already exists, skipping.")
        return

    print("Downloading Boston neighborhood boundaries …")
    resp = requests.get(BOUNDARIES_URL, timeout=60)
    resp.raise_for_status()
    BOUNDARIES_FILE.write_bytes(resp.content)
    print(f"  saved {BOUNDARIES_FILE}")


def assign_stops_to_neighborhoods():
    """Spatial-join MBTA stops to Boston neighborhoods. Returns dict: stop_id → GNN name."""
    stops = pd.read_csv(GTFS_DIR / "stops.txt", dtype=str)
    # Keep physical stops/stations only (location_type 0 or empty, and 1)
    stops = stops[
        stops["location_type"].fillna("0").isin(["0", "1", ""])
    ].copy()
    stops["stop_lat"] = stops["stop_lat"].astype(float)
    stops["stop_lon"] = stops["stop_lon"].astype(float)

    geometry = [Point(lon, lat) for lon, lat in zip(stops["stop_lon"], stops["stop_lat"])]
    stops_gdf = gpd.GeoDataFrame(stops, geometry=geometry, crs="EPSG:4326")

    # Load boundaries
    boundaries = gpd.read_file(BOUNDARIES_FILE)
    # Try common column names for neighborhood label
    name_col = None
    for col in ["blockgr2020_ctr_neighb_name", "neighborhood", "Name", "name",
                 "NEIGHBORHOOD", "neighb_name", "BlockGr2020_CtrNeighb_Name"]:
        if col in boundaries.columns:
            name_col = col
            break
    if name_col is None:
        # Print columns to help debug and pick the right one
        print(f"  Boundary columns: {list(boundaries.columns)}")
        # Try any column containing 'neighb' (case-insensitive)
        for col in boundaries.columns:
            if "neighb" in col.lower():
                name_col = col
                break
    if name_col is None:
        raise ValueError(f"Cannot find neighborhood name column. Columns: {list(boundaries.columns)}")

    print(f"  Using boundary column: '{name_col}'")

    # Dissolve block groups into neighborhood polygons
    boundaries["gnn_name"] = boundaries[name_col].map(BOUNDARY_TO_GNN)
    # Drop block groups outside the 14 neighborhoods
    boundaries = boundaries.dropna(subset=["gnn_name"])
    neighborhoods_gdf = boundaries.dissolve(by="gnn_name").reset_index()

    # Spatial join
    joined = gpd.sjoin(stops_gdf, neighborhoods_gdf[["gnn_name", "geometry"]],
                        how="left", predicate="within")

    stop_to_neighborhood = {}
    for _, row in joined.iterrows():
        if pd.notna(row.get("gnn_name")):
            stop_to_neighborhood[row["stop_id"]] = row["gnn_name"]

    # Summary
    assigned = len(stop_to_neighborhood)
    total = len(stops)
    print(f"  Assigned {assigned}/{total} stops to Boston neighborhoods "
          f"({total - assigned} outside Boston, dropped)")

    covered = set(stop_to_neighborhood.values())
    missing = set(NEIGHBORHOODS) - covered
    if missing:
        print(f"  WARNING: No stops found for: {missing}")
    else:
        print("  All 14 neighborhoods have at least one stop.")

    return stop_to_neighborhood


def get_representative_services():
    """Find representative weekday, Saturday, Sunday service_ids.

    Returns dict: {'weekday': set, 'saturday': set, 'sunday': set}
    """
    calendar_file = GTFS_DIR / "calendar.txt"
    calendar_dates_file = GTFS_DIR / "calendar_dates.txt"

    services = {"weekday": set(), "saturday": set(), "sunday": set()}

    if calendar_file.exists():
        cal = pd.read_csv(calendar_file, dtype=str)
        for _, row in cal.iterrows():
            sid = row["service_id"]
            if row.get("monday", "0") == "1" and row.get("tuesday", "0") == "1":
                services["weekday"].add(sid)
            if row.get("saturday", "0") == "1":
                services["saturday"].add(sid)
            if row.get("sunday", "0") == "1":
                services["sunday"].add(sid)

    # If calendar.txt didn't yield results, fall back to calendar_dates.txt
    if not any(services.values()) and calendar_dates_file.exists():
        cal_dates = pd.read_csv(calendar_dates_file, dtype=str)
        cal_dates["date"] = pd.to_datetime(cal_dates["date"], format="%Y%m%d")
        # Only additions (exception_type == 1)
        additions = cal_dates[cal_dates["exception_type"] == "1"].copy()
        additions["dow"] = additions["date"].dt.dayofweek

        # Pick the most recent date for each day type
        for dow_range, key in [((0, 1, 2, 3, 4), "weekday"), ((5,), "saturday"), ((6,), "sunday")]:
            subset = additions[additions["dow"].isin(dow_range)]
            if not subset.empty:
                latest_date = subset["date"].max()
                services[key] = set(
                    subset[subset["date"] == latest_date]["service_id"]
                )

    print(f"  Service IDs — weekday: {len(services['weekday'])}, "
          f"saturday: {len(services['saturday'])}, sunday: {len(services['sunday'])}")
    return services


def count_transitions(stop_to_neighborhood, services):
    """Count cross-neighborhood transitions for consecutive stops on each trip.

    Returns dict: {('weekday'|'saturday'|'sunday'): Counter of (n1, n2) pairs}
    """
    stop_times = pd.read_csv(GTFS_DIR / "stop_times.txt", dtype=str,
                              usecols=["trip_id", "stop_id", "stop_sequence"])
    stop_times["stop_sequence"] = stop_times["stop_sequence"].astype(int)

    trips = pd.read_csv(GTFS_DIR / "trips.txt", dtype=str,
                         usecols=["trip_id", "service_id"])

    # Build service_id → day_type lookup
    sid_to_day = {}
    for day_type, sids in services.items():
        for sid in sids:
            sid_to_day[sid] = day_type

    # Filter trips to representative services
    trips = trips[trips["service_id"].isin(sid_to_day)]
    trip_to_day = dict(zip(trips["trip_id"], trips["service_id"].map(sid_to_day)))

    # Filter stop_times to relevant trips
    stop_times = stop_times[stop_times["trip_id"].isin(trip_to_day)]

    print(f"  Processing {len(trip_to_day)} trips, "
          f"{len(stop_times)} stop_time records …")

    # Sort for sequential walk
    stop_times = stop_times.sort_values(["trip_id", "stop_sequence"])

    counts = {
        "weekday": defaultdict(int),
        "saturday": defaultdict(int),
        "sunday": defaultdict(int),
    }

    prev_trip = None
    prev_neigh = None

    for _, row in stop_times.iterrows():
        tid = row["trip_id"]
        sid = row["stop_id"]
        day = trip_to_day.get(tid)
        if day is None:
            continue

        neigh = stop_to_neighborhood.get(sid)

        if tid == prev_trip and neigh is not None and prev_neigh is not None:
            if neigh != prev_neigh:
                pair = tuple(sorted([neigh, prev_neigh]))
                counts[day][pair] += 1

        if tid != prev_trip:
            prev_trip = tid
        prev_neigh = neigh

    for day in counts:
        print(f"    {day}: {sum(counts[day].values())} cross-boundary transitions, "
              f"{len(counts[day])} unique pairs")

    return counts


def build_adjacency(counts):
    """Build 14×14 symmetric adjacency matrix from transition counts."""
    n = len(NEIGHBORHOODS)
    idx = {name: i for i, name in enumerate(NEIGHBORHOODS)}

    # Raw weekly trips
    raw = pd.DataFrame(0, index=NEIGHBORHOODS, columns=NEIGHBORHOODS, dtype=float)

    for day_type, multiplier in [("weekday", 5), ("saturday", 1), ("sunday", 1)]:
        for (n1, n2), count in counts[day_type].items():
            i, j = idx.get(n1), idx.get(n2)
            if i is not None and j is not None:
                raw.iloc[i, j] += count * multiplier
                raw.iloc[j, i] += count * multiplier

    # Normalize to [0, 1]
    max_val = raw.values.max()
    if max_val > 0:
        normalized = raw / max_val
    else:
        normalized = raw.copy()

    # Build edge list
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if raw.iloc[i, j] > 0:
                edges.append({
                    "neighborhood_1": NEIGHBORHOODS[i],
                    "neighborhood_2": NEIGHBORHOODS[j],
                    "weight": round(normalized.iloc[i, j], 6),
                    "raw_weekly_trips": int(raw.iloc[i, j]),
                })

    edges_df = pd.DataFrame(edges).sort_values("weight", ascending=False)

    return normalized, edges_df, raw


def main():
    print("=" * 60)
    print("MBTA Transit Edge Scraper for GNN")
    print("=" * 60)

    print("\n[1/6] Downloading GTFS feed …")
    download_gtfs()

    print("\n[2/6] Downloading neighborhood boundaries …")
    download_boundaries()

    print("\n[3/6] Assigning stops to neighborhoods …")
    stop_to_neighborhood = assign_stops_to_neighborhoods()

    print("\n[4/6] Finding representative service schedules …")
    services = get_representative_services()

    print("\n[5/6] Counting cross-neighborhood transitions …")
    counts = count_transitions(stop_to_neighborhood, services)

    print("\n[6/6] Building adjacency matrix …")
    normalized, edges_df, raw = build_adjacency(counts)

    # Save outputs
    edges_df.to_csv(DATA_DIR / "mbta_edges.csv", index=False)
    normalized.to_csv(DATA_DIR / "mbta_adjacency_matrix.csv")

    # Summary
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"\nEdges with nonzero weight: {len(edges_df)}")
    print(f"Max raw weekly trips: {int(raw.values.max())}")

    # Check symmetry
    diff = (normalized.values - normalized.values.T).sum()
    print(f"Symmetry check (should be 0): {diff:.6f}")

    # Isolated nodes
    row_sums = raw.sum(axis=1)
    isolated = row_sums[row_sums == 0].index.tolist()
    if isolated:
        print(f"WARNING — isolated neighborhoods: {isolated}")
    else:
        print("No isolated neighborhoods — all 14 are connected.")

    # Top edges
    print("\nTop 10 edges by weight:")
    for _, row in edges_df.head(10).iterrows():
        print(f"  {row['neighborhood_1']:50s} <-> {row['neighborhood_2']:20s}  "
              f"w={row['weight']:.4f}  ({row['raw_weekly_trips']} trips/wk)")

    print(f"\nOutputs saved to {DATA_DIR}/")
    print("  - mbta_edges.csv")
    print("  - mbta_adjacency_matrix.csv")


if __name__ == "__main__":
    main()
