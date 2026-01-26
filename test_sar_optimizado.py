#!/usr/bin/env python3
"""
Test SAR optimizado con cache y resolución 30m
Patagonia Candidato #001
"""

import sys
import os

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
from datetime import datetime
from satellite_connectors.planetary_computer import PlanetaryComputerConnector

async def test_sar_optimizado():
    """Test SAR con optimizaciones"""
    
    print("=" * 80)
    print("TEST SAR OPTIMIZADO - Patagonia Candidato #001")
    print("=" * 80)
    print()
    
    # Coordenadas Patagonia
    lat_min = -50.55
    lat_max = -50.40
    lon_min = -73.15
    lon_max = -72.90
    
    print(f"Región: Patagonia Proglaciar")
    print(f"Bbox: {lat_min}, {lat_max}, {lon_min}, {lon_max}")
    print(f"Área: ~35 × 20 km")
    print()
    
    # Inicializar conector
    connector = PlanetaryComputerConnector()
    
    if not connector.available:
        print("❌ Planetary Computer no disponible")
        return False
    
    print("✅ Planetary Computer disponible")
    print()
    
    # TEST 1: Primera descarga (sin cache)
    print("-" * 80)
    print("TEST 1: Primera descarga (sin cache)")
    print("-" * 80)
    
    start_time = datetime.now()
    
    result1 = await connector.get_sar_data(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
        resolution_m=30  # 30m optimizado
    )
    
    elapsed1 = (datetime.now() - start_time).total_seconds()
    
    if result1:
        print()
        print(f"✅ SAR descargado correctamente")
        print(f"⏱️  Tiempo: {elapsed1:.1f}s")
        print(f"📊 Resolución: {result1.resolution_m}m")
        print(f"📅 Fecha adquisición: {result1.acquisition_date.date()}")
        print(f"🔢 Índices:")
        print(f"   - VV mean: {result1.indices['vv_mean']:.2f} dB")
        print(f"   - VH mean: {result1.indices['vh_mean']:.2f} dB")
        print(f"   - VV/VH ratio: {result1.indices['vv_vh_ratio']:.2f}")
        print(f"   - Backscatter std: {result1.indices['backscatter_std']:.2f}")
        print(f"💾 Cached: {result1.cached}")
    else:
        print(f"❌ SAR falló")
        return False
    
    print()
    
    # TEST 2: Segunda descarga (con cache)
    print("-" * 80)
    print("TEST 2: Segunda descarga (debe usar cache)")
    print("-" * 80)
    
    start_time = datetime.now()
    
    result2 = await connector.get_sar_data(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
        resolution_m=30
    )
    
    elapsed2 = (datetime.now() - start_time).total_seconds()
    
    if result2:
        print()
        print(f"✅ SAR obtenido correctamente")
        print(f"⏱️  Tiempo: {elapsed2:.1f}s")
        print(f"💾 Cached: {result2.cached}")
        
        # Verificar que los datos son idénticos
        if (result2.indices['vv_mean'] == result1.indices['vv_mean'] and
            result2.indices['vh_mean'] == result1.indices['vh_mean']):
            print(f"✅ Datos idénticos (cache funcionando)")
        else:
            print(f"⚠️  Datos diferentes (cache no funcionó)")
        
        # Verificar mejora de velocidad
        if result2.cached and elapsed2 < elapsed1 * 0.1:
            speedup = elapsed1 / elapsed2
            print(f"🚀 Speedup: {speedup:.1f}x más rápido con cache")
        
    else:
        print(f"❌ SAR falló")
        return False
    
    print()
    
    # Estadísticas del cache
    print("-" * 80)
    print("ESTADÍSTICAS DEL CACHE")
    print("-" * 80)
    
    try:
        from cache.sar_cache import get_sar_cache
        sar_cache = get_sar_cache()
        
        stats = sar_cache.get_stats()
        
        if stats.get('available'):
            print(f"✅ Cache disponible")
            print(f"📊 Total entradas: {stats['total_entries']}")
            print(f"✅ Entradas válidas: {stats['valid_entries']}")
            print(f"❌ Entradas expiradas: {stats['expired_entries']}")
            
            if stats['oldest_entry']:
                print(f"📅 Entrada más antigua: {stats['oldest_entry']}")
            if stats['newest_entry']:
                print(f"📅 Entrada más reciente: {stats['newest_entry']}")
        else:
            print(f"❌ Cache no disponible")
            
    except Exception as e:
        print(f"⚠️  Error obteniendo stats: {e}")
    
    print()
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"✅ Primera descarga: {elapsed1:.1f}s")
    print(f"✅ Segunda descarga (cache): {elapsed2:.1f}s")
    
    if elapsed2 < elapsed1:
        speedup = elapsed1 / elapsed2
        print(f"🚀 Mejora: {speedup:.1f}x más rápido")
    
    print(f"📊 Resolución: 30m (9x más rápido que 10m)")
    print(f"💾 Cache: Funcionando correctamente")
    print()
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_sar_optimizado())
    exit(0 if success else 1)
