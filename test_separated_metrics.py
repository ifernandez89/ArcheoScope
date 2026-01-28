#!/usr/bin/env python3
"""
Test de Métricas Separadas (Estado del Arte)
==============================================

Verificar que el sistema separa correctamente:
1. Origen antropogénico (¿fue creado por humanos?)
2. Actividad antropogénica (¿hay actividad actual?)
3. Anomalía instrumental (¿hay anomalía detectable?)
4. Confianza del modelo (¿qué tan seguro está el modelo?)

Casos de prueba:
- Giza/Esfinge: origen alto (90%), actividad baja (5%), anomalía 0%
- Machu Picchu: origen alto (85%), actividad baja (10%), anomalía 0%
- Nazca: origen muy alto (95%), actividad muy baja (2%), anomalía 0%
"""

import requests
import json

def test_separated_metrics():
    """Test de métricas separadas en sitios conocidos."""
    
    print("="*80)
    print("TEST: MÉTRICAS SEPARADAS (ESTADO DEL ARTE)")
    print("="*80)
    print()
    
    # Casos de prueba
    test_cases = [
        {
            "name": "Giza/Esfinge",
            "coords": {
                "lat_min": 29.974,
                "lat_max": 29.976,
                "lon_min": 31.136,
                "lon_max": 31.138,
                "region_name": "Giza Sphinx Egypt"
            },
            "expected": {
                "origin": (0.70, 0.95),  # 70-95%
                "activity": (0.0, 0.15),  # 0-15%
                "anomaly": (0.0, 0.05)    # 0-5%
            }
        },
        {
            "name": "Machu Picchu",
            "coords": {
                "lat_min": -13.164,
                "lat_max": -13.162,
                "lon_min": -72.546,
                "lon_max": -72.544,
                "region_name": "Machu Picchu Peru"
            },
            "expected": {
                "origin": (0.70, 0.95),  # 70-95%
                "activity": (0.0, 0.20),  # 0-20%
                "anomaly": (0.0, 0.05)    # 0-5%
            }
        },
        {
            "name": "Nazca Lines",
            "coords": {
                "lat_min": -14.692,
                "lat_max": -14.690,
                "lon_min": -75.138,
                "lon_max": -75.136,
                "region_name": "Nazca Lines Peru"
            },
            "expected": {
                "origin": (0.75, 0.98),  # 75-98%
                "activity": (0.0, 0.10),  # 0-10%
                "anomaly": (0.0, 0.05)    # 0-5%
            }
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"🏛️ CASO: {test_case['name']}")
        print(f"{'='*80}")
        
        try:
            response = requests.post(
                "http://localhost:8002/api/scientific/analyze",
                json=test_case['coords'],
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"❌ Error HTTP: {response.status_code}")
                results.append({
                    "name": test_case['name'],
                    "status": "error",
                    "error": f"HTTP {response.status_code}"
                })
                continue
            
            data = response.json()
            scientific = data.get('scientific_output', {})
            phase_d = data.get('phase_d_anthropic', {})
            
            # Extraer métricas separadas
            origin = scientific.get('anthropic_origin_probability', 0.0)
            activity = scientific.get('anthropic_activity_probability', 0.0)
            anomaly = scientific.get('instrumental_anomaly_probability', 0.0)
            confidence = scientific.get('model_inference_confidence', 'unknown')
            
            # Métricas legacy para comparación
            legacy_prob = scientific.get('anthropic_probability', 0.0)
            anomaly_score = scientific.get('anomaly_score', 0.0)
            
            print(f"\n📊 MÉTRICAS SEPARADAS:")
            print(f"  Origen antropogénico:     {origin:.1%}")
            print(f"  Actividad antropogénica:  {activity:.1%}")
            print(f"  Anomalía instrumental:    {anomaly:.1%}")
            print(f"  Confianza del modelo:     {confidence}")
            
            print(f"\n📊 MÉTRICAS LEGACY (comparación):")
            print(f"  Probabilidad antropogénica: {legacy_prob:.1%}")
            print(f"  Anomaly score:              {anomaly_score:.1%}")
            
            # Verificar rangos esperados
            expected = test_case['expected']
            origin_ok = expected['origin'][0] <= origin <= expected['origin'][1]
            activity_ok = expected['activity'][0] <= activity <= expected['activity'][1]
            anomaly_ok = expected['anomaly'][0] <= anomaly <= expected['anomaly'][1]
            
            print(f"\n✅ VALIDACIÓN:")
            print(f"  Origen en rango esperado:    {'✅' if origin_ok else '❌'} ({expected['origin'][0]:.0%}-{expected['origin'][1]:.0%})")
            print(f"  Actividad en rango esperado: {'✅' if activity_ok else '❌'} ({expected['activity'][0]:.0%}-{expected['activity'][1]:.0%})")
            print(f"  Anomalía en rango esperado:  {'✅' if anomaly_ok else '❌'} ({expected['anomaly'][0]:.0%}-{expected['anomaly'][1]:.0%})")
            
            # Verificar coherencia científica
            print(f"\n🔬 COHERENCIA CIENTÍFICA:")
            
            # Para sitios históricos: origen >> actividad
            origin_activity_ratio = origin / (activity + 0.01)
            print(f"  Ratio origen/actividad: {origin_activity_ratio:.1f}x")
            if origin_activity_ratio > 3.0:
                print(f"  ✅ Coherente: origen >> actividad (sitio histórico)")
            else:
                print(f"  ⚠️ Ratio bajo: esperado >3x para sitio histórico")
            
            # Anomalía debe ser baja para sitios integrados al paisaje
            if anomaly < 0.05:
                print(f"  ✅ Coherente: anomalía baja (estructura integrada)")
            else:
                print(f"  ⚠️ Anomalía alta: inesperado para sitio histórico")
            
            # ESS debe estar presente
            ess = scientific.get('explanatory_strangeness', 'none')
            ess_score = scientific.get('strangeness_score', 0.0)
            print(f"  ESS: {ess} (score: {ess_score:.3f})")
            if ess in ['high', 'very_high']:
                print(f"  ✅ ESS activado correctamente")
            else:
                print(f"  ⚠️ ESS no activado (esperado para sitios históricos)")
            
            # Guardar resultado
            results.append({
                "name": test_case['name'],
                "status": "success",
                "metrics": {
                    "origin": origin,
                    "activity": activity,
                    "anomaly": anomaly,
                    "confidence": confidence
                },
                "validation": {
                    "origin_ok": origin_ok,
                    "activity_ok": activity_ok,
                    "anomaly_ok": anomaly_ok,
                    "ratio_ok": origin_activity_ratio > 3.0,
                    "ess_ok": ess in ['high', 'very_high']
                }
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "name": test_case['name'],
                "status": "error",
                "error": str(e)
            })
    
    # Resumen final
    print(f"\n{'='*80}")
    print("📊 RESUMEN FINAL")
    print(f"{'='*80}")
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    total_count = len(results)
    
    print(f"\nCasos ejecutados: {success_count}/{total_count}")
    
    if success_count > 0:
        # Verificar validaciones
        all_validations = []
        for r in results:
            if r['status'] == 'success':
                val = r['validation']
                all_validations.append(all(val.values()))
                
                print(f"\n{r['name']}:")
                print(f"  Origen:    {r['metrics']['origin']:.1%}")
                print(f"  Actividad: {r['metrics']['activity']:.1%}")
                print(f"  Anomalía:  {r['metrics']['anomaly']:.1%}")
                print(f"  Validación: {'✅ PASS' if all(val.values()) else '⚠️ PARTIAL'}")
        
        all_pass = all(all_validations)
        print(f"\n{'='*80}")
        if all_pass:
            print("✅ TODOS LOS CASOS PASARON")
        else:
            print("⚠️ ALGUNOS CASOS REQUIEREN AJUSTE")
        print(f"{'='*80}")
    
    return results

if __name__ == "__main__":
    results = test_separated_metrics()
    
    # Guardar resultados
    with open('separated_metrics_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Resultados guardados en: separated_metrics_test_results.json")
