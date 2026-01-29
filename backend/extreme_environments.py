#!/usr/bin/env python3
"""
Extreme Environments Configuration - SALTO EVOLUTIVO 3
======================================================

Configuración de ambientes extremos donde ArcheoScope brilla.

CONCEPTO CLAVE:
- No ir "a lo extremo" al azar
- Ir donde el sistema brilla naturalmente
- Ambientes con alta relación señal/ruido

AMBIENTES IDEALES:
1. Desiertos hiperáridos (NDVI ≈ 0 → cualquier señal resalta)
2. Sabkhas/Salares (contraste térmico brutal)
3. Tells urbanos (estratigrafía humana pura)
4. Paleocauces fósiles (memoria hídrica profunda)
5. Oasis antiguos (vegetación artificial histórica)
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ExtremeEnvironmentType(Enum):
    """Tipos de ambientes extremos."""
    HYPERARID_DESERT = "hyperarid_desert"
    SABKHA_SALT_FLAT = "sabkha_salt_flat"
    URBAN_TELL = "urban_tell"
    FOSSIL_PALEOCHANNEL = "fossil_paleochannel"
    ANCIENT_OASIS = "ancient_oasis"
    COASTAL_LAGOON = "coastal_lagoon"
    MOUNTAIN_PLATEAU = "mountain_plateau"


@dataclass
class ExtremeEnvironmentConfig:
    """Configuración de ambiente extremo."""
    
    name: str
    env_type: ExtremeEnvironmentType
    center_lat: float
    center_lon: float
    radius_km: float
    
    # Características del ambiente
    expected_ess_range: Tuple[float, float]  # (min, max)
    optimal_sensors: List[str]
    archaeological_context: str
    
    # Justificación científica
    why_extreme: str
    expected_signals: List[str]
    
    def to_dict(self) -> Dict:
        """Convertir a diccionario."""
        return {
            "name": self.name,
            "type": self.env_type.value,
            "center": {"lat": self.center_lat, "lon": self.center_lon},
            "radius_km": self.radius_km,
            "expected_ess_range": self.expected_ess_range,
            "optimal_sensors": self.optimal_sensors,
            "archaeological_context": self.archaeological_context,
            "why_extreme": self.why_extreme,
            "expected_signals": self.expected_signals
        }


# ============================================================================
# CATÁLOGO DE AMBIENTES EXTREMOS
# ============================================================================

EXTREME_ENVIRONMENTS = {
    
    # 1. ATACAMA INTERIOR (Chile)
    "atacama_interior": ExtremeEnvironmentConfig(
        name="Atacama Interior",
        env_type=ExtremeEnvironmentType.HYPERARID_DESERT,
        center_lat=-23.5,
        center_lon=-68.2,
        radius_km=10.0,
        expected_ess_range=(0.65, 0.75),
        optimal_sensors=["sentinel_2_ndvi", "landsat_thermal", "sentinel_1_sar"],
        archaeological_context="Desierto más árido del mundo. Geoglifos, estructuras prehispánicas.",
        why_extreme="NDVI ≈ 0 → cualquier señal vegetal resalta brutalmente",
        expected_signals=[
            "Contraste NDVI extremo (cualquier vegetación = anómalo)",
            "Estabilidad térmica perfecta (sin vegetación = señal pura)",
            "SAR penetra sin interferencia atmosférica"
        ]
    ),
    
    # 2. MESOPOTAMIA - TELLS URBANOS (Irak)
    "mesopotamia_tells": ExtremeEnvironmentConfig(
        name="Mesopotamia - Tells Urbanos",
        env_type=ExtremeEnvironmentType.URBAN_TELL,
        center_lat=33.3,
        center_lon=44.4,
        radius_km=15.0,
        expected_ess_range=(0.70, 0.80),
        optimal_sensors=["srtm_elevation", "landsat_thermal", "sentinel_1_sar"],
        archaeological_context="Tells milenarios (Ur, Uruk, Babilonia). Estratigrafía urbana pura.",
        why_extreme="Estratigrafía humana pura (10-20m de ocupación continua)",
        expected_signals=[
            "Elevación anómala (tells = montículos artificiales)",
            "Inercia térmica extrema (ladrillos de barro)",
            "Contraste estratigráfico brutal (capas de ocupación)"
        ]
    ),
    
    # 3. DELTA DEL INDO - PALEOCAUCES (Pakistán)
    "indus_delta_paleochannels": ExtremeEnvironmentConfig(
        name="Delta del Indo - Paleocauces",
        env_type=ExtremeEnvironmentType.FOSSIL_PALEOCHANNEL,
        center_lat=26.0,
        center_lon=68.5,
        radius_km=20.0,
        expected_ess_range=(0.65, 0.75),
        optimal_sensors=["sentinel_1_sar", "landsat_thermal", "srtm_elevation"],
        archaeological_context="Civilización del Indo (Mohenjo-Daro, Harappa). Paleocauces del Sarasvati.",
        why_extreme="Paleocauces fósiles + tells = memoria hídrica + urbana",
        expected_signals=[
            "SAR detecta paleocauces enterrados",
            "Humedad subsuperficial residual",
            "Micro-topografía de canales antiguos"
        ]
    ),
    
    # 4. SAHARA CENTRAL - PALEOLAGO (Argelia)
    "sahara_central_paleolake": ExtremeEnvironmentConfig(
        name="Sahara Central - Paleolago",
        env_type=ExtremeEnvironmentType.FOSSIL_PALEOCHANNEL,
        center_lat=26.0,
        center_lon=3.0,
        radius_km=25.0,
        expected_ess_range=(0.60, 0.70),
        optimal_sensors=["sentinel_2_ndvi", "landsat_thermal", "sentinel_1_sar"],
        archaeological_context="Paleolago del Holoceno. Arte rupestre, asentamientos neolíticos.",
        why_extreme="Paleolago + arte rupestre = memoria hídrica + cultural",
        expected_signals=[
            "Sedimentos lacustres fósiles",
            "Vegetación residual en paleocosta",
            "Estructuras de piedra (contraste brutal en desierto)"
        ]
    ),
    
    # 5. CUENCA DEL TARIM - OASIS ANTIGUOS (China)
    "tarim_basin_oases": ExtremeEnvironmentConfig(
        name="Cuenca del Tarim - Oasis Antiguos",
        env_type=ExtremeEnvironmentType.ANCIENT_OASIS,
        center_lat=40.0,
        center_lon=85.0,
        radius_km=15.0,
        expected_ess_range=(0.65, 0.75),
        optimal_sensors=["sentinel_2_ndvi", "landsat_thermal", "sentinel_1_sar"],
        archaeological_context="Ruta de la Seda. Oasis antiguos (Loulan, Niya). Ciudades enterradas.",
        why_extreme="Oasis antiguos = vegetación artificial histórica",
        expected_signals=[
            "NDVI anómalo (vegetación artificial vs desierto)",
            "Sistemas de irrigación enterrados",
            "Estructuras de adobe (inercia térmica)"
        ]
    ),
    
    # 6. SABKHA DE RUB AL KHALI (Arabia Saudita)
    "rub_al_khali_sabkha": ExtremeEnvironmentConfig(
        name="Sabkha de Rub al Khali",
        env_type=ExtremeEnvironmentType.SABKHA_SALT_FLAT,
        center_lat=20.0,
        center_lon=50.0,
        radius_km=10.0,
        expected_ess_range=(0.60, 0.70),
        optimal_sensors=["landsat_thermal", "sentinel_1_sar", "sentinel_2_ndvi"],
        archaeological_context="Desierto del Cuarto Vacío. Rutas caravaneras antiguas.",
        why_extreme="Sabkha = contraste térmico brutal (sal vs arena)",
        expected_signals=[
            "Contraste térmico día/noche extremo",
            "SAR penetra sal (detecta estructuras enterradas)",
            "Rutas antiguas (compactación del suelo)"
        ]
    ),
    
    # 7. ALTIPLANO ANDINO (Bolivia/Perú)
    "andean_altiplano": ExtremeEnvironmentConfig(
        name="Altiplano Andino",
        env_type=ExtremeEnvironmentType.MOUNTAIN_PLATEAU,
        center_lat=-16.5,
        center_lon=-68.7,
        radius_km=20.0,
        expected_ess_range=(0.55, 0.65),
        optimal_sensors=["srtm_elevation", "sentinel_2_ndvi", "landsat_thermal"],
        archaeological_context="Tiwanaku, Pucará. Terrazas agrícolas, sistemas hidráulicos.",
        why_extreme="Altitud extrema = preservación perfecta + señal clara",
        expected_signals=[
            "Terrazas agrícolas (micro-topografía)",
            "Sistemas hidráulicos (humedad residual)",
            "Estructuras de piedra (contraste térmico)"
        ]
    ),
    
    # 8. LAGUNA COSTERA COLMATADA (Veracruz, México)
    "veracruz_coastal_lagoon": ExtremeEnvironmentConfig(
        name="Laguna Costera Colmatada",
        env_type=ExtremeEnvironmentType.COASTAL_LAGOON,
        center_lat=20.58,
        center_lon=-96.92,
        radius_km=10.0,
        expected_ess_range=(0.45, 0.55),
        optimal_sensors=["sentinel_1_sar", "landsat_thermal", "sentinel_2_ndvi"],
        archaeological_context="Zona de transición tierra-agua. Asentamientos costeros prehispánicos.",
        why_extreme="Transición agua/tierra = contraste estratigráfico natural",
        expected_signals=[
            "Contraste NDVI agua/tierra",
            "SAR detecta humedad subsuperficial",
            "Sedimentos colmatados (estratigrafía)"
        ]
    )
}


def get_environment_config(env_name: str) -> ExtremeEnvironmentConfig:
    """Obtener configuración de ambiente extremo."""
    if env_name not in EXTREME_ENVIRONMENTS:
        raise ValueError(f"Ambiente '{env_name}' no encontrado. Disponibles: {list(EXTREME_ENVIRONMENTS.keys())}")
    return EXTREME_ENVIRONMENTS[env_name]


def list_extreme_environments() -> List[str]:
    """Listar ambientes extremos disponibles."""
    return list(EXTREME_ENVIRONMENTS.keys())


def get_optimal_environment_for_ess(target_ess: float) -> List[str]:
    """
    Obtener ambientes óptimos para un ESS objetivo.
    
    Args:
        target_ess: ESS objetivo (0-1)
        
    Returns:
        Lista de nombres de ambientes que pueden alcanzar ese ESS
    """
    suitable = []
    for name, config in EXTREME_ENVIRONMENTS.items():
        min_ess, max_ess = config.expected_ess_range
        if min_ess <= target_ess <= max_ess:
            suitable.append(name)
    return suitable


def print_environment_catalog():
    """Imprimir catálogo de ambientes extremos."""
    print("="*80)
    print("🌍 CATÁLOGO DE AMBIENTES EXTREMOS - ArcheoScope")
    print("="*80)
    print()
    
    for name, config in EXTREME_ENVIRONMENTS.items():
        print(f"📍 {config.name}")
        print(f"   Tipo: {config.env_type.value}")
        print(f"   Coordenadas: {config.center_lat:.2f}, {config.center_lon:.2f}")
        print(f"   ESS Esperado: {config.expected_ess_range[0]:.2f}-{config.expected_ess_range[1]:.2f}")
        print(f"   Por qué extremo: {config.why_extreme}")
        print()


if __name__ == "__main__":
    print_environment_catalog()
