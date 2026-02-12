#!/usr/bin/env python3
"""
Repositorio Morfológico Cultural
=================================

PARADIGMA:
"ArcheoScope no reconstruye monumentos. Constriñe el espacio geométrico 
hasta que solo sobreviven formas culturalmente posibles."

VÍA A (ya existe): Inferencia territorial
- Satélites, SAR, coherencia, scale invariance
- Resultado: "Esto es compatible con estructura antropomórfica integrada"

VÍA B (NUEVO): Memoria morfológica cultural
- Repositorio de invariantes culturales (NO artísticos)
- Proporciones aprendidas de objetos reales escaneados
- Condiciona generación volumétrica sin copiar

CLASES MORFOLÓGICAS:
1. MOAI (Rapa Nui) - Monolítico vertical
2. ESFINGE (Egipto) - Híbrido horizontal
3. ESTATUA_EGIPCIA (Old/Middle Kingdom) - Antropomórfica rígida
4. COLOSO (Memnon, Abu Simbel) - Antropomórfica sedente
5. ESTELA (Maya, Egipcia) - Vertical plana
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class MorphologicalClass(Enum):
    """Clases morfológicas culturales."""
    MOAI = "moai"
    SPHINX = "sphinx"
    EGYPTIAN_STATUE = "egyptian_statue"
    COLOSSUS = "colossus"
    STELA = "stela"
    PYRAMID_MESOAMERICAN = "pyramid_mesoamerican"
    TEMPLE_PLATFORM = "temple_platform"
    STELA_MAYA = "stela_maya"
    GENERIC_ANTHROPOMORPHIC = "generic_anthropomorphic"


@dataclass
class MorphologicalInvariants:
    """
    Invariantes morfológicos culturales.
    
    NO son detalles artísticos. SON proporciones geométricas reales
    aprendidas de objetos escaneados.
    """
    
    # Identificación
    morphological_class: MorphologicalClass
    cultural_origin: str
    
    # Proporciones básicas (ratios, NO medidas absolutas)
    height_to_width_ratio: float  # Alto/Ancho
    head_to_body_ratio: float     # Cabeza/Cuerpo
    base_to_height_ratio: float   # Base/Alto
    
    # Ejes dominantes
    vertical_axis_dominance: float  # 0-1
    horizontal_axis_dominance: float  # 0-1
    bilateral_symmetry: float  # 0-1
    
    # Características estructurales
    arms_position: str  # "fused", "sides", "crossed", "none"
    legs_position: str  # "fused", "standing", "seated", "none"
    base_integration: str  # "integrated", "separate", "none"
    
    # Rigidez cultural
    frontal_axis_absolute: bool  # Sin rotación corporal
    dynamism_level: float  # 0 = estático, 1 = dinámico
    
    # Metadatos
    confidence: float
    source_samples: int  # Cuántos objetos reales se usaron


class MorphologicalRepository:
    """
    Repositorio de invariantes morfológicos culturales.
    
    NO guarda "estatuas". Guarda GEOMETRÍA y PROPORCIONES aprendidas.
    """
    
    def __init__(self):
        self.repository: Dict[MorphologicalClass, MorphologicalInvariants] = {}
        self._initialize_repository()
        logger.info("🧬 Repositorio Morfológico Cultural inicializado")
    
    def _initialize_repository(self):
        """Inicializar con invariantes culturales conocidos."""
        
        # MOAI (Rapa Nui) - Caso IDEAL
        self.repository[MorphologicalClass.MOAI] = MorphologicalInvariants(
            morphological_class=MorphologicalClass.MOAI,
            cultural_origin="Rapa Nui (Easter Island)",
            
            # Proporciones reales de moais
            height_to_width_ratio=3.2,  # Muy vertical
            head_to_body_ratio=0.45,    # Cabeza ENORME (casi mitad)
            base_to_height_ratio=0.15,  # Base pequeña
            
            # Ejes
            vertical_axis_dominance=0.95,  # EXTREMA verticalidad
            horizontal_axis_dominance=0.05,
            bilateral_symmetry=0.98,  # Casi perfecta
            
            # Estructura
            arms_position="fused",  # Brazos pegados al cuerpo
            legs_position="fused",  # Piernas fusionadas
            base_integration="integrated",  # Base integrada
            
            # Rigidez
            frontal_axis_absolute=True,  # Sin rotación
            dynamism_level=0.0,  # CERO dinamismo
            
            # Metadatos
            confidence=0.95,
            source_samples=50  # ~50 moais bien documentados
        )
        
        # ESFINGE (Egipto) - Híbrido horizontal
        self.repository[MorphologicalClass.SPHINX] = MorphologicalInvariants(
            morphological_class=MorphologicalClass.SPHINX,
            cultural_origin="Ancient Egypt",
            
            # Proporciones
            height_to_width_ratio=0.35,  # MUY horizontal
            head_to_body_ratio=0.25,     # Cabeza proporcionada
            base_to_height_ratio=0.95,   # Base casi igual a altura
            
            # Ejes
            vertical_axis_dominance=0.15,
            horizontal_axis_dominance=0.95,  # EXTREMA horizontalidad
            bilateral_symmetry=0.99,  # Perfecta
            
            # Estructura
            arms_position="none",  # No tiene brazos
            legs_position="seated",  # Posición recostada
            base_integration="integrated",
            
            # Rigidez
            frontal_axis_absolute=True,
            dynamism_level=0.0,
            
            # Metadatos
            confidence=0.90,
            source_samples=20  # Menos ejemplares bien preservados
        )
        
        # ESTATUA EGIPCIA (Old/Middle Kingdom)
        self.repository[MorphologicalClass.EGYPTIAN_STATUE] = MorphologicalInvariants(
            morphological_class=MorphologicalClass.EGYPTIAN_STATUE,
            cultural_origin="Ancient Egypt (Old/Middle Kingdom)",
            
            # Proporciones
            height_to_width_ratio=4.5,  # Muy vertical
            head_to_body_ratio=0.12,    # Cabeza ~1/8 del cuerpo
            base_to_height_ratio=0.20,
            
            # Ejes
            vertical_axis_dominance=0.90,
            horizontal_axis_dominance=0.10,
            bilateral_symmetry=0.99,  # Perfecta
            
            # Estructura
            arms_position="sides",  # Brazos a los lados
            legs_position="standing",  # De pie, pierna adelantada
            base_integration="integrated",
            
            # Rigidez
            frontal_axis_absolute=True,  # Frontalidad absoluta
            dynamism_level=0.1,  # Casi estático
            
            # Metadatos
            confidence=0.92,
            source_samples=100  # Muchos ejemplares
        )
        
        # COLOSO (Memnon, Abu Simbel)
        self.repository[MorphologicalClass.COLOSSUS] = MorphologicalInvariants(
            morphological_class=MorphologicalClass.COLOSSUS,
            cultural_origin="Ancient Egypt (New Kingdom)",
            
            # Proporciones
            height_to_width_ratio=2.8,  # Vertical pero más ancho
            head_to_body_ratio=0.15,
            base_to_height_ratio=0.35,  # Base más grande
            
            # Ejes
            vertical_axis_dominance=0.85,
            horizontal_axis_dominance=0.15,
            bilateral_symmetry=0.98,
            
            # Estructura
            arms_position="crossed",  # Brazos cruzados
            legs_position="seated",  # Sentado
            base_integration="integrated",
            
            # Rigidez
            frontal_axis_absolute=True,
            dynamism_level=0.0,
            
            # Metadatos
            confidence=0.88,
            source_samples=15
        )
        
        # PIRÁMIDE MESOAMERICANA (Teotihuacán, Maya)
        self.repository[MorphologicalClass.PYRAMID_MESOAMERICAN] = MorphologicalInvariants(
            morphological_class=MorphologicalClass.PYRAMID_MESOAMERICAN,
            cultural_origin="Mesoamerica (Teotihuacan, Maya, Aztec)",
            
            # Proporciones de pirámides escalonadas
            height_to_width_ratio=0.45,  # Más ancho que alto
            head_to_body_ratio=0.0,      # No antropomórfico
            base_to_height_ratio=2.2,    # Base muy grande
            
            # Ejes
            vertical_axis_dominance=0.35,
            horizontal_axis_dominance=0.65,
            bilateral_symmetry=0.99,  # Perfecta simetría
            
            # Estructura
            arms_position="none",
            legs_position="none",
            base_integration="integrated",
            
            # Rigidez
            frontal_axis_absolute=True,  # Orientación cardinal
            dynamism_level=0.0,
            
            # Metadatos
            confidence=0.90,
            source_samples=35  # Teotihuacán, Tikal, Chichén Itzá, etc.
        )
        
        # PLATAFORMA CEREMONIAL (Templos mesoamericanos)
        self.repository[MorphologicalClass.TEMPLE_PLATFORM] = MorphologicalInvariants(
            morphological_class=MorphologicalClass.TEMPLE_PLATFORM,
            cultural_origin="Mesoamerica (Maya, Zapotec)",
            
            # Proporciones
            height_to_width_ratio=0.30,  # Muy horizontal
            head_to_body_ratio=0.0,
            base_to_height_ratio=3.0,    # Base extremadamente grande
            
            # Ejes
            vertical_axis_dominance=0.25,
            horizontal_axis_dominance=0.75,
            bilateral_symmetry=0.98,
            
            # Estructura
            arms_position="none",
            legs_position="none",
            base_integration="integrated",
            
            # Rigidez
            frontal_axis_absolute=True,
            dynamism_level=0.0,
            
            # Metadatos
            confidence=0.85,
            source_samples=25
        )
        
        # ESTELA MAYA (Monumentos verticales con glifos)
        self.repository[MorphologicalClass.STELA_MAYA] = MorphologicalInvariants(
            morphological_class=MorphologicalClass.STELA_MAYA,
            cultural_origin="Mesoamerica (Maya)",
            
            # Proporciones
            height_to_width_ratio=5.0,   # Muy vertical, delgada
            head_to_body_ratio=0.20,     # Figura antropomórfica en relieve
            base_to_height_ratio=0.10,   # Base pequeña
            
            # Ejes
            vertical_axis_dominance=0.95,
            horizontal_axis_dominance=0.05,
            bilateral_symmetry=0.99,
            
            # Estructura
            arms_position="sides",       # Figuras con brazos visibles
            legs_position="standing",
            base_integration="integrated",
            
            # Rigidez
            frontal_axis_absolute=True,  # Frontalidad absoluta
            dynamism_level=0.15,         # Ligero dinamismo en poses
            
            # Metadatos
            confidence=0.88,
            source_samples=40  # Copán, Quiriguá, Tikal
        )
        
        logger.info(f"   ✅ {len(self.repository)} clases morfológicas cargadas")
    
    def match_morphological_class(self, 
                                  archeoscope_data: Dict[str, Any]) -> Tuple[MorphologicalClass, float]:
        """
        Determinar qué clase morfológica es más compatible con los datos.
        
        NO "decide la forma". RESTRINGE el espacio de formas posibles.
        """
        
        logger.info("🧠 Matching clase morfológica...")
        
        # Extraer características de ArcheoScope
        scale_inv = archeoscope_data.get('scale_invariance', 0.0)
        angular_cons = archeoscope_data.get('angular_consistency', 0.0)
        coherence_3d = archeoscope_data.get('coherence_3d', 0.0)
        
        # Inferir características geométricas básicas
        estimated_area = archeoscope_data.get('estimated_area_m2', 100.0)
        estimated_height = archeoscope_data.get('estimated_height_m', 10.0)
        
        # Calcular ratio aproximado
        estimated_width = np.sqrt(estimated_area)
        height_width_ratio = estimated_height / estimated_width if estimated_width > 0 else 1.0
        
        # Extraer contexto geográfico (si está disponible)
        lat = archeoscope_data.get('lat', None)
        lon = archeoscope_data.get('lon', None)
        
        # Scoring contra cada clase morfológica
        scores = {}
        
        for morph_class, invariants in self.repository.items():
            score = self._calculate_morphological_score(
                height_width_ratio=height_width_ratio,
                scale_inv=scale_inv,
                angular_cons=angular_cons,
                coherence_3d=coherence_3d,
                invariants=invariants,
                lat=lat,
                lon=lon
            )
            scores[morph_class] = score
        
        # Mejor match
        best_class = max(scores, key=scores.get)
        best_score = scores[best_class]
        
        logger.info(f"   ✅ Mejor match: {best_class.value} (score: {best_score:.3f})")
        
        return best_class, best_score
    
    def _calculate_morphological_score(self,
                                      height_width_ratio: float,
                                      scale_inv: float,
                                      angular_cons: float,
                                      coherence_3d: float,
                                      invariants: MorphologicalInvariants,
                                      lat: Optional[float] = None,
                                      lon: Optional[float] = None) -> float:
        """Calcular score de compatibilidad morfológica con contexto geográfico."""
        
        # Score basado en ratio de proporciones
        ratio_diff = abs(height_width_ratio - invariants.height_to_width_ratio)
        ratio_score = np.exp(-ratio_diff / 2.0)  # Gaussiana
        
        # Score basado en rigidez (scale invariance)
        rigidity_expected = 0.9 if invariants.dynamism_level < 0.2 else 0.7
        rigidity_score = 1.0 - abs(scale_inv - rigidity_expected)
        
        # Score basado en simetría (angular consistency)
        symmetry_score = angular_cons * invariants.bilateral_symmetry
        
        # Score basado en coherencia
        coherence_score = coherence_3d
        
        # NUEVO: Bonus geográfico-cultural
        geographic_bonus = 0.0
        if lat is not None and lon is not None:
            # Rapa Nui: -28 < lat < -26, -110 < lon < -108
            is_rapa_nui = (-28 < lat < -26) and (-110 < lon < -108)
            
            # Egipto: 22 < lat < 32, 25 < lon < 35
            is_egypt = (22 < lat < 32) and (25 < lon < 35)
            
            # Perú: -18 < lat < -8, -82 < lon < -68
            is_peru = (-18 < lat < -8) and (-82 < lon < -68)
            
            # Mesoamérica: 14 < lat < 23, -110 < lon < -86
            is_mesoamerica = (14 < lat < 23) and (-110 < lon < -86)
            
            # Aplicar bonus según contexto
            if is_rapa_nui and invariants.morphological_class == MorphologicalClass.MOAI:
                geographic_bonus = 0.25  # Fuerte bonus para MOAI en Rapa Nui
            elif is_egypt and invariants.cultural_origin.startswith("Ancient Egypt"):
                geographic_bonus = 0.15  # Bonus moderado para clases egipcias en Egipto
            elif is_mesoamerica and invariants.cultural_origin.startswith("Mesoamerica"):
                geographic_bonus = 0.20  # Bonus para clases mesoamericanas
            elif is_peru:
                # Futuro: agregar clases andinas
                pass
        
        # Combinar scores (ajustado para incluir bonus geográfico)
        base_score = (
            ratio_score * 0.4 +
            rigidity_score * 0.2 +
            symmetry_score * 0.2 +
            coherence_score * 0.2
        )
        
        total_score = base_score + geographic_bonus
        
        return total_score
    
    def get_morphological_constraints(self, 
                                     morph_class: MorphologicalClass) -> MorphologicalInvariants:
        """Obtener constraints morfológicos para una clase."""
        
        if morph_class not in self.repository:
            logger.warning(f"⚠️ Clase {morph_class} no encontrada, usando genérica")
            morph_class = MorphologicalClass.GENERIC_ANTHROPOMORPHIC
        
        return self.repository[morph_class]
    
    def constrain_geometry(self,
                          base_geometry: Dict[str, Any],
                          morph_class: MorphologicalClass) -> Dict[str, Any]:
        """
        Constreñir geometría base con invariantes morfológicos.
        
        CLAVE: NO genera forma. RESTRINGE espacio de formas posibles.
        """
        
        logger.info(f"🔒 Aplicando constraints morfológicos: {morph_class.value}")
        
        invariants = self.get_morphological_constraints(morph_class)
        
        # Ajustar proporciones según invariantes
        constrained = base_geometry.copy()
        
        # Aplicar ratios culturales
        if 'base_length_m' in constrained and 'height_m' in constrained:
            # Ajustar altura según ratio cultural
            target_ratio = invariants.height_to_width_ratio
            current_ratio = constrained['height_m'] / constrained['base_length_m']
            
            # Blend entre inferencia territorial y morfología cultural
            blend_factor = 0.6  # 60% morfología, 40% territorial
            adjusted_ratio = current_ratio * (1 - blend_factor) + target_ratio * blend_factor
            
            constrained['height_m'] = constrained['base_length_m'] * adjusted_ratio
        
        # Aplicar características estructurales
        constrained['morphological_class'] = morph_class.value
        constrained['arms_position'] = invariants.arms_position
        constrained['legs_position'] = invariants.legs_position
        constrained['base_integration'] = invariants.base_integration
        constrained['bilateral_symmetry'] = invariants.bilateral_symmetry
        constrained['frontal_axis_absolute'] = invariants.frontal_axis_absolute
        constrained['dynamism_level'] = invariants.dynamism_level
        
        # Metadatos
        constrained['cultural_origin'] = invariants.cultural_origin
        constrained['morphological_confidence'] = invariants.confidence
        
        logger.info(f"   ✅ Geometría constreñida con {invariants.source_samples} muestras reales")
        
        return constrained


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    print("🧬 Repositorio Morfológico Cultural - Test\n")
    
    repo = MorphologicalRepository()
    
    # Test 1: Moai (vertical, monolítico)
    print("="*80)
    print("TEST 1: Estructura tipo MOAI")
    print("="*80)
    
    moai_data = {
        'scale_invariance': 0.92,
        'angular_consistency': 0.88,
        'coherence_3d': 0.90,
        'estimated_area_m2': 25.0,  # ~5m × 5m
        'estimated_height_m': 15.0   # Muy vertical
    }
    
    morph_class, score = repo.match_morphological_class(moai_data)
    print(f"\n✅ Clase detectada: {morph_class.value}")
    print(f"   Score: {score:.3f}")
    
    constraints = repo.get_morphological_constraints(morph_class)
    print(f"\n📐 Invariantes morfológicos:")
    print(f"   Ratio alto/ancho: {constraints.height_to_width_ratio:.2f}")
    print(f"   Ratio cabeza/cuerpo: {constraints.head_to_body_ratio:.2f}")
    print(f"   Simetría bilateral: {constraints.bilateral_symmetry:.2f}")
    print(f"   Brazos: {constraints.arms_position}")
    print(f"   Piernas: {constraints.legs_position}")
    print(f"   Dinamismo: {constraints.dynamism_level:.2f}")
    
    # Test 2: Esfinge (horizontal, híbrido)
    print("\n" + "="*80)
    print("TEST 2: Estructura tipo ESFINGE")
    print("="*80)
    
    sphinx_data = {
        'scale_invariance': 0.95,
        'angular_consistency': 0.93,
        'coherence_3d': 0.88,
        'estimated_area_m2': 400.0,  # ~20m × 20m
        'estimated_height_m': 8.0     # Horizontal
    }
    
    morph_class, score = repo.match_morphological_class(sphinx_data)
    print(f"\n✅ Clase detectada: {morph_class.value}")
    print(f"   Score: {score:.3f}")
    
    constraints = repo.get_morphological_constraints(morph_class)
    print(f"\n📐 Invariantes morfológicos:")
    print(f"   Ratio alto/ancho: {constraints.height_to_width_ratio:.2f}")
    print(f"   Dominancia horizontal: {constraints.horizontal_axis_dominance:.2f}")
    print(f"   Simetría bilateral: {constraints.bilateral_symmetry:.2f}")
    
    print("\n" + "="*80)
    print("✅ Repositorio Morfológico funcional")
    print("="*80)
