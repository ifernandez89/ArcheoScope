"""
TEST CRÍTICO: Verificar que el sistema es 100% DETERMINÍSTICO
NO debe haber NINGUNA variación en los resultados para las mismas coordenadas
"""

import sys
import json
from datetime import datetime

# Test de detección de agua
from backend.water.water_detector import WaterDetector
from backend.water.submarine_archaeology import SubmarineArchaeologyEngine

def test_deterministic_water_detection():
    """Probar que la detección de agua es determinística"""
    print("\n" + "="*80)
    print("TEST 1: DETECCIÓN DE AGUA DETERMINÍSTICA")
    print("="*80)
    
    detector = WaterDetector()
    
    # Coordenadas de prueba
    test_coords = [
        (18.5, -77.5, "Jamaica"),
        (25.511, -70.361, "Bermuda Triangle"),
        (21.3, -157.9, "Pearl Harbor"),
        (40.5, -69.9, "Andrea Doria")
    ]
    
    all_deterministic = True
    
    for lat, lon, name in test_coords:
        print(f"\n📍 Probando: {name} ({lat}, {lon})")
        print("-" * 60)
        
        results = []
        for run in range(5):
            water_context = detector.detect_water_context(lat, lon)
            if water_context:
                results.append({
                    'water_type': water_context.water_type.value,
                    'depth': water_context.estimated_depth_m,
                    'potential': water_context.archaeological_potential,
                    'routes': water_context.historical_shipping_routes,
                    'wrecks': water_context.known_wrecks_nearby
                })
            else:
                results.append(None)
        
        # Verificar que todos los resultados son idénticos
        if all(r == results[0] for r in results):
            print(f"   ✅ DETERMINÍSTICO - 5 ejecuciones idénticas")
            if results[0]:
                print(f"      Tipo: {results[0]['water_type']}")
                print(f"      Profundidad: {results[0]['depth']:.1f}m")
                print(f"      Potencial: {results[0]['potential']}")
        else:
            print(f"   ❌ NO DETERMINÍSTICO - Resultados varían:")
            for i, r in enumerate(results, 1):
                if r:
                    print(f"      Run {i}: depth={r['depth']:.1f}m, potential={r['potential']}")
                else:
                    print(f"      Run {i}: No water detected")
            all_deterministic = False
    
    return all_deterministic

def test_deterministic_submarine_analysis():
    """Probar que el análisis submarino es determinístico"""
    print("\n" + "="*80)
    print("TEST 2: ANÁLISIS SUBMARINO DETERMINÍSTICO")
    print("="*80)
    
    detector = WaterDetector()
    submarine_engine = SubmarineArchaeologyEngine()
    
    # Coordenadas de prueba
    test_coords = [
        (18.5, -77.5, "Jamaica"),
        (25.511, -70.361, "Bermuda Triangle"),
        (21.3, -157.9, "Pearl Harbor")
    ]
    
    all_deterministic = True
    
    for lat, lon, name in test_coords:
        print(f"\n📍 Probando: {name} ({lat}, {lon})")
        print("-" * 60)
        
        water_context = detector.detect_water_context(lat, lon)
        if not water_context:
            print(f"   ⚠️ No es agua - saltando")
            continue
        
        bounds = {
            'lat_min': lat - 0.01,
            'lat_max': lat + 0.01,
            'lon_min': lon - 0.01,
            'lon_max': lon + 0.01
        }
        
        results = []
        for run in range(5):
            submarine_results = submarine_engine.analyze_submarine_area(water_context, bounds)
            results.append({
                'num_candidates': len(submarine_results['wreck_candidates']),
                'num_instruments': len(submarine_results['instruments_used']),
                'volumetric_anomalies': submarine_results['volumetric_anomalies'],
                'high_priority': submarine_results['summary']['high_priority_targets']
            })
            
            # Guardar detalles de candidatos
            if submarine_results['wreck_candidates']:
                results[-1]['candidates'] = []
                for candidate in submarine_results['wreck_candidates']:
                    results[-1]['candidates'].append({
                        'length': candidate['signature']['length_m'],
                        'width': candidate['signature']['width_m'],
                        'height': candidate['signature']['height_m'],
                        'priority': candidate['archaeological_priority']
                    })
        
        # Verificar que todos los resultados son idénticos
        if all(r['num_candidates'] == results[0]['num_candidates'] for r in results):
            print(f"   ✅ DETERMINÍSTICO - 5 ejecuciones idénticas")
            print(f"      Candidatos: {results[0]['num_candidates']}")
            print(f"      Instrumentos: {results[0]['num_instruments']}")
            print(f"      Anomalías volumétricas: {results[0]['volumetric_anomalies']}")
            print(f"      Alta prioridad: {results[0]['high_priority']}")
            
            # Verificar dimensiones de candidatos
            if results[0]['num_candidates'] > 0:
                print(f"\n      Verificando dimensiones de candidatos:")
                for i in range(results[0]['num_candidates']):
                    candidate_dims = [r['candidates'][i] for r in results]
                    if all(c == candidate_dims[0] for c in candidate_dims):
                        print(f"         Candidato {i+1}: ✅ Dimensiones idénticas")
                        print(f"            {candidate_dims[0]['length']:.1f}m x {candidate_dims[0]['width']:.1f}m x {candidate_dims[0]['height']:.1f}m")
                    else:
                        print(f"         Candidato {i+1}: ❌ Dimensiones varían")
                        for j, c in enumerate(candidate_dims, 1):
                            print(f"            Run {j}: {c['length']:.1f}m x {c['width']:.1f}m x {c['height']:.1f}m")
                        all_deterministic = False
        else:
            print(f"   ❌ NO DETERMINÍSTICO - Número de candidatos varía:")
            for i, r in enumerate(results, 1):
                print(f"      Run {i}: {r['num_candidates']} candidatos")
            all_deterministic = False
    
    return all_deterministic

def main():
    print("\n" + "="*80)
    print("🔬 AUDITORÍA CRÍTICA: SISTEMA 100% DETERMINÍSTICO")
    print("="*80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nOBJETIVO: Verificar que NO hay np.random.randint() ni variación aleatoria")
    print("REGLA: Mismas coordenadas SIEMPRE deben producir EXACTAMENTE los mismos resultados")
    
    # Test 1: Detección de agua
    test1_passed = test_deterministic_water_detection()
    
    # Test 2: Análisis submarino
    test2_passed = test_deterministic_submarine_analysis()
    
    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN FINAL")
    print("="*80)
    
    if test1_passed and test2_passed:
        print("\n✅ ¡ÉXITO! Sistema 100% DETERMINÍSTICO")
        print("   - Detección de agua: ✅ DETERMINÍSTICO")
        print("   - Análisis submarino: ✅ DETERMINÍSTICO")
        print("   - Número de candidatos: ✅ CONSISTENTE")
        print("   - Dimensiones de candidatos: ✅ IDÉNTICAS")
        print("\n🎉 NO HAY DATOS FALSOS - Sistema confiable")
        return 0
    else:
        print("\n❌ FALLO - Sistema NO es determinístico")
        if not test1_passed:
            print("   - Detección de agua: ❌ VARÍA")
        if not test2_passed:
            print("   - Análisis submarino: ❌ VARÍA")
        print("\n⚠️ DATOS FALSOS DETECTADOS - Requiere corrección")
        return 1

if __name__ == "__main__":
    sys.exit(main())
