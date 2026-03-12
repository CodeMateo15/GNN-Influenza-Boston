MBTA Transit Edge Data — Collection & Methodology
===================================================
Generated: 2026-03-12
Script:    Code/scrape_mbta_edges.py


1. PURPOSE
----------
The GNN model uses a hand-coded binary adjacency matrix based on geographic
borders between 14 Boston neighborhoods. This data adds weighted edges based
on actual MBTA transit connectivity, where the weight reflects how many
scheduled trips per week cross between each pair of neighborhoods. The idea
is that neighborhoods connected by frequent transit service likely share more
commuter flow (and therefore more potential disease transmission) than
neighborhoods that merely share a border.


2. DATA SOURCES
---------------

A) MBTA GTFS Static Feed
   URL:      https://cdn.mbta.com/MBTA_GTFS.zip
   Downloaded: 2026-03-12 (13.2 MB zip)
   Format:   General Transit Feed Specification (GTFS) — an industry-standard
             format used by transit agencies worldwide.
   License:  Free, public, no API key required.
   Contents used:
     - stops.txt       (8,060 physical stops/stations within scope)
     - stop_times.txt  (1,035,760 records for representative services)
     - trips.txt       (39,713 trips in representative services)
     - routes.txt      (398 routes total)
     - calendar.txt    (60 service patterns)

   The feed covers the schedule period 2026-03-04 through 2026-04-04.

B) Boston Neighborhood Boundaries (2020 Census Block Groups)
   URL:      https://data.boston.gov (via CKAN API)
   Dataset:  "Boston Neighborhood Boundaries Approximated by 2020 Census
              Block Groups"
   Format:   GeoJSON with polygon geometries
   Field used: blockgr2020_ctr_neighb_name (neighborhood label per block group)


3. WHAT TRANSIT MODES ARE INCLUDED
-----------------------------------
The GTFS feed contains ALL MBTA services. The script does not filter by mode
— every scheduled trip contributes to the edge weights. The breakdown of the
39,713 trips processed:

   Local Bus .............. 15,691 trips  (39.5%)
   Frequent Bus ........... 13,118 trips  (33.0%)  [includes Silver Line]
   Rapid Transit ..........  8,950 trips  (22.5%)
   Regional Rail (Commuter)    900 trips   (2.3%)
   Commuter Bus ...........    381 trips   (1.0%)
   Coverage Bus ............   248 trips   (0.6%)
   Ferry ...................   220 trips   (0.6%)
   Rail Replacement Bus ....   115 trips   (0.3%)
   Seasonal Ferry ..........    81 trips   (0.2%)
   Supplemental Bus ........     9 trips   (0.0%)

Rapid Transit includes all subway/light rail lines:
   Red Line, Orange Line, Blue Line, Green Line (B/C/D/E branches),
   Mattapan Trolley

Frequent Bus includes Silver Line (SL1, SL2, SL3, SL4, SL5) and other
high-frequency bus routes.

So in short: the edges capture bus + subway + commuter rail + Silver Line +
ferry — the full MBTA network. Bus service dominates (~73% of trips), which
makes sense because MBTA operates ~129 bus routes vs. 8 rapid transit lines,
and buses run on more varied corridors throughout the city.

Only trips with stops physically inside Boston city limits contribute.
Stops in Cambridge, Somerville, Brookline, Quincy, Braintree, etc. are
dropped. A trip that goes Boston -> Cambridge -> Boston still counts the
Boston-Boston transitions but not the segments through Cambridge.


4. METHODOLOGY
--------------

Step 1: Spatial Assignment of Stops to Neighborhoods
   - Load all 8,060 physical stops (location_type 0 = stop, 1 = station)
     from stops.txt.
   - Convert to point geometries using lat/lon coordinates.
   - Spatial join (point-in-polygon) against dissolved neighborhood
     boundary polygons.
   - 2,299 stops fall within Boston; 5,761 are outside Boston (dropped).
   - All 14 neighborhoods have at least one assigned stop.
   - Fine-grained boundary names are mapped to the 14 canonical GNN nodes:
       Allston + Brighton                         -> Allston/Brighton
       Back Bay + Beacon Hill + Downtown +
         North End + West End + Bay Village +
         Chinatown + Leather District              -> Back Bay/Beacon Hill/Downtown/North End/West End
       Charlestown                                 -> Charlestown
       Dorchester (both zip zones)                 -> Dorchester
       East Boston                                 -> East Boston
       Fenway + Longwood                           -> Fenway
       Hyde Park                                   -> Hyde Park
       Jamaica Plain                               -> Jamaica Plain
       Mattapan                                    -> Mattapan
       Roslindale                                  -> Roslindale
       Mission Hill + Roxbury                      -> Roxbury
       South Boston + South Boston Waterfront      -> South Boston
       South End                                   -> South End
       West Roxbury                                -> West Roxbury

Step 2: Representative Service Selection
   - Parse calendar.txt to identify service patterns that run on:
       Weekdays (monday=1 AND tuesday=1): 16 service IDs
       Saturdays: 21 service IDs
       Sundays: 18 service IDs
   - These represent a "typical week" of MBTA service.

Step 3: Counting Cross-Neighborhood Transitions
   - For each trip in the representative services:
       1. Sort its stop_times by stop_sequence.
       2. Walk consecutive stop pairs (stop N -> stop N+1).
       3. If stop N is in neighborhood A and stop N+1 is in neighborhood B,
          and A != B, increment the count for the (A, B) pair.
   - Only CONSECUTIVE stops are counted, not all-pairs on a route. This is
     a better proxy for actual ridership because most riders travel short
     segments, not the full route end-to-end. It also avoids quadratic
     blowup on long routes.
   - If either stop in a pair is outside Boston, that transition is skipped.

Step 4: Weekly Aggregation
   - Weekly trips = (weekday count x 5) + (Saturday count x 1) + (Sunday count x 1)
   - The matrix is made symmetric: weight(A,B) = weight(B,A). This is natural
     because a bus going A->B will also go B->A on its return trip, and we
     care about connectivity, not directionality.

Step 5: Normalization
   - The raw weekly trip counts are divided by the maximum value to produce
     weights in [0, 1].
   - Max raw value: 14,896 weekly trips (Back Bay <-> South Boston).


5. RESULTS SUMMARY
------------------
32 neighborhood pairs have nonzero transit connectivity (out of 91 possible).

Top 10 edges by weight:

   Back Bay/etc <-> South Boston ......... 1.0000  (14,896 trips/wk)
   Jamaica Plain <-> Roxbury ............ 0.9595  (14,293 trips/wk)
   Fenway <-> Roxbury ................... 0.9327  (13,893 trips/wk)
   Back Bay/etc <-> South End ........... 0.8036  (11,970 trips/wk)
   Dorchester <-> South Boston .......... 0.7490  (11,157 trips/wk)
   Dorchester <-> Roxbury ............... 0.7176  (10,690 trips/wk)
   Back Bay/etc <-> Fenway .............. 0.6464   (9,629 trips/wk)
   Roxbury <-> South End ................ 0.5407   (8,055 trips/wk)
   Jamaica Plain <-> Roslindale ......... 0.4239   (6,314 trips/wk)
   Dorchester <-> Mattapan .............. 0.3234   (4,818 trips/wk)

Weakest edges:
   Back Bay/etc <-> Hyde Park ........... 0.0003      (5 trips/wk)
   Allston/Brighton <-> Back Bay/etc .... 0.0030     (45 trips/wk)
   Hyde Park <-> Jamaica Plain .......... 0.0040     (60 trips/wk)
   Allston/Brighton <-> South End ....... 0.0040     (60 trips/wk)


6. INTERPRETATION
-----------------

- The strongest edge (Back Bay <-> South Boston) reflects the Red Line and
  Silver Line corridors, plus many bus routes through the downtown core. This
  makes geographic and transit-network sense — South Station is a major hub
  right at the Back Bay/South Boston boundary.

- Roxbury is a major transit hub: it has strong connections to Jamaica Plain
  (Orange Line + buses), Fenway (numerous bus routes through Ruggles),
  Dorchester (buses along Blue Hill Ave and Warren St), and South End. This
  aligns with Roxbury's role as a central transfer point.

- The Dorchester <-> Mattapan connection (0.32) captures the Mattapan Trolley
  (Red Line branch) plus several bus routes along Blue Hill Ave.

- Charlestown is only connected to Back Bay/Downtown (0.27), reflecting the
  Orange Line and a few bus routes. It's relatively isolated transit-wise.

- West Roxbury connects only to Roslindale (0.18), Hyde Park (0.08), and
  weakly to Jamaica Plain (0.02). This matches its position at the end of the
  Needham commuter rail line and limited bus service.

- The weakest edge (Back Bay <-> Hyde Park, 5 trips/wk) likely represents
  a single commuter rail line with very few stops that happen to land in
  both neighborhoods.

- East Boston connects to Back Bay/Downtown (0.22, Blue Line) and South
  Boston (0.21, SL1 via airport). No other Boston neighborhoods — it's
  geographically isolated across the harbor.


7. LIMITATIONS & CAVEATS
-------------------------

- SCHEDULE, NOT RIDERSHIP: These are scheduled trips, not actual passenger
  counts. A bus that runs every 10 minutes but carries 5 people gets the same
  weight as a subway train every 10 minutes carrying 500 people. Actual
  ridership data (from MBTA's AFC/automated fare collection system) would be
  more accurate but is not freely available at the stop-pair level.

- STATIC SNAPSHOT: The GTFS feed represents the schedule as of March 2026.
  Service levels change seasonally and have changed significantly since COVID.
  The relative connectivity between neighborhoods is fairly stable over time,
  but absolute trip counts may differ from earlier years.

- CONSECUTIVE STOPS ONLY: We count transitions between consecutive stops on
  a route, not origin-destination pairs. A rider taking the Orange Line from
  Jamaica Plain to Back Bay passes through Roxbury and South End — our method
  counts JP<->Roxbury, Roxbury<->South End, South End<->Back Bay, but not
  the direct JP<->Back Bay connection. This underweights long-distance
  connections but better reflects local transmission risk (people on the
  same train car for one stop vs. many stops).

- STOPS OUTSIDE BOSTON DROPPED: If a route goes through Cambridge between
  two Boston neighborhoods, the Boston<->Cambridge and Cambridge<->Boston
  transitions are invisible. This mainly affects the Red Line (through
  Cambridge/Somerville), Green Line (through Brookline), and commuter rail.

- NO BACKGROUND NODE: The Background node (index 14) in the GNN is a
  synthetic anchor for boundary effects. It has no physical location and
  receives no MBTA edges.

- BOUNDARY PRECISION: Stop-to-neighborhood assignment uses point-in-polygon
  with 2020 Census Block Group boundaries. A stop right on a boundary line
  could be assigned to either side. This affects a small number of stops.


8. OUTPUT FILES
---------------

mbta_edges.csv
   Columns: neighborhood_1, neighborhood_2, weight, raw_weekly_trips
   32 rows (one per nonzero edge), sorted by weight descending.
   weight is normalized to [0, 1].

mbta_adjacency_matrix.csv
   14x14 symmetric matrix with neighborhood names as row/column headers.
   Values are normalized weights [0, 1]. Zero means no direct transit
   connection between those neighborhoods.


9. REPRODUCIBILITY
------------------
To regenerate:
   python Code/scrape_mbta_edges.py

Dependencies: requests, pandas, geopandas (includes shapely), zipfile (stdlib)

The GTFS feed URL is stable but the content updates periodically as MBTA
publishes new schedules. Re-running will download the latest feed, so results
may differ slightly from the original March 2026 run. The extracted GTFS and
boundary files are cached in Data/MBTA/ and reused if present — delete them
to force a fresh download.
