#!/usr/bin/env python3
"""
Análisis completo de los 5 candidatos arqueológicos con detección de anomalías.
Guarda resultados en BD.
"""

import asyncio
import asyncpg
import sys
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from backend.core_anomaly_detector import CoreAnomalyDetector
from backend.satellite_connectors.real_data_integrator import RealDataIntegrator
from backend.environment_classifier import EnvironmentClassifier

async def analizar_candidatos():
    """Analizar los 5 candidatos guardados en BD."""
    
    # Conectar a BD
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    print("="*80)
    print("ANÁLISIS COMPLETO DE 5 CANDIDATOS ARQUEOLÓGICOS")
    print("="*80)
    
    # Obtener candidatos únicos de las mediciones
    candidatos = await conn.fetch("""
        SELECT DISTINCT 
            analysis_id,
            region_name,
            latitude,
            longitude,
            MIN(measurement_timestamp) as timestamp
        FROM measurements
        GROUP BY analysis_id, region_name, latitude, longitude
        ORDER BY MIN(measurement_timestamp)
    """)
    
    print(f"\nEncontrados {len(candidatos)} candidatos en BD")
    print(f"Iniciando análisis con CoreAnomalyDetector...\n")
    
    # Inicializar componentes
    integrator = RealDataIntegrator()
    classifier = EnvironmentClassifier()
    detector = CoreAnomalyDetector(integrator, classifier)
    
    resultados = []
    
    for idx, candidato in enumerate(candidatos, 1):
        analysis_id = candidato['analysis_id']
        region_name = candidato['region_name']
        lat = candidato['latitude']
        lon = candidato['longitude']
        
        print(f"\n{'='*80}")
        print(f"CANDIDATO {idx}/5: {region_name}")
        print(f"{'='*80}")
        print(f"Coordenadas: {lat:.4f}, {lon:.4f}")
        print(f"Analysis ID: {analysis_id}")
        
        # Definir bounds (±0.05 grados ~ 5km)
        lat_min = lat - 0.05
        lat_max = lat + 0.05
        lon_min = lon - 0.05
        lon_max = lon + 0.05
        
        try:
            # Ejecutar análisis completo
            print(f"\n🔍 Ejecutando análisis de anomalías...")
            
            resultado = await detector.detect_anomaly(
                lat=lat,
                lon=lon,
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                region_name=region_name
            )
            
            # Mostrar resultados
            print(f"\n📊 RESULTADOS DEL ANÁLISIS:")
            print(f"   Probabilidad arqueológica: {resultado.archaeological_probability:.3f}")
            print(f"   Tipo de ambiente: {resultado.environment_type}")
            print(f"   Confianza ambiente: {resultado.environment_confidence:.2f}")
            print(f"   Instrumentos convergentes: {resultado.instruments_converging}")
            print(f"   Nivel de confianza: {resultado.confidence_level}")
            
            if resultado.known_site_nearby:
                print(f"   ⚠️ Sitio conocido cercano: {resultado.known_site_name}")
                print(f"      Distancia: {resultado.distance_to_known_site:.2f} km")
            
            # Mostrar mediciones
            print(f"\n📡 MEDICIONES INSTRUMENTALES ({len(resultado.measurements)}):")
            for m in resultado.measurements:
                status = "✅" if m.exceeds_threshold else "⚪"
                print(f"   {status} {m.instrument_name}: {m.value:.3f} (threshold: {m.threshold:.3f}, conf: {m.confidence})")
            
            # Determinar si es anomalía
            es_anomalia = resultado.archaeological_probability >= 0.5
            
            if es_anomalia:
                print(f"\n🎯 ANOMALÍA DETECTADA")
                print(f"   Score: {resultado.archaeological_probability:.3f}")
                print(f"   Recomendación: Investigación adicional requerida")
            else:
                print(f"\n⚪ NO ES ANOMALÍA")
                print(f"   Score: {resultado.archaeological_probability:.3f}")
                print(f"   Recomendación: Consistente con procesos naturales")
            
            # Guardar en BD
            print(f"\n💾 Guardando resultados en BD...")
            
            # 1. Guardar/actualizar candidato
            candidate_id = await conn.fetchval("""
                INSERT INTO archaeological_candidates 
                (latitude, longitude, region_name, archaeological_probability, 
                 environment_type, confidence_level, instruments_converging,
                 known_site_nearby, known_site_name, distance_to_known_site)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ON CONFLICT (latitude, longitude) 
                DO UPDATE SET
                    archaeological_probability = EXCLUDED.archaeological_probability,
                    environment_type = EXCLUDED.environment_type,
                    confidence_level = EXCLUDED.confidence_level,
                    instruments_converging = EXCLUDED.instruments_converging,
                    known_site_nearby = EXCLUDED.known_site_nearby,
                    known_site_name = EXCLUDED.known_site_name,
                    distance_to_known_site = EXCLUDED.distance_to_known_site,
                    updated_at = NOW()
                RETURNING id
            """, lat, lon, region_name, resultado.archaeological_probability,
                resultado.environment_type, resultado.confidence_level,
                resultado.instruments_converging, resultado.known_site_nearby,
                resultado.known_site_name, resultado.distance_to_known_site)
            
            print(f"   ✅ Candidato guardado (ID: {candidate_id})")
            
            # 2. Guardar análisis detallado
            analysis_record_id = await conn.fetchval("""
                INSERT INTO archaeological_candidate_analyses
                (candidate_id, analysis_id, archaeological_probability,
                 environment_type, confidence_level, instruments_converging,
                 analysis_metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id
            """, candidate_id, analysis_id, resultado.archaeological_probability,
                resultado.environment_type, resultado.confidence_level,
                resultado.instruments_converging, {
                    'region_name': region_name,
                    'bounds': {
                        'lat_min': lat_min, 'lat_max': lat_max,
                        'lon_min': lon_min, 'lon_max': lon_max
                    },
                    'known_site_nearby': resultado.known_site_nearby,
                    'known_site_name': resultado.known_site_name,
                    'distance_to_known_site': resultado.distance_to_known_site
                })
            
            print(f"   ✅ Análisis guardado (ID: {analysis_record_id})")
            
            # Guardar resultado para resumen
            resultados.append({
                'idx': idx,
                'region_name': region_name,
                'lat': lat,
                'lon': lon,
                'probability': resultado.archaeological_probability,
                'es_anomalia': es_anomalia,
                'instruments': resultado.instruments_converging,
                'confidence': resultado.confidence_level,
                'candidate_id': candidate_id
            })
            
        except Exception as e:
            print(f"\n❌ ERROR en análisis: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # RESUMEN FINAL
    print(f"\n\n{'='*80}")
    print("RESUMEN FINAL DE ANÁLISIS")
    print(f"{'='*80}\n")
    
    anomalias = [r for r in resultados if r['es_anomalia']]
    no_anomalias = [r for r in resultados if not r['es_anomalia']]
    
    print(f"Total candidatos analizados: {len(resultados)}")
    print(f"Anomalías detectadas: {len(anomalias)}")
    print(f"No anomalías: {len(no_anomalias)}")
    
    if anomalias:
        print(f"\n🎯 ANOMALÍAS DETECTADAS:")
        for r in anomalias:
            print(f"   {r['idx']}. {r['region_name']}")
            print(f"      Score: {r['probability']:.3f}")
            print(f"      Instrumentos: {r['instruments']}")
            print(f"      Confianza: {r['confidence']}")
            print(f"      Candidate ID: {r['candidate_id']}")
    
    if no_anomalias:
        print(f"\n⚪ NO ANOMALÍAS:")
        for r in no_anomalias:
            print(f"   {r['idx']}. {r['region_name']}")
            print(f"      Score: {r['probability']:.3f}")
            print(f"      Instrumentos: {r['instruments']}")
    
    # Estadísticas de BD
    print(f"\n{'='*80}")
    print("ESTADÍSTICAS DE BASE DE DATOS")
    print(f"{'='*80}")
    
    total_candidates = await conn.fetchval('SELECT COUNT(*) FROM archaeological_candidates')
    total_analyses = await conn.fetchval('SELECT COUNT(*) FROM archaeological_candidate_analyses')
    total_measurements = await conn.fetchval('SELECT COUNT(*) FROM measurements')
    
    print(f"Candidatos en BD: {total_candidates}")
    print(f"Análisis en BD: {total_analyses}")
    print(f"Mediciones en BD: {total_measurements}")
    
    await conn.close()
    
    print(f"\n✅ Análisis completo finalizado")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(analizar_candidatos())
