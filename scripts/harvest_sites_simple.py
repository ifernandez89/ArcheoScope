#!/usr/bin/env python3
"""
ArcheoScope - Comprehensive Archaeological Sites Harvester
Recopila sitios de múltiples fuentes públicas globales
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

def harvest_osm_region(bbox: tuple, region_name: str) -> List[Dict[str, Any]]:
    """Recopilar sitios de OpenStreetMap en una región específica"""
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
                        'country': tags.get('addr:country', region_name),
                        'latitude': float(lat),
                        'longitude': float(lon),
                        'site_type': tags.get('site_type', ''),
                        'heritage': tags.get('heritage', ''),
                        'osm_id': element.get('id'),
                        'osm_type': element.get('type')
                    })
            
            return sites
    except Exception as e:
        print(f"   ⚠️  Error OSM {region_name}: {e}")
    
    return []

def harvest_osm_global() -> List[Dict[str, Any]]:
    """Recopilar sitios de OpenStreetMap por regiones"""
    print("🗺️  Recopilando OpenStreetMap Archaeological Sites (por regiones)...")
    
    # Dividir el mundo en regiones para no sobrecargar la API
    regions = [
        ((-90, -180, -60, -30), "South America South"),
        ((-60, -90, -30, -30), "South America Central"),
        ((-30, -120, 0, -30), "South America North"),
        ((0, -120, 30, -30), "Central America & Caribbean"),
        ((30, -130, 50, -60), "North America"),
        ((50, -180, 75, -30), "North America Arctic"),
        ((-35, -20, 40, 60), "Africa"),
        ((35, -10, 72, 60), "Europe & North Africa"),
        ((0, 60, 40, 150), "Middle East & Central Asia"),
        ((-50, 100, 0, 180), "Southeast Asia & Oceania"),
        ((0, 100, 50, 150), "East Asia"),
        ((50, 60, 75, 180), "Siberia"),
    ]
    
    all_sites = []
    
    for bbox, region_name in regions:
        print(f"   📍 Región: {region_name}...")
        sites = harvest_osm_region(bbox, region_name)
        all_sites.extend(sites)
        print(f"      → {len(sites)} sitios")
        time.sleep(2)  # Rate limiting
    
    print(f"   ✅ OpenStreetMap: {len(all_sites)} sitios recopilados")
    return all_sites

def harvest_pleiades() -> List[Dict[str, Any]]:
    """Recopilar sitios del Pleiades Gazetteer (mundo antiguo)"""
    print("🏺 Recopilando Pleiades Gazetteer (mundo clásico)...")
    
    # Pleiades ofrece un dump JSON completo
    url = "https://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz"
    
    try:
        print("   ⏳ Descargando dataset completo (puede tardar)...")
        response = requests.get(url, timeout=300, stream=True)
        
        if response.status_code == 200:
            import gzip
            import io
            
            # Descomprimir y parsear
            with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
                data = json.load(f)
            
            sites = []
            for feature in data.get('features', []):
                props = feature.get('properties', {})
                geom = feature.get('geometry')
                
                if geom and geom.get('coordinates'):
                    coords = geom['coordinates']
                    # Manejar diferentes tipos de geometría
                    if geom['type'] == 'Point':
                        lon, lat = coords
                    elif geom['type'] in ['MultiPoint', 'LineString']:
                        lon, lat = coords[0]
                    else:
                        continue
                    
                    sites.append({
                        'source': 'Pleiades',
                        'name': props.get('title', ''),
                        'country': '',  # Pleiades no siempre tiene país moderno
                        'latitude': float(lat),
                        'longitude': float(lon),
                        'period': ', '.join(props.get('timePeriods', [])),
                        'pleiades_id': props.get('id', ''),
                        'url': props.get('uri', '')
                    })
            
            print(f"   ✅ Pleiades: {len(sites)} sitios recopilados")
            return sites
    except Exception as e:
        print(f"   ❌ Error Pleiades: {e}")
    
    return []

def deduplicate_sites(sites: List[Dict[str, Any]], distance_threshold_km=1.0) -> List[Dict[str, Any]]:
    """Deduplicar sitios por proximidad geográfica y nombre similar"""
    print(f"\n🔍 Deduplicando sitios (umbral: {distance_threshold_km} km)...")
    
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calcular distancia en km entre dos coordenadas"""
        R = 6371  # Radio de la Tierra en km
        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def name_similarity(name1, name2):
        """Similitud simple de nombres (normalizado)"""
        # Manejar None y valores vacíos
        if not name1 or not name2:
            return 0.0
        
        try:
            n1 = str(name1).lower().strip()
            n2 = str(name2).lower().strip()
        except:
            return 0.0
        
        if not n1 or not n2:
            return 0.0
        
        if n1 == n2:
            return 1.0
        if n1 in n2 or n2 in n1:
            return 0.8
        
        # Jaccard similarity de palabras
        words1 = set(n1.split())
        words2 = set(n2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    unique_sites = []
    duplicates_count = 0
    
    for site in sites:
        is_duplicate = False
        
        for unique_site in unique_sites:
            distance = haversine_distance(
                site['latitude'], site['longitude'],
                unique_site['latitude'], unique_site['longitude']
            )
            
            name_sim = name_similarity(site.get('name', ''), unique_site.get('name', ''))
            
            # Considerar duplicado si está cerca Y tiene nombre similar
            if distance < distance_threshold_km and name_sim > 0.6:
                is_duplicate = True
                duplicates_count += 1
                
                # Enriquecer el sitio único con información adicional
                if 'sources' not in unique_site:
                    unique_site['sources'] = [unique_site['source']]
                
                if site['source'] not in unique_site['sources']:
                    unique_site['sources'].append(site['source'])
                
                # Preferir UNESCO ID si existe
                if 'unesco_id' in site and 'unesco_id' not in unique_site:
                    unique_site['unesco_id'] = site['unesco_id']
                
                break
        
        if not is_duplicate:
            unique_sites.append(site)
    
    print(f"   ✅ Eliminados {duplicates_count} duplicados")
    print(f"   ✅ Sitios únicos: {len(unique_sites)}")
    
    return unique_sites

def assign_confidence(sites: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Asignar nivel de confianza basado en la fuente"""
    print("\n📊 Asignando niveles de confianza...")
    
    confidence_map = {
        'UNESCO': 'confirmed',
        'Wikidata': 'high',
        'Pleiades': 'high',
        'OpenStreetMap': 'moderate'
    }
    
    for site in sites:
        # Si tiene múltiples fuentes, usar la de mayor confianza
        if 'sources' in site:
            if 'UNESCO' in site['sources']:
                site['confidence_level'] = 'confirmed'
            elif 'Pleiades' in site['sources'] or 'Wikidata' in site['sources']:
                site['confidence_level'] = 'high'
            else:
                site['confidence_level'] = 'moderate'
        else:
            site['confidence_level'] = confidence_map.get(site['source'], 'moderate')
    
    return sites

def save_results(sites: List[Dict[str, Any]], filename='harvested_sites.json'):
    """Guardar resultados con estadísticas"""
    
    # Estadísticas por fuente
    source_stats = {}
    for site in sites:
        sources = site.get('sources', [site['source']])
        for source in sources:
            source_stats[source] = source_stats.get(source, 0) + 1
    
    # Estadísticas por confianza
    confidence_stats = {}
    for site in sites:
        conf = site.get('confidence_level', 'unknown')
        confidence_stats[conf] = confidence_stats.get(conf, 0) + 1
    
    # Estadísticas por país (top 20)
    country_stats = {}
    for site in sites:
        country = site.get('country', 'Unknown')
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
            'description': 'Archaeological sites harvested from multiple public sources'
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
║   ArcheoScope - Comprehensive Archaeological Harvester      ║
║                                                              ║
║   Recopilando de fuentes globales:                          ║
║   • UNESCO World Heritage                                   ║
║   • Wikidata                                                ║
║   • OpenStreetMap                                           ║
║   • Pleiades Gazetteer                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    all_sites = []
    
    # 1. UNESCO (máxima calidad)
    unesco_sites = harvest_unesco()
    all_sites.extend(unesco_sites)
    
    # 2. Wikidata (gran volumen estructurado)
    wikidata_sites = harvest_wikidata(limit=10000)
    all_sites.extend(wikidata_sites)
    
    # 3. OpenStreetMap (máximo volumen)
    osm_sites = harvest_osm_global()
    all_sites.extend(osm_sites)
    
    # 4. Pleiades (mundo clásico)
    pleiades_sites = harvest_pleiades()
    all_sites.extend(pleiades_sites)
    
    # Resumen antes de deduplicar
    print(f"\n{'='*70}")
    print(f"📊 RESUMEN ANTES DE DEDUPLICAR")
    print(f"{'='*70}")
    print(f"Total de sitios recopilados: {len(all_sites)}")
    print(f"  - UNESCO: {len(unesco_sites)}")
    print(f"  - Wikidata: {len(wikidata_sites)}")
    print(f"  - OpenStreetMap: {len(osm_sites)}")
    print(f"  - Pleiades: {len(pleiades_sites)}")
    
    # Deduplicar
    unique_sites = deduplicate_sites(all_sites, distance_threshold_km=1.0)
    
    # Asignar confianza
    unique_sites = assign_confidence(unique_sites)
    
    # Guardar
    result = save_results(unique_sites, filename='harvested_archaeological_sites.json')
    
    # Resumen final
    print(f"\n{'='*70}")
    print(f"📊 RESUMEN FINAL")
    print(f"{'='*70}")
    print(f"✅ Total de sitios únicos: {result['metadata']['total_sites']}")
    print(f"\n📍 Por fuente:")
    for source, count in result['metadata']['source_statistics'].items():
        print(f"   • {source}: {count}")
    print(f"\n🎯 Por nivel de confianza:")
    for conf, count in result['metadata']['confidence_statistics'].items():
        print(f"   • {conf}: {count}")
    print(f"\n🌍 Top 10 países:")
    for i, (country, count) in enumerate(list(result['metadata']['top_20_countries'].items())[:10], 1):
        print(f"   {i}. {country}: {count}")
    
    print(f"\n✅ ¡Recopilación completada exitosamente!")
    print(f"\n💡 Siguiente paso: Ejecutar migrate_json_to_postgres.py para cargar a la base de datos")

if __name__ == "__main__":
    main()
