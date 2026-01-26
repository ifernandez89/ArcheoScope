#!/usr/bin/env python3
"""
Harvester para Pleiades - Mundo Antiguo (Greco-Romano)
~35,000 sitios del Mediterráneo, Medio Oriente, Europa
"""

import requests
import json
import gzip
from datetime import datetime
from typing import List, Dict

print("=" * 80)
print("🏛️  PLEIADES HARVESTER - Mundo Antiguo")
print("=" * 80)

def download_pleiades_data():
    """Descargar datos de Pleiades"""
    print("\n📥 Descargando datos de Pleiades...")
    print("   URL: https://atlantides.org/downloads/pleiades/json/")
    
    # URL del dump JSON
    url = "https://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz"
    
    print(f"\n⏳ Descargando archivo comprimido...")
    print(f"   (Esto puede tomar 2-3 minutos)")
    
    try:
        response = requests.get(url, timeout=300, stream=True)
        
        if response.status_code == 200:
            # Guardar archivo comprimido
            gz_file = "pleiades-places-latest.json.gz"
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(gz_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r   Progreso: {progress:.1f}%", end='')
            
            print(f"\n✅ Descarga completada: {downloaded / 1024 / 1024:.1f} MB")
            
            # Descomprimir
            print(f"\n📦 Descomprimiendo...")
            
            with gzip.open(gz_file, 'rb') as f_in:
                with open('pleiades-places-latest.json', 'wb') as f_out:
                    f_out.write(f_in.read())
            
            print(f"✅ Descompresión completada")
            
            return 'pleiades-places-latest.json'
            
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def parse_pleiades_data(filepath: str) -> List[Dict]:
    """Parsear datos de Pleiades"""
    print(f"\n📖 Parseando datos de Pleiades...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Archivo cargado")
    print(f"   Tipo: {data.get('@type', 'N/A')}")
    print(f"   Total features: {len(data.get('features', []))}")
    
    sites = []
    
    for feature in data.get('features', []):
        try:
            properties = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            
            # Extraer coordenadas
            coords = geometry.get('coordinates', [])
            if not coords or len(coords) < 2:
                continue
            
            lon, lat = coords[0], coords[1]
            
            # Extraer información
            title = properties.get('title', 'Unknown')
            description = properties.get('description', '')
            place_types = properties.get('placeTypes', [])
            
            # Filtrar solo sitios arqueológicos relevantes
            archaeological_types = [
                'settlement', 'temple', 'fort', 'villa', 'theater',
                'amphitheater', 'aqueduct', 'bridge', 'road', 'tomb',
                'sanctuary', 'city', 'town', 'village', 'fortress'
            ]
            
            is_archaeological = any(
                any(arch_type in pt.lower() for arch_type in archaeological_types)
                for pt in place_types
            )
            
            if not is_archaeological and place_types:
                continue
            
            site = {
                'source': 'Pleiades',
                'name': title,
                'latitude': lat,
                'longitude': lon,
                'description': description,
                'place_types': place_types,
                'pleiades_id': properties.get('id', ''),
                'uri': properties.get('uri', ''),
                'time_periods': properties.get('timePeriods', []),
                'country': 'Unknown'  # Pleiades no siempre tiene país
            }
            
            sites.append(site)
            
        except Exception as e:
            continue
    
    print(f"\n✅ Sitios arqueológicos extraídos: {len(sites):,}")
    
    return sites


def save_pleiades_sites(sites: List[Dict]):
    """Guardar sitios de Pleiades"""
    output_file = f"pleiades_sites_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Estadísticas
    place_types_count = {}
    for site in sites:
        for pt in site.get('place_types', []):
            place_types_count[pt] = place_types_count.get(pt, 0) + 1
    
    output = {
        'metadata': {
            'source': 'Pleiades',
            'harvested_at': datetime.now().isoformat(),
            'total_sites': len(sites),
            'url': 'https://pleiades.stoa.org/',
            'coverage': 'Mediterranean, Middle East, Europe',
            'period': 'Classical Antiquity',
            'place_types_distribution': place_types_count
        },
        'sites': sites
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Datos guardados en: {output_file}")
    
    # Mostrar estadísticas
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   Total sitios: {len(sites):,}")
    
    print(f"\n   Top 10 tipos de lugares:")
    for pt, count in sorted(place_types_count.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"      {pt}: {count:,}")
    
    return output_file


def main():
    """Proceso principal"""
    
    start_time = datetime.now()
    
    # 1. Descargar datos
    filepath = download_pleiades_data()
    
    if not filepath:
        print("\n❌ No se pudo descargar los datos")
        return
    
    # 2. Parsear datos
    sites = parse_pleiades_data(filepath)
    
    if not sites:
        print("\n❌ No se encontraron sitios")
        return
    
    # 3. Guardar resultados
    output_file = save_pleiades_sites(sites)
    
    # Resumen final
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n" + "=" * 80)
    print(f"✅ HARVEST COMPLETADO")
    print(f"=" * 80)
    
    print(f"\n📊 RESUMEN:")
    print(f"   Sitios recopilados: {len(sites):,}")
    print(f"   Tiempo: {duration:.1f} segundos ({duration/60:.1f} minutos)")
    print(f"   Archivo: {output_file}")
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print(f"   1. Revisar archivo JSON generado")
    print(f"   2. Importar a BD con bulk_import_new_sites.py")
    print(f"   3. Verificar cobertura del mundo antiguo")
    
    print(f"\n💡 COMANDO DE IMPORTACIÓN:")
    print(f"   python bulk_import_new_sites.py --file {output_file}")
    
    print(f"\n" + "=" * 80)


if __name__ == "__main__":
    main()
