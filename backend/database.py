"""
ArcheoScope - Database Module
Conexión y queries a PostgreSQL
"""

import os
import math
import asyncpg
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

class ArcheoScopeDB:
    """Clase para manejar conexiones a la base de datos"""
    
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        """Crear pool de conexiones"""
        if not self.pool:
            self.pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
    
    async def close(self):
        """Cerrar pool"""
        if self.pool:
            await self.pool.close()
    
    async def search_sites(
        self, 
        lat: float, 
        lon: float, 
        radius_km: float = 50,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Buscar sitios arqueológicos cerca de una ubicación
        
        Args:
            lat: Latitud
            lon: Longitud
            radius_km: Radio de búsqueda en kilómetros
            limit: Máximo número de resultados
        
        Returns:
            Lista de sitios encontrados
        """
        async with self.pool.acquire() as conn:
            # Calcular distancia usando fórmula de Haversine
            # 111.32 km por grado de latitud aproximadamente
            lat_delta = radius_km / 111.32
            lon_delta = radius_km / (111.32 * abs(math.cos(math.radians(lat))))
            
            query = '''
                SELECT 
                    id,
                    name,
                    slug,
                    "environmentType" as environment_type,
                    "siteType" as site_type,
                    "confidenceLevel" as confidence_level,
                    latitude,
                    longitude,
                    country,
                    region,
                    period,
                    "dateRangeStart" as date_range_start,
                    "dateRangeEnd" as date_range_end,
                    "unescoId" as unesco_id,
                    description,
                    "isReferencesite" as is_reference,
                    "isControlSite" as is_control,
                    -- Calcular distancia aproximada
                    (
                        6371 * acos(
                            cos(radians($1)) * cos(radians(latitude)) *
                            cos(radians(longitude) - radians($2)) +
                            sin(radians($1)) * sin(radians(latitude))
                        )
                    ) as distance_km
                FROM archaeological_sites
                WHERE 
                    latitude BETWEEN $1 - $3 AND $1 + $3
                    AND longitude BETWEEN $2 - $4 AND $2 + $4
                ORDER BY distance_km
                LIMIT $5
            '''
            
            rows = await conn.fetch(query, lat, lon, lat_delta, lon_delta, limit)
            
            return [dict(row) for row in rows]
    
    async def get_site_by_id(self, site_id: str) -> Optional[Dict[str, Any]]:
        """Obtener un sitio por ID"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT * FROM archaeological_sites WHERE id = $1',
                site_id
            )
            return dict(row) if row else None
    
    async def get_all_sites(self, limit: int = 1000, offset: int = 0) -> List[Dict[str, Any]]:
        """Obtener todos los sitios (paginado)"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                '''
                SELECT 
                    id, name, latitude, longitude, country,
                    "environmentType" as environment_type,
                    "siteType" as site_type,
                    "confidenceLevel" as confidence_level
                FROM archaeological_sites
                ORDER BY name
                LIMIT $1 OFFSET $2
                ''',
                limit, offset
            )
            return [dict(row) for row in rows]
    
    async def count_sites(self) -> int:
        """Contar total de sitios"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval('SELECT COUNT(*) FROM archaeological_sites')
    
    async def get_sites_by_country(self, country: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtener sitios por país"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                '''
                SELECT 
                    id, name, latitude, longitude, country,
                    "siteType" as site_type,
                    "confidenceLevel" as confidence_level
                FROM archaeological_sites
                WHERE country ILIKE $1
                ORDER BY name
                LIMIT $2
                ''',
                f'%{country}%', limit
            )
            return [dict(row) for row in rows]
    
    async def get_reference_sites(self) -> List[Dict[str, Any]]:
        """Obtener sitios de referencia para calibración"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                '''
                SELECT *
                FROM archaeological_sites
                WHERE "isReferencesite" = true
                ORDER BY name
                '''
            )
            return [dict(row) for row in rows]
    
    async def get_sites_paginated(
        self,
        limit: int = 100,
        offset: int = 0,
        environment_type: Optional[str] = None,
        country: Optional[str] = None,
        site_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Obtener sitios con paginación y filtros
        
        Args:
            limit: Número de resultados por página
            offset: Desplazamiento para paginación
            environment_type: Filtrar por tipo de ambiente (desert, forest, glacier, etc.)
            country: Filtrar por país
            site_type: Filtrar por tipo de sitio
        
        Returns:
            Dict con sitios, total, y metadatos de paginación
        """
        async with self.pool.acquire() as conn:
            # Construir query dinámicamente según filtros
            where_clauses = []
            params = []
            param_count = 1
            
            if environment_type:
                # Convertir a mayúsculas para match con enum PostgreSQL
                env_upper = environment_type.upper()
                where_clauses.append(f'"environmentType" = ${param_count}')
                params.append(env_upper)
                param_count += 1
            
            if country:
                where_clauses.append(f'country ILIKE ${param_count}')
                params.append(f'%{country}%')
                param_count += 1
            
            if site_type:
                where_clauses.append(f'"siteType" = ${param_count}')
                params.append(site_type)
                param_count += 1
            
            where_sql = ' AND '.join(where_clauses) if where_clauses else '1=1'
            
            # Query para contar total
            count_query = f'''
                SELECT COUNT(*) 
                FROM archaeological_sites 
                WHERE {where_sql}
            '''
            
            total = await conn.fetchval(count_query, *params)
            
            # Query para obtener sitios
            params.extend([limit, offset])
            sites_query = f'''
                SELECT 
                    id,
                    name,
                    slug,
                    "environmentType" as environment_type,
                    "siteType" as site_type,
                    "confidenceLevel" as confidence_level,
                    latitude,
                    longitude,
                    country,
                    region,
                    period,
                    "dateRangeStart" as date_range_start,
                    "dateRangeEnd" as date_range_end,
                    "unescoId" as unesco_id,
                    description,
                    "isReferencesite" as is_reference,
                    "isControlSite" as is_control,
                    "createdAt" as created_at
                FROM archaeological_sites
                WHERE {where_sql}
                ORDER BY name
                LIMIT ${param_count} OFFSET ${param_count + 1}
            '''
            
            rows = await conn.fetch(sites_query, *params)
            sites = [dict(row) for row in rows]
            
            return {
                'sites': sites,
                'total': total,
                'limit': limit,
                'offset': offset,
                'page': (offset // limit) + 1 if limit > 0 else 1,
                'total_pages': (total + limit - 1) // limit if limit > 0 else 1
            }
    
    async def get_environment_types_stats(self) -> List[Dict[str, Any]]:
        """Obtener estadísticas de sitios por tipo de ambiente"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                '''
                SELECT 
                    "environmentType" as environment_type,
                    COUNT(*) as count
                FROM archaeological_sites
                WHERE "environmentType" IS NOT NULL
                GROUP BY "environmentType"
                ORDER BY count DESC
                '''
            )
            return [dict(row) for row in rows]
    
    async def get_sites_by_environment(
        self,
        environment_type: str,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Obtener sitios filtrados por tipo de ambiente/terreno
        
        Args:
            environment_type: Tipo de ambiente (desert, forest, glacier, shallow_sea, etc.)
            limit: Número de resultados
            offset: Desplazamiento para paginación
        
        Returns:
            Dict con sitios y metadatos
        """
        return await self.get_sites_paginated(
            limit=limit,
            offset=offset,
            environment_type=environment_type
        )

# Instancia global
db = ArcheoScopeDB()
