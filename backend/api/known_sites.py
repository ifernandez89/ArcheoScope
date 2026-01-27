#!/usr/bin/env python3
"""
API Endpoints para Sitios Arqueológicos Conocidos
Permite visualizar y filtrar sitios de la BD
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

def get_db_connection():
    """Obtener conexión a BD"""
    try:
        return psycopg2.connect(os.getenv("DATABASE_URL"))
    except Exception as e:
        print(f"Error conectando a BD: {e}")
        return None

@router.get("/known-sites")
async def get_known_sites(
    lat_min: Optional[float] = Query(None, description="Latitud mínima"),
    lat_max: Optional[float] = Query(None, description="Latitud máxima"),
    lon_min: Optional[float] = Query(None, description="Longitud mínima"),
    lon_max: Optional[float] = Query(None, description="Longitud máxima"),
    country: Optional[str] = Query(None, description="Filtrar por país"),
    limit: int = Query(1000, description="Máximo de sitios a retornar", le=5000)
):
    """
    Obtener sitios arqueológicos conocidos de la BD
    
    Parámetros:
    - bbox: Filtrar por región (lat_min, lat_max, lon_min, lon_max)
    - country: Filtrar por país
    - limit: Máximo de resultados (default: 1000, max: 5000)
    
    Returns:
    - Lista de sitios con coordenadas, nombre, país
    """
    
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error conectando a base de datos")
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Construir query
        query = """
            SELECT 
                id,
                name,
                latitude,
                longitude,
                country,
                period,
                "siteType"
            FROM archaeological_sites
            WHERE latitude IS NOT NULL 
              AND longitude IS NOT NULL
        """
        
        params = []
        
        # Filtros opcionales
        if lat_min is not None and lat_max is not None:
            query += " AND latitude BETWEEN %s AND %s"
            params.extend([lat_min, lat_max])
        
        if lon_min is not None and lon_max is not None:
            query += " AND longitude BETWEEN %s AND %s"
            params.extend([lon_min, lon_max])
        
        if country:
            query += " AND country ILIKE %s"
            params.append(f"%{country}%")
        
        query += f" LIMIT {limit}"
        
        cur.execute(query, params)
        sites = cur.fetchall()
        
        # Convertir a lista de dicts
        result = []
        for site in sites:
            result.append({
                'id': site['id'],
                'name': site['name'] or 'Sitio sin nombre',
                'lat': float(site['latitude']),
                'lon': float(site['longitude']),
                'country': site['country'] or 'Desconocido',
                'period': site['period'],
                'type': site['siteType']
            })
        
        cur.close()
        conn.close()
        
        return {
            'total': len(result),
            'sites': result,
            'filters': {
                'bbox': {
                    'lat_min': lat_min,
                    'lat_max': lat_max,
                    'lon_min': lon_min,
                    'lon_max': lon_max
                } if lat_min else None,
                'country': country
            }
        }
        
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Error obteniendo sitios: {str(e)}")

@router.get("/known-sites/regions")
async def get_regions():
    """
    Obtener lista de regiones/países con sitios
    
    Returns:
    - Lista de países con conteo de sitios
    """
    
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error conectando a base de datos")
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                country,
                COUNT(*) as count,
                MIN(latitude) as lat_min,
                MAX(latitude) as lat_max,
                MIN(longitude) as lon_min,
                MAX(longitude) as lon_max
            FROM archaeological_sites
            WHERE country IS NOT NULL
              AND latitude IS NOT NULL
              AND longitude IS NOT NULL
            GROUP BY country
            ORDER BY count DESC
            LIMIT 50
        """)
        
        regions = []
        for row in cur.fetchall():
            regions.append({
                'country': row['country'],
                'count': row['count'],
                'bbox': {
                    'lat_min': float(row['lat_min']),
                    'lat_max': float(row['lat_max']),
                    'lon_min': float(row['lon_min']),
                    'lon_max': float(row['lon_max'])
                }
            })
        
        cur.close()
        conn.close()
        
        return {
            'total_regions': len(regions),
            'regions': regions
        }
        
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Error obteniendo regiones: {str(e)}")

@router.get("/known-sites/{site_id}")
async def get_site_details(site_id: str):
    """
    Obtener detalles de un sitio específico
    
    Returns:
    - Información completa del sitio
    """
    
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error conectando a base de datos")
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT *
            FROM archaeological_sites
            WHERE id = %s
        """, (site_id,))
        
        site = cur.fetchone()
        
        if not site:
            raise HTTPException(status_code=404, detail="Sitio no encontrado")
        
        cur.close()
        conn.close()
        
        return dict(site)
        
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Error obteniendo sitio: {str(e)}")

@router.get("/known-sites/nearby/{lat}/{lon}")
async def get_nearby_sites(
    lat: float,
    lon: float,
    radius_km: float = Query(50, description="Radio de búsqueda en km", le=500)
):
    """
    Obtener sitios cercanos a una coordenada
    
    Parámetros:
    - lat, lon: Coordenadas del punto
    - radius_km: Radio de búsqueda en km (default: 50km, max: 500km)
    
    Returns:
    - Lista de sitios cercanos ordenados por distancia
    """
    
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error conectando a base de datos")
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Calcular bbox aproximado (1° ≈ 111km)
        degrees = radius_km / 111.0
        
        cur.execute("""
            SELECT 
                id,
                name,
                latitude,
                longitude,
                country,
                period,
                "siteType"
            FROM archaeological_sites
            WHERE latitude IS NOT NULL 
              AND longitude IS NOT NULL
              AND latitude BETWEEN %s AND %s
              AND longitude BETWEEN %s AND %s
            LIMIT 100
        """, (
            lat - degrees, lat + degrees,
            lon - degrees, lon + degrees
        ))
        
        sites = []
        for row in cur.fetchall():
            # Calcular distancia en Python
            import math
            lat1, lon1 = math.radians(lat), math.radians(lon)
            lat2, lon2 = math.radians(float(row['latitude'])), math.radians(float(row['longitude']))
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            distance_km = 6371 * c
            
            if distance_km <= radius_km:
                sites.append({
                    'id': row['id'],
                    'name': row['name'] or 'Sitio sin nombre',
                    'lat': float(row['latitude']),
                    'lon': float(row['longitude']),
                    'country': row['country'] or 'Desconocido',
                    'period': row['period'],
                    'type': row['siteType'],
                    'distance_km': round(distance_km, 2)
                })
        
        # Ordenar por distancia
        sites.sort(key=lambda x: x['distance_km'])
        
        cur.close()
        conn.close()
        
        return {
            'center': {'lat': lat, 'lon': lon},
            'radius_km': radius_km,
            'total': len(sites),
            'sites': sites
        }
        
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Error buscando sitios cercanos: {str(e)}")
