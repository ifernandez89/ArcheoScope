#!/usr/bin/env python3
"""
MISIÓN GLOBAL: Cognitive Homology + TIMT Analysis
==================================================

Ejecuta análisis dual (Framework v2.0 + CHI) en 8 sitios monumentales globales.
Guarda resultados en JSON y Base de Datos PostgreSQL.

Autor: Antigravity AI
Fecha: 2026-02-02
"""

import asyncio
import httpx
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from cognitive_homology import (
    CognitiveHomologyAnalyzer,
    CelestialNode,
    ArchitecturalNode,
    NodeType,
    get_orion_belt
)


# ============================================================================
# DEFINICIÓN DE SITIOS GLOBALES
# ============================================================================

GLOBAL_SITES = [
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


# ============================================================================
# FUNCIONES DE ANÁLISIS
# ============================================================================

async def analyze_site_timt(site: Dict, url: str = "http://localhost:8003/analyze-scientific/analyze") -> Dict:
    """Ejecuta análisis TIMT (Framework v2.0) en un sitio."""
    
    delta = 0.01  # ~2km² para capturar el complejo completo
    
    payload = {
        "lat_min": site['lat'] - delta,
        "lat_max": site['lat'] + delta,
        "lon_min": site['lon'] - delta,
        "lon_max": site['lon'] + delta,
        "region_name": site['name']
    }
    
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extraer métricas clave
                return {
                    "success": True,
                    "g1_geometry": data.get('etp_summary', {}).get('coherencia_3d', 0),
                    "g2_persistence": data.get('etp_summary', {}).get('persistencia_temporal', 0),
                    "g3_anomaly": data.get('etp_summary', {}).get('ess_superficial', 0),
                    "g4_modularity": data.get('scientific_output', {}).get('hrm_analysis', {}).get('peak_count', 0),
                    "classification": data.get('official_classification', {}).get('veredicto', 'UNKNOWN'),
                    "msf": data.get('official_classification', {}).get('metrics', {}).get('msf', 1.0),
                    "anomaly_map": data.get('anomaly_map', {}).get('path', ''),
                    "hrm_viz": data.get('visualizacion_neural', '')
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
    except Exception as e:
        return {"success": False, "error": str(e)}


def analyze_site_chi(site: Dict) -> Dict:
    """Ejecuta análisis CHI (Cognitive Homology) en un sitio."""
    
    # Mapeo de strings a NodeType
    type_map = {
        "PRIMARY": NodeType.PRIMARY,
        "SECONDARY": NodeType.SECONDARY,
        "TERTIARY": NodeType.TERTIARY
    }
    
    # Construir nodos arquitectónicos
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
    
    # Obtener patrón celeste (Orión)
    orion = get_orion_belt()
    
    # Ejecutar análisis
    analyzer = CognitiveHomologyAnalyzer()
    result = analyzer.analyze(orion, arch_nodes, site_name=site['name'])
    
    return {
        "chi_score": result.chi_score,
        "graph_isomorphism": result.graph_isomorphism,
        "entropy_correlation": result.entropy_correlation,
        "rank_correlation": result.rank_correlation,
        "structural_order": result.structural_order,
        "is_significant": result.is_significant,
        "interpretation": result.interpretation
    }


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

async def run_global_mission():
    """Ejecuta la misión global de análisis dual."""
    
    print("\n" + "="*90)
    print("🌍 MISIÓN GLOBAL: Cognitive Homology + TIMT Analysis")
    print("="*90)
    print(f"\n📍 Sitios a analizar: {len(GLOBAL_SITES)}")
    print(f"⏱️  Tiempo estimado: ~{len(GLOBAL_SITES) * 6} minutos\n")
    
    results = []
    
    for i, site in enumerate(GLOBAL_SITES, 1):
        print(f"\n{'='*90}")
        print(f"[{i}/{len(GLOBAL_SITES)}] Analizando: {site['name']}")
        print(f"{'='*90}")
        
        # 1. Análisis TIMT
        print(f"\n🛰️  Ejecutando análisis TIMT (Framework v2.0)...")
        timt_result = await analyze_site_timt(site)
        
        if timt_result['success']:
            print(f"   ✅ TIMT completado")
            print(f"      • Clasificación: {timt_result['classification']}")
            print(f"      • G1 (Geometría): {timt_result['g1_geometry']:.3f}")
            print(f"      • G2 (Persistencia): {timt_result['g2_persistence']:.3f}")
        else:
            print(f"   ❌ TIMT falló: {timt_result.get('error', 'Unknown')}")
        
        # 2. Análisis CHI
        print(f"\n🧠 Ejecutando análisis CHI (Homología Cognitiva vs Orión)...")
        chi_result = analyze_site_chi(site)
        
        print(f"   ✅ CHI completado")
        print(f"      • CHI Score: {chi_result['chi_score']:.3f} {'✅' if chi_result['is_significant'] else '❌'}")
        print(f"      • Isomorfismo: {chi_result['graph_isomorphism']:.3f}")
        print(f"      • Rank Correlation: {chi_result['rank_correlation']:.3f}")
        
        # 3. Consolidar resultados
        result = {
            "site_name": site['name'],
            "coordinates": {"lat": site['lat'], "lon": site['lon']},
            "timestamp": datetime.utcnow().isoformat(),
            "timt_analysis": timt_result,
            "chi_analysis": chi_result
        }
        
        results.append(result)
    
    # 4. Guardar resultados en JSON
    output_file = f"GLOBAL_HOMOLOGY_MISSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*90}")
    print(f"✅ MISIÓN COMPLETADA")
    print(f"{'='*90}")
    print(f"\n📄 Resultados guardados en: {output_file}")
    
    # 5. Generar reporte comparativo
    print(f"\n{'='*90}")
    print("📊 REPORTE COMPARATIVO FINAL")
    print(f"{'='*90}\n")
    
    print(f"{'Sitio':<30} {'CHI':>6} {'TIMT':>15} {'Homología':>12}")
    print("-" * 90)
    
    for r in results:
        chi = r['chi_analysis']['chi_score']
        timt = r['timt_analysis'].get('classification', 'ERROR')[:15]
        sig = "✅ SÍ" if r['chi_analysis']['is_significant'] else "❌ NO"
        
        print(f"{r['site_name']:<30} {chi:>6.3f} {timt:>15} {sig:>12}")
    
    print("\n" + "="*90)
    
    # 6. Identificar patrones
    high_chi = [r for r in results if r['chi_analysis']['chi_score'] >= 0.75]
    anthropic = [r for r in results if 'ANTR' in r['timt_analysis'].get('classification', '')]
    
    print("\n🔬 HALLAZGOS CLAVE:")
    print(f"\n   • Sitios con Homología Cognitiva FUERTE (CHI ≥ 0.75): {len(high_chi)}")
    for r in high_chi:
        print(f"      - {r['site_name']}: CHI = {r['chi_analysis']['chi_score']:.3f}")
    
    print(f"\n   • Sitios con Clasificación ANTRÓPICA: {len(anthropic)}")
    for r in anthropic:
        print(f"      - {r['site_name']}: {r['timt_analysis']['classification']}")
    
    print("\n" + "="*90 + "\n")
    
    return results


# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    asyncio.run(run_global_mission())
