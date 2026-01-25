#!/usr/bin/env python3
"""
ArcheoScope - Complete Archaeological Sites Harvester
UNESCO + Wikidata + OpenStreetMap
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Any

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

def harvest_osm_region(bbox: tuple, region_name: str) -> List[Dict[str, Any]]:
    """Recopilar sitios de OpenStreetMap en una región"""
    min_lat, min_lon, max_lat, max_lon = bbox
    
    query = f"""
    [out:json][timeout:60];
    (
      node["historic"="archaeological_site"]({min_lat},{min_lon},{max_lat},{max_lon});
      way["historic"="archaeological_site"]({min_lat},{min_lon},{max_lat},{max_lon});
      relation["historic"="archaeological_site"]({min_lat},{min_lon},{max_lat},{max_lon});
    );
    out center;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    
    try:
        response = requests.post(url, data={'data': query}, timeout=90)
        
        if response.status_code == 200:
            data = response.json()
            sites = []
            
            for element in data.get('elements', []):
                lat = element.get('lat') or element.get('center', {}).get('lat')
                lon = element.get('lon') or element.get('center', {}).get('lon')
                
                if lat and lon:
                    tags = element.get('tags', {})
                    sites.append({
                        'source': 'OpenStreetMap',
                        'name': tags.get('name', f"OSM Site {element.get('id')}"),
                        'country': tags.get('addr:country', ''),
                        'latitude': float(lat),
                        'longitude': float(lon),
                        'site_type': tags.get('site_type', ''),
                        'heritage': tags.get('heritage', ''),
                        'osm_id': element.get('id')
                    })
            
            return sites
    except Exception as e:
        print(f"   ⚠️  Error OSM {region_name}: {e}")
    
    return []

def harvest_osm_global() -> List[Dict[str, Any]]:
    """Recopilar sitios de OpenStreetMap por regiones"""
    print("🗺️  Recopilando OpenStreetMap Archaeological Sites...")
    
    regions = [
        ((-56, -82, -34, -53), "South America South"),
        ((-34, -75, -20, -47), "South America Central"),
        ((-20, -70, 0, -47), "South America North"),
        ((0, -92, 18, -77), "Central America"),
        ((10, -85, 22, -59), "Caribbean"),
        ((14, -118, 33, -80), "Mexico & Southern USA"),
        ((33, -125, 49, -95), "USA Central"),
        ((33, -95, 49, -66), "USA East"),
        ((49, -141, 70, -95), "Canada West"),
        ((49, -95, 70, -52), "Canada East"),
        ((15, -18, 38, 12), "North Africa West"),
        ((15, 12, 38, 40), "North Africa East"),
        ((-35, 10, 15, 30), "Africa Central"),
        ((-35, 30, 15, 52), "Africa East"),
        ((36, -10, 48, 5), "Iberia & France South"),
        ((48, -5, 60, 10), "France, UK, Benelux"),
        ((45, 5, 55, 15), "Germany & Alps"),
        ((55, -10, 72, 30), "Scandinavia"),
        ((36, 10, 48, 30), "Italy & Balkans"),
        ((48, 15, 60, 40), "Eastern Europe"),
        ((60, 20, 72, 60), "Baltic & Russia West"),
        ((12, 30, 42, 50), "Middle East"),
        ((30, 50, 42, 65), "Iran & Caucasus"),
        ((35, 50, 55, 75), "Central Asia"),
        ((8, 68, 35, 88), "India & Pakistan"),
        ((0, 95, 20, 108), "Thailand & Indochina"),
        ((-11, 95, 7, 141), "Indonesia"),
        ((18, 100, 42, 122), "China South"),
        ((35, 100, 54, 135), "China North"),
        ((30, 128, 46, 146), "Japan & Korea"),
        ((-48, 112, -10, 155), "Australia"),
    ]
    
    all_sites = []
    
    for i, (bbox, region_name) in enumerate(regions, 1):
        print(f"   📍 [{i}/{len(regions)}] {region_name}...")
        sites = harvest_osm_region(bbox, region_name)
        all_sites.extend(sites)
        print(f"      → {len(sites)} sitios")
        time.sleep(2)  # Rate limiting
    
    print(f"   ✅ OpenStreetMap: {len(all_sites)} sitios recopilados")
    return all_sites

def grid_deduplicate(sites: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplicación rápida por grid (~1km)"""
    print(f"\n🔍 Deduplicando {len(sites)} sitios...")
    
    grid = {}
    unique_sites = []
    
    for i, site in enumerate(sites):
        if i % 10000 == 0 and i > 0:
            print(f"   ⏳ Procesados {i}/{len(sites)}...")
        
        try:
            # Grid de 0.01 grados (~1km)
            lat = round(site['latitude'], 2)
            lon = round(site['longitude'], 2)
            key = (lat, lon)
            
            if key not in grid:
                grid[key] = site
                unique_sites.append(site)
            else:
                # Enriquecer con múltiples fuentes
                existing = grid[key]
                if 'sources' not in existing:
                    existing['sources'] = [existing['source']]
                if site['source'] not in existing['sources']:
                    existing['sources'].append(site['source'])
                
                # Preferir UNESCO
                if site['source'] == 'UNESCO':
                    grid[key] = site
                    unique_sites[unique_sites.index(existing)] = site
        except:
            continue
    
    print(f"   ✅ Sitios únicos: {len(unique_sites)}")
    return unique_sites

def assign_confidence(sites: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Asignar confianza"""
    for site in sites:
        if 'sources' in site:
            if 'UNESCO' in site['sources']:
                site['confidence_level'] = 'confirmed'
            elif 'Wikidata' in site['sources']:
                site['confidence_level'] = 'high'
            else:
                site['confidence_level'] = 'moderate'
        else:
            conf_map = {'UNESCO': 'confirmed', 'Wikidata': 'high', 'OpenStreetMap': 'moderate'}
            site['confidence_level'] = conf_map.get(site['source'], 'moderate')
    return sites

def save_results(sites: List[Dict[str, Any]], filename='harvested_complete.json'):
    """Guardar resultados"""
    
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
    
    top_countries = sorted(country_stats.items(), key=lambda x: x[1], reverse=True)[:30]
    
    output = {
        'metadata': {
            'harvested_at': datetime.now().isoformat(),
            'total_sites': len(sites),
            'sources': list(source_stats.keys()),
            'source_statistics': source_stats,
            'confidence_statistics': confidence_stats,
            'top_30_countries': dict(top_countries),
            'version': '1.0.0',
            'description': 'Complete archaeological sites database from UNESCO, Wikidata, and OpenStreetMap'
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
║   ArcheoScope - Complete Archaeological Harvester           ║
║   UNESCO + Wikidata + OpenStreetMap                         ║
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
    
    # OpenStreetMap
    osm_sites = harvest_osm_global()
    all_sites.extend(osm_sites)
    
    print(f"\n{'='*70}")
    print(f"📊 RESUMEN ANTES DE DEDUPLICAR")
    print(f"{'='*70}")
    print(f"Total: {len(all_sites)}")
    print(f"  - UNESCO: {len(unesco_sites)}")
    print(f"  - Wikidata: {len(wikidata_sites)}")
    print(f"  - OpenStreetMap: {len(osm_sites)}")
    
    # Deduplicar
    unique_sites = grid_deduplicate(all_sites)
    
    # Asignar confianza
    unique_sites = assign_confidence(unique_sites)
    
    # Guardar
    result = save_results(unique_sites)
    
    print(f"\n{'='*70}")
    print(f"✅ COMPLETADO")
    print(f"{'='*70}")
    print(f"🎯 Total sitios únicos: {result['metadata']['total_sites']:,}")
    print(f"\n📍 Por fuente:")
    for source, count in result['metadata']['source_statistics'].items():
        print(f"   • {source}: {count:,}")
    print(f"\n🎯 Por confianza:")
    for conf, count in result['metadata']['confidence_statistics'].items():
        print(f"   • {conf}: {count:,}")
    print(f"\n🌍 Top 10 países:")
    for i, (country, count) in enumerate(list(result['metadata']['top_30_countries'].items())[:10], 1):
        print(f"   {i}. {country}: {count:,}")
    
    print(f"\n✅ ¡Recopilación completada!")
    print(f"\n💡 Siguiente paso:")
    print(f"   python scripts/migrate_json_to_postgres.py")

if __name__ == "__main__":
    main()
