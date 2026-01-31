#!/usr/bin/env python3
"""
Ejemplo Práctico: Detección de Geoglifos en Arabia
===================================================

Este script muestra cómo usar el sistema de detección de geoglifos
para analizar una zona específica en Arabia.
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


def ejemplo_1_deteccion_basica():
    """
    Ejemplo 1: Detección básica en modo científico
    
    Caso de uso: Validar un posible geoglifo reportado en Arabia
    """
    print("\n" + "="*70)
    print("📍 EJEMPLO 1: Detección Básica en Modo Científico")
    print("="*70)
    
    # Coordenadas de ejemplo en Arabia (zona de harrats)
    lat, lon = 26.5, 38.5
    
    # Bounding box (0.2° ≈ 22 km)
    lat_min, lat_max = lat - 0.1, lat + 0.1
    lon_min, lon_max = lon - 0.1, lon + 0.1
    
    print(f"\n🎯 Analizando coordenadas: ({lat}, {lon})")
    print(f"   Bbox: ({lat_min}, {lat_max}, {lon_min}, {lon_max})")
    
    # Inicializar detector en modo científico
    detector = GeoglyphDetector(mode=DetectionMode.SCIENTIFIC)
    
    # Simular DEM (en producción, usar datos reales)
    dem_data = np.random.rand(100, 100) * 100  # Elevación 0-100m
    
    # Detectar
    result = detector.detect_geoglyph(
        lat=lat,
        lon=lon,
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
        dem_data=dem_data,
        resolution_m=0.5  # WorldView/Pleiades
    )
    
    # Mostrar resultado
    print(f"\n✅ Detección completada:")
    print(f"   Tipo detectado: {result.geoglyph_type.value}")
    print(f"   Cultural Score: {result.cultural_score:.3f}")
    
    # Decisión
    if result.cultural_score >= 0.75:
        print(f"\n🏆 ALTA PROBABILIDAD - Prioridad: {result.validation_priority.upper()}")
        print("   Recomendación: Validar con imágenes de alta resolución")
    elif result.cultural_score >= 0.50:
        print(f"\n⚠️ PROBABILIDAD MODERADA - Prioridad: {result.validation_priority.upper()}")
        print("   Recomendación: Análisis adicional requerido")
    else:
        print(f"\n❌ BAJA PROBABILIDAD - Prioridad: {result.validation_priority.upper()}")
        print("   Recomendación: Probablemente formación natural")
    
    # Detalles clave
    print(f"\n📐 Detalles de Orientación:")
    print(f"   Azimut: {result.orientation.azimuth_deg:.1f}°")
    if result.orientation.is_nw_se:
        print("   ✓ Orientación NW-SE (patrón conocido en Arabia)")
    if result.orientation.is_e_w:
        print("   ✓ Orientación E-W (patrón conocido en Arabia)")
    
    print(f"\n🌋 Contexto Geológico:")
    if result.volcanic_context.on_stable_surface:
        print("   ✓ Superficie estable (favorable)")
    if not result.volcanic_context.on_young_flow:
        print("   ✓ NO en colada joven (favorable)")
    
    print(f"\n💧 Contexto Hídrico:")
    if result.paleo_hydrology.on_sediment_transition:
        print("   🏆 Transición roca-sedimento (ORO)")
    print(f"   Distancia a wadi: {result.paleo_hydrology.distance_to_wadi_km:.1f}km")
    
    return result


def ejemplo_2_exploracion_zona():
    """
    Ejemplo 2: Exploración de zona prometedora
    
    Caso de uso: Explorar sistemáticamente una zona no catalogada
    """
    print("\n" + "="*70)
    print("🗺️ EJEMPLO 2: Exploración de Zona Prometedora")
    print("="*70)
    
    # Obtener zonas prometedoras
    zones = get_promising_zones()
    
    # Seleccionar zona de alta prioridad
    zone_id = "harrat_uwayrid_south"
    zone = zones[zone_id]
    
    print(f"\n📍 Zona seleccionada: {zone['name']}")
    print(f"   Prioridad: {zone['priority'].upper()}")
    print(f"   Razón: {zone['reason']}")
    print(f"   Bbox: {zone['bbox']}")
    
    # Usar modo explorador (más sensible)
    detector = GeoglyphDetector(mode=DetectionMode.EXPLORER)
    
    # Coordenadas centrales de la zona
    lat_min, lat_max, lon_min, lon_max = zone['bbox']
    lat = (lat_min + lat_max) / 2
    lon = (lon_min + lon_max) / 2
    
    print(f"\n🔍 Analizando punto central: ({lat:.2f}, {lon:.2f})")
    
    # Detectar
    result = detector.detect_geoglyph(
        lat=lat,
        lon=lon,
        lat_min=lat - 0.05,
        lat_max=lat + 0.05,
        lon_min=lon - 0.05,
        lon_max=lon + 0.05,
        resolution_m=2.0  # Resolución moderada para exploración
    )
    
    print(f"\n📊 Resultado de exploración:")
    print(f"   Cultural Score: {result.cultural_score:.3f}")
    print(f"   Tipo: {result.geoglyph_type.value}")
    
    if result.needs_validation:
        print(f"\n✅ Candidato detectado - Prioridad: {result.validation_priority.upper()}")
        print("   Próximo paso: Análisis con mayor resolución")
    else:
        print("\n❌ No se detectó candidato significativo")
    
    return result


def ejemplo_3_comparacion_modos():
    """
    Ejemplo 3: Comparar los 3 modos operativos
    
    Caso de uso: Entender cómo cada modo afecta la detección
    """
    print("\n" + "="*70)
    print("📊 EJEMPLO 3: Comparación de Modos Operativos")
    print("="*70)
    
    # Coordenadas fijas
    lat, lon = 26.5, 38.5
    bbox = (26.4, 26.6, 38.4, 38.6)
    dem_data = np.random.rand(100, 100) * 100
    
    # Probar cada modo
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
    
    # Mostrar comparación
    print("\n" + "-"*70)
    print(f"{'Modo':<15} {'Cultural Score':<15} {'Prioridad':<12} {'Validación'}")
    print("-"*70)
    
    for name, result in results:
        validation = "SÍ" if result.needs_validation else "NO"
        print(f"{name:<15} {result.cultural_score:<15.3f} {result.validation_priority:<12} {validation}")
    
    print("-"*70)
    
    print("\n💡 Interpretación:")
    print("   • Científico: Más estricto, menos falsos positivos")
    print("   • Explorador: Balance entre sensibilidad y precisión")
    print("   • Cognitivo: Más sensible, solo para señalar anomalías")


def ejemplo_4_analisis_completo():
    """
    Ejemplo 4: Análisis completo con todos los detalles
    
    Caso de uso: Preparar reporte para validación arqueológica
    """
    print("\n" + "="*70)
    print("📋 EJEMPLO 4: Análisis Completo para Reporte")
    print("="*70)
    
    # Coordenadas de candidato
    lat, lon = 26.5, 38.5
    bbox = (26.4, 26.6, 38.4, 38.6)
    
    # Detector científico
    detector = GeoglyphDetector(mode=DetectionMode.SCIENTIFIC)
    
    # DEM simulado
    dem_data = np.random.rand(100, 100) * 100
    
    # Detectar
    result = detector.detect_geoglyph(
        lat=lat, lon=lon,
        lat_min=bbox[0], lat_max=bbox[1],
        lon_min=bbox[2], lon_max=bbox[3],
        dem_data=dem_data,
        resolution_m=0.5
    )
    
    # Generar reporte completo
    print("\n" + "="*70)
    print("REPORTE DE DETECCIÓN DE GEOGLIFO")
    print("="*70)
    
    print(f"\n1. IDENTIFICACIÓN")
    print(f"   ID: {result.candidate_id}")
    print(f"   Coordenadas: {result.lat:.4f}°, {result.lon:.4f}°")
    print(f"   Fecha: {result.detection_timestamp}")
    
    print(f"\n2. CLASIFICACIÓN")
    print(f"   Tipo: {result.geoglyph_type.value}")
    print(f"   Confianza: {result.type_confidence*100:.0f}%")
    
    print(f"\n3. SCORING")
    print(f"   Cultural Score: {result.cultural_score:.3f}")
    print(f"   - Forma: {result.form_score:.3f}")
    print(f"   - Orientación: {result.orientation_score:.3f}")
    print(f"   - Contexto: {result.context_score:.3f}")
    print(f"   - Hidrología: {result.hydrology_score:.3f}")
    
    print(f"\n4. GEOMETRÍA")
    print(f"   Azimut: {result.orientation.azimuth_deg:.1f}°")
    print(f"   Eje mayor: {result.orientation.major_axis_length_m:.1f}m")
    print(f"   Eje menor: {result.orientation.minor_axis_length_m:.1f}m")
    print(f"   Aspect ratio: {result.orientation.aspect_ratio:.2f}")
    print(f"   Simetría: {(1-result.orientation.bilateral_symmetry)*100:.0f}%")
    
    print(f"\n5. CONTEXTO GEOLÓGICO")
    print(f"   Superficie estable: {'SÍ' if result.volcanic_context.on_stable_surface else 'NO'}")
    print(f"   Colada joven: {'SÍ (DESFAVORABLE)' if result.volcanic_context.on_young_flow else 'NO'}")
    print(f"   Dist. basalto: {result.volcanic_context.distance_to_basalt_flow_km:.1f}km")
    
    print(f"\n6. CONTEXTO HÍDRICO")
    print(f"   Transición sedimento: {'SÍ (ORO)' if result.paleo_hydrology.on_sediment_transition else 'NO'}")
    print(f"   Dist. wadi: {result.paleo_hydrology.distance_to_wadi_km:.1f}km")
    print(f"   Prob. agua estacional: {result.paleo_hydrology.seasonal_water_probability*100:.0f}%")
    
    print(f"\n7. ALINEACIONES ASTRONÓMICAS")
    print(f"   Mejor alineación: {result.celestial_alignment.best_solar_alignment}")
    print(f"   Solsticio verano: {result.celestial_alignment.summer_solstice_alignment*100:.0f}%")
    print(f"   Solsticio invierno: {result.celestial_alignment.winter_solstice_alignment*100:.0f}%")
    
    print(f"\n8. VALIDACIÓN")
    print(f"   Necesita validación: {'SÍ' if result.needs_validation else 'NO'}")
    print(f"   Prioridad: {result.validation_priority.upper()}")
    print(f"   Resolución recomendada: {result.recommended_resolution_m}m/pixel")
    print(f"   Paper-level: {'SÍ' if result.paper_level_discovery else 'NO'}")
    
    print(f"\n9. RAZONAMIENTO")
    for i, reason in enumerate(result.detection_reasoning, 1):
        print(f"   {i}. {reason}")
    
    print(f"\n10. RIESGOS DE FALSO POSITIVO")
    if result.false_positive_risks:
        for i, risk in enumerate(result.false_positive_risks, 1):
            print(f"   {i}. {risk}")
    else:
        print("   Ninguno identificado")
    
    print("\n" + "="*70)
    
    return result


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "="*70)
    print("🔍 EJEMPLOS PRÁCTICOS - DETECCIÓN DE GEOGLIFOS")
    print("="*70)
    
    try:
        # Ejemplo 1: Detección básica
        ejemplo_1_deteccion_basica()
        
        # Ejemplo 2: Exploración de zona
        ejemplo_2_exploracion_zona()
        
        # Ejemplo 3: Comparación de modos
        ejemplo_3_comparacion_modos()
        
        # Ejemplo 4: Análisis completo
        ejemplo_4_analisis_completo()
        
        print("\n" + "="*70)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS")
        print("="*70)
        
        print("\n💡 Próximos pasos:")
        print("   1. Adaptar estos ejemplos a tus coordenadas específicas")
        print("   2. Integrar con datos DEM reales")
        print("   3. Usar API REST para integración con frontend")
        print("   4. Revisar GEOGLYPH_DETECTION_GUIDE.md para más detalles")
        print()
        
    except Exception as e:
        print(f"\n❌ Error en ejemplos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
