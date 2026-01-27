#!/usr/bin/env python3
"""
ArcheoScope - Copernicus CDS Integration Module
Integrates Copernicus Climate Data Store with archaeological analysis.
"""

import os
import sys
import json
import tempfile
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import logging

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArcheoScopeCDSIntegration:
    """Integration class for Copernicus CDS data in archaeological analysis."""
    
    def __init__(self):
        """Initialize CDS integration."""
        self.cds_url = os.getenv("CDS_URL")
        self.cds_api_key = os.getenv("CDS_API_KEY")
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize CDS API client."""
        try:
            import cdsapi
            
            if not self.cds_url or not self.cds_api_key:
                raise ValueError("CDS_URL and CDS_API_KEY must be configured in .env file")
            
            self.client = cdsapi.Client(
                url=self.cds_url,
                key=self.cds_api_key,
                verify=True
            )
            
            logger.info("CDS client initialized successfully")
            
        except ImportError:
            logger.error("cdsapi not installed. Install with: pip install 'cdsapi>=0.7.7'")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize CDS client: {e}")
            raise
    
    def get_soil_moisture_data(self, 
                              lat_min: float, lat_max: float, 
                              lon_min: float, lon_max: float,
                              start_date: datetime, end_date: datetime,
                              output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve soil moisture data for archaeological analysis.
        
        Soil moisture can indicate:
        - Subsurface water retention patterns
        - Potential archaeological preservation conditions
        - Historical land use patterns
        - Seasonal variations affecting site visibility
        """
        
        logger.info(f"Requesting soil moisture data for area: {lat_min},{lon_min} to {lat_max},{lon_max}")
        
        try:
            # Format dates
            years = [str(year) for year in range(start_date.year, end_date.year + 1)]
            months = [f"{month:02d}" for month in range(start_date.month, end_date.month + 1)]
            
            # Prepare request
            dataset = 'satellite-soil-moisture'
            request = {
                'variable': 'volumetric_surface_soil_moisture',
                'type_of_sensor': 'passive',
                'type_of_record': 'cdr',
                'satellite': 'smos',
                'year': years,
                'month': months,
                'version': 'v202212.0.0',
                'area': [lat_max, lon_min, lat_min, lon_max],  # North, West, South, East
                'format': 'zip',
            }
            
            # Create output file
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"soil_moisture_{timestamp}.zip"
            
            logger.info("Submitting soil moisture data request...")
            result = self.client.retrieve(dataset, request, output_file)
            
            return {
                "success": True,
                "dataset": dataset,
                "output_file": output_file,
                "request_parameters": request,
                "archaeological_relevance": {
                    "preservation_conditions": "Soil moisture affects organic material preservation",
                    "site_visibility": "Dry conditions may enhance crop mark visibility",
                    "seasonal_patterns": "Moisture variations can reveal subsurface features",
                    "land_use_history": "Long-term moisture patterns indicate historical agriculture"
                }
            }
            
        except Exception as e:
            logger.error(f"Soil moisture data request failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "dataset": "satellite-soil-moisture"
            }
    
    def get_era5_climate_data(self,
                             lat_min: float, lat_max: float,
                             lon_min: float, lon_max: float,
                             start_date: datetime, end_date: datetime,
                             variables: List[str] = None,
                             output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve ERA5 reanalysis climate data for archaeological context.
        
        Climate data can provide:
        - Environmental context for archaeological sites
        - Seasonal patterns affecting remote sensing
        - Historical climate conditions
        - Precipitation patterns affecting soil conditions
        """
        
        if variables is None:
            variables = [
                '2m_temperature',
                'total_precipitation',
                'soil_temperature_level_1',
                'volumetric_soil_water_layer_1'
            ]
        
        logger.info(f"Requesting ERA5 climate data for area: {lat_min},{lon_min} to {lat_max},{lon_max}")
        
        try:
            # Format dates - use a safe date range
            safe_end_date = min(end_date, datetime.now() - timedelta(days=5))
            years = [str(year) for year in range(start_date.year, safe_end_date.year + 1)]
            months = [f"{month:02d}" for month in range(start_date.month, safe_end_date.month + 1)]
            
            # Prepare request
            dataset = 'reanalysis-era5-single-levels'
            request = {
                'product_type': 'reanalysis',
                'variable': variables,
                'year': years,
                'month': months,
                'day': ['01', '15'],  # Sample days to reduce data volume
                'time': ['00:00', '12:00'],
                'area': [lat_max, lon_min, lat_min, lon_max],  # North, West, South, East
                'format': 'netcdf',
            }
            
            # Create output file
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"era5_climate_{timestamp}.nc"
            
            logger.info("Submitting ERA5 climate data request...")
            result = self.client.retrieve(dataset, request, output_file)
            
            return {
                "success": True,
                "dataset": dataset,
                "output_file": output_file,
                "request_parameters": request,
                "variables": variables,
                "archaeological_relevance": {
                    "environmental_context": "Climate conditions during site occupation periods",
                    "preservation_factors": "Temperature and moisture affecting artifact preservation",
                    "seasonal_analysis": "Optimal timing for remote sensing surveys",
                    "historical_climate": "Long-term environmental changes affecting human settlement"
                }
            }
            
        except Exception as e:
            logger.error(f"ERA5 climate data request failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "dataset": "reanalysis-era5-single-levels"
            }
    
    def get_land_cover_data(self,
                           lat_min: float, lat_max: float,
                           lon_min: float, lon_max: float,
                           year: int,
                           output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve land cover data for archaeological landscape analysis.
        
        Land cover data provides:
        - Current vegetation patterns
        - Land use classification
        - Seasonal vegetation changes
        - Agricultural vs. natural areas
        """
        
        logger.info(f"Requesting land cover data for area: {lat_min},{lon_min} to {lat_max},{lon_max}")
        
        try:
            # Prepare request for satellite land cover
            dataset = 'satellite-land-cover'
            request = {
                'variable': 'all',
                'format': 'zip',
                'year': str(year),
                'version': 'v2.1.1',
            }
            
            # Create output file
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"land_cover_{year}_{timestamp}.zip"
            
            logger.info("Submitting land cover data request...")
            result = self.client.retrieve(dataset, request, output_file)
            
            return {
                "success": True,
                "dataset": dataset,
                "output_file": output_file,
                "request_parameters": request,
                "year": year,
                "archaeological_relevance": {
                    "landscape_context": "Understanding current land use around archaeological sites",
                    "vegetation_analysis": "Identifying areas with minimal modern disturbance",
                    "agricultural_impact": "Assessing potential damage from farming activities",
                    "preservation_zones": "Locating areas with natural vegetation protection"
                }
            }
            
        except Exception as e:
            logger.error(f"Land cover data request failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "dataset": "satellite-land-cover"
            }
    
    def analyze_archaeological_site_environment(self,
                                              site_name: str,
                                              lat_min: float, lat_max: float,
                                              lon_min: float, lon_max: float,
                                              analysis_year: int = 2023) -> Dict[str, Any]:
        """
        Comprehensive environmental analysis for an archaeological site.
        
        Combines multiple CDS datasets to provide archaeological context.
        """
        
        logger.info(f"Starting comprehensive environmental analysis for: {site_name}")
        
        results = {
            "site_name": site_name,
            "coordinates": {
                "lat_min": lat_min, "lat_max": lat_max,
                "lon_min": lon_min, "lon_max": lon_max
            },
            "analysis_year": analysis_year,
            "timestamp": datetime.now().isoformat(),
            "datasets": {}
        }
        
        # Define analysis period
        start_date = datetime(analysis_year, 1, 1)
        end_date = datetime(analysis_year, 12, 31)
        
        try:
            # 1. Climate context
            logger.info("Analyzing climate context...")
            climate_result = self.get_era5_climate_data(
                lat_min, lat_max, lon_min, lon_max,
                start_date, end_date
            )
            results["datasets"]["climate"] = climate_result
            
            # 2. Land cover analysis
            logger.info("Analyzing land cover...")
            land_cover_result = self.get_land_cover_data(
                lat_min, lat_max, lon_min, lon_max, analysis_year
            )
            results["datasets"]["land_cover"] = land_cover_result
            
            # 3. Soil moisture (if available)
            logger.info("Analyzing soil moisture...")
            soil_moisture_result = self.get_soil_moisture_data(
                lat_min, lat_max, lon_min, lon_max,
                start_date, end_date
            )
            results["datasets"]["soil_moisture"] = soil_moisture_result
            
            # Generate archaeological interpretation
            results["archaeological_interpretation"] = self._generate_archaeological_interpretation(results)
            
            # Save comprehensive report
            report_file = f"archaeological_environment_analysis_{site_name}_{analysis_year}.json"
            with open(report_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            results["report_file"] = report_file
            logger.info(f"Comprehensive analysis completed. Report saved to: {report_file}")
            
            return results
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            results["error"] = str(e)
            return results
    
    def _generate_archaeological_interpretation(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate archaeological interpretation of environmental data."""
        
        interpretation = {
            "site_preservation_factors": [],
            "optimal_survey_conditions": [],
            "environmental_challenges": [],
            "research_recommendations": []
        }
        
        # Analyze climate data results
        if analysis_results["datasets"].get("climate", {}).get("success"):
            interpretation["site_preservation_factors"].append(
                "Climate data available for understanding preservation conditions"
            )
            interpretation["optimal_survey_conditions"].append(
                "ERA5 data can identify optimal weather windows for remote sensing"
            )
        
        # Analyze land cover results
        if analysis_results["datasets"].get("land_cover", {}).get("success"):
            interpretation["research_recommendations"].append(
                "Use land cover data to identify areas of minimal modern disturbance"
            )
            interpretation["environmental_challenges"].append(
                "Current land use may impact archaeological site visibility"
            )
        
        # Analyze soil moisture results
        if analysis_results["datasets"].get("soil_moisture", {}).get("success"):
            interpretation["site_preservation_factors"].append(
                "Soil moisture patterns indicate subsurface preservation potential"
            )
            interpretation["optimal_survey_conditions"].append(
                "Soil moisture variations can enhance crop mark visibility"
            )
        
        # General recommendations
        interpretation["research_recommendations"].extend([
            "Correlate environmental data with archaeological survey results",
            "Use seasonal patterns to plan optimal survey timing",
            "Consider long-term environmental changes in site interpretation",
            "Integrate CDS data with high-resolution satellite imagery"
        ])
        
        return interpretation

def test_archaeological_site_analysis():
    """Test the CDS integration with a sample archaeological site."""
    
    print("🏛️  Testing ArcheoScope CDS Integration")
    print("=" * 60)
    
    try:
        # Initialize integration
        cds_integration = ArcheoScopeCDSIntegration()
        
        # Test with a small area around a known archaeological region
        # Using coordinates near Angkor, Cambodia as an example
        site_name = "test_archaeological_site"
        lat_min, lat_max = 13.4, 13.5  # Small area for testing
        lon_min, lon_max = 103.8, 103.9
        
        print(f"🔍 Testing environmental analysis for: {site_name}")
        print(f"📍 Coordinates: {lat_min},{lon_min} to {lat_max},{lon_max}")
        
        # Run comprehensive analysis
        results = cds_integration.analyze_archaeological_site_environment(
            site_name, lat_min, lat_max, lon_min, lon_max, 2023
        )
        
        # Display results
        print("\n📊 ANALYSIS RESULTS:")
        print("=" * 40)
        
        for dataset_name, dataset_result in results.get("datasets", {}).items():
            status = "✅ SUCCESS" if dataset_result.get("success") else "❌ FAILED"
            print(f"{dataset_name:15} {status}")
            
            if not dataset_result.get("success"):
                print(f"                Error: {dataset_result.get('error', 'Unknown error')}")
        
        # Show archaeological interpretation
        if "archaeological_interpretation" in results:
            print("\n🏛️  ARCHAEOLOGICAL INTERPRETATION:")
            interpretation = results["archaeological_interpretation"]
            
            if interpretation.get("site_preservation_factors"):
                print("\n🛡️  Preservation Factors:")
                for factor in interpretation["site_preservation_factors"]:
                    print(f"   • {factor}")
            
            if interpretation.get("research_recommendations"):
                print("\n💡 Research Recommendations:")
                for rec in interpretation["research_recommendations"]:
                    print(f"   • {rec}")
        
        if "report_file" in results:
            print(f"\n📁 Detailed report saved to: {results['report_file']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main function for testing CDS integration."""
    
    print("🚀 ArcheoScope - Copernicus CDS Integration")
    print("=" * 60)
    
    # Check if we should run the full test
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = test_archaeological_site_analysis()
        return success
    else:
        print("💡 CDS Integration module loaded successfully!")
        print("\nAvailable functions:")
        print("   • get_soil_moisture_data() - SMOS soil moisture for subsurface analysis")
        print("   • get_era5_climate_data() - Climate context for archaeological sites")
        print("   • get_land_cover_data() - Land use and vegetation analysis")
        print("   • analyze_archaeological_site_environment() - Comprehensive analysis")
        print("\n🧪 To run test: python archeoscope_cds_integration.py --test")
        print("\n📚 Integration ready for ArcheoScope archaeological analysis!")
        return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)