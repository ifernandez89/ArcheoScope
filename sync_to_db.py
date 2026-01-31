#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - DB SYNC UTILITY
Migrando descubrimientos anteriores (RAK & GIZA) a PostgreSQL.
"""
import sys
import os
import json
import asyncio
import uuid

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Cargar módulo de base de datos directamente
import importlib.util
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "database.py")
spec = importlib.util.spec_from_file_location("database_module", db_path)
db_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db_module)
ArcheoScopeDB = db_module.ArcheoScopeDB

async def sync_previous():
    db = ArcheoScopeDB()
    await db.connect()
    print("🚀 Sincronizando campañas anteriores a la Base de Datos...")

    # 1. RUB' AL KHALI DATA
    try:
        with open('RAK_NETWORK_ANALYSIS.json', 'r') as f:
            rak_data = json.load(f)
            for site in rak_data:
                candidate = {
                    "candidate_id": f"RAK-DISC-{uuid.uuid4().hex[:8].upper()}",
                    "zone_id": "rub_al_khali_interior_v2",
                    "location": {"lat": site['coords']['lat'], "lon": site['coords']['lon'], "area_km2": site['metrics']['total_area_km2']},
                    "multi_instrumental_score": site['score'],
                    "convergence": {"count": 4, "ratio": 0.9},
                    "recommended_action": "field_validation",
                    "temporal_persistence": {"detected": True, "years": 2024},
                    "signals": {"type": "neolithic_hub", "region": "RUB_AL_KHALI", "function": site['function']},
                    "strategy": "network_scan_v1",
                    "region_bounds": {"min_lat": 20, "max_lat": 21, "min_lon": 50, "max_lon": 52}
                }
                await db.save_candidate(candidate)
        print("✅ Rub' al Khali sincronizado.")
    except Exception as e: print(f"⚠️ Error RAK: {e}")

    # 2. GIZA DATA
    giza_coords = {
        "GIZA-SITE-A": (29.95, 30.95),
        "GIZA-SITE-B": (29.40, 30.70),
        "GIZA-SITE-C": (29.60, 31.35)
    }
    try:
        with open('GIZA_DISCOVERY_DATA.json', 'r') as f:
            giza_data = json.load(f)
            for site in giza_data:
                lat, lon = giza_coords.get(site['site_code'], (0,0))
                candidate = {
                    "candidate_id": f"GIZA-DISC-{uuid.uuid4().hex[:8].upper()}",
                    "zone_id": "giza_extended_logistics",
                    "location": {"lat": lat, "lon": lon, "area_km2": site['core_area_km2']},
                    "multi_instrumental_score": site['score'],
                    "convergence": {"count": 3, "ratio": 0.8},
                    "recommended_action": "field_validation",
                    "temporal_persistence": {"detected": True, "years": 2024},
                    "signals": {"type": "dynastic_logistics", "region": "GIZA"},
                    "strategy": "giza_mode_v2.1",
                    "region_bounds": {"min_lat": 29, "max_lat": 31, "min_lon": 30, "max_lon": 32}
                }
                await db.save_candidate(candidate)
        print("✅ Giza sincronizado.")
    except Exception as e: print(f"⚠️ Error Giza: {e}")

    await db.close()

if __name__ == "__main__":
    asyncio.run(sync_previous())
