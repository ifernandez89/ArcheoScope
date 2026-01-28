#!/usr/bin/env python3
"""
Test para verificar sitios arqueológicos en la Amazonía
"""

import asyncio
import sys
from pathlib import Path

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / 'backend'))

from database import db

async def test_amazonia_sites():
    """Verificar sitios en la Amazonía brasileña"""
    
    print("🔍 Investigando sitios arqueológicos en Amazonía brasileña")
    print("=" * 80)
    
    # Conectar a BD
    await db.connect()
    
    # Región Amazonía: aproximadamente -5 a -3 lat, -62 a -60 lon
    center_lat = -4.0
    center_lon = -61.0
    radius_km = 200  # Radio amplio
    
    print(f"\n📍 Buscando sitios cerca de {center_lat}, {center_lon}")
    print(f"   Radio: {radius_km} km")
    
    sites = await db.search_sites(center_lat, center_lon, radius_km, limit=500)
    
    print(f"\n📊 Sitios encontrados: {len(sites)}")
    
    if sites:
        print("\n🗺️ Primeros 10 sitios:")
        print("-" * 80)
        for i, site in enumerate(sites[:10]):
            print(f"\n{i+1}. {site['name']}")
            print(f"   Ubicación: {site['latitude']:.4f}, {site['longitude']:.4f}")
            print(f"   País: {site.get('country', 'N/A')}")
            print(f"   Tipo: {site.get('site_type', 'N/A')}")
            print(f"   Ambiente: {site.get('environment_type', 'N/A')}")
            print(f"   Distancia: {site.get('distance_km', 0):.1f} km")
    else:
        print("\n⚠️ NO SE ENCONTRARON SITIOS EN LA REGIÓN")
        print("\nPosibles causas:")
        print("1. La base de datos no tiene sitios en esta región")
        print("2. Las coordenadas están fuera del rango de sitios conocidos")
        print("3. El radio de búsqueda es muy pequeño")
    
    # Buscar en toda la Amazonía (región más amplia)
    print("\n" + "=" * 80)
    print("🌎 Buscando en toda la región amazónica (radio 500 km)...")
    
    sites_wide = await db.search_sites(center_lat, center_lon, 500, limit=500)
    print(f"📊 Sitios encontrados: {len(sites_wide)}")
    
    if sites_wide:
        # Agrupar por país
        by_country = {}
        for site in sites_wide:
            country = site.get('country', 'Unknown')
            by_country[country] = by_country.get(country, 0) + 1
        
        print("\n📍 Sitios por país:")
        for country, count in sorted(by_country.items(), key=lambda x: x[1], reverse=True):
            print(f"   {country}: {count} sitios")
    
    # Verificar total de sitios en BD
    print("\n" + "=" * 80)
    total_sites = await db.count_sites()
    print(f"📊 Total de sitios en base de datos: {total_sites:,}")
    
    # Buscar sitios en Brasil
    print("\n🇧🇷 Buscando sitios en Brasil...")
    brazil_sites = await db.get_sites_by_country("Brazil", limit=100)
    print(f"📊 Sitios en Brasil: {len(brazil_sites)}")
    
    if brazil_sites:
        print("\n🗺️ Primeros 10 sitios en Brasil:")
        print("-" * 80)
        for i, site in enumerate(brazil_sites[:10]):
            print(f"\n{i+1}. {site['name']}")
            print(f"   Ubicación: {site['latitude']:.4f}, {site['longitude']:.4f}")
            print(f"   Tipo: {site.get('site_type', 'N/A')}")
    
    await db.close()
    
    print("\n" + "=" * 80)
    if not sites and not sites_wide:
        print("❌ PROBLEMA DETECTADO: No hay sitios en la región amazónica")
        print("\n💡 Recomendaciones:")
        print("1. Verificar que la base de datos tiene sitios sudamericanos")
        print("2. Revisar el proceso de harvesting de sitios")
        print("3. Considerar agregar sitios amazónicos manualmente")
    else:
        print("✅ Hay sitios en la región, pero pueden estar fuera del bounding box específico")

if __name__ == "__main__":
    asyncio.run(test_amazonia_sites())
