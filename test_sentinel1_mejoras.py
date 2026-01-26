#!/usr/bin/env python3
"""
Test de mejoras Sentinel-1 SAR
Fecha: 2026-01-26

MEJORAS IMPLEMENTADAS:
1. Ventana temporal ampliada: 30 → 90 días
2. Fallback a colección sentinel-1-grd
3. Logging detallado a archivo

REGIONES DE TEST:
1. Antártida (-75.7°S, -111.4°W) - Región polar, modo EW
2. Patagonia (-50.2°S, -72.3°W) - Región no-polar, modo IW
"""

import asyncio
import sys
from pathlib import Path

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from satellite_connectors.planetary_computer import PlanetaryComputerConnector

async def test_sentinel1_antarctica():
    """Test Sentinel-1 en Antártida con mejoras"""
    
    print("="*80)
    print("TEST 1: SENTINEL-1 SAR - ANTÁRTIDA")
    print("="*80)
    print("Coordenadas: -75.6997°S, -111.3530°W (West Antarctica)")
    print("Modo esperado: EW (Extra Wide para polos)")
    print("Ventana temporal: 90 días")
    print("="*80)
    
    connector = PlanetaryComputerConnector()
    
    if not connector.available:
        print("❌ Planetary Computer no disponible")
        return False
    
    # Antártida
    lat_min, lat_max = -75.75, -75.65
    lon_min, lon_max = -111.45, -111.25
    
    print("\n🔍 Iniciando búsqueda SAR...")
    
    try:
        data = await connector.get_sar_data(
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max
        )
        
        if data:
            print("\n✅ ÉXITO - Datos SAR obtenidos")
            print(f"   Fuente: {data.source}")
            print(f"   Fecha: {data.acquisition_date.date()}")
            print(f"   VV mean: {data.indices['vv_mean']:.2f} dB")
            print(f"   VH mean: {data.indices['vh_mean']:.2f} dB")
            print(f"   Tiempo: {data.processing_time_s:.2f}s")
            return True
        else:
            print("\n❌ FALLO - No se obtuvieron datos SAR")
            print("   Ver instrument_diagnostics.log para detalles")
            return False
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_sentinel1_patagonia():
    """Test Sentinel-1 en Patagonia (control positivo)"""
    
    print("\n" + "="*80)
    print("TEST 2: SENTINEL-1 SAR - PATAGONIA")
    print("="*80)
    print("Coordenadas: -50.2°S, -72.3°W (Lago Argentino)")
    print("Modo esperado: IW (Interferometric Wide)")
    print("Ventana temporal: 90 días")
    print("="*80)
    
    connector = PlanetaryComputerConnector()
    
    # Patagonia
    lat_min, lat_max = -50.3, -50.1
    lon_min, lon_max = -72.4, -72.2
    
    print("\n🔍 Iniciando búsqueda SAR...")
    
    try:
        data = await connector.get_sar_data(
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max
        )
        
        if data:
            print("\n✅ ÉXITO - Datos SAR obtenidos")
            print(f"   Fuente: {data.source}")
            print(f"   Fecha: {data.acquisition_date.date()}")
            print(f"   VV mean: {data.indices['vv_mean']:.2f} dB")
            print(f"   VH mean: {data.indices['vh_mean']:.2f} dB")
            print(f"   Tiempo: {data.processing_time_s:.2f}s")
            return True
        else:
            print("\n❌ FALLO - No se obtuvieron datos SAR")
            print("   Ver instrument_diagnostics.log para detalles")
            return False
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Ejecutar todos los tests"""
    
    print("\n" + "🛰️ "*20)
    print("TEST DE MEJORAS SENTINEL-1 SAR")
    print("Fecha: 2026-01-26")
    print("🛰️ "*20 + "\n")
    
    # Limpiar log anterior
    try:
        with open('instrument_diagnostics.log', 'w', encoding='utf-8') as f:
            f.write("=== TEST SENTINEL-1 MEJORAS 2026-01-26 ===\n\n")
    except:
        pass
    
    results = []
    
    # Test 1: Antártida
    result1 = await test_sentinel1_antarctica()
    results.append(("Antártida", result1))
    
    # Test 2: Patagonia
    result2 = await test_sentinel1_patagonia()
    results.append(("Patagonia", result2))
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE TESTS")
    print("="*80)
    
    for region, success in results:
        status = "✅ ÉXITO" if success else "❌ FALLO"
        print(f"{region:20s} {status}")
    
    total = len(results)
    passed = sum(1 for _, s in results if s)
    
    print(f"\nTotal: {passed}/{total} tests exitosos ({passed/total*100:.0f}%)")
    
    print("\n📋 Ver detalles completos en: instrument_diagnostics.log")
    print("="*80)
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
