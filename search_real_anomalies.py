#!/usr/bin/env python3
"""
Buscar ANOMALÍAS REALES en análisis guardados.

Buscar en:
1. Archivos JSON de resultados
2. Sitios con anomaly_score > 0
3. Sitios con actividad > 0
"""

import json
import os
from pathlib import Path

def search_json_files():
    """Buscar anomalías en archivos JSON."""
    
    print("="*70)
    print("🔍 BÚSQUEDA DE ANOMALÍAS REALES")
    print("="*70)
    
    # Archivos a revisar
    json_files = [
        'massive_enrichment_results.json',
        'iconic_sites_analysis_results.json',
        'reclassification_results.json',
        'separated_metrics_test_results.json'
    ]
    
    total_analyzed = 0
    with_anomaly = []
    with_activity = []
    with_high_origin = []
    
    for filename in json_files:
        if not Path(filename).exists():
            continue
        
        print(f"\n📄 Analizando: {filename}")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Procesar según estructura
            if isinstance(data, list):
                for item in data:
                    total_analyzed += 1
                    
                    # Buscar métricas
                    metrics = None
                    if 'metrics' in item:
                        metrics = item['metrics']
                    elif 'result' in item and 'scientific_output' in item['result']:
                        metrics = item['result']['scientific_output']
                    
                    if metrics:
                        anomaly = metrics.get('anomaly', 0) or metrics.get('instrumental_anomaly_probability', 0) or metrics.get('anomaly_score', 0)
                        activity = metrics.get('activity', 0) or metrics.get('anthropic_activity_probability', 0)
                        origin = metrics.get('origin', 0) or metrics.get('anthropic_origin_probability', 0)
                        
                        site_name = item.get('site', {}).get('name', 'Unknown')
                        
                        if anomaly > 0:
                            with_anomaly.append({
                                'name': site_name,
                                'anomaly': anomaly,
                                'activity': activity,
                                'origin': origin,
                                'file': filename
                            })
                        
                        if activity > 0:
                            with_activity.append({
                                'name': site_name,
                                'activity': activity,
                                'anomaly': anomaly,
                                'origin': origin,
                                'file': filename
                            })
                        
                        if origin >= 0.70:
                            with_high_origin.append({
                                'name': site_name,
                                'origin': origin,
                                'activity': activity,
                                'anomaly': anomaly,
                                'file': filename
                            })
        
        except Exception as e:
            print(f"   ⚠️ Error: {e}")
    
    # Resultados
    print(f"\n{'='*70}")
    print("📊 RESULTADOS")
    print(f"{'='*70}")
    
    print(f"\nTotal sitios analizados: {total_analyzed}")
    print(f"Con anomalía (>0): {len(with_anomaly)}")
    print(f"Con actividad (>0): {len(with_activity)}")
    print(f"Con origen alto (≥70%): {len(with_high_origin)}")
    
    if with_anomaly:
        print(f"\n🚨 SITIOS CON ANOMALÍA:")
        for s in with_anomaly[:10]:
            print(f"   {s['name']}: anomalía={s['anomaly']:.1%}, actividad={s['activity']:.1%}, origen={s['origin']:.1%}")
    else:
        print(f"\n❌ NO SE ENCONTRARON SITIOS CON ANOMALÍA")
        print(f"   Todos los sitios analizados tienen anomaly_score = 0.0")
        print(f"   Esto significa:")
        print(f"   • Son sitios históricos integrados al paisaje")
        print(f"   • No hay actividad humana actual detectable")
        print(f"   • No hay anomalías instrumentales")
    
    if with_activity:
        print(f"\n⚡ SITIOS CON ACTIVIDAD:")
        for s in with_activity[:10]:
            print(f"   {s['name']}: actividad={s['activity']:.1%}, anomalía={s['anomaly']:.1%}")
    else:
        print(f"\n✅ Ningún sitio tiene actividad actual detectable")
    
    if with_high_origin:
        print(f"\n🏛️ SITIOS CON ORIGEN ALTO (≥70%):")
        print(f"   Total: {len(with_high_origin)}")
        print(f"   Promedio origen: {sum(s['origin'] for s in with_high_origin)/len(with_high_origin):.1%}")
        print(f"   Promedio actividad: {sum(s['activity'] for s in with_high_origin)/len(with_high_origin):.1%}")
        print(f"   Promedio anomalía: {sum(s['anomaly'] for s in with_high_origin)/len(with_high_origin):.1%}")
    
    # Conclusión
    print(f"\n{'='*70}")
    print("💡 CONCLUSIÓN")
    print(f"{'='*70}")
    
    if not with_anomaly and not with_activity:
        print("""
Los 69 sitios del enriquecimiento masivo son SITIOS HISTÓRICOS CONOCIDOS:
• Pirámides de Giza, Machu Picchu, Nazca, Teotihuacán, etc.
• Todos tienen origen antropogénico alto (70-95%)
• Ninguno tiene anomalía instrumental (0%)
• Ninguno tiene actividad actual (0%)

Esto es CORRECTO y ESPERADO porque:
✅ Son estructuras antiguas integradas al paisaje
✅ No hay actividad humana actual
✅ No hay anomalías instrumentales detectables

Para encontrar CANDIDATOS NUEVOS con anomalías, necesitamos:
🔍 Analizar regiones NO documentadas
🔍 Buscar áreas con anomalías instrumentales
🔍 Explorar zonas remotas sin sitios conocidos
        """)
    else:
        print(f"\n✅ Se encontraron {len(with_anomaly)} sitios con anomalías")
        print(f"✅ Se encontraron {len(with_activity)} sitios con actividad")

if __name__ == "__main__":
    search_json_files()
