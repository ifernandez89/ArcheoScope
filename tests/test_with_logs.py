"""
Test con logs detallados para encontrar el problema
"""

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

from backend.water.water_detector import WaterDetector
from backend.water.submarine_archaeology import SubmarineArchaeologyEngine

# Coordenadas que el usuario está probando
lat, lon = 18.5, -77.5

print(f"\n{'='*80}")
print(f"🔬 PRUEBA CON LOGS DETALLADOS")
print(f"📍 Coordenadas: {lat}, {lon}")
print('='*80)

detector = WaterDetector()
submarine_engine = SubmarineArchaeologyEngine()

for run in range(3):
    print(f"\n{'─'*80}")
    print(f"▶️ EJECUCIÓN #{run + 1}")
    print('─'*80)
    
    # Detectar agua
    water_context = detector.detect_water_context(lat, lon)
    
    print(f"\n💧 Contexto de agua:")
    print(f"   Tipo: {water_context.water_type.value}")
    print(f"   Profundidad: {water_context.estimated_depth_m:.1f}m")
    print(f"   Potencial: {water_context.archaeological_potential}")
    print(f"   Rutas históricas: {water_context.historical_shipping_routes}")
    print(f"   Naufragios conocidos: {water_context.known_wrecks_nearby}")
    
    # Calcular seed
    seed = int((abs(lat) * 1000 + abs(lon) * 1000) % 2147483647)
    print(f"\n🎲 Seed calculado: {seed}")
    
    # Calcular número esperado de anomalías
    if (water_context.historical_shipping_routes or water_context.known_wrecks_nearby):
        expected = 1 + (seed % 2)
        print(f"   Rutas históricas → num_anomalies = 1 + ({seed} % 2) = {expected}")
    elif water_context.archaeological_potential == "high":
        expected = 1
        print(f"   Potencial HIGH → num_anomalies = 1")
    elif water_context.archaeological_potential == "medium":
        expected = seed % 2
        print(f"   Potencial MEDIUM → num_anomalies = {seed} % 2 = {expected}")
    else:
        expected = 0
        print(f"   Potencial LOW → num_anomalies = 0")
    
    print(f"\n   ✅ Número esperado de anomalías: {expected}")
    
    # Analizar área submarina
    bounds = {
        'lat_min': lat - 0.01,
        'lat_max': lat + 0.01,
        'lon_min': lon - 0.01,
        'lon_max': lon + 0.01
    }
    
    submarine_results = submarine_engine.analyze_submarine_area(water_context, bounds)
    
    num_candidates = len(submarine_results['wreck_candidates'])
    print(f"\n🚢 Candidatos detectados: {num_candidates}")
    
    if num_candidates != expected:
        print(f"\n❌ ¡DISCREPANCIA! Esperado: {expected}, Obtenido: {num_candidates}")
    else:
        print(f"\n✅ CORRECTO: Coincide con lo esperado")
    
    if num_candidates > 0:
        print(f"\n📊 Detalles de candidatos:")
        for i, candidate in enumerate(submarine_results['wreck_candidates'], 1):
            sig = candidate['signature']
            print(f"   Candidato {i}:")
            print(f"      Dimensiones: {sig['length_m']:.1f}m x {sig['width_m']:.1f}m x {sig['height_m']:.1f}m")
            print(f"      Prioridad: {candidate['archaeological_priority']}")

print(f"\n{'='*80}")
print("FIN DE LA PRUEBA")
print('='*80)
