"""
Test con las coordenadas EXACTAS que el usuario está usando
"""

from backend.water.water_detector import WaterDetector
from backend.water.submarine_archaeology import SubmarineArchaeologyEngine

detector = WaterDetector()
engine = SubmarineArchaeologyEngine()

# Coordenadas EXACTAS del usuario
lat, lon = 25.511, -70.361

print(f"\n🔬 Probando coordenadas EXACTAS: {lat}, {lon}")
print("="*80)

for run in range(5):
    print(f"\n▶️ Ejecución {run + 1}/5")
    
    water = detector.detect_water_context(lat, lon)
    print(f"   Potencial: {water.archaeological_potential}")
    print(f"   Profundidad: {water.estimated_depth_m:.1f}m")
    print(f"   Rutas históricas: {water.historical_shipping_routes}")
    
    # Bounds que usa el frontend
    bounds = {
        'lat_min': lat - 0.005,
        'lat_max': lat + 0.005,
        'lon_min': lon - 0.005,
        'lon_max': lon + 0.005
    }
    
    result = engine.analyze_submarine_area(water, bounds)
    num_candidates = len(result['wreck_candidates'])
    
    print(f"   🚢 Candidatos: {num_candidates}")
    
    if num_candidates > 0:
        for i, candidate in enumerate(result['wreck_candidates'], 1):
            sig = candidate['signature']
            print(f"      Candidato {i}: {sig['length_m']:.1f}m x {sig['width_m']:.1f}m")

print(f"\n{'='*80}")
print("FIN")
