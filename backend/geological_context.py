#!/usr/bin/env python3
"""
Geological Context System - Substrato Geológico
==============================================

EL GRAN FALTANTE: Contexto geológico para diferenciar anomalías culturales vs ruido geológico.

FUENTES PÚBLICAS:
- OneGeology (global geological data)
- USGS Geological Surveys
- GLiM (Global Lithological Map)
- National geological surveys

VALOR AGREGADO:
- Diferencia "anomalía cultural" vs "ruido geológico"
- Profundidad plausible (no solo estimada)
- Mejora brutal de coherencia 3D
- Contexto litológico para interpretación

Sin esto, el "subsuelo" sigue siendo probabilístico, no contextual.
"""

import requests
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)

class LithologyType(Enum):
    """Tipos litológicos principales."""
    SEDIMENTARY = "sedimentary"
    IGNEOUS = "igneous"
    METAMORPHIC = "metamorphic"
    UNCONSOLIDATED = "unconsolidated"
    WATER = "water"
    UNKNOWN = "unknown"

class GeologicalAge(Enum):
    """Edades geológicas simplificadas."""
    QUATERNARY = "quaternary"
    TERTIARY = "tertiary"
    MESOZOIC = "mesozoic"
    PALEOZOIC = "paleozoic"
    PRECAMBRIAN = "precambrian"
    UNKNOWN = "unknown"

@dataclass
class GeologicalContext:
    """Contexto geológico de un territorio."""
    
    # Litología dominante
    dominant_lithology: LithologyType
    lithology_confidence: float
    
    # Edad geológica
    geological_age: GeologicalAge
    age_confidence: float
    
    # Características estructurales
    fault_density: float  # Densidad de fallas por km²
    fracture_intensity: float  # Intensidad de fracturación
    
    # Depósitos superficiales
    quaternary_deposits: bool
    deposit_thickness_m: float
    
    # Compatibilidad arqueológica
    archaeological_suitability: float  # 0-1
    preservation_potential: float  # 0-1
    
    # Explicación geológica
    geological_explanation: str

@dataclass
class GeologicalCompatibilityScore:
    """Score de compatibilidad geológica (GCS)."""
    
    gcs_score: float  # 0-1
    lithology_factor: float
    age_factor: float
    structure_factor: float
    deposit_factor: float
    
    compatibility_explanation: str
    geological_risks: List[str]
    archaeological_advantages: List[str]

class GeologicalContextSystem:
    """Sistema de contexto geológico para ETP."""
    
    def __init__(self):
        """Inicializar sistema geológico."""
        
        # URLs de fuentes geológicas públicas
        self.geological_sources = {
            'onegeology': 'https://portal.onegeology.org/OnegeologyGlobal/',
            'usgs': 'https://mrdata.usgs.gov/geology/state/',
            'glim': 'https://www.geo.uni-hamburg.de/en/geologie/forschung/aquatische-geochemie/glim.html',
            'macrostrat': 'https://macrostrat.org/api/v2/units'
        }
        
        # Mapeo de compatibilidad arqueológica por litología
        self.archaeological_compatibility = {
            LithologyType.SEDIMENTARY: 0.9,      # Excelente para preservación
            LithologyType.UNCONSOLIDATED: 0.8,   # Bueno, fácil excavación
            LithologyType.IGNEOUS: 0.4,          # Difícil, pero estructuras visibles
            LithologyType.METAMORPHIC: 0.5,      # Moderado
            LithologyType.WATER: 0.1,            # Muy difícil
            LithologyType.UNKNOWN: 0.5           # Neutro
        }
        
        # Potencial de preservación por edad
        self.preservation_potential = {
            GeologicalAge.QUATERNARY: 0.9,       # Excelente preservación
            GeologicalAge.TERTIARY: 0.7,         # Buena preservación
            GeologicalAge.MESOZOIC: 0.5,         # Moderada
            GeologicalAge.PALEOZOIC: 0.3,        # Difícil
            GeologicalAge.PRECAMBRIAN: 0.2,      # Muy difícil
            GeologicalAge.UNKNOWN: 0.5           # Neutro
        }
        
        logger.info("🗿 Geological Context System initialized")
    
    async def get_geological_context(self, lat_min: float, lat_max: float,
                                   lon_min: float, lon_max: float) -> GeologicalContext:
        """
        Obtener contexto geológico para un territorio.
        
        CRÍTICO: Diferencia anomalías culturales de ruido geológico.
        """
        
        logger.info(f"🗿 Obteniendo contexto geológico para [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
        
        try:
            # Intentar múltiples fuentes geológicas
            geological_data = await self._query_geological_sources(lat_min, lat_max, lon_min, lon_max)
            
            # Procesar datos geológicos
            context = self._process_geological_data(geological_data)
            
            logger.info(f"✅ Contexto geológico obtenido: {context.dominant_lithology.value}")
            
            return context
            
        except Exception as e:
            logger.warning(f"⚠️ Error obteniendo contexto geológico: {e}")
            return self._create_default_geological_context()
    
    async def _query_geological_sources(self, lat_min: float, lat_max: float,
                                      lon_min: float, lon_max: float) -> Dict[str, Any]:
        """Consultar fuentes geológicas públicas."""
        
        geological_data = {}
        
        # Fuente 1: Macrostrat API (más accesible)
        try:
            macrostrat_data = await self._query_macrostrat(lat_min, lat_max, lon_min, lon_max)
            if macrostrat_data:
                geological_data['macrostrat'] = macrostrat_data
                logger.info("✅ Datos Macrostrat obtenidos")
        except Exception as e:
            logger.warning(f"⚠️ Macrostrat failed: {e}")
        
        # Fuente 2: USGS (si está en USA)
        if -180 <= lon_min <= -60 and 20 <= lat_min <= 70:  # Aproximadamente USA
            try:
                usgs_data = await self._query_usgs_geology(lat_min, lat_max, lon_min, lon_max)
                if usgs_data:
                    geological_data['usgs'] = usgs_data
                    logger.info("✅ Datos USGS obtenidos")
            except Exception as e:
                logger.warning(f"⚠️ USGS failed: {e}")
        
        # Fuente 3: Estimación basada en coordenadas (fallback)
        if not geological_data:
            geological_data['estimated'] = self._estimate_geology_from_coordinates(
                lat_min, lat_max, lon_min, lon_max
            )
            logger.info("✅ Geología estimada por coordenadas")
        
        return geological_data
    
    async def _query_macrostrat(self, lat_min: float, lat_max: float,
                               lon_min: float, lon_max: float) -> Optional[Dict[str, Any]]:
        """Consultar API de Macrostrat."""
        
        try:
            # Centro del área
            lat_center = (lat_min + lat_max) / 2
            lon_center = (lon_min + lon_max) / 2
            
            # Consulta a Macrostrat
            url = f"{self.geological_sources['macrostrat']}"
            params = {
                'lat': lat_center,
                'lng': lon_center,
                'format': 'json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and data.get('data'):
                    units = data['data']
                    
                    # Procesar unidades geológicas
                    processed_data = {
                        'units': [],
                        'dominant_lithology': None,
                        'geological_age': None
                    }
                    
                    for unit in units[:5]:  # Primeras 5 unidades
                        processed_data['units'].append({
                            'name': unit.get('unit_name', 'Unknown'),
                            'lithology': unit.get('lith', 'unknown'),
                            'age': unit.get('age', 'unknown'),
                            'thickness': unit.get('max_thick', 0)
                        })
                    
                    # Determinar litología dominante
                    if units:
                        dominant_unit = units[0]
                        processed_data['dominant_lithology'] = dominant_unit.get('lith', 'unknown')
                        processed_data['geological_age'] = dominant_unit.get('age', 'unknown')
                    
                    return processed_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error consultando Macrostrat: {e}")
            return None
    
    async def _query_usgs_geology(self, lat_min: float, lat_max: float,
                                 lon_min: float, lon_max: float) -> Optional[Dict[str, Any]]:
        """Consultar datos geológicos USGS (para USA)."""
        
        try:
            # Implementación simplificada - en producción usar APIs específicas
            # Por ahora retornar estructura básica
            
            return {
                'source': 'usgs_estimated',
                'dominant_lithology': 'sedimentary',
                'geological_age': 'quaternary',
                'confidence': 0.6
            }
            
        except Exception as e:
            logger.error(f"Error consultando USGS: {e}")
            return None
    
    def _estimate_geology_from_coordinates(self, lat_min: float, lat_max: float,
                                         lon_min: float, lon_max: float) -> Dict[str, Any]:
        """Estimar geología basada en coordenadas geográficas."""
        
        lat_center = (lat_min + lat_max) / 2
        lon_center = (lon_min + lon_max) / 2
        
        # Estimaciones geológicas muy básicas por región
        if abs(lat_center) < 30:  # Trópicos
            if abs(lat_center) < 10:  # Ecuatorial
                lithology = 'unconsolidated'
                age = 'quaternary'
            else:  # Subtropical
                lithology = 'sedimentary'
                age = 'tertiary'
        elif abs(lat_center) < 60:  # Templado
            lithology = 'sedimentary'
            age = 'quaternary'
        else:  # Polar
            lithology = 'igneous'
            age = 'precambrian'
        
        # Ajustes por elevación estimada (muy básico)
        if abs(lat_center) > 45:  # Latitudes altas - más rocas antiguas
            age = 'paleozoic'
            lithology = 'metamorphic'
        
        return {
            'source': 'coordinate_estimation',
            'dominant_lithology': lithology,
            'geological_age': age,
            'confidence': 0.3,  # Baja confianza para estimaciones
            'method': 'geographic_inference'
        }
    
    def _process_geological_data(self, geological_data: Dict[str, Any]) -> GeologicalContext:
        """Procesar datos geológicos en contexto estructurado."""
        
        # Determinar litología dominante
        dominant_lithology = self._determine_dominant_lithology(geological_data)
        lithology_confidence = self._calculate_lithology_confidence(geological_data)
        
        # Determinar edad geológica
        geological_age = self._determine_geological_age(geological_data)
        age_confidence = self._calculate_age_confidence(geological_data)
        
        # Calcular características estructurales
        fault_density = self._estimate_fault_density(geological_data)
        fracture_intensity = self._estimate_fracture_intensity(geological_data)
        
        # Evaluar depósitos cuaternarios
        quaternary_deposits = self._has_quaternary_deposits(geological_data)
        deposit_thickness = self._estimate_deposit_thickness(geological_data)
        
        # Calcular compatibilidad arqueológica
        archaeological_suitability = self.archaeological_compatibility.get(dominant_lithology, 0.5)
        preservation_potential = self.preservation_potential.get(geological_age, 0.5)
        
        # Generar explicación geológica
        explanation = self._generate_geological_explanation(
            dominant_lithology, geological_age, quaternary_deposits
        )
        
        return GeologicalContext(
            dominant_lithology=dominant_lithology,
            lithology_confidence=lithology_confidence,
            geological_age=geological_age,
            age_confidence=age_confidence,
            fault_density=fault_density,
            fracture_intensity=fracture_intensity,
            quaternary_deposits=quaternary_deposits,
            deposit_thickness_m=deposit_thickness,
            archaeological_suitability=archaeological_suitability,
            preservation_potential=preservation_potential,
            geological_explanation=explanation
        )
    
    def calculate_geological_compatibility_score(self, geological_context: GeologicalContext,
                                               anomaly_depth_m: float) -> GeologicalCompatibilityScore:
        """
        Calcular Geological Compatibility Score (GCS).
        
        CRÍTICO: Diferencia anomalías culturales de ruido geológico.
        """
        
        # Factor litológico
        lithology_factor = geological_context.archaeological_suitability
        
        # Factor de edad (más reciente = mejor para arqueología)
        age_factor = geological_context.preservation_potential
        
        # Factor estructural (menos fallas = mejor preservación)
        structure_factor = max(0.1, 1.0 - geological_context.fault_density / 10.0)
        
        # Factor de depósitos (depósitos cuaternarios = mejor para arqueología)
        if geological_context.quaternary_deposits:
            deposit_factor = min(1.0, geological_context.deposit_thickness_m / 10.0)
        else:
            deposit_factor = 0.3
        
        # Ajuste por profundidad de anomalía
        depth_compatibility = self._calculate_depth_compatibility(
            anomaly_depth_m, geological_context
        )
        
        # GCS final
        gcs_score = (
            lithology_factor * 0.3 +
            age_factor * 0.25 +
            structure_factor * 0.2 +
            deposit_factor * 0.15 +
            depth_compatibility * 0.1
        )
        
        # Generar explicación
        compatibility_explanation = self._generate_compatibility_explanation(
            gcs_score, lithology_factor, age_factor, structure_factor, deposit_factor
        )
        
        # Identificar riesgos y ventajas
        geological_risks = self._identify_geological_risks(geological_context)
        archaeological_advantages = self._identify_archaeological_advantages(geological_context)
        
        return GeologicalCompatibilityScore(
            gcs_score=gcs_score,
            lithology_factor=lithology_factor,
            age_factor=age_factor,
            structure_factor=structure_factor,
            deposit_factor=deposit_factor,
            compatibility_explanation=compatibility_explanation,
            geological_risks=geological_risks,
            archaeological_advantages=archaeological_advantages
        )
    
    # Métodos auxiliares de procesamiento
    
    def _determine_dominant_lithology(self, geological_data: Dict[str, Any]) -> LithologyType:
        """Determinar litología dominante."""
        
        for source_name, data in geological_data.items():
            if 'dominant_lithology' in data:
                lithology_str = data['dominant_lithology'].lower()
                
                if 'sediment' in lithology_str or 'sand' in lithology_str or 'clay' in lithology_str:
                    return LithologyType.SEDIMENTARY
                elif 'igneous' in lithology_str or 'volcanic' in lithology_str or 'granite' in lithology_str:
                    return LithologyType.IGNEOUS
                elif 'metamorphic' in lithology_str or 'schist' in lithology_str or 'gneiss' in lithology_str:
                    return LithologyType.METAMORPHIC
                elif 'unconsolidated' in lithology_str or 'alluvium' in lithology_str:
                    return LithologyType.UNCONSOLIDATED
        
        return LithologyType.UNKNOWN
    
    def _determine_geological_age(self, geological_data: Dict[str, Any]) -> GeologicalAge:
        """Determinar edad geológica dominante."""
        
        for source_name, data in geological_data.items():
            if 'geological_age' in data:
                age_str = data['geological_age'].lower()
                
                if 'quaternary' in age_str or 'holocene' in age_str or 'pleistocene' in age_str:
                    return GeologicalAge.QUATERNARY
                elif 'tertiary' in age_str or 'neogene' in age_str or 'paleogene' in age_str:
                    return GeologicalAge.TERTIARY
                elif 'mesozoic' in age_str or 'cretaceous' in age_str or 'jurassic' in age_str:
                    return GeologicalAge.MESOZOIC
                elif 'paleozoic' in age_str or 'permian' in age_str or 'carboniferous' in age_str:
                    return GeologicalAge.PALEOZOIC
                elif 'precambrian' in age_str or 'archean' in age_str:
                    return GeologicalAge.PRECAMBRIAN
        
        return GeologicalAge.UNKNOWN
    
    def _calculate_lithology_confidence(self, geological_data: Dict[str, Any]) -> float:
        """Calcular confianza en la determinación litológica."""
        
        confidence_scores = []
        
        for source_name, data in geological_data.items():
            if 'confidence' in data:
                confidence_scores.append(data['confidence'])
            elif source_name == 'macrostrat':
                confidence_scores.append(0.8)  # Alta confianza en Macrostrat
            elif source_name == 'usgs':
                confidence_scores.append(0.9)  # Muy alta confianza en USGS
            else:
                confidence_scores.append(0.3)  # Baja confianza en estimaciones
        
        return np.mean(confidence_scores) if confidence_scores else 0.3
    
    def _calculate_age_confidence(self, geological_data: Dict[str, Any]) -> float:
        """Calcular confianza en la determinación de edad."""
        return self._calculate_lithology_confidence(geological_data)  # Mismo método
    
    def _estimate_fault_density(self, geological_data: Dict[str, Any]) -> float:
        """Estimar densidad de fallas por km²."""
        
        # Estimación muy básica basada en tipo de roca
        for source_name, data in geological_data.items():
            lithology = data.get('dominant_lithology', '').lower()
            
            if 'igneous' in lithology or 'volcanic' in lithology:
                return 2.0  # Rocas ígneas tienden a tener más fallas
            elif 'metamorphic' in lithology:
                return 3.0  # Rocas metamórficas muy fracturadas
            elif 'sedimentary' in lithology:
                return 1.0  # Rocas sedimentarias menos fracturadas
            else:
                return 0.5  # Depósitos no consolidados
        
        return 1.0  # Valor por defecto
    
    def _estimate_fracture_intensity(self, geological_data: Dict[str, Any]) -> float:
        """Estimar intensidad de fracturación (0-1)."""
        fault_density = self._estimate_fault_density(geological_data)
        return min(1.0, fault_density / 5.0)  # Normalizar a 0-1
    
    def _has_quaternary_deposits(self, geological_data: Dict[str, Any]) -> bool:
        """Determinar si hay depósitos cuaternarios."""
        
        for source_name, data in geological_data.items():
            age = data.get('geological_age', '').lower()
            lithology = data.get('dominant_lithology', '').lower()
            
            if ('quaternary' in age or 'holocene' in age or 
                'unconsolidated' in lithology or 'alluvium' in lithology):
                return True
        
        return False
    
    def _estimate_deposit_thickness(self, geological_data: Dict[str, Any]) -> float:
        """Estimar espesor de depósitos superficiales."""
        
        if self._has_quaternary_deposits(geological_data):
            # Estimación básica basada en contexto
            for source_name, data in geological_data.items():
                if 'units' in data:
                    for unit in data['units']:
                        thickness = unit.get('thickness', 0)
                        if thickness > 0:
                            return min(50.0, thickness)  # Máximo 50m
            
            return 5.0  # Valor por defecto para depósitos cuaternarios
        else:
            return 0.0  # Sin depósitos superficiales
    
    def _calculate_depth_compatibility(self, anomaly_depth_m: float, 
                                     geological_context: GeologicalContext) -> float:
        """Calcular compatibilidad de profundidad con geología."""
        
        depth = abs(anomaly_depth_m)
        
        # Compatibilidad basada en tipo de roca y profundidad
        if geological_context.quaternary_deposits:
            # Con depósitos cuaternarios
            if depth <= geological_context.deposit_thickness_m:
                return 1.0  # Perfecta compatibilidad
            elif depth <= geological_context.deposit_thickness_m * 2:
                return 0.7  # Buena compatibilidad
            else:
                return 0.3  # Baja compatibilidad
        else:
            # Sin depósitos cuaternarios - más difícil
            if depth <= 2.0:
                return 0.8  # Buena para estructuras superficiales
            elif depth <= 5.0:
                return 0.5  # Moderada
            else:
                return 0.2  # Baja para estructuras profundas
    
    def _generate_geological_explanation(self, lithology: LithologyType, 
                                       age: GeologicalAge, 
                                       quaternary_deposits: bool) -> str:
        """Generar explicación geológica."""
        
        explanations = []
        
        # Explicación litológica
        if lithology == LithologyType.SEDIMENTARY:
            explanations.append("Rocas sedimentarias favorables para preservación arqueológica")
        elif lithology == LithologyType.UNCONSOLIDATED:
            explanations.append("Depósitos no consolidados, excelentes para arqueología")
        elif lithology == LithologyType.IGNEOUS:
            explanations.append("Rocas ígneas, estructuras arqueológicas más visibles pero difíciles de excavar")
        elif lithology == LithologyType.METAMORPHIC:
            explanations.append("Rocas metamórficas, preservación moderada")
        
        # Explicación de edad
        if age == GeologicalAge.QUATERNARY:
            explanations.append("Edad cuaternaria, excelente para preservación arqueológica")
        elif age == GeologicalAge.TERTIARY:
            explanations.append("Edad terciaria, buena preservación")
        else:
            explanations.append("Rocas antiguas, preservación arqueológica limitada")
        
        # Depósitos cuaternarios
        if quaternary_deposits:
            explanations.append("Presencia de depósitos cuaternarios favorece la preservación")
        
        return ". ".join(explanations) + "."
    
    def _generate_compatibility_explanation(self, gcs_score: float, 
                                          lithology_factor: float,
                                          age_factor: float, 
                                          structure_factor: float,
                                          deposit_factor: float) -> str:
        """Generar explicación de compatibilidad geológica."""
        
        if gcs_score > 0.8:
            return f"Excelente compatibilidad geológica (GCS: {gcs_score:.2f}). Condiciones óptimas para preservación arqueológica."
        elif gcs_score > 0.6:
            return f"Buena compatibilidad geológica (GCS: {gcs_score:.2f}). Condiciones favorables para arqueología."
        elif gcs_score > 0.4:
            return f"Compatibilidad geológica moderada (GCS: {gcs_score:.2f}). Preservación variable según contexto."
        else:
            return f"Baja compatibilidad geológica (GCS: {gcs_score:.2f}). Condiciones desafiantes para preservación arqueológica."
    
    def _identify_geological_risks(self, geological_context: GeologicalContext) -> List[str]:
        """Identificar riesgos geológicos para arqueología."""
        
        risks = []
        
        if geological_context.fault_density > 2.0:
            risks.append("Alta densidad de fallas puede afectar preservación")
        
        if geological_context.dominant_lithology == LithologyType.IGNEOUS:
            risks.append("Rocas ígneas dificultan excavación")
        
        if not geological_context.quaternary_deposits:
            risks.append("Ausencia de depósitos cuaternarios limita preservación")
        
        if geological_context.geological_age in [GeologicalAge.PALEOZOIC, GeologicalAge.PRECAMBRIAN]:
            risks.append("Rocas muy antiguas con preservación limitada")
        
        return risks
    
    def _identify_archaeological_advantages(self, geological_context: GeologicalContext) -> List[str]:
        """Identificar ventajas geológicas para arqueología."""
        
        advantages = []
        
        if geological_context.quaternary_deposits:
            advantages.append("Depósitos cuaternarios favorecen preservación")
        
        if geological_context.dominant_lithology == LithologyType.SEDIMENTARY:
            advantages.append("Rocas sedimentarias excelentes para preservación")
        
        if geological_context.geological_age == GeologicalAge.QUATERNARY:
            advantages.append("Edad cuaternaria óptima para arqueología")
        
        if geological_context.fault_density < 1.0:
            advantages.append("Baja fracturación favorece integridad estructural")
        
        return advantages
    
    def _create_default_geological_context(self) -> GeologicalContext:
        """Crear contexto geológico por defecto cuando fallan las fuentes."""
        
        return GeologicalContext(
            dominant_lithology=LithologyType.UNKNOWN,
            lithology_confidence=0.1,
            geological_age=GeologicalAge.UNKNOWN,
            age_confidence=0.1,
            fault_density=1.0,
            fracture_intensity=0.5,
            quaternary_deposits=False,
            deposit_thickness_m=0.0,
            archaeological_suitability=0.5,
            preservation_potential=0.5,
            geological_explanation="Contexto geológico no disponible - usando valores por defecto"
        )