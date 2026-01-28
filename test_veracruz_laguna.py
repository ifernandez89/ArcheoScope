#!/usr/bin/env python3
"""
Test: Zona de laguna en Veracruz
Centro: 20.58, -96.92
Radio: ~10 km
Resolución: 120m

Buscando:
- Bordes de laguna
- Cambios NDVI bruscos
- Zonas donde SAR pierde coherencia
"""

import requests
import json
from datetime import datetime

# Coordenadas: Centro 20.58, -96.92 con radio ~10km
# Esto da aproximadamente 0.09 grados en cada dirección
CENTER_LAT = 20.58
CENTER_LON = -96.92
RADIUS_DEG = 0.09  # ~10 km

lat_min = CENTER_LAT - RADIUS_DEG
lat_max = CENTER_LAT + RADIUS_DEG
lon_min = CENTER_LON - RADIUS_DEG
lon_max = CENTER_LON + RADIUS_DEG

print("="*80)
print("🔬 TEST: ZONA LAGUNA VERACRUZ")
print("="*80)
print(f"Centro: {CENTER_LAT}, {CENTER_LON}")
print(f"Bbox: [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
print(f"Área: ~{(RADIUS_DEG * 111) * 2:.1f} km x {(RADIUS_DEG * 111) * 2:.1f} km")
print("="*80)

test_data = {
    "lat_min": lat_min,
    "lat_max": lat_max,
    "lon_min": lon_min,
    "lon_max": lon_max,
    "region_name": "Laguna Veracruz - Zona Transición"
}

print("\n📡 Enviando solicitud al backend...")
print(f"POST http://localhost:8002/api/scientific/analyze")

try:
    response = requests.post(
        "http://localhost:8002/api/scientific/analyze",
        json=test_data,
        timeout=180  # 3 minutos
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n" + "="*80)
        print("✅ ANÁLISIS COMPLETADO")
        print("="*80)
        
        # Extraer datos clave
        tomo = result.get('tomographic_profile', {})
        coverage = tomo.get('instrumental_coverage', {})
        
        print("\n📊 COBERTURA INSTRUMENTAL:")
        for layer_type, data in coverage.items():
            successful = data.get('successful', 0)
            total = data.get('total', 0)
            percentage = data.get('percentage', 0)
            print(f"  {layer_type:15s}: {successful}/{total} ({percentage:.0f}%)")
        
        print("\n📊 MÉTRICAS ESS:")
        print(f"  ESS Superficial:     {tomo.get('ess_superficial', 0):.3f}")
        print(f"  ESS Volumétrico:     {tomo.get('ess_volumetrico', 0):.3f}")
        print(f"  ESS Temporal:        {tomo.get('ess_temporal', 0):.3f}")
        print(f"  Coherencia 3D:       {tomo.get('coherencia_3d', 0):.3f}")
        
        print("\n🎯 RESULTADO CIENTÍFICO:")
        sci_output = result.get('scientific_output', {})
        print(f"  Anomaly Score:       {sci_output.get('anomaly_score', 0):.3f}")
        print(f"  Prob. Antropogénica: {sci_output.get('anthropic_probability', 0):.3f}")
        print(f"  Tipo:                {sci_output.get('candidate_type', 'unknown')}")
        print(f"  Acción:              {sci_output.get('recommended_action', 'unknown')}")
        
        print("\n📝 EXPLICACIÓN:")
        explanation = sci_output.get('scientific_explanation', 'No disponible')
        print(f"  {explanation[:200]}...")
        
        # Instrumentos medidos
        measurements = result.get('instrumental_measurements', [])
        successful_instruments = [m for m in measurements if m.get('success')]
        failed_instruments = [m for m in measurements if not m.get('success')]
        
        print(f"\n🛰️ INSTRUMENTOS:")
        print(f"  Exitosos: {len(successful_instruments)}/{len(measurements)}")
        
        if successful_instruments:
            print("\n  ✅ Exitosos:")
            for m in successful_instruments[:10]:  # Primeros 10
                print(f"    - {m.get('instrument_name'):25s}: {m.get('value'):.3f} (conf: {m.get('confidence'):.2f})")
        
        if failed_instruments:
            print(f"\n  ❌ Fallidos: {len(failed_instruments)}")
            for m in failed_instruments[:5]:  # Primeros 5
                print(f"    - {m.get('instrument_name'):25s}: {m.get('data_mode', 'NO_DATA')}")
        
        # Guardar resultado completo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"veracruz_laguna_result_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultado completo guardado en: {filename}")
        
        print("\n" + "="*80)
        print("🎉 TEST COMPLETADO")
        print("="*80)
        
    else:
        print(f"\n❌ Error HTTP {response.status_code}")
        print(response.text[:500])
        
except requests.exceptions.Timeout:
    print("\n⏰ TIMEOUT - El análisis tomó más de 3 minutos")
except Exception as e:
    print(f"\n💥 ERROR: {e}")
    import traceback
    traceback.print_exc()
