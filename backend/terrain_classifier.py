#!/usr/bin/env python3
"""
ArcheoScope - Terrain Classifier
Clasificación robusta de terreno usando features físicas + ML

Enfoque de 2 capas:
1. Reglas duras (clasificación física obvia)
2. Random Forest (casos ambiguos)
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TerrainType(Enum):
    """Tipos de terreno clasificados"""
    WATER = 0           # Agua (océanos, lagos, ríos)
    DESERT = 1          # Desierto árido
    VEGETATION = 2      # Vegetación (bosques, praderas)
    MOUNTAIN = 3        # Montaña (alta elevación, pendiente)
    ICE_SNOW = 4        # Hielo/Nieve (glaciares, polar)
    WETLAND = 5         # Humedal (pantanos, manglares)
    ANCIENT_URBAN = 6   # Urbano antiguo
    UNKNOWN = 7         # No clasificado


@dataclass
class TerrainFeatures:
    """Features físicas para clasificación de terreno"""
    
    # Vegetación
    ndvi_mean: float        # Normalized Difference Vegetation Index
    ndvi_std: float         # Desviación estándar NDVI
    
    # Agua
    ndwi_mean: float        # Normalized Difference Water Index
    
    # Nieve/Hielo
    ndsi_mean: float        # Normalized Difference Snow Index
    
    # Temperatura
    lst_mean: float         # Land Surface Temperature (°C)
    
    # Topografía
    elevation_mean: float   # Elevación (m)
    slope_mean: float       # Pendiente (grados)
    
    # SAR
    sar_backscatter: float  # Backscatter SAR (dB)
    
    # Clima
    precipitation_mean: float  # Precipitación anual (mm)
    
    # Rugosidad
    roughness: float        # Rugosidad del terreno


@dataclass
class TerrainClassification:
    """Resultado de clasificación de terreno"""
    
    terrain_type: TerrainType
    confidence: float
    probabilities: Dict[str, float]
    method: str  # "hard_rules" o "ml_classifier"
    features_used: Dict[str, float]


class TerrainClassifier:
    """
    Clasificador robusto de terreno usando enfoque de 2 capas
    
    Capa 1: Reglas duras (casos obvios)
    Capa 2: Random Forest (casos ambiguos)
    """
    
    def __init__(self):
        self.model = None
        self.feature_names = [
            'ndvi_mean', 'ndvi_std', 'ndwi_mean', 'ndsi_mean',
            'lst_mean', 'elevation_mean', 'slope_mean',
            'sar_backscatter', 'precipitation_mean', 'roughness'
        ]
        
        logger.info("TerrainClassifier inicializado")
    
    def classify_with_hard_rules(
        self,
        features: TerrainFeatures
    ) -> Optional[TerrainClassification]:
        """
        Capa 1: Clasificación usando reglas duras (casos obvios)
        
        Retorna None si no es obvio (pasa a ML)
        """
        
        # REGLA 1: Agua (NDWI alto)
        if features.ndwi_mean > 0.4:
            return TerrainClassification(
                terrain_type=TerrainType.WATER,
                confidence=0.95,
                probabilities={'water': 0.95, 'wetland': 0.05},
                method='hard_rules',
                features_used={'ndwi_mean': features.ndwi_mean}
            )
        
        # REGLA 2: Hielo/Nieve (NDSI alto)
        if features.ndsi_mean > 0.4:
            return TerrainClassification(
                terrain_type=TerrainType.ICE_SNOW,
                confidence=0.95,
                probabilities={'ice_snow': 0.95, 'mountain': 0.05},
                method='hard_rules',
                features_used={'ndsi_mean': features.ndsi_mean}
            )
        
        # REGLA 3: Desierto (NDVI bajo + precipitación baja)
        if features.ndvi_mean < 0.1 and features.precipitation_mean < 200:
            return TerrainClassification(
                terrain_type=TerrainType.DESERT,
                confidence=0.90,
                probabilities={'desert': 0.90, 'mountain': 0.10},
                method='hard_rules',
                features_used={
                    'ndvi_mean': features.ndvi_mean,
                    'precipitation_mean': features.precipitation_mean
                }
            )
        
        # REGLA 4: Montaña alta (elevación > 3000m + pendiente alta)
        if features.elevation_mean > 3000 and features.slope_mean > 15:
            return TerrainClassification(
                terrain_type=TerrainType.MOUNTAIN,
                confidence=0.85,
                probabilities={'mountain': 0.85, 'ice_snow': 0.15},
                method='hard_rules',
                features_used={
                    'elevation_mean': features.elevation_mean,
                    'slope_mean': features.slope_mean
                }
            )
        
        # REGLA 5: Humedal (NDWI moderado + NDVI moderado)
        if 0.2 < features.ndwi_mean < 0.4 and features.ndvi_mean > 0.3:
            return TerrainClassification(
                terrain_type=TerrainType.WETLAND,
                confidence=0.80,
                probabilities={'wetland': 0.80, 'vegetation': 0.20},
                method='hard_rules',
                features_used={
                    'ndwi_mean': features.ndwi_mean,
                    'ndvi_mean': features.ndvi_mean
                }
            )
        
        # No es obvio → pasar a ML
        return None
    
    def classify_with_ml(
        self,
        features: TerrainFeatures
    ) -> TerrainClassification:
        """
        Capa 2: Clasificación usando Random Forest (casos ambiguos)
        
        Si no hay modelo entrenado, usa heurísticas mejoradas
        """
        
        if self.model is None:
            # Fallback: heurísticas mejoradas
            return self._classify_with_heuristics(features)
        
        # TODO: Implementar clasificación con modelo entrenado
        # feature_vector = self._extract_feature_vector(features)
        # probabilities = self.model.predict_proba([feature_vector])[0]
        # terrain_type = TerrainType(np.argmax(probabilities))
        
        return self._classify_with_heuristics(features)
    
    def _classify_with_heuristics(
        self,
        features: TerrainFeatures
    ) -> TerrainClassification:
        """Heurísticas mejoradas para casos ambiguos"""
        
        # Calcular scores para cada tipo de terreno
        scores = {}
        
        # Score VEGETACIÓN
        veg_score = 0.0
        if features.ndvi_mean > 0.3:
            veg_score += 0.4
        if features.precipitation_mean > 500:
            veg_score += 0.3
        if features.lst_mean > 10 and features.lst_mean < 30:
            veg_score += 0.3
        scores['vegetation'] = veg_score
        
        # Score DESIERTO
        desert_score = 0.0
        if features.ndvi_mean < 0.2:
            desert_score += 0.4
        if features.precipitation_mean < 300:
            desert_score += 0.4
        if features.lst_mean > 25:
            desert_score += 0.2
        scores['desert'] = desert_score
        
        # Score MONTAÑA
        mountain_score = 0.0
        if features.elevation_mean > 1500:
            mountain_score += 0.4
        if features.slope_mean > 10:
            mountain_score += 0.3
        if features.roughness > 50:
            mountain_score += 0.3
        scores['mountain'] = mountain_score
        
        # Score HUMEDAL
        wetland_score = 0.0
        if 0.1 < features.ndwi_mean < 0.3:
            wetland_score += 0.4
        if features.ndvi_mean > 0.2:
            wetland_score += 0.3
        if features.precipitation_mean > 800:
            wetland_score += 0.3
        scores['wetland'] = wetland_score
        
        # Normalizar scores a probabilidades
        total = sum(scores.values())
        if total > 0:
            probabilities = {k: v/total for k, v in scores.items()}
        else:
            probabilities = {'unknown': 1.0}
        
        # Seleccionar tipo con mayor probabilidad
        if probabilities:
            best_type = max(probabilities.items(), key=lambda x: x[1])
            terrain_map = {
                'vegetation': TerrainType.VEGETATION,
                'desert': TerrainType.DESERT,
                'mountain': TerrainType.MOUNTAIN,
                'wetland': TerrainType.WETLAND,
                'unknown': TerrainType.UNKNOWN
            }
            
            return TerrainClassification(
                terrain_type=terrain_map.get(best_type[0], TerrainType.UNKNOWN),
                confidence=best_type[1],
                probabilities=probabilities,
                method='ml_heuristics',
                features_used=self._get_features_dict(features)
            )
        
        return TerrainClassification(
            terrain_type=TerrainType.UNKNOWN,
            confidence=0.0,
            probabilities={'unknown': 1.0},
            method='fallback',
            features_used={}
        )
    
    def classify(
        self,
        features: TerrainFeatures
    ) -> TerrainClassification:
        """
        Clasificar terreno usando enfoque de 2 capas
        
        1. Intentar reglas duras (casos obvios)
        2. Si no es obvio, usar ML
        """
        
        # Capa 1: Reglas duras
        hard_result = self.classify_with_hard_rules(features)
        if hard_result is not None:
            logger.debug(f"Clasificado con reglas duras: {hard_result.terrain_type.name}")
            return hard_result
        
        # Capa 2: ML
        ml_result = self.classify_with_ml(features)
        logger.debug(f"Clasificado con ML: {ml_result.terrain_type.name}")
        return ml_result
    
    def _get_features_dict(self, features: TerrainFeatures) -> Dict[str, float]:
        """Convertir features a diccionario"""
        return {
            'ndvi_mean': features.ndvi_mean,
            'ndvi_std': features.ndvi_std,
            'ndwi_mean': features.ndwi_mean,
            'ndsi_mean': features.ndsi_mean,
            'lst_mean': features.lst_mean,
            'elevation_mean': features.elevation_mean,
            'slope_mean': features.slope_mean,
            'sar_backscatter': features.sar_backscatter,
            'precipitation_mean': features.precipitation_mean,
            'roughness': features.roughness
        }
    
    def classify_from_coordinates(
        self,
        latitude: float,
        longitude: float
    ) -> TerrainClassification:
        """
        Clasificar terreno desde coordenadas
        
        Extrae features de APIs públicas y clasifica
        """
        
        # TODO: Implementar extracción de features desde APIs
        # Por ahora, usar features sintéticas basadas en coordenadas
        
        features = self._extract_features_from_coordinates(latitude, longitude)
        return self.classify(features)
    
    def _extract_features_from_coordinates(
        self,
        latitude: float,
        longitude: float
    ) -> TerrainFeatures:
        """
        Extraer features físicas desde coordenadas
        
        Usa heurísticas geográficas simples
        TODO: Reemplazar con APIs reales (Sentinel, MODIS, SRTM)
        """
        
        # Heurísticas simples basadas en geografía
        
        # Elevación aproximada (muy simplificado)
        # Montañas: Andes, Himalaya, Alpes, Rockies
        elevation = 100.0
        if abs(latitude) > 30 and abs(latitude) < 50:
            elevation = 500.0  # Zonas montañosas templadas
        
        # NDVI aproximado por latitud
        ndvi = 0.5  # Default: vegetación moderada
        if abs(latitude) > 60:
            ndvi = 0.1  # Polar: poca vegetación
        elif abs(latitude) < 30:
            if abs(longitude) > 10 and abs(longitude) < 50:
                ndvi = 0.05  # Desiertos (Sahara, Arabia)
            else:
                ndvi = 0.7  # Tropical: alta vegetación
        
        # Temperatura aproximada por latitud
        lst = 20.0 - abs(latitude) * 0.5
        
        # Precipitación aproximada
        precipitation = 800.0
        if abs(latitude) > 60:
            precipitation = 300.0  # Polar: baja precipitación
        elif abs(latitude) < 30:
            if abs(longitude) > 10 and abs(longitude) < 50:
                precipitation = 50.0  # Desiertos
            else:
                precipitation = 2000.0  # Tropical
        
        return TerrainFeatures(
            ndvi_mean=ndvi,
            ndvi_std=0.1,
            ndwi_mean=0.0,
            ndsi_mean=0.1 if abs(latitude) > 60 else 0.0,
            lst_mean=lst,
            elevation_mean=elevation,
            slope_mean=5.0,
            sar_backscatter=-10.0,
            precipitation_mean=precipitation,
            roughness=30.0
        )


# Instancia global
terrain_classifier = TerrainClassifier()
