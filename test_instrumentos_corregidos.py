#!/usr/bin/env python3
"""
Test de Instrumentos Corregidos
================================

Verifica las correcciones aplicadas a:
1. PALSAR - Retorna InstrumentMeasurement, bug en _select_best_scene corregido
2. MODIS LST - Timeout aumentado a 120s
3. OpenTopography - Timeout aumentado a 120s

Fecha: 2026-01-29
"""

import asyncio
import sys
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from satellite_connectors.palsar_connector import PALSARConnector
from satellite_connectors.modis_lst_connector import MODISLSTConnector
from satellite_connectors.opentopography_connector import OpenTopographyConnector
from instrument_contract import InstrumentMeasurement


async def test_palsar():
    """Test PALSAR con InstrumentMeasurement"""
    
    print("\n" + "="*80)
    print("TEST 1: PALSAR-2 Connector")
    print("="*80)
    
    connector = PALSARConnector()
    
    # Test región pequeña (Tiwanaku, Bolivia)
    print("\n📡 Test: PALSAR backscatter (Tiwanaku)")
    result = await connector.get_sar_backscatter(
        lat_min=-16.56,
        lat_max=-16.55,
        lon_min=-68.68,
        lon_max=-68.67,
        polarization='HH'
    )
    
    if result:
        print(f"   ✅ Tipo: {type(result).__name__}")
        print(f"   ✅ Es InstrumentMeasurement: {isinstance(result, InstrumentMeasurement)}")
        print(f"   ✅ Status: {result.status.value}")
        print(f"   ✅ Value: {result.value}")
        print(f"   ✅ Unit: {result.unit}")
        print(f"   ✅ Confidence: {result.confidence}")
        print(f"   ✅ Usable: {result.is_usable()}")
        
        if result.is_usable():
            print(f"   📊 Backscatter: {result.value:.2f} {result.unit}")
            print(f"   📊 Source: {result.source}")
    else:
        print("   ❌ No result")
    
    # Test penetración forestal
    print("\n📡 Test: PALSAR forest penetration")
    result2 = await connector.get_forest_penetration(
        lat_min=-16.56,
        lat_max=-16.55,
        lon_min=-68.68,
        lon_max=-68.67
    )
    
    if result2:
        print(f"   ✅ Tipo: {type(result2).__name__}")
        print(f"   ✅ Status: {result2.status.value}")
        print(f"   ✅ Usable: {result2.is_usable()}")
    else:
        print("   ❌ No result")
    
    # Test humedad del suelo
    print("\n📡 Test: PALSAR soil moisture")
    result3 = await connector.get_soil_moisture(
        lat_min=-16.56,
        lat_max=-16.55,
        lon_min=-68.68,
        lon_max=-68.67
    )
    
    if result3:
        print(f"   ✅ Tipo: {type(result3).__name__}")
        print(f"   ✅ Status: {result3.status.value}")
        print(f"   ✅ Usable: {result3.is_usable()}")
    else:
        print("   ❌ No result")
    
    return result is not None


async def test_modis_lst():
    """Test MODIS LST con timeout aumentado"""
    
    print("\n" + "="*80)
    print("TEST 2: MODIS LST Connector (timeout 120s)")
    print("="*80)
    
    connector = MODISLSTConnector()
    
    if not connector.available:
        print("   ⚠️ MODIS LST no disponible (credenciales faltantes)")
        return False
    
    # Test región templada (Roma)
    print("\n🌡️ Test: MODIS LST (Roma)")
    result = await connector.get_land_surface_temperature(
        lat_min=41.8,
        lat_max=41.9,
        lon_min=12.4,
        lon_max=12.5
    )
    
    if result:
        print(f"   ✅ Tipo: {type(result).__name__}")
        print(f"   ✅ Data mode: {result.get('data_mode', 'N/A')}")
        print(f"   ✅ LST día: {result.get('lst_day_celsius', 'N/A'):.1f}°C")
        print(f"   ✅ LST noche: {result.get('lst_night_celsius', 'N/A'):.1f}°C")
        print(f"   ✅ Inercia térmica: {result.get('thermal_inertia', 'N/A'):.1f}K")
        print(f"   📊 Source: {result.get('source', 'N/A')}")
    else:
        print("   ❌ No result")
    
    return result is not None


async def test_opentopography():
    """Test OpenTopography con timeout aumentado"""
    
    print("\n" + "="*80)
    print("TEST 3: OpenTopography Connector (timeout 120s)")
    print("="*80)
    
    connector = OpenTopographyConnector()
    
    if not connector.available:
        print("   ⚠️ OpenTopography no disponible (API key faltante)")
        return False
    
    # Test región pequeña (Tiwanaku)
    print("\n🌍 Test: OpenTopography DEM (Tiwanaku)")
    result = await connector.get_elevation_data(
        lat_min=-16.56,
        lat_max=-16.55,
        lon_min=-68.68,
        lon_max=-68.67,
        dem_type='SRTMGL1'
    )
    
    if result:
        print(f"   ✅ Tipo: {type(result).__name__}")
        print(f"   ✅ Es InstrumentMeasurement: {isinstance(result, InstrumentMeasurement)}")
        print(f"   ✅ Status: {result.status.value}")
        print(f"   ✅ Value (rugosity): {result.value}")
        print(f"   ✅ Unit: {result.unit}")
        print(f"   ✅ Confidence: {result.confidence}")
        print(f"   ✅ Usable: {result.is_usable()}")
        
        if result.is_usable():
            print(f"   📊 Rugosity: {result.value:.3f}")
            print(f"   📊 Source: {result.source}")
    else:
        print("   ❌ No result (puede ser timeout o región no disponible)")
    
    return result is not None


async def main():
    """Ejecutar todos los tests"""
    
    print("="*80)
    print("TEST DE INSTRUMENTOS CORREGIDOS")
    print("="*80)
    print("\nCorrecciones aplicadas:")
    print("1. PALSAR: Retorna InstrumentMeasurement, bug en _select_best_scene corregido")
    print("2. MODIS LST: Timeout aumentado a 120s")
    print("3. OpenTopography: Timeout aumentado a 120s")
    
    results = {}
    
    # Test PALSAR
    try:
        results['palsar'] = await test_palsar()
    except Exception as e:
        print(f"\n❌ PALSAR test failed: {e}")
        results['palsar'] = False
    
    # Test MODIS LST
    try:
        results['modis_lst'] = await test_modis_lst()
    except Exception as e:
        print(f"\n❌ MODIS LST test failed: {e}")
        results['modis_lst'] = False
    
    # Test OpenTopography
    try:
        results['opentopography'] = await test_opentopography()
    except Exception as e:
        print(f"\n❌ OpenTopography test failed: {e}")
        results['opentopography'] = False
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE TESTS")
    print("="*80)
    
    for instrument, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {instrument}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 TODOS LOS TESTS PASARON")
    else:
        print(f"\n⚠️ {total - passed} tests fallaron")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
