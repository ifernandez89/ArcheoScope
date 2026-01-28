#!/usr/bin/env python3
"""
Test del primer candidato con pipeline científico completo.
Guarda resultados en BD.
"""

import asyncio
import asyncpg
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8002"

async def test_primer_candidato():
    """Analizar primer candidato con pipeline científico."""
    
    # Conectar a BD
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    print("="*80, flush=True)
    print("TEST PRIMER CANDIDATO - PIPELINE CIENTÍFICO", flush=True)
    print("="*80, flush=True)
    
    # Obtener primer candidato
    candidato = await conn.fetchrow("""
        SELECT 
            analysis_id,
            region_name,
            latitude,
            longitude,
            measurement_timestamp
        FROM measurements
        ORDER BY measurement_timestamp
        LIMIT 1
    """)
    
    if not candidato:
        print("\nNo hay candidatos en BD", flush=True)
        await conn.close()
        return
    
    analysis_id = candidato['analysis_id']
    region_name = candidato['region_name']
    lat = float(candidato['latitude'])
    lon = float(candidato['longitude'])
    
    print(f"\nCANDIDATO 1: {region_name}", flush=True)
    print(f"Coordenadas: {lat:.4f}, {lon:.4f}", flush=True)
    print(f"Analysis ID: {analysis_id}", flush=True)
    
    # Definir bounds (±0.05 grados ~ 5km)
    lat_min = lat - 0.05
    lat_max = lat + 0.05
    lon_min = lon - 0.05
    lon_max = lon + 0.05
    
    try:
        # Ejecutar análisis científico
        print(f"\n[ANALISIS] Ejecutando pipeline científico...", flush=True)
        
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
        
        # Extraer información clave
        scientific_output = resultado.get('scientific_output', {})
        phase_a = resultado.get('phase_a_normalized', {})
        phase_b = resultado.get('phase_b_anomaly', {})
        phase_c = resultado.get('phase_c_morphology', {})
        phase_d = resultado.get('phase_d_anthropic', {})
        phase_e = resultado.get('phase_e_anti_pattern')
        environment = resultado.get('environment_context', {})
        measurements = resultado.get('instrumental_measurements', [])
        
        # Mostrar resultados
        print(f"\n{'='*80}", flush=True)
        print("RESULTADOS DEL ANÁLISIS CIENTÍFICO", flush=True)
        print(f"{'='*80}", flush=True)
        
        print(f"\n[AMBIENTE]", flush=True)
        print(f"  Tipo: {environment.get('environment_type', 'unknown')}", flush=True)
        print(f"  Confianza: {environment.get('confidence', 0):.2f}", flush=True)
        print(f"  Visibilidad arqueológica: {environment.get('archaeological_visibility', 'unknown')}", flush=True)
        
        print(f"\n[FASE A - NORMALIZACIÓN]", flush=True)
        features = phase_a.get('features', {})
        print(f"  Features normalizadas: {len(features)}", flush=True)
        for k, v in list(features.items())[:5]:
            print(f"    - {k}: {v:.3f}", flush=True)
        
        print(f"\n[FASE B - ANOMALÍA PURA]", flush=True)
        print(f"  Anomaly score: {phase_b.get('anomaly_score', 0):.3f}", flush=True)
        print(f"  Confianza: {phase_b.get('confidence', 'unknown')}", flush=True)
        print(f"  Dimensiones outlier: {len(phase_b.get('outlier_dimensions', []))}", flush=True)
        
        print(f"\n[FASE C - MORFOLOGÍA]", flush=True)
        print(f"  Simetría: {phase_c.get('symmetry_score', 0):.3f}", flush=True)
        print(f"  Regularidad bordes: {phase_c.get('edge_regularity', 0):.3f}", flush=True)
        print(f"  Planaridad: {phase_c.get('planarity', 0):.3f}", flush=True)
        print(f"  Indicadores artificiales: {phase_c.get('artificial_indicators', [])}", flush=True)
        
        print(f"\n[FASE D - INFERENCIA ANTROPOGÉNICA]", flush=True)
        print(f"  Probabilidad antropogénica: {phase_d.get('anthropic_probability', 0):.3f}", flush=True)
        print(f"  Intervalo confianza: {phase_d.get('confidence_interval', [0, 0])}", flush=True)
        print(f"  Confianza: {phase_d.get('confidence', 'unknown')}", flush=True)
        print(f"  Razonamiento:", flush=True)
        for r in phase_d.get('reasoning', []):
            print(f"    - {r}", flush=True)
        
        print(f"\n[FASE E - ANTI-PATRONES]", flush=True)
        if phase_e:
            print(f"  RECHAZADO como: {phase_e.get('rejected_as', 'unknown')}", flush=True)
            print(f"  Confianza rechazo: {phase_e.get('confidence', 0):.2f}", flush=True)
        else:
            print(f"  No se detectaron anti-patrones", flush=True)
        
        print(f"\n[FASE F - SALIDA CIENTÍFICA]", flush=True)
        print(f"  Anomaly score: {scientific_output.get('anomaly_score', 0):.3f}", flush=True)
        print(f"  Probabilidad antropogénica: {scientific_output.get('anthropic_probability', 0):.3f}", flush=True)
        print(f"  Intervalo confianza: {scientific_output.get('confidence_interval', [0, 0])}", flush=True)
        print(f"  Acción recomendada: {scientific_output.get('recommended_action', 'unknown')}", flush=True)
        print(f"  Notas: {scientific_output.get('notes', 'N/A')}", flush=True)
        
        print(f"\n[MEDICIONES INSTRUMENTALES]", flush=True)
        print(f"  Total: {len(measurements)}", flush=True)
        usables = sum(1 for m in measurements if m.get('data_mode') in ['OK', 'DERIVED'])
        print(f"  Usables: {usables}/{len(measurements)}", flush=True)
        
        # Determinar si es anomalía
        es_anomalia = scientific_output.get('anthropic_probability', 0) >= 0.5
        
        if es_anomalia:
            print(f"\n[RESULTADO] ANOMALÍA DETECTADA", flush=True)
        else:
            print(f"\n[RESULTADO] NO ES ANOMALÍA", flush=True)
        
        # Guardar en BD
        print(f"\n{'='*80}", flush=True)
        print("GUARDANDO EN BASE DE DATOS", flush=True)
        print(f"{'='*80}", flush=True)
        
        # Borrar candidato existente si existe
        await conn.execute("""
            DELETE FROM archaeological_candidates 
            WHERE candidate_id = $1
        """, str(analysis_id))
        
        # 1. Guardar candidato
        status_value = 'analyzed' if es_anomalia else 'rejected'
        
        # Calcular área aproximada (bounds de ±0.05 grados ~ 5km)
        area_km2 = 0.1 * 0.1 * 111 * 111  # Aproximación simple
        
        # Calcular convergence_ratio
        total_instruments = len(measurements) if len(measurements) > 0 else 1
        convergence_ratio = usables / total_instruments
        
        # Mapear recommended_action a valores del enum
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
            str(analysis_id),  # candidate_id
            lat, lon, 
            region_name,
            area_km2,
            scientific_output.get('anthropic_probability', 0),
            usables,
            convergence_ratio,
            recommended_action_value,
            status_value,
            json.dumps(scientific_output),
            json.dumps(phase_a.get('features', {}))
        )
        
        print(f"[OK] Candidato guardado (ID: {candidate_id})", flush=True)
        
        # 2. Guardar análisis detallado
        analysis_metadata = {
            'scientific_output': scientific_output,
            'phase_a_normalized': phase_a,
            'phase_b_anomaly': phase_b,
            'phase_c_morphology': phase_c,
            'phase_d_anthropic': phase_d,
            'phase_e_anti_pattern': phase_e,
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
            str(candidate_id),  # Convertir UUID a string
            region_name,
            region_name,
            environment.get('environment_type', 'unknown'),
            environment.get('confidence', 0),
            scientific_output.get('anthropic_probability', 0),
            {'high': 0.9, 'medium': 0.6, 'low': 0.3, 'unknown': 0.0}.get(phase_d.get('confidence', 'unknown'), 0.0),
            'anomaly' if es_anomalia else 'normal',
            usables,
            len(measurements),
            usables > 0,
            False,  # ai_available
            json.dumps(analysis_metadata)
        )
        
        print(f"[OK] Análisis guardado (ID: {analysis_record_id})", flush=True)
        
        # Estadísticas finales
        print(f"\n{'='*80}", flush=True)
        print("ESTADÍSTICAS DE BASE DE DATOS", flush=True)
        print(f"{'='*80}", flush=True)
        
        total_candidates = await conn.fetchval('SELECT COUNT(*) FROM archaeological_candidates')
        total_analyses = await conn.fetchval('SELECT COUNT(*) FROM archaeological_candidate_analyses')
        total_measurements = await conn.fetchval('SELECT COUNT(*) FROM measurements')
        
        print(f"Candidatos en BD: {total_candidates}", flush=True)
        print(f"Análisis en BD: {total_analyses}", flush=True)
        print(f"Mediciones en BD: {total_measurements}", flush=True)
        
        print(f"\n[SUCCESS] Test completado exitosamente", flush=True)
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
    asyncio.run(test_primer_candidato())
