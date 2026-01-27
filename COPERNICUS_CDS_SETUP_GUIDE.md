# Copernicus CDS Integration for ArcheoScope

## Overview

The Copernicus Climate Data Store (CDS) provides valuable environmental data for archaeological analysis, including soil moisture, climate patterns, and land cover information that can enhance remote sensing archaeological surveys.

## Setup Complete ✅

Your ArcheoScope installation is now configured with Copernicus CDS integration:

- **CDS API Key**: Configured in `.env` file
- **Authentication**: ✅ Working
- **Client Library**: ✅ Installed (`cdsapi>=0.7.7`)
- **Configuration File**: ✅ Created (`~/.cdsapirc`)

## Available Datasets for Archaeological Applications

### 1. SMOS Soil Moisture Data
- **Dataset**: `satellite-soil-moisture`
- **Archaeological Value**: 
  - Subsurface water retention patterns
  - Archaeological preservation conditions
  - Seasonal variations affecting site visibility
  - Historical land use patterns

### 2. ERA5 Climate Reanalysis
- **Dataset**: `reanalysis-era5-single-levels`
- **Archaeological Value**:
  - Environmental context for archaeological sites
  - Optimal timing for remote sensing surveys
  - Historical climate conditions
  - Precipitation patterns affecting soil conditions

### 3. Land Cover Data
- **Dataset**: `satellite-land-cover`
- **Archaeological Value**:
  - Current vegetation patterns around sites
  - Land use classification
  - Agricultural vs. natural areas
  - Areas with minimal modern disturbance

## Usage Examples

### Basic Authentication Test
```bash
python test_cds_auth_only.py
```

### Comprehensive Integration Test
```bash
python archeoscope_cds_integration.py --test
```

### Using in ArcheoScope Analysis
```python
from archeoscope_cds_integration import ArcheoScopeCDSIntegration

# Initialize CDS integration
cds = ArcheoScopeCDSIntegration()

# Analyze archaeological site environment
results = cds.analyze_archaeological_site_environment(
    site_name="My_Archaeological_Site",
    lat_min=40.0, lat_max=40.1,
    lon_min=-3.0, lon_max=-2.9,
    analysis_year=2023
)
```

## Integration with ArcheoScope Workflow

### 1. Site Discovery Phase
- Use ERA5 climate data to understand seasonal patterns
- Identify optimal weather windows for satellite imagery acquisition
- Analyze historical climate conditions for site context

### 2. Environmental Context
- Retrieve soil moisture data to assess preservation conditions
- Analyze land cover to identify areas of minimal disturbance
- Understand current land use around archaeological sites

### 3. Survey Planning
- Use climate data to plan optimal survey timing
- Correlate soil moisture patterns with crop mark visibility
- Identify seasonal variations that enhance archaeological features

### 4. Site Interpretation
- Provide environmental context for archaeological findings
- Understand long-term environmental changes
- Assess preservation potential based on soil conditions

## Dataset Terms of Use

**Important**: Before downloading data from any CDS dataset, you must:

1. **Register** at: https://cds.climate.copernicus.eu/user/register
2. **Login** to your account
3. **Accept Terms of Use** for each dataset you want to use
4. Visit the dataset page and scroll to the bottom of the download form
5. Click "Accept Terms" before making API requests

### Key Datasets to Accept:
- ERA5 Reanalysis: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
- Soil Moisture: https://cds.climate.copernicus.eu/datasets/satellite-soil-moisture
- Land Cover: https://cds.climate.copernicus.eu/datasets/satellite-land-cover

## File Structure

```
ArcheoScope/
├── .env                              # CDS API configuration
├── ~/.cdsapirc                       # CDS client configuration
├── test_cds_auth_only.py            # Authentication test
├── archeoscope_cds_integration.py   # Main integration module
├── COPERNICUS_CDS_SETUP_GUIDE.md   # This guide
└── requirements-cds.txt             # CDS dependencies
```

## Troubleshooting

### Authentication Issues
- Verify your API key at: https://cds.climate.copernicus.eu/user/login
- Check that your account is active
- Ensure you've accepted terms of use for datasets

### Data Request Failures
- **"None of the data you have requested is available yet"**: Request older dates (ERA5 has ~5 day delay)
- **"Invalid request"**: Check dataset documentation for valid parameters
- **"Unauthorized"**: Accept terms of use for the specific dataset

### Network Issues
- Check internet connectivity
- Verify firewall settings allow HTTPS to `cds.climate.copernicus.eu`
- Try requests during off-peak hours (CDS can be busy)

## Performance Considerations

### Data Volume
- Start with small geographic areas for testing
- Use date ranges appropriate for your analysis needs
- Consider data processing requirements for large downloads

### Request Timing
- CDS requests can take several minutes to hours
- Plan for asynchronous processing in ArcheoScope
- Implement proper timeout handling

### Caching Strategy
- Cache downloaded data locally
- Reuse data for multiple archaeological analyses
- Implement data versioning for reproducibility

## Archaeological Applications

### Crop Mark Enhancement
```python
# Get soil moisture data for crop mark analysis
soil_data = cds.get_soil_moisture_data(
    lat_min, lat_max, lon_min, lon_max,
    start_date, end_date
)
# Correlate with satellite imagery for enhanced detection
```

### Seasonal Survey Planning
```python
# Get climate data for optimal survey timing
climate_data = cds.get_era5_climate_data(
    lat_min, lat_max, lon_min, lon_max,
    start_date, end_date,
    variables=['2m_temperature', 'total_precipitation']
)
# Identify dry periods optimal for aerial survey
```

### Site Preservation Assessment
```python
# Comprehensive environmental analysis
analysis = cds.analyze_archaeological_site_environment(
    "Site_Name", lat_min, lat_max, lon_min, lon_max, 2023
)
# Use results to assess preservation conditions
```

## Next Steps

1. **Accept Dataset Terms**: Visit CDS website and accept terms for datasets you need
2. **Test Integration**: Run the test scripts to verify functionality
3. **Integrate with ArcheoScope**: Add CDS data to your archaeological analysis workflow
4. **Develop Workflows**: Create specific analysis pipelines combining CDS data with satellite imagery
5. **Document Results**: Use CDS data to provide environmental context in archaeological reports

## Support

- **CDS Documentation**: https://cds.climate.copernicus.eu/how-to-api
- **Dataset Catalog**: https://cds.climate.copernicus.eu/datasets
- **API Reference**: https://cds.climate.copernicus.eu/api-how-to
- **ArcheoScope Integration**: See `archeoscope_cds_integration.py` for examples

---

**Status**: ✅ **CDS Integration Ready for Archaeological Analysis**

Your ArcheoScope installation can now access Copernicus environmental data to enhance archaeological remote sensing capabilities!