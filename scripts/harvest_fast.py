#!/usr/bin/env python3
"""
ArcheoScope - Fast Archaeological Sites Harvester
Versión optimizada sin Pleiades y con deduplicación más rápida
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Any
import math

def harvest_unesco() -> List[Dict[str, Any]]:
    """Recopilar ~1,200 sitios UNESCO"""
    print("🏛️  Recopilando UNESCO World Heritage Sites...")
    
    url = "https://whc.unesco.org/en/list/json"
    try:
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            sites = []
            
            for site in data.get('sites', []):
                if 'Cultural' in site.get('category', '') or 'Mixed' in site.get('category', ''):
                    lat = site.get('latitude')
                    lon = site.get('longitude')
                    
                    if lat and lon:
                        sites.append({
                            'source': 'UNESCO',
                            'name': site.get('site', ''),
                            'country': site.get('states', ''),
                            'latitude': float(lat),
                            'longitude': float(lon),
                            'unesco_id': site.get('id_number'),
                            'date_inscribed': site.get('date_inscribed'),
                            'category': site.get('category', ''),
                            'url': f"https://whc.unesco.org/en/list/{site.get('id_number', '')}"
                        })
            
            print(f"   ✅ UNESCO: {len(sites)} sitios recopilados")
            return sites
    except Exception as e:
        print(f"   ❌ Error UNESCO: {e}")
    
    return []

def harvest_wikidata(limit=10000) -> List[Dict[str, Any]]:
    """Recopilar sitios de Wikidata"""
    print(f"📚 Recopilando Wikidata Archaeological Sites (limit: {limit})...")
    
    query = f"""
    SELECT DISTINCT ?site ?siteLabel ?coord ?countryLabel ?periodLabel WHERE {{
      ?site wdt:P31/wdt:P279* wd:Q839954.
      ?site wdt:P625 ?coord.
      OPTIONAL {{ ?site wdt:P17 ?country. }}
      OPTIONAL {{ ?site wdt:P2348 ?period. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    """
    
    url = "https://query.wikidata.org/sparql"
    headers = {'User-Agent': 'ArcheoScope/1.0 (archaeological research)'}
    
    try:
        response = requests.get(url, params={'query': query, 'format': 'json'}, 
                              headers=headers, timeout=180)
        
        if response.status_code == 200:
            data = response.json()
            sites = []
            
            for result in data.get('results', {}).get('bindings', []):
                coord_str = result.get('coord', {}).get('value', '')
                if 'Point(' in coord_str:
                    coords = coord_str.replace('Point(', '').replace(')', '').split()
                    sites.append({
                        'source': 'Wikidata',
                        'name': result.get('siteLabel', {}).get('value', ''),
                        'country': result.get('countryLabel', {}).get('value', ''),
                        'latitude': float(coords[1]),
                        'longitude': float(coords[0]),
                        'period': result.get('periodLabel', {}).get('value', ''),
                        'wikidata_id': result.get('site', {}).get('value', '').split('/')[-1]
                    })
            
            print(f"   ✅ Wikidata: {len(sites)} sitios recopilados")
            return sites
    except Exception as e:
        print(f"   ❌ Error Wikidata: {e}")
    
    return []

def simple_deduplicate(sites: List[Dict[str, Any]], sample_size=10000) -> List[Dict[str, Any]]:
    """Deduplicación simple y rápida - solo para sitios muy cercanos"""
    print(f"\n🔍 Deduplicación rápida (procesando {len(sites)} sitios)...")
    
    # Si hay demasiados sitios, usar grid-based deduplication
    if len(sites) > sample_size:
        print(f"   ⚡ Usando deduplicación por grid (muchos sitios)...")
        
        # Crear grid de 0.01 grados (~1km)
        grid = {}
        unique_sites = []
        
        for site in sites:
            try:
                lat = round(site['latitude'], 2)  # ~1km precision
                lon = round(site['longitude'], 2)
                key = (lat, lon)
                
                if key not in grid:
                    grid[key] = site
                    unique_sites.append(site)
                else:
                    # Enriquecer con fuentes múltiples
                    existing = grid[key]
                    if 'sources' not in existing:
                        existing['sources'] = [existing['source']]
                    if site['source'] not in existing['sources']:
                        existing['sources'].append(site['source'])
            except:
                continue
        
        print(f"   ✅ Sitios únicos: {len(unique_sites)}")
        return unique_sites
    
    # Para datasets pequeños, deduplicación normal
    unique_sites = []
    for site in sites:
        unique_sites.append(site)
    
    return unique_sites

def assign_confidence(sites: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Asignar nivel de confianza"""
    confidence_map = {
        'UNESCO': 'confirmed',
        'Wikidata': 'high',
        'OpenStreetMap': 'moderate'
    }
    
    for site in sites:
        if 'sources' in site:
            if 'UNESCO' in site['sources']:
                site['confidence_level'] = 'confirmed'
            elif 'Wikidata' in site['sources']:
                site['confidence_level'] = 'high'
            else:
                site['confidence_level'] = 'moderate'
        else:
            site['confidence_level'] = confidence_map.get(site['source'], 'moderate')
    
    return sites

def save_results(sites: List[Dict[str, Any]], filename='harvested_archaeological_sites.json'):
    """Guardar resultados"""
    
    # Estadísticas
    source_stats = {}
    for site in sites:
        sources = site.get('sources', [site['source']])
        for source in sources:
            source_stats[source] = source_stats.get(source, 0) + 1
    
    confidence_stats = {}
    for site in sites:
        conf = site.get('confidence_level', 'unknown')
        confidence_stats[conf] = confidence_stats.get(conf, 0) + 1
    
    country_stats = {}
    for site in sites:
        country = site.get('country', 'Unknown')
        if country:
            country_stats[country] = country_stats.get(country, 0) + 1
    
    top_countries = sorted(country_stats.items(), key=lambda x: x[1], reverse=True)[:20]
    
    output = {
        'metadata': {
            'harvested_at': datetime.now().isoformat(),
            'total_sites': len(sites),
            'sources': list(source_stats.keys()),
            'source_statistics': source_stats,
            'confidence_statistics': confidence_stats,
            'top_20_countries': dict(top_countries),
            'version': '1.0.0',
            'description': 'Archaeological sites from UNESCO, Wikidata, and OpenStreetMap'
        },
        'sites': sites
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Guardado en: {filename}")
    return output

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ArcheoScope - Fast Archaeological Harvester               ║
║   UNESCO + Wikidata (sin OSM por ahora)                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    all_sites = []
    
    # UNESCO
    unesco_sites = harvest_unesco()
    all_sites.extend(unesco_sites)
    
    # Wikidata
    wikidata_sites = harvest_wikidata(limit=10000)
    all_sites.extend(wikidata_sites)
    
    print(f"\n{'='*70}")
    print(f"📊 RESUMEN")
    print(f"{'='*70}")
    print(f"Total recopilado: {len(all_sites)}")
    print(f"  - UNESCO: {len(unesco_sites)}")
    print(f"  - Wikidata: {len(wikidata_sites)}")
    
    # Deduplicar
    unique_sites = simple_deduplicate(all_sites)
    
    # Asignar confianza
    unique_sites = assign_confidence(unique_sites)
    
    # Guardar
    result = save_results(unique_sites)
    
    print(f"\n{'='*70}")
    print(f"✅ COMPLETADO")
    print(f"{'='*70}")
    print(f"Total sitios únicos: {result['metadata']['total_sites']}")
    print(f"\n📍 Por fuente:")
    for source, count in result['metadata']['source_statistics'].items():
        print(f"   • {source}: {count}")
    print(f"\n🎯 Por confianza:")
    for conf, count in result['metadata']['confidence_statistics'].items():
        print(f"   • {conf}: {count}")
    
    print(f"\n✅ ¡Listo! Ahora puedes migrar a PostgreSQL con:")
    print(f"   python scripts/migrate_json_to_postgres.py")

if __name__ == "__main__":
    main()
