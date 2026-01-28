#!/usr/bin/env python3
"""
Test del clasificador refinado con el caso de la Esfinge.

CASO DE PRUEBA CRÍTICO:
- Estructura antropogénica conocida (Esfinge de Giza)
- Extremadamente antigua (~4500 años)
- Totalmente integrada al entorno geológico
- Sin actividad humana reciente detectable

EXPECTATIVA:
- Origen antropogénico: ALTO (~70-95%)
- Actividad antropogénica: BAJO (~5-20%)
- Anomaly Score: BAJO (0-10%)
- Clasificación: "historical_structure"

Esto NO es contradictorio - es arqueología histórica.
"""

import sys
sys.path.insert(0, 'backend')

from anthropic_classifier_refined import RefinedAnthropicClassifier
import numpy as np

def test_sphinx_case():
    """Test caso Esfinge: alto origen, baja actividad, baja anomalía."""
    
    print("🐪 TEST: Esfinge de Giza - Clasificación Refinada")
    print("=" * 70)
    
    # Datos simulados de la Esfinge (basados en análisis real)
    anomaly_score = 0.0  # Sin anomalía detectable
    
    morphology = {
        'symmetry_score': 0.75,  # Alta simetría (estructura tallada)
        'edge_regularity': 0.70,  # Bordes regulares (aunque erosionados)
        'planarity': 0.65,  # Superficie relativamente plana
        'artificial_indicators': ['geometric_symmetry', 'carved_features'],
        'geomorphology_hint': 'limestone_plateau'  # Contexto geológico
    }
    
    normalized_features = {
        'sentinel_2_ndvi_zscore': -1.2,  # NDVI bajo (desierto)
        'sentinel_1_sar_zscore': -0.8,   # SAR bajo (piedra erosionada ≈ roca natural)
        'modis_lst_zscore': 0.3,         # Térmico normal
        'landsat_thermal_zscore': 0.2,   # Sin calor residual
        'opentopography_zscore': -0.5    # Topografía baja
    }
    
    raw_measurements = {
        'environment_type': 'desert',
        'instruments_available': 5
    }
    
    # Clasificar
    classifier = RefinedAnthropicClassifier()
    result = classifier.classify(
        anomaly_score=anomaly_score,
        morphology=morphology,
        normalized_features=normalized_features,
        raw_measurements=raw_measurements,
        environment_type='desert'
    )
    
    # Mostrar resultados
    print(f"\n📊 RESULTADOS:")
    print(f"\n🏛️  ORIGEN ANTROPOGÉNICO:")
    print(f"   Probabilidad: {result.anthropic_origin_probability:.1%}")
    print(f"   Intervalo: [{result.origin_confidence_interval[0]:.1%}, {result.origin_confidence_interval[1]:.1%}]")
    print(f"   Razonamiento:")
    for reason in result.origin_reasoning:
        print(f"      • {reason}")
    
    print(f"\n🔥 ACTIVIDAD ANTROPOGÉNICA:")
    print(f"   Probabilidad: {result.anthropic_activity_probability:.1%}")
    print(f"   Intervalo: [{result.activity_confidence_interval[0]:.1%}, {result.activity_confidence_interval[1]:.1%}]")
    print(f"   Razonamiento:")
    for reason in result.activity_reasoning:
        print(f"      • {reason}")
    
    print(f"\n📍 CLASIFICACIÓN: {result.site_classification}")
    print(f"🎯 CONFIANZA: {result.confidence}")
    print(f"📡 COBERTURA: {result.coverage_raw:.1%} raw, {result.coverage_effective:.1%} effective")
    
    # Verificaciones
    print(f"\n✅ VERIFICACIONES:")
    
    checks = []
    
    # 1. Origen debe ser alto
    if result.anthropic_origin_probability >= 0.6:
        print(f"   ✓ Origen antropogénico alto ({result.anthropic_origin_probability:.1%})")
        checks.append(True)
    else:
        print(f"   ✗ Origen antropogénico bajo ({result.anthropic_origin_probability:.1%}) - ESPERADO ALTO")
        checks.append(False)
    
    # 2. Actividad debe ser baja
    if result.anthropic_activity_probability <= 0.4:
        print(f"   ✓ Actividad antropogénica baja ({result.anthropic_activity_probability:.1%})")
        checks.append(True)
    else:
        print(f"   ✗ Actividad antropogénica alta ({result.anthropic_activity_probability:.1%}) - ESPERADO BAJO")
        checks.append(False)
    
    # 3. Clasificación debe ser "historical_structure"
    if result.site_classification == "historical_structure":
        print(f"   ✓ Clasificación correcta: {result.site_classification}")
        checks.append(True)
    else:
        print(f"   ✗ Clasificación incorrecta: {result.site_classification} - ESPERADO historical_structure")
        checks.append(False)
    
    # 4. NO debe haber contradicción origen-anomalía
    if result.anthropic_origin_probability > 0.6 and anomaly_score < 0.2:
        print(f"   ✓ Sin contradicción: alto origen ({result.anthropic_origin_probability:.1%}), baja anomalía ({anomaly_score:.1%})")
        checks.append(True)
    
    # 5. Intervalos de confianza deben ser coherentes
    origin_in_interval = (result.origin_confidence_interval[0] <= 
                         result.anthropic_origin_probability <= 
                         result.origin_confidence_interval[1])
    activity_in_interval = (result.activity_confidence_interval[0] <= 
                           result.anthropic_activity_probability <= 
                           result.activity_confidence_interval[1])
    
    if origin_in_interval and activity_in_interval:
        print(f"   ✓ Intervalos de confianza coherentes")
        checks.append(True)
    else:
        print(f"   ✗ Intervalos de confianza incoherentes")
        checks.append(False)
    
    print(f"\n{'=' * 70}")
    
    if all(checks):
        print("✅ TODOS LOS CHECKS PASARON - Clasificador refinado funciona correctamente")
        print("\n💡 INTERPRETACIÓN:")
        print("   La Esfinge es una estructura antropogénica histórica sin actividad reciente.")
        print("   Alto origen + baja actividad + baja anomalía = ARQUEOLOGÍA HISTÓRICA ✓")
        return True
    else:
        print(f"⚠️ {sum(checks)}/{len(checks)} checks pasaron - Revisar clasificador")
        return False


def test_active_site_case():
    """Test caso sitio activo: alto origen, alta actividad, alta anomalía."""
    
    print("\n\n🏗️ TEST: Sitio Activo - Clasificación Refinada")
    print("=" * 70)
    
    # Datos simulados de un sitio con actividad reciente
    anomaly_score = 0.65  # Alta anomalía
    
    morphology = {
        'symmetry_score': 0.80,
        'edge_regularity': 0.75,
        'planarity': 0.70,
        'artificial_indicators': ['geometric_pattern', 'regular_spacing'],
        'geomorphology_hint': 'modified_terrain'
    }
    
    normalized_features = {
        'sentinel_2_ndvi_zscore': 2.5,   # NDVI anómalo
        'sentinel_1_sar_zscore': 3.0,    # SAR muy anómalo
        'modis_lst_zscore': 2.0,         # Térmico anómalo
        'landsat_thermal_zscore': 1.8,   # Calor residual
        'opentopography_zscore': 1.5     # Topografía modificada
    }
    
    raw_measurements = {
        'environment_type': 'agricultural',
        'instruments_available': 5
    }
    
    # Clasificar
    classifier = RefinedAnthropicClassifier()
    result = classifier.classify(
        anomaly_score=anomaly_score,
        morphology=morphology,
        normalized_features=normalized_features,
        raw_measurements=raw_measurements,
        environment_type='agricultural'
    )
    
    print(f"\n📊 RESULTADOS:")
    print(f"   🏛️  Origen: {result.anthropic_origin_probability:.1%}")
    print(f"   🔥 Actividad: {result.anthropic_activity_probability:.1%}")
    print(f"   📍 Clasificación: {result.site_classification}")
    
    # Verificación
    if (result.anthropic_origin_probability > 0.6 and 
        result.anthropic_activity_probability > 0.3 and
        result.site_classification == "active_site"):
        print(f"\n✅ Sitio activo detectado correctamente")
        return True
    else:
        print(f"\n⚠️ Clasificación incorrecta para sitio activo")
        return False


def test_natural_formation_case():
    """Test caso formación natural: bajo origen, baja actividad, posible anomalía."""
    
    print("\n\n🏔️ TEST: Formación Natural - Clasificación Refinada")
    print("=" * 70)
    
    # Datos simulados de formación natural
    anomaly_score = 0.35  # Anomalía moderada (geomorfología inusual)
    
    morphology = {
        'symmetry_score': 0.30,
        'edge_regularity': 0.25,
        'planarity': 0.40,
        'artificial_indicators': [],
        'geomorphology_hint': 'glacial_moraine'
    }
    
    normalized_features = {
        'sentinel_2_ndvi_zscore': 1.2,
        'sentinel_1_sar_zscore': 1.5,
        'modis_lst_zscore': 0.8,
        'landsat_thermal_zscore': 0.5,
        'opentopography_zscore': 1.8
    }
    
    raw_measurements = {
        'environment_type': 'mountain',
        'instruments_available': 5
    }
    
    # Clasificar
    classifier = RefinedAnthropicClassifier()
    result = classifier.classify(
        anomaly_score=anomaly_score,
        morphology=morphology,
        normalized_features=normalized_features,
        raw_measurements=raw_measurements,
        environment_type='mountain'
    )
    
    print(f"\n📊 RESULTADOS:")
    print(f"   🏛️  Origen: {result.anthropic_origin_probability:.1%}")
    print(f"   🔥 Actividad: {result.anthropic_activity_probability:.1%}")
    print(f"   📍 Clasificación: {result.site_classification}")
    
    # Verificación
    if (result.anthropic_origin_probability < 0.5 and 
        result.site_classification in ["natural_formation", "natural_anomaly"]):
        print(f"\n✅ Formación natural detectada correctamente")
        return True
    else:
        print(f"\n⚠️ Clasificación incorrecta para formación natural")
        return False


if __name__ == "__main__":
    print("\n🧪 SUITE DE TESTS: Clasificador Antropogénico Refinado")
    print("=" * 70)
    print("\nObjetivo: Resolver el problema de la Esfinge")
    print("Separar origen antropogénico de actividad antropogénica\n")
    
    results = []
    
    # Test 1: Esfinge (caso crítico)
    results.append(test_sphinx_case())
    
    # Test 2: Sitio activo
    results.append(test_active_site_case())
    
    # Test 3: Formación natural
    results.append(test_natural_formation_case())
    
    # Resumen
    print("\n\n" + "=" * 70)
    print(f"📊 RESUMEN: {sum(results)}/{len(results)} tests pasaron")
    
    if all(results):
        print("\n🎉 CLASIFICADOR REFINADO FUNCIONA CORRECTAMENTE")
        print("\n💡 MEJORAS IMPLEMENTADAS:")
        print("   ✓ Separación origen vs actividad antropogénica")
        print("   ✓ Intervalos de confianza coherentes")
        print("   ✓ Clasificación de sitios (histórico/activo/natural)")
        print("   ✓ Sin contradicciones origen-anomalía")
        print("   ✓ Razonamiento separado por eje")
    else:
        print("\n⚠️ Algunos tests fallaron - revisar implementación")
