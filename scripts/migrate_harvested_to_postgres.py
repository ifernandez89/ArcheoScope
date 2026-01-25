#!/usr/bin/env python3
"""
Migración de Sitios Recopilados a PostgreSQL
============================================

Migra los 75,595+ sitios recopilados de harvested_complete.json a PostgreSQL.
"""

import json
import asyncio
import asyncpg
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL no configurada en .env")
    exit(1)

class HarvestedSitesMigrator:
    """Migrador de sitios recopilados a PostgreSQL"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.conn = None
        self.stats = {
            'total': 0,
            'inserted': 0,
            'skipped': 0,
            'errors': 0
        }
        
    async def connect(self):
        """Conectar a PostgreSQL"""
        print("Conectando a PostgreSQL...")
        self.conn = await asyncpg.connect(self.database_url)
        print("Conectado exitosamente")
        
    async def disconnect(self):
        """Desconectar"""
        if self.conn:
            await self.conn.close()
            print("Desconectado")
    
    def load_harvested_data(self) -> Dict[str, Any]:
        """Cargar datos recopilados"""
        print("\nCargando sitios recopilados...")
        
        json_path = Path(__file__).parent.parent / "harvested_complete.json"
        
        if not json_path.exists():
            raise FileNotFoundError(f"No se encontró: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total = data.get('metadata', {}).get('total_sites', 0)
        print(f"Cargados {total:,} sitios")
        
        return data
    
    def infer_environment_type(self, site: Dict[str, Any]) -> str:
        """Inferir tipo de ambiente basado en datos disponibles"""
        # Por ahora, usar UNKNOWN - luego se puede mejorar con clasificación
        return 'UNKNOWN'
    
    def infer_site_type(self, site: Dict[str, Any]) -> str:
        """Inferir tipo de sitio"""
        site_type = site.get('site_type', '').lower()
        heritage = site.get('heritage', '').lower()
        
        # Mapeo básico
        if 'temple' in site_type or 'temple' in heritage:
            return 'TEMPLE_COMPLEX'
        elif 'fort' in site_type or 'castle' in site_type:
            return 'FORTIFICATION'
        elif 'burial' in site_type or 'tomb' in site_type:
            return 'BURIAL_SITE'
        elif 'settlement' in site_type or 'city' in site_type:
            return 'URBAN_SETTLEMENT'
        
        return 'UNKNOWN'
    
    def determine_confidence(self, site: Dict[str, Any]) -> str:
        """Determinar nivel de confianza"""
        conf = site.get('confidence_level', '').upper()
        
        mapping = {
            'CONFIRMED': 'CONFIRMED',
            'HIGH': 'HIGH',
            'MODERATE': 'MODERATE',
            'LOW': 'LOW'
        }
        
        return mapping.get(conf, 'MODERATE')
    
    def create_slug(self, name: str, site_id: str) -> str:
        """Crear slug único"""
        import re
        
        # Limpiar nombre
        slug = name.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = slug[:200]  # Limitar longitud
        
        # Agregar ID para unicidad
        if site_id:
            slug = f"{slug}-{site_id}"[:255]
        
        return slug or 'unknown-site'
    
    async def site_exists(self, latitude: float, longitude: float, name: str) -> bool:
        """Verificar si un sitio ya existe (por coordenadas cercanas)"""
        # Buscar sitios dentro de ~100m (0.001 grados)
        existing = await self.conn.fetchval('''
            SELECT id FROM archaeological_sites
            WHERE ABS(latitude - $1) < 0.001
            AND ABS(longitude - $2) < 0.001
            AND name = $3
            LIMIT 1
        ''', latitude, longitude, name)
        
        return existing is not None
    
    async def migrate_site(self, site: Dict[str, Any]) -> bool:
        """Migrar un sitio individual"""
        
        try:
            # Datos básicos
            name = site.get('name', 'Unknown Site')
            latitude = float(site.get('latitude', 0))
            longitude = float(site.get('longitude', 0))
            
            # Validar coordenadas
            if latitude == 0 and longitude == 0:
                self.stats['skipped'] += 1
                return False
            
            # Verificar si ya existe
            if await self.site_exists(latitude, longitude, name):
                self.stats['skipped'] += 1
                return False
            
            # Crear slug
            site_id = site.get('wikidata_id') or site.get('osm_id') or site.get('unesco_id', '')
            slug = self.create_slug(name, str(site_id))
            
            # Clasificación
            environment_type = self.infer_environment_type(site)
            site_type = self.infer_site_type(site)
            confidence_level = self.determine_confidence(site)
            
            # Ubicación
            country = site.get('country', 'Unknown')[:100]
            
            # Información temporal
            period = site.get('period', '')[:255] if site.get('period') else None
            
            # IDs externos
            unesco_id = site.get('unesco_id')
            
            # Descripción
            description = site.get('description', '')[:1000] if site.get('description') else None
            
            # URL
            url = site.get('url', '')
            
            # Metadatos
            is_reference = False  # Los sitios recopilados no son de referencia
            is_control = False
            
            # Insertar sitio
            site_uuid = await self.conn.fetchval('''
                INSERT INTO archaeological_sites (
                    name, slug,
                    "environmentType", "siteType", "confidenceLevel",
                    latitude, longitude,
                    country,
                    period,
                    "unescoId",
                    description,
                    "isReferencesite", "isControlSite"
                ) VALUES (
                    $1, $2,
                    $3, $4, $5,
                    $6, $7,
                    $8,
                    $9,
                    $10,
                    $11,
                    $12, $13
                ) RETURNING id
            ''',
                name, slug,
                environment_type, site_type, confidence_level,
                latitude, longitude,
                country,
                period,
                unesco_id,
                description,
                is_reference, is_control
            )
            
            # Agregar fuente de datos
            source = site.get('source', 'Unknown')
            await self.conn.execute('''
                INSERT INTO data_sources ("siteId", "sourceType", "sourceName", "sourceUrl")
                VALUES ($1, $2, $3, $4)
            ''', site_uuid, 'harvested', source, url)
            
            self.stats['inserted'] += 1
            return True
            
        except Exception as e:
            self.stats['errors'] += 1
            if self.stats['errors'] <= 10:  # Solo mostrar primeros 10 errores
                print(f"   Error en sitio '{site.get('name', 'unknown')}': {e}")
            return False
    
    async def migrate_all(self, batch_size: int = 1000):
        """Migrar todos los sitios"""
        
        print("\n" + "="*80)
        print("INICIANDO MIGRACION DE SITIOS RECOPILADOS")
        print("="*80)
        
        # Conectar
        await self.connect()
        
        # Cargar datos
        data = self.load_harvested_data()
        sites = data.get('sites', [])
        self.stats['total'] = len(sites)
        
        print(f"\nMigrando {self.stats['total']:,} sitios...")
        print(f"   (Procesando en lotes de {batch_size})")
        
        # Migrar en lotes
        for i in range(0, len(sites), batch_size):
            batch = sites[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(sites) + batch_size - 1) // batch_size
            
            print(f"\nLote {batch_num}/{total_batches} ({i+1}-{min(i+batch_size, len(sites))})...")
            
            for site in batch:
                await self.migrate_site(site)
            
            # Progreso
            progress = (i + len(batch)) / len(sites) * 100
            print(f"   Insertados: {self.stats['inserted']:,}")
            print(f"   Omitidos: {self.stats['skipped']:,}")
            print(f"   Errores: {self.stats['errors']:,}")
            print(f"   Progreso: {progress:.1f}%")
        
        # Resumen final
        print("\n" + "="*80)
        print("RESUMEN DE MIGRACION")
        print("="*80)
        
        total_db = await self.conn.fetchval('SELECT COUNT(*) FROM archaeological_sites')
        harvested_count = await self.conn.fetchval('''
            SELECT COUNT(DISTINCT s.id)
            FROM archaeological_sites s
            JOIN data_sources ds ON ds."siteId" = s.id
            WHERE ds."sourceType" = 'harvested'
        ''')
        
        print(f"Total en base de datos: {total_db:,}")
        print(f"Sitios recopilados insertados: {harvested_count:,}")
        print(f"Sitios omitidos (duplicados): {self.stats['skipped']:,}")
        print(f"Errores: {self.stats['errors']:,}")
        
        # Desconectar
        await self.disconnect()

async def main():
    print("ArcheoScope - Migracion de Sitios Recopilados")
    print("harvested_complete.json -> PostgreSQL")
    print("")
    
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL no configurada")
        print("\nConfigura DATABASE_URL en .env")
        return 1
    
    print(f"DATABASE_URL configurada")
    
    migrator = HarvestedSitesMigrator(DATABASE_URL)
    
    try:
        await migrator.migrate_all(batch_size=1000)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
