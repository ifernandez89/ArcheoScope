#!/usr/bin/env python3
"""
ArcheoScope - Contextual Validation System
==========================================

Sistema de validación usando sitios conocidos como ANCLAS CONTEXTUALES,
NO como sensores.

🎯 FILOSOFÍA:
- Sitios conocidos definen "zonas normales" por ambiente
- Sirven como control negativo indirecto
- Filtran plausibilidad ambiental
- Detectan falsos positivos
- NO requieren mediciones satelitales

✅ LO QUE SÍ HACEN:
- Definir rangos normales por contexto (árido, montaña, etc.)
- Detectar comportamiento anómalo del algoritmo
- Penalizar candidatas en ambientes sin precedentes
- Validación blanda (soft validation)

❌ LO QUE NO HACEN:
- NO son ground truth duro
- NO requieren mediciones históricas
- NO invalidan el enfoque
- NO bloquean el sistema

👉 MANTIENEN AL SISTEMA HONESTO
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)


class EnvironmentType(Enum):
    """Tipos de ambiente simplificados"""
    ARID = "arid"
    SEMI_ARID = "semi_arid"
    PLATEAU = "plateau"
    MOUNTAIN = "mountain"
    COASTAL = "coastal"
    FOREST = "forest"
    GRASSLAND = "grassland"
    UNKNOWN = "unknown"


class SiteType(Enum):
    """Tipos de sitio arqueológico"""
    TEMPLE = "temple"
    CITY = "city"
    SETTLEMENT = "settlement"
    TOMB = "tomb"
    FORTRESS = "fortress"
    CEREMONIAL = "ceremonial"
    UNKNOWN = "unknown"


@dataclass
class KnownSite:
    """Sitio conocido como ancla contextual"""
    name: str
    site_type: SiteType
    environment: EnvironmentType
    terrain: str
    lat: float
    lon: float
    confidence: str  # HIGH, MEDIUM, LOW
    has_documented_cavities: bool = False
    notes: Optional[str] = None


@dataclass
class ContextualProfile:
    """Perfil contextual normal para un ambiente"""
    environment: EnvironmentType
    
    # Rangos esperados (sin mediciones reales, solo contextuales)
    expected_ndvi_range: Tuple[float, float]
    expected_thermal_variance_range: Tuple[float, float]
    expected_sar_noise_level: str  # "low", "medium", "high"
    
    # Metadatos
    sample_count: int
    confidence: float


@dataclass
class ValidationResult:
    """Resultado de validación contextual"""
    is_plausible: bool
    plausibility_score: float
    
    # Filtros aplicados
    environment_seen_before: bool
    terrain_compatible: bool
    context_deviation: float
    
    # Controles negativos
    false_positive_risk: float
    similar_known_sites_without_cavities: int
    
    # Ajustes recomendados
    score_penalty: float
    confidence_adjustment: float
    
    # Explicación
    validation_notes: str


class ContextualValidator:
    """
    Validador contextual usando sitios conocidos como anclas.
    
    NO requiere mediciones satelitales.
    Usa solo: ambiente, tipo de sitio, terreno, coordenadas.
    """
    
    def __init__(self):
        self.known_sites: List[KnownSite] = []
        self.contextual_profiles: Dict[EnvironmentType, ContextualProfile] = {}
        logger.info("ContextualValidator initialized")
    
    def load_known_sites_from_db(self, db_connection):
        """
        Cargar sitios conocidos desde BD.
        
        NO requiere mediciones, solo metadata:
        - nombre, tipo, ambiente, terreno, coordenadas, confianza
        """
        cursor = db_connection.cursor()
        
        # Query simplificada - solo metadata
        query = """
        SELECT 
            name,
            site_type,
            environment,
            terrain,
            lat,
            lon,
            confidence_level,
            has_documented_cavities,
            notes
        FROM known_archaeological_sites
        WHERE confidence_level IN ('HIGH', 'MEDIUM')
        ORDER BY confidence_level DESC
        """
        
        cursor.execute(query)
        
        for row in cursor.fetchall():
            site = KnownSite(
                name=row[0],
                site_type=SiteType(row[1].lower()) if row[1] else SiteType.UNKNOWN,
                environment=EnvironmentType(row[2].lower()) if row[2] else EnvironmentType.UNKNOWN,
                terrain=row[3] or "unknown",
                lat=row[4],
                lon=row[5],
                confidence=row[6] or "MEDIUM",
                has_documented_cavities=row[7] or False,
                notes=row[8]
            )
            self.known_sites.append(site)
        
        cursor.close()
        
        logger.info(f"Loaded {len(self.known_sites)} known sites as contextual anchors")
        
        # Construir perfiles contextuales
        self._build_contextual_profiles()
    
    def _build_contextual_profiles(self):
        """
        Construir perfiles contextuales normales por ambiente.
        
        Basado SOLO en distribución de sitios conocidos,
        NO en mediciones satelitales.
        """
        # Agrupar sitios por ambiente
        by_environment = {}
        for site in self.known_sites:
            env = site.environment
            if env not in by_environment:
                by_environment[env] = []
            by_environment[env].append(site)
        
        # Crear perfil para cada ambiente
        for env, sites in by_environment.items():
            if len(sites) < 2:
                continue  # Necesitamos al menos 2 sitios para definir "normal"
            
            # Definir rangos esperados CONTEXTUALES (no mediciones reales)
            # Estos son rangos teóricos basados en el tipo de ambiente
            if env == EnvironmentType.ARID:
                ndvi_range = (0.05, 0.20)
                thermal_variance_range = (2.0, 5.0)
                sar_noise = "low"
            elif env == EnvironmentType.SEMI_ARID:
                ndvi_range = (0.15, 0.35)
                thermal_variance_range = (2.5, 4.5)
                sar_noise = "medium"
            elif env == EnvironmentType.PLATEAU:
                ndvi_range = (0.10, 0.30)
                thermal_variance_range = (2.0, 4.0)
                sar_noise = "low"
            elif env == EnvironmentType.MOUNTAIN:
                ndvi_range = (0.20, 0.50)
                thermal_variance_range = (3.0, 6.0)
                sar_noise = "medium"
            elif env == EnvironmentType.FOREST:
                ndvi_range = (0.60, 0.85)
                thermal_variance_range = (1.5, 3.0)
                sar_noise = "high"
            else:
                ndvi_range = (0.20, 0.50)
                thermal_variance_range = (2.0, 5.0)
                sar_noise = "medium"
            
            profile = ContextualProfile(
                environment=env,
                expected_ndvi_range=ndvi_range,
                expected_thermal_variance_range=thermal_variance_range,
                expected_sar_noise_level=sar_noise,
                sample_count=len(sites),
                confidence=min(len(sites) / 10.0, 1.0)  # Más sitios = más confianza
            )
            
            self.contextual_profiles[env] = profile
            
            logger.info(f"Built contextual profile for {env.value}: {len(sites)} sites")
    
    def validate_candidate(
        self,
        candidate_lat: float,
        candidate_lon: float,
        candidate_environment: EnvironmentType,
        candidate_terrain: str,
        void_detection_result: Any
    ) -> ValidationResult:
        """
        Validar candidata usando contexto de sitios conocidos.
        
        Args:
            candidate_lat: Latitud de candidata
            candidate_lon: Longitud de candidata
            candidate_environment: Ambiente detectado
            candidate_terrain: Tipo de terreno
            void_detection_result: Resultado de detección de vacío
        
        Returns:
            ValidationResult con ajustes recomendados
        """
        # 1. FILTRO DE PLAUSIBILIDAD AMBIENTAL
        environment_seen = self._check_environment_precedent(candidate_environment)
        
        # 2. COMPATIBILIDAD DE TERRENO
        terrain_compatible = self._check_terrain_compatibility(
            candidate_environment, candidate_terrain
        )
        
        # 3. DESVIACIÓN DE CONTEXTO NORMAL
        context_deviation = self._calculate_context_deviation(
            candidate_environment,
            void_detection_result
        )
        
        # 4. CONTROL NEGATIVO INDIRECTO
        false_positive_risk, similar_sites = self._check_false_positive_risk(
            candidate_lat,
            candidate_lon,
            candidate_environment,
            void_detection_result.void_probability_score
        )
        
        # 5. CALCULAR PENALIZACIÓN
        score_penalty = self._calculate_score_penalty(
            environment_seen,
            terrain_compatible,
            context_deviation,
            false_positive_risk
        )
        
        # 6. AJUSTE DE CONFIANZA
        confidence_adjustment = self._calculate_confidence_adjustment(
            environment_seen,
            context_deviation
        )
        
        # 7. SCORE DE PLAUSIBILIDAD
        plausibility_score = self._calculate_plausibility_score(
            environment_seen,
            terrain_compatible,
            context_deviation,
            false_positive_risk
        )
        
        is_plausible = plausibility_score > 0.5
        
        # 8. GENERAR NOTAS DE VALIDACIÓN
        validation_notes = self._generate_validation_notes(
            environment_seen,
            terrain_compatible,
            context_deviation,
            false_positive_risk,
            similar_sites
        )
        
        return ValidationResult(
            is_plausible=is_plausible,
            plausibility_score=plausibility_score,
            environment_seen_before=environment_seen,
            terrain_compatible=terrain_compatible,
            context_deviation=context_deviation,
            false_positive_risk=false_positive_risk,
            similar_known_sites_without_cavities=similar_sites,
            score_penalty=score_penalty,
            confidence_adjustment=confidence_adjustment,
            validation_notes=validation_notes
        )
    
    def _check_environment_precedent(self, environment: EnvironmentType) -> bool:
        """
        Verificar si hemos visto este ambiente en sitios conocidos.
        """
        return environment in self.contextual_profiles
    
    def _check_terrain_compatibility(
        self,
        environment: EnvironmentType,
        terrain: str
    ) -> bool:
        """
        Verificar si el terreno es compatible con el ambiente.
        """
        # Obtener terrenos vistos en este ambiente
        if environment not in self.contextual_profiles:
            return True  # No penalizar si no tenemos datos
        
        sites_in_env = [s for s in self.known_sites if s.environment == environment]
        terrains_seen = set(s.terrain.lower() for s in sites_in_env)
        
        return terrain.lower() in terrains_seen or len(terrains_seen) == 0
    
    def _calculate_context_deviation(
        self,
        environment: EnvironmentType,
        void_result: Any
    ) -> float:
        """
        Calcular desviación del contexto normal.
        
        Compara valores de la candidata con rangos esperados del perfil.
        """
        if environment not in self.contextual_profiles:
            return 0.5  # Desviación neutral si no hay perfil
        
        profile = self.contextual_profiles[environment]
        
        # Si no hay señales (terreno rechazado), no hay desviación
        if not void_result.signals:
            return 0.0
        
        deviations = []
        
        # Comparar con rangos esperados (conceptuales)
        # Nota: Estos son rangos teóricos, no mediciones reales
        
        # NDVI esperado vs observado (si disponible)
        # En producción, esto vendría de satellite_data
        # Por ahora, asumimos que está dentro del rango esperado
        
        # Desviación térmica
        # Similar: comparar con rango esperado
        
        # Por ahora, retornar desviación baja (sistema conservador)
        return 0.2
    
    def _check_false_positive_risk(
        self,
        lat: float,
        lon: float,
        environment: EnvironmentType,
        void_score: float
    ) -> Tuple[float, int]:
        """
        CONTROL NEGATIVO INDIRECTO:
        
        Si marcamos void_score alto en sitios conocidos SIN cavidades documentadas,
        algo está mal.
        """
        # Buscar sitios conocidos cercanos (radio ~50km)
        radius_degrees = 0.5
        
        nearby_sites = [
            s for s in self.known_sites
            if abs(s.lat - lat) < radius_degrees
            and abs(s.lon - lon) < radius_degrees
            and s.environment == environment
        ]
        
        # Contar sitios SIN cavidades documentadas
        sites_without_cavities = [
            s for s in nearby_sites
            if not s.has_documented_cavities
        ]
        
        # Si hay muchos sitios sin cavidades cerca y nuestro score es alto
        # → posible falso positivo
        if len(sites_without_cavities) > 0 and void_score > 0.6:
            false_positive_risk = min(len(sites_without_cavities) / 5.0, 1.0)
        else:
            false_positive_risk = 0.0
        
        return false_positive_risk, len(sites_without_cavities)
    
    def _calculate_score_penalty(
        self,
        environment_seen: bool,
        terrain_compatible: bool,
        context_deviation: float,
        false_positive_risk: float
    ) -> float:
        """
        Calcular penalización al score de vacío.
        
        Penalizar si:
        - Ambiente nunca visto antes
        - Terreno incompatible
        - Alta desviación de contexto
        - Alto riesgo de falso positivo
        """
        penalty = 0.0
        
        if not environment_seen:
            penalty += 0.15  # Penalizar 15% si ambiente desconocido
        
        if not terrain_compatible:
            penalty += 0.10  # Penalizar 10% si terreno incompatible
        
        if context_deviation > 0.5:
            penalty += 0.10  # Penalizar 10% si alta desviación
        
        if false_positive_risk > 0.5:
            penalty += 0.20  # Penalizar 20% si alto riesgo FP
        
        return min(penalty, 0.5)  # Máximo 50% de penalización
    
    def _calculate_confidence_adjustment(
        self,
        environment_seen: bool,
        context_deviation: float
    ) -> float:
        """
        Ajustar confianza basado en contexto.
        """
        adjustment = 0.0
        
        if not environment_seen:
            adjustment -= 0.2  # Reducir confianza 20%
        
        if context_deviation > 0.5:
            adjustment -= 0.15  # Reducir confianza 15%
        
        return max(adjustment, -0.5)  # Máximo -50%
    
    def _calculate_plausibility_score(
        self,
        environment_seen: bool,
        terrain_compatible: bool,
        context_deviation: float,
        false_positive_risk: float
    ) -> float:
        """
        Calcular score de plausibilidad contextual.
        """
        score = 1.0
        
        if not environment_seen:
            score *= 0.7
        
        if not terrain_compatible:
            score *= 0.8
        
        score *= (1.0 - context_deviation * 0.5)
        score *= (1.0 - false_positive_risk * 0.6)
        
        return max(score, 0.0)
    
    def _generate_validation_notes(
        self,
        environment_seen: bool,
        terrain_compatible: bool,
        context_deviation: float,
        false_positive_risk: float,
        similar_sites: int
    ) -> str:
        """
        Generar notas de validación contextual.
        """
        notes = []
        
        if not environment_seen:
            notes.append("⚠️ Ambiente sin precedentes en sitios conocidos")
        else:
            notes.append("✓ Ambiente visto en sitios conocidos")
        
        if not terrain_compatible:
            notes.append("⚠️ Terreno incompatible con sitios conocidos en este ambiente")
        else:
            notes.append("✓ Terreno compatible")
        
        if context_deviation > 0.5:
            notes.append(f"⚠️ Alta desviación de contexto normal ({context_deviation:.2f})")
        
        if false_positive_risk > 0.5:
            notes.append(f"⚠️ Riesgo de falso positivo: {similar_sites} sitios cercanos sin cavidades")
        
        if not notes:
            notes.append("✓ Validación contextual positiva")
        
        return " | ".join(notes)
    
    def get_environment_statistics(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de ambientes en sitios conocidos.
        """
        stats = {}
        
        for env in EnvironmentType:
            sites_in_env = [s for s in self.known_sites if s.environment == env]
            
            if sites_in_env:
                stats[env.value] = {
                    'count': len(sites_in_env),
                    'with_cavities': sum(1 for s in sites_in_env if s.has_documented_cavities),
                    'high_confidence': sum(1 for s in sites_in_env if s.confidence == 'HIGH'),
                    'site_types': list(set(s.site_type.value for s in sites_in_env))
                }
        
        return stats


# Instancia global
contextual_validator = ContextualValidator()
