#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importar Candidatas REALES a la Base de Datos
"""

import asyncio
import json
import sys
import psycopg2
from psycopg2.extras import Json

DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}


def import_candidates():
    """Importar candidatas con datos reales a PostgreSQL"""
    
    print("="*80)
    print("IMPORTACION DE CANDIDATAS REALES A BASE DE DATOS")
    print("="*80)
    
    # Conectar a BD
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Leer archivo JSON
    json_file = "real_candidates_20260125_232040.json"
    
    print(f"\nLeyendo archivo: {json_file}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    candidates = data['candidates']
    
    print(f"OK - {len(candidates)} candidatas encontradas")
    print(f"Generadas: {data['generation_date']}")
    
    # Importar cada candidata
    print(f"\n{'='*80}")
    print("IMPORTANDO CANDIDATAS")
    print(f"{'='*80}")
    
    imported_count = 0
    
    for i, candidate in enumerate(candidates, 1):
        print(f"\n{i}. {candidate['region_name']}")
        print(f"   ID: {candidate['candidate_id']}")
        print(f"   Score: {candidate['multi_instrumental_score']:.3f}")
        print(f"   Prioridad: {candidate['priority']}")
        
        try:
            location = candidate['location']
            bbox = location['bbox']
            
            # INSERT directo
            cursor.execute("""
                INSERT INTO archaeological_candidates (
                    candidate_id,
                    zone_id,
                    center_lat,
                    center_lon,
                    area_km2,
                    multi_instrumental_score,
                    convergence_count,
                    convergence_ratio,
                    recommended_action,
                    temporal_persistence,
                    temporal_years,
                    signals,
                    strategy,
                    region_bounds
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (candidate_id) DO UPDATE SET
                    multi_instrumental_score = EXCLUDED.multi_instrumental_score,
                    convergence_count = EXCLUDED.convergence_count
                RETURNING id
            """, (
                candidate['candidate_id'],
                candidate['zone_id'],
                location['lat'],
                location['lon'],
                1.0,
                candidate['multi_instrumental_score'],
                candidate['convergence']['count'],
                candidate['convergence']['ratio'],
                'field_validation' if candidate['priority'] in ['CRITICAL', 'HIGH'] else 'detailed_analysis',
                True,
                0,
                Json(candidate.get('real_data_sources', {})),
                'real_satellite_data',
                Json({
                    'lat_min': bbox[0],
                    'lat_max': bbox[1],
                    'lon_min': bbox[2],
                    'lon_max': bbox[3]
                })
            ))
            
            result = cursor.fetchone()
            db_id = result[0] if result else None
            
            conn.commit()
            
            print(f"   OK - Importada (DB ID: {db_id})")
            imported_count += 1
            
        except Exception as e:
            print(f"   ERROR: {e}")
            conn.rollback()
    
    print(f"\n{'='*80}")
    print(f"IMPORTACION COMPLETADA")
    print(f"{'='*80}")
    
    print(f"\nRESUMEN:")
    print(f"   Total candidatas: {len(candidates)}")
    print(f"   Importadas: {imported_count}")
    print(f"   Fallidas: {len(candidates) - imported_count}")
    
    # Verificar en BD
    print(f"\nVerificando en base de datos...")
    
    cursor.execute("SELECT COUNT(*) FROM archaeological_candidates")
    total = cursor.fetchone()[0]
    
    print(f"\nTotal candidatas en BD: {total}")
    
    cursor.close()
    conn.close()
    
    return imported_count > 0


if __name__ == "__main__":
    print("\nIniciando importacion...\n")
    
    success = import_candidates()
    
    if success:
        print("\nOK - Importacion exitosa!")
        print("\nProximo paso:")
        print("   - Visualizar en el mapa de ArcheoScope")
        print("   - http://localhost:8080/priority_zones_map.html")
        sys.exit(0)
    else:
        print("\nERROR - Importacion fallida")
        sys.exit(1)
