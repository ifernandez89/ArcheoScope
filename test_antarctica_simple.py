#!/usr/bin/env python3
"""
Test simple de Antártida - solo análisis sin BD
"""

import requests
import json
from datetime import datetime

# Coordenadas
lat = -75.69969950817202
lon = -111.35296997427601

print("="*80)
print("TEST ANTARTIDA - ANALISIS SIMPLE")
print("="*80)
print()
print(f"Coordenadas: {lat}, {lon}")
print(f"Ubicacion: Antartida Occidental")
print()

# Crear bounding box
delta = 0.05
test_data = {
    "lat_min": lat - delta,
    "lat_max": lat + delta,
    "lon_min": lon - delta,
    "lon_max": lon + delta,
    "region_name": "Antartida Test"
}

print(f"Bounding box: [{test_data['lat_min']:.4f}, {test_data['lat_max']:.4f}] x [{test_data['lon_min']:.4f}, {test_data['lon_max']:.4f}]")
print()

try:
    print("Enviando request al backend...")
    start_time = datetime.now()
    
    response = requests.post(
        "http://localhost:8002/analyze",
        json=test_data,
        timeout=90
    )
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print(f"Status: {response.status_code}")
    print(f"Tiempo: {elapsed:.2f} segundos")
    print()
    
    if response.status_code == 200:
        result = response.json()
        
        # Guardar resultado
        output_file = f"antarctica_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print("="*80)
        print("RESULTADO")
        print("="*80)
        print()
        
        # Contexto espacial
        spatial = result.get('spatial_context', {})
        print("CONTEXTO ESPACIAL:")
        print(f"  Area: {spatial.get('area_km2', 0):.2f} km2")
        print(f"  Ambiente: {spatial.get('environment_type', 'N/A')}")
        print(f"  Confianza: {spatial.get('environment_confidence', 0):.2%}")
        print()
        
        # Resultados arqueológicos
        arch = result.get('archaeological_results', {})
        print("RESULTADOS ARQUEOLOGICOS:")
        print(f"  Tipo: {arch.get('result_type', 'N/A')}")
        print(f"  Probabilidad: {arch.get('archaeological_probability', 0):.2%}")
        print(f"  Confianza: {arch.get('confidence_level', 'N/A')}")
        print(f"  Mediciones: {arch.get('measurements_count', 0)}")
        print(f"  Convergencia: {arch.get('instruments_converging', 0)}/{arch.get('minimum_required', 0)}")
        print()
        
        # Instrumentos
        measurements = arch.get('measurements', [])
        if measurements:
            print(f"INSTRUMENTOS USADOS ({len(measurements)}):")
            for m in measurements:
                print(f"\n  {m.get('instrument_name', 'N/A')}:")
                print(f"    Valor: {m.get('value', 0):.3f} {m.get('unit', '')}")
                print(f"    Umbral: {m.get('threshold', 0):.3f}")
                print(f"    Excede: {'SI' if m.get('exceeds_threshold') else 'NO'}")
                print(f"    Confianza: {m.get('confidence', 'N/A')}")
        else:
            print("INSTRUMENTOS: Ninguno (0 mediciones)")
        
        print()
        print(f"Resultado guardado en: {output_file}")
        print()
        print("="*80)
        print("EXITO")
        print("="*80)
        
    else:
        print(f"ERROR: Status {response.status_code}")
        print(response.text[:500])

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
