#!/usr/bin/env python3
"""
Optimized Core Anomaly Detector - Integration of all optimizations
This replaces the slow core_anomaly_detector.py with optimized version
"""

import json
import logging
import time
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Import optimized components
from .bermuda_fast_path import bermuda_fast_path, analyze_bermuda_coordinates_fast
from .optimized_measurement import simulate_measurement_optimized, PerformanceLevel
from .ai_prioritizer import create_optimized_execution_plan, execute_optimized_plan, ComputationPriority

logger = logging.getLogger(__name__)

@dataclass
class OptimizedInstrumentMeasurement:
    """Optimized instrument measurement with performance tracking"""
    instrument_name: str
    measurement_type: str
    value: float
    unit: str
    threshold: float
    exceeds_threshold: bool
    confidence: str
    computation_time_ms: float
    optimization_notes: str

@dataclass
class OptimizedAnomalyDetectionResult:
    """Optimized anomaly detection result with performance metrics"""
    anomaly_detected: bool
    confidence_level: str
    archaeological_probability: float
    
    # Performance metrics
    total_time_ms: float
    optimization_time_ms: float
    measurement_time_ms: float
    ai_planning_time_ms: float
    
    # Environment details
    environment_type: str
    environment_confidence: float
    
    # Optimized measurements
    measurements: List[OptimizedInstrumentMeasurement]
    instruments_converging: int
    minimum_required: int
    
    # Validation
    known_site_nearby: bool
    known_site_name: Optional[str]
    known_site_distance_km: Optional[float]
    
    # Optimization details
    optimization_strategy: str
    performance_level: str
    cache_hits: int
    ai_confidence: float
    
    # Standard fields
    explanation: str
    detection_reasoning: List[str]
    false_positive_risks: List[str]
    recommended_validation: List[str]

class OptimizedCoreAnomalyDetector:
    """
    Optimized Core Anomaly Detector with AI-driven performance optimization
    """
    
    def __init__(self, environment_classifier, real_validator, data_loader, 
                 performance_level: PerformanceLevel = PerformanceLevel.BALANCED):
        """
        Initialize optimized detector
        
        Args:
            environment_classifier: Environment classification system
            real_validator: Archaeological site validator
            data_loader: Data loading system
            performance_level: Target performance level
        """
        self.environment_classifier = environment_classifier
        self.real_validator = real_validator
        self.data_loader = data_loader
        self.performance_level = performance_level
        
        # Load anomaly signatures
        self.anomaly_signatures = self._load_anomaly_signatures()
        
        # Performance tracking
        self.performance_stats = {
            'total_analyses': 0,
            'avg_time_ms': 0,
            'cache_hits': 0,
            'bermuda_fast_paths': 0
        }
        
        # AI optimization enabled
        self.ai_optimization_enabled = True
        
        logger.info(f"🚀 OptimizedCoreAnomalyDetector initialized in {performance_level.value} mode")
    
    def detect_anomaly_optimized(self, lat: float, lon: float, 
                                lat_min: float, lat_max: float,
                                lon_min: float, lon_max: float,
                                region_name: str = "Unknown Region",
                                time_budget_ms: Optional[float] = None) -> OptimizedAnomalyDetectionResult:
        """
        Optimized anomaly detection with AI-driven performance optimization
        
        Args:
            lat, lon: Center coordinates
            lat_min, lat_max, lon_min, lon_max: Bounding box
            region_name: Region name
            time_budget_ms: Optional time budget constraint
            
        Returns:
            OptimizedAnomalyDetectionResult with performance metrics
        """
        
        start_time = time.time()
        
        try:
            logger.info("="*80)
            logger.info(f"🚀 OPTIMIZED CORE DETECTOR - {self.performance_level.value.upper()} MODE")
            logger.info(f"   Region: {region_name}")
            logger.info(f"   Coordinates: {lat:.4f}, {lon:.4f}")
            
            # Set time budget based on performance level
            if time_budget_ms is None:
                time_budget_ms = self._get_default_time_budget()
            
            logger.info(f"   Time Budget: {time_budget_ms}ms")
            logger.info("="*80)
            
            # OPTIMIZATION 1: Bermuda fast path
            optimization_start = time.time()
            
            if bermuda_fast_path.is_bermuda_coordinates(lat, lon):
                logger.info("🏝️ Using Bermuda fast path optimization")
                self.performance_stats['bermuda_fast_paths'] += 1
                
                bermuda_result = analyze_bermuda_coordinates_fast(lat, lon, {
                    'lat_min': lat_min, 'lat_max': lat_max,
                    'lon_min': lon_min, 'lon_max': lon_max
                })
                
                return self._convert_bermuda_result(bermuda_result, start_time)
            
            optimization_time = (time.time() - optimization_start) * 1000
            
            # STEP 1: Fast environment classification
            env_start = time.time()
            env_context = self.environment_classifier.classify(lat, lon)
            env_time = (time.time() - env_start) * 1000
            
            logger.info(f"   ✅ Environment: {env_context.environment_type.value} ({env_time:.1f}ms)")
            
            # STEP 2: AI-driven computation planning
            ai_start = time.time()
            
            if self.ai_optimization_enabled:
                execution_plan = self._create_ai_execution_plan(
                    lat_min, lat_max, lon_min, lon_max, env_context, time_budget_ms
                )
                ai_time = (time.time() - ai_start) * 1000
                logger.info(f"   🧠 AI Planning: {ai_time:.1f}ms, {len(execution_plan.tasks)} tasks")
            else:
                execution_plan = None
                ai_time = 0
            
            # STEP 3: Optimized measurements
            measurement_start = time.time()
            measurements = self._perform_optimized_measurements(
                env_context, lat_min, lat_max, lon_min, lon_max, execution_plan, time_budget_ms
            )
            measurement_time = (time.time() - measurement_start) * 1000
            
            logger.info(f"   📊 Measurements: {len(measurements)} instruments ({measurement_time:.1f}ms)")
            
            # STEP 4: Fast analysis and validation
            analysis_start = time.time()
            
            anomaly_analysis = self._fast_anomaly_analysis(measurements, env_context)
            validation = self._fast_validation(lat_min, lat_max, lon_min, lon_max)
            archaeological_probability = self._fast_probability_calculation(
                anomaly_analysis, env_context, validation
            )
            
            analysis_time = (time.time() - analysis_start) * 1000
            
            # STEP 5: Generate optimized result
            total_time = (time.time() - start_time) * 1000
            
            result = self._generate_optimized_result(
                env_context, measurements, anomaly_analysis, validation,
                archaeological_probability, total_time, optimization_time,
                measurement_time, ai_time, execution_plan
            )
            
            # Update performance stats
            self._update_performance_stats(result)
            
            logger.info("="*80)
            logger.info(f"🎯 OPTIMIZED RESULT: {'ANOMALY' if result.anomaly_detected else 'NO ANOMALY'}")
            logger.info(f"   Total Time: {total_time:.1f}ms (Budget: {time_budget_ms}ms)")
            logger.info(f"   Strategy: {result.optimization_strategy}")
            logger.info(f"   Confidence: {result.confidence_level} ({result.archaeological_probability:.2%})")
            logger.info("="*80)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in optimized anomaly detection: {e}")
            return self._create_optimized_fallback_result(lat, lon, start_time)
    
    def _create_ai_execution_plan(self, lat_min: float, lat_max: float,
                                 lon_min: float, lon_max: float,
                                 env_context, time_budget_ms: float):
        """Create AI-driven execution plan"""
        
        # Define available computations
        computations = {}
        
        env_type = env_context.environment_type.value
        env_signatures = self._get_signatures_for_environment(env_type)
        
        if not env_signatures:
            return None
        
        # Create computations for each indicator
        for indicator_name, indicator_config in env_signatures.get('archaeological_indicators', {}).items():
            def create_measurement_func(name, config):
                return lambda: simulate_measurement_optimized(
                    name, config, env_context, lat_min, lat_max, lon_min, lon_max, self.performance_level
                )
            
            computations[indicator_name] = {
                'function': create_measurement_func(indicator_name, indicator_config),
                'priority': self._determine_computation_priority(indicator_name, env_type),
                'dependencies': []
            }
        
        # Create AI execution plan
        context = {
            'environment_type': env_type,
            'bounds': {
                'lat_min': lat_min, 'lat_max': lat_max,
                'lon_min': lon_min, 'lon_max': lon_max
            },
            'time_budget_ms': time_budget_ms
        }
        
        return create_optimized_execution_plan(computations, context, time_budget_ms)
    
    def _perform_optimized_measurements(self, env_context, lat_min: float, lat_max: float,
                                       lon_min: float, lon_max: float,
                                       execution_plan, time_budget_ms: float) -> List[OptimizedInstrumentMeasurement]:
        """Perform measurements with AI optimization"""
        
        if execution_plan and self.ai_optimization_enabled:
            # Use AI execution plan
            results = execute_optimized_plan(execution_plan, parallel=True)
            
            measurements = []
            for task_name, result in results.items():
                if result is not None:
                    # Convert to optimized measurement
                    optimized_measurement = OptimizedInstrumentMeasurement(
                        instrument_name=result.instrument_name,
                        measurement_type=result.measurement_type,
                        value=result.value,
                        unit=result.unit,
                        threshold=result.threshold,
                        exceeds_threshold=result.exceeds_threshold,
                        confidence=result.confidence,
                        computation_time_ms=result.computation_time_ms,
                        optimization_notes=result.optimization_notes
                    )
                    measurements.append(optimized_measurement)
            
            return measurements
        
        else:
            # Fallback to standard optimized measurement
            env_signatures = self._get_signatures_for_environment(env_context.environment_type.value)
            
            if not env_signatures:
                return []
            
            measurements = []
            indicators = env_signatures.get('archaeological_indicators', {})
            
            for indicator_name, indicator_config in indicators.items():
                measurement = simulate_measurement_optimized(
                    indicator_name, indicator_config, env_context,
                    lat_min, lat_max, lon_min, lon_max, self.performance_level
                )
                
                if measurement:
                    optimized_measurement = OptimizedInstrumentMeasurement(
                        instrument_name=measurement.instrument_name,
                        measurement_type=measurement.measurement_type,
                        value=measurement.value,
                        unit=measurement.unit,
                        threshold=measurement.threshold,
                        exceeds_threshold=measurement.exceeds_threshold,
                        confidence=measurement.confidence,
                        computation_time_ms=measurement.computation_time_ms,
                        optimization_notes=measurement.optimization_notes
                    )
                    measurements.append(optimized_measurement)
            
            return measurements
    
    def _determine_computation_priority(self, indicator_name: str, env_type: str) -> str:
        """Determine computation priority for AI planning"""
        
        # Environment-specific priorities
        critical_indicators = {
            'desert': ['thermal_anomalies', 'sar_backscatter'],
            'forest': ['lidar_elevation_anomalies', 'ndvi_canopy_gaps'],
            'shallow_sea': ['magnetic_anomalies', 'bathymetric_anomalies'],
            'glacier': ['thermal_ice_anomalies', 'sar_polarimetric_anomalies']
        }
        
        if indicator_name in critical_indicators.get(env_type, []):
            return 'critical'
        elif 'magnetic' in indicator_name or 'thermal' in indicator_name:
            return 'high'
        else:
            return 'medium'
    
    def _fast_anomaly_analysis(self, measurements: List[OptimizedInstrumentMeasurement],
                              env_context) -> Dict[str, Any]:
        """Fast anomaly analysis without complex computations"""
        
        instruments_exceeding = sum(1 for m in measurements if m.exceeds_threshold)
        high_confidence_count = sum(1 for m in measurements if m.confidence == "high")
        moderate_confidence_count = sum(1 for m in measurements if m.confidence == "moderate")
        
        # Get minimum convergence from environment signatures
        env_signatures = self._get_signatures_for_environment(env_context.environment_type.value)
        minimum_required = env_signatures.get('minimum_convergence', 2)
        convergence_met = instruments_exceeding >= minimum_required
        
        return {
            'instruments_exceeding': instruments_exceeding,
            'high_confidence_count': high_confidence_count,
            'moderate_confidence_count': moderate_confidence_count,
            'minimum_required': minimum_required,
            'convergence_met': convergence_met,
            'total_measurements': len(measurements)
        }
    
    def _fast_validation(self, lat_min: float, lat_max: float,
                        lon_min: float, lon_max: float) -> Dict[str, Any]:
        """Fast validation with caching"""
        
        validation_results = self.real_validator.validate_region(
            lat_min, lat_max, lon_min, lon_max
        )
        
        overlapping = validation_results.get('overlapping_sites', [])
        nearby = validation_results.get('nearby_sites', [])
        
        if overlapping:
            return {
                'known_site_nearby': True,
                'site_name': overlapping[0].name,
                'distance_km': 0.0,
                'site_type': overlapping[0].site_type,
                'confidence_level': overlapping[0].confidence_level
            }
        elif nearby:
            site, distance = nearby[0]
            return {
                'known_site_nearby': True,
                'site_name': site.name,
                'distance_km': distance,
                'site_type': site.site_type,
                'confidence_level': site.confidence_level
            }
        else:
            return {
                'known_site_nearby': False,
                'site_name': None,
                'distance_km': None,
                'site_type': None,
                'confidence_level': None
            }
    
    def _fast_probability_calculation(self, anomaly_analysis: Dict[str, Any],
                                     env_context, validation: Dict[str, Any]) -> float:
        """Fast probability calculation with simplified logic"""
        
        # Simplified probability calculation
        convergence_factor = 0.0
        if anomaly_analysis['convergence_met']:
            ratio = anomaly_analysis['instruments_exceeding'] / anomaly_analysis['minimum_required']
            convergence_factor = min(ratio / 2.0, 1.0)
        
        confidence_factor = 0.0
        total = anomaly_analysis['total_measurements']
        if total > 0:
            high_weight = anomaly_analysis['high_confidence_count'] * 1.0
            moderate_weight = anomaly_analysis['moderate_confidence_count'] * 0.6
            confidence_factor = (high_weight + moderate_weight) / total
        
        # Simplified environment factor
        env_factor = {
            'desert': 0.9, 'glacier': 0.8, 'shallow_sea': 0.7,
            'forest': 0.6, 'polar_ice': 0.5, 'unknown': 0.3
        }.get(env_context.environment_type.value, 0.5)
        
        probability = (
            convergence_factor * 0.5 +
            confidence_factor * 0.3 +
            env_factor * 0.2
        )
        
        return min(probability, 1.0)
    
    def _generate_optimized_result(self, env_context, measurements: List[OptimizedInstrumentMeasurement],
                                  anomaly_analysis: Dict[str, Any], validation: Dict[str, Any],
                                  archaeological_probability: float, total_time: float,
                                  optimization_time: float, measurement_time: float,
                                  ai_time: float, execution_plan) -> OptimizedAnomalyDetectionResult:
        """Generate optimized result with performance metrics"""
        
        # Determine anomaly detection
        anomaly_detected = anomaly_analysis['convergence_met'] and archaeological_probability > 0.5
        
        # Determine confidence level
        if archaeological_probability > 0.7 and anomaly_analysis['high_confidence_count'] >= 2:
            confidence_level = "high"
        elif archaeological_probability > 0.5 and anomaly_analysis['convergence_met']:
            confidence_level = "moderate"
        elif archaeological_probability > 0.3:
            confidence_level = "low"
        else:
            confidence_level = "none"
        
        # Calculate cache hits
        cache_hits = sum(1 for m in measurements if 'Cache hit' in m.optimization_notes)
        
        # Determine optimization strategy
        if execution_plan:
            optimization_strategy = execution_plan.optimization_strategy
            ai_confidence = execution_plan.ai_confidence
        else:
            optimization_strategy = "standard_optimized"
            ai_confidence = 0.5
        
        # Generate explanation
        explanation = self._generate_optimized_explanation(
            env_context, measurements, anomaly_analysis, validation, archaeological_probability
        )
        
        return OptimizedAnomalyDetectionResult(
            anomaly_detected=anomaly_detected,
            confidence_level=confidence_level,
            archaeological_probability=archaeological_probability,
            
            # Performance metrics
            total_time_ms=total_time,
            optimization_time_ms=optimization_time,
            measurement_time_ms=measurement_time,
            ai_planning_time_ms=ai_time,
            
            # Environment details
            environment_type=env_context.environment_type.value,
            environment_confidence=env_context.confidence,
            
            # Measurements
            measurements=measurements,
            instruments_converging=anomaly_analysis['instruments_exceeding'],
            minimum_required=anomaly_analysis['minimum_required'],
            
            # Validation
            known_site_nearby=validation['known_site_nearby'],
            known_site_name=validation['site_name'],
            known_site_distance_km=validation['distance_km'],
            
            # Optimization details
            optimization_strategy=optimization_strategy,
            performance_level=self.performance_level.value,
            cache_hits=cache_hits,
            ai_confidence=ai_confidence,
            
            # Standard fields
            explanation=explanation,
            detection_reasoning=[m.optimization_notes for m in measurements if m.exceeds_threshold],
            false_positive_risks=self._identify_false_positive_risks(measurements),
            recommended_validation=self._generate_validation_recommendations(
                env_context, anomaly_detected, confidence_level
            )
        )
    
    def _generate_optimized_explanation(self, env_context, measurements: List[OptimizedInstrumentMeasurement],
                                       anomaly_analysis: Dict[str, Any], validation: Dict[str, Any],
                                       archaeological_probability: float) -> str:
        """Generate optimized explanation"""
        
        parts = []
        parts.append(f"Optimized analysis in {env_context.environment_type.value} environment.")
        parts.append(f"Analysis completed in {sum(m.computation_time_ms for m in measurements):.1f}ms.")
        
        exceeding = [m for m in measurements if m.exceeds_threshold]
        if exceeding:
            parts.append(f"{len(exceeding)} of {len(measurements)} instruments detected anomalies.")
        else:
            parts.append("No significant anomalies detected.")
        
        if archaeological_probability > 0.7:
            parts.append("High archaeological probability detected.")
        elif archaeological_probability > 0.5:
            parts.append("Moderate archaeological probability.")
        else:
            parts.append("Low archaeological probability.")
        
        return " ".join(parts)
    
    def _identify_false_positive_risks(self, measurements: List[OptimizedInstrumentMeasurement]) -> List[str]:
        """Identify false positive risks"""
        
        risks = []
        
        for measurement in measurements:
            if measurement.exceeds_threshold and measurement.confidence in ['low', 'moderate']:
                risks.append(f"Potential false positive in {measurement.instrument_name}")
        
        return risks
    
    def _generate_validation_recommendations(self, env_context, anomaly_detected: bool,
                                          confidence_level: str) -> List[str]:
        """Generate validation recommendations"""
        
        recommendations = []
        
        if anomaly_detected:
            if confidence_level == "high":
                recommendations.append("Field validation recommended")
                recommendations.append("High-resolution data acquisition")
            elif confidence_level == "moderate":
                recommendations.append("Additional analysis recommended")
            else:
                recommendations.append("More evidence needed")
        
        # Environment-specific recommendations
        env_type = env_context.environment_type.value
        if env_type == "forest":
            recommendations.append("LiDAR verification recommended")
        elif env_type == "shallow_sea":
            recommendations.append("Underwater survey recommended")
        
        return recommendations
    
    def _get_default_time_budget(self) -> float:
        """Get default time budget based on performance level"""
        
        budgets = {
            PerformanceLevel.FAST: 10000,    # 10 seconds
            PerformanceLevel.BALANCED: 30000,  # 30 seconds
            PerformanceLevel.THOROUGH: 60000   # 60 seconds
        }
        
        return budgets[self.performance_level]
    
    def _convert_bermuda_result(self, bermuda_result, start_time: float) -> OptimizedAnomalyDetectionResult:
        """Convert Bermuda result to optimized result format"""
        
        total_time = (time.time() - start_time) * 1000
        
        # Create measurements from Bermuda candidates
        measurements = []
        for i, candidate in enumerate(bermuda_result.candidates[:5]):
            measurement = OptimizedInstrumentMeasurement(
                instrument_name=f"bermuda_candidate_{i}",
                measurement_type=candidate['type'],
                value=candidate['archaeological_probability'],
                unit="probability",
                threshold=0.5,
                exceeds_threshold=candidate['archaeological_probability'] > 0.5,
                confidence="high" if candidate['archaeological_probability'] > 0.7 else "moderate",
                computation_time_ms=bermuda_result.analysis_time_ms / len(bermuda_result.candidates),
                optimization_notes="Bermuda fast path"
            )
            measurements.append(measurement)
        
        return OptimizedAnomalyDetectionResult(
            anomaly_detected=len(bermuda_result.candidates) > 0,
            confidence_level="high" if bermuda_result.confidence_score > 0.7 else "moderate",
            archaeological_probability=bermuda_result.confidence_score,
            
            # Performance metrics
            total_time_ms=total_time,
            optimization_time_ms=0,
            measurement_time_ms=bermuda_result.analysis_time_ms,
            ai_planning_time_ms=0,
            
            # Environment details
            environment_type="shallow_sea",
            environment_confidence=0.95,
            
            # Measurements
            measurements=measurements,
            instruments_converging=len([m for m in measurements if m.exceeds_threshold]),
            minimum_required=2,
            
            # Validation
            known_site_nearby=False,
            known_site_name=None,
            known_site_distance_km=None,
            
            # Optimization details
            optimization_strategy="bermuda_fast_path",
            performance_level=self.performance_level.value,
            cache_hits=0,
            ai_confidence=0.9,
            
            # Standard fields
            explanation=bermuda_result.optimization_notes,
            detection_reasoning=[bermuda_result.optimization_notes],
            false_positive_risks=[],
            recommended_validation=["Underwater survey recommended"]
        )
    
    def _update_performance_stats(self, result: OptimizedAnomalyDetectionResult):
        """Update performance statistics"""
        
        self.performance_stats['total_analyses'] += 1
        
        # Update average time
        current_avg = self.performance_stats['avg_time_ms']
        total_analyses = self.performance_stats['total_analyses']
        
        new_avg = (current_avg * (total_analyses - 1) + result.total_time_ms) / total_analyses
        self.performance_stats['avg_time_ms'] = new_avg
        
        # Update cache hits
        self.performance_stats['cache_hits'] += result.cache_hits
        
        # Log performance if significantly over budget
        default_budget = self._get_default_time_budget()
        if result.total_time_ms > default_budget * 1.5:
            logger.warning(f"⚠️ Performance alert: {result.total_time_ms:.1f}ms > {default_budget * 1.5:.1f}ms budget")
    
    def _create_optimized_fallback_result(self, lat: float, lon: float, start_time: float) -> OptimizedAnomalyDetectionResult:
        """Create fallback optimized result"""
        
        total_time = (time.time() - start_time) * 1000
        
        return OptimizedAnomalyDetectionResult(
            anomaly_detected=False,
            confidence_level="none",
            archaeological_probability=0.0,
            total_time_ms=total_time,
            optimization_time_ms=0,
            measurement_time_ms=0,
            ai_planning_time_ms=0,
            environment_type="unknown",
            environment_confidence=0.0,
            measurements=[],
            instruments_converging=0,
            minimum_required=0,
            known_site_nearby=False,
            known_site_name=None,
            known_site_distance_km=None,
            optimization_strategy="fallback",
            performance_level=self.performance_level.value,
            cache_hits=0,
            ai_confidence=0.0,
            explanation="Analysis failed - fallback result",
            detection_reasoning=["Analysis failed"],
            false_positive_risks=["Fallback analysis"],
            recommended_validation=["Manual analysis required"]
        )
    
    # Reuse methods from original detector
    def _load_anomaly_signatures(self) -> Dict[str, Any]:
        """Load anomaly signatures"""
        try:
            signatures_path = Path(__file__).parent.parent.parent / "data" / "anomaly_signatures_by_environment.json"
            
            if not signatures_path.exists():
                logger.error(f"Signature file not found: {signatures_path}")
                return {}
            
            with open(signatures_path, 'r', encoding='utf-8') as f:
                signatures = json.load(f)
            
            logger.info(f"✅ Loaded signatures for {len(signatures.get('environment_signatures', {}))} environments")
            return signatures
        
        except Exception as e:
            logger.error(f"Error loading signatures: {e}")
            return {}
    
    def _get_signatures_for_environment(self, environment_type: str) -> Dict[str, Any]:
        """Get signatures for environment"""
        env_signatures = self.anomaly_signatures.get('environment_signatures', {})
        return env_signatures.get(environment_type, env_signatures.get('unknown', {}))
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return self.performance_stats.copy()
    
    def reset_performance_stats(self):
        """Reset performance statistics"""
        self.performance_stats = {
            'total_analyses': 0,
            'avg_time_ms': 0,
            'cache_hits': 0,
            'bermuda_fast_paths': 0
        }
        logger.info("📊 Performance statistics reset")

# Factory function
def create_optimized_detector(environment_classifier, real_validator, data_loader,
                             performance_level: PerformanceLevel = PerformanceLevel.BALANCED) -> OptimizedCoreAnomalyDetector:
    """Create optimized core anomaly detector"""
    return OptimizedCoreAnomalyDetector(
        environment_classifier, real_validator, data_loader, performance_level
    )