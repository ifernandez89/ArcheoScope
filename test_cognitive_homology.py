#!/usr/bin/env python3
"""
Test del Cognitive Homology Index (CHI)
Evalúa la hipótesis de correlación Orión-Giza
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from cognitive_homology import (
    CognitiveHomologyAnalyzer,
    CelestialNode,
    ArchitecturalNode,
    NodeType,
    get_orion_belt,
    get_giza_pyramids
)


def test_giza_orion():
    """Test principal: Giza vs Cinturón de Orión."""
    
    print("\n" + "="*80)
    print("🔬 COGNITIVE HOMOLOGY INDEX (CHI) - TEST CIENTÍFICO")
    print("="*80)
    print("\n📍 Hipótesis: Las pirámides de Giza reproducen la estructura relacional")
    print("   del Cinturón de Orión (NO geométrica, sino cognitiva).\n")
    
    # Cargar datos
    orion = get_orion_belt()
    giza = get_giza_pyramids()
    
    print("🌌 PATRÓN CELESTE: Cinturón de Orión")
    print("-" * 40)
    for star in orion:
        print(f"  • {star.name:10} | Mag: {star.magnitude:.2f} | Tipo: {star.node_type.value}")
    
    print("\n🏛️ PATRÓN ARQUITECTÓNICO: Pirámides de Giza")
    print("-" * 40)
    for pyramid in giza:
        print(f"  • {pyramid.name:10} | Vol: {pyramid.volume_m3/1e6:.2f}M m³ | Altura: {pyramid.height_m:.1f}m")
    
    # Ejecutar análisis
    analyzer = CognitiveHomologyAnalyzer()
    result = analyzer.analyze(orion, giza, site_name="Giza")
    
    # Reporte de resultados
    print("\n" + "="*80)
    print("📊 RESULTADOS DEL ANÁLISIS")
    print("="*80)
    print(f"\n🎯 CHI Score (Cognitive Homology Index): {result.chi_score:.3f}")
    print(f"   {'✅ SIGNIFICATIVO' if result.is_significant else '❌ NO SIGNIFICATIVO'}")
    
    print(f"\n📈 Métricas Detalladas:")
    print(f"   • Isomorfismo de Grafos:      {result.graph_isomorphism:.3f}")
    print(f"   • Correlación de Entropía:    {result.entropy_correlation:.3f}")
    print(f"   • Correlación de Rankings:    {result.rank_correlation:.3f}")
    print(f"   • Orden Estructural:          {result.structural_order:.3f}")
    
    print(f"\n💬 Interpretación Científica:")
    print(f"   {result.interpretation}")
    
    print("\n" + "="*80)
    print("🧠 CONCLUSIÓN")
    print("="*80)
    
    if result.chi_score >= 0.65:
        print("""
✅ Los datos RESPALDAN la hipótesis de homología cognitiva.

Esto NO significa que "copiaron el cielo punto por punto".
Significa que existe evidencia cuantificable de que:

1. La jerarquía arquitectónica replica la jerarquía estelar
2. Las relaciones topológicas son similares
3. El nivel de orden no es aleatorio

Interpretación válida:
"El Cinturón de Orión pudo haber servido como MARCO COGNITIVO
para organizar el complejo de Giza, reproduciendo relaciones
jerárquicas más que posiciones astronómicas exactas."
        """)
    else:
        print("""
❌ Los datos NO respaldan la hipótesis de homología cognitiva.

El patrón arquitectónico no muestra similitud estructural significativa
con el patrón celeste. Posibles explicaciones:

1. Organización independiente basada en otros factores
2. Coincidencia fortuita
3. Modelo celeste diferente (no Orión)
        """)
    
    print("="*80 + "\n")
    
    return result


def test_xian_orion():
    """Test adicional: Xi'an vs Orión (control negativo esperado)."""
    
    print("\n" + "="*80)
    print("🔬 TEST DE CONTROL: Xi'an vs Orión")
    print("="*80)
    
    orion = get_orion_belt()
    
    # Pirámides de Xi'an (datos aproximados)
    xian = [
        ArchitecturalNode("Gran Pirámide Blanca", 34.3828, 109.2753, 1000000, 76, NodeType.PRIMARY, 0.9),
        ArchitecturalNode("Pirámide Norte", 34.3850, 109.2760, 500000, 55, NodeType.SECONDARY, 0.7),
        ArchitecturalNode("Pirámide Sur", 34.3800, 109.2740, 450000, 50, NodeType.SECONDARY, 0.65)
    ]
    
    analyzer = CognitiveHomologyAnalyzer()
    result = analyzer.analyze(orion, xian, site_name="Xi'an")
    
    print(f"\n🎯 CHI Score: {result.chi_score:.3f}")
    print(f"   {'✅ SIGNIFICATIVO' if result.is_significant else '❌ NO SIGNIFICATIVO'}")
    print(f"\n💬 {result.interpretation}")
    print("\n" + "="*80 + "\n")
    
    return result


if __name__ == "__main__":
    # Test principal
    giza_result = test_giza_orion()
    
    # Test de control
    xian_result = test_xian_orion()
    
    # Comparación
    print("\n" + "="*80)
    print("📊 COMPARACIÓN FINAL")
    print("="*80)
    print(f"\nGiza vs Orión:  CHI = {giza_result.chi_score:.3f} {'✅' if giza_result.is_significant else '❌'}")
    print(f"Xi'an vs Orión: CHI = {xian_result.chi_score:.3f} {'✅' if xian_result.is_significant else '❌'}")
    
    if giza_result.chi_score > xian_result.chi_score:
        print("\n✅ Giza muestra mayor homología con Orión que Xi'an.")
        print("   Esto respalda la especificidad de la hipótesis Giza-Orión.")
    else:
        print("\n⚠️ Xi'an muestra homología similar o mayor que Giza.")
        print("   Esto sugiere que el patrón podría ser más general.")
    
    print("\n" + "="*80 + "\n")
