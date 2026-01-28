#!/usr/bin/env python3
"""
RECLASIFICAR SITIOS ARQUEOLÓGICOS CONOCIDOS

Objetivo:
- Tomar los 69 sitios del enriquecimiento masivo
- Re-analizarlos con las métricas separadas nuevas
- Verificar que origen > 70% para sitios históricos
- Actualizar clasificación en BD
"""

import requests
import json
import time
from typing import Dict, List

API_BASE_URL = "http://localhost:8002"

def load_sites_from_enrichment() -> List[Dict]:
    """Cargar sitios del enriquecimiento masivo."""
    with open('massive_enrichment_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Extraer solo sitios exitosos
    sites = []
    for r in results:
        if r.get('success'):
            sites.append(r['site'])
    
    return sites

def analyze_with_new_metrics(site: Dict) -> Dict:
    """Analizar sitio con métricas separadas."""
    
    request_data = {
        "lat_min": site['lat'] - 0.01,
        "lat_max": site['lat'] + 0.01,
        "lon_min": site['lon'] - 0.01,
        "lon_max": site['lon'] + 0.01,
        "region_name": f"{site['name']}, {site['country']}"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/scientific/analyze",
            json=request_data,
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            sci = result.get('scientific_output', {})
            
            return {
                'success': True,
                'origin': sci.get('anthropic_origin_probability', 0),
                'activity': sci.get('anthropic_activity_probability', 0),
                'anomaly': sci.get('instrumental_anomaly_probability', 0),
                'legacy_prob': sci.get('anthropic_probability', 0),
                'ess': sci.get('explanatory_strangeness', 'none'),
                'ess_score': sci.get('strangeness_score', 0),
                'confidence': sci.get('model_inference_confidence', 'unknown'),
                'action': sci.get('recommended_action', 'unknown')
            }
        else:
            return {'success': False, 'error': f'HTTP {response.status_code}'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    print("="*70)
    print("🔄 RECLASIFICACIÓN DE SITIOS ARQUEOLÓGICOS CONOCIDOS")
    print("="*70)
    
    # Cargar sitios
    sites = load_sites_from_enrichment()
    print(f"\n📊 Sitios a reclasificar: {len(sites)}")
    
    # Verificar backend
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Backend no disponible")
            return
        print("✅ Backend disponible\n")
    except Exception as e:
        print(f"❌ Backend no disponible: {e}")
        return
    
    # Analizar muestra (primeros 10 para verificar)
    sample_size = 10
    print(f"🔬 Analizando muestra de {sample_size} sitios...\n")
    
    results = []
    
    for i, site in enumerate(sites[:sample_size], 1):
        print(f"[{i}/{sample_size}] {site['name']}, {site['country']}")
        
        metrics = analyze_with_new_metrics(site)
        
        if metrics['success']:
            print(f"  ✅ Origen: {metrics['origin']:.1%} | "
                  f"Actividad: {metrics['activity']:.1%} | "
                  f"Anomalía: {metrics['anomaly']:.1%}")
            print(f"     Legacy: {metrics['legacy_prob']:.1%} | "
                  f"ESS: {metrics['ess'].upper()} ({metrics['ess_score']:.3f})")
            
            # Verificar si cumple umbrales
            origin_ok = metrics['origin'] >= 0.70
            activity_ok = metrics['activity'] <= 0.20
            anomaly_ok = metrics['anomaly'] <= 0.05
            
            status = "✅ PASS" if (origin_ok and activity_ok and anomaly_ok) else "⚠️ REVISAR"
            print(f"     {status}")
            
            results.append({
                'site': site,
                'metrics': metrics,
                'pass': origin_ok and activity_ok and anomaly_ok
            })
        else:
            print(f"  ❌ Error: {metrics.get('error')}")
            results.append({
                'site': site,
                'metrics': metrics,
                'pass': False
            })
        
        print()
        time.sleep(2)
    
    # Resumen
    print("="*70)
    print("📊 RESUMEN DE RECLASIFICACIÓN")
    print("="*70)
    
    success_count = sum(1 for r in results if r['metrics']['success'])
    pass_count = sum(1 for r in results if r['pass'])
    
    print(f"\nAnalizados: {success_count}/{sample_size}")
    print(f"Pasan umbrales: {pass_count}/{success_count}")
    
    if success_count > 0:
        origins = [r['metrics']['origin'] for r in results if r['metrics']['success']]
        activities = [r['metrics']['activity'] for r in results if r['metrics']['success']]
        legacy_probs = [r['metrics']['legacy_prob'] for r in results if r['metrics']['success']]
        
        print(f"\n📈 MÉTRICAS PROMEDIO:")
        print(f"   Origen: {sum(origins)/len(origins):.1%}")
        print(f"   Actividad: {sum(activities)/len(activities):.1%}")
        print(f"   Legacy prob: {sum(legacy_probs)/len(legacy_probs):.1%}")
        
        # Sitios que no pasan
        failed = [r for r in results if not r['pass'] and r['metrics']['success']]
        if failed:
            print(f"\n⚠️ SITIOS QUE REQUIEREN AJUSTE ({len(failed)}):")
            for r in failed:
                site = r['site']
                m = r['metrics']
                print(f"   {site['name']}: origen={m['origin']:.1%} (esperado ≥70%)")
    
    # Guardar resultados
    with open('reclassification_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: reclassification_results.json")

if __name__ == "__main__":
    main()
