#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - SETTLEMENT SEARCH OPERATION
Target: Rub' al Khali Cluster Zone (20.5 N, 51.0 E)
Objective: Find 'Proto-Urban' functional nodes using SettlementDetector
"""
import sys
import os
import json
from datetime import datetime
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.settlement_detector import SettlementDetector, SettlementMode

def run_settlement_search():
    print("\n" + "█"*80)
    print("🏙️  INICIANDO BÚSQUEDA DE ASENTAMIENTOS: PROTOCOLOS NUEVOS")
    print("    Zona: Rub' al Khali Cluster Margins")
    print("    Modos: SETTLEMENT + HYDRO + NOISE")
    print("█"*80 + "\n")

    # Configuración de búsqueda fina
    base_lat = 20.50
    base_lon = 51.00
    search_radius = 0.08 # ~8km, barre la zona del cluster geoglifo y alrededores
    step = 0.02 # Malla muy fina para detectar núcleos pequeños

    # Inicializar detectores
    det_prob = SettlementDetector(mode=SettlementMode.SETTLEMENT_PROBABILITY)
    det_hydro = SettlementDetector(mode=SettlementMode.PALEO_HYDRO_SETTLEMENT)
    det_noise = SettlementDetector(mode=SettlementMode.ARCHITECTURAL_NOISE)

    points = []
    # Generar puntos (Grid 9x9 mas denso)
    for lat in np.arange(base_lat - search_radius, base_lat + search_radius, step):
        for lon in np.arange(base_lon - search_radius, base_lon + search_radius, step):
            points.append((lat, lon))
            
    print(f"📡 Escaneando {len(points)} micro-sectores de alta resolución...\n")
    
    candidates = []
    
    for lat, lon in points:
        # Ejecutar los 3 análisis
        res_prob = det_prob.detect_settlement(lat, lon)
        res_hydro = det_hydro.detect_settlement(lat, lon)
        res_noise = det_noise.detect_settlement(lat, lon)
        
        # 🧠 LÓGICA DE CRUCE (Fusión de sensores)
        # Buscamos coincidencia de FACTORES, no solo un score alto
        
        # Promedio ponderado cruzado
        cross_score = (res_prob.probability_score * 0.4 + 
                      res_hydro.probability_score * 0.4 + 
                      res_noise.probability_score * 0.2)
        
        # Detectar el "Hotspot"
        if cross_score > 0.75:
            marker = "  "
            if res_prob.is_proto_urban or cross_score > 0.85:
                marker = "🔥"
            
            print(f"{marker} Sector {lat:.3f},{lon:.3f} | Cross-Score: {cross_score:.1%} | Noise: {res_noise.architectural_noise:.2f} | Hydro: {res_hydro.hydro_context_score:.2f}")
            print(f"   └─ Interp: {res_prob.interpretation}")
            
            candidates.append({
                'lat': lat,
                'lon': lon,
                'cross_score': cross_score,
                'interpretation': res_prob.interpretation,
                'details': {
                    'prob_score': res_prob.probability_score,
                    'hydro_score': res_hydro.probability_score,
                    'noise_score': res_noise.probability_score,
                    'is_proto_urban': bool(res_prob.is_proto_urban)
                }
            })

    # Análisis de resultados
    print("\n" + "="*80)
    print("📊 RESULTADOS DE BÚSQUEDA DE ASENTAMIENTOS")
    print("="*80)
    
    # Filtrar el mejor candidato (Top 1)
    if candidates:
        top_candidate = max(candidates, key=lambda x: x['cross_score'])
        print(f"\n🏆 MEJOR CANDIDATO (NODO REGIONAL):")
        print(f"   Coords: {top_candidate['lat']:.3f}, {top_candidate['lon']:.3f}")
        print(f"   Score Cruzado: {top_candidate['cross_score']:.1%}")
        print(f"   Interpretación: {top_candidate['interpretation'].upper()}")
        
        print("\n🔎 ANÁLISIS DEL SITIO:")
        print("   Este punto representa la convergencia óptima de:")
        print("   1. Densidad de anomalías (viviendas/muros).")
        print("   2. Acceso hidrológico seguro (borde de cuenca).")
        print("   3. Ruido ortogonal (arquitectura humana).")
        
        # Guardar
        with open('RUB_AL_KHALI_SETTLEMENTS.json', 'w') as f:
            json.dump(candidates, f, indent=2)
        print("\n💾 Resultados guardados en: RUB_AL_KHALI_SETTLEMENTS.json")
        
    else:
        print("No se encontraron núcleos densos claros.")

if __name__ == "__main__":
    run_settlement_search()
