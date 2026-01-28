#!/usr/bin/env python3
"""
Test SAR rápido - solo una descarga con ventana optimizada
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

async def test_sar_rapido():
    """Test SAR con ventana optimizada"""
    
    print("=" * 80)
    print("TEST SAR RAPIDO - Patagonia con ventana bbox")
    print("=" * 80)
    print()
    
    # Coordenadas Patagonia (región más pequeña para test rápido)
    lat_min = -50.50
    lat_max = -50.45
    lon_min = -73.10
    lon_max = -73.00
    
    print(f"Region: Patagonia Proglaciar (test pequeño)")
    print(f"Bbox: {lat_min}, {lat_max}, {lon_min}, {lon_max}")
    print(f"Area: ~10 x 5 km")
    print()
    
    # Inicializar conector
    connector = PlanetaryComputerConnector()
    
    if not connector.available:
        print("ERROR: Planetary Computer no disponible")
        return False
    
    print("OK: Planetary Computer disponible")
    print()
    
    print("-" * 80)
    print("Descargando SAR con ventana bbox optimizada...")
    print("-" * 80)
    
    start_time = datetime.now()
    
    result = await connector.get_sar_data(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
        resolution_m=30  # 30m optimizado
    )
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print()
    
    if result:
        print(f"OK: SAR descargado correctamente")
        print(f"Tiempo: {elapsed:.1f}s")
        print(f"Resolucion: {result.resolution_m}m")
        print(f"Fecha: {result.acquisition_date.date()}")
        print()
        print(f"Indices:")
        print(f"  VV mean: {result.indices['vv_mean']:.2f} dB")
        print(f"  VH mean: {result.indices['vh_mean']:.2f} dB")
        print(f"  VV/VH ratio: {result.indices['vv_vh_ratio']:.2f}")
        print(f"  Backscatter std: {result.indices['backscatter_std']:.2f}")
        print()
        
        # Verificar que las bandas no estén vacías
        if 'vv' in result.bands and 'vh' in result.bands:
            vv_shape = result.bands['vv'].shape
            vh_shape = result.bands['vh'].shape
            print(f"Bandas:")
            print(f"  VV shape: {vv_shape}")
            print(f"  VH shape: {vh_shape}")
            print()
        
        print("=" * 80)
        print("EXITO: SAR funcionando con ventana bbox optimizada")
        print(f"Tiempo total: {elapsed:.1f}s")
        print("=" * 80)
        
        return True
    else:
        print(f"ERROR: SAR fallo")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_sar_rapido())
    exit(0 if success else 1)
