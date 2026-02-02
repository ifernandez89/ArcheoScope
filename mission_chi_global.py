#!/usr/bin/env python3
"""
MISIÓN GLOBAL CHI: Cognitive Homology Analysis
===============================================

Ejecuta análisis de Homología Cognitiva en 8 sitios monumentales globales.
Guarda resultados en JSON estructurado.

Autor: Antigravity AI
Fecha: 2026-02-02
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from cognitive_homology import (
    CognitiveHomologyAnalyzer,
    CelestialNode,
    ArchitecturalNode,
    NodeType,
    get_orion_belt,
    get_giza_pyramids
)


# ============================================================================
# SITIOS GLOBALES
# ============================================================================

GLOBAL_SITES = [
    {
        "name": "Giza (Egipto)",
        "lat": 29.9792,
        "lon": 31.1342,
        "pyramids": [
            {"name": "Khufu", "volume": 2583283, "height": 146.5, "type": "PRIMARY", "importance": 1.0},
            {"name": "Khafre", "volume": 2211096, "height": 143.5, "type": "PRIMARY", "importance": 0.95},
            {"name": "Menkaure", "volume": 235183, "height": 65.5, "type": "SECONDARY", "importance": 0.75}
        ]
    },
    {
        "name": "Xi'an (China)",
        "lat": 34.3828,
        "lon": 109.2753,
        "pyramids": [
            {"name": "Gran Pirámide Blanca", "volume": 1000000, "height": 76, "type": "PRIMARY", "importance": 0.9},
            {"name": "Pirámide Norte", "volume": 500000, "height": 55, "type": "SECONDARY", "importance": 0.7},
            {"name": "Pirámide Sur", "volume": 450000, "height": 50, "type": "SECONDARY", "importance": 0.65}
        ]
    },
    {
        "name": "Teotihuacán (México)",
        "lat": 19.6925,
        "lon": -98.8437,
        "pyramids": [
            {"name": "Pirámide del Sol", "volume": 1200000, "height": 65, "type": "PRIMARY", "importance": 1.0},
            {"name": "Pirámide de la Luna", "volume": 500000, "height": 43, "type": "PRIMARY", "importance": 0.95},
            {"name": "Templo Quetzalcóatl", "volume": 200000, "height": 17, "type": "SECONDARY", "importance": 0.85}
        ]
    },
    {
        "name": "Cholula (México)",
        "lat": 19.0590,
        "lon": -98.3017,
        "pyramids": [
            {"name": "Gran Pirámide", "volume": 4500000, "height": 66, "type": "PRIMARY", "importance": 1.0},
            {"name": "Estructura Norte", "volume": 300000, "height": 25, "type": "SECONDARY", "importance": 0.6},
            {"name": "Estructura Sur", "volume": 250000, "height": 22, "type": "SECONDARY", "importance": 0.55}
        ]
    },
    {
        "name": "Angkor Wat (Camboya)",
        "lat": 13.4125,
        "lon": 103.8670,
        "pyramids": [
            {"name": "Torre Central", "volume": 800000, "height": 65, "type": "PRIMARY", "importance": 1.0},
            {"name": "Torre Noroeste", "volume": 400000, "height": 58, "type": "PRIMARY", "importance": 0.9},
            {"name": "Torre Suroeste", "volume": 400000, "height": 58, "type": "PRIMARY", "importance": 0.9}
        ]
    },
    {
        "name": "Caral (Perú)",
        "lat": -10.8933,
        "lon": -77.5200,
        "pyramids": [
            {"name": "Pirámide Mayor", "volume": 150000, "height": 18, "type": "PRIMARY", "importance": 1.0},
            {"name": "Pirámide Galería", "volume": 80000, "height": 12, "type": "SECONDARY", "importance": 0.8},
            {"name": "Pirámide Huanca", "volume": 60000, "height": 10, "type": "SECONDARY", "importance": 0.7}
        ]
    },
    {
        "name": "Tikal (Guatemala)",
        "lat": 17.2221,
        "lon": -89.6236,
        "pyramids": [
            {"name": "Templo IV", "volume": 180000, "height": 65, "type": "PRIMARY", "importance": 1.0},
            {"name": "Templo I", "volume": 120000, "height": 47, "type": "PRIMARY", "importance": 0.95},
            {"name": "Templo II", "volume": 100000, "height": 38, "type": "SECONDARY", "importance": 0.85}
        ]
    },
    {
        "name": "Borobudur (Indonesia)",
        "lat": -7.6079,
        "lon": 110.2038,
        "pyramids": [
            {"name": "Nivel Superior", "volume": 600000, "height": 35, "type": "PRIMARY", "importance": 1.0},
            {"name": "Nivel Medio", "volume": 400000, "height": 25, "type": "SECONDARY", "importance": 0.7},
            {"name": "Nivel Inferior", "volume": 300000, "height": 15, "type": "TERTIARY", "importance": 0.5}
        ]
    },
    {
        "name": "Stonehenge (UK)",
        "lat": 51.1789,
        "lon": -1.8262,
        "pyramids": [
            {"name": "Círculo Sarsen", "volume": 5000, "height": 7, "type": "PRIMARY", "importance": 1.0},
            {"name": "Herradura Trilitos", "volume": 3000, "height": 6, "type": "SECONDARY", "importance": 0.8},
            {"name": "Círculo Azul", "volume": 2000, "height": 4, "type": "TERTIARY", "importance": 0.6}
        ]
    },
    {
        "name": "Machu Picchu (Perú)",
        "lat": -13.1631,
        "lon": -72.5450,
        "pyramids": [
            {"name": "Templo del Sol", "volume": 8000, "height": 12, "type": "PRIMARY", "importance": 1.0},
            {"name": "Intihuatana", "volume": 3000, "height": 8, "type": "SECONDARY", "importance": 0.9},
            {"name": "Templo Principal", "volume": 5000, "height": 10, "type": "SECONDARY", "importance": 0.85}
        ]
    }
]


def analyze_site_chi(site: Dict) -> Dict:
    """Ejecuta análisis CHI (Cognitive Homology) en un sitio."""
    
    type_map = {
        "PRIMARY": NodeType.PRIMARY,
        "SECONDARY": NodeType.SECONDARY,
        "TERTIARY": NodeType.TERTIARY
    }
    
    arch_nodes = []
    for pyr in site['pyramids']:
        arch_nodes.append(
            ArchitecturalNode(
                name=pyr['name'],
                lat=site['lat'],
                lon=site['lon'],
                volume_m3=pyr['volume'],
                height_m=pyr['height'],
                node_type=type_map[pyr['type']],
                ritual_importance=pyr['importance']
            )
        )
    
    orion = get_orion_belt()
    analyzer = CognitiveHomologyAnalyzer()
    result = analyzer.analyze(orion, arch_nodes, site_name=site['name'])
    
    # Convertir a dict serializable
    return {
        "chi_score": float(result.chi_score),
        "graph_isomorphism": float(result.graph_isomorphism),
        "entropy_correlation": float(result.entropy_correlation),
        "rank_correlation": float(result.rank_correlation),
        "structural_order": float(result.structural_order),
        "is_significant": bool(result.is_significant),  # Convertir explícitamente
        "interpretation": str(result.interpretation)
    }


def run_global_mission():
    """Ejecuta la misión global de análisis CHI."""
    
    print("\n" + "="*90)
    print("🌍 MISIÓN GLOBAL: Cognitive Homology Index (Orión)")
    print("="*90)
    print(f"\n📍 Sitios a analizar: {len(GLOBAL_SITES)}\n")
    
    results = []
    
    for i, site in enumerate(GLOBAL_SITES, 1):
        print(f"[{i}/{len(GLOBAL_SITES)}] {site['name']:<30}", end=" ")
        
        chi_result = analyze_site_chi(site)
        
        result = {
            "site_name": site['name'],
            "coordinates": {"lat": site['lat'], "lon": site['lon']},
            "timestamp": datetime.utcnow().isoformat(),
            "chi_analysis": chi_result
        }
        
        results.append(result)
        
        sig = "✅" if chi_result['is_significant'] else "❌"
        print(f"CHI: {chi_result['chi_score']:.3f} {sig}")
    
    # Guardar en JSON
    output_file = f"GLOBAL_CHI_MISSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*90}")
    print(f"✅ MISIÓN COMPLETADA - Resultados: {output_file}")
    print(f"{'='*90}\n")
    
    # Reporte comparativo
    print(f"{'Sitio':<30} {'CHI':>6} {'Isomorf':>8} {'Rank':>6} {'Homología':>12}")
    print("-" * 90)
    
    for r in results:
        chi = r['chi_analysis']
        sig = "✅ SÍ" if chi['is_significant'] else "❌ NO"
        print(f"{r['site_name']:<30} {chi['chi_score']:>6.3f} {chi['graph_isomorphism']:>8.3f} {chi['rank_correlation']:>6.3f} {sig:>12}")
    
    # Hallazgos clave
    high_chi = [r for r in results if r['chi_analysis']['chi_score'] >= 0.75]
    
    print("\n" + "="*90)
    print("🔬 HALLAZGOS CLAVE:")
    print("="*90)
    print(f"\n✅ Sitios con Homología Cognitiva FUERTE (CHI ≥ 0.75): {len(high_chi)}/{len(results)}")
    
    for r in sorted(high_chi, key=lambda x: x['chi_analysis']['chi_score'], reverse=True):
        chi = r['chi_analysis']['chi_score']
        rank = r['chi_analysis']['rank_correlation']
        print(f"   • {r['site_name']:<30} CHI={chi:.3f} | Rank={rank:.3f}")
    
    print("\n" + "="*90 + "\n")
    
    return results


if __name__ == "__main__":
    run_global_mission()
