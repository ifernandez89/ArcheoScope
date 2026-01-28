#!/usr/bin/env python3
"""
Test del Explanatory Strangeness Score (ESS).

CASOS DE PRUEBA:
1. 🗿 Machu Picchu: arquitectura simétrica en relieve extremo
2. 🐪 Giza/Esfinge: geometría regular en entorno sedimentario
3. 🌀 Nazca: patrones geométricos no explicables por erosión
4. ❌ Control negativo: sin geometría regular
"""

import sys
sys.path.insert(0, 'backend')

from scientific_pipeline import ScientificPipeline

def test_machu_picchu_case():
    """Test Machu Picchu: arquitectura simétrica en relieve extremo."""
    
    print("🗿 TEST 1: Machu Picchu - Arquitectura en Relieve Extremo")
    print("=" * 70)
    
    pipeline = ScientificPipeline()
    
    # Datos simulados de Machu Picchu
    anomaly_score = 0.0  # Sin anomalía instrumental
    anthropic_probability = 0.28  # Probabilidad moderada-baja
    symmetry = 0.85  # Alta simetría (terrazas)
    planarity = 0.75  # Alta planaridad (plataformas)
    edge_regularity = 0.80
    epistemic_uncertainty = 0.65  # Alta incertidumbre (NDVI ausente)
    geomorphology_hint = "anthropogenic_terracing_possible"
    environment_type = "mountain"
    
    level, score, reasons = pipeline._calculate_explanatory_strangeness(
        anomaly_score=anomaly_score,
        anthropic_probability=anthropic_probability,
        symmetry=symmetry,
        planarity=planarity,
        edge_regularity=edge_regularity,
        epistemic_uncertainty=epistemic_uncertainty,
        geomorphology_hint=geomorphology_hint,
        environment_type=environment_type
    )
    
    print(f"\n📊 RESULTADO:")
    print(f"   Anomaly Score: {anomaly_score:.3f}")
    print(f"   Anthropic Probability: {anthropic_probability:.3f}")
    print(f"   Explanatory Strangeness: {level.upper()} (score={score:.3f})")
    print(f"   Razones:")
    for reason in reasons:
        print(f"      • {reason}")
    
    # Verificación
    if level in ["high", "very_high"]:
        print(f"\n✅ CORRECTO: ESS detectado como {level.upper()}")
        print(f"   Interpretación: Arquitectura simétrica integrada en relieve extremo")
        return True
    else:
        print(f"\n⚠️ ESS bajo: {level} (esperado high/very_high)")
        return False


def test_giza_sphinx_case():
    """Test Giza/Esfinge: geometría regular en entorno sedimentario."""
    
    print("\n\n🐪 TEST 2: Giza/Esfinge - Geometría en Entorno Sedimentario")
    print("=" * 70)
    
    pipeline = ScientificPipeline()
    
    # Datos simulados de Giza/Esfinge
    anomaly_score = 0.0  # Sin anomalía instrumental
    anthropic_probability = 0.58  # Probabilidad moderada-alta
    symmetry = 0.75  # Alta simetría
    planarity = 0.88  # Planaridad extrema
    edge_regularity = 0.70
    epistemic_uncertainty = 0.50  # Incertidumbre moderada
    geomorphology_hint = "desert_terrain_general"
    environment_type = "desert"
    
    level, score, reasons = pipeline._calculate_explanatory_strangeness(
        anomaly_score=anomaly_score,
        anthropic_probability=anthropic_probability,
        symmetry=symmetry,
        planarity=planarity,
        edge_regularity=edge_regularity,
        epistemic_uncertainty=epistemic_uncertainty,
        geomorphology_hint=geomorphology_hint,
        environment_type=environment_type
    )
    
    print(f"\n📊 RESULTADO:")
    print(f"   Anomaly Score: {anomaly_score:.3f}")
    print(f"   Anthropic Probability: {anthropic_probability:.3f}")
    print(f"   Explanatory Strangeness: {level.upper()} (score={score:.3f})")
    print(f"   Razones:")
    for reason in reasons:
        print(f"      • {reason}")
    
    # Verificación
    if level in ["high", "very_high"]:
        print(f"\n✅ CORRECTO: ESS detectado como {level.upper()}")
        print(f"   Interpretación: Geometría regular en entorno sedimentario")
        return True
    else:
        print(f"\n⚠️ ESS bajo: {level} (esperado high/very_high)")
        return False


def test_nazca_case():
    """Test Nazca: patrones geométricos no explicables por erosión."""
    
    print("\n\n🌀 TEST 3: Nazca - Patrones Geométricos en Desierto")
    print("=" * 70)
    
    pipeline = ScientificPipeline()
    
    # Datos simulados de Nazca
    anomaly_score = 0.0  # Sin anomalía instrumental
    anthropic_probability = 0.35  # Probabilidad moderada
    symmetry = 0.90  # Simetría muy alta (líneas geométricas)
    planarity = 0.85  # Planaridad muy alta (superficie plana)
    edge_regularity = 0.88
    epistemic_uncertainty = 0.70  # Alta incertidumbre
    geomorphology_hint = "surface_pattern_anthropic_possible"
    environment_type = "desert"
    
    level, score, reasons = pipeline._calculate_explanatory_strangeness(
        anomaly_score=anomaly_score,
        anthropic_probability=anthropic_probability,
        symmetry=symmetry,
        planarity=planarity,
        edge_regularity=edge_regularity,
        epistemic_uncertainty=epistemic_uncertainty,
        geomorphology_hint=geomorphology_hint,
        environment_type=environment_type
    )
    
    print(f"\n📊 RESULTADO:")
    print(f"   Anomaly Score: {anomaly_score:.3f}")
    print(f"   Anthropic Probability: {anthropic_probability:.3f}")
    print(f"   Explanatory Strangeness: {level.upper()} (score={score:.3f})")
    print(f"   Razones:")
    for reason in reasons:
        print(f"      • {reason}")
    
    # Verificación
    if level == "very_high":
        print(f"\n✅ CORRECTO: ESS detectado como VERY_HIGH")
        print(f"   Interpretación: Patrones geométricos no explicables por erosión aleatoria")
        return True
    else:
        print(f"\n⚠️ ESS: {level} (esperado very_high)")
        return False


def test_negative_control():
    """Test control negativo: sin geometría regular."""
    
    print("\n\n❌ TEST 4: Control Negativo - Sin Geometría Regular")
    print("=" * 70)
    
    pipeline = ScientificPipeline()
    
    # Datos de formación natural sin geometría
    anomaly_score = 0.0
    anthropic_probability = 0.30
    symmetry = 0.35  # Baja simetría
    planarity = 0.40  # Baja planaridad
    edge_regularity = 0.30
    epistemic_uncertainty = 0.60
    geomorphology_hint = "aeolian_dune_field"
    environment_type = "desert"
    
    level, score, reasons = pipeline._calculate_explanatory_strangeness(
        anomaly_score=anomaly_score,
        anthropic_probability=anthropic_probability,
        symmetry=symmetry,
        planarity=planarity,
        edge_regularity=edge_regularity,
        epistemic_uncertainty=epistemic_uncertainty,
        geomorphology_hint=geomorphology_hint,
        environment_type=environment_type
    )
    
    print(f"\n📊 RESULTADO:")
    print(f"   Anomaly Score: {anomaly_score:.3f}")
    print(f"   Anthropic Probability: {anthropic_probability:.3f}")
    print(f"   Explanatory Strangeness: {level.upper()} (score={score:.3f})")
    
    # Verificación
    if level == "none":
        print(f"\n✅ CORRECTO: ESS no activado (geometría baja)")
        return True
    else:
        print(f"\n⚠️ ESS activado incorrectamente: {level}")
        return False


def test_high_anomaly_no_ess():
    """Test: alta anomalía NO activa ESS."""
    
    print("\n\n🔬 TEST 5: Alta Anomalía - ESS No Activado")
    print("=" * 70)
    
    pipeline = ScientificPipeline()
    
    # Alta anomalía → ESS no debe activarse
    anomaly_score = 0.65  # Alta anomalía
    anthropic_probability = 0.40
    symmetry = 0.85
    planarity = 0.80
    edge_regularity = 0.75
    epistemic_uncertainty = 0.50
    geomorphology_hint = "unknown"
    environment_type = "desert"
    
    level, score, reasons = pipeline._calculate_explanatory_strangeness(
        anomaly_score=anomaly_score,
        anthropic_probability=anthropic_probability,
        symmetry=symmetry,
        planarity=planarity,
        edge_regularity=edge_regularity,
        epistemic_uncertainty=epistemic_uncertainty,
        geomorphology_hint=geomorphology_hint,
        environment_type=environment_type
    )
    
    print(f"\n📊 RESULTADO:")
    print(f"   Anomaly Score: {anomaly_score:.3f} (alta)")
    print(f"   Explanatory Strangeness: {level.upper()}")
    
    # Verificación
    if level == "none":
        print(f"\n✅ CORRECTO: ESS no activado (anomalía alta detectada)")
        print(f"   Razón: ESS solo para casos sin anomalía instrumental")
        return True
    else:
        print(f"\n⚠️ ESS activado incorrectamente: {level}")
        return False


if __name__ == "__main__":
    print("\n🔬 SUITE DE TESTS: Explanatory Strangeness Score (ESS)")
    print("=" * 70)
    print("\nObjetivo: Capturar 'algo extraño' sin sensacionalismo")
    print("Filosofía: Modelo natural insuficiente ≠ pseudociencia\n")
    
    results = []
    
    # Test 1: Machu Picchu
    results.append(test_machu_picchu_case())
    
    # Test 2: Giza/Esfinge
    results.append(test_giza_sphinx_case())
    
    # Test 3: Nazca
    results.append(test_nazca_case())
    
    # Test 4: Control negativo
    results.append(test_negative_control())
    
    # Test 5: Alta anomalía
    results.append(test_high_anomaly_no_ess())
    
    # Resumen
    print("\n\n" + "=" * 70)
    print(f"📊 RESUMEN: {sum(results)}/{len(results)} tests pasaron")
    
    if all(results):
        print("\n🎉 EXPLANATORY STRANGENESS SCORE IMPLEMENTADO CORRECTAMENTE")
        print("\n💡 CASOS CUBIERTOS:")
        print("   ✓ Machu Picchu: arquitectura simétrica en relieve extremo")
        print("   ✓ Giza/Esfinge: geometría regular en entorno sedimentario")
        print("   ✓ Nazca: patrones geométricos no explicables por erosión")
        print("   ✓ Control negativo: sin geometría → ESS no activado")
        print("   ✓ Alta anomalía → ESS no activado (ya hay señal)")
        print("\n🔬 INTERPRETACIÓN CIENTÍFICA:")
        print("   'No hay anomalía instrumental, pero el modelo natural es")
        print("    insuficiente para explicar los patrones geométricos observados.'")
        print("\n   Esto NO es pseudociencia - es honestidad epistemológica.")
    else:
        print("\n⚠️ Algunos tests fallaron - revisar implementación")
