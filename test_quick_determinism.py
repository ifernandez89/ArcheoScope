"""
Test rápido de determinismo - sin input del usuario
"""

from backend.water.water_detector import WaterDetector
from backend.water.submarine_archaeology import SubmarineArchaeologyEngine

# Coordenadas de prueba
test_coords = [
    (18.5, -77.5, "Jamaica"),
    (25.511, -70.361, "Bermuda Triangle"),
]

detector = WaterDetector()
submarine_engine = SubmarineArchaeologyEngine()

for lat, lon, name in test_coords:
    print(f"\n{'='*80}")
    print(f"🔬 Probando: {name} ({lat}, {lon})")
    print('='*80)
    
    results = []
    
    for run in range(5):
        water_context = detector.detect_water_context(lat, lon)
        
        if not water_context:
            print(f"Run {run+1}: No water")
            results.append(0)
            continue
        
        bounds = {
            'lat_min': lat - 0.01,
            'lat_max': lat + 0.01,
            'lon_min': lon - 0.01,
            'lon_max': lon + 0.01
        }
        
        submarine_results = submarine_engine.analyze_submarine_area(water_context, bounds)
        num_candidates = len(submarine_results['wreck_candidates'])
        
        print(f"Run {run+1}: {num_candidates} candidatos")
        results.append(num_candidates)
    
    # Verificar
    if len(set(results)) == 1:
        print(f"\n✅ DETERMINÍSTICO: Siempre {results[0]} candidatos")
    else:
        print(f"\n❌ NO DETERMINÍSTICO: {results}")
        print(f"   Valores únicos: {set(results)}")
