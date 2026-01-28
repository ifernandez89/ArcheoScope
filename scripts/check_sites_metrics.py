#!/usr/bin/env python3
"""
Verificar métricas de sitios en la BD.
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check_metrics():
    """Verificar métricas de sitios arqueológicos."""
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL no configurada")
        return
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Contar sitios totales
        total = await conn.fetchval("SELECT COUNT(*) FROM archaeological_sites")
        print(f"📊 Total sitios en BD: {total}")
        
        # Obtener muestra de sitios con métricas
        sites = await conn.fetch("""
            SELECT 
                name,
                country,
                description,
                "confidenceLevel" as confidence_level,
                "siteType" as site_type
            FROM archaeological_sites
            WHERE name IN (
                'Pirámides de Giza',
                'Machu Picchu',
                'Líneas de Nazca',
                'Teotihuacán',
                'Angkor Wat',
                'Stonehenge'
            )
            ORDER BY name
        """)
        
        print(f"\n🏛️ MUESTRA DE SITIOS CONOCIDOS:")
        print("="*70)
        
        for site in sites:
            print(f"\n{site['name']}, {site['country']}")
            print(f"  Tipo: {site['site_type']}")
            print(f"  Confianza: {site['confidence_level']}")
            print(f"  Descripción: {site['description'][:80]}...")
        
        # Verificar si hay análisis guardados
        analyses = await conn.fetch("""
            SELECT COUNT(*) as count, 
                   AVG(CAST(data->>'anthropic_probability' AS FLOAT)) as avg_prob
            FROM analyses
            WHERE data->>'anthropic_probability' IS NOT NULL
        """)
        
        if analyses and analyses[0]['count'] > 0:
            print(f"\n📈 ANÁLISIS EN BD:")
            print(f"  Total análisis: {analyses[0]['count']}")
            print(f"  Prob. antropogénica promedio: {analyses[0]['avg_prob']:.3f}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(check_metrics())
