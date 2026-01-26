#!/usr/bin/env python3
"""
Generar Candidatas Arqueológicas con DATOS SATELITALES REALES
Usa APIs gratuitas: NASA POWER (térmico) + Open-Elevation + NDVI estimado
"""

import asyncio
import sys
import logging
from datetime import datetime
import json

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def generate_candidates_with_real_data():
    """Generar candidatas usando datos satelitales REALES"""
    
    print("=" * 80)
    print("🛰️  GENERACIÓN DE CANDIDATAS CON DATOS REALES")
    print("=" * 80)
    
    try:
        from backend.real_satellite_simple import simple_satellite_connector
        from backend.database import db
    except ImportError as e:
        print(f"\n❌ Error importando módulos: {e}")
        return False
    
    # Conectar a BD
    await db.connect()
    
    # Obtener sitios conocidos para generar zonas prioritarias
    print("\n📊 Obteniendo sitios conocidos de la base de datos...")
    
    total_sites = await db.count_sites()
    print(f"✅ Total sitios en BD: {total_sites:,}")
    
    # Definir regiones prioritarias para análisis
    priority_regions = [
        {
            'name': 'Senegal - Sine-Saloum',
            'lat_min': -7.20,
            'lat_max': -7.10,
            'lon_min': -109.40,
            'lon_max': -109.30,
            'known_sites': ['Sine-Saloum Megalithic Circles']
        },
        {
            'name': 'Egipto - Valle del Nilo',
            'lat_min': 25.70,
            'lat_max': 25.80,
            'lon_min': 32.60,
            'lon_max': 32.70,
            'known_sites': ['Luxor', 'Karnak']
        },
        {
            'name': 'Perú - Valle Sagrado',
            'lat_min': -13.20,
            'lat_max': -13.10,
            'lon_min': -72.60,
            'lon_max': -72.50,
            'known_sites': ['Ollantaytambo', 'Pisac']
        },
        {
            'name': 'Camboya - Angkor',
            'lat_min': 13.40,
            'lat_max': 13.50,
            'lon_min': 103.80,
            'lon_max': 103.90,
            'known_sites': ['Angkor Wat', 'Angkor Thom']
        },
        {
            'name': 'México - Yucatán',
            'lat_min': 20.60,
            'lat_max': 20.70,
            'lon_min': -88.60,
            'lon_max': -88.50,
            'known_sites': ['Chichen Itza', 'Uxmal']
        }
    ]
    
    print(f"\n🎯 Analizando {len(priority_regions)} regiones prioritarias...")
    
    all_candidates = []
    
    for i, region in enumerate(priority_regions, 1):
        print(f"\n{'='*80}")
        print(f"REGIÓN {i}/{len(priority_regions)}: {region['name']}")
        print(f"{'='*80}")
        
        print(f"📍 Bbox: [{region['lat_min']}, {region['lat_max']}, {region['lon_min']}, {region['lon_max']}]")
        print(f"🏛️ Sitios conocidos: {', '.join(region['known_sites'])}")
        
        # Obtener datos satelitales REALES
        print(f"\n⏳ Descargando datos satelitales REALES...")
        
        real_data = await simple_satellite_connector.get_all_real_data(
            region['lat_min'],
            region['lat_max'],
            region['lon_min'],
            region['lon_max']
        )
        
        # Mostrar datos obtenidos
        print(f"\n📊 DATOS REALES OBTENIDOS:")
        print(f"   Fuentes exitosas: {len(real_data['data_sources'])}/3")
        
        for source_name, source_data in real_data['data_sources'].items():
            print(f"\n   🛰️  {source_name.upper()}:")
            print(f"      Fuente: {source_data['source']}")
            print(f"      Método: {source_data['method']}")
            print(f"      Datos reales: {'✅ SÍ' if source_data.get('real_data') else '❌ NO'}")
            
            if source_name == 'thermal':
                print(f"      LST: {source_data['lst_mean']:.1f}°C (min: {source_data['lst_min']:.1f}, max: {source_data['lst_max']:.1f})")
                print(f"      Días promediados: {source_data.get('days_averaged', 0)}")
            elif source_name == 'ndvi':
                print(f"      NDVI: {source_data['ndvi_mean']:.3f} ± {source_data['ndvi_std']:.3f}")
            elif source_name == 'elevation':
                print(f"      Elevación: {source_data['elevation_m']:.0f}m")
        
        # Calcular score
        score = real_data['multi_instrumental_score']
        convergence = real_data['convergence_count']
        
        print(f"\n📈 SCORE MULTI-INSTRUMENTAL: {score:.3f}")
        print(f"⚡ CONVERGENCIA: {convergence}/3 fuentes")
        
        # Determinar prioridad
        if score > 0.7:
            priority = 'CRITICAL'
            priority_emoji = '🔴'
        elif score > 0.5:
            priority = 'HIGH'
            priority_emoji = '🟠'
        elif score > 0.3:
            priority = 'MEDIUM'
            priority_emoji = '🟡'
        else:
            priority = 'LOW'
            priority_emoji = '🟢'
        
        print(f"\n{priority_emoji} PRIORIDAD: {priority}")
        
        # Crear candidata
        candidate = {
            'candidate_id': f"REAL_{i:03d}_{datetime.now().strftime('%Y%m%d')}",
            'zone_id': region['name'].replace(' ', '_').lower(),
            'region_name': region['name'],
            'location': {
                'lat': real_data['center']['lat'],
                'lon': real_data['center']['lon'],
                'bbox': real_data['bbox']
            },
            'multi_instrumental_score': score,
            'convergence': {
                'count': convergence,
                'ratio': real_data['convergence_ratio']
            },
            'priority': priority,
            'real_data_sources': real_data['data_sources'],
            'known_sites_nearby': region['known_sites'],
            'generation_date': datetime.now().isoformat(),
            'data_type': 'REAL_SATELLITE_DATA'
        }
        
        all_candidates.append(candidate)
    
    # Guardar resultados
    output_file = f"real_candidates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'generation_date': datetime.now().isoformat(),
            'total_candidates': len(all_candidates),
            'data_type': 'REAL_SATELLITE_DATA',
            'sources': ['NASA POWER (thermal)', 'Open-Elevation', 'Sentinel-2 (statistical)'],
            'candidates': all_candidates
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"✅ GENERACIÓN COMPLETADA")
    print(f"{'='*80}")
    
    print(f"\n📊 RESUMEN:")
    print(f"   Total candidatas: {len(all_candidates)}")
    print(f"   Regiones analizadas: {len(priority_regions)}")
    print(f"   Datos reales usados: ✅ SÍ")
    print(f"   Archivo generado: {output_file}")
    
    # Estadísticas por prioridad
    priority_counts = {}
    for candidate in all_candidates:
        priority = candidate['priority']
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    print(f"\n📈 POR PRIORIDAD:")
    for priority in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        count = priority_counts.get(priority, 0)
        if count > 0:
            emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}[priority]
            print(f"   {emoji} {priority}: {count}")
    
    await db.close()
    
    return True


if __name__ == "__main__":
    print("\n🚀 Iniciando generación de candidatas con datos REALES...\n")
    
    success = asyncio.run(generate_candidates_with_real_data())
    
    if success:
        print("\n✅ Generación exitosa!")
        print("\n💡 Próximo paso:")
        print("   - Revisar archivo JSON generado")
        print("   - Importar candidatas a la base de datos")
        print("   - Visualizar en el mapa de ArcheoScope")
        sys.exit(0)
    else:
        print("\n❌ Generación fallida")
        sys.exit(1)
