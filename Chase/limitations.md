# Limitations and Assumptions Analysis

## 1. DATA SPARSITY AND EXPERT JUDGMENT

**LIMITATION:** The Conditional Probability Distributions (CPDs) in this model are based on domain knowledge and reasonable assumptions rather than empirical data from actual Singapore MRT operations. This introduces subjective bias and potential inaccuracies.

**IMPACT:** Without real ridership data, station-level crowding measurements, or service disruption logs, the probability values may not accurately reflect true operational patterns. The model's predictions are only as good as the estimated probabilities.

**MITIGATION:** In a production system, CPDs should be learned from historical data using Maximum Likelihood Estimation or Bayesian Parameter Estimation with real-world observations of weather, service status, and crowding levels.

---

## 2. DISCRETIZATION OF CONTINUOUS VARIABLES

**LIMITATION:** Many real-world variables are continuous but have been discretized:
- Weather conditions reduced to 3 states (Clear/Rainy/Thunderstorms)
- Time reduced to 3 periods (Morning/Afternoon/Evening)
- Demand and Crowding reduced to 3 levels (Low/Medium/High)

**IMPACT:** This discretization loses granularity. For example, "Morning" encompasses both 6 AM and 11 AM which have very different commuting patterns. "Medium crowding" could represent a wide range of actual passenger densities.

**MITIGATION:** Could use finer discretization (e.g., hourly time bins) or hybrid models that incorporate continuous variables, though this increases model complexity and data requirements.

---

## 3. INDEPENDENCE ASSUMPTIONS

**LIMITATION:** The Bayesian Network structure assumes conditional independence between variables given their parents. For example:
- Weather and Service Status are modeled as independent, but severe weather could cause service disruptions
- Time and Day are independent, but weekend morning patterns differ from weekday mornings in ways not fully captured

**IMPACT:** The model may miss important correlations, potentially underestimating crowding in scenarios where multiple factors interact in complex ways.

**MITIGATION:** Additional edges could be added (Weather→Service, Time-Day interaction node), but this increases model complexity and requires more parameters to estimate.

---

## 4. SIMPLIFIED NETWORK REPRESENTATION

**LIMITATION:** The "Mode" variable (Today vs Future) is a binary simplification of complex network expansion projects. It doesn't capture:
- Partial completion stages during construction
- Specific route alternatives for different origin-destination pairs
- Capacity variations across different segments of new lines

**IMPACT:** The model provides aggregate capacity improvement estimates but cannot answer location-specific questions like "How does TEL affect crowding at Orchard station specifically?"

**MITIGATION:** A more detailed spatial model could represent individual stations and line segments, though this significantly increases complexity.

---

## 5. TEMPORAL DYNAMICS NOT CAPTURED

**LIMITATION:** This is a static Bayesian Network that represents a snapshot in time. It doesn't model:
- How crowding evolves throughout the day
- Queue buildup during disruptions
- Time-dependent passenger decision-making

**IMPACT:** Cannot predict how long crowding will persist or how it propagates through the network over time.

**MITIGATION:** Dynamic Bayesian Networks (DBNs) could model temporal evolution, but require significantly more complex inference algorithms.

---

## 6. MISSING VARIABLES AND EXTERNAL FACTORS

**LIMITATION:** Several important factors are not included:
- Special events (concerts, sporting events, festivals)
- School holidays vs. regular periods
- Economic factors affecting ridership patterns
- COVID-19 or pandemic-related behavioral changes
- Real-time train frequency adjustments

**IMPACT:** The model cannot account for exceptional circumstances that deviate from typical patterns.

**MITIGATION:** Additional parent nodes could be added for these factors, though each increases the size of child CPD tables exponentially.

---

## 7. HOMOGENEOUS DEMAND ASSUMPTION

**LIMITATION:** The Demand variable represents overall system demand without distinguishing between:
- Direction of travel (inbound vs. outbound)
- Specific corridors (North-South vs. East-West)
- Different types of trips (commute vs. leisure)

**IMPACT:** Crowding is actually highly directional and location-specific, which this aggregate model cannot capture.

**MITIGATION:** A hierarchical model with corridor-specific demand nodes would be more accurate but substantially more complex.

---

## 8. CPD TABLE SIZE EXPLOSION

**LIMITATION:** The Crowding variable depends on 3 parents (Demand, Service, Mode) with cardinalities 3×3×2, requiring 18 probability values per crowding state (54 total). Adding more parents or increasing cardinalities causes exponential growth.

**IMPACT:** Limits the number of factors that can be considered and makes parameter estimation from data increasingly difficult with sparse observations.

**MITIGATION:** Techniques like noisy-OR/noisy-MAX gates, or parameter tying can reduce the number of parameters, though with some loss of expressiveness.

---

## 9. VALIDATION CHALLENGES

**LIMITATION:** Without ground truth data, we cannot validate whether the model's predictions match reality. The probabilities appear reasonable but are unverified.

**IMPACT:** Unknown accuracy of predictions; risk of overconfidence in model outputs.

**MITIGATION:** Model should be validated against held-out real-world data, with performance metrics like log-likelihood, classification accuracy, or calibration curves.

---

## 10. FUTURE MODE ASSUMPTIONS

**LIMITATION:** The Future Mode CPDs assume that TELe and CRL will reduce crowding according to our estimated capacity improvements. This assumes:
- Lines open on schedule
- Expected ridership distribution materializes
- No induced demand from improved service (Jevons paradox)

**IMPACT:** Actual outcomes may differ if network expansion induces more travel or if implementation differs from plans.

**MITIGATION:** Sensitivity analysis on Future Mode parameters, and regular model updates as actual post-expansion data becomes available.

---

## CONCLUSION

This Bayesian Network provides a reasonable framework for reasoning about MRT crowding under uncertainty, but should be viewed as a **simplified prototype** rather than a production-ready forecasting tool. 

### Its primary value is in:
- Demonstrating probabilistic reasoning about transport systems
- Comparing relative outcomes between scenarios
- Identifying key factors influencing crowding
- Supporting qualitative decision-making

### For operational deployment, the model would require:
- Parameter learning from real operational data
- Validation against ground truth observations
- Finer spatial and temporal granularity
- Integration with real-time data feeds
- Regular recalibration as conditions change
