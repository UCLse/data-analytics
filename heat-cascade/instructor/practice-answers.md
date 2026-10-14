# Practice answers

Attempt each task before using these responses. These answers support self-study; assessment variants should be issued separately.

## 01. Python fundamentals through a heat example

The excesses are 0, 1.0 and 6.0 C. Raising the boundary lowers each positive excess and can move a value below the boundary. This is a property of the chosen rule, not evidence of changing exposure.

## 02. Reading and exploring tables with pandas

Four neighbourhoods meet the rule: Canal Quarter, Dockside, Market Ward and Station Quarter. Use an explicit filter, then save the result. A count of four refers to areas, not four people.

## 03. Cleaning measurements with a recorded audit

13 / 1,080 * 100 = approximately 1.20%. A zero would lower the average and conceal the missing measurement. Valid-reading counts differ between neighbourhoods, so the denominator must accompany the average.

## 04. Joining ecosystem, heat and vulnerability data

Dockside has the largest loss, -6.5 percentage points. The annual snapshot masks within-year change. Real work also requires the observation date, spatial support, collection method and whether that information existed at prediction time.

## 05. Exploration, visualisation and the cascade boundary

The valid-reading counts sum to 1,067. Brookside and Canal Quarter each have 90 valid readings; the other ten neighbourhoods have fewer. Fern Park has 88 and Station Quarter has 87. The interpretation must distinguish surface from air heat and association from causation.

## 06. A transparent teaching index and sensitivity check

The new component changes score levels and may change ranks. Its observed range is only 0.14 to 0.28, while deprivation spans 0.18 to 0.86. Equal mathematical weights therefore do not guarantee equal practical influence. State both the domain boundary and the observed spread.

## 07. Linear regression with a held-out neighbourhood test

Use `evaluation["absolute_error_c"] = evaluation["residual_c"].abs()` followed by a grouped mean. Report the three errors and the sample counts. A broader validation design would include spatial blocks, time-separated evaluation, multiple cities and checks of measurement compatibility. None is supplied by this single three-area holdout.

## 08. Decision trees, logistic regression and error trade-offs

Use the bottom-left matrix entry for false negatives. The procedure must specify the consequences of both errors, validate probabilities, choose a threshold using separate validation records and reserve a final test set. High recall alone cannot guarantee that the service can handle all flagged cases.

## 09. Exploratory neighbourhood profiles through clustering

Refit a scaler and K-means on the two chosen columns. Compare which neighbourhoods are grouped together, then explain any differences. Because these inputs covary strongly, a stable partition would not establish external validity. Stability across features, seeds and alternative samples is a further requirement.

## 10. Time series with chronological, one-day-ahead evaluation

The worst day is obtained from `(evaluation["surface_mean_c"] - evaluation["Lag regression"]).abs().idxmax()`. Yesterday's observed city mean, the mean seven days earlier and the target date are available at a one-day origin. Later observed means cannot be supplied to a seven-day fixed-origin forecast. A separate multi-horizon backtest is required.

## 11. Scenario comparison under deep uncertainty

The larger budget makes `Combined` feasible and it reduces burden most in every supplied future under the additive toy assumptions. This is conditional dominance within this model. Real canopy maturity, costs, maintenance, water demand and displaced investment could change it. An expected-value calculation would require defensible probabilities or a clearly declared decision convention.

## 12. Game telemetry, paired observations and text limitations

The incomplete-pair percentage is 1 / 36 * 100 = approximately 2.78%. A stronger evaluation needs a defined learning construct, reviewed items, planned repeated measurements, an appropriate comparison design, retention reporting and checks on practice effects. Actual participant collection also requires the institution's agreed consent, ethics and data-governance process.

## 13. An evidence-led Heat Cascade analytical brief

The capstone has no single correct neighbourhood ranking or policy recommendation. Strong work reproduces its calculations, describes the observation boundary, compares a meaningful baseline and evaluates how uncertainty changes the recommendation. The guided script creates starting artefacts; it does not complete the assessed brief.

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
