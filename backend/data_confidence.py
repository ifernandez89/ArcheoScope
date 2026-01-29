#!/usr/bin/env python3
"""
Data Confidence System - Transparencia científica
==================================================

Clasifica la confianza en los datos instrumentales disponibles.

CORE = 5 instrumentos esenciales:
1. Sentinel-2 NDVI (vegetación)
2. Sentinel-1 SAR (subsuperficie)
3. Landsat Thermal (térmico)
4. DEM (relieve)
5. ERA5 (clima)
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


def calculate_data_confidence(instrument_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcular confianza en datos instrumentales.
    
    Args:
        instrument_results: Lista de resultados de instrumentos
    
    Returns:
        Dict con métricas de confianza
    """
    
    # Instrumentos CORE
    core_instruments = {
        'sentinel_2_ndvi': False,
        'sentinel_1_sar': False,
        'landsat_thermal': False,
        'dem': False,  # SRTM, NASADEM, Copernicus, OpenTopography
        'era5_climate': False
    }
    
    # Moduladores opcionales
    modulators = []
    
    # Analizar resultados
    for result in instrument_results:
        instrument_name = result.get('instrument', '').lower()
        status = result.get('status', '')
        
        # Verificar CORE
        if 'sentinel_2' in instrument_name or 'ndvi' in instrument_name:
            if status in ['SUCCESS', 'DEGRADED']:
                core_instruments['sentinel_2_ndvi'] = True
        
        elif 'sentinel_1' in instrument_name or 'sar' in instrument_name:
            if status in ['SUCCESS', 'DEGRADED']:
                core_instruments['sentinel_1_sar'] = True
        
        elif 'landsat' in instrument_name or 'thermal' in instrument_name:
            if status in ['SUCCESS', 'DEGRADED']:
                core_instruments['landsat_thermal'] = True
        
        elif any(x in instrument_name for x in ['srtm', 'nasadem', 'dem', 'opentopography', 'copernicus_dem']):
            if status in ['SUCCESS', 'DEGRADED']:
                core_instruments['dem'] = True
        
        elif 'era5' in instrument_name:
            if status in ['SUCCESS', 'DEGRADED']:
                core_instruments['era5_climate'] = True
        
        # Contar moduladores
        else:
            if status in ['SUCCESS', 'DEGRADED']:
                modulators.append(instrument_name)
    
    # Calcular métricas
    core_count = sum(core_instruments.values())
    core_complete = core_count == 5
    
    # Calidad DEM
    dem_quality = "NONE"
    if core_instruments['dem']:
        # Determinar calidad según fuente (se puede mejorar)
        dem_quality = "HIGH"  # Asumimos alta si está disponible
    
    # Score de confianza
    confidence_score = (
        core_count / 5.0 * 0.8 +  # 80% peso en CORE
        min(len(modulators) / 5.0, 1.0) * 0.2  # 20% peso en moduladores
    )
    
    return {
        "core_complete": core_complete,
        "core_count": core_count,
        "core_instruments": core_instruments,
        "dem_quality": dem_quality,
        "climate_corrected": core_instruments['era5_climate'],
        "subsurface_supported": core_instruments['sentinel_1_sar'],
        "modulators_count": len(modulators),
        "modulators": modulators,
        "confidence_score": round(confidence_score, 3),
        "interpretation": _interpret_confidence(core_complete, confidence_score)
    }


def _interpret_confidence(core_complete: bool, score: float) -> str:
    """Interpretar score de confianza."""
    
    if core_complete and score >= 0.9:
        return "EXCELLENT - All core instruments available with modulators"
    elif core_complete:
        return "VERY_GOOD - All core instruments available"
    elif score >= 0.7:
        return "GOOD - Most core instruments available"
    elif score >= 0.5:
        return "MODERATE - Some core instruments missing"
    elif score >= 0.3:
        return "LIMITED - Many core instruments missing"
    else:
        return "POOR - Insufficient instrumental data"


def get_confidence_message(confidence: Dict[str, Any]) -> str:
    """
    Generar mensaje de confianza para el usuario.
    
    Frase clave: "Los datos lo permiten, no el modelo lo imagina"
    """
    
    if confidence['core_complete']:
        return (
            f"✅ High confidence detection: All core instruments available. "
            f"This candidate is strong because **the data supports it**, "
            f"not because the model imagined it."
        )
    else:
        missing = [k for k, v in confidence['core_instruments'].items() if not v]
        return (
            f"⚠️ Moderate confidence: {confidence['core_count']}/5 core instruments available. "
            f"Missing: {', '.join(missing)}. "
            f"Detection based on available data only."
        )


if __name__ == "__main__":
    # Test
    test_results = [
        {'instrument': 'sentinel_2_ndvi', 'status': 'SUCCESS'},
        {'instrument': 'sentinel_1_sar', 'status': 'SUCCESS'},
        {'instrument': 'landsat_thermal', 'status': 'SUCCESS'},
        {'instrument': 'srtm_elevation', 'status': 'SUCCESS'},
        {'instrument': 'modis_lst', 'status': 'SUCCESS'},
    ]
    
    confidence = calculate_data_confidence(test_results)
    print(confidence)
    print(get_confidence_message(confidence))
