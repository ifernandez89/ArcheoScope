#!/usr/bin/env python3
"""
Guardador de resultados de Predicción Ciega en Base de Datos
=============================================================
"""

import asyncio
import asyncpg
import json
import os
from datetime import datetime
from pathlib import Path


async def save_blind_prediction_to_db(results_file: str):
    """Guarda resultados de predicción ciega en la base de datos."""
    
    # Leer resultados del JSON
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Conectar a la BD
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("⚠️ DATABASE_URL no configurada. Resultados solo en JSON.")
        return
    
    try:
        conn = await asyncpg.connect(database_url)
        print(f"✅ Conectado a PostgreSQL")
        
        # Crear tabla si no existe
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS blind_prediction_results (
                id SERIAL PRIMARY KEY,
                site_id VARCHAR(50) NOT NULL,
                site_name VARCHAR(255) NOT NULL,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                analysis_radius_km DOUBLE PRECISION,
                prediction_hypothesis TEXT,
                material_expected VARCHAR(255),
                context TEXT,
                
                -- Resultados TIMT
                g1_geometry DOUBLE PRECISION,
                g2_persistence DOUBLE PRECISION,
                g3_anomaly DOUBLE PRECISION,
                g4_modularity INTEGER,
                msf DOUBLE PRECISION,
                classification VARCHAR(100),
                
                -- Estimación CHI
                chi_score_estimated DOUBLE PRECISION,
                chi_confidence VARCHAR(50),
                
                -- Metadata
                blind_protocol BOOLEAN DEFAULT TRUE,
                interpretation_pending BOOLEAN DEFAULT TRUE,
                analysis_timestamp TIMESTAMP,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        print(f"✅ Tabla blind_prediction_results lista")
        
        # Insertar resultados
        inserted = 0
        for result in results:
            timt = result.get('timt_analysis', {})
            chi_est = result.get('chi_estimation', {})
            
            await conn.execute("""
                INSERT INTO blind_prediction_results (
                    site_id, site_name, latitude, longitude, analysis_radius_km,
                    prediction_hypothesis, material_expected, context,
                    g1_geometry, g2_persistence, g3_anomaly, g4_modularity, msf,
                    classification, chi_score_estimated, chi_confidence,
                    analysis_timestamp
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
            """,
                result['site_id'],
                result['site_name'],
                result['coordinates']['lat'],
                result['coordinates']['lon'],
                result['analysis_radius_km'],
                result['prediction_hypothesis'],
                result['material_expected'],
                result['context'],
                timt.get('g1_geometry'),
                timt.get('g2_persistence'),
                timt.get('g3_anomaly'),
                timt.get('g4_modularity'),
                timt.get('msf'),
                timt.get('classification'),
                chi_est.get('chi_score_estimated'),
                chi_est.get('confidence'),
                datetime.fromisoformat(result['timestamp'])
            )
            
            inserted += 1
            status = "✅" if timt.get('success') else "❌"
            print(f"   {status} {result['site_name']}")
        
        await conn.close()
        
        print(f"\n✅ {inserted}/{len(results)} resultados guardados en BD")
        
    except Exception as e:
        print(f"❌ Error guardando en BD: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Buscar el archivo más reciente
        files = list(Path(".").glob("BLIND_PREDICTION_MISSION_*.json"))
        if not files:
            print("❌ No se encontró archivo de resultados")
            sys.exit(1)
        
        latest_file = max(files, key=lambda p: p.stat().st_mtime)
        print(f"📄 Usando archivo más reciente: {latest_file}")
    else:
        latest_file = sys.argv[1]
    
    asyncio.run(save_blind_prediction_to_db(str(latest_file)))
