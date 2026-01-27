#!/usr/bin/env python3
"""
Analizar Acre Brasil - Geoglifos Amazónicos con pipeline científico completo.
"""

import asyncio
import asyncpg
import requests
import json

API_BASE = "http://localhost:8002"

async def analyze_acre():
    """Analizar Acre Brasil."""
    
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    print("="*80, flush=True)
    print("ANÁLISIS: ACRE BRASIL - GEOGLIFOS AMAZÓNICOS", flush=True)
    print("="*80, flush=True)
    
    # Datos del candidato
    analysis_id = "7181a57d-0061-44a6-997d-f6440525e2e1"
    region_name = "Acre Brasil - Geoglifos Amazonicos"
    lat = -9.8
    lon = -67.8
    
    print(f"\nCANDIDATO: {region_name}", flush=True)
    print(f"Coordenadas: {lat:.4f}, {lon:.4f}", flush=True)
    print(f"Analysis ID: {analysis_id}", flush=True)
    
    # Ver mediciones existentes
    measurements = await conn.fetch("""
        SELECT instrument_name, value, data_mode
        FROM measurements
        WHERE analysis_id = $1
        ORDER BY instrument_name
        LIMIT 10
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
        scientific_output = resultado.get('scientific_output', {})
        environment = resultado.get('environment_context', {})
        
        print(f"\n{'='*80}", flush=True)
        print("RESULTADO", flush=True)
        print(f"{'='*80}", flush=True)
        print(f"Ambiente: {environment.get('environment_type')}", flush=True)
        print(f"Anomaly score: {scientific_output.get('anomaly_score', 0):.3f}", flush=True)
        print(f"Probabilidad antropogénica: {scientific_output.get('anthropic_probability', 0):.3f}", flush=True)
        print(f"Tipo candidato: {scientific_output.get('candidate_type')}", flush=True)
        print(f"Confianza científica: {scientific_output.get('scientific_confidence')}", flush=True)
        print(f"Acción: {scientific_output.get('recommended_action')}", flush=True)
        
        # Sitios conocidos
        is_rediscovery = scientific_output.get('is_known_site_rediscovery', False)
        if is_rediscovery:
            overlapping = scientific_output.get('overlapping_known_site')
            print(f"\n⚠️ REDESCUBRIMIENTO: {overlapping['name']}", flush=True)
        
        es_anomalia = scientific_output.get('anthropic_probability', 0) >= 0.5
        print(f"\n{'🎯 ANOMALÍA' if es_anomalia else '⚪ NO ANOMALÍA'}", flush=True)
        
        await conn.close()
        
    except Exception as e:
        print(f"\n[ERROR] {e}", flush=True)
        import traceback
        traceback.print_exc()
        await conn.close()

if __name__ == "__main__":
    asyncio.run(analyze_acre())
