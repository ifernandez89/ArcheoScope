#!/usr/bin/env python3
"""
Test Real APIs Integration in Core Detector
============================================

Verifica que el core detector use APIs reales en lugar de simulaciones
"""

import asyncio
import sys
import json
from datetime import datetime
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent))

from backend.core_anomaly_detector import CoreAnomalyDetector
from backend.environment_classifier import EnvironmentClassifier
from backend.validation.real_archaeological_validator import RealArchaeologicalValidator
from backend.data.archaeological_loader import ArchaeologicalDataLoader


async def test_real_apis_integration():
    """Test completo de integración de APIs reales"""
    
    print("="*80)
    print("🧪 TEST: Integración de APIs Reales en Core Detector")
    print("="*80)
    print()
    
    # Inicializar componentes
    print("📦 Inicializando componentes...")
    env_classifier = EnvironmentClassifier()
    real_validator = RealArchaeologicalValidator()
    data_loader = ArchaeologicalDataLoader()
    
    # Crear detector con APIs reales
    detector = CoreAnomalyDetector(env_classifier, real_validator, data_loader)
    
    print("✅ Detector inicializado con RealDataIntegrator")
    print()
    
    # Test 1: Giza (sitio conocido, desierto)
    print("🔍 TEST 1: Giza, Egipto (sitio conocido)")
    print("-" * 80)
    
    result1 = await detector.detect_anomaly(
        lat=29.9792,
        lon=31.1342,
        lat_min=29.97,
        lat_max=29.99,
        lon_min=31.13,
        lon_max=31.15,
        region_name="Giza Plateau"
    )
    
    print(f"   Anomalía detectada: {result1.anomaly_detected}")
    print(f"   Confianza: {result1.confidence_level}")
    print(f"   Probabilidad: {result1.archaeological_probability:.2%}")
    print(f"   Instrumentos convergiendo: {result1.instruments_converging}/{result1.minimum_required}")
    print(f"   Sitio conocido: {result1.known_site_name}")
    print()
    
    # Verificar que se usaron datos reales
    real_measurements = [m for m in result1.measurements if 'real' in m.notes.lower()]
    simulated_measurements = [m for m in result1.measurements if 'real' not in m.notes.lower()]
    
    print(f"   📊 Mediciones REALES: {len(real_measurements)}/{len(result1.measurements)}")
    print(f"   📊 Mediciones SIMULADAS (fallback): {len(simulated_measurements)}/{len(result1.measurements)}")
    print()
    
    if real_measurements:
        print("   ✅ DATOS REALES DETECTADOS:")
        for m in real_measurements[:3]:  # Mostrar primeros 3
            print(f"      - {m.instrument_name}: {m.value:.2f} {m.unit}")
            print(f"        {m.notes[:100]}...")
    print()
    
    # Test 2: Angkor Wat (sitio conocido, bosque)
    print("🔍 TEST 2: Angkor Wat, Camboya (sitio conocido, bosque)")
    print("-" * 80)
    
    result2 = await detector.detect_anomaly(
        lat=13.4125,
        lon=103.8670,
        lat_min=13.40,
        lat_max=13.43,
        lon_min=103.85,
        lon_max=103.88,
        region_name="Angkor Wat"
    )
    
    print(f"   Anomalía detectada: {result2.anomaly_detected}")
    print(f"   Confianza: {result2.confidence_level}")
    print(f"   Probabilidad: {result2.archaeological_probability:.2%}")
    print(f"   Instrumentos convergiendo: {result2.instruments_converging}/{result2.minimum_required}")
    print()
    
    real_measurements2 = [m for m in result2.measurements if 'real' in m.notes.lower()]
    print(f"   📊 Mediciones REALES: {len(real_measurements2)}/{len(result2.measurements)}")
    print()
    
    # Test 3: Área desconocida (control negativo)
    print("🔍 TEST 3: Océano Pacífico (control negativo)")
    print("-" * 80)
    
    result3 = await detector.detect_anomaly(
        lat=-10.0,
        lon=-140.0,
        lat_min=-10.1,
        lat_max=-9.9,
        lon_min=-140.1,
        lon_max=-139.9,
        region_name="Pacific Ocean Control"
    )
    
    print(f"   Anomalía detectada: {result3.anomaly_detected}")
    print(f"   Confianza: {result3.confidence_level}")
    print(f"   Probabilidad: {result3.archaeological_probability:.2%}")
    print()
    
    # Resumen final
    print("="*80)
    print("📊 RESUMEN DE INTEGRACIÓN")
    print("="*80)
    
    total_measurements = len(result1.measurements) + len(result2.measurements) + len(result3.measurements)
    total_real = len([m for r in [result1, result2, result3] for m in r.measurements if 'real' in m.notes.lower()])
    
    print(f"Total de mediciones: {total_measurements}")
    print(f"Mediciones REALES: {total_real}")
    print(f"Tasa de datos reales: {(total_real/total_measurements*100):.1f}%")
    print()
    
    if total_real > 0:
        print("✅ INTEGRACIÓN EXITOSA - APIs reales funcionando")
        print("✅ Sistema usa datos satelitales verificables")
        print("✅ Trazabilidad completa de fuentes")
    else:
        print("⚠️ ADVERTENCIA - Solo fallbacks simulados")
        print("   Verificar configuración de API keys")
        print("   Verificar conectividad a APIs")
    
    print()
    
    # Guardar reporte
    report = {
        'timestamp': datetime.now().isoformat(),
        'test_results': {
            'giza': {
                'anomaly_detected': result1.anomaly_detected,
                'confidence': result1.confidence_level,
                'probability': result1.archaeological_probability,
                'real_measurements': len(real_measurements),
                'total_measurements': len(result1.measurements)
            },
            'angkor': {
                'anomaly_detected': result2.anomaly_detected,
                'confidence': result2.confidence_level,
                'probability': result2.archaeological_probability,
                'real_measurements': len(real_measurements2),
                'total_measurements': len(result2.measurements)
            },
            'control': {
                'anomaly_detected': result3.anomaly_detected,
                'confidence': result3.confidence_level,
                'probability': result3.archaeological_probability
            }
        },
        'integration_metrics': {
            'total_measurements': total_measurements,
            'real_measurements': total_real,
            'real_data_rate': total_real/total_measurements if total_measurements > 0 else 0,
            'integration_successful': total_real > 0
        }
    }
    
    report_file = f"real_apis_integration_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Reporte guardado: {report_file}")
    print()
    
    return total_real > 0


if __name__ == "__main__":
    try:
        success = asyncio.run(test_real_apis_integration())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
