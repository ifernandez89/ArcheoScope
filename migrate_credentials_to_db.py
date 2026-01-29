#!/usr/bin/env python3
"""
Migrar credenciales del archivo .env a la base de datos.
"""

import asyncio
import sys
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from credentials_manager import CredentialsManager


async def migrate_credentials():
    """Migrar credenciales de .env a BD."""
    
    print("="*80)
    print("🔐 Migrando credenciales de .env a base de datos")
    print("="*80)
    print()
    
    cm = CredentialsManager()
    
    # Credenciales de Earthdata
    print("📡 Earthdata (NASA):")
    earthdata_username = "nacho.xiphos"
    earthdata_password = "SfLujan2020@"
    
    cm.store_credential("earthdata", "username", earthdata_username, "NASA Earthdata username")
    print(f"   ✅ Username guardado")
    
    cm.store_credential("earthdata", "password", earthdata_password, "NASA Earthdata password")
    print(f"   ✅ Password guardado")
    print()
    
    # Credenciales de Copernicus Marine
    print("🌊 Copernicus Marine:")
    copernicus_username = "nacho.xiphos@gmail.com"
    copernicus_password = "SfLujan2020@"
    
    cm.store_credential("copernicus_marine", "username", copernicus_username, "Copernicus Marine username")
    print(f"   ✅ Username guardado")
    
    cm.store_credential("copernicus_marine", "password", copernicus_password, "Copernicus Marine password")
    print(f"   ✅ Password guardado")
    print()
    
    # Credenciales de OpenTopography
    print("🏔️ OpenTopography:")
    opentopography_api_key = "a50282b0e5ff10cc45ada6d8ac1bf0b3"
    
    cm.store_credential("opentopography", "api_key", opentopography_api_key, "OpenTopography API key")
    print(f"   ✅ API Key guardada")
    print()
    
    # Credenciales de Copernicus CDS
    print("🌍 Copernicus CDS:")
    cds_api_key = "688997f8-954e-4cc4-bfae-430d5a67f4d3"
    cds_url = "https://cds.climate.copernicus.eu/api/v2"
    
    cm.store_credential("copernicus_cds", "api_key", cds_api_key, "Copernicus CDS API Key")
    print(f"   ✅ API Key guardada")
    
    cm.store_credential("copernicus_cds", "url", cds_url, "Copernicus CDS API URL")
    print(f"   ✅ URL guardada")
    print()
    
    # Verificar que se guardaron correctamente
    print("="*80)
    print("🔍 Verificando credenciales guardadas")
    print("="*80)
    print()
    
    earthdata_user = cm.get_credential("earthdata", "username")
    earthdata_pass = cm.get_credential("earthdata", "password")
    
    if earthdata_user and earthdata_pass:
        print(f"✅ Earthdata: {earthdata_user} / {'*' * len(earthdata_pass)}")
    else:
        print("❌ Earthdata: No encontrado")
    
    copernicus_user = cm.get_credential("copernicus_marine", "username")
    copernicus_pass = cm.get_credential("copernicus_marine", "password")
    
    if copernicus_user and copernicus_pass:
        print(f"✅ Copernicus Marine: {copernicus_user} / {'*' * len(copernicus_pass)}")
    else:
        print("❌ Copernicus Marine: No encontrado")
    
    opentopo_key = cm.get_credential("opentopography", "api_key")
    
    if opentopo_key:
        print(f"✅ OpenTopography: {opentopo_key[:10]}...{opentopo_key[-5:]}")
    else:
        print("❌ OpenTopography: No encontrado")
    
    cds_key = cm.get_credential("copernicus_cds", "api_key")
    
    if cds_key:
        print(f"✅ Copernicus CDS: {cds_key[:10]}...{cds_key[-5:]}")
    else:
        print("❌ Copernicus CDS: No encontrado")
    
    print()
    print("="*80)
    print("✅ Migración completada")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(migrate_credentials())
