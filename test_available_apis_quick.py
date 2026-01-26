#!/usr/bin/env python3
"""
Test Rápido de APIs Disponibles - ArcheoScope
Solo prueba las APIs que NO requieren autenticación
"""

import asyncio
import time
import json
from datetime import datetime
from typing import Dict, Any
import sys
import os

# Agregar backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from satellite_connectors.planetary_computer import PlanetaryComputerConnector
from satellite_connectors.palsar_connector import PALSARConnector
from satellite_connectors.smap_connector import SMAPConnector
from satellite_connectors.nsidc_connector import NSIDCConnector


async def test_api(name: str, test_func, timeout_s: int = 30):
    """Probar una API con timeout"""
    
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {name}")
    print(f"{'='*60}")
    
    result = {
        'api_name': name,
        'tested_at': datetime.now().isoformat(),
        'success': False,
        'response_time_s': None,
        'error': None,
        'data_received': False
    }
    
    try:
        print(f"📡 Conectando a {name}...")
        start_time = time.time()
        
        # Ejecutar con timeout
        data = await asyncio.wait_for(test_func(), timeout=timeout_s)
        
        response_time = time.time() - start_time
        result['response_time_s'] = round(response_time, 2)
        
        if data:
            result['success'] = True
            result['data_received'] = True
            
            print(f"✅ {name} - OK")
            print(f"   Tiempo de respuesta: {response_time:.2f}s")
            print(f"   Datos recibidos: ✅")
        else:
            result['error'] = 'No data returned'
            print(f"⚠️  {name} - Sin datos")
    
    except asyncio.TimeoutError:
        result['error'] = f'Timeout after {timeout_s}s'
        print(f"⏱️  {name} - Timeout ({timeout_s}s)")
    
    except Exception as e:
        result['error'] = str(e)
        print(f"❌ {name} - Error: {e}")
    
    return result


async def main():
    """Ejecutar tests rápidos"""
    
    print("\n" + "="*60)
    print("🚀 TEST RÁPIDO DE APIS DISPONIBLES")
    print("="*60)
    print("Solo probando APIs que NO requieren autenticación")
    
    results = []
    
    # Coordenadas de prueba: Giza
    test_coords = {
        'lat_min': 29.97,
        'lat_max': 29.98,
        'lon_min': 31.13,
        'lon_max': 31.14
    }
    
    print(f"\nCoordenadas: Giza Pyramids")
    print(f"Lat: {test_coords['lat_min']}-{test_coords['lat_max']}")
    print(f"Lon: {test_coords['lon_min']}-{test_coords['lon_max']}")
    
    # 1. Planetary Computer - Sentinel-2
    pc = PlanetaryComputerConnector()
    result = await test_api(
        "Planetary Computer - Sentinel-2",
        lambda: pc.get_multispectral_data(**test_coords),
        timeout_s=45
    )
    results.append(result)
    
    # 2. Planetary Computer - Sentinel-1
    result = await test_api(
        "Planetary Computer - Sentinel-1 SAR",
        lambda: pc.get_sar_data(**test_coords),
        timeout_s=45
    )
    results.append(result)
    
    # 3. Planetary Computer - Landsat
    result = await test_api(
        "Planetary Computer - Landsat Thermal",
        lambda: pc.get_thermal_data(**test_coords),
        timeout_s=45
    )
    results.append(result)
    
    # 4. NSIDC (no requiere coordenadas específicas)
    nsidc = NSIDCConnector()
    result = await test_api(
        "NSIDC Ice Extent",
        lambda: nsidc.get_ice_extent_timeseries(
            hemisphere="north",
            start_year=2022,
            end_year=2023
        ),
        timeout_s=30
    )
    results.append(result)
    
    # 5. PALSAR
    palsar = PALSARConnector()
    result = await test_api(
        "PALSAR L-band",
        lambda: palsar.get_lband_data(**test_coords),
        timeout_s=30
    )
    results.append(result)
    
    # 6. SMAP
    smap = SMAPConnector()
    result = await test_api(
        "SMAP Soil Moisture",
        lambda: smap.get_soil_moisture(**test_coords),
        timeout_s=30
    )
    results.append(result)
    
    # Generar resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE TESTS")
    print("="*60)
    
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    failed = total - successful
    
    print(f"\nAPIs Probadas: {total}")
    print(f"APIs Exitosas: {successful} ✅")
    print(f"APIs Fallidas: {failed} ❌")
    print(f"Tasa de Éxito: {(successful/total*100):.1f}%")
    
    # Calcular tiempo promedio
    response_times = [r['response_time_s'] for r in results if r['response_time_s']]
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        print(f"Tiempo Promedio: {avg_time:.2f}s")
    
    print("\n" + "-"*60)
    print("DETALLE POR API")
    print("-"*60)
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        time_str = f"{result['response_time_s']:.2f}s" if result['response_time_s'] else "N/A"
        
        print(f"{status} {result['api_name']:<45} {time_str:>8}")
        
        if result['error']:
            print(f"   Error: {result['error']}")
    
    print("\n" + "="*60)
    
    if successful >= 3:
        print("✅ Sistema funcional con datos reales")
    elif successful > 0:
        print("⚠️  Sistema parcialmente funcional")
    else:
        print("❌ Sistema no funcional")
    
    print("="*60)
    
    # Guardar reporte
    report = {
        'test_date': datetime.now().isoformat(),
        'test_type': 'quick_available_apis',
        'summary': {
            'total_apis': total,
            'successful_apis': successful,
            'failed_apis': failed,
            'success_rate': (successful/total*100) if total > 0 else 0,
            'avg_response_time_s': round(avg_time, 2) if response_times else None
        },
        'apis': results
    }
    
    filename = f"api_test_quick_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Reporte guardado: {filename}")
    
    return 0 if successful >= 3 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
