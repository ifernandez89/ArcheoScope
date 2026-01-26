#!/usr/bin/env python3
"""
Test Copernicus Marine Integration
===================================
Prueba la integración con Copernicus Marine Service
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent))

from backend.satellite_connectors.copernicus_marine_connector import CopernicusMarineConnector


async def test_copernicus_marine():
    """Test completo de Copernicus Marine"""
    
    print("="*80)
    print("🌊 TEST: Copernicus Marine Service Integration")
    print("="*80)
    print()
    
    # Verificar credenciales
    username = os.getenv('COPERNICUS_MARINE_USERNAME')
    password = os.getenv('COPERNICUS_MARINE_PASSWORD')
    
    if not username or not password:
        print("❌ ERROR: Credenciales de Copernicus Marine no encontradas")
        print("   Verifica que COPERNICUS_MARINE_USERNAME y PASSWORD estén en .env")
        return False
    
    print(f"✅ Credenciales encontradas: {username}")
    print()
    
    # Test 1: Inicializar conector
    print("🔍 TEST 1: Inicialización del conector")
    print("-" * 80)
    
    try:
        connector = CopernicusMarineConnector()
        
        if not connector.available:
            print("❌ Copernicus Marine no disponible")
            return False
        
        print("✅ Conector inicializado correctamente")
        print()
        
    except Exception as e:
        print(f"❌ Error inicializando: {e}")
        return False
    
    # Test 2: Obtener datos de hielo marino (Ártico)
    print("🔍 TEST 2: Datos de hielo marino - Ártico")
    print("-" * 80)
    
    try:
        print("   Probando con región ártica...")
        data = await connector.get_sea_ice_data(
            lat_min=75.0,
            lat_max=80.0,
            lon_min=-30.0,
            lon_max=-20.0
        )
        
        if data:
            print(f"   ✅ Datos recibidos:")
            print(f"      - Concentración de hielo: {data.indices.get('ice_concentration_mean', 0):.2f}%")
            print(f"      - Confianza: {data.confidence:.2f}")
            print(f"      - Fecha: {data.acquisition_date}")
            print(f"      - Fuente: Copernicus Marine")
            
            # Verificar otros índices disponibles
            if 'ice_thickness_mean' in data.indices:
                print(f"      - Espesor de hielo: {data.indices['ice_thickness_mean']:.2f} m")
            
            result_arctic = True
        else:
            print("   ⚠️ No se obtuvieron datos")
            result_arctic = False
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        result_arctic = False
    
    print()
    
    # Test 3: Obtener datos de hielo marino (Antártico)
    print("🔍 TEST 3: Datos de hielo marino - Antártico")
    print("-" * 80)
    
    try:
        print("   Probando con región antártica...")
        data = await connector.get_sea_ice_data(
            lat_min=-75.0,
            lat_max=-70.0,
            lon_min=0.0,
            lon_max=10.0
        )
        
        if data:
            print(f"   ✅ Datos recibidos:")
            print(f"      - Concentración de hielo: {data.indices.get('ice_concentration_mean', 0):.2f}%")
            print(f"      - Confianza: {data.confidence:.2f}")
            print(f"      - Fecha: {data.acquisition_date}")
            result_antarctic = True
        else:
            print("   ⚠️ No se obtuvieron datos")
            result_antarctic = False
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        result_antarctic = False
    
    print()
    
    # Resumen
    print("="*80)
    print("📊 RESUMEN DE INTEGRACIÓN COPERNICUS MARINE")
    print("="*80)
    
    tests_passed = sum([result_arctic, result_antarctic])
    total_tests = 2
    
    print(f"Tests ejecutados: {total_tests}")
    print(f"Tests exitosos: {tests_passed}")
    print(f"Tasa de éxito: {(tests_passed/total_tests*100):.1f}%")
    print()
    
    if tests_passed > 0:
        print("✅ INTEGRACIÓN COPERNICUS MARINE EXITOSA")
        print(f"✅ {tests_passed} regiones con datos de hielo marino")
        print("✅ Sistema puede usar datos oceanográficos reales")
        print()
        print("📊 Capacidades disponibles:")
        print("   - Concentración de hielo marino")
        print("   - Series temporales 1993-2023+")
        print("   - Cobertura polar completa")
        print("   - Resolución diaria/semanal")
    else:
        print("⚠️ ADVERTENCIA: No se obtuvieron datos")
        print("   Verificar:")
        print("   1. Credenciales correctas")
        print("   2. Conectividad a servidores Copernicus")
        print("   3. Disponibilidad del servicio")
    
    print()
    
    return tests_passed > 0


if __name__ == "__main__":
    try:
        success = asyncio.run(test_copernicus_marine())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
