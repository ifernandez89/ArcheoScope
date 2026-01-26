#!/usr/bin/env python3
"""
Test NASA Earthdata Integration
================================

Prueba la integración con ICESat-2, MODIS y SMAP usando credenciales reales
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent))

from backend.satellite_connectors.icesat2_connector import ICESat2Connector
from backend.satellite_connectors.modis_connector import MODISConnector
from backend.satellite_connectors.smap_connector import SMAPConnector


async def test_earthdata_apis():
    """Test completo de APIs de NASA Earthdata"""
    
    print("="*80)
    print("🛰️ TEST: NASA Earthdata Integration")
    print("="*80)
    print()
    
    # Verificar credenciales
    username = os.getenv('EARTHDATA_USERNAME')
    token = os.getenv('EARTHDATA_TOKEN')
    
    if not username or not token:
        print("❌ ERROR: Credenciales de Earthdata no encontradas")
        print("   Verifica que EARTHDATA_USERNAME y EARTHDATA_TOKEN estén en .env")
        return False
    
    print(f"✅ Credenciales encontradas: {username}")
    print()
    
    results = {
        'icesat2': False,
        'modis': False,
        'smap': False
    }
    
    # Test 1: ICESat-2 (Elevación de hielo)
    print("🔍 TEST 1: ICESat-2 - Elevación de hielo")
    print("-" * 80)
    
    try:
        icesat2 = ICESat2Connector()
        
        if not icesat2.available:
            print("⚠️ ICESat-2 no disponible - instalar: pip install earthaccess h5py")
        else:
            print("✅ ICESat-2 connector inicializado")
            
            # Probar con Groenlandia (área con hielo)
            print("   Probando con Groenlandia...")
            data = await icesat2.get_elevation_data(
                lat_min=72.0,
                lat_max=72.1,
                lon_min=-38.0,
                lon_max=-37.9
            )
            
            if data:
                print(f"   ✅ Datos recibidos:")
                print(f"      - Elevación media: {data.indices.get('elevation_mean', 0):.2f} m")
                print(f"      - Confianza: {data.confidence:.2f}")
                print(f"      - Fecha: {data.acquisition_date}")
                results['icesat2'] = True
            else:
                print("   ⚠️ No se obtuvieron datos (puede ser normal si no hay tracks)")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: MODIS (Temperatura superficial)
    print("🔍 TEST 2: MODIS - Temperatura superficial")
    print("-" * 80)
    
    try:
        modis = MODISConnector()
        
        if not modis.available:
            print("⚠️ MODIS no disponible - requiere credenciales Earthdata")
        else:
            print("✅ MODIS connector inicializado")
            
            # Probar con Giza (desierto)
            print("   Probando con Giza, Egipto...")
            data = await modis.get_lst_data(
                lat_min=29.97,
                lat_max=29.99,
                lon_min=31.12,
                lon_max=31.14
            )
            
            if data:
                print(f"   ✅ Datos recibidos:")
                print(f"      - LST media: {data.indices.get('lst_mean', 0):.2f} K")
                print(f"      - Confianza: {data.confidence:.2f}")
                print(f"      - Fecha: {data.acquisition_date}")
                results['modis'] = True
            else:
                print("   ⚠️ No se obtuvieron datos")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: SMAP (Humedad del suelo)
    print("🔍 TEST 3: SMAP - Humedad del suelo")
    print("-" * 80)
    
    try:
        smap = SMAPConnector()
        
        if not smap.available:
            print("⚠️ SMAP no disponible - instalar: pip install earthaccess")
        else:
            print("✅ SMAP connector inicializado")
            
            # Probar con área agrícola
            print("   Probando con área agrícola...")
            data = await smap.get_soil_moisture(
                lat_min=40.0,
                lat_max=40.1,
                lon_min=-100.0,
                lon_max=-99.9
            )
            
            if data:
                print(f"   ✅ Datos recibidos:")
                print(f"      - Humedad: {data.indices.get('soil_moisture', 0):.3f}")
                print(f"      - Confianza: {data.confidence:.2f}")
                print(f"      - Fecha: {data.acquisition_date}")
                results['smap'] = True
            else:
                print("   ⚠️ No se obtuvieron datos")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Resumen
    print("="*80)
    print("📊 RESUMEN DE INTEGRACIÓN EARTHDATA")
    print("="*80)
    
    total_tests = len(results)
    successful = sum(1 for v in results.values() if v)
    
    print(f"Tests ejecutados: {total_tests}")
    print(f"Tests exitosos: {successful}")
    print(f"Tasa de éxito: {(successful/total_tests*100):.1f}%")
    print()
    
    for api, success in results.items():
        icon = "✅" if success else "❌"
        print(f"{icon} {api.upper()}: {'Funcionando' if success else 'No disponible'}")
    
    print()
    
    if successful > 0:
        print("✅ INTEGRACIÓN EARTHDATA EXITOSA")
        print(f"✅ {successful} APIs de NASA funcionando correctamente")
        print("✅ Sistema puede usar datos satelitales reales de NASA")
    else:
        print("⚠️ ADVERTENCIA: Ninguna API de Earthdata funcionó")
        print("   Verificar:")
        print("   1. Credenciales correctas en .env")
        print("   2. Dependencias instaladas (earthaccess, h5py)")
        print("   3. Conectividad a servidores de NASA")
    
    print()
    
    return successful > 0


if __name__ == "__main__":
    try:
        success = asyncio.run(test_earthdata_apis())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
