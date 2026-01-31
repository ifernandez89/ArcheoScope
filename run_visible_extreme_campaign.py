#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - VISIBLE MODE EXTREMO
Goal: Identify only monumental structures (Type C, >= 92% Score)
Scientific Credibility: Rub' al Khali is expected to FAIL this scan.
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

async def run_extreme_visible():
    print("\n" + "🛡️"*40)
    print("ARCHEOSCOPE: VISIBLE MODE EXTREMO (TYPE C ONLY)")
    print("Criterion: Visible from Earth without processing (>= 92%)")
    print("🛡️"*40 + "\n")

    db = ArcheoScopeDB()
    await db.connect()
    
    # Campañas Segregadas
    campaigns = [
        {"region": "RAK_VISIBLE", "name": "RUB' AL KHALI (Dune Control)", "targets": [
            {"name": "RAK-VIS-01 (Kite-like)", "lat": 19.92, "lon": 51.05}
        ]},
        {"region": "HARRAT_KHAYBAR", "name": "HARRAT KHAYBAR (Saudi Arabia)", "targets": [
            {"name": "THE GATES OF KHAYBAR", "lat": 25.85, "lon": 39.65}
        ]},
        {"region": "GOBI_ALTAI", "name": "GOBI / ALTAI (Mongolia)", "targets": [
            {"name": "ENCLOSURE DELTA", "lat": 47.30, "lon": 90.80}
        ]},
        {"region": "ATACAMA_PEDREGOSO", "name": "ATACAMA BORDELANDS (Chile)", "targets": [
            {"name": "DESERT GEOGLYPH HUB", "lat": -22.95, "lon": -68.20}
        ]}
    ]

    for campaign in campaigns:
        region = campaign['region']
        print(f"\n🌍 SCANNING REGION: {campaign['name']}")
        detector = SettlementDetector(mode=SettlementMode.SURFACE_GEOMETRY_SCAN, region=region)
        
        for t in campaign['targets']:
            print(f"   📡 Target: {t['name']}")
            res = detector.detect_settlement(t['lat'], t['lon'])
            
            print(f"      📊 Score: {res.probability_score:.1%}")
            print(f"      📝 Verdict: {res.interpretation}")
            
            if res.probability_score >= 0.92:
                print(f"      ✅ GOLD STANDARD DETECTED (TYPE C)")
                
                candidate = {
                    "candidate_id": f"EXT-{region[:3].upper()}-{uuid.uuid4().hex[:8].upper()}",
                    "zone_id": f"extreme_visible_{region.lower()}",
                    "location": {"lat": t['lat'], "lon": t['lon'], "area_km2": 10.0},
                    "multi_instrumental_score": res.probability_score,
                    "convergence": {"count": 6, "ratio": 1.0},
                    "recommended_action": "field_validation",
                    "temporal_persistence": {"detected": True, "years": 2024},
                    "signals": {
                        "monumentality": "extreme",
                        "verdict": res.interpretation,
                        "region": region
                    },
                    "strategy": "visible_ext_92",
                    "region_bounds": {"min_lat": t['lat']-0.05, "max_lat": t['lat']+0.05, "min_lon": t['lon']-0.05, "max_lon": t['lon']+0.05}
                }
                c_id = await db.save_candidate(candidate)
                print(f"      💾 Persisted to DB (ID: {c_id})")
            else:
                print(f"      ❌ DISCARDED (Below Extreme Threshold)")
        
        print("-" * 60)

    await db.close()

if __name__ == "__main__":
    asyncio.run(run_extreme_visible())
