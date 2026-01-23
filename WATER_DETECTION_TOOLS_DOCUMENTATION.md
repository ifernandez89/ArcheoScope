# ArcheoScope Water Detection Tools Documentation

## Overview

ArcheoScope includes specialized water detection and submarine archaeology capabilities that automatically detect when coordinates are over water and switch to maritime-specific instruments for underwater archaeological analysis.

## Core Components

### 1. WaterDetector Class (`backend/water/water_detector.py`)

**Purpose**: Automatically detects if coordinates are over water and characterizes the aquatic environment.

**Key Features**:
- Automatic water body detection (ocean, sea, lake, river, coastal, deep ocean)
- Depth estimation and salinity classification
- Archaeological potential assessment
- Historical shipping route correlation
- Known wreck site proximity detection
- Sediment type and current strength estimation

**Water Body Types Supported**:
- `OCEAN`: Open ocean waters
- `SEA`: Enclosed or semi-enclosed seas (Mediterranean, Black Sea, etc.)
- `LAKE`: Large freshwater bodies (Great Lakes, Caspian Sea)
- `RIVER`: Major river systems (Amazon, Nile, Mississippi)
- `COASTAL`: Shallow coastal waters
- `DEEP_OCEAN`: Deep oceanic waters (>200m depth)
- `SHALLOW_WATER`: Shallow waters (<50m depth)

**Detection Methods**:
```python
# Basic usage
water_detector = WaterDetector()
water_context = water_detector.detect_water_context(lat, lon)

# Returns WaterContext with:
# - is_water: bool
# - water_type: WaterBodyType
# - estimated_depth_m: float
# - salinity_type: str ("saltwater", "freshwater", "brackish")
# - archaeological_potential: str ("high", "medium", "low")
# - historical_shipping_routes: bool
# - known_wrecks_nearby: bool
# - sediment_type: str
# - current_strength: str
```

### 2. SubmarineArchaeologyEngine Class (`backend/water/submarine_archaeology.py`)

**Purpose**: Specialized archaeological analysis for underwater environments using maritime-specific instruments.

**Submarine Instruments**:
- `MULTIBEAM_SONAR`: High-resolution bathymetry mapping
- `SIDE_SCAN_SONAR`: Acoustic imaging of seafloor
- `SUB_BOTTOM_PROFILER`: Sediment layer analysis
- `MAGNETOMETER`: Detection of ferrous objects (metal hulls)
- `ACOUSTIC_REFLECTANCE`: Seafloor material classification
- `UNDERWATER_PHOTOGRAMMETRY`: Visual documentation (shallow water)
- `ROV_SURVEY`: Remote operated vehicle inspection

**Analysis Pipeline**:
1. **Instrument Selection**: Chooses appropriate tools based on water depth and type
2. **Volumetric Anomaly Detection**: Identifies potential wreck sites using sonar data
3. **Acoustic Signature Analysis**: Characterizes detected objects
4. **Historical Correlation**: Cross-references with shipping routes and known wrecks
5. **Wreck Classification**: Estimates vessel type, period, and preservation state
6. **Investigation Planning**: Generates detailed research recommendations

**Wreck Candidate Classification**:
```python
# Vessel types detected:
- passenger_liner (>200m, high aspect ratio)
- cargo_ship (50-200m, moderate aspect ratio)
- warship (>50m, low aspect ratio, high magnetic signature)
- fishing_vessel (20-50m)
- merchant_vessel (ancient/medieval trading ships)
- yacht/small_craft (<20m)

# Historical periods:
- ancient (low/no magnetic signature)
- medieval (minimal metal components)
- industrial (moderate magnetic signature)
- modern (high magnetic signature, steel construction)

# Preservation states:
- excellent (high geometric coherence, minimal burial)
- good (moderate coherence)
- poor (low coherence, significant degradation)
- debris_field (scattered remains)
```

### 3. Integration with Main Analysis Pipeline

The water detection is automatically integrated into the main ArcheoScope analysis:

```python
# In backend/api/main.py
water_detector = WaterDetector()
submarine_archaeology = SubmarineArchaeologyEngine()

# Automatic detection and switching
water_context = water_detector.detect_water_context(lat, lon)

if water_context.is_water:
    # Switch to submarine archaeology mode
    results = submarine_archaeology.analyze_submarine_area(water_context, bounds)
else:
    # Use terrestrial archaeology mode
    results = perform_terrestrial_analysis(...)
```

## Submarine Archaeology Workflow

### Phase 1: Detection
1. **Multibeam Sonar Survey**: Create high-resolution bathymetric map
2. **Side-scan Sonar**: Generate acoustic images of seafloor
3. **Anomaly Detection**: Identify geometric anomalies inconsistent with natural seafloor

### Phase 2: Characterization
1. **Sub-bottom Profiler**: Analyze sediment layers and buried objects
2. **Magnetometer Survey**: Detect ferrous materials (metal hulls, anchors, cannons)
3. **Acoustic Analysis**: Measure reflectance and backscatter properties

### Phase 3: Classification
1. **Dimensional Analysis**: Estimate vessel size and type from sonar shadows
2. **Magnetic Signature**: Determine construction materials and historical period
3. **Preservation Assessment**: Evaluate structural integrity and burial state

### Phase 4: Validation
1. **ROV Survey**: Visual inspection and photogrammetry (if accessible)
2. **Targeted Sampling**: Archaeological artifact recovery (if appropriate)
3. **Historical Research**: Cross-reference with maritime records

## Archaeological Applications

### Shipwreck Detection
- **Ancient Vessels**: Wood/ceramic construction, low magnetic signature
- **Medieval Ships**: Mixed construction, moderate metal components
- **Modern Wrecks**: Steel hulls, high magnetic signature, precise dating possible

### Submerged Settlements
- **Coastal Inundation**: Rising sea levels covering ancient sites
- **Lake/River Sites**: Seasonal flooding or dam construction
- **Tsunami Deposits**: Catastrophic burial events

### Maritime Infrastructure
- **Ancient Harbors**: Stone quays, breakwaters, anchorages
- **Underwater Causeways**: Connecting islands or crossing water
- **Fish Traps**: Stone or wooden fishing installations

## Technical Specifications

### Depth Capabilities
- **Shallow Water** (0-50m): Full instrument suite including photogrammetry
- **Medium Depth** (50-200m): Sonar and magnetometer primary tools
- **Deep Water** (>200m): Acoustic methods only, ROV surveys for validation

### Resolution Limits
- **Multibeam Sonar**: 0.1-1m resolution depending on depth
- **Side-scan Sonar**: 0.5-2m resolution, excellent for object detection
- **Magnetometer**: Detects ferrous objects >1m³ volume
- **Sub-bottom Profiler**: Penetrates 10-50m into sediment

### Environmental Considerations
- **Current Strength**: Affects survey patterns and ROV operations
- **Sediment Type**: Influences burial rates and preservation
- **Water Clarity**: Determines photogrammetry feasibility
- **Salinity**: Affects corrosion rates and preservation

## Data Products

### Bathymetric Maps
- High-resolution seafloor topography
- Anomaly highlighting and classification
- Depth contours and navigation hazards

### Acoustic Images
- Side-scan sonar mosaics
- Object identification and measurement
- Seafloor texture classification

### Magnetic Anomaly Maps
- Total magnetic field intensity
- Anomaly isolation and interpretation
- Ferrous object location and size estimation

### 3D Models
- Photogrammetric reconstructions (shallow water)
- Sonar-derived volumetric models
- Structural integrity assessments

## Quality Control

### Confidence Metrics
- **Detection Confidence**: Probability of actual archaeological target
- **Geometric Coherence**: Structural integrity and preservation
- **Historical Correlation**: Consistency with known maritime activity

### Validation Requirements
- **Independent Survey**: Multiple instrument confirmation
- **Historical Research**: Documentary evidence correlation
- **Expert Review**: Maritime archaeologist interpretation

### Uncertainty Quantification
- **Depth Estimation**: ±10-20% typical accuracy
- **Dimensional Measurements**: ±1-2m for large objects
- **Age Estimation**: Broad categories only without artifacts

## Limitations and Considerations

### Technical Limitations
- **Deep Water Access**: ROV surveys expensive and weather-dependent
- **Sediment Burial**: Objects may be completely buried and undetectable
- **Natural Mimics**: Geological features can resemble archaeological targets

### Environmental Factors
- **Dynamic Environment**: Currents, storms can move or bury objects
- **Biological Growth**: Marine organisms can obscure features
- **Human Activity**: Fishing, dredging, development impacts

### Legal and Ethical
- **Maritime Law**: Territorial waters and international regulations
- **Cultural Heritage**: Respect for maritime graves and cultural sites
- **Salvage Rights**: Complex legal frameworks for wreck ownership

## Future Enhancements

### Planned Improvements
- **AI-Enhanced Detection**: Machine learning for pattern recognition
- **Real-time Processing**: Onboard analysis during surveys
- **Multi-temporal Analysis**: Change detection over time
- **Predictive Modeling**: Wreck distribution probability maps

### Integration Opportunities
- **Satellite Bathymetry**: Large-scale seafloor mapping
- **AUV Surveys**: Autonomous underwater vehicle deployment
- **Crowdsourced Data**: Fishing vessel and recreational diver reports
- **Historical GIS**: Integration with maritime archaeological databases

---

*This documentation covers the current implementation of ArcheoScope's water detection and submarine archaeology capabilities. The system provides a comprehensive framework for maritime archaeological research while maintaining scientific rigor and uncertainty quantification.*