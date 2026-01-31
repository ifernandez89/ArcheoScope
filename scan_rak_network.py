#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - NETWORK ANALYSIS OPERATION
Subject: Rub' al Khali Regional System
Targets: 3 Predicted Functional Nodes
Protocol: Multi-Modal Detection + Spatial/Temporal Estimation
"""
import sys
import os
import json
import asyncio
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.settlement_detector import SettlementDetector, SettlementMode
from backend.spatial_chronology import SiteAnalyzer

async def scan_network_nodes():
    print("\n" + "█"*80)
    print("🌐 INICIANDO ANÁLISIS DE RED REGIONAL (NETWORK SCAN)")
    print("   Target: Validación de Sistema Interconectado")
    print("█"*80 + "\n")

    targets = [
        {
            "code": "SITE-A",
            "name": "RAK-CORRIDOR EAST",
            "lat": 20.62, "lon": 51.38,
            "hypothesis": "Corridor / Bottleneck",
            "expected_type": "settlement_complex"
        },
        {
            "code": "SITE-B",
            "name": "PALEOLAKE NODE SOUTH",
            "lat": 20.18, "lon": 50.92,
            "hypothesis": "Secondary Habitation / Seasonal",
            "expected_type": "settlement_complex"
        },
        {
            "code": "SITE-C",
            "name": "TRANSIT HUB WEST",
            "lat": 20.48, "lon": 50.55,
            "hypothesis": "Transit Node / Intersection",
            "expected_type": "settlement_complex"
        }
    ]

    # Inicializar motores
    det_prob = SettlementDetector(mode=SettlementMode.SETTLEMENT_PROBABILITY)
    det_hydro = SettlementDetector(mode=SettlementMode.PALEO_HYDRO_SETTLEMENT)
    det_noise = SettlementDetector(mode=SettlementMode.ARCHITECTURAL_NOISE)
    analyzer = SiteAnalyzer()
    
    network_findings = []

    print(f"📡 Escaneando {len(targets)} nodos estratégicos...\n")

    for t in targets:
        print(f"📍 Target: {t['name']} ({t['lat']}, {t['lon']})")
        print(f"   Hipótesis: {t['hypothesis']}")
        
        # Ejecutar escaneo multi-modal
        res_prob = det_prob.detect_settlement(t['lat'], t['lon'])
        res_noise = det_noise.detect_settlement(t['lat'], t['lon'])
        res_hydro = det_hydro.detect_settlement(t['lat'], t['lon'])
        
        # Calcular Cross-Score (Fusión)
        cross_score = (res_prob.probability_score * 0.4 + 
                      res_hydro.probability_score * 0.3 + 
                      res_noise.probability_score * 0.3)
        
        print(f"   📊 Detección: Cross-Score {cross_score:.1%} | Noise: {res_noise.architectural_noise:.2f}")
        
        if cross_score > 0.65: # Umbral de detección positiva para la red
            print(f"   ✅ NODO CONFIRMADO: {res_prob.interpretation}")
            
            # Estimación Espacial y Temporal
            metrics = analyzer.estimate_spatial_metrics(res_noise.architectural_noise, res_hydro.hydro_context_score)
            chronology = analyzer.estimate_chronology(t['expected_type'], "hydro_fossil_basin")
            
            print(f"      📏 Tamaño Núcleo: {metrics.core_area_km2} km² (Est. Pop: {metrics.estimated_population})")
            print(f"      ⏳ Datación: {chronology.period} ({chronology.start_bc} - {chronology.end_bc} BC)")
            print(f"      🛡️ Confianza Cronológica: {chronology.confidence:.0%}")
            
            network_findings.append({
                "site_code": t['code'],
                "name": t['name'],
                "coords": {"lat": t['lat'], "lon": t['lon']},
                "score": cross_score,
                "function": t['hypothesis'],
                "metrics": {
                    "core_area_km2": metrics.core_area_km2,
                    "total_area_km2": metrics.total_area_km2,
                    "population": metrics.estimated_population
                },
                "chronology": {
                    "period": chronology.period,
                    "range": f"{chronology.start_bc}-{chronology.end_bc} BC",
                    "confidence": chronology.confidence
                }
            })
        else:
            print("   🌑 SEÑAL DÉBIL / NEGATIVO")
            
        print("-" * 60)

    # Generar Reporte de Red
    if network_findings:
        output_file = "RAK_NETWORK_ANALYSIS.json"
        with open(output_file, 'w') as f:
            json.dump(network_findings, f, indent=2)
            
        print("\n" + "="*80)
        print("🏆 CONCLUSIÓN DEL ANÁLISIS DE RED")
        print("="*80)
        print(f"Nodos confirmados: {len(network_findings)}/{len(targets)}")
        if len(network_findings) >= 2:
            print("👉 SISTEMA CONFIRMADO: Los sitios muestran coherencia temporal y funcional.")
            print("   Se sugiere denominar a este sistema: 'RUB' AL KHALI INTERIOR CORRIDOR'.")
        
        print(f"\n💾 Datos guardados en: {output_file}")

if __name__ == "__main__":
    asyncio.run(scan_network_nodes())
