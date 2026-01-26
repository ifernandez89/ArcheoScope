#!/usr/bin/env python3
"""
Importar Candidatas REALES a la Base de Datos
"""

import asyncio
import json
import sys
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def import_candidates_to_db():
    """Importar candidatas con datos reales a PostgreSQL"""
    
    print("=" * 80)
    print("📥 IMPORTACIÓN DE CANDIDATAS REALES A BASE DE DATOS")
    print("=" * 80)
    
    try:
        from backend.database import db
    except ImportError as e:
        print(f"\n❌ Error importando módulos: {e}")
        return False
    
    # Conectar a BD
    await db.connect()
    
    # Leer archivo JSON
    json_file = "real_candidates_20260125_232040.json"
    
    print(f"\n📂 Leyendo archivo: {json_file}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    candidates = data['candidates']
    
    print(f"✅ {len(candidates)} candidatas encontradas")
    print(f"📅 Generadas: {data['generation_date']}")
    print(f"🛰️ Fuentes: {', '.join(data['sources'])}")
    
    # Importar cada candidata
    print(f"\n{'='*80}")
    print("IMPORTANDO CANDIDATAS")
    print(f"{'='*80}")
    
    imported_count = 0
    
    for i, candidate in enumerate(candidates, 1):
        print(f"\n{i}. {candidate['region_name']}")
        print(f"   ID: {candidate['candidate_id']}")
        print(f"   Score: {candidate['multi_instrumental_score']:.3f}")
        print(f"   Prioridad: {candidate['priority']}")
        
        try:
            # Preparar datos para BD
            location = candidate.get('location', {})
            bbox = location.get('bbox', [0, 0, 0, 0])
            
            candidate_data = {
                'candidate_id': candidate['candidate_id'],
                'zone_id': candidate['zone_id'],
                'center_lat': location.get('lat', 0),
                'center_lon': location.get('lon', 0),
                'area_km2': 1.0,  # Área aproximada
                'multi_instrumental_score': candidate['multi_instrumental_score'],
                'convergence_count': candidate['convergence']['count'],
                'convergence_ratio': candidate['convergence']['ratio'],
                'recommended_action': 'field_validation' if candidate['priority'] in ['CRITICAL', 'HIGH'] else 'detailed_analysis',
                'temporal_persistence': True,
                'temporal_years': 0,
                'signals': candidate.get('real_data_sources', {}),
                'strategy': 'real_satellite_data',
                'region_bounds': {
                    'lat_min': bbox[0] if len(bbox) > 0 else 0,
                    'lat_max': bbox[1] if len(bbox) > 1 else 0,
                    'lon_min': bbox[2] if len(bbox) > 2 else 0,
                    'lon_max': bbox[3] if len(bbox) > 3 else 0
                }
            }
            
            # Guardar en BD
            candidate_id = await db.save_candidate(candidate_data)
            
            print(f"   ✅ Importada (DB ID: {candidate_id})")
            imported_count += 1
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print(f"✅ IMPORTACIÓN COMPLETADA")
    print(f"{'='*80}")
    
    print(f"\n📊 RESUMEN:")
    print(f"   Total candidatas: {len(candidates)}")
    print(f"   Importadas exitosamente: {imported_count}")
    print(f"   Fallidas: {len(candidates) - imported_count}")
    
    # Verificar en BD
    print(f"\n🔍 Verificando en base de datos...")
    
    stats = await db.get_candidates_statistics()
    
    if stats:
        print(f"\n📊 ESTADÍSTICAS DE CANDIDATAS EN BD:")
        print(f"   Total: {stats.get('total_candidates', 0)}")
        print(f"   Pendientes: {stats.get('pending_count', 0)}")
        print(f"   Analizadas: {stats.get('analyzed_count', 0)}")
        print(f"   Score promedio: {stats.get('avg_score', 0):.3f}")
    
    await db.close()
    
    return True


if __name__ == "__main__":
    print("\n🚀 Iniciando importación...\n")
    
    success = asyncio.run(import_candidates_to_db())
    
    if success:
        print("\n✅ Importación exitosa!")
        print("\n💡 Próximo paso:")
        print("   - Visualizar en el mapa de ArcheoScope")
        print("   - Acceder a: http://localhost:8080/priority_zones_map.html")
        sys.exit(0)
    else:
        print("\n❌ Importación fallida")
        sys.exit(1)
