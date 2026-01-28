#!/usr/bin/env python3
"""
Análisis completo del candidato 4: Patagonia Lago Buenos Aires
"""

import asyncio
import asyncpg
import requests
import json

API_BASE = "http://localhost:8002"

async def analyze_patagonia_complete():
    """Analizar Patagonia Lago Buenos Aires con reporte completo."""
    
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    print("="*80, flush=True)
    print("ANÁLISIS COMPLETO - CANDIDATO 4", flush=True)
    print("PATAGONIA LAGO BUENOS AIRES", flush=True)
    print("="*80, flush=True)
    
    # Datos del candidato
    region_name = "Patagonia Lago Buenos Aires"
    lat = -46.5
    lon = -71.0
    
    print(f"\n📍 UBICACIÓN", flush=True)
    print(f"  Región: {region_name}", flush=True)
    print(f"  Coordenadas: {lat:.4f}°S, {lon:.4f}°W", flush=True)
    
    # Ver si hay mediciones existentes
    measurements = await conn.fetch("""
        SELECT instrument_name, value, data_mode, source, analysis_id
        FROM measurements
        WHERE latitude BETWEEN $1 AND $2
          AND longitude BETWEEN $3 AND $4
        ORDER BY measurement_timestamp DESC
        LIMIT 10
    """, lat - 0.1, lat + 0.1, lon - 0.1, lon + 0.1)
    
    if measurements:
        print(f"\n📊 MEDICIONES PREVIAS EN BD: {len(measurements)} registros", flush=True)
        analysis_id = measurements[0]['analysis_id']
        print(f"  Analysis ID: {analysis_id}", flush=True)
        for m in measurements[:6]:
            print(f"  • {m['instrument_name']}: {m['value']:.3f} ({m['data_mode']})", flush=True)
    else:
        print(f"\n📊 No hay mediciones previas en BD", flush=True)
        analysis_id = None
    
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
            "candidate_id": str(analysis_id) if analysis_id else None
        }
        
        response = requests.post(
            f"{API_BASE}/analyze-scientific",
            json=payload,
            timeout=180
        )
        
        if response.status_code != 200:
            print(f"❌ ERROR en API: {response.status_code}", flush=True)
            print(f"Response: {response.text}", flush=True)
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
        
        # MEDICIONES INSTRUMENTALES
        print(f"\n🛰️ MEDICIONES INSTRUMENTALES UTILIZADAS", flush=True)
        print(f"  Total instrumentos: {len(new_measurements)}", flush=True)
        usables = [m for m in new_measurements if m.get('data_mode') in ['OK', 'DERIVED']]
        print(f"  Instrumentos con datos válidos: {len(usables)}/{len(new_measurements)}", flush=True)
        coverage_pct = (len(usables) / 8 * 100) if len(usables) > 0 else 0
        print(f"  Cobertura instrumental: {coverage_pct:.0f}%", flush=True)
        print(f"\n  Detalle por instrumento:", flush=True)
        for m in new_measurements:
            status = "✅" if m.get('data_mode') in ['OK', 'DERIVED'] else "❌"
            print(f"    {status} {m.get('instrument_name')}: {m.get('value', 0):.3f} ({m.get('data_mode')})", flush=True)
        
        # FASE B
        print(f"\n🔍 FASE B: DETECCIÓN DE ANOMALÍA PURA", flush=True)
        print(f"  Anomaly score: {phase_b.get('anomaly_score', 0):.3f}", flush=True)
        print(f"  Confianza: {phase_b.get('confidence', 'unknown')}", flush=True)
        outliers = phase_b.get('outlier_dimensions', [])
        if outliers:
            print(f"  Dimensiones outlier: {len(outliers)}", flush=True)
        
        # FASE C
        print(f"\n🏗️ FASE C: ANÁLISIS MORFOLÓGICO", flush=True)
        print(f"  Simetría: {phase_c.get('symmetry_score', 0):.3f}", flush=True)
        print(f"  Regularidad de bordes: {phase_c.get('edge_regularity', 0):.3f}", flush=True)
        print(f"  Planaridad: {phase_c.get('planarity', 0):.3f}", flush=True)
        print(f"  Geomorfología inferida: {phase_c.get('geomorphology_hint', 'unknown')}", flush=True)
        
        paleo_sig = phase_c.get('paleo_signature')
        if paleo_sig:
            print(f"\n  🏜️ FIRMA ESPECIAL DETECTADA:", flush=True)
            print(f"    Tipo: {paleo_sig.get('type', 'unknown')}", flush=True)
            print(f"    Probabilidad: {paleo_sig.get('probability', 0):.2f}", flush=True)
        
        # FASE D
        print(f"\n🧠 FASE D: INFERENCIA ANTROPOGÉNICA", flush=True)
        print(f"  Probabilidad antropogénica: {phase_d.get('anthropic_probability', 0):.3f}", flush=True)
        print(f"  Intervalo de confianza: [{phase_d.get('confidence_interval', [0, 0])[0]:.3f}, {phase_d.get('confidence_interval', [0, 0])[1]:.3f}]", flush=True)
        print(f"  Confianza: {phase_d.get('confidence', 'unknown')}", flush=True)
        print(f"  Razonamiento:", flush=True)
        for r in phase_d.get('reasoning', []):
            print(f"    • {r}", flush=True)
        
        # FASE E
        print(f"\n⚠️ FASE E: VERIFICACIÓN DE ANTI-PATRONES", flush=True)
        if phase_e:
            print(f"  ❌ RECHAZADO como: {phase_e.get('rejected_as', 'unknown')}", flush=True)
        else:
            print(f"  ✅ No se detectaron anti-patrones naturales", flush=True)
        
        # FASE F
        print(f"\n🏛️ FASE F: VALIDACIÓN CONTRA SITIOS CONOCIDOS", flush=True)
        is_rediscovery = scientific_output.get('is_known_site_rediscovery', False)
        nearby = scientific_output.get('known_sites_nearby', [])
        
        if is_rediscovery:
            overlapping = scientific_output.get('overlapping_known_site')
            print(f"  🎯 REDESCUBRIMIENTO: {overlapping['name']}", flush=True)
        elif nearby:
            print(f"  📍 Sitios conocidos cercanos: {len(nearby)}", flush=True)
            for site in nearby[:3]:
                print(f"    • {site['name']} ({site['distance_km']:.1f}km)", flush=True)
        else:
            print(f"  ℹ️ No hay sitios arqueológicos conocidos cercanos", flush=True)
        
        # FASE G
        print(f"\n📋 FASE G: SALIDA CIENTÍFICA", flush=True)
        print(f"  Anomaly score final: {scientific_output.get('anomaly_score', 0):.3f}", flush=True)
        print(f"  Probabilidad antropogénica final: {scientific_output.get('anthropic_probability', 0):.3f}", flush=True)
        print(f"  Tipo de candidato: {scientific_output.get('candidate_type', 'unknown')}", flush=True)
        print(f"  Confianza científica: {scientific_output.get('scientific_confidence', 'unknown')}", flush=True)
        print(f"  Acción recomendada: {scientific_output.get('recommended_action', 'unknown')}", flush=True)
        print(f"  Notas: {scientific_output.get('notes', 'N/A')}", flush=True)
        
        # ETIQUETADO EPISTEMOLÓGICO
        print(f"\n🔬 ETIQUETADO EPISTEMOLÓGICO", flush=True)
        print(f"  Modo epistémico: {scientific_output.get('epistemic_mode', 'unknown')}", flush=True)
        print(f"  IA utilizada: {scientific_output.get('ai_used', False)}", flush=True)
        print(f"  Reproducible: {scientific_output.get('reproducible', False)}", flush=True)
        print(f"  Transparencia: {scientific_output.get('method_transparency', 'unknown')}", flush=True)
        
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
    asyncio.run(analyze_patagonia_complete())
