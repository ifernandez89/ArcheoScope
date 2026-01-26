#!/usr/bin/env python3
"""
Script para calcular y actualizar scores de confianza de sitios arqueológicos
Basado en el sistema de pesos probabilísticos
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

# Agregar backend al path
sys.path.append(str(Path(__file__).parent.parent))

from backend.database import db
from backend.site_confidence_system import site_confidence_system


async def calculate_confidence_for_site(site: Dict[str, Any]) -> float:
    """
    Calcular confianza para un sitio individual
    
    Args:
        site: Diccionario con datos del sitio
    
    Returns:
        Score de confianza (0.0 - 1.0)
    """
    
    # Mapear confidence_level de BD a source para sistema de confianza
    confidence_mapping = {
        'CONFIRMED': 'excavated',
        'HIGH': 'national',
        'MODERATE': 'wikidata',
        'LOW': 'osm',
        'NEGATIVE_CONTROL': 'osm',
        'CANDIDATE': 'osm'
    }
    
    source = confidence_mapping.get(site.get('confidence_level', 'MODERATE'), 'osm')
    
    # Preparar datos para sistema de confianza
    site_data = {
        'id': site.get('id'),
        'name': site.get('name'),
        'source': source,
        'excavated': False,  # No tenemos este dato aún
        'references': site.get('description'),  # Usar descripción como proxy
        'geometry_accuracy_m': 100.0,  # Asumimos buena precisión
        'period': site.get('period'),
        'source_count': 1
    }
    
    # Calcular confianza
    confidence = site_confidence_system.calculate_site_confidence(site_data)
    
    return confidence.final_confidence


async def update_all_site_confidences():
    """Actualizar scores de confianza para todos los sitios"""
    
    print("="*80)
    print("🔍 CÁLCULO DE CONFIANZA DE SITIOS ARQUEOLÓGICOS")
    print("="*80)
    print()
    
    # Conectar a BD
    await db.connect()
    
    try:
        # Obtener total de sitios
        total_sites = await db.count_sites()
        print(f"📊 Total de sitios en BD: {total_sites:,}")
        print()
        
        # Procesar en lotes
        batch_size = 1000
        offset = 0
        updated_count = 0
        
        while offset < total_sites:
            print(f"🔄 Procesando lote {offset//batch_size + 1} (sitios {offset+1}-{min(offset+batch_size, total_sites)})...")
            
            # Obtener lote de sitios
            sites = await db.get_all_sites(limit=batch_size, offset=offset)
            
            # Calcular confianza para cada sitio
            for site in sites:
                try:
                    confidence_score = await calculate_confidence_for_site(site)
                    
                    # Aquí actualizaríamos la BD con el score
                    # Por ahora solo contamos
                    updated_count += 1
                    
                    if updated_count % 100 == 0:
                        print(f"   ✅ Procesados: {updated_count:,}/{total_sites:,}")
                
                except Exception as e:
                    print(f"   ⚠️ Error procesando {site.get('name')}: {e}")
            
            offset += batch_size
        
        print()
        print("="*80)
        print(f"✅ COMPLETADO: {updated_count:,} sitios procesados")
        print("="*80)
        print()
        print("📝 NOTA: Los scores de confianza se calcularon pero NO se guardaron en BD")
        print("   Para guardarlos, necesitamos agregar un campo 'confidence_score' a la tabla")
        print()
    
    finally:
        await db.close()


async def show_confidence_examples():
    """Mostrar ejemplos de cálculo de confianza"""
    
    print("="*80)
    print("📊 EJEMPLOS DE CÁLCULO DE CONFIANZA")
    print("="*80)
    print()
    
    await db.connect()
    
    try:
        # Obtener algunos sitios de ejemplo
        sites = await db.get_all_sites(limit=10)
        
        print(f"Mostrando primeros 10 sitios:\n")
        
        for site in sites:
            confidence_score = await calculate_confidence_for_site(site)
            
            print(f"📍 {site.get('name')}")
            print(f"   País: {site.get('country')}")
            print(f"   Nivel BD: {site.get('confidence_level')}")
            print(f"   Score calculado: {confidence_score:.3f}")
            print()
    
    finally:
        await db.close()


def main():
    """Función principal"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Calcular confianza de sitios arqueológicos')
    parser.add_argument('--examples', action='store_true', help='Mostrar ejemplos de cálculo')
    parser.add_argument('--update-all', action='store_true', help='Actualizar todos los sitios')
    
    args = parser.parse_args()
    
    if args.examples:
        asyncio.run(show_confidence_examples())
    elif args.update_all:
        asyncio.run(update_all_site_confidences())
    else:
        print("Uso:")
        print("  python scripts/calculate_site_confidence.py --examples")
        print("  python scripts/calculate_site_confidence.py --update-all")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
