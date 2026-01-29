#!/usr/bin/env python3
"""
Test de Instrumentos Profundos - Diagnóstico
============================================

Verificar por qué SRTM, LiDAR, GPR, InSAR no funcionan.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from satellite_connectors.srtm_connector import SRTMConnector
from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2

async def test_srtm():
    """Test SRTM DEM."""
    print("="*80)
    print("🏔️ TEST 1: SRTM DEM")
    print("="*80)
    print()
    
    try:
        connector = SRTMConnector()
        print("✅ SRTM Connector inicializado")
        
        # Test en Mediterráneo Oriental
        result = await connector.get_elevation_data(
            lat_min=35.3,
            lat_max=35.5,
            lon_min=36.4,
            lon_max=36.6
        )
        
        if result:
            print(f"✅ SRTM funcionó!")
            print(f"   Elevación media: {result.get('value')} m")
            print(f"   Fuente: {result.get('source')}")
            print(f"   Píxeles: {result.get('pixel_count')}")
        else:
            print("❌ SRTM devolvió None")
            print()
            print("RAZONES POSIBLES:")
            print("  1. API keys no configuradas (OPENTOPOGRAPHY_API_KEY)")
            print("  2. Bbox muy pequeño (< 0.01° puede fallar)")
            print("  3. Timeout de red")
            print("  4. Región sin cobertura SRTM")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()

async def test_icesat2():
    """Test ICESat-2 (LiDAR espacial)."""
    print("="*80)
    print("🛰️ TEST 2: ICESat-2 (LiDAR Espacial)")
    print("="*80)
    print()
    
    try:
        integrator = RealDataIntegratorV2()
        
        result = await integrator.get_instrument_measurement_robust(
            instrument_name='icesat2',
            lat_min=35.3,
            lat_max=35.5,
            lon_min=36.4,
            lon_max=36.6
        )
        
        if result and result.value is not None:
            print(f"✅ ICESat-2 funcionó!")
            print(f"   Elevación: {result.value} m")
        else:
            print("❌ ICESat-2 devolvió None")
            print()
            print("RAZONES POSIBLES:")
            print("  1. Cobertura limitada (órbitas específicas)")
            print("  2. No hay datos en esta región")
            print("  3. Bbox muy pequeño (sin intersección con tracks)")
            print("  4. API de NASA no responde")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()

async def test_gpr():
    """Test GPR (Ground Penetrating Radar)."""
    print("="*80)
    print("📡 TEST 3: GPR (Ground Penetrating Radar)")
    print("="*80)
    print()
    
    print("❌ GPR NO DISPONIBLE")
    print()
    print("RAZÓN:")
    print("  GPR requiere mediciones de CAMPO (no satelital)")
    print("  No hay datos GPR disponibles remotamente")
    print()
    print("ALTERNATIVAS:")
    print("  1. Inferir profundidad con DIL (Deep Inference Layer)")
    print("  2. Usar SAR coherence loss como proxy")
    print("  3. Usar thermal inertia (masa enterrada)")
    print()

async def test_insar():
    """Test InSAR (Interferometría SAR)."""
    print("="*80)
    print("📊 TEST 4: InSAR (Interferometría SAR)")
    print("="*80)
    print()
    
    print("❌ InSAR NO IMPLEMENTADO")
    print()
    print("RAZÓN:")
    print("  InSAR requiere datos COMPLEJOS (amplitud + fase)")
    print("  Planetary Computer solo tiene backscatter (amplitud)")
    print()
    print("PARA IMPLEMENTAR:")
    print("  1. Acceso a datos crudos Sentinel-1 SLC (Single Look Complex)")
    print("  2. Procesamiento de interferogramas (SNAP, ISCE)")
    print("  3. Cálculo de coherencia temporal")
    print("  4. Detección de subsidencia/elevación")
    print()
    print("ESTADO: Feature futuro (requiere 8-10 horas implementación)")
    print()

async def test_lidar_aereo():
    """Test LiDAR aéreo."""
    print("="*80)
    print("✈️ TEST 5: LiDAR Aéreo")
    print("="*80)
    print()
    
    print("❌ LiDAR AÉREO NO DISPONIBLE")
    print()
    print("RAZÓN:")
    print("  LiDAR aéreo requiere campañas específicas")
    print("  No hay cobertura global disponible públicamente")
    print()
    print("ALTERNATIVAS:")
    print("  1. ICESat-2 (LiDAR espacial, cobertura limitada)")
    print("  2. SRTM DEM (30m resolución)")
    print("  3. Copernicus DEM (30m resolución)")
    print()

async def diagnostico_completo():
    """Diagnóstico completo de instrumentos profundos."""
    
    print()
    print("="*80)
    print("🔬 DIAGNÓSTICO: INSTRUMENTOS PROFUNDOS")
    print("="*80)
    print()
    
    await test_srtm()
    await test_icesat2()
    await test_gpr()
    await test_insar()
    await test_lidar_aereo()
    
    print("="*80)
    print("📊 RESUMEN")
    print("="*80)
    print()
    
    print("INSTRUMENTOS PROFUNDOS:")
    print()
    print("❌ SRTM DEM:")
    print("   Problema: API keys no configuradas o bbox muy pequeño")
    print("   Solución: Configurar OPENTOPOGRAPHY_API_KEY o usar bbox > 0.1°")
    print()
    print("❌ ICESat-2 (LiDAR espacial):")
    print("   Problema: Cobertura limitada (órbitas específicas)")
    print("   Solución: Normal - solo funciona en algunas regiones")
    print()
    print("❌ GPR:")
    print("   Problema: No es satelital (requiere campo)")
    print("   Solución: Usar DIL (inferencia) como alternativa")
    print()
    print("❌ InSAR:")
    print("   Problema: No implementado (requiere datos complejos)")
    print("   Solución: Feature futuro (8-10 horas)")
    print()
    print("❌ LiDAR aéreo:")
    print("   Problema: No hay cobertura global pública")
    print("   Solución: Usar SRTM/ICESat-2 como alternativa")
    print()
    print("="*80)
    print("💡 RECOMENDACIÓN")
    print("="*80)
    print()
    print("Para mejorar cobertura profunda:")
    print()
    print("1. INMEDIATO (1-2h):")
    print("   • Configurar OPENTOPOGRAPHY_API_KEY")
    print("   • Aumentar bbox mínimo a 0.1° para SRTM")
    print("   • Mejorar DIL para compensar falta de sensores")
    print()
    print("2. CORTO PLAZO (4-6h):")
    print("   • Implementar Copernicus DEM (alternativa a SRTM)")
    print("   • Mejorar inferencia de profundidad (DIL)")
    print("   • Usar SAR coherence loss como proxy de profundidad")
    print()
    print("3. MEDIANO PLAZO (8-10h):")
    print("   • Implementar InSAR básico")
    print("   • Integrar más fuentes DEM")
    print()
    print("="*80)

if __name__ == "__main__":
    asyncio.run(diagnostico_completo())
