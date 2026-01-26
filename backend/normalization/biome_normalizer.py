#!/usr/bin/env python3
"""
ArcheoScope Biome Normalizer
=============================

PROBLEMA CRÍTICO:
Un score 0.7 en hielo NO significa lo mismo que 0.7 en selva.
Cada ambiente tiene diferentes niveles de ruido, visibilidad y preservación.

SOLUCIÓN:
Normalización inter-ambiente usando:
1. Z-scores por bioma (desviación estándar)
2. Percentiles por entorno
3. Ajuste por características ambientales

FÓRMULA FINAL:
finalScore = biomeNormalizedScore * globalConfidence * environmentFactor
"""

import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class BiomeType(Enum):
    """Tipos de bioma para normalización"""
    POLAR_ICE = "polar_ice"
    GLACIER = "glacier"
    PERMAFROST = "permafrost"
    DEEP_OCEAN = "deep_ocean"
    SHALLOW_SEA = "shallow_sea"
    DESERT = "desert"
    SEMI_ARID = "semi_arid"
    FOREST = "forest"
    GRASSLAND = "grassland"
    MOUNTAIN = "mountain"
    AGRICULTURAL = "agricultural"
    UNKNOWN = "unknown"

@dataclass
class BiomeStatistics:
    """Estadísticas de un bioma específico"""
    biome_type: BiomeType
    mean_score: float
    std_dev: float
    percentile_25: float
    percentile_50: float
    percentile_75: float
    percentile_90: float
    sample_count: int
    noise_level: float  # 0.0 - 1.0
    visibility_factor: float  # 0.0 - 1.0
    preservation_factor: float  # 0.0 - 1.0

@dataclass
class NormalizedScore:
    """Score normalizado con metadata"""
    original_score: float
    normalized_score: float
    z_score: float
    percentile: float
    biome_type: BiomeType
    confidence: float
    adjustment_factor: float
    explanation: str

class BiomeNormalizer:
    """
    Normalizador de scores por bioma.
    
    FILOSOFÍA:
    - Cada bioma tiene su propia distribución de scores
    - Normalizar permite comparaciones justas entre ambientes
    - Mantener trazabilidad del score original
    """
    
    def __init__(self):
        """Inicializar con estadísticas de biomas"""
        self.biome_stats = self._initialize_biome_statistics()
        logger.info("BiomeNormalizer inicializado con estadísticas de 11 biomas")
    
    def _initialize_biome_statistics(self) -> Dict[BiomeType, BiomeStatistics]:
        """
        Inicializar estadísticas por bioma.
        
        NOTA: Estas son estadísticas iniciales basadas en conocimiento arqueológico.
        En producción, se actualizarían con datos reales de la BD.
        """
        
        stats = {}
        
        # POLAR ICE - Excelente preservación, baja visibilidad
        stats[BiomeType.POLAR_ICE] = BiomeStatistics(
            biome_type=BiomeType.POLAR_ICE,
            mean_score=0.35,  # Pocos sitios, pero bien preservados
            std_dev=0.15,
            percentile_25=0.25,
            percentile_50=0.35,
            percentile_75=0.50,
            percentile_90=0.65,
            sample_count=50,
            noise_level=0.2,  # Bajo ruido (ambiente estable)
            visibility_factor=0.4,  # Baja visibilidad (hielo cubre todo)
            preservation_factor=0.95  # Excelente preservación
        )
        
        # GLACIER - Similar a polar ice pero más accesible
        stats[BiomeType.GLACIER] = BiomeStatistics(
            biome_type=BiomeType.GLACIER,
            mean_score=0.40,
            std_dev=0.18,
            percentile_25=0.28,
            percentile_50=0.40,
            percentile_75=0.55,
            percentile_90=0.70,
            sample_count=80,
            noise_level=0.25,
            visibility_factor=0.5,
            preservation_factor=0.90
        )
        
        # DESERT - Excelente visibilidad y preservación
        stats[BiomeType.DESERT] = BiomeStatistics(
            biome_type=BiomeType.DESERT,
            mean_score=0.55,  # Muchos sitios detectables
            std_dev=0.20,
            percentile_25=0.40,
            percentile_50=0.55,
            percentile_75=0.70,
            percentile_90=0.85,
            sample_count=500,
            noise_level=0.15,  # Bajo ruido (ambiente seco)
            visibility_factor=0.95,  # Excelente visibilidad
            preservation_factor=0.90  # Excelente preservación
        )
        
        # FOREST - Baja visibilidad, preservación variable
        stats[BiomeType.FOREST] = BiomeStatistics(
            biome_type=BiomeType.FOREST,
            mean_score=0.45,
            std_dev=0.25,  # Alta variabilidad
            percentile_25=0.30,
            percentile_50=0.45,
            percentile_75=0.60,
            percentile_90=0.75,
            sample_count=300,
            noise_level=0.40,  # Alto ruido (vegetación densa)
            visibility_factor=0.30,  # Baja visibilidad (requiere LiDAR)
            preservation_factor=0.50  # Preservación pobre (humedad)
        )
        
        # SHALLOW SEA - Buena detección con sonar
        stats[BiomeType.SHALLOW_SEA] = BiomeStatistics(
            biome_type=BiomeType.SHALLOW_SEA,
            mean_score=0.50,
            std_dev=0.22,
            percentile_25=0.35,
            percentile_50=0.50,
            percentile_75=0.65,
            percentile_90=0.80,
            sample_count=200,
            noise_level=0.30,  # Ruido moderado (corrientes, sedimentos)
            visibility_factor=0.60,  # Buena con sonar
            preservation_factor=0.70  # Buena preservación
        )
        
        # DEEP OCEAN - Excelente preservación, difícil acceso
        stats[BiomeType.DEEP_OCEAN] = BiomeStatistics(
            biome_type=BiomeType.DEEP_OCEAN,
            mean_score=0.30,
            std_dev=0.12,
            percentile_25=0.22,
            percentile_50=0.30,
            percentile_75=0.40,
            percentile_90=0.50,
            sample_count=100,
            noise_level=0.15,  # Bajo ruido (ambiente estable)
            visibility_factor=0.35,  # Baja visibilidad (profundidad)
            preservation_factor=0.95  # Excelente preservación
        )
        
        # MOUNTAIN - Topografía compleja
        stats[BiomeType.MOUNTAIN] = BiomeStatistics(
            biome_type=BiomeType.MOUNTAIN,
            mean_score=0.48,
            std_dev=0.20,
            percentile_25=0.35,
            percentile_50=0.48,
            percentile_75=0.62,
            percentile_90=0.75,
            sample_count=250,
            noise_level=0.35,  # Ruido moderado-alto (topografía)
            visibility_factor=0.65,  # Buena visibilidad
            preservation_factor=0.80  # Buena preservación
        )
        
        # GRASSLAND - Buena visibilidad
        stats[BiomeType.GRASSLAND] = BiomeStatistics(
            biome_type=BiomeType.GRASSLAND,
            mean_score=0.52,
            std_dev=0.18,
            percentile_25=0.40,
            percentile_50=0.52,
            percentile_75=0.65,
            percentile_90=0.78,
            sample_count=350,
            noise_level=0.25,  # Ruido moderado
            visibility_factor=0.80,  # Buena visibilidad
            preservation_factor=0.70  # Preservación moderada
        )
        
        # AGRICULTURAL - Modificado por humanos
        stats[BiomeType.AGRICULTURAL] = BiomeStatistics(
            biome_type=BiomeType.AGRICULTURAL,
            mean_score=0.50,
            std_dev=0.22,
            percentile_25=0.38,
            percentile_50=0.50,
            percentile_75=0.63,
            percentile_90=0.75,
            sample_count=400,
            noise_level=0.45,  # Alto ruido (actividad humana)
            visibility_factor=0.70,  # Buena visibilidad
            preservation_factor=0.55  # Preservación moderada-baja
        )
        
        # SEMI_ARID - Entre desierto y grassland
        stats[BiomeType.SEMI_ARID] = BiomeStatistics(
            biome_type=BiomeType.SEMI_ARID,
            mean_score=0.53,
            std_dev=0.19,
            percentile_25=0.40,
            percentile_50=0.53,
            percentile_75=0.67,
            percentile_90=0.80,
            sample_count=280,
            noise_level=0.20,  # Bajo ruido
            visibility_factor=0.85,  # Muy buena visibilidad
            preservation_factor=0.80  # Buena preservación
        )
        
        # PERMAFROST - Tundra ártica
        stats[BiomeType.PERMAFROST] = BiomeStatistics(
            biome_type=BiomeType.PERMAFROST,
            mean_score=0.38,
            std_dev=0.16,
            percentile_25=0.28,
            percentile_50=0.38,
            percentile_75=0.50,
            percentile_90=0.62,
            sample_count=120,
            noise_level=0.25,  # Ruido moderado
            visibility_factor=0.60,  # Visibilidad moderada
            preservation_factor=0.90  # Excelente preservación
        )
        
        # UNKNOWN - Fallback conservador
        stats[BiomeType.UNKNOWN] = BiomeStatistics(
            biome_type=BiomeType.UNKNOWN,
            mean_score=0.45,
            std_dev=0.25,
            percentile_25=0.30,
            percentile_50=0.45,
            percentile_75=0.60,
            percentile_90=0.75,
            sample_count=100,
            noise_level=0.50,  # Alto ruido (desconocido)
            visibility_factor=0.50,  # Visibilidad media
            preservation_factor=0.50  # Preservación media
        )
        
        return stats
    
    def normalize_score(self, 
                       original_score: float,
                       biome_type: str,
                       global_confidence: float = 1.0,
                       context: Optional[Dict[str, Any]] = None) -> NormalizedScore:
        """
        Normalizar score por bioma.
        
        Args:
            original_score: Score original del detector (0.0 - 1.0)
            biome_type: Tipo de bioma (string)
            global_confidence: Confianza global del análisis (0.0 - 1.0)
            context: Contexto adicional
            
        Returns:
            NormalizedScore con score ajustado y metadata
        """
        
        context = context or {}
        
        # Convertir string a BiomeType
        try:
            biome_enum = BiomeType(biome_type)
        except ValueError:
            logger.warning(f"Bioma desconocido: {biome_type}, usando UNKNOWN")
            biome_enum = BiomeType.UNKNOWN
        
        # Obtener estadísticas del bioma
        stats = self.biome_stats.get(biome_enum, self.biome_stats[BiomeType.UNKNOWN])
        
        # 1. CALCULAR Z-SCORE
        z_score = (original_score - stats.mean_score) / stats.std_dev if stats.std_dev > 0 else 0.0
        
        # 2. CALCULAR PERCENTIL
        percentile = self._calculate_percentile(original_score, stats)
        
        # 3. NORMALIZAR SCORE
        # Fórmula: score normalizado = percentil ajustado por factores ambientales
        environment_factor = (
            stats.visibility_factor * 0.4 +
            stats.preservation_factor * 0.3 +
            (1.0 - stats.noise_level) * 0.3
        )
        
        # Score normalizado base
        normalized_base = percentile * environment_factor
        
        # 4. APLICAR CONFIANZA GLOBAL
        normalized_score = normalized_base * global_confidence
        
        # 5. CALCULAR FACTOR DE AJUSTE
        adjustment_factor = normalized_score / original_score if original_score > 0 else 1.0
        
        # 6. GENERAR EXPLICACIÓN
        explanation = self._generate_explanation(
            original_score, normalized_score, z_score, percentile,
            stats, environment_factor, adjustment_factor
        )
        
        logger.info(f"📊 Normalización {biome_enum.value}:")
        logger.info(f"   Original: {original_score:.3f}")
        logger.info(f"   Z-score: {z_score:.2f}")
        logger.info(f"   Percentil: {percentile:.0%}")
        logger.info(f"   Normalizado: {normalized_score:.3f}")
        logger.info(f"   Ajuste: {adjustment_factor:.2f}x")
        
        return NormalizedScore(
            original_score=original_score,
            normalized_score=normalized_score,
            z_score=z_score,
            percentile=percentile,
            biome_type=biome_enum,
            confidence=global_confidence,
            adjustment_factor=adjustment_factor,
            explanation=explanation
        )
    
    def _calculate_percentile(self, score: float, stats: BiomeStatistics) -> float:
        """
        Calcular percentil del score dentro de la distribución del bioma.
        
        Usa interpolación lineal entre percentiles conocidos.
        """
        
        if score <= stats.percentile_25:
            # Entre 0 y percentil 25
            if score <= stats.mean_score - 2 * stats.std_dev:
                return 0.0
            else:
                return 0.25 * (score / stats.percentile_25)
        
        elif score <= stats.percentile_50:
            # Entre percentil 25 y 50
            ratio = (score - stats.percentile_25) / (stats.percentile_50 - stats.percentile_25)
            return 0.25 + 0.25 * ratio
        
        elif score <= stats.percentile_75:
            # Entre percentil 50 y 75
            ratio = (score - stats.percentile_50) / (stats.percentile_75 - stats.percentile_50)
            return 0.50 + 0.25 * ratio
        
        elif score <= stats.percentile_90:
            # Entre percentil 75 y 90
            ratio = (score - stats.percentile_75) / (stats.percentile_90 - stats.percentile_75)
            return 0.75 + 0.15 * ratio
        
        else:
            # Por encima del percentil 90
            if score >= stats.mean_score + 2 * stats.std_dev:
                return 1.0
            else:
                ratio = (score - stats.percentile_90) / (stats.mean_score + 2 * stats.std_dev - stats.percentile_90)
                return 0.90 + 0.10 * ratio
    
    def _generate_explanation(self,
                            original_score: float,
                            normalized_score: float,
                            z_score: float,
                            percentile: float,
                            stats: BiomeStatistics,
                            environment_factor: float,
                            adjustment_factor: float) -> str:
        """Generar explicación de la normalización"""
        
        parts = []
        
        # Contexto del bioma
        parts.append(f"Bioma: {stats.biome_type.value}")
        parts.append(f"Score original: {original_score:.3f}")
        
        # Posición en distribución
        if z_score > 2.0:
            parts.append(f"Muy por encima de la media del bioma (z={z_score:.1f})")
        elif z_score > 1.0:
            parts.append(f"Por encima de la media del bioma (z={z_score:.1f})")
        elif z_score > -1.0:
            parts.append(f"Cerca de la media del bioma (z={z_score:.1f})")
        elif z_score > -2.0:
            parts.append(f"Por debajo de la media del bioma (z={z_score:.1f})")
        else:
            parts.append(f"Muy por debajo de la media del bioma (z={z_score:.1f})")
        
        # Percentil
        parts.append(f"Percentil {percentile:.0%} en este bioma")
        
        # Factores ambientales
        parts.append(f"Factor ambiental: {environment_factor:.2f} (visibilidad={stats.visibility_factor:.2f}, preservación={stats.preservation_factor:.2f}, ruido={stats.noise_level:.2f})")
        
        # Ajuste final
        if adjustment_factor > 1.1:
            parts.append(f"Score aumentado {adjustment_factor:.2f}x por condiciones favorables del bioma")
        elif adjustment_factor < 0.9:
            parts.append(f"Score reducido {adjustment_factor:.2f}x por condiciones desafiantes del bioma")
        else:
            parts.append(f"Score mantenido (ajuste mínimo: {adjustment_factor:.2f}x)")
        
        parts.append(f"Score normalizado final: {normalized_score:.3f}")
        
        return " | ".join(parts)
    
    def compare_across_biomes(self, 
                             scores: List[Tuple[float, str]]) -> List[Dict[str, Any]]:
        """
        Comparar scores de diferentes biomas de forma justa.
        
        Args:
            scores: Lista de (score, biome_type)
            
        Returns:
            Lista ordenada de scores normalizados con ranking
        """
        
        normalized_results = []
        
        for score, biome_type in scores:
            normalized = self.normalize_score(score, biome_type)
            normalized_results.append({
                'original_score': score,
                'normalized_score': normalized.normalized_score,
                'biome_type': biome_type,
                'percentile': normalized.percentile,
                'z_score': normalized.z_score,
                'adjustment_factor': normalized.adjustment_factor
            })
        
        # Ordenar por score normalizado
        normalized_results.sort(key=lambda x: x['normalized_score'], reverse=True)
        
        # Agregar ranking
        for i, result in enumerate(normalized_results, 1):
            result['rank'] = i
        
        return normalized_results
    
    def update_biome_statistics(self, 
                               biome_type: str,
                               new_scores: List[float]) -> None:
        """
        Actualizar estadísticas de un bioma con nuevos datos.
        
        IMPORTANTE: En producción, esto se llamaría periódicamente
        con datos reales de la BD para mantener estadísticas actualizadas.
        """
        
        try:
            biome_enum = BiomeType(biome_type)
        except ValueError:
            logger.warning(f"Bioma desconocido: {biome_type}")
            return
        
        if not new_scores:
            return
        
        # Calcular nuevas estadísticas
        mean_score = np.mean(new_scores)
        std_dev = np.std(new_scores)
        percentile_25 = np.percentile(new_scores, 25)
        percentile_50 = np.percentile(new_scores, 50)
        percentile_75 = np.percentile(new_scores, 75)
        percentile_90 = np.percentile(new_scores, 90)
        
        # Obtener estadísticas actuales
        current_stats = self.biome_stats[biome_enum]
        
        # Actualizar con promedio ponderado (70% histórico, 30% nuevo)
        updated_stats = BiomeStatistics(
            biome_type=biome_enum,
            mean_score=current_stats.mean_score * 0.7 + mean_score * 0.3,
            std_dev=current_stats.std_dev * 0.7 + std_dev * 0.3,
            percentile_25=current_stats.percentile_25 * 0.7 + percentile_25 * 0.3,
            percentile_50=current_stats.percentile_50 * 0.7 + percentile_50 * 0.3,
            percentile_75=current_stats.percentile_75 * 0.7 + percentile_75 * 0.3,
            percentile_90=current_stats.percentile_90 * 0.7 + percentile_90 * 0.3,
            sample_count=current_stats.sample_count + len(new_scores),
            noise_level=current_stats.noise_level,  # Mantener constante
            visibility_factor=current_stats.visibility_factor,  # Mantener constante
            preservation_factor=current_stats.preservation_factor  # Mantener constante
        )
        
        self.biome_stats[biome_enum] = updated_stats
        
        logger.info(f"✅ Estadísticas actualizadas para {biome_type}:")
        logger.info(f"   Muestras: {current_stats.sample_count} → {updated_stats.sample_count}")
        logger.info(f"   Media: {current_stats.mean_score:.3f} → {updated_stats.mean_score:.3f}")
        logger.info(f"   Std Dev: {current_stats.std_dev:.3f} → {updated_stats.std_dev:.3f}")
    
    def get_biome_statistics(self, biome_type: str) -> Optional[BiomeStatistics]:
        """Obtener estadísticas de un bioma específico"""
        try:
            biome_enum = BiomeType(biome_type)
            return self.biome_stats.get(biome_enum)
        except ValueError:
            return None
    
    def get_all_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Obtener todas las estadísticas de biomas"""
        return {
            biome.value: {
                'mean_score': stats.mean_score,
                'std_dev': stats.std_dev,
                'percentile_50': stats.percentile_50,
                'sample_count': stats.sample_count,
                'noise_level': stats.noise_level,
                'visibility_factor': stats.visibility_factor,
                'preservation_factor': stats.preservation_factor
            }
            for biome, stats in self.biome_stats.items()
        }
