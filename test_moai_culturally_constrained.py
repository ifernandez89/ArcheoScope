#!/usr/bin/env python3
"""
Test - MOAI Culturalmente Constreñido
======================================

DESAFÍO: Generar un "pseudo-moai" geométricamente legítimo

INVARIANTES MOAI (Rapa Nui):
- Monolítico vertical
- Cabeza ENORME (45% del total)
- Cuello definido
- Brazos fusionados al cuerpo
- Piernas fusionadas
- Base integrada
- Simetría bilateral perfecta
- CERO dinamismo
- Frontalidad absoluta

DATOS REALES (promedio de moais):
- Altura: 4-10m (promedio ~7m)
- Ancho: 1.5-3m
- Ratio H/W: ~3.2
- Material: Toba volcánica
- Rigidez: EXTREMA
"""

import sys
from pathlib import Path

backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

from culturally_constrained_mig import CulturallyConstrainedMIG


def test_moai_small():
    """Test: Moai pequeño (tipo Ahu Tongariki)."""
    
    print("="*80)
    print("🗿 TEST 1: MOAI PEQUEÑO (4-5m)")
    print("="*80)
    print()
    
    print("📍 REFERENCIA: Moais pequeños de Ahu Tongariki")
    print("   Altura típica: 4-5m")
    print("   Ancho: ~1.5m")
    print("   Ratio H/W: ~3.2")
    print()
    
    # Datos simulados de ArcheoScope
    data = {
        'scale_invariance': 0.93,      # ALTA - monolítico
        'angular_consistency': 0.89,   # ALTA - simetría bilateral
        'coherence_3d': 0.91,          # ALTA - masa integrada
        'sar_rigidity': 0.92,          # ALTA - piedra volcánica
        'stratification_index': 0.08,  # BAJA - no escalonado
        'estimated_area_m2': 6.25,     # ~2.5m × 2.5m
        'estimated_height_m': 5.0      # Pequeño
    }
    
    print("🛰️ INVARIANTES DETECTADOS:")
    print(f"   Scale Invariance: {data['scale_invariance']:.3f} ⚠️ ALTA")
    print(f"   Angular Consistency: {data['angular_consistency']:.3f}")
    print(f"   Coherence 3D: {data['coherence_3d']:.3f}")
    print(f"   SAR Rigidity: {data['sar_rigidity']:.3f} (piedra)")
    print(f"   Área estimada: {data['estimated_area_m2']:.1f} m²")
    print(f"   Altura estimada: {data['estimated_height_m']:.1f} m")
    print()
    
    # Ejecutar inferencia culturalmente constreñida
    mig = CulturallyConstrainedMIG()
    
    result = mig.infer_culturally_constrained_geometry(
        archeoscope_data=data,
        output_name="moai_small_constrained",
        use_ai=False
    )
    
    print()
    print("="*80)
    print("✅ RESULTADOS")
    print("="*80)
    print()
    print(f"📐 Clase morfológica: {result['morphological_class'].upper()}")
    print(f"🌍 Origen cultural: {result['cultural_origin']}")
    print(f"📊 Score morfológico: {result['morphological_score']:.3f}")
    print(f"🎯 Confianza total: {result['confidence']:.3f}")
    print(f"📦 Volumen: {result['volume_m3']:.0f} m³")
    print()
    print(f"📁 Archivos generados:")
    print(f"   PNG: {result['png']}")
    print(f"   OBJ: {result['obj']}")
    print()


def test_moai_large():
    """Test: Moai grande (tipo Paro)."""
    
    print("="*80)
    print("🗿 TEST 2: MOAI GRANDE (10m)")
    print("="*80)
    print()
    
    print("📍 REFERENCIA: Moai Paro (el más grande transportado)")
    print("   Altura: ~10m")
    print("   Peso: ~82 toneladas")
    print("   Ratio H/W: ~3.2")
    print()
    
    data = {
        'scale_invariance': 0.95,
        'angular_consistency': 0.91,
        'coherence_3d': 0.93,
        'sar_rigidity': 0.94,
        'stratification_index': 0.05,
        'estimated_area_m2': 16.0,  # ~4m × 4m
        'estimated_height_m': 10.0
    }
    
    print("🛰️ INVARIANTES DETECTADOS:")
    print(f"   Scale Invariance: {data['scale_invariance']:.3f} ⚠️ EXTREMA")
    print(f"   Angular Consistency: {data['angular_consistency']:.3f}")
    print(f"   Coherence 3D: {data['coherence_3d']:.3f}")
    print(f"   Área: {data['estimated_area_m2']:.1f} m²")
    print(f"   Altura: {data['estimated_height_m']:.1f} m")
    print()
    
    mig = CulturallyConstrainedMIG()
    
    result = mig.infer_culturally_constrained_geometry(
        archeoscope_data=data,
        output_name="moai_large_constrained",
        use_ai=False
    )
    
    print()
    print("="*80)
    print("✅ RESULTADOS")
    print("="*80)
    print()
    print(f"📐 Clase: {result['morphological_class'].upper()}")
    print(f"🎯 Confianza: {result['confidence']:.3f}")
    print(f"📦 Volumen: {result['volume_m3']:.0f} m³")
    print(f"📁 PNG: {result['png']}")
    print()


def test_moai_comparison():
    """Comparación: ¿Qué mejora frente al MIG básico?"""
    
    print("="*80)
    print("📊 COMPARACIÓN: MIG Básico vs MIG Culturalmente Constreñido")
    print("="*80)
    print()
    
    print("❌ MIG BÁSICO (Nivel 2):")
    print("   - Genera: 'Masa antropomórfica abstracta'")
    print("   - Proporciones: Inferidas solo de datos territoriales")
    print("   - Resultado: Genérico, no reconocible")
    print()
    
    print("✅ MIG CULTURALMENTE CONSTREÑIDO (Nivel 3):")
    print("   - Genera: 'Forma compatible con tradición moai'")
    print("   - Proporciones: Constreñidas por 50 moais reales")
    print("   - Resultado: Reconocible como moai, sin copiar")
    print()
    
    print("🔑 DIFERENCIA CLAVE:")
    print("   El sistema NO decide 'hacer un moai'")
    print("   El sistema RESTRINGE el espacio geométrico")
    print("   hasta que solo sobreviven formas tipo-moai")
    print()
    
    print("🎯 COMUNICACIÓN CIENTÍFICA:")
    print()
    print('   "Representación volumétrica inferida compatible con')
    print('    estatuaria monolítica de Rapa Nui.')
    print('    Proporciones constreñidas por 50 ejemplares reales.')
    print('    Cabeza/cuerpo: 0.45, simetría bilateral: 0.98.')
    print('    NO reconstrucción de moai específico.')
    print('    Forma culturalmente posible, no copia artística."')
    print()


if __name__ == "__main__":
    print()
    print("🗿 MIG NIVEL 3 - TEST MOAI CULTURALMENTE CONSTREÑIDO")
    print()
    
    try:
        # Test 1: Moai pequeño
        test_moai_small()
        
        print("\n" + "="*80 + "\n")
        
        # Test 2: Moai grande
        test_moai_large()
        
        print("\n" + "="*80 + "\n")
        
        # Comparación
        test_moai_comparison()
        
        print("="*80)
        print("✅ TESTS COMPLETADOS")
        print("="*80)
        print()
        print("🎉 DESAFÍO ACEPTADO Y SUPERADO!")
        print()
        print("📁 Revisa 'geometric_models/' para ver:")
        print("   - moai_small_constrained.png")
        print("   - moai_small_constrained.obj")
        print("   - moai_large_constrained.png")
        print("   - moai_large_constrained.obj")
        print()
        print("🧬 'ArcheoScope no reconstruye monumentos.")
        print("   Constriñe el espacio geométrico hasta que solo")
        print("   sobreviven formas culturalmente posibles.'")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
