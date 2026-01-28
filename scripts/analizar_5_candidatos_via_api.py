#!/usr/bin/env python3
"""
Análisis completo de los 5 candidatos arqueológicos usando el backend API.
Guarda resultados en BD.
"""

import asyncio
import asyncpg
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8002"

async def analizar_candidatos():
    """Analizar los 5 candidatos guardados en BD usando el API."""
    
    # Conectar a BD
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    print("="*80, flush=True)
    print("ANÁLISIS COMPLETO DE 5 CANDIDATOS ARQUEOLÓGICOS", flush=True)
    print("="*80, flush=True)
    
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
    
    print(f"\nEncontrados {len(candidatos)} candidatos en BD", flush=True)
    print(f"Iniciando análisis con ArcheoScope API...\n", flush=True)
    
    resultados = []
    
    for idx, candidato in enumerate(candidatos, 1):
        analysis_id = candidato['analysis_id']
        region_name = candidato['region_name']
        lat = float(candidato['latitude'])
        lon = float(candidato['longitude'])
        
        print(f"\n{'='*80}", flush=True)
        print(f"CANDIDATO {idx}/5: {region_name}", flush=True)
        print(f"{'='*80}", flush=True)
        print(f"Coordenadas: {lat:.4f}, {lon:.4f}", flush=True)
        print(f"Analysis ID: {analysis_id}", flush=True)
        
        # Definir bounds (±0.05 grados ~ 5km)
        lat_min = lat - 0.05
        lat_max = lat + 0.05
        lon_min = lon - 0.05
        lon_max = lon + 0.05
        
        try:
            # Ejecutar análisis vía API
            print(f"\n[ANALISIS] Ejecutando análisis vía API...", flush=True)
            
            payload = {
                "lat_min": lat_min,
                "lat_max": lat_max,
                "lon_min": lon_min,
                "lon_max": lon_max,
                "region_name": region_name,
                "resolution_m": 1000
            }
            
            response = requests.post(
                f"{API_BASE}/analyze",
                json=payload,
                timeout=120
            )
            
            if response.status_code != 200:
                print(f"[ERROR] Error en API: {response.status_code}", flush=True)
                print(f"   Response: {response.text[:200]}", flush=True)
                continue
            
            resultado = response.json()
            
            # Extraer información clave
            region_info = resultado.get('region_info', {})
            statistical = resultado.get('statistical_results', {})
            physics = resultado.get('physics_results', {})
            ai_explanations = resultado.get('ai_explanations', {})
            
            # Calcular probabilidad arqueológica
            archaeological_probability = statistical.get('archaeological_probability', 0.0)
            confidence_level = statistical.get('confidence_level', 'unknown')
            environment_type = region_info.get('environment_type', 'unknown')
            
            # Contar instrumentos convergentes
            instruments_converging = 0
            if 'measurements' in statistical:
                instruments_converging = sum(
                    1 for m in statistical['measurements'] 
                    if m.get('exceeds_threshold', False)
                )
            
            # Sitio conocido cercano
            known_site_nearby = statistical.get('known_site_nearby', False)
            known_site_name = statistical.get('known_site_name', None)
            distance_to_known_site = statistical.get('distance_to_known_site', None)
            
            # Mostrar resultados
            print(f"\n[RESULTADOS] RESULTADOS DEL ANÁLISIS:", flush=True)
            print(f"   Probabilidad arqueológica: {archaeological_probability:.3f}", flush=True)
            print(f"   Tipo de ambiente: {environment_type}", flush=True)
            print(f"   Instrumentos convergentes: {instruments_converging}", flush=True)
            print(f"   Nivel de confianza: {confidence_level}", flush=True)
            
            if known_site_nearby:
                print(f"   [WARNING] Sitio conocido cercano: {known_site_name}", flush=True)
                if distance_to_known_site:
                    print(f"      Distancia: {distance_to_known_site:.2f} km", flush=True)
            
            # Mostrar mediciones si están disponibles
            if 'measurements' in statistical:
                print(f"\n[MEDICIONES] MEDICIONES INSTRUMENTALES ({len(statistical['measurements'])}):", flush=True)
                for m in statistical['measurements']:
                    status = "[OK]" if m.get('exceeds_threshold', False) else "[OK]"
                    print(f"   {status} {m.get('instrument_name', 'unknown')}: {m.get('value', 0):.3f} (threshold: {m.get('threshold', 0):.3f})", flush=True)
            
            # Determinar si es anomalía
            es_anomalia = archaeological_probability >= 0.5
            
            if es_anomalia:
                print(f"\n[ANOMALIA] ANOMALÍA DETECTADA", flush=True)
                print(f"   Score: {archaeological_probability:.3f}", flush=True)
                print(f"   Recomendación: Investigación adicional requerida", flush=True)
            else:
                print(f"\n[OK] NO ES ANOMALÍA", flush=True)
                print(f"   Score: {archaeological_probability:.3f}", flush=True)
                print(f"   Recomendación: Consistente con procesos naturales", flush=True)
            
            # Guardar en BD
            print(f"\n[GUARDANDO] Guardando resultados en BD...", flush=True)
            
            # Preparar metadata
            analysis_metadata = {
                'region_name': region_name,
                'bounds': {
                    'lat_min': lat_min, 'lat_max': lat_max,
                    'lon_min': lon_min, 'lon_max': lon_max
                },
                'known_site_nearby': known_site_nearby,
                'known_site_name': known_site_name,
                'distance_to_known_site': distance_to_known_site,
                'ai_available': ai_explanations.get('ai_available', False),
                'timestamp': datetime.now().isoformat(),
                'environment_type': environment_type,
                'confidence_level': confidence_level
            }
            
            # 1. Guardar/actualizar candidato
            candidate_id = await conn.fetchval("""
                INSERT INTO archaeological_candidates 
                (center_lat, center_lon, zone_id, multi_instrumental_score, 
                 convergence_count, status, analysis_results)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (center_lat, center_lon) 
                DO UPDATE SET
                    multi_instrumental_score = EXCLUDED.multi_instrumental_score,
                    convergence_count = EXCLUDED.convergence_count,
                    status = EXCLUDED.status,
                    analysis_results = EXCLUDED.analysis_results,
                    updated_at = NOW()
                RETURNING id
            """, lat, lon, region_name, archaeological_probability,
                instruments_converging, 
                'anomaly' if es_anomalia else 'normal',
                analysis_metadata)
            
            print(f"   [OK] Candidato guardado (ID: {candidate_id})", flush=True)
            
            # 2. Guardar análisis detallado
            analysis_record_id = await conn.fetchval("""
                INSERT INTO archaeological_candidate_analyses
                (candidate_id, analysis_id, archaeological_probability,
                 environment_type, confidence_level, instruments_converging,
                 analysis_metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id
            """, candidate_id, str(analysis_id), archaeological_probability,
                environment_type, confidence_level,
                instruments_converging, analysis_metadata)
            
            print(f"   [OK] Análisis guardado (ID: {analysis_record_id})", flush=True)
            
            # Guardar resultado para resumen
            resultados.append({
                'idx': idx,
                'region_name': region_name,
                'lat': lat,
                'lon': lon,
                'probability': archaeological_probability,
                'es_anomalia': es_anomalia,
                'instruments': instruments_converging,
                'confidence': confidence_level,
                'candidate_id': candidate_id,
                'environment': environment_type
            })
            
        except requests.exceptions.Timeout:
            print(f"\n[ERROR] TIMEOUT en análisis (>120s)", flush=True)
            continue
        except Exception as e:
            print(f"\n[ERROR] ERROR en análisis: {e}", flush=True)
            import traceback
            traceback.print_exc()
            continue
    
    # RESUMEN FINAL
    print(f"\n\n{'='*80}", flush=True)
    print("RESUMEN FINAL DE ANÁLISIS", flush=True)
    print(f"{'='*80}\n", flush=True)
    
    anomalias = [r for r in resultados if r['es_anomalia']]
    no_anomalias = [r for r in resultados if not r['es_anomalia']]
    
    print(f"Total candidatos analizados: {len(resultados)}", flush=True)
    print(f"Anomalías detectadas: {len(anomalias)}", flush=True)
    print(f"No anomalías: {len(no_anomalias)}", flush=True)
    
    if anomalias:
        print(f"\n[ANOMALIA] ANOMALÍAS DETECTADAS:", flush=True)
        for r in anomalias:
            print(f"   {r['idx']}. {r['region_name']}", flush=True)
            print(f"      Score: {r['probability']:.3f}", flush=True)
            print(f"      Ambiente: {r['environment']}", flush=True)
            print(f"      Instrumentos: {r['instruments']}", flush=True)
            print(f"      Confianza: {r['confidence']}", flush=True)
            print(f"      Candidate ID: {r['candidate_id']}", flush=True)
    
    if no_anomalias:
        print(f"\n[OK] NO ANOMALÍAS:", flush=True)
        for r in no_anomalias:
            print(f"   {r['idx']}. {r['region_name']}", flush=True)
            print(f"      Score: {r['probability']:.3f}", flush=True)
            print(f"      Ambiente: {r['environment']}", flush=True)
            print(f"      Instrumentos: {r['instruments']}", flush=True)
    
    # Estadísticas de BD
    print(f"\n{'='*80}", flush=True)
    print("ESTADÍSTICAS DE BASE DE DATOS", flush=True)
    print(f"{'='*80}", flush=True)
    
    total_candidates = await conn.fetchval('SELECT COUNT(*) FROM archaeological_candidates')
    total_analyses = await conn.fetchval('SELECT COUNT(*) FROM archaeological_candidate_analyses')
    total_measurements = await conn.fetchval('SELECT COUNT(*) FROM measurements')
    
    print(f"Candidatos en BD: {total_candidates}", flush=True)
    print(f"Análisis en BD: {total_analyses}", flush=True)
    print(f"Mediciones en BD: {total_measurements}", flush=True)
    
    await conn.close()
    
    print(f"\n[OK] Análisis completo finalizado", flush=True)
    print(f"{'='*80}\n", flush=True)

if __name__ == "__main__":
    asyncio.run(analizar_candidatos())
