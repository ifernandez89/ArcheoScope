#!/usr/bin/env python3
"""
Buscar candidatos con ANOMALÍAS en la BD.

Criterios:
1. Anomalía instrumental > 0 (algo detectado)
2. Origen antropogénico > 50% (posible origen humano)
3. Actividad > 0 (actividad actual)
4. NO son sitios históricos conocidos
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def find_anomalous_candidates():
    """Buscar candidatos con anomalías."""
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL no configurada")
        return
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("="*70)
        print("🔍 BÚSQUEDA DE CANDIDATOS CON ANOMALÍAS")
        print("="*70)
        
        # Total sitios
        total = await conn.fetchval("SELECT COUNT(*) FROM archaeological_sites")
        print(f"\n📊 Total sitios en BD: {total:,}")
        
        # Buscar por tipo de sitio
        print(f"\n📋 DISTRIBUCIÓN POR TIPO:")
        types = await conn.fetch("""
            SELECT "siteType", COUNT(*) as count
            FROM archaeological_sites
            GROUP BY "siteType"
            ORDER BY count DESC
        """)
        
        for t in types[:10]:
            print(f"   {t['siteType']}: {t['count']:,}")
        
        # Buscar candidatos (no confirmados)
        print(f"\n🔍 CANDIDATOS (no confirmados):")
        candidates = await conn.fetch("""
            SELECT 
                name,
                country,
                "siteType",
                "environmentType",
                "confidenceLevel",
                description,
                latitude,
                longitude
            FROM archaeological_sites
            WHERE "confidenceLevel" = 'CANDIDATE'
               OR "siteType" = 'UNKNOWN'
            ORDER BY "createdAt" DESC
            LIMIT 20
        """)
        
        print(f"   Total candidatos: {len(candidates)}")
        
        if candidates:
            print(f"\n🏺 MUESTRA DE CANDIDATOS:")
            for i, c in enumerate(candidates[:10], 1):
                print(f"\n{i}. {c['name']}, {c['country']}")
                print(f"   Tipo: {c['siteType']} | Ambiente: {c['environmentType']}")
                print(f"   Confianza: {c['confidenceLevel']}")
                print(f"   Coords: ({c['latitude']:.4f}, {c['longitude']:.4f})")
                
                # Extraer métricas de la descripción si existen
                desc = c['description']
                if 'Origen' in desc:
                    print(f"   Desc: {desc[:100]}...")
                elif 'Probabilidad antropogénica' in desc:
                    # Descripción antigua
                    import re
                    match = re.search(r'Probabilidad antropogénica: ([\d.]+)', desc)
                    if match:
                        prob = float(match.group(1))
                        print(f"   ⚠️ Prob legacy: {prob:.1%} (descripción antigua)")
        
        # Buscar sitios con descripciones que mencionen anomalía
        print(f"\n🚨 SITIOS CON MENCIÓN DE ANOMALÍA:")
        anomalous = await conn.fetch("""
            SELECT 
                name,
                country,
                description,
                "siteType",
                "confidenceLevel"
            FROM archaeological_sites
            WHERE description LIKE '%Anomaly score%'
               OR description LIKE '%anomalía%'
            LIMIT 10
        """)
        
        if anomalous:
            for a in anomalous:
                print(f"\n• {a['name']}, {a['country']}")
                print(f"  Tipo: {a['siteType']} | Confianza: {a['confidenceLevel']}")
                
                # Extraer anomaly score
                import re
                match = re.search(r'Anomaly score: ([\d.]+)', a['description'])
                if match:
                    score = float(match.group(1))
                    print(f"  🔴 Anomaly score: {score:.3f}")
        else:
            print("   No se encontraron sitios con anomalía en descripción")
        
        # Buscar por acción recomendada
        print(f"\n🎯 SITIOS POR ACCIÓN RECOMENDADA:")
        actions = await conn.fetch("""
            SELECT 
                name,
                country,
                description,
                "confidenceLevel"
            FROM archaeological_sites
            WHERE description LIKE '%field_verification%'
               OR description LIKE '%monitoring_targeted%'
            LIMIT 10
        """)
        
        if actions:
            for a in actions:
                print(f"\n• {a['name']}, {a['country']}")
                print(f"  Confianza: {a['confidenceLevel']}")
                
                # Extraer acción
                if 'field_verification' in a['description']:
                    print(f"  ✅ Acción: FIELD_VERIFICATION")
                elif 'monitoring_targeted' in a['description']:
                    print(f"  🎯 Acción: MONITORING_TARGETED")
        
        # Estadísticas de confianza
        print(f"\n📊 DISTRIBUCIÓN POR NIVEL DE CONFIANZA:")
        confidence = await conn.fetch("""
            SELECT "confidenceLevel", COUNT(*) as count
            FROM archaeological_sites
            GROUP BY "confidenceLevel"
            ORDER BY count DESC
        """)
        
        for c in confidence:
            print(f"   {c['confidenceLevel']}: {c['count']:,}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(find_anomalous_candidates())
