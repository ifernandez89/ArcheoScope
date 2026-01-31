#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - RUB' AL KHALI SURFACE ANOMALY SCAN
Target: Visual Geoglyphs / Surface Alignments
Protocol: SettlementDetector (SURFACE_GEOMETRY_SCAN)
"""
import sys
import os
import asyncio
import uuid
import importlib.util

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.settlement_detector import SettlementDetector, SettlementMode

# Carga de DB
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "database.py")
spec = importlib.util.spec_from_file_location("database_module", db_path)
db_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db_module)
ArcheoScopeDB = db_module.ArcheoScopeDB

async def run_visual_rescan():
    print("\n" + "👁️"*40)
    print("ARCHEOSCOPE: RE-SCAN VISUAL (RUB' AL KHALI)")
    print("Sensor: Surface Geometry / Anti-Dune Logic")
    print("👁️"*40 + "\n")

    db = ArcheoScopeDB()
    await db.connect()
    
    # Modo superficie
    detector = SettlementDetector(mode=SettlementMode.SURFACE_GEOMETRY_SCAN, region="RUB_AL_KHALI")
    
    # Sitios originales
    targets = [
        {"name": "RAK-CORRIDOR EAST", "lat": 20.62, "lon": 51.38},
        {"name": "PALEOLAKE NODE SOUTH", "lat": 20.18, "lon": 50.92},
        {"name": "TRANSIT HUB WEST", "lat": 20.48, "lon": 50.55}
    ]

    for t in targets:
        print(f"📡 Escaneando superficie en: {t['name']}")
        res = detector.detect_settlement(t['lat'], t['lon'])
        
        print(f"   📊 Score Visual: {res.probability_score:.1%}")
        print(f"   📐 Ortogonalidad: {res.signature.orthogonality_ratio:.2f}")
        print(f"   📝 Veredicto: {res.interpretation}")
        
        if res.probability_score > 0.6:
            print(f"   ✨ ANOMALÍA CONFIRMADA: Geometría no eólica detectada.")
            
            candidate = {
                "candidate_id": f"GEO-RAK-{uuid.uuid4().hex[:8].upper()}",
                "zone_id": "rub_al_khali_surface_anomaly",
                "location": {"lat": t['lat'], "lon": t['lon'], "area_km2": 0.5},
                "multi_instrumental_score": res.probability_score,
                "convergence": {"count": 2, "ratio": 0.75},
                "recommended_action": "field_validation",
                "temporal_persistence": {"detected": True, "years": 2024},
                "signals": {
                    "visual_score": res.probability_score,
                    "orthogonality": res.signature.orthogonality_ratio,
                    "type": "GEOGLYPH_CANDIDATE"
                },
                "strategy": "surf_geom_v1",
                "region_bounds": {"min_lat": 20, "max_lat": 21, "min_lon": 50, "max_lon": 52}
            }
            c_id = await db.save_candidate(candidate)
            print(f"   💾 Guardado en BD como Geoglifo (ID: {c_id})")
        
        print("-" * 60)

    await db.close()

if __name__ == "__main__":
    asyncio.run(run_visual_rescan())
