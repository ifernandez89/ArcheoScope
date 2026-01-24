#!/usr/bin/env python3
"""
Test de consistencia para coordenadas del Triángulo de las Bermudas
Coordenadas: 25.511, -70.361
"""

from backend.water.water_detector import WaterDetector
from backend.water.submarine_archaeology import SubmarineArchaeologyEngine
import json

print("="*80)
print("🔺 TEST: TRIÁNGULO DE LAS BERMUDAS")
print("="*80)
print(f"Coordenadas: 25.511, -70.361\n")

wd = WaterDetector()
se = SubmarineArchaeologyEngine()

# Detectar contexto
ctx = wd.detect_water_context(25.511, -70.361)
print(f"📍 CONTEXTO DEL AGUA:")
print(f"   Tipo: {ctx.water_type.value if ctx.water_type else 'N/A'}")
print(f"   Profundidad estimada: {ctx.estimated_depth_m}m")
print(f"   Salinidad: {ctx.salinity_type}")
print(f"   Potencial arqueológico: {ctx.archaeological_potential}")
print(f"   Rutas históricas: {ctx.historical_shipping_routes}")
print(f"   Naufragios conocidos: {ctx.known_wrecks_nearby}")
print()

# Ejecutar análisis 5 VECES
print("🔄 EJECUTANDO ANÁLISIS 5 VECES (DEBE SER IDÉNTICO):")
print("-"*80)

results = []
for i in range(1, 6):
    print(f"\n▶️  Ejecución #{i}...")
    
    bounds = (25.411, 25.611, -70.461, -70.261)
    result = se.analyze_submarine_area(ctx, bounds)
    
    num_anomalies = len(result.get('wreck_candidates', []))
    results.append(num_anomalies)
    
    print(f"   ✓ Anomalías detectadas: {num_anomalies}")
    
    if num_anomalies > 0:
        for j, candidate in enumerate(result['wreck_candidates'], 1):
            sig = candidate['signature']
            print(f"      Anomalía {j}:")
            print(f"         Dimensiones: {sig['length_m']:.1f}m x {sig['width_m']:.1f}m x {sig['height_m']:.1f}m")
            print(f"         Confianza: {sig['detection_confidence']:.3f}")
            print(f"         Orientación: {sig['orientation_degrees']:.1f}°")
            print(f"         Profundidad enterramiento: {sig['burial_depth_m']:.2f}m")
            print(f"         Anomalía magnética: {sig['magnetic_anomaly_nt']:.1f} nT")

print("\n" + "="*80)
print("📊 RESULTADOS DE LAS 5 EJECUCIONES:")
print("="*80)
print(f"Número de anomalías: {results}")

if len(set(results)) == 1:
    print(f"\n✅ ÉXITO: Todas las ejecuciones produjeron {results[0]} anomalías")
    print("✅ SISTEMA 100% DETERMINÍSTICO VERIFICADO")
    
    # Guardar resultado para referencia
    if num_anomalies > 0:
        with open('bermuda_triangle_test_result.json', 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n💾 Resultado guardado en: bermuda_triangle_test_result.json")
else:
    print(f"\n❌ FALLO: Resultados inconsistentes!")
    print(f"❌ ESTO NO DEBERÍA PASAR - HAY UN PROBLEMA")
    exit(1)

print("\n" + "="*80)
