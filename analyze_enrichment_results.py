#!/usr/bin/env python3
"""
Analizar resultados del enriquecimiento masivo.
"""

import json
from collections import Counter

# Cargar resultados
with open('massive_enrichment_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print("="*70)
print("📊 ANÁLISIS DE RESULTADOS - ENRIQUECIMIENTO MASIVO")
print("="*70)

# Estadísticas básicas
total = len(results)
success = sum(1 for r in results if r.get('success', False))
failed = total - success

print(f"\n📈 ESTADÍSTICAS GENERALES:")
print(f"   Total sitios: {total}")
print(f"   Exitosos: {success}")
print(f"   Fallidos: {failed}")

if success > 0:
    # Análisis de ESS
    ess_counts = Counter(r.get('ess', 'none') for r in results if r.get('success'))
    ess_scores = [r.get('ess_score', 0) for r in results if r.get('success')]
    
    print(f"\n🔬 EXPLANATORY STRANGENESS SCORE (ESS):")
    print(f"   Very High: {ess_counts.get('very_high', 0)}")
    print(f"   High: {ess_counts.get('high', 0)}")
    print(f"   Medium: {ess_counts.get('medium', 0)}")
    print(f"   Low: {ess_counts.get('low', 0)}")
    print(f"   None: {ess_counts.get('none', 0)}")
    print(f"   Score promedio: {sum(ess_scores)/len(ess_scores):.3f}")
    
    # Sitios por país
    countries = Counter(r['site']['country'] for r in results if r.get('success'))
    print(f"\n🌍 SITIOS POR PAÍS:")
    for country, count in countries.most_common():
        print(f"   {country}: {count}")
    
    # Sitios con ESS alto
    high_ess = [r for r in results if r.get('success') and r.get('ess') in ['high', 'very_high']]
    print(f"\n🏛️ SITIOS CON ESS ALTO/MUY ALTO ({len(high_ess)}):")
    for r in high_ess[:10]:  # Primeros 10
        site = r['site']
        print(f"   {site['name']}, {site['country']}: ESS={r['ess'].upper()} ({r['ess_score']:.3f})")

print(f"\n{'='*70}")
print("✅ Análisis completado")
print(f"{'='*70}")
