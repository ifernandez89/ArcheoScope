#!/usr/bin/env python3
"""
Script de Migración: JSON → PostgreSQL
======================================

Migra los datos de archaeological_sites_database.json a PostgreSQL.
"""

import json
import asyncio
import asyncpg
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL no configurada en .env")
    print("   Copia .env.example a .env y configura tu DATABASE_URL")
    exit(1)

class JSONToPostgresMigrator:
    """Migrador de JSON a PostgreSQL"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.conn = None
        
    async def connect(self):
        """Conectar a PostgreSQL"""
        print("🔌 Conectando a PostgreSQL...")
        self.conn = await asyncpg.connect(self.database_url)
        print("✅ Conectado exitosamente")
        
    async def disconnect(self):
        """Desconectar de PostgreSQL"""
        if self.conn:
            await self.conn.close()
            print("🔌 Desconectado de PostgreSQL")
    
    async def clear_existing_data(self):
        """Limpiar datos existentes (opcional)"""
        print("\n🗑️  Limpiando datos existentes...")
        
        # Eliminar en orden inverso por dependencias
        tables = [
            'research_questions',
            'site_threats',
            'site_data_availability',
            'data_sources',
            'archaeological_features',
            'calibration_data',
            'detection_history',
            'archaeological_sites',
        ]
        
        for table in tables:
            await self.conn.execute(f'DELETE FROM {table}')
            print(f"   ✅ {table} limpiado")
    
    def load_json_data(self) -> Dict[str, Any]:
        """Cargar datos del JSON"""
        print("\n📂 Cargando datos del JSON...")
        
        json_path = Path(__file__).parent.parent / "data" / "archaeological_sites_database.json"
        
        if not json_path.exists():
            raise FileNotFoundError(f"No se encontró: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ JSON cargado: {len(data.get('reference_sites', {}))} sitios de referencia")
        print(f"✅ JSON cargado: {len(data.get('control_sites', {}))} sitios de control")
        
        return data
    
    def map_environment_type(self, env_type: str) -> str:
        """Mapear tipo de ambiente del JSON al enum de PostgreSQL"""
        mapping = {
            'desert': 'DESERT',
            'forest': 'FOREST',
            'ice': 'GLACIER',
            'water': 'SHALLOW_SEA',
            'mountain': 'MOUNTAIN',
            'grassland': 'GRASSLAND',
            'polar_ice': 'POLAR_ICE',
            'glacier': 'GLACIER',
            'shallow_sea': 'SHALLOW_SEA',
        }
        return mapping.get(env_type.lower(), 'UNKNOWN')
    
    def map_site_type(self, site_type: str) -> str:
        """Mapear tipo de sitio del JSON al enum de PostgreSQL"""
        mapping = {
            'monumental_complex': 'MONUMENTAL_COMPLEX',
            'temple_complex': 'TEMPLE_COMPLEX',
            'mountain_citadel': 'MOUNTAIN_CITADEL',
            'rock_cut_city': 'ROCK_CUT_CITY',
            'megalithic_monument': 'MEGALITHIC_MONUMENT',
            'submerged_city': 'SUBMERGED_CITY',
            'glacier_mummy': 'GLACIER_MUMMY',
            'natural_control': 'NATURAL_CONTROL',
            'natural_desert_control': 'NATURAL_CONTROL',
            'natural_forest_control': 'NATURAL_CONTROL',
            'natural_ice_control': 'NATURAL_CONTROL',
            'natural_ocean_control': 'NATURAL_CONTROL',
        }
        return mapping.get(site_type.lower(), 'UNKNOWN')
    
    def map_confidence_level(self, confidence: str) -> str:
        """Mapear nivel de confianza"""
        mapping = {
            'confirmed': 'CONFIRMED',
            'high': 'HIGH',
            'moderate': 'MODERATE',
            'low': 'LOW',
            'negative_control': 'NEGATIVE_CONTROL',
        }
        return mapping.get(confidence.lower(), 'MODERATE')
    
    def map_excavation_status(self, status: str) -> str:
        """Mapear estado de excavación"""
        mapping = {
            'extensively_excavated': 'EXTENSIVELY_EXCAVATED',
            'ongoing_research': 'ONGOING_RESEARCH',
            'partially_excavated': 'PARTIALLY_EXCAVATED',
            'unexcavated': 'UNEXCAVATED',
            'fully_excavated': 'FULLY_EXCAVATED',
            'ongoing_underwater_excavation': 'ONGOING_UNDERWATER',
            'not_applicable': 'NOT_APPLICABLE',
        }
        return mapping.get(status.lower().replace(' ', '_'), 'UNEXCAVATED')
    
    def map_preservation_status(self, status: str) -> str:
        """Mapear estado de preservación"""
        mapping = {
            'excellent': 'EXCELLENT',
            'good': 'GOOD',
            'fair': 'FAIR',
            'poor': 'POOR',
            'deteriorating': 'DETERIORATING',
        }
        return mapping.get(status.lower(), 'UNKNOWN')
    
    async def migrate_site(self, site_id: str, site_data: Dict[str, Any], is_control: bool = False):
        """Migrar un sitio individual"""
        
        # Crear slug desde el site_id
        slug = site_id.replace('_', '-')
        
        # Datos básicos
        name = site_data.get('name', site_id)
        alternate_names = site_data.get('alternate_names', [])
        
        # Clasificación
        environment_type = self.map_environment_type(site_data.get('environment_type', 'unknown'))
        site_type = self.map_site_type(site_data.get('site_type', 'unknown'))
        confidence_level = self.map_confidence_level(site_data.get('confidence_level', 'moderate'))
        excavation_status = self.map_excavation_status(site_data.get('excavation_status', 'unexcavated'))
        preservation_status = self.map_preservation_status(site_data.get('preservation_status', 'unknown'))
        
        # Ubicación
        coords = site_data.get('coordinates', {})
        latitude = coords.get('lat', 0.0)
        longitude = coords.get('lon', 0.0)
        elevation = site_data.get('discovery_elevation_m') or site_data.get('water_depth_m')
        if elevation and 'water_depth_m' in site_data:
            elevation = -abs(elevation)  # Negativo para profundidad
        
        area_km2 = site_data.get('area_km2')
        country = site_data.get('country', 'Unknown')
        region = site_data.get('region')
        
        # Información temporal
        period = site_data.get('period')
        date_range = site_data.get('date_range', {})
        date_range_start = date_range.get('start')
        date_range_end = date_range.get('end')
        date_unit = date_range.get('unit', 'CE')
        
        # UNESCO
        unesco_id = site_data.get('unesco_id')
        unesco_status = site_data.get('unesco_status')
        unesco_year = site_data.get('unesco_year')
        
        # Descripción
        description = site_data.get('description')
        scientific_significance = site_data.get('scientific_significance')
        
        # Metadatos
        is_reference = not is_control
        is_control_site = is_control
        last_verified = datetime.fromisoformat(site_data.get('last_verified', '2026-01-25'))
        discovery_date = None
        if 'discovery_date' in site_data:
            discovery_date = datetime.fromisoformat(site_data['discovery_date'])
        
        # Insertar sitio
        site_uuid = await self.conn.fetchval('''
            INSERT INTO archaeological_sites (
                name, "alternateNames", slug,
                "environmentType", "siteType", "confidenceLevel",
                "excavationStatus", "preservationStatus",
                latitude, longitude, elevation, "areaKm2",
                country, region,
                period, "dateRangeStart", "dateRangeEnd", "dateUnit",
                "unescoId", "unescoStatus", "unescoYear",
                description, "scientificSignificance",
                "isReferencesite", "isControlSite",
                "lastVerified", "discoveryDate"
            ) VALUES (
                $1, $2, $3,
                $4, $5, $6,
                $7, $8,
                $9, $10, $11, $12,
                $13, $14,
                $15, $16, $17, $18,
                $19, $20, $21,
                $22, $23,
                $24, $25,
                $26, $27
            ) RETURNING id
        ''',
            name, alternate_names, slug,
            environment_type, site_type, confidence_level,
            excavation_status, preservation_status,
            latitude, longitude, elevation, area_km2,
            country, region,
            period, date_range_start, date_range_end, date_unit,
            unesco_id, unesco_status, unesco_year,
            description, scientific_significance,
            is_reference, is_control_site,
            last_verified, discovery_date
        )
        
        print(f"   ✅ {name} ({site_uuid})")
        
        # Migrar características (features)
        if 'archaeological_features' in site_data:
            for feature in site_data['archaeological_features']:
                await self.conn.execute('''
                    INSERT INTO archaeological_features ("siteId", name, "featureType")
                    VALUES ($1, $2, $3)
                ''', site_uuid, feature, 'feature')
        
        # Migrar fuentes de datos
        if 'data_sources' in site_data:
            sources = site_data['data_sources']
            for source_type, source_name in sources.items():
                source_url = site_data.get('public_urls', {}).get(source_type.replace('_source', ''))
                await self.conn.execute('''
                    INSERT INTO data_sources ("siteId", "sourceType", "sourceName", "sourceUrl")
                    VALUES ($1, $2, $3, $4)
                ''', site_uuid, source_type, source_name, source_url)
        
        # Migrar disponibilidad de datos
        if 'data_available' in site_data:
            data_avail = site_data['data_available']
            data_type_mapping = {
                'lidar': 'LIDAR',
                'satellite_multispectral': 'SATELLITE_MULTISPECTRAL',
                'satellite_thermal': 'SATELLITE_THERMAL',
                'sar': 'SAR',
                'photogrammetry': 'PHOTOGRAMMETRY',
                'ground_penetrating_radar': 'GROUND_PENETRATING_RADAR',
                'excavation_reports': 'EXCAVATION_REPORTS',
                '3d_models': 'MODELS_3D',
                'icesat2': 'ICESAT2',
                'multibeam_sonar': 'MULTIBEAM_SONAR',
                'side_scan_sonar': 'SIDE_SCAN_SONAR',
                'magnetometry': 'MAGNETOMETRY',
                'sub_bottom_profiler': 'SUB_BOTTOM_PROFILER',
            }
            
            for data_key, available in data_avail.items():
                if data_key in data_type_mapping:
                    await self.conn.execute('''
                        INSERT INTO site_data_availability ("siteId", "dataType", available)
                        VALUES ($1, $2, $3)
                    ''', site_uuid, data_type_mapping[data_key], available)
        
        # Migrar amenazas
        if 'threats' in site_data:
            for threat in site_data['threats']:
                await self.conn.execute('''
                    INSERT INTO site_threats ("siteId", "threatType", severity)
                    VALUES ($1, $2, $3)
                ''', site_uuid, threat, 'medium')
        
        # Migrar preguntas de investigación
        if 'research_questions' in site_data:
            for question in site_data['research_questions']:
                await self.conn.execute('''
                    INSERT INTO research_questions ("siteId", question, priority, status)
                    VALUES ($1, $2, $3, $4)
                ''', site_uuid, question, 'medium', 'open')
        
        # Migrar datos de calibración
        if 'calibration_notes' in site_data or site_id in ['giza_pyramids', 'angkor_wat', 'otzi_iceman', 'port_royal', 'machu_picchu', 'petra', 'stonehenge']:
            # Buscar firmas esperadas en metadata
            calibration_sites = site_data.get('expected_signatures', {})
            
            await self.conn.execute('''
                INSERT INTO calibration_data (
                    "siteId",
                    "thermalDeltaK",
                    "sarBackscatterDb",
                    "ndviDelta",
                    "lidarHeightM",
                    "elevationTerracingM",
                    "slopeDeltaDegrees",
                    "sarCoherence",
                    "bathymetricHeightM",
                    "acousticReflectance",
                    "magneticAnomalyNt",
                    "calibrationNotes",
                    "lastCalibrated",
                    "calibrationConfidence"
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14
                )
            ''',
                site_uuid,
                calibration_sites.get('thermal_delta_k'),
                calibration_sites.get('sar_backscatter_db'),
                calibration_sites.get('ndvi_delta'),
                calibration_sites.get('lidar_height_m'),
                calibration_sites.get('elevation_terracing_m'),
                calibration_sites.get('slope_delta_degrees'),
                calibration_sites.get('sar_coherence'),
                calibration_sites.get('bathymetric_height_m'),
                calibration_sites.get('acoustic_reflectance'),
                calibration_sites.get('magnetic_anomaly_nt'),
                site_data.get('calibration_notes', f'Migrated from JSON - {name}'),
                last_verified,
                0.90
            )
        
        return site_uuid
    
    async def migrate_all(self, clear_existing: bool = False):
        """Migrar todos los datos"""
        
        print("\n" + "="*80)
        print("🚀 INICIANDO MIGRACIÓN JSON → PostgreSQL")
        print("="*80)
        
        # Conectar
        await self.connect()
        
        # Limpiar datos existentes si se solicita
        if clear_existing:
            await self.clear_existing_data()
        
        # Cargar JSON
        data = self.load_json_data()
        
        # Migrar sitios de referencia
        print("\n🏛️  Migrando sitios de referencia...")
        reference_sites = data.get('reference_sites', {})
        for site_id, site_data in reference_sites.items():
            await self.migrate_site(site_id, site_data, is_control=False)
        
        # Migrar sitios de control
        print("\n🌿 Migrando sitios de control...")
        control_sites = data.get('control_sites', {})
        for site_id, site_data in control_sites.items():
            await self.migrate_site(site_id, site_data, is_control=True)
        
        # Resumen
        print("\n" + "="*80)
        print("📊 RESUMEN DE MIGRACIÓN")
        print("="*80)
        
        total_sites = await self.conn.fetchval('SELECT COUNT(*) FROM archaeological_sites')
        reference_count = await self.conn.fetchval('SELECT COUNT(*) FROM archaeological_sites WHERE "isReferencesite" = true')
        control_count = await self.conn.fetchval('SELECT COUNT(*) FROM archaeological_sites WHERE "isControlSite" = true')
        features_count = await self.conn.fetchval('SELECT COUNT(*) FROM archaeological_features')
        sources_count = await self.conn.fetchval('SELECT COUNT(*) FROM data_sources')
        
        print(f"✅ Total de sitios migrados: {total_sites}")
        print(f"   - Sitios de referencia: {reference_count}")
        print(f"   - Sitios de control: {control_count}")
        print(f"✅ Características migradas: {features_count}")
        print(f"✅ Fuentes de datos migradas: {sources_count}")
        
        # Desconectar
        await self.disconnect()
        
        print("\n✅ ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
        print("="*80)

async def main():
    """Función principal"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ArcheoScope - Migración JSON → PostgreSQL                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar DATABASE_URL
    if not DATABASE_URL:
        print("❌ ERROR: DATABASE_URL no configurada")
        print("\n📝 Pasos para configurar:")
        print("   1. Copia .env.example a .env")
        print("   2. Configura DATABASE_URL con tu conexión PostgreSQL")
        print("   3. Ejecuta: npm run prisma:migrate")
        print("   4. Ejecuta este script nuevamente")
        return
    
    print(f"🔗 DATABASE_URL configurada")
    print(f"   Host: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'local'}")
    
    # Confirmar migración
    print("\n⚠️  ADVERTENCIA: Este script migrará datos del JSON a PostgreSQL")
    print("   ¿Deseas limpiar datos existentes antes de migrar? (s/n): ", end='')
    
    # Para automatización, asumir 'n' (no limpiar)
    clear_existing = False
    
    # Crear migrador
    migrator = JSONToPostgresMigrator(DATABASE_URL)
    
    try:
        # Ejecutar migración
        await migrator.migrate_all(clear_existing=clear_existing)
        
    except Exception as e:
        print(f"\n❌ ERROR durante la migración: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
