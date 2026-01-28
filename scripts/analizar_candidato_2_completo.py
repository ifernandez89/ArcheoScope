#!/usr/bin/env python3
"""
Análisis completo del candidato 2: Acre Brasil - Geoglifos Amazónicos
"""

import asyncio
import asyncpg
import requests
import json

API_BASE = "http://localhost:8002"

async def analyze_acre_complete():
    """Analizar Acre Brasil con reporte completo."""
    
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    print("="*80, flush=True)
    print("ANÁLISIS COMPLETO - CANDIDATO 2", flush=True)
    print("ACRE BRASIL - GEOGLIFOS AMAZÓNICOS", flush=True)
    print("="*80, flush=True)
    
    # Datos del candidato
    analysis_id = "7181a57d-0061-44a6-997d-f6440525e2e1"
    region_name = "Acre Brasil - Geoglifos Amazonicos"
    lat = -9.8
    lon = -67.8
    
    print(f"\n📍 UBICACIÓN", flush=True)
    print(f"  Región: {region_name}", flush=True)
    print(f"  Coordenadas: {lat:.4f}°S, {lon:.4f}°W", flush=True)
    print(f"  Analysis ID: {analysis_id}", flush=True)
    
    # Ver mediciones existentes
    measurements = await conn.fetch("""
        SELECT instrument_name, value, data_mode, source
        FROM measurements
        WHERE analysis_id = $1
        ORDER BY instrument_name
        LIMIT 10
    """, analysis_id)
    
    print(f"\n📊 MEDICIONES PREVIAS EN BD: {len(measurements)} instrumentos", flush=True)
    for m in measurements:
        print(f"  • {m['instrument_name']}: {m['value']:.3f} ({m['data_mode']})", flush=True)
    
    lat_min = lat - 0.05
    lat_max = lat + 0.05
    lon_min = lon - 0.05
    lon_max = lon + 0.05
    
    try:
        print(f"\n🔬 EJECUTANDO PIPELINE CIENTÍFICO...", flush=True)
        
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
            print(f"❌ ERROR en API: {response.status_code}", flush=True)
            await conn.close()
            return
        
        resultado = response.json()
        
        # Extraer todas las fases
        scientific_output = resultado.get('scientific_output', {})
        phase_a = resultado.get('phase_a_normalized', {})
        phase_b = resultado.get('phase_b_anomaly', {})
        phase_c = resultado.get('phase_c_morphology', {})
        phase_d = resultado.get('phase_d_anthropic', {})
        phase_e = resultado.get('phase_e_anti_pattern')
        environment = resultado.get('environment_context', {})
        new_measurements = resultado.get('instrumental_measurements', [])
        
        print(f"\n{'='*80}", flush=True)
        print("RESULTADOS DEL ANÁLISIS", flush=True)
        print(f"{'='*80}", flush=True)
        
        # AMBIENTE
        print(f"\n🌍 AMBIENTE DETECTADO", flush=True)
        print(f"  Tipo: {environment.get('environment_type', 'unknown')}", flush=True)
        print(f"  Confianza: {environment.get('confidence', 0):.2f}", flush=True)
        print(f"  Visibilidad arqueológica: {environment.get('archaeological_visibility', 'unknown')}", flush=True)
        print(f"  Potencial preservación: {environment.get('preservation_potential', 'unknown')}", flush=True)
        print(f"  Sensores primarios: {', '.join(environment.get('primary_sensors', []))}", flush=True)
        
        # FASE 0
        print(f"\n📚 FASE 0: ENRIQUECIMIENTO CON DATOS HISTÓRICOS", flush=True)
        previous_analyses = phase_a.get('local_context', {}).get('previous_analyses')
        if previous_analyses:
            print(f"  ✅ Enriquecido con {len(previous_analyses)} análisis previos en región", flush=True)
            for pa in previous_analyses[:3]:
                print(f"    • {pa.get('candidate_name')}: prob={pa.get('archaeological_probability', 0):.3f}", flush=True)
        else:
            print(f"  ℹ️ No hay análisis previos en la región", flush=True)
        
        # MEDICIONES INSTRUMENTALES
        print(f"\n🛰️ MEDICIONES INSTRUMENTALES UTILIZADAS", flush=True)
        print(f"  Total instrumentos: {len(new_measurements)}", flush=True)
        usables = [m for m in new_measurements if m.get('data_mode') in ['OK', 'DERIVED']]
        print(f"  Instrumentos con datos válidos: {len(usables)}/{len(new_measurements)}", flush=True)
        print(f"\n  Detalle por instrumento:", flush=True)
        for m in new_measurements:
            status = "✅" if m.get('data_mode') in ['OK', 'DERIVED'] else "❌"
            print(f"    {status} {m.get('instrument_name')}: {m.get('value', 0):.3f} ({m.get('data_mode')})", flush=True)
            if m.get('source'):
                print(f"       Fuente: {m.get('source')}", flush=True)
        
        # FASE A
        print(f"\n📐 FASE A: NORMALIZACIÓN", flush=True)
        local_context = phase_a.get('local_context', {})
        features = phase_a.get('features', {})
        print(f"  Status: {local_context.get('features_status', 'unknown')}", flush=True)
        if local_context.get('reason'):
            print(f"  Razón: {local_context.get('reason')}", flush=True)
        print(f"  Features normalizadas: {len(features)}", flush=True)
        if len(features) > 0:
            print(f"  Top features:", flush=True)
            for k, v in list(features.items())[:5]:
                print(f"    • {k}: {v:.3f}", flush=True)
        
        # FASE B
        print(f"\n🔍 FASE B: DETECCIÓN DE ANOMALÍA PURA", flush=True)
        print(f"  Anomaly score: {phase_b.get('anomaly_score', 0):.3f}", flush=True)
        print(f"  Confianza: {phase_b.get('confidence', 'unknown')}", flush=True)
        print(f"  Método: {phase_b.get('method', 'unknown')}", flush=True)
        outliers = phase_b.get('outlier_dimensions', [])
        if outliers:
            print(f"  Dimensiones outlier detectadas:", flush=True)
            for o in outliers[:5]:
                print(f"    • {o}", flush=True)
        
        # FASE C
        print(f"\n🏗️ FASE C: ANÁLISIS MORFOLÓGICO", flush=True)
        print(f"  Simetría: {phase_c.get('symmetry_score', 0):.3f}", flush=True)
        print(f"  Regularidad de bordes: {phase_c.get('edge_regularity', 0):.3f}", flush=True)
        print(f"  Planaridad: {phase_c.get('planarity', 0):.3f}", flush=True)
        indicators = phase_c.get('artificial_indicators', [])
        if indicators:
            print(f"  Indicadores artificiales:", flush=True)
            for ind in indicators:
                print(f"    • {ind}", flush=True)
        else:
            print(f"  Indicadores artificiales: ninguno", flush=True)
        print(f"  Geomorfología inferida: {phase_c.get('geomorphology_hint', 'unknown')}", flush=True)
        
        # FASE D
        print(f"\n🧠 FASE D: INFERENCIA ANTROPOGÉNICA", flush=True)
        print(f"  Probabilidad antropogénica: {phase_d.get('anthropic_probability', 0):.3f}", flush=True)
        print(f"  Intervalo de confianza: [{phase_d.get('confidence_interval', [0, 0])[0]:.3f}, {phase_d.get('confidence_interval', [0, 0])[1]:.3f}]", flush=True)
        print(f"  Confianza: {phase_d.get('confidence', 'unknown')}", flush=True)
        print(f"  Modelo usado: {phase_d.get('model_used', 'unknown')}", flush=True)
        print(f"  Razonamiento:", flush=True)
        for r in phase_d.get('reasoning', []):
            print(f"    • {r}", flush=True)
        
        # FASE E
        print(f"\n⚠️ FASE E: VERIFICACIÓN DE ANTI-PATRONES", flush=True)
        if phase_e:
            print(f"  ❌ RECHAZADO como: {phase_e.get('rejected_as', 'unknown')}", flush=True)
            print(f"  Confianza del rechazo: {phase_e.get('confidence', 0):.2f}", flush=True)
            print(f"  Features en conflicto: {', '.join(phase_e.get('features_conflict', []))}", flush=True)
        else:
            print(f"  ✅ No se detectaron anti-patrones naturales", flush=True)
        
        # FASE F
        print(f"\n🏛️ FASE F: VALIDACIÓN CONTRA SITIOS CONOCIDOS", flush=True)
        is_rediscovery = scientific_output.get('is_known_site_rediscovery', False)
        overlapping = scientific_output.get('overlapping_known_site')
        nearby = scientific_output.get('known_sites_nearby', [])
        distance = scientific_output.get('distance_to_known_site_km')
        
        if is_rediscovery:
            print(f"  🎯 REDESCUBRIMIENTO DE SITIO CONOCIDO", flush=True)
            print(f"    Nombre: {overlapping['name']}", flush=True)
            print(f"    Tipo: {overlapping['site_type']}", flush=True)
            print(f"    Período: {overlapping.get('period', 'unknown')}", flush=True)
            print(f"    Nivel de confianza: {overlapping['confidence_level']}", flush=True)
            print(f"    Fuente: {overlapping['source']}", flush=True)
        elif nearby:
            print(f"  📍 Sitios conocidos cercanos: {len(nearby)}", flush=True)
            for site in nearby[:3]:
                print(f"    • {site['name']} ({site['distance_km']:.1f}km)", flush=True)
                print(f"      Tipo: {site['site_type']}", flush=True)
        else:
            print(f"  ℹ️ No hay sitios arqueológicos conocidos cercanos", flush=True)
        
        if distance is not None:
            print(f"  Distancia al sitio más cercano: {distance:.1f}km", flush=True)
        
        # FASE G
        print(f"\n📋 FASE G: SALIDA CIENTÍFICA", flush=True)
        print(f"  Anomaly score final: {scientific_output.get('anomaly_score', 0):.3f}", flush=True)
        print(f"  Probabilidad antropogénica final: {scientific_output.get('anthropic_probability', 0):.3f}", flush=True)
        print(f"  Intervalo de confianza: {scientific_output.get('confidence_interval', [0, 0])}", flush=True)
        print(f"  Tipo de candidato: {scientific_output.get('candidate_type', 'unknown')}", flush=True)
        print(f"  Tipo de descarte: {scientific_output.get('discard_type', 'none')}", flush=True)
        print(f"  Confianza científica: {scientific_output.get('scientific_confidence', 'unknown')}", flush=True)
        print(f"  Acción recomendada: {scientific_output.get('recommended_action', 'unknown')}", flush=True)
        if scientific_output.get('negative_reason'):
            print(f"  Razón negativa: {scientific_output.get('negative_reason')}", flush=True)
            print(f"  Reusar para entrenamiento: {scientific_output.get('reuse_for_training', False)}", flush=True)
        print(f"  Notas: {scientific_output.get('notes', 'N/A')}", flush=True)
        
        # RESULTADO FINAL
        es_anomalia = scientific_output.get('anthropic_probability', 0) >= 0.5
        
        print(f"\n{'='*80}", flush=True)
        print("RESULTADO FINAL", flush=True)
        print(f"{'='*80}", flush=True)
        
        if es_anomalia:
            print(f"\n🎯 ANOMALÍA DETECTADA", flush=True)
            print(f"  Probabilidad: {scientific_output.get('anthropic_probability', 0):.1%}", flush=True)
            print(f"  Requiere: {scientific_output.get('recommended_action', 'unknown')}", flush=True)
        else:
            print(f"\n⚪ NO ES ANOMALÍA", flush=True)
            print(f"  Probabilidad: {scientific_output.get('anthropic_probability', 0):.1%}", flush=True)
            print(f"  Clasificación: {scientific_output.get('candidate_type', 'unknown')}", flush=True)
        
        print(f"\n✅ Análisis completado exitosamente", flush=True)
        
        await conn.close()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()
        await conn.close()

if __name__ == "__main__":
    asyncio.run(analyze_acre_complete())
