# ArcheoScope System Classification
## Official Declaration: Pre-Screening Scientific System

**Version**: 1.0  
**Date**: January 27, 2026  
**Status**: Production

---

## System Classification

ArcheoScope is officially classified as a **Pre-Screening Scientific System**, NOT a discovery engine.

### What ArcheoScope IS:

✅ **Pre-screening tool** for archaeological candidate identification  
✅ **Anomaly detection system** using multi-instrumental remote sensing  
✅ **Decision support system** for field archaeology prioritization  
✅ **Reproducible scientific pipeline** with full methodological transparency  
✅ **Negative evidence generator** for training and calibration  

### What ArcheoScope IS NOT:

❌ **NOT a discovery engine** - does not claim to "find" archaeological sites  
❌ **NOT an AI-based predictor** - uses deterministic mathematical methods  
❌ **NOT a replacement for field archaeology** - requires ground-truthing  
❌ **NOT a black box** - every decision is traceable and explainable  
❌ **NOT a final authority** - provides recommendations, not conclusions  

---

## Core Philosophy

> **"ArcheoScope does not seek to discover ruins. It seeks to not be wrong."**

This conservative approach prioritizes:
1. **False negative tolerance** over false positive avoidance
2. **Instrumental honesty** - explicit about coverage limitations
3. **Contextual awareness** - different thresholds for different environments
4. **Scientific rigor** - reproducible, deterministic, transparent

---

## System Outputs

### Primary Output Categories:

1. **Positive Candidates** (prob ≥ threshold)
   - `field_verification_priority` - High confidence, immediate action
   - `field_verification` - Standard verification recommended

2. **Uncertain Candidates** (0.30 < prob < threshold)
   - `monitoring_targeted` - Specific instruments required
   - `monitoring_passive` - Periodic observation
   - `instrument_upgrade_required` - Critical coverage gap ⭐

3. **Negative References** (prob ≤ 0.30)
   - `archive_scientific_negative` - Valuable for training
   - `discard_operational` - No scientific value

4. **Rejected** (anti-patterns detected)
   - `reject_natural_process` - Identified geological feature

### Decision Thresholds (Context-Aware):

| Environment | Threshold | Rationale |
|-------------|-----------|-----------|
| Desert | 0.45 | High visibility, low complexity |
| Semi-arid | 0.45 | Similar to desert |
| Default | 0.50 | Standard threshold |
| Forest | 0.52 | Medium-high complexity |
| Polar ice | 0.55 | High complexity, requires certainty |
| Glacier | 0.55 | Similar to polar |
| Shallow sea | 0.55 | High complexity, limited instruments |
| Deep ocean | 0.60 | Very high complexity |
| Known archaeological region | 0.45 | Historical context lowers threshold |

---

## Epistemic Transparency

Every analysis includes formal epistemic labeling:

```json
{
  "epistemic_mode": "deterministic_scientific",
  "ai_used": false,
  "ai_role": null,
  "reproducible": true,
  "method_transparency": "full"
}
```

### Epistemic Modes:

- **deterministic_scientific**: Pure mathematical pipeline (current default)
- **assistive_ai**: AI used for explanation only (optional)
- **hybrid**: Mixed deterministic + AI validation (future)

---

## Instrumental Coverage System

### Context-Aware Weighting:

Instruments are weighted by relevance to environment:

**Example - Marine Environment:**
- Multibeam sonar: 0.30 (critical)
- Side scan sonar: 0.25 (critical)
- Magnetometer: 0.20 (important)
- MODIS LST: 0.02 (minimal utility)

**Example - Terrestrial Environment:**
- Sentinel-1 SAR: 0.20 (critical)
- Sentinel-2 NDVI: 0.15 (important)
- MODIS LST: 0.10 (useful)

### Coverage Penalties:

| Effective Coverage | Penalty | Action |
|-------------------|---------|--------|
| < 30% | -20% | instrument_upgrade_required |
| 30-50% | -15% | targeted_reanalysis |
| 50-75% | -8% | monitoring recommended |
| > 75% | 0% | adequate coverage |

---

## Scientific Pipeline (7 Phases)

### FASE 0: Historical Data Enrichment
- Query database for previous measurements
- Aggregate by instrument
- Enrich current analysis

### FASE A: Normalization
- Z-score by instrument
- Local percentiles
- Environment-specific baselines

### FASE B: Pure Anomaly Detection
- Isolation Forest (simulated)
- Local Outlier Factor
- PCA residuals

### FASE C: Explicit Morphology
- Symmetry score
- Edge regularity
- Planarity
- Geomorphology inference (non-archaeological)

### FASE D: Anthropic Inference
- Weighted ensemble (40% anomaly, 40% morphology, 20% context)
- Contextual brakes (glacial, marine)
- Coverage penalties

### FASE E: Anti-Pattern Verification
- Volcanic cones
- Aeolian dunes
- Erosion patterns
- Karst formations

### FASE F: Known Sites Validation
- Query 80,512 documented archaeological sites
- Detect overlaps and rediscoveries
- Calculate distances to known sites

### FASE G: Scientific Output
- Apply context-aware thresholds
- Generate recommendations
- Assign epistemic labels

---

## Use Cases

### ✅ Appropriate Uses:

1. **Pre-screening large regions** before field campaigns
2. **Prioritizing field archaeology resources** based on probability
3. **Identifying instrument gaps** for specific regions
4. **Training negative reference datasets** for ML models
5. **Validating known sites** with multi-instrumental data
6. **Generating hypotheses** for archaeological investigation

### ❌ Inappropriate Uses:

1. **Claiming discoveries** without field verification
2. **Publishing coordinates** as "new archaeological sites"
3. **Replacing field archaeology** or expert judgment
4. **Making heritage decisions** based solely on system output
5. **Using in legal contexts** without ground-truthing
6. **Ignoring instrumental limitations** flagged by system

---

## Validation Strategy

### Positive Validation:
- Field verification of high-probability candidates
- Comparison with known archaeological sites
- Expert review of morphological indicators

### Negative Validation (Critical):
- **Document cases where system correctly rejected natural features**
- **Archive false positives for training**
- **Maintain negative reference database**

See: `ARCHEOSCOPE_NEGATIVE_CASES.md` for documented examples.

---

## Academic Positioning

### Suitable for Publication:

✅ **Methods papers** - Novel multi-instrumental pipeline  
✅ **Validation studies** - Comparison with known sites  
✅ **Negative evidence papers** - What the system correctly rejects  
✅ **Instrumental coverage studies** - Context-aware weighting  
✅ **Pre-screening methodology** - Decision support systems  

### NOT Suitable for Publication:

❌ **Discovery claims** - "New site found by ArcheoScope"  
❌ **Unverified candidates** - Without field confirmation  
❌ **Black box results** - Without methodological transparency  

---

## Legal and Ethical Considerations

### Disclaimers:

1. **No Guarantees**: System provides probabilities, not certainties
2. **Instrumental Limitations**: Explicitly flagged in every analysis
3. **Context Dependency**: Thresholds vary by environment
4. **Field Verification Required**: Ground-truthing is mandatory
5. **Heritage Protection**: Coordinates should be handled responsibly

### Recommended Citation:

```
ArcheoScope Pre-Screening System v1.0 (2026)
Multi-instrumental anomaly detection for archaeological candidate identification
Epistemic Mode: Deterministic Scientific
Reproducibility: Full methodological transparency
```

---

## System Maturity

**Current Status**: Production-ready for pre-screening

**Strengths**:
- Deterministic, reproducible pipeline
- Context-aware instrumental weighting
- Explicit epistemic labeling
- Negative evidence generation
- 80K+ known sites validation

**Limitations**:
- Marine instruments not available (sonar, magnetometer)
- No LiDAR for dense vegetation
- Limited to satellite-accessible regions
- Requires minimum instrumental coverage

**Future Enhancements**:
- FASE C2: Spatial persistence analysis (multi-resolution)
- Negative morphology scoring
- Expanded marine instrument integration
- Regional calibration datasets

---

## Conclusion

ArcheoScope is a **pre-screening scientific system** designed to:
1. Identify candidates requiring field verification
2. Prioritize archaeological resources efficiently
3. Generate negative evidence for training
4. Maintain full methodological transparency

It is **NOT** a discovery engine, AI predictor, or replacement for field archaeology.

**Core Principle**: *"Better to miss a site than to waste resources on false positives."*

This conservative, scientifically rigorous approach makes ArcheoScope:
- **Defendible** in academic contexts
- **Publishable** in peer-reviewed journals
- **Replicable** by independent researchers
- **Difficult to attack** methodologically

---

**Document Status**: Official System Classification  
**Approval**: System Architecture Team  
**Review Date**: January 27, 2026  
**Next Review**: January 2027
