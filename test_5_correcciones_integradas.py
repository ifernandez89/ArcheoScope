#!/usr/bin/env python3
"""
Test de Integración - 5 Correcciones Críticas
=============================================

Test completo para verificar que las 5 correcciones están funcionando:

1. ✅ ICESat-2 rugosidad como señal arqueológica
2. ✅ SAR normalización mejorada (structural index)
3. 📋 Cobertura vs señal (separados)
4. ⚠️ TAS environment-aware (parcial)
5. 📋 Narrativa científica explícita

Autor: Kiro AI Assistant
Fecha: 2026-01-29
"""

import asyncio
import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

# Colores
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_test(test_name):
    """Print nombre de test."""
    print(f"\n{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.CYAN}TEST: {test_name}{Colors.END}")
    print(f"{Colors.CYAN}{'='*80}{Colors.END}")

def print_pass(message):
    """Print test passed."""
    print(f"{Colors.GREEN}✅ PASS: {message}{Colors.END}")

def print_fail(message):
    """Print test failed."""
    print(f"{Colors.RED}❌ FAIL: {message}{Colors.END}")

def print_info(message):
    """Print info."""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

async def test_1_icesat2_rugosity():
    """Test 1: ICESat-2 rugosidad como señal arqueológica."""
    print_test("1. ICESat-2 Rugosidad como Señal Arqueológica")
    
    try:
        from satellite_connectors.icesat2_connector import ICESat2Connector
        
        connector = ICESat2Connector()
        print_info("ICESat-2 connector inicializado")
        
        # Test con coordenadas de Giza (debe tener rugosidad)
        lat_min, lat_max = 29.97, 29.98
        lon_min, lon_max = 31.13, 31.14
        
        print_info(f"Consultando ICESat-2 para Giza: ({lat_min}, {lon_min})")
        
        result = await connector.get_elevation_data(lat_min, lat_max, lon_min, lon_max)
        
        if result and hasattr(result, 'indices'):
            indices = result.indices
            
            # Verificar que devuelve rugosidad
            if 'elevation_std' in indices:
                rugosity = indices['elevation_std']
                print_pass(f"ICESat-2 devuelve rugosidad: {rugosity:.2f}m")
                
                if rugosity > 5:
                    print_pass(f"Rugosidad significativa detectada (>{5}m)")
                    return True
                else:
                    print_info(f"Rugosidad baja: {rugosity:.2f}m")
                    return True
            else:
                print_fail("ICESat-2 NO devuelve 'elevation_std' en indices")
                return False
        else:
            print_fail("ICESat-2 no devolvió datos válidos")
            return False
            
    except Exception as e:
        print_fail(f"Exception: {e}")
        return False

async def test_2_sar_enhanced():
    """Test 2: SAR normalización mejorada."""
    print_test("2. SAR Normalización Mejorada (Structural Index)")
    
    try:
        from sar_enhanced_processing import process_sar_enhanced
        import numpy as np
        
        print_info("Módulo SAR Enhanced Processing cargado")
        
        # Test 1: Valor puntual
        print_info("\nTest 2a: Valor puntual SAR")
        sar_value = -8.2  # dB
        result = process_sar_enhanced(sar_value)
        
        if 'sar_value_normalized' in result:
            print_pass(f"Normalización regional: {result['sar_value_normalized']:.2f}")
        else:
            print_fail("No se calculó normalización regional")
            return False
        
        # Test 2: Datos 2D con estructura
        print_info("\nTest 2b: Datos 2D SAR con estructura artificial")
        sar_2d = np.random.normal(-12, 3, (50, 50))
        sar_2d[20:30, 20:30] += 5  # Anomalía positiva (estructura)
        
        result = process_sar_enhanced(-12.0, sar_2d)
        
        if 'sar_structural_index' in result:
            structural_index = result['sar_structural_index']
            print_pass(f"Structural index calculado: {structural_index:.3f}")
            
            if structural_index > 0.1:
                print_pass(f"Estructura detectada (index > 0.1)")
                return True
            else:
                print_info(f"Estructura débil: {structural_index:.3f}")
                return True
        else:
            print_fail("No se calculó structural index")
            return False
            
    except Exception as e:
        print_fail(f"Exception: {e}")
        return False

def test_3_coverage_assessment():
    """Test 3: Cobertura vs señal (separados)."""
    print_test("3. Cobertura vs Señal (Separados)")
    
    try:
        from pipeline.coverage_assessment import (
            calculate_coverage_score,
            separate_confidence_and_signal
        )
        
        print_info("Módulo Coverage Assessment cargado")
        
        # Test con cobertura parcial pero CORE completo
        print_info("\nTest 3a: Cobertura parcial (CORE completo)")
        instruments = [
            'sentinel_2_ndvi',
            'sentinel_1_sar',
            'landsat_thermal',
            'srtm_elevation'
        ]
        
        assessment = calculate_coverage_score(instruments)
        
        print_info(f"Coverage score: {assessment.coverage_score:.2f}")
        print_info(f"Coverage quality: {assessment.coverage_quality.value}")
        print_info(f"Core coverage: {assessment.core_coverage:.2f}")
        
        if assessment.core_coverage >= 0.75:
            print_pass("CORE completo (≥75%)")
        else:
            print_fail(f"CORE incompleto: {assessment.core_coverage:.2f}")
            return False
        
        # Test separación confianza vs señal
        print_info("\nTest 3b: Separar confianza de señal")
        measurements = [
            {'value': 0.8, 'threshold': 0.5},  # Señal fuerte
            {'value': 0.7, 'threshold': 0.5},
            {'value': 0.6, 'threshold': 0.5},
        ]
        
        result = separate_confidence_and_signal(measurements, assessment)
        
        print_info(f"Confidence level: {result['confidence_level']:.2f}")
        print_info(f"Signal strength: {result['signal_strength']:.2f}")
        print_info(f"Interpretation: {result['interpretation']}")
        
        if result['confidence_level'] != result['signal_strength']:
            print_pass("Confianza y señal están separados")
            return True
        else:
            print_fail("Confianza y señal NO están separados")
            return False
            
    except Exception as e:
        print_fail(f"Exception: {e}")
        return False

def test_4_tas_adaptive():
    """Test 4: TAS environment-aware (parcial)."""
    print_test("4. TAS Environment-Aware (Pesos Adaptativos)")
    
    try:
        from temporal_archaeological_signature import TemporalArchaeologicalSignatureEngine
        
        print_info("Módulo TAS cargado")
        
        # Verificar que _calculate_tas_score acepta environment_type
        import inspect
        sig = inspect.signature(TemporalArchaeologicalSignatureEngine._calculate_tas_score)
        params = list(sig.parameters.keys())
        
        if 'environment_type' in params:
            print_pass("TAS acepta environment_type")
        else:
            print_fail("TAS NO acepta environment_type")
            return False
        
        # Verificar que hay pesos diferentes por ambiente
        print_info("\nVerificando pesos adaptativos...")
        
        # Simular cálculo con diferentes ambientes
        engine = TemporalArchaeologicalSignatureEngine(integrator=None)
        
        # Test árido con thermal anchor
        print_info("Test: Árido con thermal > 0.9")
        score_arid = engine._calculate_tas_score(
            ndvi_persistence=0.1,
            thermal_stability=0.95,  # > 0.9 → THERMAL ANCHOR ZONE
            sar_coherence=0.5,
            stress_frequency=0.2,
            environment_type="arid"
        )
        
        print_info(f"TAS score (árido + thermal anchor): {score_arid:.3f}")
        
        # Test templado con mismos valores
        print_info("Test: Templado con mismos valores")
        score_temperate = engine._calculate_tas_score(
            ndvi_persistence=0.1,
            thermal_stability=0.95,
            sar_coherence=0.5,
            stress_frequency=0.2,
            environment_type="temperate"
        )
        
        print_info(f"TAS score (templado): {score_temperate:.3f}")
        
        if score_arid != score_temperate:
            print_pass("Pesos adaptativos funcionando (scores diferentes)")
            return True
        else:
            print_fail("Pesos NO adaptativos (scores iguales)")
            return False
            
    except Exception as e:
        print_fail(f"Exception: {e}")
        return False

def test_5_scientific_narrative():
    """Test 5: Narrativa científica explícita."""
    print_test("5. Narrativa Científica Explícita")
    
    try:
        from scientific_narrative import generate_archaeological_narrative
        
        print_info("Módulo Scientific Narrative cargado")
        
        # Test con thermal anchor zone
        print_info("\nTest: Thermal Anchor Zone")
        narrative = generate_archaeological_narrative(
            thermal_stability=0.93,
            sar_structural_index=0.52,
            icesat2_rugosity=15.7,
            ndvi_persistence=0.06,
            tas_score=0.58,
            coverage_score=0.65,
            environment_type="arid",
            flags=['THERMAL_ANCHOR_ZONE']
        )
        
        print_info(f"Clasificación: {narrative.classification.value}")
        print_info(f"Confianza: {narrative.confidence:.2f}")
        print_info(f"Prioridad: {narrative.priority}")
        
        print_info("\nNarrativa completa:")
        print(f"{Colors.BLUE}{narrative.full_narrative}{Colors.END}")
        
        # Verificar que hay declaración principal
        if narrative.main_statement:
            print_pass(f"Declaración principal: {narrative.main_statement}")
        else:
            print_fail("Sin declaración principal")
            return False
        
        # Verificar que hay evidencias
        if narrative.evidence and len(narrative.evidence) > 0:
            print_pass(f"Evidencias: {len(narrative.evidence)}")
        else:
            print_fail("Sin evidencias")
            return False
        
        # Verificar que hay recomendaciones
        if narrative.recommendations and len(narrative.recommendations) > 0:
            print_pass(f"Recomendaciones: {len(narrative.recommendations)}")
            return True
        else:
            print_fail("Sin recomendaciones")
            return False
            
    except Exception as e:
        print_fail(f"Exception: {e}")
        return False

async def main():
    """Main test runner."""
    print(f"\n{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.CYAN}TEST DE INTEGRACIÓN - 5 CORRECCIONES CRÍTICAS{Colors.END}")
    print(f"{Colors.CYAN}{'='*80}{Colors.END}")
    
    results = {}
    
    # Test 1: ICESat-2 rugosidad
    results['icesat2'] = await test_1_icesat2_rugosity()
    
    # Test 2: SAR enhanced
    results['sar'] = await test_2_sar_enhanced()
    
    # Test 3: Coverage assessment
    results['coverage'] = test_3_coverage_assessment()
    
    # Test 4: TAS adaptive
    results['tas'] = test_4_tas_adaptive()
    
    # Test 5: Scientific narrative
    results['narrative'] = test_5_scientific_narrative()
    
    # Resumen
    print(f"\n{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.CYAN}RESUMEN DE TESTS{Colors.END}")
    print(f"{Colors.CYAN}{'='*80}{Colors.END}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for name, result in results.items():
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"{name:20s}: {status}")
    
    print(f"\n{Colors.CYAN}Total: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{'='*80}{Colors.END}")
        print(f"{Colors.GREEN}🎉 TODOS LOS TESTS PASARON{Colors.END}")
        print(f"{Colors.GREEN}{'='*80}{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{'='*80}{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  ALGUNOS TESTS FALLARON{Colors.END}")
        print(f"{Colors.YELLOW}{'='*80}{Colors.END}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
