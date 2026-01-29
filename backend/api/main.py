#!/usr/bin/env python3
"""
API principal para ArcheoScope - Archaeological Remote Sensing Engine.
VERSIÓN LIMPIA - Solo endpoints funcionales y críticos.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path
import logging
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el backend al path
sys.path.append(str(Path(__file__).parent.parent))

def convert_numpy_types(obj):
    """Convertir tipos numpy a tipos Python nativos para serialización JSON."""
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

from rules.archaeological_rules import ArchaeologicalRulesEngine
from ai.archaeological_assistant import ArchaeologicalAssistant
from explainability.scientific_explainer import ScientificExplainer
from volumetric.geometric_inference_engine import GeometricInferenceEngine
from environment_classifier import EnvironmentClassifier
from core_anomaly_detector import CoreAnomalyDetector
from validation.data_source_transparency import DataSourceTransparency
from database import db as database_connection

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="ArcheoScope API",
    description="""
# ArcheoScope - Archaeological Remote Sensing Engine

Sistema científico de detección de persistencias espaciales mediante sensores remotos.

## Endpoints Principales

### Análisis Científico
- `POST /api/scientific/analyze` - Análisis científico completo (pipeline de 7 fases)
- `GET /api/scientific/analyses/recent` - Consultar análisis recientes
- `GET /api/scientific/analyses/{id}` - Consultar análisis específico
- `GET /api/scientific/analyses/by-region/{name}` - Consultar análisis por región

### Sistema
- `GET /` - Información del sistema
- `GET /status` - Estado operacional
- `GET /status/detailed` - Estado detallado con instrumentos

### Datos y Validación
- `GET /data-sources` - Fuentes de datos utilizadas
- `GET /lidar-benchmark` - Datos LIDAR de referencia
- `GET /instruments/archaeological-value` - Matriz de valor arqueológico

### Candidatos
- `GET /archaeological-sites/candidates` - Candidatos detectados

### Volumétrico
- `GET /volumetric/sites/catalog` - Catálogo de sitios con datos volumétricos

## Filosofía

- **100% Determinístico**: Sin aleatoriedad en análisis científicos
- **Transparencia Total**: Trazabilidad completa de datos
- **Validación Rigurosa**: Comparación con sitios arqueológicos verificados
- **IA Solo para Explicaciones**: No para decisiones científicas
    """,
    version="2.0.0-clean",
    openapi_tags=[
        {"name": "Status", "description": "Estado del sistema"},
        {"name": "Scientific Analysis", "description": "Análisis científico completo"},
        {"name": "Data", "description": "Fuentes de datos y validación"},
        {"name": "Candidates", "description": "Candidatos arqueológicos"},
        {"name": "Volumetric", "description": "Análisis volumétrico LIDAR"}
    ]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Modelos
class RegionRequest(BaseModel):
    """Solicitud de análisis arqueológico"""
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    resolution_m: Optional[int] = 1000
    region_name: Optional[str] = "Unknown Region"

class SystemStatus(BaseModel):
    """Estado del sistema"""
    backend_status: str
    ai_status: str
    available_rules: List[str]

# Estado global
system_components = {
    'rules_engine': None,
    'ai_assistant': None,
    'explainer': None,
    'geometric_engine': None,
    'environment_classifier': None,
    'core_anomaly_detector': None,
    'transparency': None
}

def initialize_system():
    """Inicializar componentes del sistema."""
    try:
        system_components['rules_engine'] = ArchaeologicalRulesEngine()
        system_components['ai_assistant'] = ArchaeologicalAssistant()
        system_components['explainer'] = ScientificExplainer()
        system_components['geometric_engine'] = GeometricInferenceEngine()
        system_components['environment_classifier'] = EnvironmentClassifier()
        system_components['core_anomaly_detector'] = CoreAnomalyDetector(
            environment_classifier=system_components.get('environment_classifier')
        )
        system_components['transparency'] = DataSourceTransparency()
        
        logger.info("✅ Sistema ArcheoScope inicializado correctamente")
        return True
    except Exception as e:
        logger.error(f"❌ Error inicializando ArcheoScope: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Inicializar sistema al arrancar."""
    initialize_system()
    
    # Inicializar BD
    try:
        await database_connection.connect()
        site_count = await database_connection.count_sites()
        logger.info(f"✅ Base de datos conectada - {site_count:,} sitios disponibles")
    except Exception as e:
        logger.error(f"❌ Error conectando a BD: {e}")
    
    # Inicializar pool para endpoint científico
    try:
        from api.scientific_endpoint import init_db_pool, initialize_timt_engine
        await init_db_pool()
        initialize_timt_engine()  # Inicializar TIMT para fusión transparente
        logger.info("✅ Motor TIMT inicializado para fusión transparente")
    except Exception as e:
        logger.error(f"❌ Error inicializando pool científico o TIMT: {e}")
    
    # Inicializar pool para TIMT
    try:
        from api.timt_endpoints import init_timt_db_pool
        await init_timt_db_pool()
    except Exception as e:
        logger.error(f"❌ Error inicializando pool TIMT: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cerrar conexiones."""
    try:
        await database_connection.close()
        logger.info("✅ Conexión a BD cerrada")
    except Exception as e:
        logger.error(f"❌ Error cerrando BD: {e}")

# ============================================================================
# ENDPOINTS FUNCIONALES
# ============================================================================

@app.get("/", tags=["Status"])
async def root():
    """Información del sistema."""
    return {
        "name": "ArcheoScope - Archaeological Remote Sensing Engine",
        "version": "2.0.0-clean",
        "status": "operational",
        "paradigm": "spatial_persistence_detection"
    }

@app.get("/status", response_model=SystemStatus, tags=["Status"])
async def get_system_status():
    """Estado operacional del sistema."""
    backend_status = "operational" if all(system_components.values()) else "limited"
    ai_assistant = system_components.get('ai_assistant')
    ai_status = "available" if ai_assistant and ai_assistant.is_available else "offline"
    rules_engine = system_components.get('rules_engine')
    available_rules = [rule.name for rule in rules_engine.rules] if rules_engine else []
    
    return SystemStatus(
        backend_status=backend_status,
        ai_status=ai_status,
        available_rules=available_rules
    )

@app.get("/status/detailed", tags=["Status"])
async def get_detailed_system_status():
    """Estado detallado del sistema con todos los componentes."""
    ai_assistant = system_components.get('ai_assistant')
    
    return {
        "backend_status": "operational" if all(system_components.values()) else "limited",
        "ai_status": "available" if ai_assistant and ai_assistant.is_available else "offline",
        "ai_model": (ai_assistant.openrouter_model if ai_assistant.openrouter_enabled 
                    else ai_assistant.ollama_model) if ai_assistant else "none",
        "system_components": {
            "rules_engine": "operational" if system_components.get('rules_engine') else "offline",
            "ai_assistant": "operational" if system_components.get('ai_assistant') else "offline",
            "explainer": "operational" if system_components.get('explainer') else "offline",
            "geometric_engine": "operational" if system_components.get('geometric_engine') else "offline",
            "environment_classifier": "operational" if system_components.get('environment_classifier') else "offline",
            "core_anomaly_detector": "operational" if system_components.get('core_anomaly_detector') else "offline"
        },
        "capabilities": {
            "scientific_analysis": True,
            "volumetric_inference": bool(system_components.get('geometric_engine')),
            "environment_classification": bool(system_components.get('environment_classifier')),
            "ai_explanations": bool(ai_assistant and ai_assistant.is_available)
        }
    }

@app.get("/data-sources", tags=["Data"])
async def get_data_sources():
    """Información sobre fuentes de datos utilizadas."""
    transparency = system_components.get('transparency')
    if not transparency:
        # Retornar datos básicos si el componente no está disponible
        return {
            "sources": {
                "sentinel2": {
                    "name": "Sentinel-2",
                    "provider": "ESA Copernicus",
                    "type": "optical_multispectral",
                    "resolution_m": 10
                },
                "landsat8": {
                    "name": "Landsat 8",
                    "provider": "NASA/USGS",
                    "type": "optical_thermal",
                    "resolution_m": 30
                },
                "icesat2": {
                    "name": "ICESat-2",
                    "provider": "NASA",
                    "type": "lidar_altimetry",
                    "resolution_m": 0.7
                }
            },
            "total_sources": 3,
            "note": "Lista básica de fuentes - componente de transparencia no disponible"
        }
    
    try:
        return transparency.get_all_sources()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo fuentes: {str(e)}")

@app.get("/lidar-benchmark", tags=["Data"])
async def get_lidar_benchmark_data():
    """Datos LIDAR de referencia para benchmarking."""
    return {
        "benchmark_sites": {
            "angkor_wat": {
                "name": "Angkor Wat Archaeological Park",
                "location": "Cambodia",
                "coordinates": [13.4125, 103.8670],
                "lidar_type": "airborne_als",
                "resolution_cm": 50,
                "acquisition_year": 2015,
                "data_source": "Khmer Archaeology LiDAR Consortium",
                "reference": "Evans et al. (2013) PNAS"
            },
            "caracol": {
                "name": "Caracol Maya Site",
                "location": "Belize",
                "coordinates": [16.7631, -89.1167],
                "lidar_type": "airborne_als",
                "resolution_cm": 25,
                "acquisition_year": 2009,
                "data_source": "NCALM",
                "reference": "Chase et al. (2011) Journal of Archaeological Science"
            }
        },
        "total_sites": 2,
        "purpose": "Validación de algoritmos de detección volumétrica"
    }

@app.get("/instruments/archaeological-value", tags=["Data"])
async def get_archaeological_value_matrix():
    """Matriz de valor arqueológico de instrumentos por ambiente."""
    return {
        "matrix": {
            "desert": {
                "Sentinel-2 NDVI": 0.85,
                "Landsat 8 Thermal": 0.90,
                "MODIS LST": 0.75,
                "Sentinel-1 SAR": 0.80,
                "PALSAR-2": 0.70
            },
            "forest": {
                "OpenTopography": 0.95,
                "Sentinel-1 SAR": 0.85,
                "PALSAR-2": 0.90,
                "Sentinel-2 NDVI": 0.60
            },
            "polar_ice": {
                "ICESat-2": 0.95,
                "Sentinel-1 SAR": 0.90,
                "PALSAR-2": 0.85,
                "MODIS LST": 0.70
            }
        },
        "description": "Valor arqueológico de cada instrumento por tipo de ambiente (0-1)"
    }

@app.get("/archaeological-sites/candidates", tags=["Candidates"])
async def get_archeoscope_candidate_sites():
    """Candidatos arqueológicos detectados por ArcheoScope."""
    return {
        "total_candidates": 0,
        "candidates": [],
        "note": "Los candidatos se generan mediante análisis científico en /api/scientific/analyze"
    }

@app.get("/volumetric/sites/catalog", tags=["Volumetric"])
async def get_sites_catalog():
    """Catálogo de sitios con datos volumétricos LIDAR."""
    return {
        "total_sites": 2,
        "sites": {
            "angkor_wat": {
                "name": "Angkor Wat Archaeological Park",
                "coordinates": [13.4125, 103.8670],
                "site_type": "archaeological_confirmed",
                "lidar_type": "airborne_als",
                "resolution_cm": 50,
                "acquisition_year": 2015
            },
            "caracol": {
                "name": "Caracol Maya Site",
                "coordinates": [16.7631, -89.1167],
                "site_type": "archaeological_confirmed",
                "lidar_type": "airborne_als",
                "resolution_cm": 25,
                "acquisition_year": 2009
            }
        }
    }

@app.post("/test-analyze", tags=["Status"])
async def test_analyze(request: RegionRequest):
    """Endpoint de test para verificar conectividad."""
    return {
        "status": "ok",
        "region": request.region_name,
        "message": "Backend funcionando correctamente"
    }

# ============================================================================
# INCLUIR ROUTER CIENTÍFICO (CRÍTICO)
# ============================================================================

try:
    from api.scientific_endpoint import router as scientific_router
    app.include_router(
        scientific_router,
        prefix="/api/scientific",
        tags=["Scientific Analysis"]
    )
    logger.info("✅ Router científico incluido en /api/scientific")
except ImportError as e:
    logger.error(f"❌ No se pudo cargar router científico: {e}")

# ============================================================================
# INCLUIR ROUTER TIMT (TERRITORIAL INFERENTIAL TOMOGRAPHY)
# ============================================================================

try:
    import sys
    from pathlib import Path
    
    # Asegurar que backend esté en el path
    backend_path = Path(__file__).parent.parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    
    from api.timt_endpoints import timt_router, initialize_timt_engine
    
    # Inicializar motor TIMT
    initialize_timt_engine()
    
    app.include_router(
        timt_router,
        tags=["Territorial Inferential Tomography"]
    )
    logger.info("✅ Router TIMT incluido en /timt")
except ImportError as e:
    logger.error(f"❌ No se pudo cargar router TIMT: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    logger.error(f"❌ Error inicializando motor TIMT: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# INCLUIR ROUTER ANOMALY VISUALIZATION (NUEVO)
# ============================================================================

try:
    from api.anomaly_visualization_endpoint import router as anomaly_viz_router
    
    app.include_router(
        anomaly_viz_router,
        tags=["Anomaly Visualization"]
    )
    logger.info("✅ Router Anomaly Visualization incluido")
except ImportError as e:
    logger.error(f"❌ No se pudo cargar router Anomaly Visualization: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    logger.error(f"❌ Error inicializando Anomaly Visualization: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# ENDPOINT /analyze PRINCIPAL (MANTENER PARA COMPATIBILIDAD)
# ============================================================================

# TODO: Implementar /analyze principal o redirigir a /api/scientific/analyze

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
