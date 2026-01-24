#!/usr/bin/env python3
"""
Explicación del sistema de seed y potencial arqueológico
"""

from backend.water.water_detector import WaterDetector

print("="*80)
print("🎓 EXPLICACIÓN DEL SISTEMA DE SEED Y POTENCIAL ARQUEOLÓGICO")
print("="*80)

wd = WaterDetector()

# Diferentes coordenadas para comparar
test_coords = [
    (25.511, -70.361, "Triángulo Bermudas"),
    (18.5, -77.5, "Jamaica"),
    (21.3, -157.9, "Pearl Harbor"),
    (40.5, -69.9, "Andrea Doria"),
    (41.7, -49.9, "Titanic"),
]

print("\n📍 ANÁLISIS DE DIFERENTES UBICACIONES:\n")

for lat, lon, name in test_coords:
    # Calcular seed
    seed = int((abs(lat) * 1000 + abs(lon) * 1000) % 2147483647)
    
    # Detectar contexto
    ctx = wd.detect_water_context(lat, lon)
    
    # Determinar número de anomalías según lógica
    if ctx.historical_shipping_routes or ctx.known_wrecks_nearby:
        num_anomalies = f"1-2 (rutas históricas)"
    elif ctx.archaeological_potential == "high":
        num_anomalies = "1 (siempre)"
    elif ctx.archaeological_potential == "medium":
        num_anomalies = f"{seed % 2} (seed % 2)"
    else:
        num_anomalies = "0 (bajo potencial)"
    
    print(f"📌 {name}")
    print(f"   Coordenadas: {lat}, {lon}")
    print(f"   Seed: {seed} ({'PAR' if seed % 2 == 0 else 'IMPAR'})")
    print(f"   Tipo agua: {ctx.water_type.value if ctx.water_type else 'N/A'}")
    print(f"   Profundidad: {ctx.estimated_depth_m:.0f}m" if ctx.estimated_depth_m else "   Profundidad: N/A")
    print(f"   Potencial: {ctx.archaeological_potential.upper()}")
    print(f"   Rutas históricas: {'SÍ' if ctx.historical_shipping_routes else 'NO'}")
    print(f"   Naufragios cerca: {'SÍ' if ctx.known_wrecks_nearby else 'NO'}")
    print(f"   → Anomalías generadas: {num_anomalies}")
    print()

print("="*80)
print("🔑 RESUMEN DEL SISTEMA:")
print("="*80)
print("""
1. SEED = Número único calculado de coordenadas
   • Fórmula: (lat*1000 + lon*1000) % 2147483647
   • Garantiza consistencia: mismas coords → mismo seed

2. POTENCIAL ARQUEOLÓGICO = Evaluación del contexto
   • HIGH: Ríos, costas, mares, rutas históricas
   • MEDIUM: Océano profundo sin rutas conocidas
   • LOW: Océano muy profundo o áreas remotas

3. NÚMERO DE ANOMALÍAS = Decisión determinística
   • Rutas históricas: 1-2 anomalías (1 + seed%2)
   • HIGH: 1 anomalía (siempre)
   • MEDIUM: 0-1 anomalía (seed%2)
   • LOW: 0 anomalías

4. ¿POR QUÉ seed % 2?
   • Seed PAR (95872) → 95872 % 2 = 0 → 0 anomalías
   • Seed IMPAR (95873) → 95873 % 2 = 1 → 1 anomalía
   • Introduce variación realista pero DETERMINÍSTICA
""")
print("="*80)
