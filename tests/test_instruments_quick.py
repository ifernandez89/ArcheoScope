#!/usr/bin/env python3
"""
Test RÁPIDO para diagnosticar instrumentos - sin BD
"""

import sys
import asyncio
from pathlib import Path

# Agregar backend al path
backend_path = str(Path(__file__).parent / "backend")
sys.path.insert(0, backend_path)

async def test_quick():
    """Test rápido sin BD"""
    
    print("="*80)
    print("DIAGNÓSTICO RÁPIDO DE INSTRUMENTOS")
    print("="*80)
    
    # Test 1: RealDataIntegrator
    print("\n1. RealDataIntegrator...")
    try:
        from satellite_connectors.real_data_integrator import RealDataIntegrator
        integrator = RealDataIntegrator()
        print("   [OK] Inicializado")
        
        available = integrator.get_available_instruments()
        print(f"   [OK] {sum(available.values())}/{len(available)} instrumentos disponibles")
    except Exception as e:
        print(f"   [FAIL] {e}")
        return
    
    # Test 2: Test de medición directa (sin CoreAnomalyDetector)
    print("\n2. Test de medición directa (Sentinel-2 NDVI)...")
    try:
        # Coordenadas de Giza
        lat_min, lat_max = 29.97, 29.98
        lon_min, lon_max = 31.13, 31.14
        
        result = await integrator.get_instrument_measurement(
            instrument_name="sentinel_2_ndvi",
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max
        )
        
        if result:
            print(f"   [OK] Medición exitosa")
            print(f"      Valor: {result.get('value', 'N/A')}")
            print(f"      Fuente: {result.get('source', 'N/A')}")
            print(f"      Status: {result.get('status', 'N/A')}")
        else:
            print("   [FAIL] Sin datos")
            
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Test de ICESat-2 (migrado a InstrumentContract)
    print("\n3. Test de ICESat-2 (InstrumentContract)...")
    try:
        result = await integrator.get_instrument_measurement(
            instrument_name="icesat2",
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max
        )
        
        if result:
            print(f"   [OK] Medición exitosa")
            print(f"      Valor: {result.get('value', 'N/A')}")
            print(f"      Status: {result.get('status', 'N/A')}")
            print(f"      Confidence: {result.get('confidence', 'N/A')}")
        else:
            print("   [FAIL] Sin datos")
            
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Verificar que el log se crea
    print("\n4. Verificando sistema de logging...")
    import os
    if os.path.exists('instrument_diagnostics.log'):
        print("   [OK] Log de diagnóstico existe")
        # Leer últimas líneas
        with open('instrument_diagnostics.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                print(f"   [OK] {len(lines)} líneas en el log")
                print("   Últimas 5 líneas:")
                for line in lines[-5:]:
                    print(f"      {line.rstrip()}")
    else:
        print("   [INFO] Log no existe aún (normal en primera ejecución)")
    
    print("\n" + "="*80)
    print("DIAGNÓSTICO COMPLETADO")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_quick())
