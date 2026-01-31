#!/usr/bin/env python3
"""
Guardar resultados del escaneo de Rub' al Khali en BD
"""
import sys
import os
import asyncio
import importlib.util
import json
import uuid

# Setup DB import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
db_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "database.py")
spec = importlib.util.spec_from_file_location("full_database_module", db_file_path)
db_module = importlib.util.module_from_spec(spec)
sys.modules["full_database_module"] = db_module
spec.loader.exec_module(db_module)
ArcheoScopeDB = db_module.ArcheoScopeDB

async def save_rak_results():
    # Leer resultados del scan
    try:
        with open('RUB_AL_KHALI_SCAN_RESULTS.json', 'r') as f:
            findings = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró RUB_AL_KHALI_SCAN_RESULTS.json")
        return

    print(f"📊 Cargando {len(findings)} hallazgos a la Base de Datos...")
    
    db = ArcheoScopeDB()
    await db.connect()
    
    saved_count = 0
    try:
        for f in findings:
            # Generar datos enriquecidos para BD
            candidate_id = f"RAK_{uuid.uuid4().hex[:8]}"
            
            candidate_data = {
                'candidate_id': candidate_id,
                'zone_id': 'ZONE_RUB_AL_KHALI_MARGINS',
                'location': {
                    'lat': f['lat'],
                    'lon': f['lon'],
                    'area_km2': 0.25
                },
                'multi_instrumental_score': f['score'],
                'convergence': {'count': 1, 'ratio': f['score']},
                'recommended_action': 'field_validation',
                'temporal_persistence': {'detected': True, 'years': 3000},
                'signals': {
                    'type': 'geoglyph_detection',
                    'geoglyph_type': f['type'],
                    'context': f['context'],
                    'source': 'GRID_SCAN_V2.1'
                },
                'strategy': 'DESERT_EXTREME_GRID',
                'region_bounds': {}
            }
            
            id_db = await db.save_candidate(candidate_data)
            print(f"   ✅ Guardado: {f['id']} -> BD ID: {id_db}")
            saved_count += 1
            
    finally:
        await db.close()
        print(f"\n💾 Total guardados en BD: {saved_count}/{len(findings)}")

if __name__ == "__main__":
    asyncio.run(save_rak_results())
