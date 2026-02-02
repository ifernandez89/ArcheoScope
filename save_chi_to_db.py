#!/usr/bin/env python3
"""
Guardador de resultados CHI en Base de Datos PostgreSQL
========================================================
"""

import asyncio
import asyncpg
import json
import os
from datetime import datetime
from pathlib import Path


async def save_chi_results_to_db(results_file: str):
    """Guarda resultados CHI en la base de datos."""
    
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
            CREATE TABLE IF NOT EXISTS cognitive_homology_results (
                id SERIAL PRIMARY KEY,
                site_name VARCHAR(255) NOT NULL,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                chi_score DOUBLE PRECISION NOT NULL,
                graph_isomorphism DOUBLE PRECISION,
                entropy_correlation DOUBLE PRECISION,
                rank_correlation DOUBLE PRECISION,
                structural_order DOUBLE PRECISION,
                is_significant BOOLEAN,
                interpretation TEXT,
                celestial_pattern VARCHAR(100) DEFAULT 'Orion Belt',
                analysis_timestamp TIMESTAMP DEFAULT NOW(),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        print(f"✅ Tabla cognitive_homology_results lista")
        
        # Insertar resultados
        inserted = 0
        for result in results:
            site = result['site_name']
            coords = result['coordinates']
            chi = result['chi_analysis']
            
            await conn.execute("""
                INSERT INTO cognitive_homology_results (
                    site_name, latitude, longitude,
                    chi_score, graph_isomorphism, entropy_correlation,
                    rank_correlation, structural_order, is_significant,
                    interpretation, analysis_timestamp
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """,
                site,
                coords['lat'],
                coords['lon'],
                chi['chi_score'],
                chi['graph_isomorphism'],
                chi['entropy_correlation'],
                chi['rank_correlation'],
                chi['structural_order'],
                chi['is_significant'],
                chi['interpretation'],
                datetime.fromisoformat(result['timestamp'])
            )
            
            inserted += 1
            print(f"   ✅ {site}: CHI={chi['chi_score']:.3f}")
        
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
        files = list(Path(".").glob("GLOBAL_CHI_MISSION_*.json"))
        if not files:
            print("❌ No se encontró archivo de resultados")
            sys.exit(1)
        
        latest_file = max(files, key=lambda p: p.stat().st_mtime)
        print(f"📄 Usando archivo más reciente: {latest_file}")
    else:
        latest_file = sys.argv[1]
    
    asyncio.run(save_chi_results_to_db(str(latest_file)))
