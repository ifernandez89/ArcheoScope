#!/usr/bin/env python3
"""
Test de Velocidad - ArcheoScope con Timeouts Optimizados
=========================================================

Prueba la velocidad de respuesta del sistema con diferentes regiones.
"""

import requests
import time
import json
from datetime import datetime

API_BASE = 'http://localhost:8002'

# Regiones de prueba
test_regions = [
    {
        'name': 'Petén, Guatemala (pequeña)',
        'lat_min': 16.0,
        'lat_max': 16.1,
        'lon_min': -90.0,
        'lon_max': -89.9
    },
    {
        'name': 'Giza, Egipto (pequeña)',
        'lat_min': 29.9,
        'lat_max': 30.0,
        'lon_min': 31.1,
        'lon_max': 31.2
    },
    {
        'name': 'Angkor, Camboya (pequeña)',
        'lat_min': 13.4,
        'lat_max': 13.5,
        'lon_min': 103.8,
        'lon_max': 103.9
    }
]

print("="*80)
print("⏱️  TEST DE VELOCIDAD - ARCHEOSCOPE")
print("="*80)
print()
print("Configuración:")
print("  • Timeout API: 5 segundos")
print("  • Connect timeout: 3 segundos")
print("  • Max retries: 1")
print()
print("="*80)
print()

results = []

for i, region in enumerate(test_regions, 1):
    print(f"🔍 Test {i}/{len(test_regions)}: {region['name']}")
    print(f"   Coordenadas: [{region['lat_min']}, {region['lat_max']}] x [{region['lon_min']}, {region['lon_max']}]")
    
    # Preparar request
    payload = {
        'lat_min': region['lat_min'],
        'lat_max': region['lat_max'],
        'lon_min': region['lon_min'],
        'lon_max': region['lon_max'],
        'region_name': region['name'],
        'resolution_m': 1000
    }
    
    # Medir tiempo
    start_time = time.time()
    
    try:
        response = requests.post(
            f'{API_BASE}/analyze',
            json=payload,
            timeout=30  # Timeout del cliente (más alto que el del servidor)
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            # Extraer información clave
            result_type = data.get('archaeological_results', {}).get('result_type', 'unknown')
            confidence = data.get('archaeological_results', {}).get('confidence', 0)
            ai_available = data.get('ai_explanations', {}).get('ai_available', False)
            
            print(f"   ✅ Respuesta en {elapsed:.2f}s")
            print(f"   📊 Resultado: {result_type} (confianza: {confidence:.2%})")
            print(f"   🤖 IA: {'✅' if ai_available else '❌'}")
            
            results.append({
                'region': region['name'],
                'time': elapsed,
                'status': 'success',
                'result_type': result_type,
                'confidence': confidence
            })
            
        else:
            elapsed = time.time() - start_time
            print(f"   ❌ Error HTTP {response.status_code} en {elapsed:.2f}s")
            results.append({
                'region': region['name'],
                'time': elapsed,
                'status': f'error_{response.status_code}'
            })
            
    except requests.Timeout:
        elapsed = time.time() - start_time
        print(f"   ⏱️  TIMEOUT después de {elapsed:.2f}s")
        results.append({
            'region': region['name'],
            'time': elapsed,
            'status': 'timeout'
        })
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"   ❌ Error: {e} ({elapsed:.2f}s)")
        results.append({
            'region': region['name'],
            'time': elapsed,
            'status': 'error',
            'error': str(e)
        })
    
    print()

# Resumen
print("="*80)
print("📊 RESUMEN DE VELOCIDAD")
print("="*80)
print()

successful = [r for r in results if r['status'] == 'success']
timeouts = [r for r in results if r['status'] == 'timeout']
errors = [r for r in results if r['status'].startswith('error')]

print(f"Total pruebas: {len(results)}")
print(f"  ✅ Exitosas: {len(successful)}")
print(f"  ⏱️  Timeouts: {len(timeouts)}")
print(f"  ❌ Errores: {len(errors)}")
print()

if successful:
    times = [r['time'] for r in successful]
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"⏱️  TIEMPOS DE RESPUESTA:")
    print(f"   Promedio: {avg_time:.2f}s")
    print(f"   Mínimo: {min_time:.2f}s")
    print(f"   Máximo: {max_time:.2f}s")
    print()
    
    # Clasificación de velocidad
    if avg_time < 5:
        print("   🚀 EXCELENTE - Sistema muy rápido")
    elif avg_time < 10:
        print("   ✅ BUENO - Velocidad aceptable")
    elif avg_time < 20:
        print("   ⚠️  LENTO - Considerar optimizaciones")
    else:
        print("   ❌ MUY LENTO - Requiere optimización urgente")

print()
print("="*80)

# Guardar resultados
output_file = f"speed_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'test_date': datetime.now().isoformat(),
        'configuration': {
            'api_timeout': 5,
            'connect_timeout': 3,
            'max_retries': 1
        },
        'results': results,
        'summary': {
            'total': len(results),
            'successful': len(successful),
            'timeouts': len(timeouts),
            'errors': len(errors),
            'avg_time': avg_time if successful else None,
            'min_time': min_time if successful else None,
            'max_time': max_time if successful else None
        }
    }, f, indent=2, ensure_ascii=False)

print(f"💾 Resultados guardados en: {output_file}")
print()
