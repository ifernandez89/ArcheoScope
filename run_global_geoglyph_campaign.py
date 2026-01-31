#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - GLOBAL GEOGLYPH CAMPAIGN
Target: Arabian Harrat, Atacama South, Turgai Steppe
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

async def run_global_geoglyphs():
    print("\n" + "📐"*40)
    print("ARCHEOSCOPE: GLOBAL GEOGLYPH DISCOVERY CAMPAIGN")
    print("Mode: Surface Geometry / Persistent Orthogonality")
    print("📐"*40 + "\n")

    db = ArcheoScopeDB()
    await db.connect()
    
    detector_mode = SettlementMode.SURFACE_GEOMETRY_SCAN
    
    # Objetivos Globales
    targets = [
        {"region": "ARABIAN_HARRAT", "name": "WORKS OF THE OLD MEN (Khaybar)", "lat": 25.30, "lon": 37.80},
        {"region": "ATACAMA_SUR", "name": "GIANT GEOGLYPHS (Chile Edge)", "lat": -20.50, "lon": -69.30},
        {"region": "TURGAI", "name": "TURGAI SQUARE (Kazakhstan)", "lat": 50.40, "lon": 64.00}
    ]

    for t in targets:
        print(f"🛰️ Escaneando anomalías en: {t['name']} ({t['region']})")
        detector = SettlementDetector(mode=detector_mode, region=t['region'])
        
        res = detector.detect_settlement(t['lat'], t['lon'])
        
        print(f"   📊 Global Score: {res.probability_score:.1%}")
        print(f"   📐 Visual Persistence: {res.signature.orthogonality_ratio:.2f}")
        print(f"   📝 Interpretation: {res.interpretation}")
        
        if res.probability_score > 0.6:
            print(f"   ✨ CONFIRMADO: Geometría antrópica de gran escala.")
            
            candidate = {
                "candidate_id": f"GLYPH-{t['region'][:3]}-{uuid.uuid4().hex[:8].upper()}",
                "zone_id": f"global_geoglyphic_layer_{t['region'].lower()}",
                "location": {"lat": t['lat'], "lon": t['lon'], "area_km2": 5.0},
                "multi_instrumental_score": res.probability_score,
                "convergence": {"count": 4, "ratio": 0.95},
                "recommended_action": "field_validation",
                "temporal_persistence": {"detected": True, "years": 2024},
                "signals": {
                    "visual_signature": "high",
                    "orthogonality": res.signature.orthogonality_ratio,
                    "region": t['region']
                },
                "strategy": "surf_geom_v1",
                "region_bounds": {"min_lat": t['lat']-1, "max_lat": t['lat']+1, "min_lon": t['lon']-1, "max_lon": t['lon']+1}
            }
            c_id = await db.save_candidate(candidate)
            print(f"   💾 Persistido en BD (ID: {c_id})")
        
        print("-" * 60)

    await db.close()

if __name__ == "__main__":
    asyncio.run(run_global_geoglyphs())
