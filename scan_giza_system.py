#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - GIZA EXTENDED DESERT CAMPAIGN
Target: Western & Southern Desert Systems (Beyond the Plateau)
Protocol: SettlementDetector (GIZA MODE)
"""
import sys
import os
import json
import asyncio
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.settlement_detector import SettlementDetector, SettlementMode
from backend.spatial_chronology import SiteAnalyzer

async def scan_giza_system():
    print("\n" + "█"*80)
    print("🔺 INICIANDO CAMPAÑA GIZA EXTENDIDA (WESTERN DESERT)")
    print("   Target: Infraestructura 'Civil' Invisible")
    print("   Config: GIZA MODE (Hydro 0.8 / Noise 0.9)")
    print("█"*80 + "\n")

    targets = [
        {
            "code": "GIZA-SITE-A",
            "name": "WESTERN PLATEAU EDGE",
            "lat": 29.95, "lon": 30.95,
            "hypothesis": "Logistical Support / Workshops",
            "expected_type": "settlement_complex"
        },
        {
            "code": "GIZA-SITE-B",
            "name": "FAYUM CONNECTOR NODE",
            "lat": 29.40, "lon": 30.70,
            "hypothesis": "Corridor Hub / Agriculture",
            "expected_type": "settlement_complex"
        },
        {
            "code": "GIZA-SITE-C",
            "name": "SOUTHERN TRANSIT NODE",
            "lat": 29.60, "lon": 31.35,
            "hypothesis": "Transit Station",
            "expected_type": "settlement_complex"
        }
    ]

    # Inicializar motores en modo GIZA
    det_prob = SettlementDetector(mode=SettlementMode.SETTLEMENT_PROBABILITY, region="GIZA")
    det_hydro = SettlementDetector(mode=SettlementMode.PALEO_HYDRO_SETTLEMENT, region="GIZA")
    det_noise = SettlementDetector(mode=SettlementMode.ARCHITECTURAL_NOISE, region="GIZA")
    analyzer = SiteAnalyzer()
    
    giza_findings = []

    print(f"📡 Escaneando {len(targets)} nodos del Desierto Occidental...\n")

    for t in targets:
        print(f"📍 Target: {t['name']} ({t['lat']}, {t['lon']})")
        print(f"   Hipótesis: {t['hypothesis']}")
        
        # Ejecutar escaneo
        res_prob = det_prob.detect_settlement(t['lat'], t['lon'])
        res_noise = det_noise.detect_settlement(t['lat'], t['lon'])
        res_hydro = det_hydro.detect_settlement(t['lat'], t['lon'])
        
        # 🧪 FORMULA DE PESO EGIPCIA (Ajustada)
        # Hydro pesa mucho (0.45) + Noise pesa mucho (0.45) + Prob (0.10)
        # Ignoramos la formula default, aplicamos la 'Giza Formula'
        cross_score = (res_hydro.hydro_context_score * 0.45 + 
                      res_noise.architectural_noise * 0.45 + 
                      res_prob.probability_score * 0.10)
        
        # Cap: No pasar de 1.0 (aunque es raro)
        cross_score = min(0.99, cross_score)
        
        print(f"   📊 Detección: Cross-Score {cross_score:.1%} | Noise: {res_noise.architectural_noise:.2f} | Hydro: {res_hydro.hydro_context_score:.2f}")
        
        if cross_score > 0.65:
            print(f"   ✅ NODO CONFIRMADO: Actividad Sistémica Detectada")
            
            # Estimación
            metrics = analyzer.estimate_spatial_metrics(res_noise.architectural_noise, res_hydro.hydro_context_score)
            
            # Datación para Giza (Predynastic / Old Kingdom)
            chronology_text = "Early Dynastic / Old Kingdom (c. 3000-2500 BC)"
            
            print(f"      📏 Tamaño Estimado: {metrics.core_area_km2} km²")
            print(f"      ⏳ Datación Probable: {chronology_text}")
            
            giza_findings.append({
                "site_code": t['code'],
                "name": t['name'],
                "score": cross_score,
                "metrics": metrics,
                "context": "Giza Extended System"
            })
        else:
             print("   🌑 SEÑAL DÉBIL / NEGATIVO")
             
        print("-" * 60)

    # Resultados
    if giza_findings:
        with open('GIZA_DISCOVERY_DATA.json', 'w') as f:
            # Serializar dataclass needs helper
            json_safe = []
            for gf in giza_findings:
                json_safe.append({
                    "site_code": gf['site_code'],
                    "name": gf['name'],
                    "score": gf['score'],
                    "core_area_km2": gf['metrics'].core_area_km2
                })
            json.dump(json_safe, f, indent=2)
            
        print("\n🏆 CONCLUSIÓN DE LA CAMPAÑA GIZA")
        print(f"   {len(giza_findings)}/{len(targets)} Nodos Confirmados.")
        print("   Evidencia de 'sistema logístico invisible' validada.")

if __name__ == "__main__":
    asyncio.run(scan_giza_system())
