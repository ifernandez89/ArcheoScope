#!/usr/bin/env python3
"""
Test del Sistema de Detección de Geoglifos
==========================================

Prueba las capacidades del detector de geoglifos en diferentes modos.
"""

import sys
from pathlib import Path
import numpy as np

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from geoglyph_detector import (
    GeoglyphDetector,
    DetectionMode,
    get_promising_zones
)


def test_scientific_mode():
    """Test en modo científico"""
    print("\n" + "="*70)
    print("🧪 TEST: Modo Científico")
    print("="*70)
    
    detector = GeoglyphDetector(mode=DetectionMode.SCIENTIFIC)
    
    # Coordenadas de ejemplo (Arabia)
    lat, lon = 26.5, 38.5
    bbox = (26.4, 26.6, 38.4, 38.6)
    
    # DEM simulado
    dem_data = np.random.rand(100, 100) * 100  # Elevación 0-100m
    
    result = detector.detect_geoglyph(
        lat=lat,
        lon=lon,
        lat_min=bbox[0],
        lat_max=bbox[1],
        lon_min=bbox[2],
        lon_max=bbox[3],
        dem_data=dem_data,
        resolution_m=0.5
    )
    
    print(f"\n📋 Resultado:")
    print(f"   ID: {result.candidate_id}")
    print(f"   Tipo: {result.geoglyph_type.value}")
    print(f"   Confianza tipo: {result.type_confidence:.2f}")
    print(f"\n📊 Scores:")
    print(f"   Cultural: {result.cultural_score:.3f}")
    print(f"   Forma: {result.form_score:.3f}")
    print(f"   Orientación: {result.orientation_score:.3f}")
    print(f"   Contexto: {result.context_score:.3f}")
    print(f"   Hidrología: {result.hydrology_score:.3f}")
    
    print(f"\n📐 Orientación:")
    print(f"   Azimut: {result.orientation.azimuth_deg:.1f}°")
    print(f"   Eje mayor: {result.orientation.major_axis_length_m:.1f}m")
    print(f"   Eje menor: {result.orientation.minor_axis_length_m:.1f}m")
    print(f"   Aspect ratio: {result.orientation.aspect_ratio:.2f}")
    print(f"   Simetría: {(1-result.orientation.bilateral_symmetry)*100:.0f}%")
    print(f"   NW-SE: {'✓' if result.orientation.is_nw_se else '✗'}")
    print(f"   E-W: {'✓' if result.orientation.is_e_w else '✗'}")
    
    print(f"\n🌋 Contexto Volcánico:")
    if result.volcanic_context:
        print(f"   Dist. basalto: {result.volcanic_context.distance_to_basalt_flow_km:.1f}km")
        print(f"   Superficie estable: {'✓' if result.volcanic_context.on_stable_surface else '✗'}")
        print(f"   Colada joven: {'✗' if not result.volcanic_context.on_young_flow else '✓ (MALO)'}")
    
    print(f"\n💧 Paleohidrología:")
    if result.paleo_hydrology:
        print(f"   Dist. wadi: {result.paleo_hydrology.distance_to_wadi_km:.1f}km")
        print(f"   Transición sedimento: {'✓ ORO' if result.paleo_hydrology.on_sediment_transition else '✗'}")
        print(f"   Prob. agua estacional: {result.paleo_hydrology.seasonal_water_probability*100:.0f}%")
    
    print(f"\n☀️ Alineaciones Astronómicas:")
    if result.celestial_alignment:
        print(f"   Mejor alineación: {result.celestial_alignment.best_solar_alignment}")
        print(f"   Solsticio verano: {result.celestial_alignment.summer_solstice_alignment*100:.0f}%")
        print(f"   Solsticio invierno: {result.celestial_alignment.winter_solstice_alignment*100:.0f}%")
        print(f"   Equinoccio: {result.celestial_alignment.equinox_alignment*100:.0f}%")
    
    print(f"\n✅ Validación:")
    print(f"   Necesita validación: {'SÍ' if result.needs_validation else 'NO'}")
    print(f"   Prioridad: {result.validation_priority.upper()}")
    print(f"   Resolución recomendada: {result.recommended_resolution_m}m/pixel")
    print(f"   Paper-level: {'🏆 SÍ' if result.paper_level_discovery else 'No'}")
    
    print(f"\n📝 Razonamiento:")
    for reason in result.detection_reasoning:
        print(f"   • {reason}")
    
    print(f"\n⚠️ Riesgos de Falso Positivo:")
    for risk in result.false_positive_risks:
        print(f"   • {risk}")
    
    return result


def test_explorer_mode():
    """Test en modo explorador"""
    print("\n" + "="*70)
    print("🧭 TEST: Modo Explorador")
    print("="*70)
    
    detector = GeoglyphDetector(mode=DetectionMode.EXPLORER)
    
    lat, lon = 29.5, 37.5  # Límite Arabia-Jordania
    bbox = (29.4, 29.6, 37.4, 37.6)
    
    result = detector.detect_geoglyph(
        lat=lat,
        lon=lon,
        lat_min=bbox[0],
        lat_max=bbox[1],
        lon_min=bbox[2],
        lon_max=bbox[3],
        resolution_m=2.0  # Resolución más baja
    )
    
    print(f"\n📋 Resultado:")
    print(f"   Modo: {result.detection_mode.value}")
    print(f"   Cultural Score: {result.cultural_score:.3f}")
    print(f"   Prioridad: {result.validation_priority.upper()}")
    
    return result


def test_cognitive_mode():
    """Test en modo cognitivo"""
    print("\n" + "="*70)
    print("🧠 TEST: Modo Cognitivo")
    print("="*70)
    
    detector = GeoglyphDetector(mode=DetectionMode.COGNITIVE)
    
    lat, lon = 20.0, 51.0  # Bordes Rub' al Khali
    bbox = (19.9, 20.1, 50.9, 51.1)
    
    result = detector.detect_geoglyph(
        lat=lat,
        lon=lon,
        lat_min=bbox[0],
        lat_max=bbox[1],
        lon_min=bbox[2],
        lon_max=bbox[3],
        resolution_m=5.0  # Resolución baja
    )
    
    print(f"\n📋 Resultado:")
    print(f"   Modo: {result.detection_mode.value}")
    print(f"   Cultural Score: {result.cultural_score:.3f}")
    print(f"   Filosofía: Solo señalar, NO afirmar")
    
    return result


def test_promising_zones():
    """Test de zonas prometedoras"""
    print("\n" + "="*70)
    print("🗺️ TEST: Zonas Prometedoras")
    print("="*70)
    
    zones = get_promising_zones()
    
    print(f"\n📍 Total de zonas: {len(zones)}\n")
    
    for zone_id, zone_info in zones.items():
        print(f"🔍 {zone_info['name']}")
        print(f"   ID: {zone_id}")
        print(f"   Bbox: {zone_info['bbox']}")
        print(f"   Prioridad: {zone_info['priority'].upper()}")
        print(f"   Razón: {zone_info['reason']}")
        print()


def test_comparison():
    """Comparar los 3 modos"""
    print("\n" + "="*70)
    print("📊 COMPARACIÓN DE MODOS")
    print("="*70)
    
    lat, lon = 26.5, 38.5
    bbox = (26.4, 26.6, 38.4, 38.6)
    dem_data = np.random.rand(100, 100) * 100
    
    modes = [
        (DetectionMode.SCIENTIFIC, "Científico"),
        (DetectionMode.EXPLORER, "Explorador"),
        (DetectionMode.COGNITIVE, "Cognitivo")
    ]
    
    results = []
    
    for mode, name in modes:
        detector = GeoglyphDetector(mode=mode)
        result = detector.detect_geoglyph(
            lat=lat, lon=lon,
            lat_min=bbox[0], lat_max=bbox[1],
            lon_min=bbox[2], lon_max=bbox[3],
            dem_data=dem_data,
            resolution_m=1.0
        )
        results.append((name, result))
    
    print("\n| Modo | Cultural Score | Prioridad | Paper-Level |")
    print("|------|---------------|-----------|-------------|")
    
    for name, result in results:
        paper = "🏆 SÍ" if result.paper_level_discovery else "No"
        print(f"| {name:12} | {result.cultural_score:.3f} | {result.validation_priority:8} | {paper:11} |")


def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("🔍 SISTEMA DE DETECCIÓN DE GEOGLIFOS - TESTS")
    print("="*70)
    
    try:
        # Test individual de cada modo
        test_scientific_mode()
        test_explorer_mode()
        test_cognitive_mode()
        
        # Test de zonas
        test_promising_zones()
        
        # Comparación
        test_comparison()
        
        print("\n" + "="*70)
        print("✅ TODOS LOS TESTS COMPLETADOS")
        print("="*70)
        print("\n💡 Próximos pasos:")
        print("   1. Levantar backend: python backend/api/main.py")
        print("   2. Probar API: http://localhost:8003/docs")
        print("   3. Ver endpoints en /geoglyph/*")
        print("   4. Revisar GEOGLYPH_DETECTION_GUIDE.md")
        print()
        
    except Exception as e:
        print(f"\n❌ Error en tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
