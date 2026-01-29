#!/usr/bin/env python3
"""
Test rápido del CORE (5 instrumentos esenciales)
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2


async def test_core():
    """Test solo CORE (5 instrumentos)."""
    
    print("="*80)
    print("🎯 TEST CORE (5 instrumentos esenciales)")
    print("="*80)
    
    integrator = RealDataIntegratorV2()
    
    # Solo CORE
    core_instruments = [
        'sentinel_2_ndvi',      # 1. Vegetación
        'sentinel_1_sar',       # 2. Subsuperficie
        'landsat_thermal',      # 3. Térmico
        'srtm_elevation',       # 4. Relieve
        'era5_climate'          # 5. Clima
    ]
    
    # Giza, Egipto (test rápido)
    lat_min, lat_max = 29.95, 30.05
    lon_min, lon_max = 31.10, 31.20
    
    print(f"\n📍 Región: Giza, Egipto")
    print(f"   [{lat_min}, {lat_max}] x [{lon_min}, {lon_max}]")
    print(f"\n🔬 Testeando {len(core_instruments)} instrumentos CORE...\n")
    
    results = {}
    
    for i, instrument in enumerate(core_instruments, 1):
        print(f"[{i}/5] {instrument}...", end=" ", flush=True)
        
        try:
            result = await integrator.get_instrument_measurement_robust(
                instrument, lat_min, lat_max, lon_min, lon_max
            )
            
            status = result.status.value if hasattr(result, 'status') else 'UNKNOWN'
            results[instrument] = status
            
            if status == 'SUCCESS':
                print(f"✅ {status}")
            elif status == 'DEGRADED':
                print(f"⚠️ {status}")
            else:
                print(f"❌ {status}")
                
        except Exception as e:
            print(f"💥 ERROR: {e}")
            results[instrument] = 'ERROR'
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMEN CORE")
    print("="*80)
    
    success_count = sum(1 for s in results.values() if s in ['SUCCESS', 'DEGRADED'])
    total = len(results)
    
    print(f"\nInstrumentos funcionando: {success_count}/{total} ({success_count/total*100:.1f}%)")
    
    print("\nDetalle:")
    for instrument, status in results.items():
        emoji = "✅" if status in ['SUCCESS', 'DEGRADED'] else "❌"
        print(f"  {emoji} {instrument}: {status}")
    
    print("\n" + "="*80)
    
    if success_count == total:
        print("✅ CORE COMPLETO: Todos los instrumentos funcionando")
        print("="*80)
        return True
    else:
        print(f"⚠️ CORE INCOMPLETO: {total - success_count} instrumentos fallando")
        print("="*80)
        return False


if __name__ == "__main__":
    success = asyncio.run(test_core())
    sys.exit(0 if success else 1)
