#!/usr/bin/env python3
"""
Test de 4 zonas + guardado en BD (Data Adapted)
"""
import sys
import os
import asyncio
import importlib.util
import uuid

# Agregar root al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 🔧 IMPORTAR ArcheoScopeDB DESDE ARCHIVO DIRECTAMENTE
db_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "database.py")
spec = importlib.util.spec_from_file_location("full_database_module", db_file_path)
db_module = importlib.util.module_from_spec(spec)
sys.modules["full_database_module"] = db_module
spec.loader.exec_module(db_module)

ArcheoScopeDB = db_module.ArcheoScopeDB

from backend.geoglyph_detector import GeoglyphDetector, DetectionMode
import numpy as np
import json
from datetime import datetime

async def test_4_zonas_con_bd():
    """Testear 4 zonas y guardar en BD con estructura adaptada"""
    
    zonas = [
        {
            'nombre': 'Harrat Khaybar',
            'lat': 25.0,
            'lon': 39.9,
            'region': 'Arabia Central',
            'descripcion': 'Campo volcánico con estructuras reportadas'
        },
        {
            'nombre': 'Sur Harrat Uwayrid',
            'lat': 26.5,
            'lon': 38.5,
            'region': 'Arabia Central',
            'descripcion': 'Basalto antiguo, baja intervención moderna'
        },
        {
            'nombre': 'Límite Arabia-Jordania',
            'lat': 29.5,
            'lon': 37.5,
            'region': 'Arabia Norte',
            'descripcion': 'Paleorutas, ausencia de papers'
        },
        {
            'nombre': 'Interior Rub al Khali',
            'lat': 20.5,
            'lon': 51.0,
            'region': 'Arabia Sur',
            'descripcion': 'Bordes del desierto vacío'
        }
    ]
    
    resultados = []
    db = ArcheoScopeDB()
    
    print("\n" + "="*90)
    print("🔍 TEST 4 ZONAS + GUARDADO EN BD (ADAPTADO)")
    print("="*90)
    
    try:
        await db.connect()
        print("✅ Conexión a BD establecida")
        
        for i, zona in enumerate(zonas, 1):
            print(f"\n{'─'*90}")
            print(f"[{i}/4] 📍 {zona['nombre']}")
            
            # Inicializar detector
            detector = GeoglyphDetector(mode=DetectionMode.EXPLORER)
            
            # Definir bbox
            lat_min = zona['lat'] - 0.05
            lat_max = zona['lat'] + 0.05
            lon_min = zona['lon'] - 0.05
            lon_max = zona['lon'] + 0.05
            
            # DEM simulado
            dem_data = np.random.rand(100, 100) * 100
            
            # DETECTAR
            result = detector.detect_geoglyph(
                lat=zona['lat'],
                lon=zona['lon'],
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                dem_data=dem_data,
                resolution_m=1.0
            )
            
            print(f"✅ Detectado: {result.geoglyph_type.value.upper()} (Score: {result.cultural_score:.2%})")
            
            # ADAPTAR DATOS PARA DB.save_candidate
            generated_id = f"GEO_{uuid.uuid4().hex[:8]}"
            
            # Datos específicos de geoglifos van en 'signals'
            geoglyph_signals = {
                'type': 'geoglyph_detection',
                'geoglyph_type': result.geoglyph_type.value,
                'geoglyph_type_confidence': result.type_confidence,
                'orientation': {
                    'azimuth': result.orientation.azimuth_deg,
                    'is_nw_se': result.orientation.is_nw_se,
                    'aspect_ratio': result.orientation.aspect_ratio,
                    'symmetry_error': result.orientation.bilateral_symmetry,
                    'functional_asymmetry': result.orientation.functional_asymmetry,
                    'tail_slope_deviation': result.orientation.tail_slope_deviation,
                    'distal_erosion_ratio': result.orientation.distal_erosion_ratio,
                    'axis_offset_m': result.orientation.axis_offset_m
                },
                'context': {
                    'volcanic': {
                        'stable_surface': result.volcanic_context.on_stable_surface if result.volcanic_context else None,
                        'young_flow': result.volcanic_context.on_young_flow if result.volcanic_context else None
                    },
                    'hydrology': {
                        'sediment_transition': result.paleo_hydrology.on_sediment_transition if result.paleo_hydrology else None,
                        'dist_wadi_km': result.paleo_hydrology.distance_to_wadi_km if result.paleo_hydrology else None
                    }
                },
                'notes': zona['descripcion']
            }
            
            db_candidate_data = {
                'candidate_id': generated_id,
                'zone_id': f"ZONE_{zona['region'].replace(' ', '_').upper()}",
                'location': {
                    'lat': zona['lat'],
                    'lon': zona['lon'],
                    'area_km2': 0.1 # Aprox 300x300m
                },
                'multi_instrumental_score': result.cultural_score,
                'convergence': {
                    'count': 1, # Solo geoglifo por ahora
                    'ratio': result.cultural_score
                },
                'recommended_action': 'field_validation',
                'temporal_persistence': {
                    'detected': True,
                    'years': 2000 # Antigüedad estimada
                },
                'signals': geoglyph_signals,
                'strategy': 'GEOGLYPH_EXPLORER_V2',
                'region_bounds': {
                    'lat_min': lat_min, 'lat_max': lat_max,
                    'lon_min': lon_min, 'lon_max': lon_max
                }
            }
            
            # 💾 GUARDAR EN BASE DE DATOS
            try:
                db_id = await db.save_candidate(db_candidate_data)
                print(f"💾 GUARDADO EN BD EXITOSAMENTE -> DB_ID: {db_id} (Ref: {generated_id})")
                
                zona['db_id'] = db_id
                resultados.append(zona)
                
            except Exception as e:
                print(f"⚠️  ERROR AL GUARDAR EN BD: {str(e)}")
        
        return resultados
        
    finally:
        await db.close()
        print("\n🔒 Conexión a BD cerrada")


if __name__ == "__main__":
    try:
        resultados = asyncio.run(test_4_zonas_con_bd())
        print(f"\n✅ Proceso finalizado. {len(resultados)} geoglifos guardados.")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
