#!/usr/bin/env python3
"""
Test rápido para diagnosticar estado de instrumentos
"""

import sys
import asyncio
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_instruments():
    """Test de instrumentos"""
    
    print("="*80)
    print("DIAGNÓSTICO DE INSTRUMENTOS")
    print("="*80)
    
    # Test 1: Verificar que RealDataIntegrator funciona
    print("\n1. Verificando RealDataIntegrator...")
    try:
        from satellite_connectors.real_data_integrator import RealDataIntegrator
        integrator = RealDataIntegrator()
        print("   [OK] RealDataIntegrator inicializado")
        
        # Verificar instrumentos disponibles
        available = integrator.get_available_instruments()
        print(f"   [OK] Instrumentos disponibles: {sum(available.values())}/{len(available)}")
        for name, status in available.items():
            status_mark = "OK" if status else "FAIL"
            print(f"      {name}: {status_mark}")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Verificar que CoreAnomalyDetector se inicializa
    print("\n2. Verificando CoreAnomalyDetector...")
    detector = None
    db_instance = None
    try:
        from environment_classifier import EnvironmentClassifier
        from validation.real_archaeological_validator import RealArchaeologicalValidator
        # Importar directamente desde el archivo database.py
        sys.path.insert(0, str(Path(__file__).parent / "backend"))
        from database import ArcheoScopeDB
        
        # Inicializar componentes
        env_classifier = EnvironmentClassifier()
        print("   [OK] EnvironmentClassifier inicializado")
        
        # Conectar a BD
        db_instance = ArcheoScopeDB()
        await db_instance.connect()
        validator = RealArchaeologicalValidator(db_instance)
        print("   [OK] RealArchaeologicalValidator inicializado")
        
        # Inicializar detector
        from core_anomaly_detector import CoreAnomalyDetector
        detector = CoreAnomalyDetector(
            environment_classifier=env_classifier,
            real_validator=validator,
            data_loader=None
        )
        print("   [OK] CoreAnomalyDetector inicializado")
        
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 3: Test de medición simple
    print("\n3. Test de medición simple (Giza)...")
    if detector is None:
        print("   [SKIP] Detector no inicializado, saltando test")
        return
        
    try:
        # Coordenadas de Giza
        lat_min, lat_max = 29.97, 29.98
        lon_min, lon_max = 31.13, 31.14
        
        result = await detector.detect_anomaly(
            lat=29.975,
            lon=31.135,
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max,
            region_name="Giza Test"
        )
        
        print(f"   [OK] Análisis completado")
        print(f"   Instrumentos que midieron: {len(result.measurements)}")
        print(f"   Anomalía detectada: {result.anomaly_detected}")
        
        # Mostrar detalles de mediciones
        if result.measurements:
            print("\n   Mediciones:")
            for m in result.measurements:
                print(f"      - {m.instrument_name}: {m.value:.3f} {m.unit} (umbral: {m.threshold:.3f})")
        else:
            print("   [WARN] ¡0 instrumentos midieron!")
            
            # Verificar si el log de diagnóstico existe
            import os
            if os.path.exists('instrument_diagnostics.log'):
                print("\n   Log de diagnóstico encontrado:")
                with open('instrument_diagnostics.log', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Mostrar últimas 50 líneas
                    for line in lines[-50:]:
                        print(f"      {line.rstrip()}")
            else:
                print("   [CRITICAL] ¡Log de diagnóstico NO EXISTE!")
                print("   Esto significa que _measure_with_instruments() NO SE EJECUTÓ")
        
        if db_instance:
            await db_instance.close()
        
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("DIAGNÓSTICO COMPLETADO")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_instruments())
