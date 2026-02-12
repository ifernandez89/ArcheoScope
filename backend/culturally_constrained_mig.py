#!/usr/bin/env python3
"""
MIG Culturalmente Constreñido
==============================

NIVEL 3: Generación volumétrica condicionada por morfología cultural

DOBLE VÍA:
- VÍA A: Inferencia territorial (ArcheoScope) → invariantes espaciales
- VÍA B: Memoria morfológica cultural → proporciones aprendidas

RESULTADO: Forma culturalmente posible, NO copia artística

"ArcheoScope no reconstruye monumentos. Constriñe el espacio geométrico 
hasta que solo sobreviven formas culturalmente posibles."
"""

import sys
from pathlib import Path
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI para servidor
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from typing import Dict, Any, Tuple
import logging

# Importar componentes
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from morphological_repository import MorphologicalRepository, MorphologicalClass
from geometric_inference_engine import GeometricInferenceEngine

logger = logging.getLogger(__name__)


class CulturallyConstrainedMIG:
    """
    Motor de Inferencia Geométrica con Constraints Culturales.
    
    Combina:
    1. Datos territoriales (ArcheoScope)
    2. Invariantes morfológicos (repositorio cultural)
    3. Generación procedural constreñida
    """
    
    def __init__(self, output_dir: str = "geometric_models"):
        # Usar ruta absoluta
        if not Path(output_dir).is_absolute():
            # Si es relativa, hacerla relativa al directorio del proyecto
            project_root = Path(__file__).parent.parent
            output_dir = str(project_root / output_dir)
        
        self.mig = GeometricInferenceEngine(output_dir=output_dir)
        self.morph_repo = MorphologicalRepository()
        self.output_dir = Path(output_dir)
        logger.info(f"🧬 MIG Culturalmente Constreñido inicializado - Output: {self.output_dir.absolute()}")
    
    def infer_culturally_constrained_geometry(self,
                                             archeoscope_data: Dict[str, Any],
                                             output_name: str,
                                             use_ai: bool = False) -> Dict[str, Any]:
        """
        Pipeline completo con constraints culturales.
        
        1. VÍA A: Inferencia territorial
        2. VÍA B: Matching morfológico
        3. Constreñir geometría
        4. Generar modelo 3D
        5. Render + export
        """
        
        logger.info("="*80)
        logger.info("🧬 MIG CULTURALMENTE CONSTREÑIDO")
        logger.info("="*80)
        
        # VÍA A: Inferencia territorial (ArcheoScope)
        logger.info("\n📡 VÍA A: Inferencia Territorial")
        logger.info(f"   Scale Invariance: {archeoscope_data.get('scale_invariance', 0):.3f}")
        logger.info(f"   Angular Consistency: {archeoscope_data.get('angular_consistency', 0):.3f}")
        logger.info(f"   Coherence 3D: {archeoscope_data.get('coherence_3d', 0):.3f}")
        
        # VÍA B: Matching morfológico cultural
        logger.info("\n🧬 VÍA B: Memoria Morfológica Cultural")
        morph_class, morph_score = self.morph_repo.match_morphological_class(archeoscope_data)
        logger.info(f"   ✅ Clase morfológica: {morph_class.value}")
        logger.info(f"   📊 Score de compatibilidad: {morph_score:.3f}")
        
        # Obtener constraints morfológicos
        morph_invariants = self.morph_repo.get_morphological_constraints(morph_class)
        
        # Generar geometría base (territorial)
        logger.info("\n⚙️ Generando geometría base...")
        base_rules = self.mig.infer_geometric_rules(archeoscope_data, use_ai_reasoning=use_ai)
        
        # Aplicar constraints culturales
        logger.info(f"\n🔒 Aplicando constraints culturales: {morph_class.value}")
        constrained_geometry = self._apply_cultural_constraints(
            base_rules=base_rules,
            morph_invariants=morph_invariants,
            morph_class=morph_class
        )
        
        # Generar modelo 3D constreñido
        logger.info("\n🎨 Generando modelo 3D culturalmente constreñido...")
        model = self._generate_culturally_constrained_model(
            constrained_geometry,
            morph_class
        )
        
        # Render a PNG
        png_path = str(self.output_dir / f"{output_name}.png")
        self._render_culturally_constrained(model, png_path, morph_class, morph_invariants)
        
        # Export OBJ
        obj_path = str(self.output_dir / f"{output_name}.obj")
        mesh = trimesh.Trimesh(vertices=model['vertices'], faces=model['faces'])
        mesh.export(obj_path)
        
        logger.info("\n" + "="*80)
        logger.info("✅ INFERENCIA CULTURALMENTE CONSTREÑIDA COMPLETA")
        logger.info("="*80)
        
        return {
            'png': png_path,
            'obj': obj_path,
            'morphological_class': morph_class.value,
            'morphological_score': morph_score,
            'cultural_origin': morph_invariants.cultural_origin,
            'confidence': base_rules.confidence * morph_score,
            'volume_m3': model['volume_m3']
        }
    
    def _apply_cultural_constraints(self,
                                   base_rules: Any,
                                   morph_invariants: Any,
                                   morph_class: MorphologicalClass) -> Dict[str, Any]:
        """Aplicar constraints morfológicos a geometría base."""
        
        # Blend entre inferencia territorial y morfología cultural
        blend_factor = 0.65  # 65% morfología, 35% territorial
        
        # Ajustar proporciones
        base_width = base_rules.base_width_m
        
        # Aplicar ratio cultural
        target_height = base_width * morph_invariants.height_to_width_ratio
        current_height = base_rules.height_m
        
        adjusted_height = current_height * (1 - blend_factor) + target_height * blend_factor
        
        # Construir geometría constreñida
        constrained = {
            'base_length_m': base_rules.base_length_m,
            'base_width_m': base_rules.base_width_m,
            'height_m': adjusted_height,
            'morphological_class': morph_class,
            'head_to_body_ratio': morph_invariants.head_to_body_ratio,
            'bilateral_symmetry': morph_invariants.bilateral_symmetry,
            'arms_position': morph_invariants.arms_position,
            'legs_position': morph_invariants.legs_position,
            'frontal_axis_absolute': morph_invariants.frontal_axis_absolute,
            'dynamism_level': morph_invariants.dynamism_level,
            'cultural_origin': morph_invariants.cultural_origin
        }
        
        logger.info(f"   📐 Altura ajustada: {current_height:.1f}m → {adjusted_height:.1f}m")
        logger.info(f"   📊 Ratio H/W: {adjusted_height/base_width:.2f} (target: {morph_invariants.height_to_width_ratio:.2f})")
        
        return constrained
    
    def _generate_culturally_constrained_model(self,
                                              geometry: Dict[str, Any],
                                              morph_class: MorphologicalClass) -> Dict[str, Any]:
        """Generar modelo 3D con constraints culturales."""
        
        if morph_class == MorphologicalClass.MOAI:
            mesh = self._generate_moai_constrained(geometry)
        elif morph_class == MorphologicalClass.SPHINX:
            mesh = self._generate_sphinx_constrained(geometry)
        elif morph_class == MorphologicalClass.EGYPTIAN_STATUE:
            mesh = self._generate_egyptian_statue_constrained(geometry)
        elif morph_class == MorphologicalClass.COLOSSUS:
            mesh = self._generate_colossus_constrained(geometry)
        elif morph_class == MorphologicalClass.PYRAMID_MESOAMERICAN:
            mesh = self._generate_pyramid_mesoamerican_constrained(geometry)
        elif morph_class == MorphologicalClass.TEMPLE_PLATFORM:
            mesh = self._generate_temple_platform_constrained(geometry)
        elif morph_class == MorphologicalClass.STELA_MAYA:
            mesh = self._generate_stela_maya_constrained(geometry)
        else:
            mesh = self._generate_generic_anthropomorphic(geometry)
        
        return {
            'vertices': mesh.vertices,
            'faces': mesh.faces,
            'volume_m3': mesh.volume if hasattr(mesh, 'volume') else 0.0,
            'geometry': geometry
        }
    
    def _generate_moai_constrained(self, geometry: Dict[str, Any]) -> trimesh.Trimesh:
        """
        Generar MOAI culturalmente constreñido.
        
        MEJORAS IMPLEMENTADAS:
        - Más subdivisiones para forma más suave
        - Transiciones graduales entre secciones
        - Cabeza más detallada con frente prominente
        - Hombros definidos
        - Base integrada con mejor proporción
        
        Invariantes MOAI:
        - Cabeza ENORME (45% del total)
        - Cuello definido
        - Cuerpo rectangular
        - Brazos fusionados
        - Base integrada
        - Simetría bilateral perfecta
        - CERO dinamismo
        """
        
        height = geometry['height_m']
        base_width = geometry['base_width_m']
        head_ratio = geometry['head_to_body_ratio']
        
        # Proporciones MOAI mejoradas
        head_height = height * head_ratio  # ~45% cabeza
        neck_height = height * 0.10
        shoulder_height = height * 0.08
        body_height = height - head_height - neck_height - shoulder_height
        
        # Anchos con más variación
        head_width = base_width * 0.90
        head_depth = base_width * 0.75  # Cabeza más profunda
        neck_width = base_width * 0.42
        shoulder_width = base_width * 1.05  # Hombros más anchos
        body_width = base_width
        
        meshes = []
        
        # BASE (cuerpo inferior) - más detallada
        base_height = body_height * 0.3
        base = trimesh.creation.box(
            extents=[body_width, body_width * 0.7, base_height]
        )
        base.apply_translation([0, 0, base_height/2])
        meshes.append(base)
        
        # CUERPO MEDIO
        mid_body_height = body_height * 0.7
        mid_body = trimesh.creation.box(
            extents=[body_width * 0.95, body_width * 0.65, mid_body_height]
        )
        mid_body.apply_translation([0, 0, base_height + mid_body_height/2])
        meshes.append(mid_body)
        
        # HOMBROS (transición al cuello)
        shoulder = trimesh.creation.box(
            extents=[shoulder_width, body_width * 0.6, shoulder_height]
        )
        shoulder.apply_translation([0, 0, body_height + shoulder_height/2])
        meshes.append(shoulder)
        
        # CUELLO (transición suave)
        neck_z = body_height + shoulder_height
        # Cuello inferior (más ancho)
        neck_lower = trimesh.creation.box(
            extents=[neck_width * 1.2, neck_width * 0.9, neck_height * 0.5]
        )
        neck_lower.apply_translation([0, 0, neck_z + neck_height * 0.25])
        meshes.append(neck_lower)
        
        # Cuello superior (más estrecho)
        neck_upper = trimesh.creation.box(
            extents=[neck_width, neck_width * 0.8, neck_height * 0.5]
        )
        neck_upper.apply_translation([0, 0, neck_z + neck_height * 0.75])
        meshes.append(neck_upper)
        
        # CABEZA (múltiples secciones para más detalle)
        head_z_base = body_height + shoulder_height + neck_height
        
        # Mandíbula/base de cabeza
        jaw_height = head_height * 0.25
        jaw = trimesh.creation.box(
            extents=[head_width * 0.85, head_depth * 0.8, jaw_height]
        )
        jaw.apply_translation([0, 0, head_z_base + jaw_height/2])
        meshes.append(jaw)
        
        # Cara media (parte principal)
        face_height = head_height * 0.45
        face = trimesh.creation.box(
            extents=[head_width, head_depth, face_height]
        )
        face.apply_translation([0, 0, head_z_base + jaw_height + face_height/2])
        meshes.append(face)
        
        # Frente prominente (característica moai)
        forehead_height = head_height * 0.20
        forehead = trimesh.creation.box(
            extents=[head_width * 0.95, head_depth * 0.85, forehead_height]
        )
        forehead.apply_translation([0, 0, head_z_base + jaw_height + face_height + forehead_height/2])
        meshes.append(forehead)
        
        # Corona/top de cabeza
        crown_height = head_height * 0.10
        crown = trimesh.creation.box(
            extents=[head_width * 0.85, head_depth * 0.75, crown_height]
        )
        crown.apply_translation([0, 0, head_z_base + jaw_height + face_height + forehead_height + crown_height/2])
        meshes.append(crown)
        
        mesh = trimesh.util.concatenate(meshes)
        
        return mesh
    
    def _generate_sphinx_constrained(self, geometry: Dict[str, Any]) -> trimesh.Trimesh:
        """
        Generar ESFINGE culturalmente constreñida.
        
        MEJORAS IMPLEMENTADAS:
        - Cuerpo más detallado con secciones
        - Patas delanteras definidas
        - Transición suave cuerpo-cabeza
        - Cabeza con más proporciones
        - Base/plataforma integrada
        
        Invariantes ESFINGE:
        - Cuerpo horizontal (león)
        - Cabeza vertical (humana)
        - Transición gradual
        - Patas delanteras extendidas
        - Base integrada
        """
        
        height = geometry['height_m']
        length = geometry['base_length_m']
        width = geometry['base_width_m']
        
        # Proporciones esfinge mejoradas
        body_length = length * 0.65  # Cuerpo de león
        head_length = length * 0.25  # Cabeza humana
        paws_length = length * 0.10  # Patas delanteras
        
        meshes = []
        
        # BASE/PLATAFORMA
        platform_height = height * 0.15
        platform = trimesh.creation.box(
            extents=[length * 1.05, width * 1.1, platform_height]
        )
        platform.apply_translation([length/2, 0, platform_height/2])
        meshes.append(platform)
        
        # CUERPO TRASERO (cuartos traseros)
        rear_body_height = height * 0.50
        rear_body = trimesh.creation.box(
            extents=[body_length * 0.4, width, rear_body_height]
        )
        rear_body.apply_translation([body_length * 0.2, 0, platform_height + rear_body_height/2])
        meshes.append(rear_body)
        
        # CUERPO MEDIO (torso)
        mid_body_height = height * 0.55
        mid_body = trimesh.creation.box(
            extents=[body_length * 0.35, width * 0.95, mid_body_height]
        )
        mid_body.apply_translation([body_length * 0.575, 0, platform_height + mid_body_height/2])
        meshes.append(mid_body)
        
        # PECHO (transición a patas delanteras)
        chest_height = height * 0.60
        chest = trimesh.creation.box(
            extents=[body_length * 0.25, width * 0.85, chest_height]
        )
        chest.apply_translation([body_length * 0.875, 0, platform_height + chest_height/2])
        meshes.append(chest)
        
        # PATAS DELANTERAS (extendidas)
        paw_height = height * 0.70
        paw_width = width * 0.35
        
        # Pata izquierda
        left_paw = trimesh.creation.box(
            extents=[paws_length, paw_width, paw_height]
        )
        left_paw.apply_translation([body_length + paws_length/2, width * 0.25, platform_height + paw_height/2])
        meshes.append(left_paw)
        
        # Pata derecha
        right_paw = trimesh.creation.box(
            extents=[paws_length, paw_width, paw_height]
        )
        right_paw.apply_translation([body_length + paws_length/2, -width * 0.25, platform_height + paw_height/2])
        meshes.append(right_paw)
        
        # CUELLO (transición)
        neck_height = height * 0.40
        neck_width = width * 0.55
        neck = trimesh.creation.box(
            extents=[head_length * 0.4, neck_width, neck_height]
        )
        neck.apply_translation([body_length + paws_length + head_length * 0.2, 0, platform_height + paw_height + neck_height/2])
        meshes.append(neck)
        
        # CABEZA (múltiples secciones)
        head_base_z = platform_height + paw_height + neck_height
        
        # Base de cabeza (mandíbula)
        jaw_height = height * 0.35
        jaw = trimesh.creation.box(
            extents=[head_length * 0.8, width * 0.65, jaw_height]
        )
        jaw.apply_translation([body_length + paws_length + head_length * 0.6, 0, head_base_z + jaw_height/2])
        meshes.append(jaw)
        
        # Cara superior
        face_height = height * 0.40
        face = trimesh.creation.box(
            extents=[head_length * 0.75, width * 0.60, face_height]
        )
        face.apply_translation([body_length + paws_length + head_length * 0.625, 0, head_base_z + jaw_height + face_height/2])
        meshes.append(face)
        
        # Corona/tocado (nemes)
        crown_height = height * 0.30
        crown = trimesh.creation.box(
            extents=[head_length * 0.85, width * 0.70, crown_height]
        )
        crown.apply_translation([body_length + paws_length + head_length * 0.6, 0, head_base_z + jaw_height + face_height + crown_height/2])
        meshes.append(crown)
        
        mesh = trimesh.util.concatenate(meshes)
        
        return mesh
    
    def _generate_egyptian_statue_constrained(self, geometry: Dict[str, Any]) -> trimesh.Trimesh:
        """
        Generar ESTATUA EGIPCIA culturalmente constreñida.
        
        Invariantes:
        - Frontalidad absoluta
        - Cabeza ~1/8 del cuerpo
        - Brazos a los lados
        - Pierna adelantada
        - Base integrada
        """
        
        height = geometry['height_m']
        base_width = geometry['base_width_m']
        
        # Proporciones egipcias (canon de 18 cuadrículas)
        head_height = height / 8
        body_height = height - head_height
        
        # Cuerpo (prisma rectangular)
        body = trimesh.creation.box(extents=[base_width, base_width * 0.4, body_height])
        body.apply_translation([0, 0, body_height/2])
        
        # Cabeza (cubo)
        head = trimesh.creation.box(extents=[base_width * 0.6, base_width * 0.4, head_height])
        head.apply_translation([0, 0, body_height + head_height/2])
        
        # Combinar
        mesh = trimesh.util.concatenate([body, head])
        
        return mesh
    
    def _generate_colossus_constrained(self, geometry: Dict[str, Any]) -> trimesh.Trimesh:
        """Generar COLOSO (sentado) culturalmente constreñido."""
        
        height = geometry['height_m']
        base_width = geometry['base_width_m']
        
        # Coloso sentado
        body = trimesh.creation.box(extents=[base_width, base_width, height * 0.7])
        body.apply_translation([0, 0, height * 0.35])
        
        head = trimesh.creation.box(extents=[base_width * 0.6, base_width * 0.6, height * 0.3])
        head.apply_translation([0, 0, height * 0.7 + height * 0.15])
        
        mesh = trimesh.util.concatenate([body, head])
        
        return mesh
    
    def _generate_pyramid_mesoamerican_constrained(self, geometry: Dict[str, Any]) -> trimesh.Trimesh:
        """
        Generar PIRÁMIDE MESOAMERICANA culturalmente constreñida.
        
        MEJORAS IMPLEMENTADAS:
        - Más subdivisiones para geometría suave
        - Escalinata frontal real (no implícita)
        - Talud-tablero (estilo Teotihuacán)
        - Transiciones suaves entre niveles
        - Templo superior detallado
        """
        
        height = geometry['height_m']
        base_width = geometry['base_width_m']
        base_length = geometry.get('base_length_m', base_width)
        
        # Número de niveles basado en altura (más niveles = más detalle)
        num_levels = max(5, min(8, int(height / 8)))
        
        meshes = []
        current_z = 0
        level_height = height / num_levels
        
        for level in range(num_levels):
            # Reducción progresiva del ancho (más suave)
            scale_factor = 1.0 - (level / num_levels) * 0.65
            level_width = base_width * scale_factor
            level_length = base_length * scale_factor
            
            # TALUD (parte inclinada) - más subdivisiones
            talud_height = level_height * 0.7
            talud = trimesh.creation.box(
                extents=[level_length, level_width, talud_height]
            )
            talud.apply_translation([0, 0, current_z + talud_height/2])
            meshes.append(talud)
            
            # TABLERO (parte vertical superior) - característico de Teotihuacán
            tablero_height = level_height * 0.3
            tablero_width = level_width * 0.95  # Ligeramente más estrecho
            tablero = trimesh.creation.box(
                extents=[level_length * 0.95, tablero_width, tablero_height]
            )
            tablero.apply_translation([0, 0, current_z + talud_height + tablero_height/2])
            meshes.append(tablero)
            
            current_z += level_height
        
        # ESCALINATA FRONTAL (detalle importante)
        stair_width = base_width * 0.25
        stair_length = base_length * 0.05
        num_stairs = num_levels * 3  # 3 escalones por nivel
        stair_height = height / num_stairs
        
        for stair in range(num_stairs):
            stair_z = stair * stair_height
            # Escalón que sube por el frente
            stair_mesh = trimesh.creation.box(
                extents=[stair_width, stair_length, stair_height]
            )
            # Posicionar en el frente, subiendo
            stair_y = base_length/2 - (stair / num_stairs) * base_length * 0.4
            stair_mesh.apply_translation([0, stair_y, stair_z + stair_height/2])
            meshes.append(stair_mesh)
        
        # TEMPLO SUPERIOR (estructura detallada en la cima)
        temple_width = base_width * 0.18
        temple_height = height * 0.18
        
        # Base del templo
        temple_base = trimesh.creation.box(
            extents=[temple_width * 1.2, temple_width * 1.2, temple_height * 0.3]
        )
        temple_base.apply_translation([0, 0, height + temple_height * 0.15])
        meshes.append(temple_base)
        
        # Cuerpo del templo
        temple_body = trimesh.creation.box(
            extents=[temple_width, temple_width * 0.8, temple_height * 0.5]
        )
        temple_body.apply_translation([0, 0, height + temple_height * 0.3 + temple_height * 0.25])
        meshes.append(temple_body)
        
        # Techo del templo (inclinado simulado)
        temple_roof = trimesh.creation.box(
            extents=[temple_width * 1.1, temple_width * 0.9, temple_height * 0.2]
        )
        temple_roof.apply_translation([0, 0, height + temple_height * 0.3 + temple_height * 0.5 + temple_height * 0.1])
        meshes.append(temple_roof)
        
        mesh = trimesh.util.concatenate(meshes)
        
        return mesh
    
    def _generate_temple_platform_constrained(self, geometry: Dict[str, Any]) -> trimesh.Trimesh:
        """
        Generar PLATAFORMA CEREMONIAL mesoamericana.
        
        Invariantes:
        - Muy horizontal (base grande, altura pequeña)
        - 2-3 niveles escalonados
        - Escalinatas múltiples
        - Plaza superior amplia
        """
        
        height = geometry['height_m']
        base_width = geometry['base_width_m']
        base_length = geometry.get('base_length_m', base_width * 1.5)
        
        meshes = []
        
        # Nivel inferior (base amplia)
        base_level = trimesh.creation.box(
            extents=[base_length, base_width, height * 0.4]
        )
        base_level.apply_translation([0, 0, height * 0.2])
        meshes.append(base_level)
        
        # Nivel medio
        mid_level = trimesh.creation.box(
            extents=[base_length * 0.8, base_width * 0.8, height * 0.3]
        )
        mid_level.apply_translation([0, 0, height * 0.4 + height * 0.15])
        meshes.append(mid_level)
        
        # Nivel superior (plaza)
        top_level = trimesh.creation.box(
            extents=[base_length * 0.6, base_width * 0.6, height * 0.3]
        )
        top_level.apply_translation([0, 0, height * 0.7 + height * 0.15])
        meshes.append(top_level)
        
        mesh = trimesh.util.concatenate(meshes)
        
        return mesh
    
    def _generate_stela_maya_constrained(self, geometry: Dict[str, Any]) -> trimesh.Trimesh:
        """
        Generar ESTELA MAYA culturalmente constreñida.
        
        Invariantes:
        - Muy vertical y delgada
        - Forma de losa rectangular
        - Figura antropomórfica en relieve (simplificada)
        - Base integrada
        - Frontalidad absoluta
        """
        
        height = geometry['height_m']
        base_width = geometry['base_width_m']
        
        # Estela: losa vertical delgada
        stela_thickness = base_width * 0.2
        stela_width = base_width
        
        # Cuerpo principal de la estela
        main_body = trimesh.creation.box(
            extents=[stela_width, stela_thickness, height * 0.85]
        )
        main_body.apply_translation([0, 0, height * 0.425])
        
        # Parte superior (cabeza/tocado)
        top_section = trimesh.creation.box(
            extents=[stela_width * 0.9, stela_thickness, height * 0.15]
        )
        top_section.apply_translation([0, 0, height * 0.85 + height * 0.075])
        
        # Base
        base = trimesh.creation.box(
            extents=[stela_width * 1.1, stela_thickness * 1.5, height * 0.05]
        )
        base.apply_translation([0, 0, height * 0.025])
        
        mesh = trimesh.util.concatenate([base, main_body, top_section])
        
        return mesh
    
    def _generate_generic_anthropomorphic(self, geometry: Dict[str, Any]) -> trimesh.Trimesh:
        """Generar forma antropomórfica genérica."""
        
        height = geometry['height_m']
        base_width = geometry['base_width_m']
        
        return trimesh.creation.box(extents=[base_width, base_width * 0.5, height])
    
    def _render_culturally_constrained(self,
                                      model: Dict[str, Any],
                                      output_path: str,
                                      morph_class: MorphologicalClass,
                                      morph_invariants: Any):
        """Render con disclaimers culturales y calidad mejorada."""
        
        try:
            logger.info(f"🎨 Iniciando render de alta calidad a: {output_path}")
            
            # Figura más grande para mejor calidad
            fig = plt.figure(figsize=(16, 14), facecolor='#0a0a0a')
            ax = fig.add_subplot(111, projection='3d', facecolor='#0a0a0a')
            
            # Determinar color según clase morfológica
            if morph_class == MorphologicalClass.SPHINX:
                # Esfinge: Piedra caliza dorada del desierto
                face_color = '#D4A574'  # Dorado arena
                edge_color = '#8B6F47'  # Marrón oscuro
                alpha = 0.95
            elif morph_class == MorphologicalClass.MOAI:
                # Moai: Toba volcánica gris
                face_color = '#6B6B6B'
                edge_color = '#3a3a3a'
                alpha = 0.92
            elif morph_class == MorphologicalClass.EGYPTIAN_STATUE:
                # Estatua egipcia: Granito rojo/gris
                face_color = '#8B7355'
                edge_color = '#4a4a4a'
                alpha = 0.90
            elif morph_class == MorphologicalClass.COLOSSUS:
                # Coloso: Piedra arenisca
                face_color = '#C19A6B'
                edge_color = '#6B5A3D'
                alpha = 0.93
            elif morph_class == MorphologicalClass.PYRAMID_MESOAMERICAN:
                # Pirámide mesoamericana: Piedra volcánica/caliza
                face_color = '#A0826D'  # Beige piedra
                edge_color = '#5a4a3d'
                alpha = 0.94
            elif morph_class == MorphologicalClass.TEMPLE_PLATFORM:
                # Plataforma: Piedra caliza clara
                face_color = '#C8B8A0'
                edge_color = '#7a6a5d'
                alpha = 0.91
            elif morph_class == MorphologicalClass.STELA_MAYA:
                # Estela maya: Piedra caliza con relieve
                face_color = '#B8A890'
                edge_color = '#6a5a4d'
                alpha = 0.93
            else:
                # Default
                face_color = '#8B7355'
                edge_color = '#2a2a2a'
                alpha = 0.90
            
            # Crear colección de polígonos con mejor calidad
            poly_collection = Poly3DCollection(
                model['vertices'][model['faces']],
                alpha=alpha,
                facecolor=face_color,
                edgecolor=edge_color,
                linewidths=0.3,
                antialiased=True
            )
            
            # Agregar sombreado para profundidad
            poly_collection.set_edgecolor(edge_color)
            
            ax.add_collection3d(poly_collection)
            
            # Configurar límites con mejor encuadre
            vertices = model['vertices']
            max_range = np.ptp(vertices, axis=0).max() / 2
            mid = vertices.mean(axis=0)
            
            ax.set_xlim(mid[0] - max_range * 1.1, mid[0] + max_range * 1.1)
            ax.set_ylim(mid[1] - max_range * 1.1, mid[1] + max_range * 1.1)
            ax.set_zlim(0, vertices[:, 2].max() * 1.05)
            
            # Vista optimizada según clase
            if morph_class == MorphologicalClass.SPHINX:
                # Vista lateral-frontal para Esfinge (horizontal)
                ax.view_init(elev=20, azim=35)
            elif morph_class == MorphologicalClass.MOAI:
                # Vista frontal para Moai (vertical)
                ax.view_init(elev=15, azim=45)
            elif morph_class == MorphologicalClass.PYRAMID_MESOAMERICAN:
                # Vista elevada para pirámides escalonadas
                ax.view_init(elev=30, azim=45)
            elif morph_class == MorphologicalClass.TEMPLE_PLATFORM:
                # Vista aérea para plataformas
                ax.view_init(elev=35, azim=45)
            elif morph_class == MorphologicalClass.STELA_MAYA:
                # Vista frontal para estelas
                ax.view_init(elev=10, azim=0)
            else:
                # Vista isométrica estándar
                ax.view_init(elev=25, azim=45)
            
            # Etiquetas con mejor estilo
            ax.set_xlabel('X (m)', color='#888888', fontsize=11, labelpad=10)
            ax.set_ylabel('Y (m)', color='#888888', fontsize=11, labelpad=10)
            ax.set_zlabel('Z (m)', color='#888888', fontsize=11, labelpad=10)
            ax.grid(True, alpha=0.2, color='#444444', linestyle='--', linewidth=0.5)
            
            # Título mejorado con más información
            geometry = model['geometry']
            h_w_ratio = geometry['height_m'] / geometry['base_width_m']
            
            title = (
                f"╔═══════════════════════════════════════════════════════════════════════════════╗\n"
                f"║  ARCHEOSCOPE MIG - NIVEL 3: INFERENCIA CULTURALMENTE CONSTREÑIDA            ║\n"
                f"╚═══════════════════════════════════════════════════════════════════════════════╝\n\n"
                f"🏛️  Clase Morfológica: {morph_class.value.upper()}  |  "
                f"🌍 Origen: {morph_invariants.cultural_origin}\n\n"
                f"📐 Dimensiones: {geometry['base_length_m']:.1f}m (L) × "
                f"{geometry['base_width_m']:.1f}m (W) × {geometry['height_m']:.1f}m (H)  |  "
                f"📦 Volumen: {model['volume_m3']:.0f} m³\n"
                f"📊 Ratio H/W: {h_w_ratio:.2f} (cultural: {morph_invariants.height_to_width_ratio:.2f})  |  "
                f"🔄 Simetría Bilateral: {morph_invariants.bilateral_symmetry:.2%}\n"
                f"🎯 Verticalidad: {morph_invariants.vertical_axis_dominance:.2%}  |  "
                f"🔒 Rigidez: {1.0 - morph_invariants.dynamism_level:.2%}\n\n"
                f"⚠️  FORMA CULTURALMENTE POSIBLE - NO RECONSTRUCCIÓN ESPECÍFICA\n"
                f"📚 Constreñida por {morph_invariants.source_samples} muestras arqueológicas reales"
            )
            
            ax.set_title(title, color='#CCCCCC', fontsize=9, pad=25, 
                        family='monospace', ha='center')
            
            # Estilo mejorado
            ax.tick_params(colors='#666666', labelsize=9)
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.xaxis.pane.set_edgecolor('#333333')
            ax.yaxis.pane.set_edgecolor('#333333')
            ax.zaxis.pane.set_edgecolor('#333333')
            
            # Agregar iluminación simulada
            ax.set_facecolor('#0a0a0a')
            
            logger.info(f"💾 Guardando PNG de alta calidad...")
            plt.savefig(output_path, bbox_inches='tight', dpi=200, 
                       facecolor='#0a0a0a', edgecolor='none')
            plt.close()
            
            # Verificar que el archivo se creó
            from pathlib import Path
            if Path(output_path).exists():
                file_size = Path(output_path).stat().st_size
                logger.info(f"   ✅ PNG creado exitosamente: {output_path} ({file_size:,} bytes)")
            else:
                logger.error(f"   ❌ PNG NO se creó: {output_path}")
                raise FileNotFoundError(f"No se pudo crear el archivo: {output_path}")
                
        except Exception as e:
            logger.error(f"❌ Error en render: {e}", exc_info=True)
            raise


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    print("🧬 MIG Culturalmente Constreñido - Test\n")
    
    mig = CulturallyConstrainedMIG()
    
    # Test: Estructura tipo MOAI
    print("="*80)
    print("TEST: Estructura tipo MOAI (Rapa Nui)")
    print("="*80)
    
    moai_data = {
        'scale_invariance': 0.92,
        'angular_consistency': 0.88,
        'coherence_3d': 0.90,
        'sar_rigidity': 0.91,
        'stratification_index': 0.10,
        'estimated_area_m2': 25.0,  # ~5m × 5m
        'estimated_height_m': 15.0   # Muy vertical
    }
    
    result = mig.infer_culturally_constrained_geometry(
        archeoscope_data=moai_data,
        output_name="moai_culturally_constrained",
        use_ai=False
    )
    
    print(f"\n✅ Resultados:")
    print(f"   PNG: {result['png']}")
    print(f"   OBJ: {result['obj']}")
    print(f"   Clase morfológica: {result['morphological_class']}")
    print(f"   Origen cultural: {result['cultural_origin']}")
    print(f"   Score morfológico: {result['morphological_score']:.3f}")
    print(f"   Confianza total: {result['confidence']:.3f}")
    print(f"   Volumen: {result['volume_m3']:.0f} m³")
    
    print("\n" + "="*80)
    print("✅ MIG NIVEL 3 FUNCIONAL")
    print("="*80)
    print("\n🎯 'ArcheoScope no reconstruye monumentos.")
    print("   Constriñe el espacio geométrico hasta que solo")
    print("   sobreviven formas culturalmente posibles.'\n")
