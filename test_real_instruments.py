#!/usr/bin/env python3
"""Test REAL de instrumentos con credenciales configuradas"""

import sys
import os
sys.path.insert(0, 'backend')

from dotenv import load_dotenv
load_dotenv()

print("="*80)
print("VERIFICACION DE CREDENCIALES Y APIS")
print("="*80)

# Verificar credenciales
print("\n1. CREDENCIALES EN .env:")
print(f"   EARTHDATA_USERNAME: {os.getenv('EARTHDATA_USERNAME', 'NO CONFIGURADO')}")
print(f"   EARTHDATA_PASSWORD: {'***' if os.getenv('EARTHDATA_PASSWORD') else 'NO CONFIGURADO'}")
print(f"   COPERNICUS_MARINE_USERNAME: {os.getenv('COPERNICUS_MARINE_USERNAME', 'NO CONFIGURADO')}")
print(f"   COPERNICUS_MARINE_PASSWORD: {'***' if os.getenv('COPERNICUS_MARINE_PASSWORD') else 'NO CONFIGURADO'}")
print(f"   OPENTOPOGRAPHY_API_KEY: {os.getenv('OPENTOPOGRAPHY_API_KEY', 'NO CONFIGURADO')[:20]}..." if os.getenv('OPENTOPOGRAPHY_API_KEY') else 'NO CONFIGURADO')

# Test ICESat-2
print("\n2. TEST ICESat-2:")
try:
    from satellite_connectors.icesat2_connector import ICESat2Connector
    icesat2 = ICESat2Connector()
    print(f"   Disponible: {icesat2.available}")
    if icesat2.available:
        print("   [OK] ICESat-2 configurado correctamente")
    else:
        print("   [FAIL] ICESat-2 no disponible")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test NSIDC
print("\n3. TEST NSIDC:")
try:
    from satellite_connectors.nsidc_connector import NSIDCConnector
    nsidc = NSIDCConnector()
    print(f"   Disponible: {nsidc.available}")
    if nsidc.available:
        print("   [OK] NSIDC configurado correctamente")
    else:
        print("   [FAIL] NSIDC no disponible")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test Copernicus Marine
print("\n4. TEST Copernicus Marine:")
try:
    from satellite_connectors.copernicus_marine import CopernicusMarineConnector
    copernicus = CopernicusMarineConnector()
    print(f"   Disponible: {copernicus.available}")
    if copernicus.available:
        print("   [OK] Copernicus Marine configurado correctamente")
    else:
        print("   [FAIL] Copernicus Marine no disponible")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test OpenTopography
print("\n5. TEST OpenTopography:")
try:
    from satellite_connectors.opentopography import OpenTopographyConnector
    opentopo = OpenTopographyConnector()
    print(f"   Disponible: {opentopo.available}")
    if opentopo.available:
        print("   [OK] OpenTopography configurado correctamente")
    else:
        print("   [FAIL] OpenTopography no disponible")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test Planetary Computer (Sentinel-2, Sentinel-1, Landsat)
print("\n6. TEST Planetary Computer:")
try:
    from satellite_connectors.planetary_computer import PlanetaryComputerConnector
    pc = PlanetaryComputerConnector()
    print(f"   Disponible: {pc.available}")
    if pc.available:
        print("   [OK] Planetary Computer configurado correctamente")
    else:
        print("   [FAIL] Planetary Computer no disponible")
except Exception as e:
    print(f"   [ERROR] {e}")

print("\n" + "="*80)
print("RESUMEN:")
print("="*80)

# Contar disponibles
available_count = 0
total_count = 6

try:
    if ICESat2Connector().available: available_count += 1
except: pass

try:
    if NSIDCConnector().available: available_count += 1
except: pass

try:
    if CopernicusMarineConnector().available: available_count += 1
except: pass

try:
    if OpenTopographyConnector().available: available_count += 1
except: pass

try:
    if PlanetaryComputerConnector().available: available_count += 1
except: pass

print(f"\nInstrumentos disponibles: {available_count}/{total_count}")
print("="*80)
