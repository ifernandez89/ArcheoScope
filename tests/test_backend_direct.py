"""
Test directo del backend para verificar determinismo
"""

from backend.water.water_detector import WaterDetector
from backend.water.submarine_archaeology import SubmarineArchaeologyEngine

def test_same_coordinates_multiple_times():
    """Probar las mismas coordenadas 10 veces"""
    
    # Usa las coordenadas que estás probando
    lat = float(input("Ingresa latitud: "))
    lon = float(input("Ingresa longitud: "))
    
    print(f"\n🔬 Probando coordenadas: {lat}, {lon}")
    print("="*80)
    
    detector = WaterDetector()
    submarine_engine = SubmarineArchaeologyEngine()
    
    results = []
    
    for run in range(10):
        print(f"\n▶️ Ejecución {run + 1}/10")
        
        # Detectar agua
        water_context = detector.detect_water_context(lat, lon)
        
        if not water_context:
            print("   ❌ No es agua")
            results.append({'candidates': 0, 'water': False})
            continue
        
        print(f"   💧 Agua detectada: {water_context.water_type.value}")
        print(f"   📏 Profundidad: {water_context.estimated_depth_m:.1f}m")
        print(f"   🎯 Potencial: {water_context.archaeological_potential}")
        
        # Analizar área submarina
        bounds = {
            'lat_min': lat - 0.01,
            'lat_max': lat + 0.01,
            'lon_min': lon - 0.01,
            'lon_max': lon + 0.01
        }
        
        submarine_results = submarine_engine.analyze_submarine_area(water_context, bounds)
        
        num_candidates = len(submarine_results['wreck_candidates'])
        print(f"   🚢 Candidatos detectados: {num_candidates}")
        
        if num_candidates > 0:
            for i, candidate in enumerate(submarine_results['wreck_candidates'], 1):
                sig = candidate['signature']
                print(f"      Candidato {i}: {sig['length_m']:.1f}m x {sig['width_m']:.1f}m x {sig['height_m']:.1f}m")
        
        results.append({
            'candidates': num_candidates,
            'water': True,
            'depth': water_context.estimated_depth_m,
            'potential': water_context.archaeological_potential
        })
    
    # Verificar consistencia
    print("\n" + "="*80)
    print("📊 ANÁLISIS DE RESULTADOS")
    print("="*80)
    
    candidate_counts = [r['candidates'] for r in results]
    unique_counts = set(candidate_counts)
    
    print(f"\nNúmero de candidatos por ejecución:")
    for i, count in enumerate(candidate_counts, 1):
        print(f"   Ejecución {i}: {count} candidatos")
    
    print(f"\nValores únicos encontrados: {sorted(unique_counts)}")
    
    if len(unique_counts) == 1:
        print("\n✅ ¡ÉXITO! Sistema 100% DETERMINÍSTICO")
        print(f"   Siempre produce: {candidate_counts[0]} candidatos")
    else:
        print("\n❌ ¡FALLO! Sistema NO es determinístico")
        print(f"   Produce valores diferentes: {sorted(unique_counts)}")
        print("\n🔍 Distribución:")
        for count in sorted(unique_counts):
            occurrences = candidate_counts.count(count)
            print(f"   {count} candidatos: {occurrences} veces ({occurrences*10}%)")

if __name__ == "__main__":
    test_same_coordinates_multiple_times()
