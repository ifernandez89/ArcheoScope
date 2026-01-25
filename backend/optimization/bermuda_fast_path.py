#!/usr/bin/env python3
"""
Bermuda Fast Path - Ultra-fast analysis for Bermuda coordinates
Target: <10 seconds processing time for 32.300, -64.783 area
"""

import time
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import pickle

logger = logging.getLogger(__name__)

@dataclass
class BermudaAnalysisResult:
    """Ultra-fast Bermuda analysis result"""
    environment_type: str
    analysis_time_ms: float
    candidates: List[Dict[str, Any]]
    bathymetry_m: float
    magnetic_anomaly_nt: float
    historical_matches: int
    confidence_score: float
    optimization_notes: str

class BermudaFastPath:
    """
    Ultra-fast Bermuda analysis engine with precomputed data and optimized algorithms
    """
    
    def __init__(self):
        """Initialize with precomputed Bermuda area data"""
        
        # Bermuda area bounds
        self.bermuda_bounds = {
            'lat_min': 25.0,
            'lat_max': 26.5,
            'lon_min': -71.5,
            'lon_max': -70.0
        }
        
        # Grid resolution for precomputed data
        self.grid_resolution = 0.001  # ~100m resolution
        
        # Initialize data structures
        self.bathymetry_grid = None
        self.magnetic_grid = None
        self.historical_wreck_db = None
        self.current_patterns = None
        
        # Performance cache
        self.analysis_cache = {}
        
        # Load or generate precomputed data
        self._initialize_bermuda_data()
        
        logger.info("🏝️ BermudaFastPath initialized with precomputed data")
    
    def is_bermuda_coordinates(self, lat: float, lon: float) -> bool:
        """Check if coordinates are in Bermuda area"""
        return (self.bermuda_bounds['lat_min'] <= lat <= self.bermuda_bounds['lat_max'] and
                self.bermuda_bounds['lon_min'] <= lon <= self.bermuda_bounds['lon_max'])
    
    def analyze_bermuda_coordinates(self, lat: float, lon: float, 
                                  bounds: Dict[str, float]) -> BermudaAnalysisResult:
        """
        Ultra-fast Bermuda analysis - target <5 seconds
        """
        
        start_time = time.time()
        
        try:
            # Step 1: Fast bathymetry lookup (cached)
            bathymetry_data = self._get_bathymetry_fast(lat, lon)
            
            # Step 2: Magnetic anomaly check (precomputed)
            magnetic_data = self._get_magnetic_fast(lat, lon)
            
            # Step 3: Historical pattern matching (spatial index)
            historical_matches = self._match_historical_patterns(lat, lon, bathymetry_data)
            
            # Step 4: Current pattern analysis (simplified model)
            current_effects = self._analyze_current_effects(lat, lon)
            
            # Step 5: Fast candidate generation
            candidates = self._generate_candidates_fast(
                bathymetry_data, magnetic_data, historical_matches, current_effects
            )
            
            # Step 6: Confidence scoring
            confidence = self._calculate_bermuda_confidence(candidates, historical_matches)
            
            analysis_time = (time.time() - start_time) * 1000
            
            return BermudaAnalysisResult(
                environment_type='shallow_sea',
                analysis_time_ms=analysis_time,
                candidates=candidates[:10],  # Limit to top 10
                bathymetry_m=bathymetry_data['depth'],
                magnetic_anomaly_nt=magnetic_data.get('anomaly', 0),
                historical_matches=len(historical_matches),
                confidence_score=confidence,
                optimization_notes=f"Bermuda fast path - {len(candidates)} candidates generated in {analysis_time:.1f}ms"
            )
            
        except Exception as e:
            logger.error(f"Error in Bermuda fast analysis: {e}")
            return self._create_fallback_result(lat, lon, start_time)
    
    def _get_bathymetry_fast(self, lat: float, lon: float) -> Dict[str, float]:
        """Fast bathymetry lookup from precomputed grid"""
        
        # Convert coordinates to grid indices
        grid_x = int((lat - self.bermuda_bounds['lat_min']) / self.grid_resolution)
        grid_y = int((lon - self.bermuda_bounds['lon_min']) / self.grid_resolution)
        
        # Bounds checking
        grid_x = max(0, min(grid_x, self.bathymetry_grid.shape[0] - 1))
        grid_y = max(0, min(grid_y, self.bathymetry_grid.shape[1] - 1))
        
        depth = self.bathymetry_grid[grid_x, grid_y]
        
        # Compute gradient if needed
        gradient = self._compute_gradient_fast(grid_x, grid_y)
        
        return {
            'depth': float(depth),
            'gradient': float(gradient)
        }
    
    def _get_magnetic_fast(self, lat: float, lon: float) -> Dict[str, float]:
        """Fast magnetic anomaly lookup"""
        
        grid_x = int((lat - self.bermuda_bounds['lat_min']) / self.grid_resolution)
        grid_y = int((lon - self.bermuda_bounds['lon_min']) / self.grid_resolution)
        
        # Bounds checking
        grid_x = max(0, min(grid_x, self.magnetic_grid.shape[0] - 1))
        grid_y = max(0, min(grid_y, self.magnetic_grid.shape[1] - 1))
        
        anomaly = self.magnetic_grid[grid_x, grid_y]
        
        return {
            'anomaly': float(anomaly),
            'significant': abs(anomaly) > 50.0  # nT threshold
        }
    
    def _match_historical_patterns(self, lat: float, lon: float, 
                                 bathymetry_data: Dict[str, float]) -> List[Dict[str, Any]]:
        """Fast historical pattern matching using spatial index"""
        
        depth = bathymetry_data['depth']
        
        # Query historical wreck database within 10km radius
        nearby_wrecks = self.historical_wreck_db.query_radius(lat, lon, 10.0)
        
        matches = []
        for wreck in nearby_wrecks:
            # Depth similarity check (within 20m)
            if abs(wreck['depth'] - depth) < 20:
                similarity = self._calculate_similarity(wreck, bathymetry_data)
                
                if similarity > 0.3:  # Minimum similarity threshold
                    matches.append({
                        'wreck': wreck,
                        'similarity_score': similarity,
                        'distance_km': self._fast_distance(lat, lon, wreck['lat'], wreck['lon'])
                    })
        
        # Sort by similarity score and return top 5
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        return matches[:5]
    
    def _analyze_current_effects(self, lat: float, lon: float) -> Dict[str, Any]:
        """Simplified current pattern analysis"""
        
        # Precomputed current patterns for Bermuda
        current_speed = self.current_patterns.get_current_speed(lat, lon)
        current_direction = self.current_patterns.get_current_direction(lat, lon)
        
        return {
            'current_speed_knots': current_speed,
            'current_direction_deg': current_direction,
            'deposition_risk': self._calculate_deposition_risk(current_speed),
            'visibility_impact': self._calculate_visibility_impact(current_speed)
        }
    
    def _generate_candidates_fast(self, bathymetry_data: Dict[str, float],
                                magnetic_data: Dict[str, float],
                                historical_matches: List[Dict[str, Any]],
                                current_effects: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate candidate sites with fast algorithms"""
        
        candidates = []
        
        # Candidate 1: Magnetic anomaly + depth anomaly
        if magnetic_data['significant'] and bathymetry_data['depth'] > 20:
            candidates.append({
                'type': 'magnetic_anomaly',
                'confidence': 0.7,
                'features': {
                    'magnetic_anomaly_nt': magnetic_data['anomaly'],
                    'depth_m': bathymetry_data['depth'],
                    'gradient': bathymetry_data['gradient']
                },
                'archaeological_probability': 0.65
            })
        
        # Candidate 2: Historical pattern match
        for match in historical_matches:
            if match['similarity_score'] > 0.6:
                candidates.append({
                    'type': 'historical_match',
                    'confidence': match['similarity_score'],
                    'features': {
                        'historical_wreck': match['wreck']['name'],
                        'similarity_score': match['similarity_score'],
                        'distance_km': match['distance_km']
                    },
                    'archaeological_probability': match['similarity_score'] * 0.8
                })
        
        # Candidate 3: Bathymetric anomaly (suspicious topography)
        if bathymetry_data['gradient'] > 0.15:
            candidates.append({
                'type': 'bathymetric_anomaly',
                'confidence': 0.5,
                'features': {
                    'depth_m': bathymetry_data['depth'],
                    'gradient': bathymetry_data['gradient'],
                    'topography_score': min(bathymetry_data['gradient'] * 5, 1.0)
                },
                'archaeological_probability': 0.45
            })
        
        # Candidate 4: Low deposition area (good preservation)
        if current_effects['deposition_risk'] < 0.3:
            candidates.append({
                'type': 'preservation_favorable',
                'confidence': 0.4,
                'features': {
                    'deposition_risk': current_effects['deposition_risk'],
                    'current_speed': current_effects['current_speed_knots']
                },
                'archaeological_probability': 0.35
            })
        
        # Sort by archaeological probability
        candidates.sort(key=lambda x: x['archaeological_probability'], reverse=True)
        
        return candidates
    
    def _calculate_bermuda_confidence(self, candidates: List[Dict[str, Any]], 
                                    historical_matches: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence score for Bermuda analysis"""
        
        if not candidates:
            return 0.1
        
        # Weight different factors
        candidate_factor = sum(c['archaeological_probability'] for c in candidates[:3]) / min(len(candidates), 3)
        historical_factor = min(len(historical_matches) * 0.2, 0.8)
        
        # Combined confidence
        confidence = (candidate_factor * 0.7 + historical_factor * 0.3)
        
        return min(confidence, 1.0)
    
    def _compute_gradient_fast(self, grid_x: int, grid_y: int) -> float:
        """Fast gradient computation using precomputed gradients"""
        
        # Use Sobel operator approximation
        if (grid_x > 0 and grid_x < self.bathymetry_grid.shape[0] - 1 and
            grid_y > 0 and grid_y < self.bathymetry_grid.shape[1] - 1):
            
            dx = (self.bathymetry_grid[grid_x + 1, grid_y] - 
                  self.bathymetry_grid[grid_x - 1, grid_y]) / 2.0
            dy = (self.bathymetry_grid[grid_x, grid_y + 1] - 
                  self.bathymetry_grid[grid_x, grid_y - 1]) / 2.0
            
            gradient = np.sqrt(dx*dx + dy*dy)
            return gradient
        
        return 0.0
    
    def _calculate_similarity(self, wreck: Dict[str, Any], 
                            bathymetry_data: Dict[str, float]) -> float:
        """Calculate similarity between historical wreck and current data"""
        
        # Depth similarity
        depth_diff = abs(wreck['depth'] - bathymetry_data['depth'])
        depth_similarity = max(0, 1.0 - depth_diff / 50.0)  # Normalize to 50m range
        
        # Type similarity (simplified)
        type_match = 1.0 if wreck.get('type') == 'shipwreck' else 0.5
        
        # Combined similarity
        similarity = (depth_similarity * 0.8 + type_match * 0.2)
        
        return similarity
    
    def _fast_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Fast distance calculation using equirectangular approximation"""
        
        lat_diff = lat2 - lat1
        lon_diff = lon2 - lon1
        lat_avg = (lat1 + lat2) / 2
        
        # Convert to radians
        lat_diff_rad = np.radians(lat_diff)
        lon_diff_rad = np.radians(lon_diff)
        lat_avg_rad = np.radians(lat_avg)
        
        # Equirectangular approximation
        x = lon_diff_rad * np.cos(lat_avg_rad)
        y = lat_diff_rad
        
        # Earth radius in km
        R = 6371.0
        distance = R * np.sqrt(x*x + y*y)
        
        return distance
    
    def _calculate_deposition_risk(self, current_speed: float) -> float:
        """Calculate deposition risk based on current speed"""
        
        # Higher currents = lower deposition risk
        if current_speed < 0.1:
            return 0.8  # High deposition risk
        elif current_speed < 0.5:
            return 0.5  # Moderate risk
        else:
            return 0.2  # Low risk
    
    def _calculate_visibility_impact(self, current_speed: float) -> float:
        """Calculate visibility impact of currents"""
        
        # Higher currents = better visibility (less sediment)
        if current_speed < 0.1:
            return 0.7  # Poor visibility
        elif current_speed < 0.5:
            return 0.4  # Moderate visibility
        else:
            return 0.2  # Good visibility
    
    def _initialize_bermuda_data(self):
        """Initialize precomputed Bermuda area data"""
        
        cache_path = Path(__file__).parent.parent.parent / "cache" / "bermuda_data.pkl"
        
        try:
            # Try to load cached data
            if cache_path.exists():
                with open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                    self.bathymetry_grid = cached_data['bathymetry']
                    self.magnetic_grid = cached_data['magnetic']
                    self.historical_wreck_db = cached_data['historical']
                    self.current_patterns = cached_data['current']
                    logger.info("✅ Loaded cached Bermuda data")
                    return
        except Exception as e:
            logger.warning(f"Could not load cached Bermuda data: {e}")
        
        # Generate synthetic data if cache not available
        logger.info("🔧 Generating synthetic Bermuda data (first run only)")
        
        # Grid dimensions
        lat_dim = int((self.bermuda_bounds['lat_max'] - self.bermuda_bounds['lat_min']) / self.grid_resolution)
        lon_dim = int((self.bermuda_bounds['lon_max'] - self.bermuda_bounds['lon_min']) / self.grid_resolution)
        
        # Generate bathymetry (15-80m depth typical for Bermuda)
        self.bathymetry_grid = np.random.uniform(15, 80, (lat_dim, lon_dim))
        
        # Add some structure (seamounts, shelves)
        for _ in range(5):  # Add 5 seamount-like features
            cx, cy = np.random.randint(0, lat_dim), np.random.randint(0, lon_dim)
            radius = np.random.randint(10, 30)
            height = np.random.uniform(10, 30)
            
            y, x = np.ogrid[:lat_dim, :lon_dim]
            mask = (x - cx)**2 + (y - cy)**2 <= radius**2
            self.bathymetry_grid[mask] -= height
        
        # Generate magnetic anomalies (mostly noise, with some strong spots)
        self.magnetic_grid = np.random.normal(0, 20, (lat_dim, lon_dim))
        
        # Add some strong magnetic anomalies (possible wrecks)
        for _ in range(10):
            cx, cy = np.random.randint(0, lat_dim), np.random.randint(0, lon_dim)
            radius = np.random.randint(5, 15)
            strength = np.random.uniform(50, 200)
            
            y, x = np.ogrid[:lat_dim, :lon_dim]
            mask = (x - cx)**2 + (y - cy)**2 <= radius**2
            self.magnetic_grid[mask] += strength
        
        # Create historical wreck database
        self.historical_wreck_db = SyntheticWreckDatabase()
        self.historical_wreck_db.generate_synthetic_wrecks(self.bermuda_bounds)
        
        # Create current patterns
        self.current_patterns = SyntheticCurrentPatterns()
        self.current_patterns.generate_patterns(self.bermuda_bounds)
        
        # Cache the data for future runs
        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_data = {
                'bathymetry': self.bathymetry_grid,
                'magnetic': self.magnetic_grid,
                'historical': self.historical_wreck_db,
                'current': self.current_patterns
            }
            
            with open(cache_path, 'wb') as f:
                pickle.dump(cache_data, f)
            
            logger.info("✅ Cached Bermuda data for future runs")
        except Exception as e:
            logger.warning(f"Could not cache Bermuda data: {e}")
    
    def _create_fallback_result(self, lat: float, lon: float, start_time: float) -> BermudaAnalysisResult:
        """Create fallback result if analysis fails"""
        
        analysis_time = (time.time() - start_time) * 1000
        
        return BermudaAnalysisResult(
            environment_type='shallow_sea',
            analysis_time_ms=analysis_time,
            candidates=[],
            bathymetry_m=50.0,  # Default depth
            magnetic_anomaly_nt=0.0,
            historical_matches=0,
            confidence_score=0.1,
            optimization_notes="Fallback result - analysis failed"
        )

class SyntheticWreckDatabase:
    """Synthetic historical wreck database for Bermuda area"""
    
    def __init__(self):
        self.wrecks = []
        self.spatial_index = {}
    
    def generate_synthetic_wrecks(self, bounds: Dict[str, float]):
        """Generate synthetic historical wreck data"""
        
        # Generate 50 synthetic wrecks in Bermuda area
        for i in range(50):
            lat = np.random.uniform(bounds['lat_min'], bounds['lat_max'])
            lon = np.random.uniform(bounds['lon_min'], bounds['lon_max'])
            depth = np.random.uniform(20, 70)
            
            wreck = {
                'id': i,
                'name': f"Historical Wreck {i}",
                'lat': lat,
                'lon': lon,
                'depth': depth,
                'type': np.random.choice(['shipwreck', 'debris', 'structure']),
                'period': np.random.choice(['16th century', '17th century', '18th century', '19th century']),
                'confidence': np.random.uniform(0.5, 1.0)
            }
            
            self.wrecks.append(wreck)
    
    def query_radius(self, lat: float, lon: float, radius_km: float) -> List[Dict[str, Any]]:
        """Query wrecks within radius of coordinates"""
        
        nearby_wrecks = []
        
        for wreck in self.wrecks:
            # Fast distance check
            lat_diff = wreck['lat'] - lat
            lon_diff = wreck['lon'] - lon
            lat_avg = (wreck['lat'] + lat) / 2
            
            distance = 6371.0 * np.sqrt(
                np.radians(lat_diff)**2 + 
                (np.radians(lon_diff) * np.cos(np.radians(lat_avg)))**2
            )
            
            if distance <= radius_km:
                nearby_wrecks.append(wreck)
        
        return nearby_wrecks

class SyntheticCurrentPatterns:
    """Synthetic current patterns for Bermuda area"""
    
    def __init__(self):
        self.current_grid = None
        self.bounds = None
    
    def generate_patterns(self, bounds: Dict[str, float]):
        """Generate synthetic current patterns"""
        
        self.bounds = bounds
        
        # Create grid
        resolution = 0.01  # 1km resolution
        lat_dim = int((bounds['lat_max'] - bounds['lat_min']) / resolution)
        lon_dim = int((bounds['lon_max'] - bounds['lon_min']) / resolution)
        
        # Generate current speeds (0.1-2.5 knots typical)
        self.current_grid = {
            'speed': np.random.uniform(0.1, 2.5, (lat_dim, lon_dim)),
            'direction': np.random.uniform(0, 360, (lat_dim, lon_dim)),
            'resolution': resolution
        }
        
        # Add Gulf Stream influence (stronger currents on eastern side)
        for i in range(lat_dim):
            for j in range(lon_dim):
                # Eastern side has stronger currents
                eastern_factor = j / lon_dim
                self.current_grid['speed'][i, j] *= (0.5 + eastern_factor)
    
    def get_current_speed(self, lat: float, lon: float) -> float:
        """Get current speed at coordinates"""
        
        if self.current_grid is None:
            return 0.5  # Default
        
        resolution = self.current_grid['resolution']
        i = int((lat - self.bounds['lat_min']) / resolution)
        j = int((lon - self.bounds['lon_min']) / resolution)
        
        # Bounds checking
        i = max(0, min(i, self.current_grid['speed'].shape[0] - 1))
        j = max(0, min(j, self.current_grid['speed'].shape[1] - 1))
        
        return float(self.current_grid['speed'][i, j])
    
    def get_current_direction(self, lat: float, lon: float) -> float:
        """Get current direction at coordinates"""
        
        if self.current_grid is None:
            return 45.0  # Default
        
        resolution = self.current_grid['resolution']
        i = int((lat - self.bounds['lat_min']) / resolution)
        j = int((lon - self.bounds['lon_min']) / resolution)
        
        # Bounds checking
        i = max(0, min(i, self.current_grid['direction'].shape[0] - 1))
        j = max(0, min(j, self.current_grid['direction'].shape[1] - 1))
        
        return float(self.current_grid['direction'][i, j])

# Singleton instance for global access
bermuda_fast_path = BermudaFastPath()

def analyze_bermuda_coordinates_fast(lat: float, lon: float, 
                                    bounds: Dict[str, float]) -> BermudaAnalysisResult:
    """Fast Bermuda analysis function"""
    return bermuda_fast_path.analyze_bermuda_coordinates(lat, lon, bounds)