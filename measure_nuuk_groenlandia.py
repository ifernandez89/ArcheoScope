#!/usr/bin/env python3
"""
Medición instrumental - Nuuk, Groenlandia
Candidato 1: Márgenes glaciares retraídos
"""

import sys
import asyncio
import asyncpg
from pathlib import Path
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def measure_nuuk():
    from satellite_connectors.real_data_integrator import RealDataIntegrator
    
    # Coordenadas: Suroeste de Groenlandia - costa de Nuuk
    center_lat = 64.2
    center_lon = -51.7
    
    # Bbox de ~10km x 10km
    lat_min = center_lat - 0.05
    lat_max = center_lat + 0.05
    lon_min = center_lon - 0.05
    lon_max = center_lon + 0.05
    
    region_name = "Nuuk SW Groenlandia - Margen Glaciar"
    
    print("="*80)
    print("MEDICION INSTRUMENTAL - CANDIDATO 1")
    print("="*80)
    print(f"Region: {region_name}")
    print(f"Centro: {center_lat:.4f}N, {center_lon:.4f}W")
    print(f"Bbox: [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
    print(f"Objetivo: Terrazas costeras, alineamientos, estructuras liticas")
    print("="*80)
    
    integrator = RealDataIntegrator()
    
    # Instrumentos a medir (todos los disponibles)
    instrumentos = [
        ("icesat2", "ICESat-2 Elevacion"),
        ("sentinel_1_sar", "Sentinel-1 SAR"),
        ("sentinel_2_ndvi", "Sentinel-2 NDVI"),
        ("landsat_thermal", "Landsat Thermal"),
        ("modis_lst", "MODIS LST"),
        ("opentopography", "OpenTopography DEM"),
        ("nsidc_sea_ice", "NSIDC Sea Ice"),
    ]
    
    mediciones = []
    
    for inst_name, inst_label in instrumentos:
        print(f"\n[{inst_label}]")
        
        try:
            result = await integrator.get_instrument_measurement(
                instrument_name=inst_name,
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max
            )
            
            if result:
                status = result.get('status', 'UNKNOWN')
                value = result.get('value')
                confidence = result.get('confidence', 0.0)
                source = result.get('source', 'Unknown')
                
                print(f"  Status: {status}")
                print(f"  Valor: {value}")
                print(f"  Confidence: {confidence}")
                print(f"  Fuente: {source}")
                
                mediciones.append({
                    'instrument': inst_name,
                    'label': inst_label,
                    'status': status,
                    'value': value,
                    'confidence': confidence,
                    'source': source,
                    'usable': status in ['OK', 'DERIVED']
                })
            else:
                print(f"  [NO DATA]")
                mediciones.append({
                    'instrument': inst_name,
                    'label': inst_label,
                    'status': 'NO_DATA',
                    'value': None,
                    'confidence': 0.0,
                    'source': None,
                    'usable': False
                })
                
        except Exception as e:
            print(f"  [ERROR] {e}")
            mediciones.append({
                'instrument': inst_name,
                'label': inst_label,
                'status': 'ERROR',
                'value': None,
                'confidence': 0.0,
                'source': None,
                'usable': False
            })
    
    # Guardar en BD
    print("\n" + "="*80)
    print("GUARDANDO EN BASE DE DATOS")
    print("="*80)
    
    conn = await asyncpg.connect(
        host='localhost',
        port=5433,
        user='postgres',
        password='1464',
        database='archeoscope_db'
    )
    
    # Generar analysis_id UUID
    import uuid
    analysis_id = str(uuid.uuid4())
    
    # Insertar cada medición (TODAS, incluyendo NO_DATA y ERROR)
    for med in mediciones:
        await conn.execute("""
            INSERT INTO measurements (
                measurement_timestamp,
                analysis_id,
                latitude,
                longitude,
                lat_min,
                lat_max,
                lon_min,
                lon_max,
                region_name,
                instrument_name,
                measurement_type,
                value,
                unit,
                confidence,
                source,
                data_mode
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
        """,
            datetime.now(),
            analysis_id,
            center_lat,
            center_lon,
            lat_min,
            lat_max,
            lon_min,
            lon_max,
            region_name,
            med['instrument'],
            med['label'],
            float(med['value']) if med['value'] is not None else 0.0,
            'various',
            med['confidence'],
            med['source'] if med['source'] else 'N/A',
            med['status']
        )
        status_icon = "[OK]" if med['usable'] else "[--]"
        print(f"  {status_icon} {med['label']} guardado ({med['status']})")
    
    # Verificar
    count = await conn.fetchval(
        'SELECT COUNT(*) FROM measurements WHERE analysis_id = $1',
        analysis_id
    )
    
    await conn.close()
    
    print(f"\n[OK] {count} mediciones guardadas en BD")
    print(f"Analysis ID: {analysis_id}")
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN")
    print("="*80)
    usables = sum(1 for m in mediciones if m['usable'])
    print(f"Instrumentos usables: {usables}/{len(mediciones)}")
    
    for med in mediciones:
        if med['usable']:
            print(f"  [OK] {med['label']}: {med['status']}")
        else:
            print(f"  [--] {med['label']}: {med['status']}")
    
    print("="*80)

asyncio.run(measure_nuuk())
