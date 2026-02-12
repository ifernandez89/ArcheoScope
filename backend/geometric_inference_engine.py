#!/usr/bin/env python3
"""
MIG - Motor de Inferencia Geométrica (Geometric Inference Engine)
==================================================================

PARADIGMA:
"La IA NO genera vértices. La IA define REGLAS GEOMÉTRICAS. El motor las ejecuta."

Pipeline:
1. Análisis de coherencia espacial (ArcheoScope data)
2. Razonamiento geométrico (Ollama/Qwen + HRM)
3. Inferencia de reglas geométricas
4. Generación procedural de geometría
5. Render a PNG (vista 3D)

Stack:
- trimesh: Geometría 3D procedural
- matplotlib: Render 3D a PNG
- numpy: Operaciones geométricas
- Ollama/Qwen: Razonamiento geométrico
"""

import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class StructureClass(Enum):
    """Clases estructurales inferibles."""
    PYRAMIDAL = "pyramidal"
    STEPPED_PLATFORM = "stepped_platform"
    MEGALITHIC_MONUMENT = "megalithic_monument"
    MONOLITHIC_ANTHROPOFORM = "monolithic_anthropoform"  # Tipo Moai
    ORTHOGONAL_NETWORK = "orthogonal_network"
    MOUND_EMBANKMENT = "mound_embankment"
    LINEAR_STRUCTURE = "linear_structure"
    UNDEFINED = "undefined"


class SymmetryType(Enum):
    """Tipos de simetría detectables."""
    AXIAL = "axial"
    BILATERAL = "bilateral"
    RADIAL = "radial"
    NONE = "none"


@dataclass
class GeometricRules:
    """
    Reglas geométricas inferidas (NO vértices directos).
    La IA define ESTO. El motor lo ejecuta.
    """
    structure_class: StructureClass
    base_shape: str  # "square", "rectangular", "circular", "irregular"
    
    # Dimensiones estimadas
    base_length_m: float
    base_width_m: float
    height_m: float
    
    # Propiedades geométricas
    symmetry: SymmetryType
    terracing: bool
    levels: int
    slope_angle_deg: float
    
    # Coherencia espacial (de ArcheoScope)
    scale_invariance: float
    angular_consistency: float
    coherence_3d: float
    
    # Metadatos
    confidence: float
    uncertainty: float
    material_profile: str  # "homogeneous_stone", "earth_fill", "mixed"


@dataclass
class GeometricModel:
    """Modelo geométrico 3D generado."""
    vertices: np.ndarray  # (N, 3) array
    faces: np.ndarray     # (M, 3) array de índices
    normals: np.ndarray   # (M, 3) array de normales
    
    # Metadatos
    volume_m3: float
    surface_area_m2: float
    bounding_box: Tuple[float, float, float]
    
    # Reglas usadas
    rules: GeometricRules


class GeometricInferenceEngine:
    """
    Motor de Inferencia Geométrica.
    
    Convierte datos de coherencia espacial en modelos 3D.
    """
    
    def __init__(self, output_dir: str = "geometric_models"):
        # Usar ruta absoluta
        if not Path(output_dir).is_absolute():
            # Si es relativa, hacerla relativa al directorio del proyecto
            project_root = Path(__file__).parent.parent
            output_dir = str(project_root / output_dir)
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"🧠 MIG inicializado - Output: {self.output_dir.absolute()}")
    
    def infer_geometric_rules(self, 
                             archeoscope_data: Dict[str, Any],
                             use_ai_reasoning: bool = True) -> GeometricRules:
        """
        ETAPA 1: Inferir reglas geométricas desde datos ArcheoScope.
        
        La IA (Ollama/Qwen) razona sobre los datos y define reglas.
        """
        
        logger.info("🧠 Infiriendo reglas geométricas...")
        
        # Extraer métricas clave
        scale_inv = archeoscope_data.get('scale_invariance', 0.0)
        angular_cons = archeoscope_data.get('angular_consistency', 0.0)
        coherence_3d = archeoscope_data.get('coherence_3d', 0.0)
        sar_rigidity = archeoscope_data.get('sar_rigidity', 0.0)
        stratification = archeoscope_data.get('stratification_index', 0.0)
        
        # RAZONAMIENTO GEOMÉTRICO (aquí entra Ollama/Qwen)
        if use_ai_reasoning:
            rules = self._ai_geometric_reasoning(archeoscope_data)
        else:
            rules = self._heuristic_geometric_reasoning(archeoscope_data)
        
        logger.info(f"   ✅ Reglas inferidas: {rules.structure_class.value}")
        logger.info(f"   📐 Dimensiones: {rules.base_length_m}m × {rules.base_width_m}m × {rules.height_m}m")
        logger.info(f"   🎯 Confianza: {rules.confidence:.3f}")
        
        return rules
    
    def _ai_geometric_reasoning(self, data: Dict[str, Any]) -> GeometricRules:
        """
        Razonamiento geométrico con IA (Ollama/Qwen).
        
        La IA decide:
        - Qué clase estructural es más probable
        - Qué reglas geométricas aplicar
        - Qué parámetros usar
        """
        
        # Preparar prompt para Ollama
        prompt = self._build_geometric_reasoning_prompt(data)
        
        try:
            # Llamar a Ollama (si está disponible)
            from backend.hrm.hrm_runner import generate_response_ollama
            
            response = generate_response_ollama(prompt, temperature=0.1)
            
            # Parsear respuesta JSON
            rules_dict = json.loads(response)
            
            return self._parse_ai_rules(rules_dict, data)
            
        except Exception as e:
            logger.warning(f"⚠️ AI reasoning falló: {e}, usando heurísticas")
            return self._heuristic_geometric_reasoning(data)
    
    def _build_geometric_reasoning_prompt(self, data: Dict[str, Any]) -> str:
        """Construir prompt para razonamiento geométrico."""
        
        return f"""TAREA: Inferencia Geométrica desde Datos de Teledetección

DATOS DE ENTRADA:
- Scale Invariance: {data.get('scale_invariance', 0):.3f}
- Angular Consistency: {data.get('angular_consistency', 0):.3f}
- Coherencia 3D: {data.get('coherence_3d', 0):.3f}
- SAR Rigidity: {data.get('sar_rigidity', 0):.3f}
- Stratification Index: {data.get('stratification_index', 0):.3f}
- Estimated Area: {data.get('estimated_area_m2', 0):.0f} m²

REGLAS DE INFERENCIA:
1. Scale Invariance > 0.9 + Angular Consistency > 0.9 → Estructura geométrica regular
2. Stratification > 0.5 → Estructura escalonada/terrazas
3. SAR Rigidity > 0.85 → Material compacto (piedra/mampostería)
4. Coherencia 3D > 0.8 → Volumen integrado (no natural)

RESTRICCIONES:
- NO inventar detalles arquitectónicos
- NO asumir función cultural
- SOLO geometría inferible desde datos físicos
- Incertidumbre explícita

OUTPUT (JSON):
{{
  "structure_class": "pyramidal|stepped_platform|megalithic_monument|mound_embankment|undefined",
  "base_shape": "square|rectangular|circular|irregular",
  "base_length_m": <float>,
  "base_width_m": <float>,
  "height_m": <float>,
  "symmetry": "axial|bilateral|radial|none",
  "terracing": <bool>,
  "levels": <int>,
  "slope_angle_deg": <float>,
  "confidence": <float 0-1>,
  "reasoning": "<explicación breve>"
}}"""
    
    def _parse_ai_rules(self, rules_dict: Dict[str, Any], data: Dict[str, Any]) -> GeometricRules:
        """Parsear reglas desde respuesta de IA."""
        
        return GeometricRules(
            structure_class=StructureClass(rules_dict.get('structure_class', 'undefined')),
            base_shape=rules_dict.get('base_shape', 'square'),
            base_length_m=rules_dict.get('base_length_m', 100.0),
            base_width_m=rules_dict.get('base_width_m', 100.0),
            height_m=rules_dict.get('height_m', 50.0),
            symmetry=SymmetryType(rules_dict.get('symmetry', 'axial')),
            terracing=rules_dict.get('terracing', False),
            levels=rules_dict.get('levels', 1),
            slope_angle_deg=rules_dict.get('slope_angle_deg', 45.0),
            scale_invariance=data.get('scale_invariance', 0.0),
            angular_consistency=data.get('angular_consistency', 0.0),
            coherence_3d=data.get('coherence_3d', 0.0),
            confidence=rules_dict.get('confidence', 0.5),
            uncertainty=1.0 - rules_dict.get('confidence', 0.5),
            material_profile="homogeneous_stone"
        )
    
    def _heuristic_geometric_reasoning(self, data: Dict[str, Any]) -> GeometricRules:
        """
        Razonamiento geométrico heurístico (fallback sin IA).
        """
        
        scale_inv = data.get('scale_invariance', 0.0)
        angular_cons = data.get('angular_consistency', 0.0)
        coherence_3d = data.get('coherence_3d', 0.0)
        stratification = data.get('stratification_index', 0.0)
        area_m2 = data.get('estimated_area_m2', 10000.0)
        
        # Inferir clase estructural
        if scale_inv > 0.9 and angular_cons > 0.9:
            if stratification > 0.5:
                structure_class = StructureClass.STEPPED_PLATFORM
                terracing = True
                levels = int(stratification * 10) + 1
            else:
                structure_class = StructureClass.PYRAMIDAL
                terracing = False
                levels = 1
        elif coherence_3d > 0.8:
            structure_class = StructureClass.MOUND_EMBANKMENT
            terracing = False
            levels = 1
        else:
            structure_class = StructureClass.UNDEFINED
            terracing = False
            levels = 1
        
        # Inferir dimensiones desde área
        base_length = np.sqrt(area_m2)
        base_width = base_length
        height = base_length * 0.5  # Proporción típica
        
        # Inferir simetría
        if angular_cons > 0.9:
            symmetry = SymmetryType.AXIAL
        elif angular_cons > 0.7:
            symmetry = SymmetryType.BILATERAL
        else:
            symmetry = SymmetryType.NONE
        
        confidence = (scale_inv + angular_cons + coherence_3d) / 3.0
        
        return GeometricRules(
            structure_class=structure_class,
            base_shape="square" if angular_cons > 0.8 else "rectangular",
            base_length_m=base_length,
            base_width_m=base_width,
            height_m=height,
            symmetry=symmetry,
            terracing=terracing,
            levels=levels,
            slope_angle_deg=45.0,
            scale_invariance=scale_inv,
            angular_consistency=angular_cons,
            coherence_3d=coherence_3d,
            confidence=confidence,
            uncertainty=1.0 - confidence,
            material_profile="homogeneous_stone"
        )
    
    def generate_geometry(self, rules: GeometricRules) -> GeometricModel:
        """
        ETAPA 2: Generar geometría 3D desde reglas.
        
        El motor EJECUTA las reglas (no inventa).
        """
        
        logger.info(f"⚙️ Generando geometría: {rules.structure_class.value}")
        
        if rules.structure_class == StructureClass.PYRAMIDAL:
            mesh = self._generate_pyramid(rules)
        elif rules.structure_class == StructureClass.STEPPED_PLATFORM:
            mesh = self._generate_stepped_platform(rules)
        elif rules.structure_class == StructureClass.MONOLITHIC_ANTHROPOFORM:
            mesh = self._generate_anthropoform(rules)
        elif rules.structure_class == StructureClass.MOUND_EMBANKMENT:
            mesh = self._generate_mound(rules)
        else:
            mesh = self._generate_generic_volume(rules)
        
        # Calcular propiedades
        volume = mesh.volume if hasattr(mesh, 'volume') else 0.0
        surface_area = mesh.area if hasattr(mesh, 'area') else 0.0
        bbox = mesh.bounds[1] - mesh.bounds[0] if hasattr(mesh, 'bounds') else (0, 0, 0)
        
        model = GeometricModel(
            vertices=mesh.vertices,
            faces=mesh.faces,
            normals=mesh.face_normals if hasattr(mesh, 'face_normals') else np.zeros((len(mesh.faces), 3)),
            volume_m3=volume,
            surface_area_m2=surface_area,
            bounding_box=tuple(bbox),
            rules=rules
        )
        
        logger.info(f"   ✅ Geometría generada: {len(model.vertices)} vértices, {len(model.faces)} caras")
        logger.info(f"   📦 Volumen: {volume:.0f} m³")
        
        return model
    
    def _generate_pyramid(self, rules: GeometricRules) -> trimesh.Trimesh:
        """Generar pirámide (simple o escalonada)."""
        
        base_l = rules.base_length_m
        base_w = rules.base_width_m
        height = rules.height_m
        
        if rules.terracing:
            # Pirámide escalonada
            return self._generate_stepped_pyramid(rules)
        else:
            # Pirámide simple
            vertices = np.array([
                [-base_l/2, -base_w/2, 0],  # Base
                [base_l/2, -base_w/2, 0],
                [base_l/2, base_w/2, 0],
                [-base_l/2, base_w/2, 0],
                [0, 0, height]  # Ápice
            ])
            
            faces = np.array([
                [0, 1, 4],  # Caras laterales
                [1, 2, 4],
                [2, 3, 4],
                [3, 0, 4],
                [0, 3, 2],  # Base
                [0, 2, 1]
            ])
            
            return trimesh.Trimesh(vertices=vertices, faces=faces)
    
    def _generate_stepped_pyramid(self, rules: GeometricRules) -> trimesh.Trimesh:
        """Generar pirámide escalonada (tipo Teotihuacán)."""
        
        levels = rules.levels
        base_l = rules.base_length_m
        base_w = rules.base_width_m
        total_height = rules.height_m
        
        vertices = []
        faces = []
        vertex_offset = 0
        
        for i in range(levels):
            # Dimensiones de este nivel
            level_height = total_height / levels
            z_bottom = i * level_height
            z_top = (i + 1) * level_height
            
            # Reducción de base por nivel
            scale = 1.0 - (i / levels) * 0.7
            l = base_l * scale
            w = base_w * scale
            
            # Vértices del nivel (prisma rectangular)
            level_verts = np.array([
                [-l/2, -w/2, z_bottom],
                [l/2, -w/2, z_bottom],
                [l/2, w/2, z_bottom],
                [-l/2, w/2, z_bottom],
                [-l/2, -w/2, z_top],
                [l/2, -w/2, z_top],
                [l/2, w/2, z_top],
                [-l/2, w/2, z_top]
            ])
            
            vertices.extend(level_verts)
            
            # Caras del prisma
            level_faces = np.array([
                [0, 1, 5], [0, 5, 4],  # Frente
                [1, 2, 6], [1, 6, 5],  # Derecha
                [2, 3, 7], [2, 7, 6],  # Atrás
                [3, 0, 4], [3, 4, 7],  # Izquierda
                [4, 5, 6], [4, 6, 7]   # Top
            ]) + vertex_offset
            
            faces.extend(level_faces)
            vertex_offset += 8
        
        return trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))
    
    def _generate_stepped_platform(self, rules: GeometricRules) -> trimesh.Trimesh:
        """Generar plataforma escalonada."""
        return self._generate_stepped_pyramid(rules)
    
    def _generate_anthropoform(self, rules: GeometricRules) -> trimesh.Trimesh:
        """
        Generar forma antropomórfica monolítica (tipo Moai).
        
        NO genera rasgos faciales, brazos, ni ornamentos.
        SOLO volumen antropomórfico inferido:
        - Eje vertical
        - Masa superior dominante (cabeza)
        - Cuello definido
        - Simetría bilateral
        """
        
        height = rules.height_m
        base_width = rules.base_width_m
        
        # Proporciones típicas de moai
        head_height = height * 0.4  # Cabeza sobredimensionada
        neck_height = height * 0.15
        body_height = height * 0.45
        
        # Anchos
        head_width = base_width * 0.8
        neck_width = base_width * 0.4
        body_width = base_width
        
        vertices = []
        faces = []
        
        # BASE (cuerpo inferior)
        z_base = 0
        body_verts = [
            [-body_width/2, -body_width/3, z_base],
            [body_width/2, -body_width/3, z_base],
            [body_width/2, body_width/3, z_base],
            [-body_width/2, body_width/3, z_base],
        ]
        
        # CUERPO SUPERIOR (antes del cuello)
        z_body_top = body_height
        body_top_verts = [
            [-body_width/2, -body_width/3, z_body_top],
            [body_width/2, -body_width/3, z_body_top],
            [body_width/2, body_width/3, z_body_top],
            [-body_width/2, body_width/3, z_body_top],
        ]
        
        # CUELLO
        z_neck_top = z_body_top + neck_height
        neck_verts = [
            [-neck_width/2, -neck_width/3, z_neck_top],
            [neck_width/2, -neck_width/3, z_neck_top],
            [neck_width/2, neck_width/3, z_neck_top],
            [-neck_width/2, neck_width/3, z_neck_top],
        ]
        
        # CABEZA (sobredimensionada)
        z_head_top = z_neck_top + head_height
        head_verts = [
            [-head_width/2, -head_width/3, z_head_top],
            [head_width/2, -head_width/3, z_head_top],
            [head_width/2, head_width/3, z_head_top],
            [-head_width/2, head_width/3, z_head_top],
        ]
        
        # Combinar vértices
        all_verts = body_verts + body_top_verts + neck_verts + head_verts
        vertices = np.array(all_verts)
        
        # Generar caras (conectar secciones)
        faces = []
        
        # Conectar base con cuerpo superior
        for i in range(4):
            next_i = (i + 1) % 4
            faces.append([i, next_i, 4 + next_i])
            faces.append([i, 4 + next_i, 4 + i])
        
        # Conectar cuerpo con cuello
        for i in range(4):
            next_i = (i + 1) % 4
            faces.append([4 + i, 4 + next_i, 8 + next_i])
            faces.append([4 + i, 8 + next_i, 8 + i])
        
        # Conectar cuello con cabeza
        for i in range(4):
            next_i = (i + 1) % 4
            faces.append([8 + i, 8 + next_i, 12 + next_i])
            faces.append([8 + i, 12 + next_i, 12 + i])
        
        # Base inferior
        faces.append([0, 2, 1])
        faces.append([0, 3, 2])
        
        # Top de cabeza
        faces.append([12, 13, 14])
        faces.append([12, 14, 15])
        
        return trimesh.Trimesh(vertices=vertices, faces=np.array(faces))
    
    def _generate_mound(self, rules: GeometricRules) -> trimesh.Trimesh:
        """Generar montículo/terraplén (forma orgánica)."""
        
        # Usar esfera aplastada como aproximación
        sphere = trimesh.creation.icosphere(subdivisions=3, radius=rules.base_length_m / 2)
        
        # Aplastar en Z
        sphere.vertices[:, 2] *= (rules.height_m / (rules.base_length_m / 2))
        
        # Mover a Z=0
        sphere.vertices[:, 2] -= sphere.vertices[:, 2].min()
        
        return sphere
    
    def _generate_generic_volume(self, rules: GeometricRules) -> trimesh.Trimesh:
        """Generar volumen genérico (caja)."""
        
        return trimesh.creation.box(extents=[
            rules.base_length_m,
            rules.base_width_m,
            rules.height_m
        ])
    
    def render_to_png(self, 
                     model: GeometricModel,
                     output_path: str,
                     view_angle: Tuple[float, float] = (30, 45),
                     show_grid: bool = True,
                     show_axes: bool = True) -> str:
        """
        ETAPA 3: Render modelo 3D a PNG.
        
        Genera vista 3D isométrica del modelo.
        """
        
        logger.info(f"🎨 Renderizando a PNG: {output_path}")
        
        fig = plt.figure(figsize=(12, 10), facecolor='#1a1a1a')
        ax = fig.add_subplot(111, projection='3d', facecolor='#1a1a1a')
        
        # Crear colección de polígonos
        poly_collection = Poly3DCollection(
            model.vertices[model.faces],
            alpha=0.9,
            facecolor='#8B7355',  # Color piedra
            edgecolor='#2a2a2a',
            linewidths=0.5
        )
        
        ax.add_collection3d(poly_collection)
        
        # Configurar límites
        bbox = model.bounding_box
        max_range = max(bbox) / 2
        mid_x = 0
        mid_y = 0
        mid_z = bbox[2] / 2
        
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(0, bbox[2])
        
        # Ángulo de vista
        ax.view_init(elev=view_angle[0], azim=view_angle[1])
        
        # Etiquetas
        ax.set_xlabel('X (m)', color='gray', fontsize=10)
        ax.set_ylabel('Y (m)', color='gray', fontsize=10)
        ax.set_zlabel('Z (m)', color='gray', fontsize=10)
        
        # Grid
        if show_grid:
            ax.grid(True, alpha=0.3, color='gray')
        
        # Título con metadatos y disclaimer científico
        title = (
            f"ARCHEOSCOPE MIG - REPRESENTACIÓN VOLUMÉTRICA INFERIDA\n"
            f"Clase: {model.rules.structure_class.value.upper()} | "
            f"Dimensiones: {model.rules.base_length_m:.0f}m × {model.rules.base_width_m:.0f}m × {model.rules.height_m:.0f}m | "
            f"Volumen: {model.volume_m3:.0f} m³\n"
            f"Scale Inv: {model.rules.scale_invariance:.3f} | "
            f"Angular Cons: {model.rules.angular_consistency:.3f} | "
            f"Coherence 3D: {model.rules.coherence_3d:.3f}\n"
            f"Confianza: {model.rules.confidence:.2f} | Incertidumbre: {model.rules.uncertainty:.2f}\n"
            f"⚠️ Compatible con invariantes detectados - NO reconstrucción exacta"
        )
        
        ax.set_title(title, color='white', fontsize=11, pad=20)
        
        # Estilo
        ax.tick_params(colors='gray', labelsize=8)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        # Guardar
        plt.savefig(output_path, bbox_inches='tight', dpi=150, facecolor='#1a1a1a')
        plt.close()
        
        logger.info(f"   ✅ PNG guardado: {output_path}")
        
        return output_path
    
    def export_to_obj(self, model: GeometricModel, output_path: str) -> str:
        """Exportar modelo a formato OBJ (para AutoCAD, Blender, etc.)."""
        
        mesh = trimesh.Trimesh(vertices=model.vertices, faces=model.faces)
        mesh.export(output_path)
        
        logger.info(f"   ✅ OBJ exportado: {output_path}")
        
        return output_path
    
    def run_complete_inference(self,
                              archeoscope_data: Dict[str, Any],
                              output_name: str,
                              use_ai: bool = True) -> Dict[str, str]:
        """
        Pipeline completo: Datos → Reglas → Geometría → PNG.
        """
        
        logger.info("="*80)
        logger.info("🧠 MIG - MOTOR DE INFERENCIA GEOMÉTRICA")
        logger.info("="*80)
        
        # Etapa 1: Inferir reglas
        rules = self.infer_geometric_rules(archeoscope_data, use_ai_reasoning=use_ai)
        
        # Etapa 2: Generar geometría
        model = self.generate_geometry(rules)
        
        # Etapa 3: Render a PNG
        png_path = str(self.output_dir / f"{output_name}.png")
        self.render_to_png(model, png_path)
        
        # Etapa 4: Exportar OBJ (opcional)
        obj_path = str(self.output_dir / f"{output_name}.obj")
        self.export_to_obj(model, obj_path)
        
        logger.info("="*80)
        logger.info("✅ INFERENCIA COMPLETA")
        logger.info("="*80)
        
        return {
            'png': png_path,
            'obj': obj_path,
            'structure_class': rules.structure_class.value,
            'confidence': rules.confidence,
            'volume_m3': model.volume_m3
        }


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    print("🧠 MIG - Motor de Inferencia Geométrica - Test\n")
    
    # Datos de ejemplo (Puerto Rico North)
    test_data = {
        'scale_invariance': 0.995,
        'angular_consistency': 0.910,
        'coherence_3d': 0.886,
        'sar_rigidity': 0.929,
        'stratification_index': 0.375,
        'estimated_area_m2': 10000.0
    }
    
    # Crear motor
    mig = GeometricInferenceEngine()
    
    # Ejecutar inferencia completa
    result = mig.run_complete_inference(
        archeoscope_data=test_data,
        output_name="test_structure",
        use_ai=False  # Usar heurísticas para test
    )
    
    print(f"\n✅ Resultados:")
    print(f"   PNG: {result['png']}")
    print(f"   OBJ: {result['obj']}")
    print(f"   Clase: {result['structure_class']}")
    print(f"   Confianza: {result['confidence']:.3f}")
    print(f"   Volumen: {result['volume_m3']:.0f} m³")
