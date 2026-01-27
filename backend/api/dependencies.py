#!/usr/bin/env python3
"""
Sistema de Dependency Injection para ArcheoScope
Implementa lazy loading y desacople de componentes
"""

import logging
from typing import Dict, Any, Optional
from functools import lru_cache
import sys
from pathlib import Path

# Agregar backend al path
sys.path.append(str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)

# Cache global de componentes (lazy loading)
_component_cache: Dict[str, Any] = {}
_initialization_status: Dict[str, bool] = {}

def get_system_components() -> Dict[str, Any]:
    """
    Dependency provider principal - retorna componentes del sistema
    con lazy loading implementado.
    
    CRÍTICO: Los componentes solo se instancian cuando son requeridos.
    """
    return _component_cache

@lru_cache(maxsize=1)
def get_environment_classifier():
    """Lazy loading del clasificador de ambientes."""
    
    if 'environment_classifier' not in _component_cache:
        try:
            from environment_classifier import EnvironmentClassifier
            _component_cache['environment_classifier'] = EnvironmentClassifier()
            logger.info("✅ EnvironmentClassifier cargado")
        except Exception as e:
            logger.error(f"❌ Error cargando EnvironmentClassifier: {e}")
            _component_cache['environment_classifier'] = None
    
    return _component_cache['environment_classifier']

@lru_cache(maxsize=1)
def get_core_anomaly_detector():
    """Lazy loading del detector principal de anomalías."""
    
    if 'core_anomaly_detector' not in _component_cache:
        try:
            # Cargar dependencias primero
            env_classifier = get_environment_classifier()
            real_validator = get_real_validator()
            
            from core_anomaly_detector import CoreAnomalyDetector
            _component_cache['core_anomaly_detector'] = CoreAnomalyDetector(
                environment_classifier=env_classifier,
                real_validator=real_validator,
                data_loader=None  # No usar loader que simula datos
            )
            logger.info("✅ CoreAnomalyDetector cargado")
        except Exception as e:
            logger.error(f"❌ Error cargando CoreAnomalyDetector: {e}")
            _component_cache['core_anomaly_detector'] = None
    
    return _component_cache['core_anomaly_detector']

@lru_cache(maxsize=1)
def get_real_validator():
    """Lazy loading del validador arqueológico real."""
    
    if 'real_validator' not in _component_cache:
        try:
            from validation.real_archaeological_validator import RealArchaeologicalValidator
            _component_cache['real_validator'] = RealArchaeologicalValidator()
            logger.info("✅ RealArchaeologicalValidator cargado")
        except Exception as e:
            logger.warning(f"⚠️ RealArchaeologicalValidator no disponible: {e}")
            _component_cache['real_validator'] = None
    
    return _component_cache['real_validator']

@lru_cache(maxsize=1)
def get_ai_assistant():
    """Lazy loading del asistente de IA."""
    
    if 'ai_assistant' not in _component_cache:
        try:
            from ai.archaeological_assistant import ArchaeologicalAssistant
            _component_cache['ai_assistant'] = ArchaeologicalAssistant()
            logger.info("✅ ArchaeologicalAssistant cargado")
        except Exception as e:
            logger.warning(f"⚠️ ArchaeologicalAssistant no disponible: {e}")
            _component_cache['ai_assistant'] = None
    
    return _component_cache['ai_assistant']

@lru_cache(maxsize=1)
def get_geometric_engine():
    """Lazy loading del motor geométrico volumétrico."""
    
    if 'geometric_engine' not in _component_cache:
        try:
            from volumetric.geometric_inference_engine import GeometricInferenceEngine
            _component_cache['geometric_engine'] = GeometricInferenceEngine()
            logger.info("✅ GeometricInferenceEngine cargado")
        except Exception as e:
            logger.warning(f"⚠️ GeometricInferenceEngine no disponible: {e}")
            _component_cache['geometric_engine'] = None
    
    return _component_cache['geometric_engine']

@lru_cache(maxsize=1)
def get_database_connection():
    """Lazy loading de la conexión a base de datos."""
    
    if 'database' not in _component_cache:
        try:
            from database import db
            # Test de conectividad
            db.execute("SELECT 1")
            _component_cache['database'] = db
            logger.info("✅ Database connection establecida")
        except Exception as e:
            logger.warning(f"⚠️ Database no disponible: {e}")
            _component_cache['database'] = None
    
    return _component_cache['database']

def initialize_core_components():
    """
    Inicializar componentes críticos del sistema.
    
    IMPORTANTE: Solo inicializa componentes esenciales,
    el resto se carga bajo demanda (lazy loading).
    """
    
    logger.info("🚀 Inicializando componentes críticos...")
    
    # Componentes críticos que deben estar disponibles
    critical_components = [
        ('environment_classifier', get_environment_classifier),
        ('core_anomaly_detector', get_core_anomaly_detector)
    ]
    
    success_count = 0
    
    for name, loader_func in critical_components:
        try:
            component = loader_func()
            if component is not None:
                success_count += 1
                logger.info(f"✅ {name} inicializado correctamente")
            else:
                logger.warning(f"⚠️ {name} no pudo inicializarse")
        except Exception as e:
            logger.error(f"❌ Error inicializando {name}: {e}")
    
    # Componentes opcionales (no críticos)
    optional_components = [
        ('real_validator', get_real_validator),
        ('ai_assistant', get_ai_assistant),
        ('database', get_database_connection)
    ]
    
    for name, loader_func in optional_components:
        try:
            loader_func()  # Intentar cargar pero no fallar si no funciona
        except Exception as e:
            logger.warning(f"⚠️ Componente opcional {name} no disponible: {e}")
    
    logger.info(f"🎯 Inicialización completada: {success_count}/{len(critical_components)} componentes críticos")
    
    return success_count == len(critical_components)

def perform_smoke_tests() -> Dict[str, bool]:
    """
    Ejecutar smoke tests NO bloqueantes en startup.
    
    Registra WARNINGS, nunca aborta startup.
    """
    
    logger.info("🧪 Ejecutando smoke tests...")
    
    test_results = {}
    
    # Test 1: Conectividad a DB
    try:
        db = get_database_connection()
        if db:
            db.execute("SELECT 1")
            test_results['database_connectivity'] = True
            logger.info("✅ Smoke test DB: PASS")
        else:
            test_results['database_connectivity'] = False
            logger.warning("⚠️ Smoke test DB: SKIP (no disponible)")
    except Exception as e:
        test_results['database_connectivity'] = False
        logger.warning(f"⚠️ Smoke test DB: FAIL - {e}")
    
    # Test 2: Detector principal
    try:
        detector = get_core_anomaly_detector()
        if detector:
            test_results['core_detector'] = True
            logger.info("✅ Smoke test Detector: PASS")
        else:
            test_results['core_detector'] = False
            logger.warning("⚠️ Smoke test Detector: FAIL")
    except Exception as e:
        test_results['core_detector'] = False
        logger.warning(f"⚠️ Smoke test Detector: FAIL - {e}")
    
    # Test 3: Clasificador de ambientes
    try:
        classifier = get_environment_classifier()
        if classifier:
            # Test básico de clasificación
            result = classifier.classify(0.0, 0.0)
            test_results['environment_classifier'] = True
            logger.info("✅ Smoke test Classifier: PASS")
        else:
            test_results['environment_classifier'] = False
            logger.warning("⚠️ Smoke test Classifier: FAIL")
    except Exception as e:
        test_results['environment_classifier'] = False
        logger.warning(f"⚠️ Smoke test Classifier: FAIL - {e}")
    
    # Test 4: IA (opcional)
    try:
        ai = get_ai_assistant()
        if ai:
            test_results['ai_assistant'] = True
            logger.info("✅ Smoke test IA: PASS")
        else:
            test_results['ai_assistant'] = False
            logger.info("ℹ️ Smoke test IA: SKIP (opcional)")
    except Exception as e:
        test_results['ai_assistant'] = False
        logger.info(f"ℹ️ Smoke test IA: SKIP - {e}")
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    logger.info(f"🎯 Smoke tests completados: {passed_tests}/{total_tests} PASS")
    
    return test_results

def cleanup_components():
    """Limpiar componentes al cerrar la aplicación."""
    
    logger.info("🧹 Limpiando componentes...")
    
    # Cerrar conexión a DB si existe
    try:
        db = _component_cache.get('database')
        if db:
            db.close()
            logger.info("✅ Database connection cerrada")
    except Exception as e:
        logger.error(f"❌ Error cerrando DB: {e}")
    
    # Limpiar cache
    _component_cache.clear()
    _initialization_status.clear()
    
    logger.info("✅ Limpieza completada")

# Feature flags simples vía variables de entorno
def is_feature_enabled(feature_name: str) -> bool:
    """
    Feature flags simples usando variables de entorno.
    
    Ejemplo: ARCHEOSCOPE_ENABLE_AI=true
    """
    import os
    
    env_var = f"ARCHEOSCOPE_ENABLE_{feature_name.upper()}"
    return os.getenv(env_var, "true").lower() in ("true", "1", "yes", "on")

def get_feature_flags() -> Dict[str, bool]:
    """Obtener estado de todos los feature flags."""
    
    flags = {
        'ai_analysis': is_feature_enabled('ai'),
        'volumetric_analysis': is_feature_enabled('volumetric'),
        'advanced_validation': is_feature_enabled('advanced_validation'),
        'experimental_sensors': is_feature_enabled('experimental_sensors')
    }
    
    return flags