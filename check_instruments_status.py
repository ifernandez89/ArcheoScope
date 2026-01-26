#!/usr/bin/env python3
"""
Verificar estado de instrumentos satelitales
"""

import asyncio
import sys
import os
from pathlib import Path

# FIX CRÍTICO: Configurar PROJ_LIB antes de importar rasterio
try:
    import rasterio
    proj_path = Path(rasterio.__file__).parent / 'proj_data'
    if proj_path.exists():
        os.environ['PROJ_LIB'] = str(proj_path)
        os.environ['PROJ_DATA'] = str(proj_path)
        print(f"✅ PROJ configurado: {proj_path}")
        print()
except Exception as e:
    print(f"⚠️ No se pudo configurar PROJ: {e}")
    print()

# Agregar backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from satellite_connectors.real_data_integrator import RealDataIntegrator

async def check_instruments():
    """Verificar disponibilidad de instrumentos"""
    
    print("="*60)
    print("🔍 VERIFICACIÓN DE INSTRUMENTOS SATELITALES")
    print("="*60)
    print()
    
    integrator = RealDataIntegrator()
    
    # Obtener estado de disponibilidad
    available = integrator.get_available_instruments()
    
    print("📡 Estado de instrumentos:")
    print()
    
    total = len(available)
    working = sum(1 for v in available.values() if v)
    
    for instrument, status in available.items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {instrument}")
    
    print()
    print(f"📊 Resumen: {working}/{total} instrumentos funcionando ({working/total*100:.1f}%)")
    print()
    
    # Probar una medición real
    print("🧪 Probando medición real...")
    print("   Región: Petén, Guatemala")
    print()
    
    try:
        # Probar Sentinel-2 NDVI
        result = await integrator.get_instrument_measurement(
            instrument_name="sentinel_2_ndvi",
            lat_min=16.0,
            lat_max=16.05,
            lon_min=-90.0,
            lon_max=-89.95
        )
        
        if result:
            print(f"✅ Sentinel-2 NDVI funcionando:")
            print(f"   Valor: {result['value']:.3f}")
            print(f"   Fuente: {result['source']}")
            print(f"   Confianza: {result['confidence']:.2f}")
        else:
            print("❌ Sentinel-2 NDVI no devolvió datos")
    
    except Exception as e:
        print(f"❌ Error probando Sentinel-2: {e}")
    
    print()
    
    # Probar ICESat-2
    try:
        result = await integrator.get_instrument_measurement(
            instrument_name="icesat2",
            lat_min=16.0,
            lat_max=16.05,
            lon_min=-90.0,
            lon_max=-89.95
        )
        
        if result:
            print(f"✅ ICESat-2 funcionando:")
            print(f"   Elevación: {result['value']:.2f}m")
            print(f"   Fuente: {result['source']}")
        else:
            print("❌ ICESat-2 no devolvió datos")
    
    except Exception as e:
        print(f"❌ Error probando ICESat-2: {e}")
    
    print()
    print("="*60)

if __name__ == "__main__":
    asyncio.run(check_instruments())
