#!/usr/bin/env python3
"""
Test Antártida con captura completa de logs del backend
"""

import requests
import json
from datetime import datetime
import subprocess
import time
import sys

# Coordenadas
lat = -75.69969950817202
lon = -111.35296997427601

print("="*80)
print("TEST ANTARTIDA - CON LOGS COMPLETOS")
print("="*80)
print()
print(f"Coordenadas: {lat}, {lon}")
print()

# Crear bounding box
delta = 0.05
test_data = {
    "lat_min": lat - delta,
    "lat_max": lat + delta,
    "lon_min": lon - delta,
    "lon_max": lon + delta,
    "region_name": "Antartida Test - Logging"
}

print(f"Bounding box: [{test_data['lat_min']:.4f}, {test_data['lat_max']:.4f}] x [{test_data['lon_min']:.4f}, {test_data['lon_max']:.4f}]")
print()

try:
    print("Enviando request al backend...")
    print("(Los logs del backend aparecerán en la terminal del backend)")
    print()
    
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
        output_file = f"antarctica_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print("="*80)
        print("RESULTADO")
        print("="*80)
        print()
        
        # Mediciones
        measurements = result.get('instrumental_measurements', [])
        print(f"INSTRUMENTOS ({len(measurements)}):")
        for m in measurements:
            print(f"\n  {m.get('instrument', 'N/A')}:")
            print(f"    Valor: {m.get('value', 0):.3f} {m.get('unit', '')}")
            print(f"    Umbral: {m.get('threshold', 0):.3f}")
            print(f"    Excede: {'SÍ' if m.get('exceeds_threshold') else 'NO'}")
        
        print()
        print(f"Resultado guardado en: {output_file}")
        print()
        print("="*80)
        print("REVISA LOS LOGS DEL BACKEND PARA VER DETALLES DE CADA INSTRUMENTO")
        print("="*80)
        
    else:
        print(f"ERROR: Status {response.status_code}")
        print(response.text[:500])

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
