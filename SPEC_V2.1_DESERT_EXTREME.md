# ArcheoScope v2.1 Specification: DESERT_EXTREME Strategy

**Target Environment:** Rub’ al Khali (Hyper-arid Sand Desert)
**Base Core:** v2.0 (Frozen)

---

## 1. Core Adjustments

### A. Dynamic Penalization ("The Dune Filter")
Unlike v2.0 which uses static masking, v2.1 will apply dynamic penalization based on texture covariance:
- **Active Dunes:** Detected via high variability in localized texture + wind direction alignment.
  - *Action:* `Signal_Strength *= 0.1` (Severe penalty)
- **Wind Noise:** High-frequency directional noise.
  - *Action:* Apply `Anisotropic Diffusion Filter` oriented perpendicular to prevailing wind.

### B. Signal Boosting ("The Hard-Ground Amplifier")
- **Hard Transitions:** Transition zones between Hamada (rocky desert) and Sand.
  - *Logic:* `Edge_Detection(Spectral_IR)`
  - *Action:* `Signal_Strength *= 2.5` (Strong Boost)
- **Micro-relief Stability:** Areas with low variance in elevation over small windows (<50m) but high local contrast.
  - *Action:* Flag as "Potential Anthropogenic Surface".

### C. Hydrological Focus ("The Water Tracer")
- **Buried Paleowadis:** Detection of subtle subterranean moisture traces or thermal inertia anomalies.
- **Fossil Basins:** Closed depressions with sedimentary signatures.

---

## 2. Detection Logic: `DESERT_EXTREME` Mode

```python
class DesertExtremeStrategy:
    def calculate_score(self, candidate, context):
        score = base_score(candidate)
        
        # 1. Texture Penalties
        if context.is_active_dune:
            score -= 0.8  # Kill signal
        
        # 2. Transition Bonus
        if context.is_hamada_sand_transition:
            score += 0.3  # High cultural probability zone
            
        # 3. Paleo-Hydro Lock
        if context.distance_to_fossil_basin < 1.0_km:
            score *= 1.5  # Multiplier effect
            
        return clamp(score, 0.0, 1.0)
```

## 3. Expected Outputs (New Artifacts)

1.  **Probability Heatmap:** A raster layer showing "Cultural Probability" vs "Geological Probability".
2.  **Corridor Identification:** Vector paths connecting high-probability clusters (Potential migration/trade routes).
3.  **Symbolic Nodes:** Clusters of PENDANT structures at key hydrological access points.

---

**Implementation Roadmap:**
1. Clone `GeoglyphDetector` to `RubAlKhaliDetector`.
2. Implement parameters defined above.
3. Run batch scan on defined sectors.
