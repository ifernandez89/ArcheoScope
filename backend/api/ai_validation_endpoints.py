#!/usr/bin/env python3
"""
API Endpoints para Validación IA de Anomalías - ArcheoScope

Endpoints especializados para el sistema de validación IA de anomalías arqueológicas.
Implementa la arquitectura ganadora:

Instrumentos → Core Detector → Features → AI Validator → Score Final + Explicación
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from ..ai.integrated_ai_validator import IntegratedAIValidator, IntegratedAnalysisResult
from ..ai.anomaly_validation_assistant import InstrumentalFeatures

logger = logging.getLogger(__name__)

# Router para endpoints de validación IA
ai_validation_router = APIRouter(
    prefix="/ai-validation",
    tags=["AI Validation"],
    responses={404: {"description": "Not found"}}
)

# Modelos de datos
class AIValidationRequest(BaseModel):
    """Solicitud de validación IA."""
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    region_name: str
    include_explanation: Optional[bool] = True
    include_quality_metrics: Optional[bool] = True

class BatchValidationRequest(BaseModel):
    """Solicitud de validación IA en lote."""
    regions: List[Dict[str, Any]]
    context: Optional[Dict[str, Any]] = None

class AIValidationResponse(BaseModel):
    """Respuesta de validación IA."""
    region_name: str
    original_score: float
    final_score: float
    score_adjustment: float
    ai_available: bool
    ai_coherent: Optional[bool]
    ai_confidence: Optional[float]
    false_positive_risk: Optional[float]
    quality_level: str
    integrated_explanation: str
    recommendations: List[str]
    timestamp: str

# Variable global para el validador integrado
integrated_validator: Optional[IntegratedAIValidator] = None

def get_integrated_validator() -> IntegratedAIValidator:
    """Obtener instancia del validador integrado."""
    global integrated_validator
    
    if integrated_validator is None:
    # Importar componentes necesarios
        try:
            from ..core_anomaly_detector import CoreAnomalyDetector
            from ..ai.archaeological_assistant import ArchaeologicalAssistant
            from ..environment_classifier import EnvironmentClassifier
            from ..validation.real_archaeological_validator import RealArchaeologicalValidator
            from ..data.archaeological_loader import ArchaeologicalDataLoader
            
            # Inicializar componentes
            env_classifier = EnvironmentClassifier()
            real_validator = RealArchaeologicalValidator()
            data_loader = ArchaeologicalDataLoader()
            
            core_detector = CoreAnomalyDetector(
                env_classifier, real_validator, data_loader
            )
            
            archaeological_assistant = ArchaeologicalAssistant()
            
            integrated_validator = IntegratedAIValidator(
                core_detector=core_detector,
                archaeological_assistant=archaeological_assistant
            )
            
            logger.info("✅ IntegratedAIValidator inicializado correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error inicializando IntegratedAIValidator: {e}")
            raise HTTPException(
                status_code=503, 
                detail=f"Error inicializando validador IA: {str(e)}"
            )
    
    return integrated_validator

@ai_validation_router.get("/status")
async def get_ai_validation_status():
    """
    ## Estado del Sistema de Validación IA
    
    Verifica el estado operacional del sistema de validación IA.
    
    **Retorna:**
    - `ai_validator_available`: Si el validador IA está disponible
    - `core_detector_available`: Si el detector base está disponible
    - `archaeological_assistant_available`: Si el asistente arqueológico está disponible
    - `integration_status`: Estado de la integración
    - `capabilities`: Capacidades disponibles
    
    **Ejemplo de uso:**
    ```bash
    curl http://localhost:8003/ai-validation/status
    ```
    """
    
    try:
        validator = get_integrated_validator()
        
        return {
            "ai_validator_available": validator.ai_validator.is_available,
            "core_detector_available": validator.core_detector is not None,
            "archaeological_assistant_available": (
                validator.archaeological_assistant is not None and 
                validator.archaeological_assistant.is_available
            ),
            "integration_status": "operational" if validator.is_available else "limited",
            "capabilities": {
                "anomaly_detection": True,
                "ai_validation": validator.ai_validator.is_available,
                "cognitive_reasoning": validator.ai_validator.is_available,
                "scoring_adjustment": validator.ai_validator.is_available,
                "false_positive_detection": validator.ai_validator.is_available,
                "batch_processing": True
            },
            "configuration": {
                "validation_threshold": validator.ai_validator.validation_threshold,
                "inconsistency_threshold": validator.ai_validator.inconsistency_threshold
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estado de validación IA: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@ai_validation_router.post("/analyze", response_model=AIValidationResponse)
async def analyze_with_ai_validation(request: AIValidationRequest):
    """
    ## Análisis con Validación IA
    
    Ejecuta análisis arqueológico completo con validación cognitiva IA.
    
    **Pipeline completo:**
    1. **Detección instrumental** - Core detector con múltiples sensores
    2. **Extracción de features** - Conversión a features numéricas
    3. **Validación IA** - Análisis cognitivo de coherencia
    4. **Score ajustado** - Score final con ajustes IA
    5. **Explicación integrada** - Razonamiento completo
    
    **Parámetros:**
    - `lat_min`, `lat_max`: Rango de latitud
    - `lon_min`, `lon_max`: Rango de longitud  
    - `region_name`: Nombre de la región
    - `include_explanation`: Incluir explicación detallada (default: true)
    - `include_quality_metrics`: Incluir métricas de calidad (default: true)
    
    **Retorna:**
    - `original_score`: Score del detector base
    - `final_score`: Score ajustado por IA
    - `score_adjustment`: Diferencia aplicada por IA
    - `ai_coherent`: Si la IA considera el resultado coherente
    - `ai_confidence`: Confianza de la validación IA (0-1)
    - `false_positive_risk`: Riesgo de falso positivo según IA (0-1)
    - `quality_level`: Nivel de calidad general (excellent/good/moderate/low)
    - `integrated_explanation`: Explicación completa del análisis
    - `recommendations`: Recomendaciones específicas
    
    **Ejemplo de uso:**
    ```bash
    curl -X POST http://localhost:8003/ai-validation/analyze \\
      -H "Content-Type: application/json" \\
      -d '{
        "lat_min": 29.97,
        "lat_max": 29.99,
        "lon_min": 31.12,
        "lon_max": 31.14,
        "region_name": "Giza Test",
        "include_explanation": true
      }'
    ```
    
    **Ventajas sobre análisis tradicional:**
    - ✅ Validación cognitiva de coherencia
    - ✅ Detección de inconsistencias lógicas
    - ✅ Ajuste inteligente de scoring
    - ✅ Explicaciones más ricas
    - ✅ Detección de falsos positivos
    - ✅ Recomendaciones específicas
    """
    
    try:
        validator = get_integrated_validator()
        
        if not validator.is_available:
            raise HTTPException(
                status_code=503,
                detail="Validador IA no disponible - verifique configuración"
            )
        
        # Calcular coordenadas centrales
        center_lat = (request.lat_min + request.lat_max) / 2
        center_lon = (request.lon_min + request.lon_max) / 2
        
        # Ejecutar análisis integrado
        logger.info(f"🔍 Iniciando análisis con validación IA: {request.region_name}")
        
        result = await validator.analyze_with_ai_validation(
            lat=center_lat,
            lon=center_lon,
            lat_min=request.lat_min,
            lat_max=request.lat_max,
            lon_min=request.lon_min,
            lon_max=request.lon_max,
            region_name=request.region_name,
            context={
                "include_explanation": request.include_explanation,
                "include_quality_metrics": request.include_quality_metrics
            }
        )
        
        # Construir respuesta
        response = AIValidationResponse(
            region_name=request.region_name,
            original_score=result.original_score,
            final_score=result.final_score,
            score_adjustment=result.final_score - result.original_score,
            ai_available=result.ai_validation is not None,
            ai_coherent=result.ai_validation.is_coherent if result.ai_validation else None,
            ai_confidence=result.ai_validation.confidence_score if result.ai_validation else None,
            false_positive_risk=result.ai_validation.false_positive_risk if result.ai_validation else None,
            quality_level=result.quality_metrics.get("overall_quality", "unknown"),
            integrated_explanation=result.integrated_explanation if request.include_explanation else "Explicación omitida",
            recommendations=result.final_recommendations,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"✅ Análisis IA completado: {request.region_name}")
        logger.info(f"   Score: {result.original_score:.3f} → {result.final_score:.3f}")
        logger.info(f"   Calidad: {result.quality_metrics.get('overall_quality', 'unknown')}")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en análisis con validación IA: {e}")
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@ai_validation_router.post("/batch-analyze")
async def batch_analyze_with_ai_validation(request: BatchValidationRequest):
    """
    ## Análisis en Lote con Validación IA
    
    Ejecuta análisis con validación IA para múltiples regiones.
    
    **Parámetros:**
    - `regions`: Lista de regiones con coordenadas y nombres
    - `context`: Contexto adicional opcional
    
    **Formato de región:**
    ```json
    {
      "lat": 29.98,
      "lon": 31.13,
      "lat_min": 29.97,
      "lat_max": 29.99,
      "lon_min": 31.12,
      "lon_max": 31.14,
      "name": "Region Name"
    }
    ```
    
    **Retorna:**
    - `results`: Lista de resultados de validación IA
    - `summary`: Resumen estadístico del lote
    - `quality_distribution`: Distribución de niveles de calidad
    - `recommendations`: Recomendaciones para el lote completo
    
    **Ejemplo de uso:**
    ```bash
    curl -X POST http://localhost:8003/ai-validation/batch-analyze \\
      -H "Content-Type: application/json" \\
      -d '{
        "regions": [
          {
            "lat": 29.98, "lon": 31.13,
            "lat_min": 29.97, "lat_max": 29.99,
            "lon_min": 31.12, "lon_max": 31.14,
            "name": "Giza Test"
          }
        ]
      }'
    ```
    """
    
    try:
        validator = get_integrated_validator()
        
        if not validator.is_available:
            raise HTTPException(
                status_code=503,
                detail="Validador IA no disponible"
            )
        
        if not request.regions:
            raise HTTPException(
                status_code=400,
                detail="Lista de regiones vacía"
            )
        
        logger.info(f"🔍 Iniciando análisis en lote: {len(request.regions)} regiones")
        
        # Ejecutar análisis en lote
        results = validator.batch_analyze_with_validation(
            regions=request.regions,
            context=request.context
        )
        
        # Generar resumen
        summary = validator.generate_validation_summary(results)
        
        # Convertir resultados a formato de respuesta
        formatted_results = []
        for result in results:
            formatted_result = {
                "region_name": result.base_detection.get("region_name", "Unknown"),
                "original_score": result.original_score,
                "final_score": result.final_score,
                "score_adjustment": result.final_score - result.original_score,
                "ai_available": result.ai_validation is not None,
                "ai_coherent": result.ai_validation.is_coherent if result.ai_validation else None,
                "ai_confidence": result.ai_validation.confidence_score if result.ai_validation else None,
                "false_positive_risk": result.ai_validation.false_positive_risk if result.ai_validation else None,
                "quality_level": result.quality_metrics.get("overall_quality", "unknown"),
                "recommendations": result.final_recommendations
            }
            formatted_results.append(formatted_result)
        
        response = {
            "results": formatted_results,
            "summary": summary,
            "batch_info": {
                "total_regions": len(request.regions),
                "successful_analyses": len(results),
                "success_rate": len(results) / len(request.regions),
                "processing_time": "calculated_on_client"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ Análisis en lote completado: {len(results)}/{len(request.regions)} exitosos")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en análisis en lote: {e}")
        raise HTTPException(status_code=500, detail=f"Error en análisis en lote: {str(e)}")

@ai_validation_router.get("/validation-report")
async def get_validation_report():
    """
    ## Reporte de Validación IA
    
    Genera reporte detallado del rendimiento del sistema de validación IA.
    
    **Retorna:**
    - `system_status`: Estado general del sistema
    - `performance_metrics`: Métricas de rendimiento
    - `ai_effectiveness`: Efectividad de la validación IA
    - `recommendations`: Recomendaciones de mejora
    
    **Ejemplo de uso:**
    ```bash
    curl http://localhost:8003/ai-validation/validation-report
    ```
    """
    
    try:
        validator = get_integrated_validator()
        
        # Información del sistema
        system_info = {
            "ai_validator_available": validator.ai_validator.is_available,
            "core_detector_available": validator.core_detector is not None,
            "integration_status": "operational" if validator.is_available else "limited"
        }
        
        # Métricas de configuración
        config_metrics = {
            "validation_threshold": validator.ai_validator.validation_threshold,
            "inconsistency_threshold": validator.ai_validator.inconsistency_threshold,
            "ai_model": "OpenRouter/Ollama" if validator.ai_validator.is_available else "None"
        }
        
        # Recomendaciones del sistema
        system_recommendations = []
        
        if not validator.ai_validator.is_available:
            system_recommendations.append("Habilitar IA para validación avanzada")
        
        if validator.is_available:
            system_recommendations.append("Sistema operacional - listo para análisis")
        else:
            system_recommendations.append("Verificar configuración de componentes")
        
        report = {
            "system_status": system_info,
            "configuration": config_metrics,
            "capabilities": {
                "cognitive_validation": validator.ai_validator.is_available,
                "inconsistency_detection": validator.ai_validator.is_available,
                "scoring_adjustment": validator.ai_validator.is_available,
                "false_positive_detection": validator.ai_validator.is_available,
                "batch_processing": True,
                "integrated_explanation": True
            },
            "recommendations": system_recommendations,
            "usage_instructions": {
                "single_analysis": "POST /ai-validation/analyze",
                "batch_analysis": "POST /ai-validation/batch-analyze",
                "status_check": "GET /ai-validation/status"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return report
        
    except Exception as e:
        logger.error(f"Error generando reporte de validación: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@ai_validation_router.get("/examples")
async def get_validation_examples():
    """
    ## Ejemplos de Uso de Validación IA
    
    Proporciona ejemplos prácticos de cómo usar el sistema de validación IA.
    
    **Retorna:**
    - `single_analysis_example`: Ejemplo de análisis individual
    - `batch_analysis_example`: Ejemplo de análisis en lote
    - `interpretation_guide`: Guía de interpretación de resultados
    """
    
    return {
        "single_analysis_example": {
            "description": "Análisis individual con validación IA",
            "endpoint": "POST /ai-validation/analyze",
            "request_example": {
                "lat_min": 29.97,
                "lat_max": 29.99,
                "lon_min": 31.12,
                "lon_max": 31.14,
                "region_name": "Giza Pyramids Test",
                "include_explanation": True,
                "include_quality_metrics": True
            },
            "curl_example": """curl -X POST http://localhost:8003/ai-validation/analyze \\
  -H "Content-Type: application/json" \\
  -d '{
    "lat_min": 29.97,
    "lat_max": 29.99,
    "lon_min": 31.12,
    "lon_max": 31.14,
    "region_name": "Giza Test"
  }'"""
        },
        "batch_analysis_example": {
            "description": "Análisis en lote con validación IA",
            "endpoint": "POST /ai-validation/batch-analyze",
            "request_example": {
                "regions": [
                    {
                        "lat": 29.98, "lon": 31.13,
                        "lat_min": 29.97, "lat_max": 29.99,
                        "lon_min": 31.12, "lon_max": 31.14,
                        "name": "Giza Test"
                    },
                    {
                        "lat": 13.41, "lon": 103.87,
                        "lat_min": 13.40, "lat_max": 13.42,
                        "lon_min": 103.86, "lon_max": 103.88,
                        "name": "Angkor Test"
                    }
                ],
                "context": {"batch_id": "test_batch_001"}
            }
        },
        "interpretation_guide": {
            "score_interpretation": {
                "original_score": "Score del detector instrumental base (0-1)",
                "final_score": "Score ajustado por validación IA (0-1)",
                "score_adjustment": "Diferencia aplicada por IA (+/- 0.XX)"
            },
            "ai_validation_fields": {
                "ai_coherent": "¿La IA considera el resultado coherente? (true/false)",
                "ai_confidence": "Confianza de la validación IA (0-1)",
                "false_positive_risk": "Riesgo de falso positivo según IA (0-1)"
            },
            "quality_levels": {
                "excellent": "Alta calidad - proceder con investigación",
                "good": "Buena calidad - considerar validación adicional",
                "moderate": "Calidad moderada - mejorar datos",
                "low": "Calidad insuficiente - revisar metodología"
            },
            "recommended_workflow": [
                "1. Verificar status del sistema (/ai-validation/status)",
                "2. Ejecutar análisis individual o en lote",
                "3. Revisar quality_level y ai_coherent",
                "4. Seguir recommendations específicas",
                "5. Si quality_level >= 'good' y ai_coherent = true → proceder",
                "6. Si no, seguir recomendaciones de mejora"
            ]
        },
        "timestamp": datetime.now().isoformat()
    }