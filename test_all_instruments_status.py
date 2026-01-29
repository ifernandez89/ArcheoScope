#!/usr/bin/env python3
"""
Test TODOS los instrumentos - Ver cuáles fallan y por qué
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_all_instruments():
    """Test de TODOS los 15 instrumentos."""
    
    print("="*80)
    print("🔬 TEST DE LOS 15 INSTRUMENTOS")
    print("="*80)
    print()
    
    from backend.satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
    
    integrator = RealDataIntegratorV2()
    
    # Coordenadas de test (Giza, Egipto - bbox 0.1° = ~11 km)
    lat_min, lat_max = 29.95, 30.05
    lon_min, lon_max = 31.10, 31.20
    
    print(f"📍 Región de test: Giza, Egipto")
    print(f"   Coordenadas: [{lat_min:.2f}, {lat_max:.2f}] x [{lon_min:.2f}, {lon_max:.2f}]")
    print(f"   Tamaño: ~11 km x 11 km")
    print()
    
    # Lista de TODOS los instrumentos
    instruments = [
        # Sentinel-2 (NDVI, multispectral)
        'sentinel_2_ndvi',
        
        # Sentinel-1 (SAR)
        'sentinel_1_sar',
        
        # Landsat (térmico)
        'landsat_thermal',
        
        # ICESat-2 (elevación)
        'icesat2',
        
        # MODIS LST (térmico regional)
        'modis_lst',
        
        # NSIDC (hielo, criosfera)
        'nsidc_sea_ice',
        
        # Copernicus Marine (hielo marino, SST)
        'copernicus_sst',
        
        # OpenTopography (DEM, LiDAR)
        'opentopography',
        
        # VIIRS (thermal, NDVI, fire)
        'viirs_thermal',
        
        # SRTM DEM (topographic)
        'srtm_elevation',
        
        # ALOS PALSAR-2 (L-band SAR)
        'palsar_backscatter',
        
        # ERA5 (climate)
        'era5_climate',
        
        # CHIRPS (precipitation)
        'chirps_precipitation',
    ]
    
    print(f"🔬 Testeando {len(instruments)} instrumentos...")
    print()
    
    results = {}
    
    for i, instrument in enumerate(instruments, 1):
        print(f"[{i}/{len(instruments)}] {instrument}...", end=" ", flush=True)
        
        try:
            result = await integrator.get_instrument_measurement_robust(
                instrument, lat_min, lat_max, lon_min, lon_max
            )
            
            status = str(result.status).split('.')[-1]  # InstrumentStatus.SUCCESS -> SUCCESS
            results[instrument] = {
                'status': status,
                'value': result.value,
                'reason': result.reason,
                'error': result.error_details
            }
            
            if status == 'SUCCESS':
                print(f"✅ {status}")
            elif status == 'DEGRADED':
                print(f"⚠️ {status}")
            else:
                print(f"❌ {status}: {result.reason}")
            
        except Exception as e:
            results[instrument] = {
                'status': 'EXCEPTION',
                'value': None,
                'reason': str(e),
                'error': str(e)
            }
            print(f"💥 EXCEPTION: {e}")
    
    print()
    print("="*80)
    print("📊 RESUMEN:")
    print("="*80)
    
    success_count = sum(1 for r in results.values() if r['status'] == 'SUCCESS')
    degraded_count = sum(1 for r in results.values() if r['status'] == 'DEGRADED')
    failed_count = sum(1 for r in results.values() if r['status'] not in ['SUCCESS', 'DEGRADED'])
    
    print(f"✅ SUCCESS: {success_count}/{len(instruments)}")
    print(f"⚠️ DEGRADED: {degraded_count}/{len(instruments)}")
    print(f"❌ FAILED: {failed_count}/{len(instruments)}")
    print()
    
    # Instrumentos fallando
    if failed_count > 0:
        print("❌ INSTRUMENTOS FALLANDO:")
        print("-" * 80)
        for instrument, result in results.items():
            if result['status'] not in ['SUCCESS', 'DEGRADED']:
                print(f"   • {instrument}: {result['status']}")
                if result['reason']:
                    print(f"     Razón: {result['reason']}")
                if result['error']:
                    print(f"     Error: {result['error'][:100]}")
        print()
    
    # Coverage score
    coverage = (success_count + degraded_count * 0.5) / len(instruments)
    print(f"📊 Coverage Score: {coverage:.1%}")
    print()
    
    return results


if __name__ == "__main__":
    asyncio.run(test_all_instruments())
