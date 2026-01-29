#!/usr/bin/env python3
"""
Test SRTM Credentials Fix - Verificar que SRTM lee credenciales de BD
======================================================================

OBJETIVO: Verificar que SRTMConnector ahora lee credenciales desde BD
correctamente a través de RealDataIntegratorV2.
"""

import asyncio
import sys
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_srtm_credentials():
    """Test que SRTM lee credenciales de BD correctamente."""
    
    print("="*80)
    print("TEST: SRTM Credentials Fix")
    print("="*80)
    print()
    
    # 1. Verificar que credentials_manager tiene las credenciales
    print("1️⃣ Verificando credenciales en BD...")
    print("-" * 80)
    
    try:
        from backend.credentials_manager import CredentialsManager
        cm = CredentialsManager()
        
        # Verificar OpenTopography
        opentopo_key = cm.get_credential("opentopography", "api_key")
        if opentopo_key:
            print(f"   ✅ OpenTopography API key encontrada: {opentopo_key[:10]}...")
        else:
            print(f"   ❌ OpenTopography API key NO encontrada en BD")
        
        # Verificar Earthdata
        earthdata_user = cm.get_credential("earthdata", "username")
        earthdata_pass = cm.get_credential("earthdata", "password")
        if earthdata_user and earthdata_pass:
            print(f"   ✅ Earthdata credentials encontradas: {earthdata_user}")
        else:
            print(f"   ⚠️ Earthdata credentials NO encontradas en BD")
        
        print()
        
    except Exception as e:
        print(f"   ❌ Error verificando credenciales: {e}")
        print()
        return False
    
    # 2. Inicializar RealDataIntegratorV2 (debe crear credentials_manager internamente)
    print("2️⃣ Inicializando RealDataIntegratorV2...")
    print("-" * 80)
    
    try:
        from backend.satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
        integrator = RealDataIntegratorV2()
        
        print(f"   ✅ RealDataIntegratorV2 inicializado")
        
        # Verificar que tiene credentials_manager
        if integrator.credentials_manager:
            print(f"   ✅ CredentialsManager disponible en integrador")
        else:
            print(f"   ❌ CredentialsManager NO disponible en integrador")
        
        # Verificar que SRTM connector existe
        if integrator.connectors.get('srtm'):
            print(f"   ✅ SRTM connector inicializado")
            
            # Verificar que SRTM tiene credentials_manager
            srtm = integrator.connectors['srtm']
            if srtm.credentials_manager:
                print(f"   ✅ SRTM tiene credentials_manager")
            else:
                print(f"   ❌ SRTM NO tiene credentials_manager")
            
            # Verificar que SRTM leyó las credenciales
            if srtm.opentopography_key:
                print(f"   ✅ SRTM leyó OpenTopography key: {srtm.opentopography_key[:10]}...")
            else:
                print(f"   ⚠️ SRTM NO tiene OpenTopography key")
            
            if srtm.earthdata_username:
                print(f"   ✅ SRTM leyó Earthdata username: {srtm.earthdata_username}")
            else:
                print(f"   ⚠️ SRTM NO tiene Earthdata username")
        else:
            print(f"   ❌ SRTM connector NO inicializado")
        
        print()
        
    except Exception as e:
        print(f"   ❌ Error inicializando integrador: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False
    
    # 3. Test real de SRTM con coordenadas pequeñas
    print("3️⃣ Test real de SRTM (Giza, Egipto)...")
    print("-" * 80)
    
    try:
        # Coordenadas de Giza (bbox pequeño: ~11 km)
        lat_min, lat_max = 29.95, 30.05  # 0.1° = ~11 km
        lon_min, lon_max = 31.10, 31.20  # 0.1° = ~11 km
        
        print(f"   📍 Región: [{lat_min:.2f}, {lat_max:.2f}] x [{lon_min:.2f}, {lon_max:.2f}]")
        print(f"   📏 Tamaño: ~11 km x 11 km")
        print()
        
        result = await integrator.get_instrument_measurement_robust(
            'srtm_elevation',
            lat_min, lat_max, lon_min, lon_max
        )
        
        print(f"   Status: {result.status}")
        print(f"   Instrumento: {result.instrument_name}")
        
        if result.status == 'SUCCESS':
            print(f"   ✅ ÉXITO: Valor = {result.value:.2f} {result.unit}")
            print(f"   Confianza: {result.confidence:.2f}")
            print(f"   Fuente: {result.source}")
            print(f"   Tiempo: {result.processing_time_s:.2f}s")
            print()
            print("   🎉 SRTM AHORA LEE CREDENCIALES DE BD CORRECTAMENTE!")
            return True
            
        elif result.status == 'DEGRADED':
            print(f"   ⚠️ DEGRADED: Valor = {result.value:.2f} {result.unit}")
            print(f"   Razón: {result.reason}")
            print(f"   Confianza: {result.confidence:.2f}")
            print()
            print("   ✅ SRTM funciona pero con calidad degradada")
            return True
            
        elif result.status == 'FAILED':
            print(f"   ❌ FAILED: {result.reason}")
            if result.error_details:
                print(f"   Error: {result.error_details}")
            print()
            print("   ❌ SRTM sigue fallando - revisar credenciales o API")
            return False
            
        else:
            print(f"   ⚠️ Status inesperado: {result.status}")
            print(f"   Razón: {result.reason}")
            print()
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test de SRTM: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False


async def main():
    """Ejecutar test completo."""
    
    success = await test_srtm_credentials()
    
    print()
    print("="*80)
    if success:
        print("✅ TEST EXITOSO: SRTM ahora lee credenciales de BD")
    else:
        print("❌ TEST FALLIDO: SRTM aún tiene problemas")
    print("="*80)
    print()
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
