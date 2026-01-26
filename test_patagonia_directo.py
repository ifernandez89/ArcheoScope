#!/usr/bin/env python3
"""
ArcheoScope - Test DIRECTO Patagonia
Candidato #001: Región Proglaciar Patagónica

Test simplificado que carga .env explícitamente
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# CARGAR .env EXPLÍCITAMENTE
print("Cargando variables de entorno...")
load_dotenv()

# Verificar credenciales
print("\nVerificando credenciales:")
print(f"  EARTHDATA_USERNAME: {os.getenv('EARTHDATA_USERNAME')}")
print(f"  EARTHDATA_PASSWORD: {'*' * len(os.getenv('EARTHDATA_PASSWORD', ''))}")
print(f"  OPENTOPOGRAPHY_API_KEY: {os.getenv('OPENTOPOGRAPHY_API_KEY', 'NO')[:20]}...")

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

print("\n" + "="*80)
print("ARCHEOSCOPE - TEST DIRECTO PATAGONIA")
print("Candidato #001: Region Proglaciar Patagonica")
print("="*80)
print()
print("Coordenadas: -50.4760 S, -73.0450 W")
print("Bbox: [-50.55, -50.40] x [-73.15, -72.90]")
print("Area: ~35 x 20 km")
print("="*80)
print()

# Test individual de cada instrumento
async def test_instrumentos():
    """Test individual de cada instrumento"""
    
    lat_min, lat_max = -50.55, -50.40
    lon_min, lon_max = -73.15, -72.90
    
    from satellite_connectors.real_data_integrator import RealDataIntegrator
    
    integrator = RealDataIntegrator()
    
    print("\n" + "="*80)
    print("TEST DE INSTRUMENTOS INDIVIDUALES")
    print("="*80)
    
    instrumentos = [
        ("MODIS LST", "modis_lst"),
        ("Sentinel-1 SAR", "sentinel_1_sar"),
        ("NSIDC Sea Ice", "nsidc_sea_ice"),
        ("ICESat-2", "icesat2"),
        ("OpenTopography", "opentopography")
    ]
    
    resultados = []
    
    for nombre, instrumento in instrumentos:
        print(f"\n[TEST] {nombre} ({instrumento})")
        print("-" * 80)
        
        try:
            import time
            start = time.time()
            
            data = await integrator.get_instrument_measurement(
                instrument_name=instrumento,
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max
            )
            
            elapsed = time.time() - start
            
            if data:
                print(f"  [OK] Datos obtenidos en {elapsed:.2f}s")
                print(f"  Valor: {data.get('value', 'N/A')}")
                print(f"  Fuente: {data.get('source', 'N/A')}")
                print(f"  Confianza: {data.get('confidence', 'N/A')}")
                resultados.append((nombre, True, data))
            else:
                print(f"  [FAIL] No se obtuvieron datos ({elapsed:.2f}s)")
                resultados.append((nombre, False, None))
                
        except Exception as e:
            print(f"  [ERROR] {e}")
            resultados.append((nombre, False, None))
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE INSTRUMENTOS")
    print("="*80)
    
    exitosos = sum(1 for _, success, _ in resultados if success)
    total = len(resultados)
    
    for nombre, success, data in resultados:
        status = "[OK]" if success else "[FAIL]"
        valor = f"= {data.get('value', 'N/A')}" if data else ""
        print(f"  {status} {nombre:30s} {valor}")
    
    print(f"\nTotal: {exitosos}/{total} instrumentos funcionando ({exitosos/total*100:.0f}%)")
    
    return resultados

# Test de análisis completo (si hay instrumentos funcionando)
async def test_analisis_completo(resultados_instrumentos):
    """Test de análisis completo si hay instrumentos"""
    
    exitosos = sum(1 for _, success, _ in resultados_instrumentos if success)
    
    if exitosos == 0:
        print("\n[SKIP] No hay instrumentos funcionando - saltando analisis completo")
        return
    
    print("\n" + "="*80)
    print("TEST DE ANALISIS COMPLETO")
    print("="*80)
    
    try:
        from core_anomaly_detector import CoreAnomalyDetector
        from environment_classifier import EnvironmentClassifier
        from validation.real_archaeological_validator import RealArchaeologicalValidator
        
        env_classifier = EnvironmentClassifier()
        real_validator = RealArchaeologicalValidator()
        
        detector = CoreAnomalyDetector(
            environment_classifier=env_classifier,
            real_validator=real_validator,
            data_loader=None
        )
        
        result = await detector.detect_anomaly(
            lat=-50.4760,
            lon=-73.0450,
            lat_min=-50.55,
            lat_max=-50.40,
            lon_min=-73.15,
            lon_max=-72.90,
            region_name="Patagonia Proglaciar - Candidato #001"
        )
        
        print(f"\n[RESULTADO] Anomalia: {'SI' if result.anomaly_detected else 'NO'}")
        print(f"[CONFIANZA] {result.confidence_level}")
        print(f"[PROBABILIDAD] {result.archaeological_probability:.1%}")
        print(f"[INSTRUMENTOS] {len(result.measurements)} midiendo")
        print(f"[CONVERGENCIA] {result.instruments_converging}/{result.minimum_required}")
        
        if result.measurements:
            print("\nMediciones:")
            for m in result.measurements:
                print(f"  - {m.instrument_name}: {m.value:.2f} {m.unit} (umbral: {m.threshold:.2f})")
        
    except Exception as e:
        print(f"\n[ERROR] Analisis completo fallo: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Ejecutar tests"""
    
    # Test 1: Instrumentos individuales
    resultados = await test_instrumentos()
    
    # Test 2: Análisis completo (si hay instrumentos)
    await test_analisis_completo(resultados)
    
    print("\n" + "="*80)
    print("TEST COMPLETADO")
    print("="*80)
    print("\nVer detalles en: instrument_diagnostics.log")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
