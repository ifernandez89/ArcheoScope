# Deep Analysis System - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DEEP ANALYSIS COMPLETE SYSTEM                        │
│                   run_deep_analysis_complete.py                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
        ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
        │   PHASE A     │ │   PHASE B     │ │  PHASES C&D   │
        │   Temporal    │ │     SAR       │ │  Multi-Scale  │
        └───────────────┘ └───────────────┘ └───────────────┘
                │               │               │       │
                ▼               ▼               ▼       ▼
        ┌───────────┐   ┌───────────┐   ┌───────┐ ┌────────┐
        │   MODIS   │   │ Sentinel-1│   │ICESat2│ │  TIMT  │
        │    LST    │   │    SAR    │   │ ATL06 │ │ Engine │
        └───────────┘   └───────────┘   └───────┘ └────────┘
```

## Phase A: Deep Temporal Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│              deep_temporal_analysis.py                          │
│                                                                 │
│  DeepTemporalAnalyzer                                          │
│    │                                                            │
│    ├─> analyze_thermal_phase_shift()                          │
│    │     │                                                      │
│    │     ├─> _get_daily_thermal_series()                      │
│    │     │     └─> MODISLSTConnector._estimate_lst()          │
│    │     │                                                      │
│    │     ├─> _calculate_phase_lag()                           │
│    │     │     └─> Cross-correlation analysis                 │
│    │     │                                                      │
│    │     ├─> _calculate_thermal_damping()                     │
│    │     │     └─> Variance analysis                          │
│    │     │                                                      │
│    │     ├─> _analyze_seasonal_extremes()                     │
│    │     │     └─> Summer/Winter stability                    │
│    │     │                                                      │
│    │     ├─> _detect_extreme_events()                         │
│    │     │     └─> 2-sigma anomaly detection                  │
│    │     │                                                      │
│    │     ├─> _analyze_post_event_recovery()                   │
│    │     │     └─> Baseline return time                       │
│    │     │                                                      │
│    │     └─> _calculate_thermal_inertia()                     │
│    │           └─> Integrated score (0-1)                     │
│    │                                                            │
│    └─> Output: Thermal Inertia Score + Interpretation         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Metrics:
  • Phase Lag (days)
  • Damping Factor (0-1)
  • Seasonal Stability (0-1)
  • Recovery Time (days)
  • Thermal Inertia Score (0-1)
```

## Phase B: Deep SAR Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│                deep_sar_analysis.py                             │
│                                                                 │
│  DeepSARAnalyzer                                               │
│    │                                                            │
│    ├─> analyze_sar_behavior()                                 │
│    │     │                                                      │
│    │     ├─> _get_sar_scenes()                                │
│    │     │     └─> PlanetaryComputerConnector.get_sar_data() │
│    │     │                                                      │
│    │     ├─> _analyze_polarization_divergence()               │
│    │     │     └─> VV/VH ratio analysis                       │
│    │     │                                                      │
│    │     ├─> _analyze_speckle_persistence()                   │
│    │     │     └─> Texture correlation                        │
│    │     │                                                      │
│    │     ├─> _calculate_phase_decorrelation_rate()            │
│    │     │     └─> Exponential decay model                    │
│    │     │                                                      │
│    │     ├─> _analyze_multi_angle_geometry()                  │
│    │     │     └─> Ascending vs Descending                    │
│    │     │                                                      │
│    │     ├─> _detect_stratification()                         │
│    │     │     └─> Layer estimation                           │
│    │     │                                                      │
│    │     └─> _calculate_sar_behavior_score()                  │
│    │           └─> Integrated score (0-1)                     │
│    │                                                            │
│    └─> Output: SAR Behavior Score + Interpretation            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Metrics:
  • VV/VH Ratio
  • Speckle Persistence (0-1)
  • Decorrelation Rate (1/day)
  • Rigidity Score (0-1)
  • Stratification Index (0-1)
  • SAR Behavior Score (0-1)
```

## Phase C: ICESat-2 Micro-adjustments

```
┌─────────────────────────────────────────────────────────────────┐
│            deep_multiscale_analysis.py                          │
│                                                                 │
│  ICESat2Analyzer                                               │
│    │                                                            │
│    ├─> analyze_vertical_microvariations()                     │
│    │     │                                                      │
│    │     ├─> ICESat2Connector.get_elevation_data()            │
│    │     │     └─> ATL06 product (Land Ice Height)            │
│    │     │                                                      │
│    │     ├─> Extract rugosity metrics                         │
│    │     │     ├─> elevation_std (rugosity)                   │
│    │     │     ├─> elevation_gradient                         │
│    │     │     └─> valid_points count                         │
│    │     │                                                      │
│    │     ├─> Analyze rigidity                                 │
│    │     │     └─> Rugosity > 5m = rigid anomaly              │
│    │     │                                                      │
│    │     └─> Calculate Rigidity Score                         │
│    │           └─> Based on rugosity thresholds               │
│    │                                                            │
│    └─> Output: Rigidity Score + Interpretation                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Metrics:
  • Rugosity (meters)
  • Elevation Gradient (meters)
  • Valid Points (count)
  • Rigidity Score (0-1)
  • Water Response Anomaly (bool)

Note: No coverage is NORMAL (orbital limitations)
```

## Phase D: Multi-Scale Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│            deep_multiscale_analysis.py                          │
│                                                                 │
│  MultiScaleAnalyzer                                            │
│    │                                                            │
│    ├─> analyze_scale_invariance()                             │
│    │     │                                                      │
│    │     ├─> For each scale: [50m, 100m, 250m, 500m]         │
│    │     │     │                                               │
│    │     │     └─> TerritorialInferentialTomographyEngine     │
│    │     │           └─> analyze_territory()                  │
│    │     │                 └─> RealDataIntegratorV2           │
│    │     │                       └─> ALL SENSORS              │
│    │     │                                                      │
│    │     ├─> Extract metrics per scale                        │
│    │     │     ├─> coherencia_3d                              │
│    │     │     ├─> tas_score                                  │
│    │     │     ├─> territorial_coherence                      │
│    │     │     └─> scientific_rigor                           │
│    │     │                                                      │
│    │     ├─> _analyze_scale_invariance()                      │
│    │     │     ├─> Calculate coherence decay rate             │
│    │     │     ├─> TAS stability                              │
│    │     │     └─> G1 stability                               │
│    │     │                                                      │
│    │     └─> Calculate Scale Invariance Score                 │
│    │           └─> High score = NO decay = ANOMALOUS          │
│    │                                                            │
│    └─> Output: Scale Invariance Score + Interpretation        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Metrics:
  • Coherence at 50m, 100m, 250m, 500m
  • Coherence Decay Rate (0-1)
  • TAS Stability (0-1)
  • G1 Stability (0-1)
  • Scale Invariance Score (0-1)

KEY PRINCIPLE:
  Natural formations → Lose coherence at lower scales
  Integrated masses → DO NOT lose coherence
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT                                    │
│                                                                 │
│  Zone Configuration:                                           │
│    • lat_min, lat_max                                          │
│    • lon_min, lon_max                                          │
│    • zone_name                                                 │
│    • priority                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA ACQUISITION                              │
│                                                                 │
│  Phase A: MODIS LST                                            │
│    └─> Daily thermal series (5 years)                         │
│                                                                 │
│  Phase B: Sentinel-1 SAR                                       │
│    └─> VV/VH backscatter (multiple scenes)                    │
│                                                                 │
│  Phase C: ICESat-2 ATL06                                       │
│    └─> Elevation points (if coverage)                         │
│                                                                 │
│  Phase D: All Sensors                                          │
│    └─> Complete TIMT analysis (4 scales)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PROCESSING                                 │
│                                                                 │
│  Phase A: Temporal Analysis                                    │
│    ├─> Phase lag calculation                                   │
│    ├─> Damping analysis                                        │
│    ├─> Seasonal extremes                                       │
│    ├─> Event detection                                         │
│    └─> Recovery analysis                                       │
│                                                                 │
│  Phase B: SAR Analysis                                         │
│    ├─> Polarization divergence                                 │
│    ├─> Speckle persistence                                     │
│    ├─> Phase decorrelation                                     │
│    ├─> Multi-angle geometry                                    │
│    └─> Stratification detection                                │
│                                                                 │
│  Phase C: ICESat-2 Analysis                                    │
│    ├─> Rugosity calculation                                    │
│    ├─> Gradient analysis                                       │
│    └─> Rigidity assessment                                     │
│                                                                 │
│  Phase D: Multi-Scale Analysis                                 │
│    ├─> Coherence at each scale                                 │
│    ├─> Decay rate calculation                                  │
│    └─> Invariance assessment                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       OUTPUT                                    │
│                                                                 │
│  JSON Report:                                                  │
│    {                                                            │
│      "zone": "Puerto Rico North",                              │
│      "duration_minutes": 45.2,                                 │
│      "phases": {                                               │
│        "phase_a_temporal": {                                   │
│          "thermal_inertia_score": 0.85,                        │
│          "interpretation": "..."                               │
│        },                                                       │
│        "phase_b_sar": {                                        │
│          "behavior_score": 0.92,                               │
│          "interpretation": "..."                               │
│        },                                                       │
│        "phase_c_icesat2": {                                    │
│          "rigidity_score": 0.80,                               │
│          "interpretation": "..."                               │
│        },                                                       │
│        "phase_d_multiscale": {                                 │
│          "invariance_score": 0.82,                             │
│          "interpretation": "..."                               │
│        }                                                        │
│      }                                                          │
│    }                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Score Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                  INTEGRATED ASSESSMENT                          │
│                                                                 │
│  IF:                                                            │
│    Thermal Inertia > 0.7                                       │
│    AND SAR Behavior > 0.8                                      │
│    AND Scale Invariance > 0.7                                  │
│                                                                 │
│  THEN:                                                          │
│    → ESTRUCTURA INTEGRADA MULTI-ESCALA                         │
│    → Masa térmica significativa                                │
│    → Rigidez estructural                                       │
│    → Invariancia de escala anómala                             │
│    → PRIORIDAD MÁXIMA para investigación                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Error Handling & Fallbacks

```
┌─────────────────────────────────────────────────────────────────┐
│                    FALLBACK STRATEGY                            │
│                                                                 │
│  Phase A: MODIS LST                                            │
│    Real Data → _estimate_lst() model                           │
│    Confidence: 0.85 → 0.60                                     │
│                                                                 │
│  Phase B: Sentinel-1                                           │
│    Real Data → Synthetic scenes based on real                  │
│    Confidence: 0.80 → 0.60                                     │
│                                                                 │
│  Phase C: ICESat-2                                             │
│    Real Data → "no_coverage" (NORMAL)                          │
│    Status: success → no_coverage                               │
│                                                                 │
│  Phase D: TIMT Engine                                          │
│    No fallback (uses all available sensors)                    │
│    Timeout: 5 minutes per scale                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Performance Characteristics

```
┌─────────────────────────────────────────────────────────────────┐
│                    TIMING BREAKDOWN                             │
│                                                                 │
│  Phase A: Temporal Analysis                                    │
│    • Data acquisition: 1-2 min                                 │
│    • Processing: 3-5 min                                       │
│    • Total: ~5-10 min                                          │
│                                                                 │
│  Phase B: SAR Analysis                                         │
│    • Data acquisition: 5-10 min (COG download)                 │
│    • Processing: 2-5 min                                       │
│    • Total: ~10-15 min                                         │
│                                                                 │
│  Phase C: ICESat-2 Analysis                                    │
│    • Data acquisition: 2-3 min                                 │
│    • Processing: 1-2 min                                       │
│    • Total: ~5 min                                             │
│                                                                 │
│  Phase D: Multi-Scale Analysis                                 │
│    • Per scale: 5-7 min                                        │
│    • 4 scales: 20-30 min                                       │
│    • Total: ~20-30 min                                         │
│                                                                 │
│  TOTAL (all phases): 40-60 minutes                             │
│  TOTAL (without Phase D): 20-30 minutes                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│                      DEPENDENCIES                               │
│                                                                 │
│  Python Packages:                                              │
│    • numpy (array operations)                                  │
│    • asyncio (async operations)                                │
│    • datetime (temporal analysis)                              │
│    • json (output formatting)                                  │
│                                                                 │
│  ArcheoScope Modules:                                          │
│    • satellite_connectors/modis_lst_connector                  │
│    • satellite_connectors/planetary_computer                   │
│    • satellite_connectors/icesat2_connector                    │
│    • territorial_inferential_tomography                        │
│    • real_data_integrator_v2                                   │
│                                                                 │
│  External APIs:                                                │
│    • NASA Earthdata (MODIS, ICESat-2)                         │
│    • Microsoft Planetary Computer (Sentinel-1)                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

**Architecture Version**: 1.0  
**Last Updated**: 2026-02-05  
**Status**: ✅ Fully Implemented
