#!/usr/bin/env python3
"""
Verificar cuáles fueron los 5 candidatos medidos originalmente.
"""

import asyncio
import asyncpg

async def verificar_candidatos():
    """Verificar los 5 candidatos medidos."""
    
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    print("="*80)
    print("VERIFICACIÓN DE LOS 5 CANDIDATOS MEDIDOS")
    print("="*80)
    
    # Obtener todos los analysis_id únicos de measurements
    candidatos = await conn.fetch("""
        SELECT DISTINCT
            analysis_id,
            region_name,
            latitude,
            longitude,
            measurement_timestamp
        FROM measurements
        ORDER BY measurement_timestamp
    """)
    
    print(f"\nTotal de candidatos con mediciones: {len(candidatos)}\n")
    
    for idx, candidato in enumerate(candidatos, 1):
        analysis_id = candidato['analysis_id']
        region_name = candidato['region_name']
        lat = float(candidato['latitude'])
        lon = float(candidato['longitude'])
        timestamp = candidato['measurement_timestamp']
        
        print(f"{'='*80}")
        print(f"CANDIDATO {idx}: {region_name}")
        print(f"{'='*80}")
        print(f"Analysis ID: {analysis_id}")
        print(f"Coordenadas: {lat:.4f}, {lon:.4f}")
        print(f"Timestamp: {timestamp}")
        
        # Contar mediciones
        measurements = await conn.fetch("""
            SELECT instrument_name, value, data_mode
            FROM measurements
            WHERE analysis_id = $1
            ORDER BY instrument_name
        """, analysis_id)
        
        print(f"\nMediciones: {len(measurements)} instrumentos")
        for m in measurements:
            print(f"  - {m['instrument_name']}: {m['value']:.3f} ({m['data_mode']})")
        
        # Ver si tiene análisis guardado
        analysis = await conn.fetchrow("""
            SELECT id, result_type, archaeological_probability
            FROM archaeological_candidate_analyses
            WHERE candidate_name = $1
            ORDER BY created_at DESC
            LIMIT 1
        """, region_name)
        
        if analysis:
            print(f"\nAnálisis guardado:")
            print(f"  ID: {analysis['id']}")
            print(f"  Tipo: {analysis['result_type']}")
            print(f"  Probabilidad: {analysis['archaeological_probability']:.3f}")
        else:
            print(f"\n⚠️ NO tiene análisis guardado")
        
        print()
    
    # Resumen
    print("="*80)
    print("RESUMEN")
    print("="*80)
    print(f"Total candidatos medidos: {len(candidatos)}")
    
    total_measurements = await conn.fetchval("SELECT COUNT(*) FROM measurements")
    print(f"Total mediciones en BD: {total_measurements}")
    
    total_analyses = await conn.fetchval("SELECT COUNT(*) FROM archaeological_candidate_analyses")
    print(f"Total análisis guardados: {total_analyses}")
    
    total_candidates = await conn.fetchval("SELECT COUNT(*) FROM archaeological_candidates")
    print(f"Total candidatos en tabla: {total_candidates}")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(verificar_candidatos())
