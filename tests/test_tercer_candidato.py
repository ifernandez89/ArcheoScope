#!/usr/bin/env python3
"""
Analizar el tercer candidato con pipeline científico completo.
"""

import asyncio
import asyncpg
import requests
import json

API_BASE = "http://localhost:8002"

async def analyze_third_candidate():
    """Analizar tercer candidato."""
    
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    print("="*80, flush=True)
    print("ANÁLISIS DEL TERCER CANDIDATO", flush=True)
    print("="*80, flush=True)
    
    # Obtener tercer candidato
    candidato = await conn.fetchrow("""
        SELECT 
            analysis_id,
            region_name,
            latitude,
            longitude,
            measurement_timestamp
        FROM measurements
        ORDER BY measurement_timestamp
        LIMIT 1 OFFSET 2
    """)
    
    if not candidato:
        print("\nNo hay tercer candidato en BD", flush=True)
        await conn.close()
        return
    
    analysis_id = candidato['analysis_id']
    region_name = candidato['region_name']
    lat = float(candidato['latitude'])
    lon = float(candidato['longitude'])
    
    print(f"\nCANDIDATO 3: {region_name}", flush=True)
    print(f"Coordenadas: {lat:.4f}, {lon:.4f}", flush=True)
    print(f"Analysis ID: {analysis_id}", flush=True)
    print(f"Timestamp: {candidato['measurement_timestamp']}", flush=True)
    
    # Ver mediciones existentes
    measurements = await conn.fetch("""
        SELECT instrument_name, value, data_mode
        FROM measurements
        WHERE analysis_id = $1
        ORDER BY instrument_name
    """, analysis_id)
    
    print(f"\n[MEDICIONES EXISTENTES] {len(measurements)} instrumentos", flush=True)
    for m in measurements:
        print(f"  - {m['instrument_name']}: {m['value']:.3f} ({m['data_mode']})", flush=True)
    
    lat_min = lat - 0.05
    lat_max = lat + 0.05
    lon_min = lon - 0.05
    lon_max = lon + 0.05
    
    try:
        print(f"\n[ANALISIS] Ejecutando pipeline científico completo...", flush=True)
        
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
            await conn.close()
            return
        
        resultado = response.json()
        
        # Extraer información
        scientific_output = resultado.get('scientific_output', {})
        phase_a = resultado.get('phase_a_normalized', {})
        phase_b = resultado.get('phase_b_anomaly', {})
        phase_c = resultado.get('phase_c_morphology', {})
        phase_d = resultado.get('phase_d_anthropic', {})
        phase_e = resultado.get('phase_e_anti_pattern')
        environment = resultado.get('environment_context', {})
        new_measurements = resultado.get('instrumental_measurements', [])
        
        # Mostrar resultados
        print(f"\n{'='*80}", flush=True)
        print("RESULTADOS DEL ANÁLISIS CIENTÍFICO", flush=True)
        print(f"{'='*80}", flush=True)
        
        print(f"\n[AMBIENTE]", flush=True)
        print(f"  Tipo: {environment.get('environment_type', 'unknown')}", flush=True)
        print(f"  Confianza: {environment.get('confidence', 0):.2f}", flush=True)
        print(f"  Visibilidad arqueológica: {environment.get('archaeological_visibility', 'unknown')}", flush=True)
        print(f"  Potencial preservación: {environment.get('preservation_potential', 'unknown')}", flush=True)
        
        print(f"\n[FASE 0 - ENRIQUECIMIENTO]", flush=True)
        previous_analyses = phase_a.get('local_context', {}).get('previous_analyses')
        if previous_analyses:
            print(f"  ✅ Enriquecido con {len(previous_analyses)} análisis previos", flush=True)
        else:
            print(f"  No hay análisis previos en la región", flush=True)
        
        print(f"\n[FASE A - NORMALIZACIÓN]", flush=True)
        local_context = phase_a.get('local_context', {})
        features = phase_a.get('features', {})
        print(f"  Features status: {local_context.get('features_status', 'unknown')}", flush=True)
        if local_context.get('reason'):
            print(f"  Razón: {local_context.get('reason')}", flush=True)
        print(f"  Features normalizadas: {len(features)}", flush=True)
        
        print(f"\n[FASE B - ANOMALÍA PURA]", flush=True)
        print(f"  Anomaly score: {phase_b.get('anomaly_score', 0):.3f}", flush=True)
        print(f"  Confianza: {phase_b.get('confidence', 'unknown')}", flush=True)
        outliers = phase_b.get('outlier_dimensions', [])
        if outliers:
            print(f"  Dimensiones outlier: {', '.join(outliers[:3])}", flush=True)
        
        print(f"\n[FASE C - MORFOLOGÍA]", flush=True)
        print(f"  Simetría: {phase_c.get('symmetry_score', 0):.3f}", flush=True)
        print(f"  Regularidad bordes: {phase_c.get('edge_regularity', 0):.3f}", flush=True)
        print(f"  Planaridad: {phase_c.get('planarity', 0):.3f}", flush=True)
        print(f"  Indicadores artificiales: {phase_c.get('artificial_indicators', [])}", flush=True)
        print(f"  Geomorfología: {phase_c.get('geomorphology_hint', 'unknown')}", flush=True)
        
        print(f"\n[FASE D - INFERENCIA ANTROPOGÉNICA]", flush=True)
        print(f"  Probabilidad antropogénica: {phase_d.get('anthropic_probability', 0):.3f}", flush=True)
        print(f"  Intervalo confianza: {phase_d.get('confidence_interval', [0, 0])}", flush=True)
        print(f"  Confianza: {phase_d.get('confidence', 'unknown')}", flush=True)
        print(f"  Razonamiento:", flush=True)
        for r in phase_d.get('reasoning', []):
            print(f"    - {r}", flush=True)
        
        print(f"\n[FASE E - ANTI-PATRONES]", flush=True)
        if phase_e:
            print(f"  ⚠️ RECHAZADO como: {phase_e.get('rejected_as', 'unknown')}", flush=True)
            print(f"  Confianza rechazo: {phase_e.get('confidence', 0):.2f}", flush=True)
        else:
            print(f"  ✅ No se detectaron anti-patrones", flush=True)
        
        print(f"\n[FASE F - VALIDACIÓN SITIOS CONOCIDOS]", flush=True)
        is_rediscovery = scientific_output.get('is_known_site_rediscovery', False)
        overlapping = scientific_output.get('overlapping_known_site')
        nearby = scientific_output.get('known_sites_nearby', [])
        distance = scientific_output.get('distance_to_known_site_km')
        
        if is_rediscovery:
            print(f"  ⚠️ REDESCUBRIMIENTO: {overlapping['name']}", flush=True)
            print(f"     Tipo: {overlapping['site_type']}", flush=True)
            print(f"     Período: {overlapping.get('period', 'unknown')}", flush=True)
            print(f"     Confianza: {overlapping['confidence_level']}", flush=True)
            print(f"     Fuente: {overlapping['source']}", flush=True)
        elif nearby:
            print(f"  Sitios cercanos: {len(nearby)}", flush=True)
            for site in nearby[:3]:
                print(f"    - {site['name']} ({site['distance_km']:.1f}km)", flush=True)
                print(f"      Tipo: {site['site_type']}", flush=True)
        else:
            print(f"  No hay sitios conocidos cercanos", flush=True)
        
        if distance is not None:
            print(f"  Distancia al sitio más cercano: {distance:.1f}km", flush=True)
        
        print(f"\n[FASE G - SALIDA CIENTÍFICA]", flush=True)
        print(f"  Anomaly score: {scientific_output.get('anomaly_score', 0):.3f}", flush=True)
        print(f"  Probabilidad antropogénica: {scientific_output.get('anthropic_probability', 0):.3f}", flush=True)
        print(f"  Intervalo confianza: {scientific_output.get('confidence_interval', [0, 0])}", flush=True)
        print(f"  Tipo candidato: {scientific_output.get('candidate_type', 'unknown')}", flush=True)
        print(f"  Tipo descarte: {scientific_output.get('discard_type', 'none')}", flush=True)
        print(f"  Confianza científica: {scientific_output.get('scientific_confidence', 'unknown')}", flush=True)
        print(f"  Acción recomendada: {scientific_output.get('recommended_action', 'unknown')}", flush=True)
        if scientific_output.get('negative_reason'):
            print(f"  Razón negativa: {scientific_output.get('negative_reason')}", flush=True)
            print(f"  Reusar para entrenamiento: {scientific_output.get('reuse_for_training', False)}", flush=True)
        print(f"  Notas: {scientific_output.get('notes', 'N/A')}", flush=True)
        
        print(f"\n[MEDICIONES INSTRUMENTALES]", flush=True)
        print(f"  Total: {len(new_measurements)}", flush=True)
        usables = sum(1 for m in new_measurements if m.get('data_mode') in ['OK', 'DERIVED'])
        print(f"  Usables: {usables}/{len(new_measurements)}", flush=True)
        
        es_anomalia = scientific_output.get('anthropic_probability', 0) >= 0.5
        
        if es_anomalia:
            print(f"\n🎯 [RESULTADO FINAL] ANOMALÍA DETECTADA", flush=True)
        else:
            print(f"\n⚪ [RESULTADO FINAL] NO ES ANOMALÍA", flush=True)
        
        # Guardar en BD
        print(f"\n{'='*80}", flush=True)
        print("GUARDANDO EN BASE DE DATOS", flush=True)
        print(f"{'='*80}", flush=True)
        
        # Buscar y borrar si existe
        existing_candidate_id = await conn.fetchval(
            "SELECT id FROM archaeological_candidates WHERE candidate_id::text = $1",
            str(analysis_id)
        )
        
        if existing_candidate_id:
            existing_candidate_id_str = str(existing_candidate_id)
            await conn.execute(
                "DELETE FROM archaeological_candidate_analyses WHERE candidate_id::text = $1",
                existing_candidate_id_str
            )
            await conn.execute(
                "DELETE FROM archaeological_candidates WHERE id::text = $1",
                existing_candidate_id_str
            )
            print(f"  Datos anteriores borrados", flush=True)
        
        # Guardar nuevo candidato
        status_value = 'analyzed' if es_anomalia else 'rejected'
        area_km2 = 0.1 * 0.1 * 111 * 111
        total_instruments = len(new_measurements) if len(new_measurements) > 0 else 1
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
        
        print(f"  Candidato guardado (ID: {candidate_id})", flush=True)
        
        # Guardar análisis
        analysis_metadata = {
            'scientific_output': scientific_output,
            'phase_a_normalized': phase_a,
            'phase_b_anomaly': phase_b,
            'phase_c_morphology': phase_c,
            'phase_d_anthropic': phase_d,
            'phase_e_anti_pattern': phase_e,
            'environment_context': environment,
            'timestamp': resultado.get('scientific_output', {}).get('timestamp')
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
            {'high': 0.9, 'medium_high': 0.75, 'medium': 0.6, 'low': 0.3, 'unknown': 0.0}.get(
                scientific_output.get('scientific_confidence', 'unknown'), 0.0
            ),
            'anomaly' if es_anomalia else 'normal',
            usables, len(new_measurements), usables > 0, False,
            json.dumps(analysis_metadata)
        )
        
        print(f"  Análisis guardado (ID: {analysis_record_id})", flush=True)
        
        print(f"\n✅ [SUCCESS] Análisis completado y guardado", flush=True)
        print(f"{'='*80}\n", flush=True)
        
    except requests.exceptions.Timeout:
        print(f"\n[ERROR] TIMEOUT en análisis (>180s)", flush=True)
    except Exception as e:
        print(f"\n[ERROR] Error en análisis: {e}", flush=True)
        import traceback
        traceback.print_exc()
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(analyze_third_candidate())
