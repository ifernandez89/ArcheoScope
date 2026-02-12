#!/usr/bin/env python3
"""
Test - ESFINGE Culturalmente Constreñida
=========================================

DESAFÍO: Generar una "esfinge estructuralmente compatible"

INVARIANTES ESFINGE (Egipto):
- Híbrido humano-animal
- Cuerpo horizontal (león)
- Cabeza vertical (humana)
- Transición gradual cabeza-cuerpo
- Patas delanteras extendidas
- Base integrada al sustrato
- Simetría bilateral perfecta
- CERO dinamismo

DATOS REALES (Gran Esfinge de Giza):
- Longitud: ~73m
- Ancho: ~19m
- Altura: ~20m
- Ratio L/H: ~3.65 (muy horizontal)
- Material: Piedra caliza
- Erosión: EXTREMA
"""

import sys
from pathlib import Path

backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

from culturally_constrained_mig import CulturallyConstrainedMIG


def test_sphinx_giza_scale():
    """Test: Esfinge escala Giza."""
    
    print("="*80)
    print("🦁 TEST 1: ESFINGE ESCALA GIZA")
    print("="*80)
    print()
    
    print("📍 REFERENCIA: Gran Esfinge de Giza")
    print("   Longitud: ~73m")
    print("   Ancho: ~19m")
    print("   Altura: ~20m")
    print("   Ratio L/H: ~3.65 (horizontal)")
    print()
    
    # Datos simulados de ArcheoScope
    data = {
        'scale_invariance': 0.96,      # EXTREMA - monolítico
        'angular_consistency': 0.94,   # EXTREMA - simetría perfecta
        'coherence_3d': 0.89,          # ALTA - masa integrada
        'sar_rigidity': 0.91,          # ALTA - piedra caliza
        'stratification_index': 0.12,  # BAJA - no escalonado
        'estimated_area_m2': 1387.0,   # ~73m × 19m
        'estimated_height_m': 20.0     # Horizontal dominante
    }
    
    print("🛰️ INVARIANTES DETECTADOS:")
    print(f"   Scale Invariance: {data['scale_invariance']:.3f} ⚠️ EXTREMA")
    print(f"   Angular Consistency: {data['angular_consistency']:.3f} ⚠️ EXTREMA")
    print(f"   Coherence 3D: {data['coherence_3d']:.3f}")
    print(f"   SAR Rigidity: {data['sar_rigidity']:.3f} (piedra)")
    print(f"   Área estimada: {data['estimated_area_m2']:.0f} m²")
    print(f"   Altura estimada: {data['estimated_height_m']:.1f} m")
    print()
    
    # Calcular ratio
    estimated_length = (data['estimated_area_m2'] / 0.26) ** 0.5  # Asumiendo ratio L/W ~3.8
    estimated_width = data['estimated_area_m2'] / estimated_length
    ratio_lh = estimated_length / data['estimated_height_m']
    
    print(f"📐 GEOMETRÍA INFERIDA:")
    print(f"   Longitud estimada: ~{estimated_length:.0f}m")
    print(f"   Ancho estimado: ~{estimated_width:.0f}m")
    print(f"   Ratio L/H: {ratio_lh:.2f} (muy horizontal)")
    print()
    
    # Ejecutar inferencia
    mig = CulturallyConstrainedMIG()
    
    result = mig.infer_culturally_constrained_geometry(
        archeoscope_data=data,
        output_name="sphinx_giza_constrained",
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
    print(f"📦 Volumen: {result['volume_m3']:,.0f} m³")
    print()
    print(f"📁 Archivos generados:")
    print(f"   PNG: {result['png']}")
    print(f"   OBJ: {result['obj']}")
    print()
    
    print("⚠️ DISCLAIMER:")
    print("   Esta NO es 'la' Esfinge de Giza.")
    print("   Es una forma COMPATIBLE con estatuaria tipo esfinge.")
    print("   Sin rasgos faciales, sin ornamentos, sin detalles.")
    print()


def test_sphinx_smaller():
    """Test: Esfinge más pequeña (tipo avenida de esfinges)."""
    
    print("="*80)
    print("🦁 TEST 2: ESFINGE PEQUEÑA (Avenida de Esfinges)")
    print("="*80)
    print()
    
    print("📍 REFERENCIA: Esfinges de la Avenida (Karnak-Luxor)")
    print("   Longitud típica: ~3-5m")
    print("   Altura: ~1.5-2m")
    print()
    
    data = {
        'scale_invariance': 0.92,
        'angular_consistency': 0.90,
        'coherence_3d': 0.87,
        'sar_rigidity': 0.89,
        'stratification_index': 0.10,
        'estimated_area_m2': 15.0,  # ~5m × 3m
        'estimated_height_m': 2.0
    }
    
    print("🛰️ INVARIANTES DETECTADOS:")
    print(f"   Scale Invariance: {data['scale_invariance']:.3f}")
    print(f"   Angular Consistency: {data['angular_consistency']:.3f}")
    print(f"   Área: {data['estimated_area_m2']:.1f} m²")
    print(f"   Altura: {data['estimated_height_m']:.1f} m")
    print()
    
    mig = CulturallyConstrainedMIG()
    
    result = mig.infer_culturally_constrained_geometry(
        archeoscope_data=data,
        output_name="sphinx_small_constrained",
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


def test_sphinx_vs_moai():
    """Comparación: ¿Cómo distingue el sistema entre esfinge y moai?"""
    
    print("="*80)
    print("🔬 ANÁLISIS: ¿Cómo distingue ESFINGE de MOAI?")
    print("="*80)
    print()
    
    print("🗿 MOAI (Rapa Nui):")
    print("   - Ratio H/W: ~3.2 (VERTICAL)")
    print("   - Dominancia vertical: 0.95")
    print("   - Dominancia horizontal: 0.05")
    print("   - Forma: Bloque vertical")
    print()
    
    print("🦁 ESFINGE (Egipto):")
    print("   - Ratio L/H: ~3.65 (HORIZONTAL)")
    print("   - Dominancia vertical: 0.15")
    print("   - Dominancia horizontal: 0.95")
    print("   - Forma: Cuerpo horizontal + cabeza vertical")
    print()
    
    print("🔑 DISCRIMINANTE CLAVE:")
    print("   El sistema NO 'reconoce' moais o esfinges")
    print("   El sistema MIDE proporciones geométricas")
    print("   y las COMPARA con repositorio morfológico")
    print()
    
    print("📊 SCORING:")
    print("   1. Calcular ratio H/W desde datos territoriales")
    print("   2. Comparar con ratios culturales conocidos")
    print("   3. Score = exp(-|ratio_data - ratio_cultural| / 2)")
    print("   4. Mejor match = clase morfológica inferida")
    print()
    
    print("✅ RESULTADO:")
    print("   Estructura vertical → MOAI")
    print("   Estructura horizontal → ESFINGE")
    print("   Sin 'decidir', solo restringiendo espacio geométrico")
    print()


if __name__ == "__main__":
    print()
    print("🦁 MIG NIVEL 3 - TEST ESFINGE CULTURALMENTE CONSTREÑIDA")
    print()
    
    try:
        # Test 1: Esfinge escala Giza
        test_sphinx_giza_scale()
        
        print("\n" + "="*80 + "\n")
        
        # Test 2: Esfinge pequeña
        test_sphinx_smaller()
        
        print("\n" + "="*80 + "\n")
        
        # Análisis comparativo
        test_sphinx_vs_moai()
        
        print("="*80)
        print("✅ TESTS COMPLETADOS")
        print("="*80)
        print()
        print("🎉 ESFINGE: Posible, con más cuidado")
        print()
        print("📁 Revisa 'geometric_models/' para ver:")
        print("   - sphinx_giza_constrained.png")
        print("   - sphinx_giza_constrained.obj")
        print("   - sphinx_small_constrained.png")
        print("   - sphinx_small_constrained.obj")
        print()
        print("🧬 'No la esfinge, sino una compatible'")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
