# ArcheoScope: Open Framework for Structural Invariant Analysis (SII)
**Subject:** Open Documentation of Thresholds and Logic
**Version:** 1.0

---

## 1. THE SII PHILOSOPHY
The **Structural Invariant Index (SII)** is designed to be a peer-reviewed, reproducible metric for discriminating between natural geomorphology and high-intention structural remains.

## 2. METRIC THRESHOLDS (The Open Standard)
We release the following calibrated thresholds for the community to test and challenge:

| Component | Variable | Threshold | Critical Rejection Level |
| :--- | :--- | :--- | :--- |
| **Coherence** | $C_g$ | $0.915$ | $C_g < 0.85 \to$ Natural Entropy |
| **Persistence** | $P_s$ | $0.70$ | $P_s < 0.50 \to$ Superficial Erosion |
| **Intensity** | $I_a$ | $0.58$ | $I_a < 0.40 \to$ Homogeneous Substrate |
| **Modularity**| $M_d$ | $140$ | $M_d < 80 \to$ Patternless Formation |

## 3. LOGIC & DECISION FLOW
```python
def classify_site(metrics):
    # Calculated Index
    SII = (metrics.coh * metrics.per) + (metrics.ess * (metrics.hrm / 200.0))
    
    if SII > 0.90:
        return "HISA (High-Intention Structural Anomaly)"
    elif SII > 0.75:
        return "AMBIGUOUS / ERODED STRUCTURAL SIGNAL"
    else:
        return "GEOLOGICAL ENTROPY"
```

## 4. CHALLENGE PARAMETERS
We invite the community to find "Natural False Positives". 
- **Target:** Find a natural geological formation (no human intervention) that triggers an $SII > 0.90$.
- **Objective:** Refine the $I_a$ (Intensity) and $M_d$ (Modularity) weights to filter out natural regularities like columnar basalt or perfect sedimentary stratification.

---
**GitHub:** [ifernandez89/ArcheoScope](https://github.com/ifernandez89/ArcheoScope)
**Maintainer:** ArcheoScope Global Division
