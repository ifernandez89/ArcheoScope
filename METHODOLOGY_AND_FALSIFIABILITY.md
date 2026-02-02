# ArcheoScope Methodology: Detection of High-Intention Structural Anomalies
**Version:** 1.0 (Open Framework)
**Status:** Peer-Review Ready
**Focus:** Falsifiability and Geometric Invariants (No Cultural Bias)

---

## 1. ABSTRACT
This document formalizes the methodology for detecting **High-Intention Structural Anomalies (HISA)** using the Territorial Inferential Tomography (TIMT) engine. Unlike traditional remote sensing, which seeks cultural patterns, this framework identifies statistical deviations from geological entropy through four non-negotiable geometric invariants.

---

## 2. THE CORE METRICS (The SI Index)
The **Structural Invariant Index (SII)** is the mathematical core of the framework. It evaluates the probability that a spatial arrangement is the result of systemic planning rather than stochastic geological processes.

### 2.1 Metric Definitions
1.  **G1: Geo-Coherence ($C_g$):** A measure of long-range axial and cardinal alignment. Natural limits for layered geology $\approx 0.88$. Threshold for HISA $\ge 0.915$.
2.  **G2: Persistence ($P_s$):** The vertical continuity of a signal across inferred layers ($0-12m$). High values indicate structural shadows (foundations/drainage). Threshold $\ge 0.70$.
3.  **G3: Anomaly Intensity ($I_a$ / ESS):** The magnitude of lithological or thermal rupture compared to local background noise. Threshold $\ge 0.58$.
4.  **G4: Modularity ($M_d$ / HRM Peaks):** The repetition of discrete engineering units (modular language). Threshold $\ge 140$ peaks/km².

### 2.2 Decision Logic (SII Formula)
$$SII = (C_g \times P_s) + (I_a \times \frac{M_d}{200})$$

*   **SII > 0.90:** High-Intention Structural Anomaly (HISA) - Confirmed.
*   **0.75 < SII < 0.90:** Ambiguous/Eroded Anomaly - Further geophysical ground-truth needed.
*   **SII < 0.75:** Geological Baseline - Natural Entropy.

---

## 3. FALSIFIABILITY PROTOCOLS
To ensure scientific "survivability," the framework follows three strict rejection rules:

1.  **The Negative Baseline Rule:** If a null-site (e.g., Siberian Plateau, Antarctic Plains) produces an $SII > 0.90$, the specific instrument calibration is rejected as "too sensitive."
2.  **The Randomization Test:** Coordinates are offset by random jitter ($1-5km$). If the $SII$ does not drop by at least $30\%$, the signal is classified as a "Regional Geological Feature" rather than a "Localized Structural Anomaly."
3.  **The Lithological Bias Check:** Automatic detection of granite, basalt, and limestone baselines to prevent "Natural Geometric Peaks" (e.g., Giant's Causeway) from being flagged as HISA.

---

## 4. SCIENTIFIC TERMINOLOGY
To maintain academic rigor and avoid speculative bias, participants in the Open Framework MUST use the following terminology:

*   **DO NOT USE:** "Ancient advanced technology," "Lost civilization," "Planet-wide energy grid."
*   **USE:** "Convergent engineering solutions," "Systemic intentional footprint," "Extreme geometric order," "High-Intention Structural Anomaly."

---

## 5. OPEN SOURCE LOGIC
The logic for the SII calculation and the threshold values are released as `archeoscope_classifier_logic.json`. We invite geophysicists, data scientists, and archaeologists to apply this blind test to their own datasets.

---
**Persistent Data:** `global_statistical_mission.json`
**Methodology Custodian:** ArcheoScope TIMT Engine
**Role:** Architect of Inference Framework.
