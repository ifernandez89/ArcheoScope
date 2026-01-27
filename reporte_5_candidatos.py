#!/usr/bin/env python3
import asyncpg
import asyncio

async def reporte():
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    # Obtener todos los analysis_id únicos
    analyses = await conn.fetch("""
        SELECT DISTINCT analysis_id, region_name, 
               latitude, longitude,
               MIN(measurement_timestamp) as timestamp
        FROM measurements
        GROUP BY analysis_id, region_name, latitude, longitude
        ORDER BY MIN(measurement_timestamp)
    """)
    
    print("="*80)
    print("REPORTE - 5 CANDIDATOS ARQUEOLOGICOS")
    print("="*80)
    
    for idx, analysis in enumerate(analyses, 1):
        analysis_id = analysis['analysis_id']
        region = analysis['region_name']
        lat = analysis['latitude']
        lon = analysis['longitude']
        
        # Contar instrumentos
        total = await conn.fetchval(
            'SELECT COUNT(*) FROM measurements WHERE analysis_id = $1',
            analysis_id
        )
        
        usables = await conn.fetchval(
            "SELECT COUNT(*) FROM measurements WHERE analysis_id = $1 AND data_mode IN ('OK', 'DERIVED')",
            analysis_id
        )
        
        # Obtener instrumentos OK
        ok_instruments = await conn.fetch(
            "SELECT instrument_name, value, confidence FROM measurements WHERE analysis_id = $1 AND data_mode IN ('OK', 'DERIVED')",
            analysis_id
        )
        
        print(f"\n{idx}. {region}")
        print(f"   Coords: {lat:.2f}, {lon:.2f}")
        print(f"   Instrumentos: {usables}/{total} usables")
        
        if ok_instruments:
            print(f"   Datos:")
            for inst in ok_instruments:
                print(f"      - {inst['instrument_name']}: {inst['value']:.2f} (conf: {inst['confidence']:.2f})")
        else:
            print(f"   Sin datos usables")
    
    print("\n" + "="*80)
    print("RESUMEN GLOBAL")
    print("="*80)
    
    total_measurements = await conn.fetchval('SELECT COUNT(*) FROM measurements')
    usable_measurements = await conn.fetchval("SELECT COUNT(*) FROM measurements WHERE data_mode IN ('OK', 'DERIVED')")
    
    print(f"Total mediciones: {total_measurements}")
    print(f"Mediciones usables: {usable_measurements} ({usable_measurements/total_measurements*100:.1f}%)")
    print(f"Candidatos analizados: {len(analyses)}")
    
    await conn.close()

asyncio.run(reporte())
