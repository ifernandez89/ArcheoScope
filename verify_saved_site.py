#!/usr/bin/env python3
"""Verificar que el sitio se guardó correctamente."""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def verify():
    """Verificar último sitio guardado."""
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    # Obtener último sitio
    site = await conn.fetchrow("""
        SELECT * FROM archaeological_sites 
        WHERE "isReferencesite" = false
        ORDER BY "createdAt" DESC 
        LIMIT 1
    """)
    
    if site:
        print("\n📍 ÚLTIMO SITIO GUARDADO:")
        print("="*80)
        print(f"  ID: {site['id']}")
        print(f"  Nombre: {site['name']}")
        print(f"  Slug: {site['slug']}")
        print(f"  Ambiente: {site['environmentType']}")
        print(f"  Tipo: {site['siteType']}")
        print(f"  Confianza: {site['confidenceLevel']}")
        print(f"  Coordenadas: {site['latitude']:.4f}, {site['longitude']:.4f}")
        print(f"  País: {site['country']}")
        print(f"  Región: {site['region']}")
        print(f"  Descripción: {site['description']}")
        print(f"  Significancia: {site['scientificSignificance']}")
        print(f"  Es control: {site['isControlSite']}")
        print(f"  Fecha descubrimiento: {site['discoveryDate']}")
    
    # Obtener análisis asociado
    analysis = await conn.fetchrow("""
        SELECT * FROM archaeological_candidate_analyses 
        ORDER BY created_at DESC 
        LIMIT 1
    """)
    
    if analysis:
        print("\n📊 ANÁLISIS ASOCIADO:")
        print("="*80)
        print(f"  ID: {analysis['id']}")
        print(f"  Candidato: {analysis['candidate_name']}")
        print(f"  Región: {analysis['region']}")
        print(f"  Probabilidad: {analysis['archaeological_probability']:.3f}")
        print(f"  Anomaly Score: {analysis['anomaly_score']:.3f}")
        print(f"  Instrumentos: {analysis['instruments_measuring']}/{analysis['instruments_total']}")
    
    # Obtener mediciones
    measurements = await conn.fetch("""
        SELECT instrument_name, value, data_mode, source
        FROM measurements 
        WHERE latitude = $1 AND longitude = $2
        ORDER BY measurement_timestamp DESC
        LIMIT 10
    """, site['latitude'], site['longitude'])
    
    if measurements:
        print("\n🔬 MEDICIONES INSTRUMENTALES:")
        print("="*80)
        for m in measurements:
            status = "✅" if m['data_mode'] != 'NO_DATA' else "❌"
            print(f"  {status} {m['instrument_name']:<25} = {m['value']:.3f} ({m['data_mode']})")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(verify())
