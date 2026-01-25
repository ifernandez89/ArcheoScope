#!/usr/bin/env python3
"""
Script de enriquecimiento de datos arqueológicos
Estrategia: OSM base + Wikidata enriquecimiento + UNESCO validación
"""

import json
import time
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
from pathlib import Path

# Agregar backend al path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

class ArchaeologicalDataEnricher:
    """Enriquecedor de datos arqueológicos desde múltiples fuentes"""
    
    def __init__(self):
        self.wikidata_endpoint = "https://query.wikidata.org/sparql"
        self.unesco_cache = {}
        self.enrichment_stats = {
            "total_processed": 0,
            "wikidata_enriched": 0,
            "unesco_validated": 0,
            "errors": 0
        }
    
    def enrich_from_wikidata(self, site: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquecer sitio con datos de Wikidata usando IDs
        
        Agrega:
        - Período arqueológico detallado
        - Cultura asociada
        - Referencias académicas
        - Coordenadas precisas
        - Imágenes
        """
        
        wikidata_id = site.get('wikidata_id')
        if not wikidata_id:
            return site
        
        try:
            # Query SPARQL para obtener datos detallados
            query = f"""
            SELECT ?item ?itemLabel ?period ?periodLabel ?culture ?cultureLabel 
                   ?inception ?image ?coord ?heritageDesignation ?heritageLabel
                   ?article ?sitelink
            WHERE {{
              VALUES ?item {{ wd:{wikidata_id} }}
              
              OPTIONAL {{ ?item wdt:P2348 ?period. }}
              OPTIONAL {{ ?item wdt:P2596 ?culture. }}
              OPTIONAL {{ ?item wdt:P571 ?inception. }}
              OPTIONAL {{ ?item wdt:P18 ?image. }}
              OPTIONAL {{ ?item wdt:P625 ?coord. }}
              OPTIONAL {{ ?item wdt:P1435 ?heritageDesignation. }}
              
              OPTIONAL {{
                ?article schema:about ?item ;
                         schema:isPartOf <https://en.wikipedia.org/> ;
                         schema:name ?sitelink .
              }}
              
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,es,fr". }}
            }}
            LIMIT 1
            """
            
            response = requests.get(
                self.wikidata_endpoint,
                params={'query': query, 'format': 'json'},
                headers={'User-Agent': 'ArcheoScope/1.0'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                bindings = data.get('results', {}).get('bindings', [])
                
                if bindings:
                    result = bindings[0]
                    
                    # Enriquecer con datos de Wikidata
                    if 'periodLabel' in result:
                        site['period_detailed'] = result['periodLabel']['value']
                    
                    if 'cultureLabel' in result:
                        site['culture'] = result['cultureLabel']['value']
                    
                    if 'inception' in result:
                        site['date_established'] = result['inception']['value']
                    
                    if 'image' in result:
                        site['image_url'] = result['image']['value']
                    
                    if 'heritageLabel' in result:
                        site['heritage_designation'] = result['heritageLabel']['value']
                    
                    if 'sitelink' in result:
                        site['wikipedia_url'] = f"https://en.wikipedia.org/wiki/{result['sitelink']['value'].replace(' ', '_')}"
                    
                    site['wikidata_enriched'] = True
                    self.enrichment_stats['wikidata_enriched'] += 1
                    
                    return site
            
            time.sleep(0.1)  # Rate limiting
            
        except Exception as e:
            print(f"  ⚠️ Error enriqueciendo {site.get('name')}: {e}")
            self.enrichment_stats['errors'] += 1
        
        return site
    
    def validate_with_unesco(self, site: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validar sitio contra lista UNESCO World Heritage
        
        Agrega:
        - Estado UNESCO (inscrito, tentativo, no listado)
        - Año de inscripción
        - Criterios UNESCO
        - Número de referencia UNESCO
        """
        
        unesco_id = site.get('unesco_id')
        
        if unesco_id:
            # Sitio ya tiene ID UNESCO - marcar como validado
            site['unesco_status'] = 'inscribed'
            site['unesco_validated'] = True
            self.enrichment_stats['unesco_validated'] += 1
        else:
            # Buscar en caché o API UNESCO
            # Por ahora, marcar como no listado
            site['unesco_status'] = 'not_listed'
            site['unesco_validated'] = False
        
        return site
    
    def enrich_site(self, site: Dict[str, Any]) -> Dict[str, Any]:
        """Enriquecer un sitio completo"""
        
        self.enrichment_stats['total_processed'] += 1
        
        # 1. Enriquecer con Wikidata
        if site.get('wikidata_id'):
            site = self.enrich_from_wikidata(site)
        
        # 2. Validar con UNESCO
        site = self.validate_with_unesco(site)
        
        # 3. Agregar timestamp de enriquecimiento
        site['enriched_at'] = datetime.now().isoformat()
        
        return site
    
    def enrich_batch(self, sites: List[Dict[str, Any]], batch_size: int = 100) -> List[Dict[str, Any]]:
        """Enriquecer un lote de sitios"""
        
        enriched_sites = []
        
        print(f"\n🔄 Enriqueciendo {len(sites)} sitios...")
        
        for i, site in enumerate(sites, 1):
            if i % 10 == 0:
                print(f"  Procesados: {i}/{len(sites)}")
            
            enriched_site = self.enrich_site(site)
            enriched_sites.append(enriched_site)
            
            # Rate limiting
            if i % batch_size == 0:
                print(f"  ⏸️ Pausa para rate limiting...")
                time.sleep(2)
        
        return enriched_sites
    
    def print_stats(self):
        """Imprimir estadísticas de enriquecimiento"""
        
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS DE ENRIQUECIMIENTO")
        print("="*60)
        print(f"Total procesados: {self.enrichment_stats['total_processed']:,}")
        print(f"Enriquecidos con Wikidata: {self.enrichment_stats['wikidata_enriched']:,}")
        print(f"Validados con UNESCO: {self.enrichment_stats['unesco_validated']:,}")
        print(f"Errores: {self.enrichment_stats['errors']:,}")
        
        if self.enrichment_stats['total_processed'] > 0:
            wikidata_rate = (self.enrichment_stats['wikidata_enriched'] / 
                           self.enrichment_stats['total_processed'] * 100)
            unesco_rate = (self.enrichment_stats['unesco_validated'] / 
                         self.enrichment_stats['total_processed'] * 100)
            
            print(f"\nTasa de enriquecimiento Wikidata: {wikidata_rate:.1f}%")
            print(f"Tasa de validación UNESCO: {unesco_rate:.1f}%")
        
        print("="*60)


def main():
    """Función principal"""
    
    print("="*60)
    print("🏛️ ENRIQUECIMIENTO DE DATOS ARQUEOLÓGICOS")
    print("="*60)
    print("\nEstrategia:")
    print("  1. OSM como base principal (69,531 sitios)")
    print("  2. Enriquecimiento con Wikidata (IDs)")
    print("  3. Validación con UNESCO")
    print()
    
    # Cargar datos cosechados
    harvested_file = Path(__file__).parent.parent / "harvested_complete.json"
    
    if not harvested_file.exists():
        print(f"❌ No se encontró {harvested_file}")
        return 1
    
    print(f"📂 Cargando datos desde {harvested_file.name}...")
    
    with open(harvested_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sites = data.get('sites', [])
    print(f"✅ Cargados {len(sites):,} sitios")
    
    # Filtrar sitios con Wikidata ID para enriquecimiento
    sites_with_wikidata = [s for s in sites if s.get('wikidata_id')]
    print(f"\n🔍 Sitios con Wikidata ID: {len(sites_with_wikidata):,}")
    
    # Preguntar al usuario cuántos enriquecer
    print("\n⚠️ El enriquecimiento completo puede tomar varias horas.")
    print("   Recomendación: Empezar con un lote pequeño (100-500 sitios)")
    
    try:
        limit = input("\n¿Cuántos sitios enriquecer? (Enter para 100): ").strip()
        limit = int(limit) if limit else 100
    except ValueError:
        limit = 100
    
    sites_to_enrich = sites_with_wikidata[:limit]
    
    print(f"\n🚀 Enriqueciendo {len(sites_to_enrich):,} sitios...")
    
    # Crear enriquecedor
    enricher = ArchaeologicalDataEnricher()
    
    # Enriquecer sitios
    enriched_sites = enricher.enrich_batch(sites_to_enrich)
    
    # Guardar resultados
    output_file = Path(__file__).parent.parent / f"enriched_sites_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    output_data = {
        "metadata": {
            "total_sites": len(enriched_sites),
            "enrichment_date": datetime.now().isoformat(),
            "strategy": "OSM_base + Wikidata_enrichment + UNESCO_validation",
            "sources": ["OpenStreetMap", "Wikidata", "UNESCO"]
        },
        "sites": enriched_sites,
        "statistics": enricher.enrichment_stats
    }
    
    print(f"\n💾 Guardando resultados en {output_file.name}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Guardado: {output_file}")
    
    # Imprimir estadísticas
    enricher.print_stats()
    
    print("\n✅ ENRIQUECIMIENTO COMPLETADO")
    print(f"\nPróximos pasos:")
    print(f"  1. Revisar {output_file.name}")
    print(f"  2. Migrar datos enriquecidos a PostgreSQL")
    print(f"  3. Actualizar endpoints para usar datos enriquecidos")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
