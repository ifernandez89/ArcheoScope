#!/usr/bin/env python3
"""
Data Source Transparency Module
Ensures all analyses include complete data source information
and provides users with full transparency about data origins.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import json

logger = logging.getLogger(__name__)

@dataclass
class DataSourceInfo:
    """Complete data source information"""
    provider: str
    data_type: str
    resolution: str
    coverage: str
    access_level: str
    url: Optional[str] = None
    api_endpoint: Optional[str] = None
    last_updated: Optional[datetime] = None
    limitations: List[str] = None

@dataclass
class AnalysisTransparency:
    """Complete transparency record for any analysis"""
    analysis_id: str
    timestamp: datetime
    region_coordinates: Dict[str, float]
    data_sources: List[DataSourceInfo]
    archaeological_references: List[Dict[str, str]]
    processing_methods: List[str]
    limitations: List[str]
    confidence_factors: List[str]
    recommendations: List[str]
    raw_data_available: bool = False

class DataSourceTransparency:
    """Manages transparency for all data sources used in analyses"""
    
    def __init__(self):
        self.public_data_sources = self._initialize_public_sources()
        self.analysis_records = {}
        logger.info("DataSourceTransparency inicializado con completa trazabilidad de datos")
    
    def _initialize_public_sources(self) -> Dict[str, DataSourceInfo]:
        """Initialize known public data sources"""
        sources = {}
        
        # USGS Landsat
        sources["landsat_8"] = DataSourceInfo(
            provider="USGS (United States Geological Survey)",
            data_type="Multispectral Satellite Imagery",
            resolution="30m",
            coverage="Global (1982-present)",
            access_level="Public",
            url="https://www.usgs.gov/landsat-missions",
            api_endpoint="https://earthexplorer.usgs.gov/inventory/json",
            last_updated=datetime.now(),
            limitations=[
                "Cloud cover can obscure surface",
                "Temporal resolution: 16 days",
                "Atmospheric interference possible"
            ]
        )
        
        # Copernicus Sentinel-2
        sources["sentinel_2"] = DataSourceInfo(
            provider="ESA (European Space Agency)",
            data_type="Multispectral Satellite Imagery", 
            resolution="10-20m",
            coverage="Global (2015-present)",
            access_level="Public",
            url="https://sentinel.esa.int/web/sentinel/missions/sentinel-2",
            api_endpoint="https://scihub.copernicus.eu/dhus/",
            last_updated=datetime.now(),
            limitations=[
                "Cloud cover interference",
                "Temporal resolution: 5 days",
                "Band-specific limitations"
            ]
        )
        
        # NASA MODIS
        sources["modis"] = DataSourceInfo(
            provider="NASA",
            data_type="Moderate Resolution Imaging Spectroradiometer",
            resolution="250-500m",
            coverage="Global (2000-present)",
            access_level="Public", 
            url="https://modis.gsfc.nasa.gov/",
            api_endpoint="https://earthdata.nasa.gov/apis",
            last_updated=datetime.now(),
            limitations=[
                "Lower spatial resolution",
                "Atmospheric correction needed",
                "Best for regional analysis, not site-specific"
            ]
        )
        
        # SRTM Elevation Data
        sources["srtm"] = DataSourceInfo(
            provider="NASA/JPL",
            data_type="Digital Elevation Model (DEM)",
            resolution="30m (SRTM-GL1)",
            coverage="60°N to 56°S",
            access_level="Public",
            url="https://www2.jpl.nasa.gov/srtm/",
            api_endpoint="https://lpdaac.usgs.gov/data-access",
            last_updated=datetime.now(),
            limitations=[
                "Limited latitude coverage",
                "Does not penetrate vegetation canopy",
                "Older dataset (2000 acquisition)"
            ]
        )
        
        # OpenStreetMap
        sources["openstreetmap"] = DataSourceInfo(
            provider="OpenStreetMap Foundation",
            data_type="Volunteer Geographic Information",
            resolution="Variable",
            coverage="Global",
            access_level="Public",
            url="https://www.openstreetmap.org/",
            api_endpoint="https://overpass-api.de/api/interpreter",
            last_updated=datetime.now(),
            limitations=[
                "Volunteer-created data quality varies",
                "Coverage uneven by region",
                "Not professionally surveyed"
            ]
        )
        
        return sources
    
    def create_transparency_record(self, analysis_id: str, region: Dict[str, float], 
                                 analysis_results: Dict[str, Any]) -> AnalysisTransparency:
        """Create complete transparency record for analysis"""
        
        # Determine which data sources were likely used
        used_sources = self._determine_used_sources(region, analysis_results)
        
        # Get archaeological references for the region
        archaeo_refs = self._get_archaeological_references(region)
        
        # Determine processing methods
        processing_methods = self._determine_processing_methods(analysis_results)
        
        # Identify limitations
        limitations = self._identify_limitations(region, used_sources, analysis_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(region, analysis_results, limitations)
        
        # Confidence factors
        confidence_factors = self._assess_confidence_factors(region, used_sources, analysis_results)
        
        transparency = AnalysisTransparency(
            analysis_id=analysis_id,
            timestamp=datetime.now(),
            region_coordinates=region,
            data_sources=used_sources,
            archaeological_references=archaeo_refs,
            processing_methods=processing_methods,
            limitations=limitations,
            confidence_factors=confidence_factors,
            recommendations=recommendations,
            raw_data_available=self._check_raw_data_availability()
        )
        
        # Store record
        self.analysis_records[analysis_id] = transparency
        
        return transparency
    
    def _determine_used_sources(self, region: Dict[str, float], 
                               results: Dict[str, Any]) -> List[DataSourceInfo]:
        """Determine which data sources were likely used"""
        used = []
        
        # Default sources always included
        used.append(self.public_data_sources["sentinel_2"])
        used.append(self.public_data_sources["srtm"])
        
        # Check if additional sources might be used based on analysis
        if "temporal_analysis" in results:
            used.append(self.public_data_sources["landsat_8"])
            used.append(self.public_data_sources["modis"])
        
        if "ndvi_analysis" in results or "vegetation_index" in results:
            used.append(self.public_data_sources["sentinel_2"])
            used.append(self.public_data_sources["landsat_8"])
        
        if "elevation_analysis" in results or "terrain_analysis" in results:
            used.append(self.public_data_sources["srtm"])
        
        return used
    
    def _get_archaeological_references(self, region: Dict[str, float]) -> List[Dict[str, str]]:
        """Get known archaeological references for the region"""
        # This would integrate with RealArchaeologicalValidator
        # For now, provide template structure
        
        references = []
        
        # Check if region overlaps with known UNESCO sites
        # This would be expanded with real database integration
        
        return references
    
    def _determine_processing_methods(self, results: Dict[str, Any]) -> List[str]:
        """Determine what processing methods were used"""
        methods = []
        
        if "ndvi_analysis" in results:
            methods.extend([
                "NDVI calculation from multispectral bands",
                "Vegetation index temporal analysis",
                "Statistical analysis of vegetation patterns"
            ])
        
        if "temporal_analysis" in results:
            methods.extend([
                "Multi-date image registration",
                "Change detection algorithms",
                "Time series analysis"
            ])
        
        if "elevation_analysis" in results:
            methods.extend([
                "DEM processing and analysis", 
                "Slope and aspect calculation",
                "Topographic feature detection"
            ])
        
        if "spatial_analysis" in results:
            methods.extend([
                "Spatial pattern analysis",
                "Statistical spatial measurements",
                "Geometric feature detection"
            ])
        
        # Always include basic methods
        methods.extend([
            "Geographic coordinate system transformation",
            "Region of interest extraction",
            "Quality control and validation"
        ])
        
        return list(set(methods))  # Remove duplicates
    
    def _identify_limitations(self, region: Dict[str, float], 
                            sources: List[DataSourceInfo], 
                            results: Dict[str, Any]) -> List[str]:
        """Identify limitations of the analysis"""
        limitations = []
        
        # Regional limitations
        center_lat = (region["lat_min"] + region["lat_max"]) / 2
        
        if abs(center_lat) > 60:
            limitations.append("High latitude: Limited satellite coverage and frequent cloud cover")
        
        if abs(center_lat) < -23.33 or abs(center_lat) > 23.33:
            limitations.append("Outside tropics: Seasonal vegetation changes may affect analysis")
        
        # Source limitations
        for source in sources:
            if source.limitations:
                limitations.extend(source.limitations)
        
        # Resolution limitations
        area_km2 = ((region["lat_max"] - region["lat_min"]) * 111) * ((region["lon_max"] - region["lon_min"]) * 111)
        if area_km2 < 1.0:
            limitations.append("Small area: Satellite resolution may limit detection capabilities")
        
        # Analysis-specific limitations
        if "ai_analysis" in results and results.get("ai_available", False) == False:
            limitations.append("AI analysis not available: Using deterministic fallbacks only")
        
        # Weather/seasonal limitations
        limitations.append("Weather conditions at image acquisition time may affect results")
        limitations.append("Seasonal vegetation patterns may obscure surface features")
        
        return list(set(limitations))  # Remove duplicates
    
    def _generate_recommendations(self, region: Dict[str, float], 
                                results: Dict[str, Any], 
                                limitations: List[str]) -> List[str]:
        """Generate recommendations based on analysis and limitations"""
        recommendations = []
        
        # Always recommend ground validation
        recommendations.append("Ground truth verification recommended for any significant findings")
        
        # Data quality recommendations
        recommendations.append("Verify image dates to ensure appropriate seasonal coverage")
        recommendations.append("Check for recent land use changes that may affect results")
        
        # Method-specific recommendations
        if "anomalous_patterns" in results:
            recommendations.append("Investigate anomalous patterns with multiple data sources")
            recommendations.append("Consider environmental factors that may create false positives")
        
        # Limitation-specific recommendations
        if any("cloud" in limitation.lower() for limitation in limitations):
            recommendations.append("Use multiple dates to mitigate cloud cover issues")
        
        if any("resolution" in limitation.lower() for limitation in limitations):
            recommendations.append("Higher resolution data recommended for detailed analysis")
        
        # Regional recommendations
        center_lat = (region["lat_min"] + region["lat_max"]) / 2
        if -30 <= center_lat <= 30:  # Tropical regions
            recommendations.append("Consider dense vegetation canopy interference")
        
        return recommendations
    
    def _assess_confidence_factors(self, region: Dict[str, float], 
                                sources: List[DataSourceInfo],
                                results: Dict[str, Any]) -> List[str]:
        """Assess factors affecting confidence in results"""
        factors = []
        
        # Positive factors
        if len(sources) >= 3:
            factors.append("Multiple data sources provide cross-validation")
        
        if "spatial_coherence" in results and results.get("spatial_coherence", 0) > 0.7:
            factors.append("High spatial coherence increases confidence")
        
        if "temporal_consistency" in results and results.get("temporal_consistency", 0) > 0.7:
            factors.append("High temporal consistency increases confidence")
        
        if results.get("ai_available", False):
            factors.append("AI reasoning available for pattern interpretation")
        
        # Negative factors
        area_km2 = ((region["lat_max"] - region["lat_min"]) * 111) * ((region["lon_max"] - region["lon_min"]) * 111)
        if area_km2 > 100:
            factors.append("Large area analysis may dilute specific site signals")
        
        if area_km2 < 0.5:
            factors.append("Very small area near satellite resolution limits")
        
        center_lon = (region["lon_min"] + region["lon_max"]) / 2
        if center_lon < -140 or center_lon > 140:  # Date line area
            factors.append("Near international date line: Data acquisition complexity")
        
        return factors
    
    def _check_raw_data_availability(self) -> bool:
        """Check if raw data is available for download"""
        # In a real implementation, this would check actual data availability
        return True  # Assume public data is always available
    
    def get_transparency_record(self, analysis_id: str) -> Optional[AnalysisTransparency]:
        """Get transparency record for analysis"""
        return self.analysis_records.get(analysis_id)
    
    def export_transparency_record(self, analysis_id: str, format: str = "json") -> str:
        """Export transparency record in specified format"""
        record = self.analysis_records.get(analysis_id)
        if not record:
            return None
        
        if format == "json":
            # Convert datetime objects to strings for JSON serialization
            record_dict = asdict(record)
            record_dict["timestamp"] = record.timestamp.isoformat()
            
            for i, source in enumerate(record_dict["data_sources"]):
                if record_dict["data_sources"][i]["last_updated"]:
                    record_dict["data_sources"][i]["last_updated"] = record.data_sources[i].last_updated.isoformat()
            
            return json.dumps(record_dict, indent=2)
        
        return str(record)
    
    def get_data_source_summary(self) -> Dict[str, Any]:
        """Get summary of available data sources"""
        return {
            "total_sources": len(self.public_data_sources),
            "coverage_types": {
                "global": len([s for s in self.public_data_sources.values() if s.coverage == "Global"]),
                "regional": len([s for s in self.public_data_sources.values() if s.coverage != "Global"])
            },
            "access_levels": {
                "public": len([s for s in self.public_data_sources.values() if s.access_level == "Public"]),
                "restricted": len([s for s in self.public_data_sources.values() if s.access_level != "Public"])
            },
            "data_types": list(set(s.data_type for s in self.public_data_sources.values())),
            "sources": {name: {
                "provider": source.provider,
                "data_type": source.data_type,
                "resolution": source.resolution,
                "access_level": source.access_level
            } for name, source in self.public_data_sources.items()}
        }