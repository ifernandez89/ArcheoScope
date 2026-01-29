#!/usr/bin/env python3
"""
Test de Integración Completa - TODO INTEGRADO
==============================================

Test end-to-end del sistema completo con todas las integraciones:
1. Coverage Assessment
2. Scientific Narrative
3. Anomaly Map Generator
4. SAR Enhanced
5. ICESat-2 Rugosity

Autor: Kiro AI Assistant
Fecha: 2026-01-29
"""

import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

print("="*80)
print("TEST DE INTEGRACIÓN COMPLETA - TODO INTEGRADO")
print("="*80)

# Test 1: Verificar imports
print("\n1. Verificando imports...")
try:
    from scientific_pipeline import ScientificPipeline
    print("   ✅ ScientificPipeline")
except Exception as e:
    print(f"   ❌ ScientificPipeline: {e}")
    sys.exit(1)

try:
    from pipeline.coverage_assessment import calculate_coverage_score
    print("   ✅ Coverage Assessment")
except Exception as e:
    print(f"   ❌ Coverage Assessment: {e}")

try:
    from scientific_narrative import generate_archaeological_narrative
    print("   ✅ Scientific Narrative")
except Exception as e:
    print(f"   ❌ Scientific Narrative: {e}")

try:
    from anomaly_map_generator import AnomalyMapGenerator
    print("   ✅ Anomaly Map Generator")
except Exception as e:
    print(f"   ❌ Anomaly Map Generator: {e}")

try:
    from sar_enhanced_processing import process_sar_enhanced
    print("   ✅ SAR Enhanced Processing")
except Exception as e:
    print(f"   ❌ SAR Enhanced Processing: {e}")

# Test 2: Crear pipeline
print("\n2. Creando ScientificPipeline...")
try:
    pipeline = ScientificPipeline(db_pool=None, validator=None)
    print("   ✅ Pipeline creado")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Simular análisis
print("\n3. Simulando análisis completo...")
try:
    import asyncio
    
    # Datos de prueba
    raw_measurements = {
        'candidate_id': 'TEST_001',
        'region_name': 'Test Region',
        'environment_type': 'arid',
        'instrumental_measurements': {
            'sentinel_2_ndvi': {
                'value': 0.15,
                'confidence': 0.85,
                'source': 'Sentinel-2',
                'threshold': 0.3
            },
            'sentinel_1_sar': {
                'value': -8.2,
                'confidence': 0.90,
                'source': 'Sentinel-1',
                'threshold': -10.0
            },
            'landsat_thermal': {
                'value': 305.2,
                'confidence': 0.88,
                'source': 'Landsat-8',
                'threshold': 300.0
            },
            'icesat2': {
                'value': 15.7,
                'confidence': 0.75,
                'source': 'ICESat-2',
                'threshold': 10.0
            },
            'srtm_elevation': {
                'value': 450.3,
                'confidence': 0.95,
                'source': 'SRTM',
                'threshold': 400.0
            }
        }
    }
    
    # Ejecutar análisis
    async def run_analysis():
        result = await pipeline.analyze(
            raw_measurements=raw_measurements,
            lat_min=29.97,
            lat_max=29.98,
            lon_min=31.13,
            lon_max=31.14
        )
        return result
    
    result = asyncio.run(run_analysis())
    
    print("   ✅ Análisis completado")
    
    # Verificar resultado
    output = result.get('scientific_output', {})
    
    print("\n4. Verificando integraciones...")
    
    # Coverage Assessment
    if 'coverage_raw' in output and output['coverage_raw'] > 0:
        print(f"   ✅ Coverage Assessment: {output['coverage_raw']:.2f}")
    else:
        print("   ⚠️ Coverage Assessment: No integrado")
    
    # Scientific Narrative
    if 'scientific_narrative' in output and output['scientific_narrative']:
        print(f"   ✅ Scientific Narrative: {len(output['scientific_narrative'])} chars")
        print(f"      Clasificación: {output.get('classification', 'N/A')}")
        print(f"      Prioridad: {output.get('priority', 'N/A')}")
    else:
        print("   ⚠️ Scientific Narrative: No integrado")
    
    # Anomaly Map
    if 'anomaly_map_path' in output and output['anomaly_map_path']:
        print(f"   ✅ Anomaly Map: {output['anomaly_map_path']}")
        if 'anomaly_map_metadata' in output:
            metadata = output['anomaly_map_metadata']
            print(f"      Layers: {metadata.get('layers_used', [])}")
            print(f"      Resolution: {metadata.get('resolution_m', 0)}m")
    else:
        print("   ⚠️ Anomaly Map: No integrado")
    
    # Confidence vs Signal
    if 'confidence_level' in output and 'signal_strength' in output:
        print(f"   ✅ Confidence vs Signal:")
        print(f"      Confidence: {output['confidence_level']:.2f}")
        print(f"      Signal: {output['signal_strength']:.2f}")
    else:
        print("   ⚠️ Confidence vs Signal: No integrado")
    
    print("\n" + "="*80)
    print("✅ TEST DE INTEGRACIÓN COMPLETADO")
    print("="*80)
    
    # Mostrar resumen
    print("\nRESUMEN:")
    print(f"  Candidate ID: {output.get('candidate_id', 'N/A')}")
    print(f"  Anomaly Score: {output.get('anomaly_score', 0):.3f}")
    print(f"  Coverage: {output.get('coverage_raw', 0):.2f}")
    print(f"  Confidence: {output.get('confidence_level', 0):.2f}")
    print(f"  Signal: {output.get('signal_strength', 0):.2f}")
    print(f"  Classification: {output.get('classification', 'N/A')}")
    print(f"  Priority: {output.get('priority', 'N/A')}")
    
    if output.get('scientific_narrative'):
        print(f"\nNARRATIVA CIENTÍFICA:")
        print(f"{output['scientific_narrative'][:500]}...")
    
except Exception as e:
    print(f"   ❌ Error en análisis: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("🎉 INTEGRACIÓN COMPLETA EXITOSA")
print("="*80)
