#!/usr/bin/env python3
"""
Re-analizar los 2 primeros candidatos con enriquecimiento de BD.

IMPORTANTE:
- PISA los análisis anteriores en archaeological_candidate_analyses
- PISA los candidatos en archaeological_candidates
- NO borra las mediciones instrumentales (measurements)
- Usa FASE 0 para enriquecer con datos históricos
- Usa FASE F para validar contra sitios conocidos
"""

import asyncio
import asyncpg
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8002"

async def reanalyze_candidates():
    """Re-analizar candidatos con enriquecimiento."""
    
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    print("="*80, flush=True)
    print("RE-ANÁLISIS DE CANDIDATOS CON ENRIQUECIMIENTO DE BD", flush=True)
    print("="*80, flush=True)
    
    # Obtener los 2 primeros candidatos
    candidatos = await conn.fetch("""
        SELECT 
            analysis_id,
            region_name,
            latitude,
            longitude,
            measurement_timestamp
        FROM measurements
        ORDER BY measurement_timestamp
        LIMIT 2
    """)
    
    if len(candidatos) < 2:
        print(f"\nSolo hay {len(candidatos)} candidatos en BD", flush=True)
        await conn.close()
        return
    
    print(f"\nEncontrados {len(candidatos)} candidatos para re-analizar", flush=True)
    
    for idx, candidato in enumerate(candidatos, 1):
        analysis_id = candidato['analysis_id']
        region_name = candidato['region_name']
        lat = float(candidato['latitude'])
        lon = float(candidato['longitude'])
        
        print(f"\n{'='*80}", flush=True)
        print(f"CANDIDATO {idx}/2: {region_name}", flush=True)
        print(f"{'='*80}", flush=True)
        print(f"Coordenadas: {lat:.4f}, {lon:.4f}", flush=True)
        print(f"Analysis ID: {analysis_id}", flush=True)
        
        lat_min = lat - 0.05
        lat_max = lat + 0.05
        lon_min = lon - 0.05
        lon_max = lon + 0.05
        
        try:
            print(f"\n[ANALISIS] Ejecutando pipeline con enriquecimiento...", flush=True)
            
            payload = {
                "lat_min": lat_min,
                "lat_max": lat_max,
                "lon_min": lon_min,
                "lon_max": lon_max,
                "region_name": region_name,
                "candidate_id": str(analysis_id)
            }
            
            response = requests.post(
                f"{API_BASE}/analyze-scientific",
                json=payload,
                timeout=180
            )
            
            if response.status_code != 200:
                print(f"[ERROR] Error en API: {response.status_code}", flush=True)
                print(f"Response: {response.text[:500]}", flush=True)
                continue
            
            resultado = response.json()
            
            # Extraer información
            scientific_output = resultado.get('scientific_output', {})
            phase_a = resultado.get('phase_a_normalized', {})
            environment = resultado.get('environment_context', {})
            measurements = resultado.get('instrumental_measurements', [])
            
            # Mostrar resultados
            print(f"\n[RESULTADOS]", flush=True)
            print(f"  Ambiente: {environment.get('environment_type', 'unknown')}", flush=True)
            print(f"  Anomaly score: {scientific_output.get('anomaly_score', 0):.3f}", flush=True)
            print(f"  Anthropic probability: {scientific_output.get('anthropic_probability', 0):.3f}", flush=True)
            print(f"  Candidate type: {scientific_output.get('candidate_type', 'unknown')}", flush=True)
            print(f"  Scientific confidence: {scientific_output.get('scientific_confidence', 'unknown')}", flush=True)
            
            # FASE 0: Enriquecimiento
            previous_analyses = phase_a.get('local_context', {}).get('previous_analyses')
            if previous_analyses:
                print(f"\n[FASE 0] Enriquecido con {len(previous_analyses)} análisis previos", flush=True)
            
            # FASE F: Sitios conocidos
            is_rediscovery = scientific_output.get('is_known_site_rediscovery', False)
            overlapping = scientific_output.get('overlapping_known_site')
            nearby = scientific_output.get('known_sites_nearby', [])
            distance = scientific_output.get('distance_to_known_site_km')
            
            print(f"\n[FASE F] Validación contra sitios conocidos:", flush=True)
            if is_rediscovery:
                print(f"  ⚠️ REDESCUBRIMIENTO: {overlapping['name']}", flush=True)
                print(f"     Tipo: {overlapping['site_type']}", flush=True)
                print(f"     Confianza: {overlapping['confidence_level']}", flush=True)
            elif nearby:
                print(f"  Sitios cercanos: {len(nearby)}", flush=True)
                for site in nearby[:2]:
                    print(f"    - {site['name']} ({site['distance_km']:.1f}km)", flush=True)
            else:
                print(f"  No hay sitios conocidos cercanos", flush=True)
            
            if distance is not None:
                print(f"  Distancia al sitio más cercano: {distance:.1f}km", flush=True)
            
            es_anomalia = scientific_output.get('anthropic_probability', 0) >= 0.5
            
            if es_anomalia:
                print(f"\n🎯 [RESULTADO] ANOMALÍA DETECTADA", flush=True)
            else:
                print(f"\n⚪ [RESULTADO] NO ES ANOMALÍA", flush=True)
            
            # PISAR datos en BD
            print(f"\n[BD] Pisando datos anteriores...", flush=True)
            
            # Buscar ID numérico del candidato por analysis_id
            existing_candidate_id = await conn.fetchval(
                "SELECT id FROM archaeological_candidates WHERE candidate_id::text = $1",
                str(analysis_id)
            )
            
            if existing_candidate_id:
                # Convertir UUID a string si es necesario
                existing_candidate_id_str = str(existing_candidate_id)
                
                # 1. Borrar análisis anterior
                deleted_analyses = await conn.execute(
                    "DELETE FROM archaeological_candidate_analyses WHERE candidate_id::text = $1",
                    existing_candidate_id_str
                )
                print(f"  Análisis anteriores borrados: {deleted_analyses}", flush=True)
                
                # 2. Borrar candidato anterior
                deleted_candidates = await conn.execute(
                    "DELETE FROM archaeological_candidates WHERE id::text = $1",
                    existing_candidate_id_str
                )
                print(f"  Candidatos anteriores borrados: {deleted_candidates}", flush=True)
            else:
                print(f"  No hay datos anteriores para este candidato", flush=True)
            
            # 3. Guardar nuevo candidato
            status_value = 'analyzed' if es_anomalia else 'rejected'
            area_km2 = 0.1 * 0.1 * 111 * 111
            total_instruments = len(measurements) if len(measurements) > 0 else 1
            usables = sum(1 for m in measurements if m.get('data_mode') in ['OK', 'DERIVED'])
            convergence_ratio = usables / total_instruments
            
            action_map = {
                'field_verification_priority': 'field_validation',
                'field_verification': 'field_validation',
                'monitoring': 'monitor',
                'no_action': 'discard',
                'reject_natural_process': 'discard'
            }
            recommended_action_value = action_map.get(
                scientific_output.get('recommended_action', 'no_action'),
                'discard'
            )
            
            candidate_id = await conn.fetchval("""
                INSERT INTO archaeological_candidates 
                (candidate_id, center_lat, center_lon, zone_id, area_km2, multi_instrumental_score, 
                 convergence_count, convergence_ratio, recommended_action, status, analysis_results, signals)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                RETURNING id
            """, 
                str(analysis_id), lat, lon, region_name, area_km2,
                scientific_output.get('anthropic_probability', 0),
                usables, convergence_ratio, recommended_action_value, status_value,
                json.dumps(scientific_output), json.dumps(phase_a.get('features', {}))
            )
            
            print(f"  Nuevo candidato guardado (ID: {candidate_id})", flush=True)
            
            # 4. Guardar nuevo análisis
            analysis_metadata = {
                'scientific_output': scientific_output,
                'phase_a_normalized': phase_a,
                'environment_context': environment,
                'timestamp': datetime.now().isoformat()
            }
            
            analysis_record_id = await conn.fetchval("""
                INSERT INTO archaeological_candidate_analyses
                (candidate_id, candidate_name, region, environment_detected, environment_confidence,
                 archaeological_probability, confidence, result_type, instruments_measuring,
                 instruments_total, convergence_achieved, ai_available, full_result)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                RETURNING id
            """, 
                str(candidate_id), region_name, region_name,
                environment.get('environment_type', 'unknown'),
                environment.get('confidence', 0),
                scientific_output.get('anthropic_probability', 0),
                {'high': 0.9, 'medium': 0.6, 'low': 0.3, 'unknown': 0.0}.get(scientific_output.get('scientific_confidence', 'unknown'), 0.0),
                'anomaly' if es_anomalia else 'normal',
                usables, len(measurements), usables > 0, False,
                json.dumps(analysis_metadata)
            )
            
            print(f"  Nuevo análisis guardado (ID: {analysis_record_id})", flush=True)
            
        except requests.exceptions.Timeout:
            print(f"\n[ERROR] TIMEOUT en análisis (>180s)", flush=True)
        except Exception as e:
            print(f"\n[ERROR] Error en análisis: {e}", flush=True)
            import traceback
            traceback.print_exc()
    
    # Estadísticas finales
    print(f"\n{'='*80}", flush=True)
    print("ESTADÍSTICAS FINALES", flush=True)
    print(f"{'='*80}", flush=True)
    
    total_candidates = await conn.fetchval('SELECT COUNT(*) FROM archaeological_candidates')
    total_analyses = await conn.fetchval('SELECT COUNT(*) FROM archaeological_candidate_analyses')
    total_measurements = await conn.fetchval('SELECT COUNT(*) FROM measurements')
    
    print(f"Candidatos en BD: {total_candidates}", flush=True)
    print(f"Análisis en BD: {total_analyses}", flush=True)
    print(f"Mediciones en BD: {total_measurements} (NO BORRADAS)", flush=True)
    
    print(f"\n✅ [SUCCESS] Re-análisis completado", flush=True)
    print(f"{'='*80}\n", flush=True)
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(reanalyze_candidates())
