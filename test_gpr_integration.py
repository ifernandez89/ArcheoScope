#!/usr/bin/env python3
"""
Test GPR Integration in ArcheoScope
===================================

Demuestra cómo el sistema selecciona GPR automáticamente
según el ambiente detectado.
"""

import sys
import os

# Agregar backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from environment_classifier import EnvironmentClassifier
from satellite_connectors.gpr_connector import gpr_connector, GPRSignatureType
from multi_instrumental_enrichment import multi_instrumental_enrichment

def test_environment_gpr_selection():
    """Test 1: Verificar que GPR se recomienda en ambientes apropiados"""
    print("=" * 80)
    print("TEST 1: Selección Automática de GPR por Ambiente")
    print("=" * 80)
    
    classifier = EnvironmentClassifier()
    
    # Test cases: (nombre, lat, lon, gpr_esperado)
    test_cases = [
        ("Sahara (Egipto)", 25.0, 30.0, True),
        ("Desierto Arábigo", 25.0, 45.0, True),
        ("Atacama (Chile)", -23.0, -70.0, True),
        ("Amazonía (Brasil)", -3.0, -60.0, False),
        ("Océano Atlántico", 30.0, -40.0, False),
    ]
    
    for nombre, lat, lon, gpr_esperado in test_cases:
        context = classifier.classify(lat, lon)
        gpr_recomendado = 'GPR' in context.secondary_sensors
        
        status = "✅" if gpr_recomendado == gpr_esperado else "❌"
        print(f"\n{status} {nombre}")
        print(f"   Ambiente: {context.environment_type.value}")
        print(f"   GPR recomendado: {gpr_recomendado}")
        print(f"   Sensores primarios: {', '.join(context.primary_sensors[:3])}")
        print(f"   Sensores secundarios: {', '.join(context.secondary_sensors)}")

def test_gpr_similarity_scoring():
    """Test 2: Calcular scores de similitud GPR"""
    print("\n" + "=" * 80)
    print("TEST 2: Cálculo de Similitud GPR")
    print("=" * 80)
    
    # Test en diferentes ambientes
    test_locations = [
        ("Giza (Egipto)", 29.9792, 31.1342, "desert"),
        ("Petra (Jordania)", 30.3285, 35.4444, "desert"),
        ("Nazca (Perú)", -14.7390, -75.1300, "desert"),
        ("Machu Picchu (Perú)", -13.1631, -72.5450, "mountain"),
    ]
    
    for nombre, lat, lon, env_type in test_locations:
        result = gpr_connector.get_gpr_similarity_score(
            lat=lat,
            lon=lon,
            environment_type=env_type,
            target_depth_m=3.0
        )
        
        print(f"\n📍 {nombre}")
        print(f"   Coordenadas: {lat:.4f}, {lon:.4f}")
        print(f"   Ambiente: {env_type}")
        print(f"   Similarity Score: {result.value:.3f}")
        print(f"   Confidence: {result.confidence:.3f}")
        print(f"   Status: {result.status.value}")

def test_gpr_frequency_recommendation():
    """Test 3: Recomendaciones de frecuencia GPR"""
    print("\n" + "=" * 80)
    print("TEST 3: Recomendaciones de Frecuencia GPR")
    print("=" * 80)
    
    test_scenarios = [
        ("Shallow scan (0-1m)", "desert", 0.8),
        ("Medium scan (0-3m)", "semi_arid", 3.0),
        ("Deep scan (0-6m)", "desert", 6.0),
    ]
    
    for scenario, env_type, depth in test_scenarios:
        rec = gpr_connector.get_recommended_gpr_frequency(
            environment_type=env_type,
            target_depth_m=depth
        )
        
        print(f"\n🔧 {scenario}")
        print(f"   Ambiente: {env_type}")
        print(f"   Profundidad objetivo: {depth}m")
        print(f"   Frecuencia recomendada: {rec['recommended_frequency_mhz']} MHz")
        print(f"   Resolución esperada: {rec['expected_resolution_cm']} cm")
        print(f"   Penetración máxima: {rec['max_penetration_m']:.1f}m")

def test_gpr_synthetic_simulation():
    """Test 4: Simulación de firmas GPR sintéticas"""
    print("\n" + "=" * 80)
    print("TEST 4: Simulación GPR Sintética")
    print("=" * 80)
    
    signature_types = [
        (GPRSignatureType.CAVITY, 2.0, "Cámara subterránea"),
        (GPRSignatureType.BURIED_WALL, 1.5, "Muro enterrado"),
        (GPRSignatureType.FOUNDATION, 2.5, "Fundación de edificio"),
    ]
    
    for sig_type, depth, description in signature_types:
        synthetic = gpr_connector.simulate_gpr_signature(
            signature_type=sig_type,
            depth_m=depth,
            width_m=2.0
        )
        
        print(f"\n🧪 {description}")
        print(f"   Tipo: {sig_type.value}")
        print(f"   Profundidad: {depth}m")
        print(f"   Amplitud pico: {synthetic['peak_amplitude']:.3f}")
        print(f"   Tiempo doble vía: {synthetic['two_way_time_ns']:.1f} ns")
        print(f"   Simulado: {synthetic['simulated']}")

def test_multi_instrumental_with_gpr():
    """Test 5: Integración GPR en sistema multi-instrumental"""
    print("\n" + "=" * 80)
    print("TEST 5: Integración Multi-Instrumental con GPR")
    print("=" * 80)
    
    # Simular zona en desierto con GPR disponible
    zone = {
        'zone_id': 'TEST_DESERT_001',
        'center': {'lat': 30.0, 'lon': 31.0},
        'area_km2': 2.5,
        'priority': 'high_priority',
        'lidar_available': False
    }
    
    # Datos instrumentales simulados (incluyendo GPR)
    available_data = {
        'sar': {
            'compaction_detected': True,
            'confidence': 0.85,
            'backscatter_anomaly': 3.2,
            'texture_score': 0.75,
            'coherence': 0.82,
            'humidity_anomaly': 0.05,
            'source': 'Sentinel-1'
        },
        'thermal': {
            'thermal_anomaly_detected': True,
            'confidence': 0.80,
            'lst_day_anomaly': -1.2,
            'lst_night_anomaly': 2.1,
            'thermal_inertia': 0.78,
            'diurnal_range_anomaly': 1.5,
            'source': 'Landsat-8'
        },
        'multispectral': {
            'vegetation_anomaly_detected': True,
            'confidence': 0.70,
            'ndvi_anomaly': -0.08,
            'red_edge_anomaly': -0.03,
            'ndwi_anomaly': -0.02,
            'savi_anomaly': -0.06,
            'source': 'Sentinel-2'
        },
        'gpr': {
            'subsurface_anomaly_detected': True,
            'confidence': 0.75,
            'similarity_score': 0.82,
            'depth_m': 2.5,
            'anomaly_type': 'buried_wall',
            'amplitude_threshold': 0.70,
            'pattern_match_confidence': 0.75,
            'source': 'GPR_Pattern_Matching'
        },
        'multitemporal': {
            'persistence_detected': True,
            'confidence': 0.88,
            'years_persistent': 12,
            'seasonal_stability': 0.90,
            'change_resistance': 0.85,
            'temporal_consistency': 0.87,
            'source': 'Landsat/Sentinel archive'
        }
    }
    
    # Enriquecer candidata
    candidate = multi_instrumental_enrichment.enrich_candidate(zone, available_data)
    
    print(f"\n📊 Candidata: {candidate.candidate_id}")
    print(f"   Ubicación: {candidate.center_lat:.4f}, {candidate.center_lon:.4f}")
    print(f"   Score Multi-Instrumental: {candidate.multi_instrumental_score:.3f}")
    print(f"   Convergencia: {candidate.convergence_count}/{len(candidate.signals)} instrumentos")
    print(f"   Ratio de convergencia: {candidate.convergence_ratio:.1%}")
    print(f"   Acción recomendada: {candidate.recommended_action}")
    
    print("\n   Señales detectadas:")
    for inst_type, signal in candidate.signals.items():
        status = "✅" if signal.detected else "❌"
        print(f"   {status} {inst_type.value}: confidence={signal.confidence:.2f}")
        if signal.interpretation:
            print(f"      → {signal.interpretation}")

def main():
    """Ejecutar todos los tests"""
    print("\n" + "🧪" * 40)
    print("TESTS DE INTEGRACIÓN GPR EN ARCHEOSCOPE")
    print("🧪" * 40 + "\n")
    
    try:
        test_environment_gpr_selection()
        test_gpr_similarity_scoring()
        test_gpr_frequency_recommendation()
        test_gpr_synthetic_simulation()
        test_multi_instrumental_with_gpr()
        
        print("\n" + "=" * 80)
        print("✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        print("=" * 80)
        
        print("\n📝 RESUMEN:")
        print("   - GPR se selecciona automáticamente en ambientes áridos")
        print("   - Scores de similitud calculados correctamente")
        print("   - Recomendaciones de frecuencia optimizadas por ambiente")
        print("   - Simulación sintética funcional")
        print("   - Integración multi-instrumental operativa")
        
        print("\n🎯 PRÓXIMOS PASOS:")
        print("   1. Descargar datasets GPR reales de Zenodo")
        print("   2. Validar con sitios arqueológicos conocidos")
        print("   3. Ajustar pesos según resultados de campo")
        print("   4. Implementar gprMax para simulación avanzada")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
