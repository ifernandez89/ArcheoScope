# ArcheoScope Framework v2.0: Architectural & Instrumental Audit
**Date**: 2026-02-02
**Status**: ACTIVE / PRODUCTION
**Core Logic**: `(G1 AND G2) OR (G1 AND G4) OR (G2 AND G3)`

## 1. Scientific Architecture (TIMT Engine)
The **Territorial Inferential Multi-domain Tomography (TIMT)** has been upgraded to the 2.0 standard, enforcing a deterministic decision matrix based on Archeological Invariants.

### 1.1 The 3-Layer Flow
- **Layer 0 (TCP - Territorial Context Profile)**: Pre-measurement context. Establishes the Material Sensitivity Factor (MSF) based on geological lithology and climate.
- **Layer 1 (ETP - Environmental Tomographic Profile)**: Targeted acquisition of 15 instruments. Generates XZ/YZ tomographic slices to measure volumetric contrast (ESS).
- **Layer 2 (Formal Classification)**: Application of the Universal Classifier v2.0. Determines the final ontic status (Natural, Anthropic Stone, or Anthropic Soft Material).

## 2. Instrumental Strategy (15 Instruments)
The system integrates 15 distinct satellite and geospatial sensors, categorized by penetration depth:

| Instrument | Domain | Data Type | Archeological Relevance |
| :--- | :--- | :--- | :--- |
| **Sentinel-2** | Optical/SWIR | NDVI/Spectral | Surface vegetation anomalies (cropmarks) |
| **Sentinel-1 SAR** | Radar (C-Band) | Backscatter | Structural texture, buried volumes (de-speckled) |
| **Landsat 8/9** | Thermal/Optical | TIRS | Thermal inertia of buried structures |
| **ICESat-2** | Laser Altimetry | Photons | High-precision micro-topography (HRM) |
| **SRTM / NASADEM**| Radar | Elevation | Regional geomorphological context |
| **OpenTopography**| LiDAR/Hi-Res DEM| Elevation | Fine-grained geometric invariants (G1) |
| **MODIS** | Thermal | LST | Regional thermal stability patterns |
| **VIIRS** | Optical/Night | Night Lights/NDVI | Modern human interference vs. ancient patterns |
| **PALSAR-2** | Radar (L-Band) | Penetration | Deep sub-surface structure detection |
| **ERA5** | Climate | Reanalysis | Preservation potential / Paleohydrology |
| **CHIRPS** | Hydrology | Precipitation | Surface erosion and sediment dynamics |
| **Copernicus Marine**| Oceanographic | SST/Salinity | Context for coastal/submerged sites |
| **Global Lithology** | Geology | Discrete Map | MSF calculation (Base for AMB detection) |
| **Hydrographic Nets** | Hydrology | Vector Map | Settlement viability and paleochannels |
| **HRM Visualizer** | Artificial | Synthetic | High-resolution morphology peaks (G4) |

## 3. The MSF Revolution (Material Sensitivity Factor)
The system no longer treats all materials as equally persistent.
- **Stone (GCS > 0.9)**: MSF = 1.0. Requires high persistence (G2) for classification.
- **Soft Material (Adobe/Tierra Apisonada)**: MSF = 0.75. The system "rewards" detected persistence in degradable materials, allowing valid archaeological signatures to pass the G2 threshold even if eroded.

## 4. Formal Classifications
1. **NATURAL**: No significant correlation between invariants.
2. **ANTHROPIC_STONE**: High G1/G2/G3 in igneous/metamorphic contexts.
3. **AMB (Antrópico de Material Blando)**: Detected in sedimentary contexts with MSF correction. Priority: CRITICAL.
4. **UNKNOWN**: Insufficient instrumental coverage (< 30%).

---
**Audit performed by**: Antigravity AI
**System Version**: 2.0.0-clean
