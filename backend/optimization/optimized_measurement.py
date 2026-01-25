#!/usr/bin/env python3
"""
Optimized Measurement Simulator - Eliminates infinite loops and improves performance
Replaces the slow measurement simulation in core_anomaly_detector.py
"""

import time
import numpy as np
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class PerformanceLevel(Enum):
    FAST = "fast"       # <100ms
    BALANCED = "balanced"  # <500ms
    THOROUGH = "thorough"  # <2s

@dataclass
class MeasurementResult:
    """Optimized measurement result"""
    instrument_name: str
    measurement_type: str
    value: float
    unit: str
    threshold: float
    exceeds_threshold: bool
    confidence: str
    computation_time_ms: float
    optimization_notes: str

class OptimizedMeasurementSimulator:
    """
    Optimized measurement simulator with guaranteed termination and performance targets
    """
    
    def __init__(self, performance_level: PerformanceLevel = PerformanceLevel.BALANCED):
        self.performance_level = performance_level
        
        # Performance configuration
        self.config = self._get_performance_config(performance_level)
        
        # Performance cache
        self.measurement_cache = {}
        self.thermal_baselines = {}
        self.sar_patterns = {}
        
        # Precomputed values for common scenarios
        self._initialize_precomputed_values()
        
        logger.info(f"🚀 OptimizedMeasurementSimulator initialized in {performance_level.value} mode")
    
    def simulate_measurement(self, indicator_name: str, indicator_config: Dict[str, Any],
                           env_context, lat_min: float, lat_max: float,
                           lon_min: float, lon_max: float) -> Optional[MeasurementResult]:
        """
        Ultra-fast deterministic measurement simulation with guaranteed performance
        """
        
        start_time = time.time()
        
        try:
            # Generate cache key
            cache_key = self._generate_cache_key(indicator_name, indicator_config, 
                                               env_context, lat_min, lat_max, lon_min, lon_max)
            
            # Check cache first
            if cache_key in self.measurement_cache:
                cached_result = self.measurement_cache[cache_key]
                computation_time = (time.time() - start_time) * 1000
                
                logger.debug(f"🎯 Cache hit for {indicator_name}: {computation_time:.1f}ms")
                return MeasurementResult(
                    **cached_result,
                    computation_time_ms=computation_time,
                    optimization_notes="Cache hit"
                )
            
            # Extract threshold
            threshold = self._extract_threshold(indicator_config)
            if threshold is None:
                return None
            
            # Generate deterministic measurement
            measurement_value = self._generate_deterministic_measurement(
                indicator_name, indicator_config, env_context,
                lat_min, lat_max, lon_min, lon_max, threshold
            )
            
            # Apply environment-specific optimizations
            if hasattr(env_context, 'environment_type'):
                measurement_value = self._apply_environment_optimization(
                    measurement_value, env_context.environment_type.value, indicator_name
                )
            
            # Calculate exceeds threshold
            exceeds = measurement_value > threshold
            
            # Determine confidence
            confidence = self._calculate_confidence(measurement_value, threshold, exceeds)
            
            # Extract unit
            unit = self._extract_unit(indicator_config)
            
            computation_time = (time.time() - start_time) * 1000
            
            # Create result
            result = MeasurementResult(
                instrument_name=indicator_name,
                measurement_type=indicator_config.get('description', ''),
                value=measurement_value,
                unit=unit,
                threshold=threshold,
                exceeds_threshold=exceeds,
                confidence=confidence,
                computation_time_ms=computation_time,
                optimization_notes=f"Level: {self.performance_level.value}"
            )
            
            # Cache result if within time budget
            if computation_time < self.config['cache_threshold_ms']:
                self.measurement_cache[cache_key] = {
                    'instrument_name': result.instrument_name,
                    'measurement_type': result.measurement_type,
                    'value': result.value,
                    'unit': result.unit,
                    'threshold': result.threshold,
                    'exceeds_threshold': result.exceeds_threshold,
                    'confidence': result.confidence
                }
            
            # Log performance
            if computation_time > self.config['max_per_measurement_ms']:
                logger.warning(f"⚠️ Slow measurement {indicator_name}: {computation_time:.1f}ms > {self.config['max_per_measurement_ms']}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in optimized measurement simulation: {e}")
            return self._create_fallback_measurement(indicator_name, indicator_config, start_time)
    
    def _generate_deterministic_measurement(self, indicator_name: str, indicator_config: Dict[str, Any],
                                          env_context, lat_min: float, lat_max: float,
                                          lon_min: float, lon_max: float, threshold: float) -> float:
        """
        Generate deterministic measurement value without infinite loops
        """
        
        # Create deterministic seed based on coordinates and instrument
        coord_hash = int((abs(lat_min) * 10000 + abs(lon_min) * 10000) % 1000000)
        instrument_hash = hash(indicator_name) % 1000
        env_hash = hash(str(env_context.environment_type)) % 100
        combined_seed = coord_hash + instrument_hash + env_hash
        
        np.random.seed(combined_seed)
        
        # Performance-aware measurement generation
        if self.performance_level == PerformanceLevel.FAST:
            return self._fast_measurement_generation(indicator_name, threshold, env_context)
        elif self.performance_level == PerformanceLevel.BALANCED:
            return self._balanced_measurement_generation(indicator_name, threshold, env_context)
        else:  # THOROUGH
            return self._thorough_measurement_generation(indicator_name, threshold, env_context)
    
    def _fast_measurement_generation(self, indicator_name: str, threshold: float, env_context) -> float:
        """Ultra-fast measurement generation (<100ms)"""
        
        # Simple mathematical formula - no iterations
        base_value = threshold * (0.3 + np.random.random() * 0.8)
        
        # Quick environment adjustment
        env_multiplier = self._get_fast_env_multiplier(env_context.environment_type.value)
        
        return base_value * env_multiplier
    
    def _balanced_measurement_generation(self, indicator_name: str, threshold: float, env_context) -> float:
        """Balanced measurement generation with some complexity"""
        
        # Use precomputed patterns if available
        if indicator_name in self.sar_patterns:
            pattern_value = self.sar_patterns[indicator_name].get(env_context.environment_type.value)
            if pattern_value:
                return threshold * pattern_value
        
        # Multi-stage calculation (still fast)
        base_multiplier = 0.4 + np.random.random() * 0.6
        env_factor = self._get_balanced_env_factor(env_context.environment_type.value, indicator_name)
        instrument_factor = self._get_instrument_factor(indicator_name)
        
        return threshold * base_multiplier * env_factor * instrument_factor
    
    def _thorough_measurement_generation(self, indicator_name: str, threshold: float, env_context) -> float:
        """More thorough measurement generation with validation"""
        
        # Use more complex calculation but with hard limits
        max_iterations = 10  # Hard limit
        tolerance = 0.01
        
        base_value = threshold * (0.5 + np.random.random() * 0.8)
        
        # Apply environmental factors
        for iteration in range(max_iterations):
            env_adjustment = self._calculate_environmental_adjustment(
                indicator_name, env_context, base_value, iteration
            )
            
            new_value = base_value * (1.0 + env_adjustment)
            
            # Check convergence
            if abs(new_value - base_value) < tolerance:
                base_value = new_value
                break
            
            base_value = new_value
        
        return base_value
    
    def _get_fast_env_multiplier(self, env_type: str) -> float:
        """Fast environment multiplier lookup"""
        
        multipliers = {
            'desert': 0.7,
            'forest': 0.6,
            'shallow_sea': 0.8,
            'glacier': 0.9,
            'polar_ice': 0.85,
            'deep_ocean': 0.75,
            'grassland': 0.65,
            'mountain': 0.7,
            'unknown': 0.6
        }
        
        return multipliers.get(env_type, 0.7)
    
    def _get_balanced_env_factor(self, env_type: str, indicator_name: str) -> float:
        """Balanced environment factor calculation"""
        
        factors = {
            'desert': {
                'thermal': 0.8,
                'sar': 0.7,
                'ndvi': 0.5,
                'default': 0.65
            },
            'forest': {
                'lidar': 0.9,
                'thermal': 0.6,
                'sar': 0.5,
                'default': 0.6
            },
            'shallow_sea': {
                'sonar': 0.85,
                'magnetometer': 0.9,
                'bathymetry': 0.8,
                'default': 0.8
            },
            'glacier': {
                'thermal': 0.85,
                'sar': 0.8,
                'elevation': 0.9,
                'default': 0.8
            }
        }
        
        env_factors = factors.get(env_type, {'default': 0.7})
        
        for key in env_factors:
            if key in indicator_name.lower():
                return env_factors[key]
        
        return env_factors['default']
    
    def _calculate_environmental_adjustment(self, indicator_name: str, env_context, 
                                          current_value: float, iteration: int) -> float:
        """Calculate environmental adjustment with convergence"""
        
        # Damping factor to ensure convergence
        damping = 0.5 ** iteration
        
        # Environmental influence
        env_influence = self._get_environmental_influence(env_context.environment_type.value)
        
        # Random component (diminishing with iterations)
        random_component = (np.random.random() - 0.5) * 0.1 * damping
        
        return env_influence * damping + random_component
    
    def _get_environmental_influence(self, env_type: str) -> float:
        """Get environmental influence factor"""
        
        influences = {
            'desert': 0.2,
            'forest': -0.1,
            'shallow_sea': 0.15,
            'glacier': 0.1,
            'polar_ice': 0.05,
            'deep_ocean': -0.05
        }
        
        return influences.get(env_type, 0.0)
    
    def _get_instrument_factor(self, indicator_name: str) -> float:
        """Get instrument-specific factor"""
        
        if 'thermal' in indicator_name.lower():
            return 0.9
        elif 'sar' in indicator_name.lower():
            return 0.85
        elif 'lidar' in indicator_name.lower():
            return 0.95
        elif 'magnetometer' in indicator_name.lower():
            return 0.9
        elif 'sonar' in indicator_name.lower():
            return 0.85
        else:
            return 0.8
    
    def _apply_environment_optimization(self, value: float, env_type: str, indicator_name: str) -> float:
        """Apply environment-specific optimizations"""
        
        # Precomputed optimization factors
        if env_type == 'bermuda_area':  # Special case for Bermuda
            return self._apply_bermuda_optimization(value, indicator_name)
        
        return value
    
    def _apply_bermuda_optimization(self, value: float, indicator_name: str) -> float:
        """Apply Bermuda-specific optimizations"""
        
        # Bermuda area has specific optimization factors
        bermuda_factors = {
            'magnetometer': 1.2,  # Strong magnetic signals in Bermuda
            'sonar': 1.1,          # Good sonar penetration
            'bathymetry': 1.15     # Clear bathymetry
        }
        
        for key, factor in bermuda_factors.items():
            if key in indicator_name.lower():
                return value * factor
        
        return value
    
    def _calculate_confidence(self, value: float, threshold: float, exceeds: bool) -> str:
        """Calculate confidence level"""
        
        if not exceeds:
            return "none"
        
        ratio = value / threshold
        
        if ratio > 1.8:
            return "high"
        elif ratio > 1.4:
            return "moderate"
        else:
            return "low"
    
    def _extract_threshold(self, indicator_config: Dict[str, Any]) -> Optional[float]:
        """Extract threshold from indicator config"""
        
        threshold_keys = [k for k in indicator_config.keys() if 'threshold' in k]
        
        if threshold_keys:
            return float(indicator_config[threshold_keys[0]])
        
        return None
    
    def _extract_unit(self, indicator_config: Dict[str, Any]) -> str:
        """Extract unit from indicator config"""
        
        threshold_keys = [k for k in indicator_config.keys() if 'threshold' in k]
        
        if threshold_keys:
            threshold_key = threshold_keys[0]
            
            if 'delta_k' in threshold_key or 'temp' in threshold_key:
                return "K"
            elif '_m' in threshold_key or 'height' in threshold_key:
                return "m"
            elif '_db' in threshold_key:
                return "dB"
            elif 'ndvi' in threshold_key:
                return "NDVI"
            elif '_nt' in threshold_key:
                return "nT"
        
        return "units"
    
    def _generate_cache_key(self, indicator_name: str, indicator_config: Dict[str, Any],
                           env_context, lat_min: float, lat_max: float,
                           lon_min: float, lon_max: float) -> str:
        """Generate cache key for measurement"""
        
        env_type = getattr(env_context, 'environment_type', 'unknown').value
        
        return f"{indicator_name}_{env_type}_{lat_min:.3f}_{lat_max:.3f}_{lon_min:.3f}_{lon_max:.3f}"
    
    def _create_fallback_measurement(self, indicator_name: str, indicator_config: Dict[str, Any],
                                   start_time: float) -> MeasurementResult:
        """Create fallback measurement if simulation fails"""
        
        computation_time = (time.time() - start_time) * 1000
        
        return MeasurementResult(
            instrument_name=indicator_name,
            measurement_type=indicator_config.get('description', 'Failed measurement'),
            value=0.0,
            unit="unknown",
            threshold=0.0,
            exceeds_threshold=False,
            confidence="none",
            computation_time_ms=computation_time,
            optimization_notes="Fallback measurement"
        )
    
    def _get_performance_config(self, performance_level: PerformanceLevel) -> Dict[str, Any]:
        """Get performance configuration for level"""
        
        configs = {
            PerformanceLevel.FAST: {
                'max_per_measurement_ms': 100,
                'cache_threshold_ms': 50,
                'max_cache_size': 1000
            },
            PerformanceLevel.BALANCED: {
                'max_per_measurement_ms': 500,
                'cache_threshold_ms': 200,
                'max_cache_size': 500
            },
            PerformanceLevel.THOROUGH: {
                'max_per_measurement_ms': 2000,
                'cache_threshold_ms': 1000,
                'max_cache_size': 200
            }
        }
        
        return configs[performance_level]
    
    def _initialize_precomputed_values(self):
        """Initialize precomputed values for common scenarios"""
        
        # Precompute SAR patterns for different environments
        self.sar_patterns = {
            'sar_backscatter': {
                'desert': 0.6,
                'forest': 0.4,
                'shallow_sea': 0.7,
                'glacier': 0.8,
                'polar_ice': 0.75
            },
            'thermal_anomalies': {
                'desert': 0.8,
                'forest': 0.5,
                'shallow_sea': 0.3,
                'glacier': 0.9,
                'polar_ice': 0.85
            },
            'magnetic_anomalies': {
                'shallow_sea': 0.85,
                'deep_ocean': 0.7,
                'desert': 0.4,
                'default': 0.5
            }
        }
        
        # Precompute thermal baselines for major regions
        self.thermal_baselines = {
            'bermuda': 25.0,  # Bermuda average temperature
            'giza': 35.0,    # Giza average temperature
            'angkor': 28.0,  # Angkor average temperature
            'default': 20.0
        }
    
    def clear_cache(self):
        """Clear measurement cache"""
        self.measurement_cache.clear()
        logger.info("🗑️ Measurement cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        
        return {
            'cache_size': len(self.measurement_cache),
            'performance_level': self.performance_level.value,
            'max_per_measurement_ms': self.config['max_per_measurement_ms'],
            'cache_threshold_ms': self.config['cache_threshold_ms']
        }

# Global instances for different performance levels
fast_simulator = OptimizedMeasurementSimulator(PerformanceLevel.FAST)
balanced_simulator = OptimizedMeasurementSimulator(PerformanceLevel.BALANCED)
thorough_simulator = OptimizedMeasurementSimulator(PerformanceLevel.THOROUGH)

def simulate_measurement_optimized(indicator_name: str, indicator_config: Dict[str, Any],
                                  env_context, lat_min: float, lat_max: float,
                                  lon_min: float, lon_max: float,
                                  performance_level: PerformanceLevel = PerformanceLevel.BALANCED) -> Optional[MeasurementResult]:
    """Optimized measurement simulation function"""
    
    if performance_level == PerformanceLevel.FAST:
        return fast_simulator.simulate_measurement(indicator_name, indicator_config, env_context,
                                                 lat_min, lat_max, lon_min, lon_max)
    elif performance_level == PerformanceLevel.BALANCED:
        return balanced_simulator.simulate_measurement(indicator_name, indicator_config, env_context,
                                                      lat_min, lat_max, lon_min, lon_max)
    else:
        return thorough_simulator.simulate_measurement(indicator_name, indicator_config, env_context,
                                                     lat_min, lat_max, lon_min, lon_max)