# Data dictionary and observation boundaries

## 1. Synthetic system boundary

Every table contains invented teaching data. No source observation, actual neighbourhood, participant response or intervention estimate appears in these files. The generation seed is `20261013`; the generator and deliberate defects are recorded in [the generation manifest](../data/generation_manifest.json).

An identifier connects records. It does not establish a causal relationship. Different observation levels must remain explicit when tables are joined, aggregated or evaluated.

| File | Observation level | Key | Raw rows | Coverage |
| --- | --- | --- | --- | --- |
| `neighbourhoods.csv` | Fictional neighbourhood | `neighbourhood_id` | 12 | One static teaching snapshot |
| `ecosystems.csv` | Neighbourhood-year | `neighbourhood_id`, `year` | 72 | 2020 to 2025, inclusive |
| `monitoring.csv` | Neighbourhood-day, before cleaning | `neighbourhood_id`, `date` after cleaning | 1,088 | 1 June to 29 August 2025; eight duplicate rows |
| `sessions.csv` | Fictional game session | `session_id` | 36 | Each session is linked to one fictional area |
| `questionnaires.csv` | Session-phase | `session_id`, `phase` | 71 | 36 pre records; 35 post records |
| `game_choices.csv` | Session-turn | `session_id`, `turn` | 108 | Three sequential choices per session |
| `scenario_assumptions.csv` | Assumed future | `future` | 3 | Futures A, B and C have no assigned probabilities |
| `interventions.csv` | Programme option | `intervention` | 4 | Invented effects and programme costs |

All CSV files are in [data/raw](../data/raw/). `data_status` marks the first six tables as `synthetic`. The scenario and intervention tables also contain entirely synthetic assumptions, even though that marker column is absent.

## 2. Area and ecosystem attributes

| Field | Type and units | Meaning and interpretation boundary |
| --- | --- | --- |
| `neighbourhood_id` | Text, `N01` to `N12` | Fictional area key; whitespace and case defects occur in monitoring |
| `neighbourhood_name` | Text | Invented name; no link to a real locality |
| `population` | Integer, people | Invented area denominator, held constant throughout the exercises |
| `older_residents_pct` | Numeric, % | Invented share of older residents; age cut-off is unspecified, so real-data use needs a definition |
| `deprivation_score` | Numeric, 0 to 100 | Arbitrary proxy; larger values mean greater illustrative deprivation; no official index is represented |
| `x_km`, `y_km` | Numeric, fictional kilometres | Coordinates on a simple teaching grid; no coordinate reference system or real geographical position |
| `year` | Integer | Annual ecosystem snapshot label; the 2025 snapshot is assumed available as baseline metadata |
| `canopy_pct` | Numeric, % | Invented area share under tree canopy; change is measured in percentage points |
| `impervious_pct` | Numeric, % | Invented impervious-surface share; held constant across years |
| `habitat_condition_score` | Numeric, 0 to 100 | Arbitrary condition proxy derived partly from canopy; no validated ecological assessment instrument |

Canopy and impervious cover are separate indicators. Their values need not sum to 100. Six annual snapshots describe invented cover trajectories; they do not identify an ecological tipping point.

## 3. Monitoring attributes and quality rules

| Field | Type and units after cleaning | Meaning and interpretation boundary |
| --- | --- | --- |
| `date` | Datetime, daily | One monitoring day; the source file stores ISO dates as text |
| `regional_air_temp_c` | Numeric, degrees Celsius | Shared regional weather input; repeated across all areas on a day |
| `surface_temp_c` | Numeric, degrees Celsius | Invented land-surface reading; distinct from air temperature or personal exposure |
| `relative_humidity_pct` | Numeric, % | Invented humidity reading |
| `electricity_kwh_per_household` | Numeric, kWh per household per day | Invented daily area mean; no actual meter records |
| `service_calls` | Integer, calls per neighbourhood-day | Invented aggregate service demand; no clinical or heat-specific outcome is supplied |

Workshop 03 removes eight exact duplicates, normalises three untidy area keys and converts unreadable surface text to missing values. Ten blanks, two `sensor_error` strings and one 99 C reading leave 13 missing surface observations in 1,080 cleaned neighbourhood-days. One humidity value of 105% becomes missing.

The teaching surface bounds are -10 to 65 C; humidity bounds are 0 to 100%. These rules handle deliberate defects. A real monitoring programme requires sensor-specific checks, provenance and review of unexpected but plausible readings.

## 4. Game-session attributes

| Field | Type and units | Meaning and interpretation boundary |
| --- | --- | --- |
| `session_id` | Text, `S001` to `S036` | Fictional session key; no person is identified |
| `feedback_text` | Text | Repeated invented comments for practising text handling |
| `phase` | Text, `pre` or `post` | Questionnaire phase within the same session |
| `knowledge_score` | Integer, 0 to 6 | Arbitrary teaching score; no items, psychometric properties or validated instrument are supplied |
| `confidence_pct` | Integer, 0 to 100 | Invented reported confidence; no paired item-level correctness measure |
| `turn` | Integer, 1 to 3 | Choice order within a session |
| `choice` | Text | `tree_cover`, `shade` or `monitor`; no option establishes objectively better judgement |
| `active_decision_seconds` | Integer, seconds | Invented time associated with a choice; real telemetry needs timing and interruption rules |
| `evidence_opened` | Integer, 0 or 1 | Whether a fictional evidence panel was opened; opening does not establish reading or comprehension |

Session `S036` has no post record. Complete-case pre/post analysis therefore has 35 pairs. The 108 turns are nested within 36 sessions, so treating turns as 108 independent participants would inflate the sample size.

## 5. Scenario and programme assumptions

| Field | Units | Role in the toy calculator |
| --- | --- | --- |
| `future` | A, B or C | Conditional scenario label; no likelihood is available |
| `background_warming_c` | Degrees Celsius | Assumed temperature increment |
| `canopy_loss_pp` | Percentage points | Assumed loss before programme effects |
| `cooling_c_per_canopy_pp` | Degrees Celsius per percentage point | Invented canopy-effect coefficient |
| `shade_cooling_c` | Degrees Celsius per shade unit | Invented street-shade effect |
| `burden_per_degree` | Arbitrary burden units per degree | Teaching coefficient above the invented surface rule |
| `intervention` | Text | Programme label |
| `canopy_gain_pp` | Percentage points | Assumed mature-canopy gain; growth delay is omitted |
| `shade_units` | Dimensionless | Zero or one shade programme unit; no physical specification |
| `programme_cost_gbp` | GBP, whole-programme cost | Invented cost for the fictional city; no appraisal, maintenance or discounting model |

The GBP 150,000 baseline budget excludes the combined option. Programme benefits apply to every area using the same coefficients. The comparison excludes changing population, rebound, biodiversity dynamics and implementation uncertainty.

## 6. Important derived fields

| Derived field | Definition | Interpretation boundary |
| --- | --- | --- |
| `service_calls_per_1000` | Calls / population × 1,000 | Daily area rate; no age standardisation or causal attribution |
| `high_service_demand` | 1 when calls are at least 12; otherwise 0 | Invented same-day aggregate target; never a clinical alert |
| `teaching_priority_score` | 100 times the weighted sum of three components | Value-dependent teaching index; no validated research risk index |
| `cluster` | K-means membership label | Arbitrary profile identifier; no ordinal risk meaning |
| `mean_teaching_burden` | Area mean of the toy burden rule | Dimensionless scenario output; not illness, financial loss or national-security risk |
| `maximum_regret` | Largest difference from the best feasible option in each stated future | Conditional decision criterion, dependent on the chosen futures and objective |

The lessons specify each transformation beside its code. [Research alignment](research-alignment.md) explains where the teaching system stops and the proposed research programme begins.

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
