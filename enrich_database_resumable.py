#!/usr/bin/env python3
"""
Enriquecimiento MASIVO de BD - VERSIÓN RESUMIBLE

Mejoras:
- Guarda progreso incremental cada 5 sitios
- Puede reanudar desde donde se quedó
- Maneja timeouts y errores gracefully
- Muestra progreso en tiempo real
"""

import requests
import json
import time
from typing import Dict, List
import sys
from pathlib import Path

API_BASE_URL = "http://localhost:8002"
RESULTS_FILE = "massive_enrichment_progress.json"
BATCH_SIZE = 5  # Guardar cada 5 sitios

# MEGA LISTA DE SITIOS (100+)
ARCHAEOLOGICAL_SITES = [
    # EGIPTO (10)
    {"name": "Pirámides de Giza", "country": "Egipto", "lat": 29.9792, "lon": 31.1342},
    {"name": "Valle de los Reyes", "country": "Egipto", "lat": 25.7402, "lon": 32.6014},
    {"name": "Karnak", "country": "Egipto", "lat": 25.7188, "lon": 32.6573},
    {"name": "Abu Simbel", "country": "Egipto", "lat": 22.3372, "lon": 31.6258},
    {"name": "Luxor", "country": "Egipto", "lat": 25.6872, "lon": 32.6396},
    {"name": "Saqqara", "country": "Egipto", "lat": 29.8714, "lon": 31.2166},
    {"name": "Dendera", "country": "Egipto", "lat": 26.1417, "lon": 32.6703},
    {"name": "Edfu", "country": "Egipto", "lat": 24.9778, "lon": 32.8736},
    {"name": "Kom Ombo", "country": "Egipto", "lat": 24.4517, "lon": 32.9317},
    {"name": "Philae", "country": "Egipto", "lat": 24.0253, "lon": 32.8844},
    
    # PERÚ (10)
    {"name": "Machu Picchu", "country": "Perú", "lat": -13.1631, "lon": -72.5450},
    {"name": "Líneas de Nazca", "country": "Perú", "lat": -14.7390, "lon": -75.1300},
    {"name": "Cusco", "country": "Perú", "lat": -13.5319, "lon": -71.9675},
    {"name": "Ollantaytambo", "country": "Perú", "lat": -13.2572, "lon": -72.2653},
    {"name": "Sacsayhuamán", "country": "Perú", "lat": -13.5089, "lon": -71.9819},
    {"name": "Chan Chan", "country": "Perú", "lat": -8.1061, "lon": -79.0747},
    {"name": "Chavín de Huántar", "country": "Perú", "lat": -9.5944, "lon": -77.1772},
    {"name": "Caral", "country": "Perú", "lat": -10.8933, "lon": -77.5203},
]

def load_progress() -> Dict:
    """Cargar progreso previo si existe."""
    if Path(RESULTS_FILE).exists():
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"completed": [], "failed": [], "last_index": 0}

def save_progress(progress: Dict):
    """Guardar progreso actual."""
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def analyze_site(site: Dict, index: int, total: int) -> Dict:
    """Analizar un sitio individual."""
    print(f"\n{'='*70}")
    print(f"[{index}/{total}] 🏛️ {site['name']}, {site['country']}")
    print(f"{'='*70}")
    
    try:
        request_data = {
            "lat_min": site['lat'] - 0.01,
            "lat_max": site['lat'] + 0.01,
            "lon_min": site['lon'] - 0.01,
            "lon_max": site['lon'] + 0.01,
            "region_name": f"{site['name']}, {site['country']}"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/scientific/analyze",
            json=request_data,
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            sci = result.get('scientific_output', {})
            phase_d = result.get('phase_d_anthropic', {})
            
            # Extraer métricas
            origin = sci.get('anthropic_origin_probability', 0)
            activity = sci.get('anthropic_activity_probability', 0)
            anomaly = sci.get('instrumental_anomaly_probability', 0)
            legacy_prob = sci.get('anthropic_probability', 0)
            ess = sci.get('explanatory_strangeness', 'none')
            ess_score = sci.get('strangeness_score', 0)
            
            print(f"✅ MÉTRICAS SEPARADAS:")
            print(f"   Origen:    {origin:.1%}")
            print(f"   Actividad: {activity:.1%}")
            print(f"   Anomalía:  {anomaly:.1%}")
            print(f"   Legacy:    {legacy_prob:.1%}")
            print(f"   ESS:       {ess.upper()} ({ess_score:.3f})")
            
            return {
                'site': site,
                'success': True,
                'metrics': {
                    'origin': origin,
                    'activity': activity,
                    'anomaly': anomaly,
                    'legacy_prob': legacy_prob,
                    'ess': ess,
                    'ess_score': ess_score
                }
            }
        else:
            print(f"❌ Error HTTP {response.status_code}")
            return {'site': site, 'success': False, 'error': f'HTTP {response.status_code}'}
            
    except requests.Timeout:
        print(f"⏱️ Timeout (>90s)")
        return {'site': site, 'success': False, 'error': 'timeout'}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {'site': site, 'success': False, 'error': str(e)}

def main():
    print("\n" + "="*70)
    print("🏛️ ENRIQUECIMIENTO MASIVO - VERSIÓN RESUMIBLE")
    print("="*70)
    
    # Cargar progreso
    progress = load_progress()
    start_idx = progress['last_index']
    
    print(f"\nTotal sitios: {len(ARCHAEOLOGICAL_SITES)}")
    print(f"Completados: {len(progress['completed'])}")
    print(f"Fallidos: {len(progress['failed'])}")
    print(f"Reanudando desde: {start_idx + 1}")
    
    # Verificar backend
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=5)
        if response.status_code == 200:
            print("✅ Backend disponible\n")
        else:
            print("❌ Backend no responde")
            return
    except:
        print("❌ Backend no disponible")
        return
    
    # Procesar sitios
    for i in range(start_idx, len(ARCHAEOLOGICAL_SITES)):
        site = ARCHAEOLOGICAL_SITES[i]
        
        result = analyze_site(site, i + 1, len(ARCHAEOLOGICAL_SITES))
        
        if result['success']:
            progress['completed'].append(result)
        else:
            progress['failed'].append(result)
        
        progress['last_index'] = i + 1
        
        # Guardar cada BATCH_SIZE sitios
        if (i + 1) % BATCH_SIZE == 0:
            save_progress(progress)
            print(f"\n💾 Progreso guardado ({i + 1}/{len(ARCHAEOLOGICAL_SITES)})")
        
        # Pausa entre requests
        if i < len(ARCHAEOLOGICAL_SITES) - 1:
            time.sleep(2)
    
    # Guardar final
    save_progress(progress)
    
    # Resumen
    print(f"\n{'='*70}")
    print("📊 RESUMEN FINAL")
    print(f"{'='*70}")
    print(f"Completados: {len(progress['completed'])}/{len(ARCHAEOLOGICAL_SITES)}")
    print(f"Fallidos: {len(progress['failed'])}")
    
    if progress['completed']:
        # Estadísticas de métricas
        origins = [r['metrics']['origin'] for r in progress['completed']]
        activities = [r['metrics']['activity'] for r in progress['completed']]
        ess_high = sum(1 for r in progress['completed'] if r['metrics']['ess'] in ['high', 'very_high'])
        
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   Origen promedio: {sum(origins)/len(origins):.1%}")
        print(f"   Actividad promedio: {sum(activities)/len(activities):.1%}")
        print(f"   ESS alto/muy alto: {ess_high}/{len(progress['completed'])}")
    
    print(f"\n💾 Resultados en: {RESULTS_FILE}")

if __name__ == "__main__":
    main()
