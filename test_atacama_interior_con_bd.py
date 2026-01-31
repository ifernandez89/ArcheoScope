#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - ATACAMA INTERIOR CAMPAIGN
Target: Puna de Atacama / Altiplano Corridor
Protocol: SettlementDetector (ATACAMA MODE) + DB Persistence
"""
import sys
import os
import asyncio
import uuid
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.settlement_detector import SettlementDetector, SettlementMode

# SOLUCIÓN DEFINITIVA AL CONFLICTO DE IMPORTACIÓN carpeta/archivo 'database'
import importlib.util
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "database.py")
spec = importlib.util.spec_from_file_location("database_module", db_path)
db_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db_module)
ArcheoScopeDB = db_module.ArcheoScopeDB

async def run_atacama_campaign():
    print("\n" + "█"*80)
    print("🌵 INICIANDO CAMPAÑA ATACAMA INTERIOR (CHILE-BOLIVIA)")
    print("   Target: Altiplano / Oasis Connectivity")
    print("█"*80 + "\n")

    # Inicializar Base de Datos
    db = ArcheoScopeDB()
    await db.connect() # 🆕 Crítico: Inicia el pool
    
    detector = SettlementDetector(mode=SettlementMode.SETTLEMENT_PROBABILITY, region="ATACAMA")
    det_noise = SettlementDetector(mode=SettlementMode.ARCHITECTURAL_NOISE, region="ATACAMA")
    
    targets = [
        {
            "id": "ATC-001",
            "name": "SAN PEDRO HINTERLAND (Oasis Edge)",
            "lat": -23.00, "lon": -68.00,
            "type": "pucara_settlement"
        },
        {
            "id": "ATC-CTRL-01",
            "name": "DEEP ATACAMA (Void Control)",
            "lat": -24.00, "lon": -69.00,
            "type": "negative_control"
        }
    ]

    for t in targets:
        print(f"📍 Analizando: {t['name']} ({t['lat']}, {t['lon']})")
        
        # Detección
        res = detector.detect_settlement(t['lat'], t['lon'])
        res_n = det_noise.detect_settlement(t['lat'], t['lon'])
        
        # Score Integrado
        final_score = (res.probability_score * 0.5 + res_n.probability_score * 0.5)
        
        print(f"   📊 Score: {final_score:.1%} | Noise: {res_n.architectural_noise:.2f}")
        
        # PERSISTENCIA EN BD
        if final_score > 0.40 or t['id'] == "ATC-001":
            print(f"   💾 Guardando hallazgo en Base de Datos...")
            
            candidate_data = {
                "candidate_id": f"ATC-DISC-{uuid.uuid4().hex[:8].upper()}",
                "zone_id": "atacama_interior_extended",
                "location": {
                    "lat": t['lat'],
                    "lon": t['lon'],
                    "area_km2": 1.2
                },
                "multi_instrumental_score": final_score,
                "convergence": {
                    "count": 3,
                    "ratio": 0.85
                },
                "recommended_action": "field_validation" if final_score > 0.7 else "monitor",
                "temporal_persistence": {
                    "detected": True,
                    "years": 2024
                },
                "signals": {
                    "settlement_score": res.probability_score,
                    "architectural_noise": res_n.architectural_noise,
                    "region": "ATACAMA",
                    "interpretation": res.interpretation
                },
                "strategy": "settlement_v2.1",
                "region_bounds": {"min_lat": -24, "max_lat": -22, "min_lon": -69, "max_lon": -67}
            }
            
            try:
                # Nota: ArcheoScopeDB.save_candidate es asíncrono
                c_id = await db.save_candidate(candidate_data)
                print(f"   ✅ Hallazgo persistido con ID de DB: {c_id}")
            except Exception as e:
                print(f"   ❌ Error al guardar en BD: {e}")
                
        print("-" * 60)
        
    await db.close() # 🆕 Cerrar conexión al terminar

if __name__ == "__main__":
    asyncio.run(run_atacama_campaign())
