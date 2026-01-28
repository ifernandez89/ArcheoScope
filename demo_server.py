#!/usr/bin/env python3
"""
Servidor de demostración simplificado para ArcheoScope.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import numpy as np
import json
import logging
import requests
import asyncio

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="ArcheoScope Demo Server",
    description="Sistema científico para detectar donde las explicaciones arqueológicas actuales fallan",
    version="1.0.0-demo"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class RegionRequest(BaseModel):
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    resolution_m: Optional[int] = 1000
    layers_to_analyze: Optional[List[str]] = ["ice_velocity", "ice_thickness", "bedrock_elevation"]
    active_rules: Optional[List[str]] = ["all"]
    region_name: Optional[str] = "Demo Region"

class AnalysisResponse(BaseModel):
    region_info: Dict[str, Any]
    statistical_results: Dict[str, Any]
    physics_results: Dict[str, Any]
    ai_explanations: Dict[str, Any]
    anomaly_map: Dict[str, Any]
    layer_data: Dict[str, Any]
    scientific_report: Dict[str, Any]
    system_status: Dict[str, Any]

@app.get("/")
async def root():
    return {
        "name": "ArcheoScope Demo Server",
        "purpose": "Detectar donde las explicaciones arqueológicas actuales fallan",
        "version": "1.0.0-demo",
        "status": "operational"
    }

@app.get("/status")
async def get_system_status():
    # Verificar estado de Ollama
    ai_status = await check_ollama_status()
    
    return {
        "backend_status": "operational",
        "ai_status": ai_status,
        "available_rules": ["ice_flow_consistency", "mass_balance", "thermal_equilibrium"],
        "supported_regions": ["demo", "synthetic"]
    }

async def check_ollama_status():
    """Verificar si Ollama está disponible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                return "available"
    except:
        pass
    return "offline"

async def generate_ai_explanation(analysis, request):
    """Generar explicación IA usando Ollama con contexto espacial"""
    try:
        # Obtener contexto espacial si está disponible
        spatial_context = getattr(request, 'spatial_context', None)
        area_km2 = analysis['region_info']['area_km2']
        
        # Determinar modo de análisis
        if spatial_context:
            analysis_mode = spatial_context.get('analysis_mode', 'scientific')
            is_exploratory = spatial_context.get('is_exploratory', False)
        else:
            # Determinar modo basado en área con umbrales REALISTAS
            if area_km2 <= 10:
                analysis_mode = 'fine'
                is_exploratory = False
            elif area_km2 <= 100:
                analysis_mode = 'medium'
                is_exploratory = False
            else:
                analysis_mode = 'exploratory'
                is_exploratory = True
        
        # Prompt científico adaptado al contexto espacial
        if is_exploratory:
            prompt = f"""IMPORTANTE: Área demasiado grande ({area_km2:.0f} km²) para análisis científico válido.

Como amplificador de hipótesis espaciales, no detector de verdades:

Región: {request.region_name} 
Contradicciones físicas: {len(analysis['physics_results']['contradictions'])}
Anomalías estadísticas: {len([r for r in analysis['statistical_results'].values() if r.get('anomaly_percentage', 0) > 2.0])}

Responde en 1-2 oraciones indicando que el área es demasiado extensa para conclusiones específicas y que se requiere subdivisión para análisis científico válido."""
        else:
            prompt = f"""Como amplificador de hipótesis espaciales para análisis glaciológico:

Región: {request.region_name} ({area_km2:.0f} km²)
Contradicciones físicas: {len(analysis['physics_results']['contradictions'])}
Anomalías estadísticas: {len([r for r in analysis['statistical_results'].values() if r.get('anomaly_percentage', 0) > 2.0])}

Explica en 2 oraciones qué procesos subglaciales específicos podrían causar estas anomalías en esta región delimitada, manteniendo tono probabilístico."""

        # Llamada a Ollama con timeout aumentado
        ollama_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b-instruct",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "num_predict": 150  # Limitar tokens para respuesta más rápida
                }
            },
            timeout=60  # Aumentar timeout para modelo local
        )
        
        if ollama_response.status_code == 200:
            ai_result = ollama_response.json()
            explanation = ai_result.get('response', '').strip()
            
            # Agregar contexto espacial a la respuesta
            spatial_note = ""
            if is_exploratory:
                spatial_note = "Análisis exploratorio de área extensa - resultados indican anomalías localizadas."
            elif analysis_mode == 'analytical':
                spatial_note = "Análisis espacialmente significativo con interpretación científica válida."
            else:
                spatial_note = "Análisis científico fino - resultados aptos para publicación."
            
            return {
                "ai_available": True,
                "explanation": explanation,
                "confidence_notes": f"Análisis generado por IA local (Ollama) - {spatial_note}",
                "suggestions": ["Verificar con datos de campo", "Considerar variabilidad temporal"] if not is_exploratory else ["Reducir área para análisis detallado", "Enfocar en subregiones críticas"],
                "limitations": "Basado en datos sintéticos para demostración",
                "mode": "ollama_ai",
                "model_used": "qwen2.5:3b-instruct",
                "spatial_context": {
                    "analysis_mode": analysis_mode,
                    "area_km2": area_km2,
                    "is_exploratory": is_exploratory
                }
            }
        else:
            raise Exception(f"Ollama error: {ollama_response.status_code}")
            
    except Exception as e:
        logger.warning(f"Error en IA: {e}")
        return {
            "ai_available": False,
            "explanation": "IA no disponible - análisis determinista aplicado",
            "mode": "error_fallback",
            "error": str(e)
        }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_region(request: RegionRequest):
    """Análisis de demostración de una región glaciológica"""
    
    logger.info(f"Analizando región demo: {request.region_name}")
    
    # Calcular área
    lat_range = request.lat_max - request.lat_min
    lon_range = request.lon_max - request.lon_min
    area_km2 = lat_range * lon_range * 111 * 85  # Aproximación
    
    # Generar datos sintéticos para demo
    height, width = 100, 100
    
    # Crear máscara de anomalías para demo
    np.random.seed(42)  # Reproducible
    anomaly_mask = np.zeros((height, width), dtype=int)
    
    # Añadir algunas anomalías estadísticas (naranja)
    statistical_anomalies = np.random.random((height, width)) < 0.15
    anomaly_mask[statistical_anomalies] = 1
    
    # Añadir algunas contradicciones físicas (rojo)
    physical_contradictions = np.random.random((height, width)) < 0.05
    anomaly_mask[physical_contradictions] = 2
    
    # Resultados estadísticos de demo
    statistical_results = {
        "velocity_vs_surface": {
            "correlation": 0.65,
            "anomaly_percentage": 15.2,
            "anomaly_pixels": int(np.sum(anomaly_mask == 1)),
            "rmse": 45.3,
            "valid_pixels": height * width
        },
        "velocity_vs_thickness": {
            "correlation": 0.78,
            "anomaly_percentage": 8.7,
            "anomaly_pixels": int(np.sum(anomaly_mask == 1) * 0.6),
            "rmse": 32.1,
            "valid_pixels": height * width
        }
    }
    
    # Resultados físicos de demo
    physics_results = {
        "evaluations": {
            "ice_flow_consistency": {
                "result": "INCONSISTENT",
                "confidence": 0.85,
                "severity": "HIGH",
                "affected_pixels": int(np.sum(anomaly_mask == 2)),
                "contradiction_details": "Velocidad de hielo inconsistente con gradiente de superficie"
            },
            "mass_balance": {
                "result": "CONSISTENT",
                "confidence": 0.92,
                "severity": "LOW",
                "affected_pixels": 0,
                "contradiction_details": ""
            }
        },
        "contradictions": [
            {
                "rule": "ice_flow_consistency",
                "severity": "HIGH",
                "details": "Velocidad de hielo inconsistente con gradiente de superficie",
                "pixels": int(np.sum(anomaly_mask == 2))
            }
        ],
        "summary": {
            "total_rules": 2,
            "consistent_rules": 1,
            "inconsistent_rules": 1
        }
    }
    
    # Explicaciones IA reales usando Ollama
    temp_analysis = {
        'region_info': {
            'area_km2': area_km2,
            'coordinates': {
                'lat_range': [request.lat_min, request.lat_max],
                'lon_range': [request.lon_min, request.lon_max]
            }
        },
        'statistical_results': statistical_results,
        'physics_results': physics_results
    }
    ai_explanations = await generate_ai_explanation(temp_analysis, request)
    
    # Si falla la IA, usar fallback determinista
    if not ai_explanations.get("ai_available", False):
        ai_explanations = {
            "ai_available": False,
            "explanation": "Análisis determinista aplicado. Las anomalías detectadas sugieren procesos subglaciales no modelados en la región analizada.",
            "mode": "deterministic_fallback"
        }
    
    # Mapa de anomalías
    anomaly_map = {
        "anomaly_mask": anomaly_mask.tolist(),
        "regions": [
            {
                "id": 1,
                "type": "critical",
                "area_km2": 150.5,
                "centroid": {"lat": (request.lat_min + request.lat_max) / 2, 
                           "lon": (request.lon_min + request.lon_max) / 2},
                "anomaly_type": "physical_contradiction",
                "severity": "HIGH"
            }
        ],
        "critical_regions": {
            "critical": [1],
            "secondary": [],
            "discarded": []
        },
        "legend": {
            "0": "consistent",
            "1": "statistical_anomaly",
            "2": "physical_contradiction"
        },
        "color_scheme": {
            "0": {"color": "#90EE90", "opacity": 0.2, "name": "Consistente"},
            "1": {"color": "#FFA500", "opacity": 0.6, "name": "Anomalía Estadística"},
            "2": {"color": "#FF4500", "opacity": 0.8, "name": "Contradicción Física"}
        },
        "statistics": {
            "total_pixels": height * width,
            "consistent_pixels": int(np.sum(anomaly_mask == 0)),
            "statistical_anomaly_pixels": int(np.sum(anomaly_mask == 1)),
            "physical_contradiction_pixels": int(np.sum(anomaly_mask == 2)),
            "consistent_percentage": float(np.sum(anomaly_mask == 0) / (height * width) * 100),
            "statistical_anomaly_percentage": float(np.sum(anomaly_mask == 1) / (height * width) * 100),
            "physical_contradiction_percentage": float(np.sum(anomaly_mask == 2) / (height * width) * 100)
        }
    }
    
    # Datos de capas
    layer_data = {
        "ice_velocity": {
            "min_value": 0.0,
            "max_value": 1500.0,
            "mean_value": 245.3,
            "shape": [height, width],
            "units": "m/year"
        },
        "ice_thickness": {
            "min_value": 0.0,
            "max_value": 3200.0,
            "mean_value": 850.7,
            "shape": [height, width],
            "units": "meters"
        },
        "bedrock_elevation": {
            "min_value": -2100.0,
            "max_value": 1200.0,
            "mean_value": -450.2,
            "shape": [height, width],
            "units": "meters"
        }
    }
    
    # Reporte científico
    scientific_report = {
        "title": f"Análisis de Coherencia Subglacial: {request.region_name}",
        "summary": {
            "region_analyzed": request.region_name,
            "analysis_date": "2024-01-20",
            "area_km2": area_km2,
            "statistical_anomalies_detected": 2,
            "physics_contradictions_detected": 1,
            "ai_explanation_available": False
        },
        "key_findings": [
            f"Región de {area_km2:,.0f} km² analizada con resolución {request.resolution_m}m",
            "Desacople significativo entre velocidad de hielo y controles geométricos detectado",
            "Contradicción física identificada en reglas de flujo de hielo",
            "Análisis espacial revela 1 región crítica para investigación detallada"
        ],
        "methodology": {
            "statistical_analysis": "Comparación multi-capa con detección de anomalías espaciales",
            "physics_evaluation": "Reglas deterministas basadas en principios glaciológicos",
            "spatial_clustering": "Agrupación de anomalías en regiones coherentes",
            "ai_assistance": "Modo demo - análisis determinista"
        }
    }
    
    # Estado del sistema
    system_status = {
        "analysis_completed": True,
        "processing_time_seconds": "<5",
        "ai_used": False,
        "rules_evaluated": 2,
        "anomalies_detected": 1
    }
    
    return AnalysisResponse(
        region_info={
            "name": request.region_name,
            "coordinates": {
                "lat_range": [request.lat_min, request.lat_max],
                "lon_range": [request.lon_min, request.lon_max]
            },
            "resolution_m": request.resolution_m,
            "area_km2": area_km2
        },
        statistical_results=statistical_results,
        physics_results=physics_results,
        ai_explanations=ai_explanations,
        anomaly_map=anomaly_map,
        layer_data=layer_data,
        scientific_report=scientific_report,
        system_status=system_status
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)