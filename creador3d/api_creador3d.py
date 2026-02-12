#!/usr/bin/env python3
"""
API Creador3D - Generación 3D Experimental
===========================================

API secundaria para explorar nuevas funcionalidades de generación 3D.
Separada de la API científica de ArcheoScope.

Puerto: 8004 (diferente de ArcheoScope en 8003)
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
from pathlib import Path
import sys

# Agregar paths necesarios
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Importar generadores del backend (reutilizamos la lógica)
from culturally_constrained_mig import CulturallyConstrainedMIG
from morphological_repository import MorphologicalClass, MorphologicalRepository

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# Crear app FastAPI
app = FastAPI(
    title="Creador3D API",
    description="API experimental de generación 3D - Separada de ArcheoScope científico",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directorio de salida
OUTPUT_DIR = project_root / "creador3d_models"
OUTPUT_DIR.mkdir(exist_ok=True)

# Instancia del generador
mig = CulturallyConstrainedMIG(output_dir=str(OUTPUT_DIR))
morph_repo = MorphologicalRepository()


# ============================================================================
# MODELOS DE DATOS
# ============================================================================

class GenerateFromDescriptionRequest(BaseModel):
    """Request para generar desde descripción textual."""
    description: str
    output_name: Optional[str] = None
    style: Optional[str] = "realistic"  # realistic, stylized, abstract


class GenerateFromParametersRequest(BaseModel):
    """Request para generar desde parámetros geométricos."""
    height_m: float
    width_m: float
    depth_m: Optional[float] = None
    shape_type: str  # pyramid, statue, platform, custom
    output_name: Optional[str] = None
    
    # Parámetros opcionales
    num_levels: Optional[int] = None
    has_stairs: Optional[bool] = False
    has_temple: Optional[bool] = False
    color: Optional[str] = None


class GenerateFromMorphologyRequest(BaseModel):
    """Request para generar desde clase morfológica."""
    morphological_class: str  # moai, sphinx, pyramid_mesoamerican, etc.
    scale_factor: Optional[float] = 1.0
    output_name: Optional[str] = None
    
    # Override de parámetros
    height_m: Optional[float] = None
    width_m: Optional[float] = None


class CustomGeometryRequest(BaseModel):
    """Request para geometría completamente custom."""
    vertices: List[List[float]]  # [[x, y, z], ...]
    faces: List[List[int]]  # [[v1, v2, v3], ...]
    output_name: Optional[str] = None


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "api": "Creador3D",
        "version": "0.1.0",
        "description": "API experimental de generación 3D",
        "status": "operational",
        "endpoints": {
            "generate_from_description": "POST /generate/description",
            "generate_from_parameters": "POST /generate/parameters",
            "generate_from_morphology": "POST /generate/morphology",
            "generate_custom": "POST /generate/custom",
            "get_model": "GET /model/{filename}",
            "list_morphologies": "GET /morphologies"
        }
    }


@app.get("/status")
async def status():
    """Estado de la API."""
    return {
        "status": "operational",
        "output_dir": str(OUTPUT_DIR),
        "models_generated": len(list(OUTPUT_DIR.glob("*.png"))),
        "morphologies_available": len(morph_repo.repository)
    }


@app.get("/morphologies")
async def list_morphologies():
    """Listar clases morfológicas disponibles."""
    
    morphologies = []
    for morph_class, invariants in morph_repo.repository.items():
        morphologies.append({
            "class": morph_class.value,
            "origin": invariants.cultural_origin,
            "height_width_ratio": invariants.height_to_width_ratio,
            "confidence": invariants.confidence,
            "samples": invariants.source_samples
        })
    
    return {
        "total": len(morphologies),
        "morphologies": morphologies
    }


@app.post("/generate/description")
async def generate_from_description(request: GenerateFromDescriptionRequest):
    """
    Generar modelo 3D desde descripción textual.
    
    EXPERIMENTAL: Usa análisis de texto para inferir parámetros.
    """
    
    logger.info(f"🎨 Generando desde descripción: {request.description}")
    
    try:
        # TODO: Implementar análisis de descripción con IA
        # Por ahora, retorna placeholder
        
        return {
            "status": "not_implemented",
            "message": "Generación desde descripción textual en desarrollo",
            "description": request.description,
            "suggestion": "Usa /generate/parameters o /generate/morphology por ahora"
        }
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/parameters")
async def generate_from_parameters(request: GenerateFromParametersRequest):
    """
    Generar modelo 3D desde parámetros geométricos directos.
    
    Permite control total sobre dimensiones y características.
    """
    
    logger.info(f"🎨 Generando desde parámetros: {request.shape_type}")
    
    try:
        # Preparar datos para el generador
        geometry_data = {
            'height_m': request.height_m,
            'base_width_m': request.width_m,
            'base_length_m': request.depth_m or request.width_m,
            'shape_type': request.shape_type
        }
        
        # Determinar clase morfológica según shape_type
        morph_class_map = {
            'pyramid': MorphologicalClass.PYRAMID_MESOAMERICAN,
            'statue': MorphologicalClass.EGYPTIAN_STATUE,
            'platform': MorphologicalClass.TEMPLE_PLATFORM,
            'moai': MorphologicalClass.MOAI,
            'sphinx': MorphologicalClass.SPHINX
        }
        
        morph_class = morph_class_map.get(
            request.shape_type.lower(),
            MorphologicalClass.PYRAMID_MESOAMERICAN
        )
        
        # Generar nombre de salida
        output_name = request.output_name or f"custom_{request.shape_type}_{int(time.time())}"
        
        # Generar modelo
        result = mig._generate_culturally_constrained_model(
            geometry=geometry_data,
            morph_class=morph_class
        )
        
        # Renderizar
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        import numpy as np
        
        png_path = OUTPUT_DIR / f"{output_name}.png"
        
        fig = plt.figure(figsize=(12, 10), facecolor='#0a0a0a')
        ax = fig.add_subplot(111, projection='3d', facecolor='#0a0a0a')
        
        # Color según request o default
        face_color = request.color or '#A0826D'
        
        poly_collection = Poly3DCollection(
            result['vertices'][result['faces']],
            alpha=0.92,
            facecolor=face_color,
            edgecolor='#5a4a3d',
            linewidths=0.3
        )
        
        ax.add_collection3d(poly_collection)
        
        vertices = result['vertices']
        max_range = np.ptp(vertices, axis=0).max() / 2
        mid = vertices.mean(axis=0)
        
        ax.set_xlim(mid[0] - max_range * 1.1, mid[0] + max_range * 1.1)
        ax.set_ylim(mid[1] - max_range * 1.1, mid[1] + max_range * 1.1)
        ax.set_zlim(0, vertices[:, 2].max() * 1.05)
        
        ax.view_init(elev=25, azim=45)
        ax.set_xlabel('X (m)', color='#888888')
        ax.set_ylabel('Y (m)', color='#888888')
        ax.set_zlabel('Z (m)', color='#888888')
        
        title = (
            f"CREADOR3D - Modelo Generado\n"
            f"Tipo: {request.shape_type.upper()} | "
            f"Dimensiones: {request.height_m:.1f}m × {request.width_m:.1f}m\n"
            f"Volumen: {result['volume_m3']:.2f} m³"
        )
        ax.set_title(title, color='#CCCCCC', fontsize=10, pad=20)
        
        plt.savefig(png_path, bbox_inches='tight', dpi=200, facecolor='#0a0a0a')
        plt.close()
        
        # Export OBJ
        obj_path = OUTPUT_DIR / f"{output_name}.obj"
        import trimesh
        mesh = trimesh.Trimesh(vertices=result['vertices'], faces=result['faces'])
        mesh.export(str(obj_path))
        
        return {
            'success': True,
            'png_filename': png_path.name,
            'obj_filename': obj_path.name,
            'png_path': str(png_path),
            'obj_path': str(obj_path),
            'shape_type': request.shape_type,
            'dimensions': {
                'height_m': request.height_m,
                'width_m': request.width_m,
                'depth_m': request.depth_m or request.width_m
            },
            'volume_m3': result['volume_m3']
        }
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/morphology")
async def generate_from_morphology(request: GenerateFromMorphologyRequest):
    """
    Generar modelo 3D desde clase morfológica conocida.
    
    Usa las clases del repositorio morfológico de ArcheoScope.
    """
    
    logger.info(f"🎨 Generando desde morfología: {request.morphological_class}")
    
    try:
        # Mapear string a enum
        morph_class_map = {
            'moai': MorphologicalClass.MOAI,
            'sphinx': MorphologicalClass.SPHINX,
            'egyptian_statue': MorphologicalClass.EGYPTIAN_STATUE,
            'colossus': MorphologicalClass.COLOSSUS,
            'pyramid_mesoamerican': MorphologicalClass.PYRAMID_MESOAMERICAN,
            'temple_platform': MorphologicalClass.TEMPLE_PLATFORM,
            'stela_maya': MorphologicalClass.STELA_MAYA
        }
        
        morph_class = morph_class_map.get(request.morphological_class.lower())
        
        if not morph_class:
            raise HTTPException(
                status_code=400,
                detail=f"Clase morfológica no reconocida: {request.morphological_class}"
            )
        
        # Obtener invariantes
        invariants = morph_repo.get_morphological_constraints(morph_class)
        
        # Dimensiones base (escaladas)
        base_height = (request.height_m or 10.0) * request.scale_factor
        base_width = base_height / invariants.height_to_width_ratio
        
        # Preparar geometría
        geometry_data = {
            'height_m': base_height,
            'base_width_m': base_width,
            'base_length_m': base_width,
            'head_to_body_ratio': invariants.head_to_body_ratio
        }
        
        # Generar nombre
        output_name = request.output_name or f"{morph_class.value}_{int(time.time())}"
        
        # Generar usando el MIG
        archeoscope_data = {
            'scale_invariance': 0.90,
            'angular_consistency': 0.88,
            'coherence_3d': 0.85,
            'estimated_area_m2': base_width ** 2,
            'estimated_height_m': base_height
        }
        
        result = mig.infer_culturally_constrained_geometry(
            archeoscope_data=archeoscope_data,
            output_name=output_name,
            use_ai=False
        )
        
        return {
            'success': True,
            'png_filename': Path(result['png']).name,
            'obj_filename': Path(result['obj']).name,
            'png_path': result['png'],
            'obj_path': result['obj'],
            'morphological_class': result['morphological_class'],
            'cultural_origin': result['cultural_origin'],
            'confidence': result['confidence'],
            'volume_m3': result['volume_m3'],
            'scale_factor': request.scale_factor
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/custom")
async def generate_custom(request: CustomGeometryRequest):
    """
    Generar modelo 3D desde geometría completamente custom.
    
    Permite especificar vértices y caras directamente.
    """
    
    logger.info(f"🎨 Generando geometría custom")
    
    try:
        import trimesh
        import numpy as np
        
        # Crear mesh desde vértices y caras
        vertices = np.array(request.vertices)
        faces = np.array(request.faces)
        
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        # Generar nombre
        output_name = request.output_name or f"custom_{int(time.time())}"
        
        # Export OBJ
        obj_path = OUTPUT_DIR / f"{output_name}.obj"
        mesh.export(str(obj_path))
        
        # Renderizar PNG
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        
        png_path = OUTPUT_DIR / f"{output_name}.png"
        
        fig = plt.figure(figsize=(12, 10), facecolor='#0a0a0a')
        ax = fig.add_subplot(111, projection='3d', facecolor='#0a0a0a')
        
        poly_collection = Poly3DCollection(
            vertices[faces],
            alpha=0.90,
            facecolor='#8B7355',
            edgecolor='#4a4a4a',
            linewidths=0.3
        )
        
        ax.add_collection3d(poly_collection)
        
        max_range = np.ptp(vertices, axis=0).max() / 2
        mid = vertices.mean(axis=0)
        
        ax.set_xlim(mid[0] - max_range * 1.1, mid[0] + max_range * 1.1)
        ax.set_ylim(mid[1] - max_range * 1.1, mid[1] + max_range * 1.1)
        ax.set_zlim(vertices[:, 2].min(), vertices[:, 2].max() * 1.05)
        
        ax.view_init(elev=25, azim=45)
        ax.set_title("CREADOR3D - Geometría Custom", color='#CCCCCC', fontsize=12)
        
        plt.savefig(png_path, bbox_inches='tight', dpi=200, facecolor='#0a0a0a')
        plt.close()
        
        return {
            'success': True,
            'png_filename': png_path.name,
            'obj_filename': obj_path.name,
            'png_path': str(png_path),
            'obj_path': str(obj_path),
            'vertices_count': len(vertices),
            'faces_count': len(faces),
            'volume_m3': float(mesh.volume) if hasattr(mesh, 'volume') else 0.0
        }
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model/{filename}")
async def get_model(filename: str):
    """Servir archivo de modelo (PNG o OBJ)."""
    
    try:
        file_path = OUTPUT_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
        media_type = "image/png" if filename.endswith('.png') else "application/octet-stream"
        
        return FileResponse(
            path=str(file_path),
            media_type=media_type,
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Evento de inicio."""
    logger.info("="*80)
    logger.info("🎨 CREADOR3D API - Iniciando")
    logger.info("="*80)
    logger.info(f"📁 Directorio de salida: {OUTPUT_DIR}")
    logger.info(f"🏛️  Clases morfológicas: {len(morph_repo.repository)}")
    logger.info("="*80)


if __name__ == "__main__":
    import uvicorn
    import time
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8004,
        log_level="info"
    )
