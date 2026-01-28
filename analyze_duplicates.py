#!/usr/bin/env python3
"""
Analizar sitios duplicados en la BD.

Criterios de duplicación:
1. Mismo nombre y país
2. Coordenadas muy cercanas (<1km)
3. Mismo slug
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from math import radians, cos, sin, asin, sqrt

load_dotenv()

def haversine(lon1, lat1, lon2, lat2):
    """Calcular distancia entre dos puntos en km."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radio de la Tierra en km
    return c * r

async def analyze_duplicates():
    """Analizar duplicados en la BD."""
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL no configurada")
        return
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("="*70)
        print("🔍 ANÁLISIS DE DUPLICADOS")
        print("="*70)
        
        total = await conn.fetchval("SELECT COUNT(*) FROM archaeological_sites")
        print(f"\n📊 Total sitios: {total:,}")
        
        # 1. Duplicados por nombre + país
        print(f"\n1️⃣ DUPLICADOS POR NOMBRE + PAÍS:")
        name_dupes = await conn.fetch("""
            SELECT name, country, COUNT(*) as count
            FROM archaeological_sites
            GROUP BY name, country
            HAVING COUNT(*) > 1
            ORDER BY count DESC
            LIMIT 20
        """)
        
        if name_dupes:
            print(f"   Total grupos duplicados: {len(name_dupes)}")
            total_dupes = sum(d['count'] for d in name_dupes)
            print(f"   Total sitios duplicados: {total_dupes:,}")
            
            print(f"\n   Top 10 duplicados:")
            for d in name_dupes[:10]:
                print(f"   • {d['name']}, {d['country']}: {d['count']} copias")
                
                # Obtener detalles
                details = await conn.fetch("""
                    SELECT id, latitude, longitude, "siteType", "confidenceLevel", "createdAt"
                    FROM archaeological_sites
                    WHERE name = $1 AND country = $2
                    ORDER BY "createdAt"
                """, d['name'], d['country'])
                
                if len(details) > 1:
                    # Verificar si son realmente duplicados (coordenadas cercanas)
                    first = details[0]
                    for other in details[1:]:
                        dist = haversine(
                            first['longitude'], first['latitude'],
                            other['longitude'], other['latitude']
                        )
                        if dist < 1.0:  # Menos de 1km
                            print(f"      ⚠️ Duplicado real: distancia {dist:.2f}km")
                        else:
                            print(f"      ✅ Sitios diferentes: distancia {dist:.2f}km")
        else:
            print("   ✅ No hay duplicados por nombre + país")
        
        # 2. Duplicados por slug
        print(f"\n2️⃣ DUPLICADOS POR SLUG:")
        slug_dupes = await conn.fetch("""
            SELECT slug, COUNT(*) as count
            FROM archaeological_sites
            GROUP BY slug
            HAVING COUNT(*) > 1
            ORDER BY count DESC
            LIMIT 10
        """)
        
        if slug_dupes:
            print(f"   Total slugs duplicados: {len(slug_dupes)}")
            for d in slug_dupes:
                print(f"   • {d['slug']}: {d['count']} copias")
        else:
            print("   ✅ No hay duplicados por slug")
        
        # 3. Coordenadas idénticas
        print(f"\n3️⃣ COORDENADAS IDÉNTICAS:")
        coord_dupes = await conn.fetch("""
            SELECT latitude, longitude, COUNT(*) as count
            FROM archaeological_sites
            GROUP BY latitude, longitude
            HAVING COUNT(*) > 1
            ORDER BY count DESC
            LIMIT 10
        """)
        
        if coord_dupes:
            print(f"   Total coordenadas duplicadas: {len(coord_dupes)}")
            for d in coord_dupes[:5]:
                print(f"   • ({d['latitude']:.4f}, {d['longitude']:.4f}): {d['count']} sitios")
                
                # Ver qué sitios están en esas coordenadas
                sites = await conn.fetch("""
                    SELECT name, country, "siteType"
                    FROM archaeological_sites
                    WHERE latitude = $1 AND longitude = $2
                    LIMIT 3
                """, d['latitude'], d['longitude'])
                
                for s in sites:
                    print(f"      - {s['name']}, {s['country']} ({s['siteType']})")
        else:
            print("   ✅ No hay coordenadas idénticas")
        
        # 4. Recomendaciones de limpieza
        print(f"\n{'='*70}")
        print("💡 RECOMENDACIONES")
        print(f"{'='*70}")
        
        if name_dupes:
            real_dupes = 0
            for d in name_dupes:
                details = await conn.fetch("""
                    SELECT latitude, longitude
                    FROM archaeological_sites
                    WHERE name = $1 AND country = $2
                """, d['name'], d['country'])
                
                if len(details) > 1:
                    first = details[0]
                    for other in details[1:]:
                        dist = haversine(
                            first['longitude'], first['latitude'],
                            other['longitude'], other['latitude']
                        )
                        if dist < 1.0:
                            real_dupes += 1
            
            if real_dupes > 0:
                print(f"\n⚠️ Se encontraron ~{real_dupes} duplicados reales")
                print(f"   Acción recomendada: Ejecutar script de deduplicación")
                print(f"   Criterio: Mantener el más antiguo (createdAt)")
            else:
                print(f"\n✅ Los 'duplicados' son sitios diferentes con mismo nombre")
                print(f"   Ejemplo: Múltiples 'Templo' en diferentes ubicaciones")
        else:
            print(f"\n✅ Base de datos limpia, sin duplicados detectados")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(analyze_duplicates())
