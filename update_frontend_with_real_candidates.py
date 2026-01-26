#!/usr/bin/env python3
"""
Actualizar frontend con candidatas REALES
Genera un archivo GeoJSON para visualización
"""

import json
import psycopg2

DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}


def generate_geojson():
    """Generar GeoJSON con candidatas reales"""
    
    print("="*80)
    print("GENERANDO GEOJSON PARA VISUALIZACION")
    print("="*80)
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Obtener candidatas
    cursor.execute("""
        SELECT 
            candidate_id,
            zone_id,
            center_lat,
            center_lon,
            multi_instrumental_score,
            convergence_count,
            convergence_ratio,
            recommended_action,
            signals,
            generation_date
        FROM archaeological_candidates
        WHERE strategy = 'real_satellite_data'
        ORDER BY multi_instrumental_score DESC
    """)
    
    rows = cursor.fetchall()
    
    print(f"\nCandidatas encontradas: {len(rows)}")
    
    # Crear GeoJSON
    features = []
    
    for row in rows:
        candidate_id, zone_id, lat, lon, score, conv_count, conv_ratio, action, signals, gen_date = row
        
        # Determinar color por score
        if score > 0.7:
            color = '#ff0000'  # Rojo - CRITICAL
            priority = 'CRITICAL'
        elif score > 0.5:
            color = '#ff8800'  # Naranja - HIGH
            priority = 'HIGH'
        elif score > 0.3:
            color = '#ffcc00'  # Amarillo - MEDIUM
            priority = 'MEDIUM'
        else:
            color = '#00ff00'  # Verde - LOW
            priority = 'LOW'
        
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [lon, lat]
            },
            'properties': {
                'candidate_id': candidate_id,
                'zone_id': zone_id,
                'score': round(score, 3),
                'convergence_count': conv_count,
                'convergence_ratio': round(conv_ratio, 2),
                'priority': priority,
                'color': color,
                'recommended_action': action,
                'data_type': 'REAL_SATELLITE_DATA',
                'generation_date': str(gen_date) if gen_date else None
            }
        }
        
        features.append(feature)
        
        print(f"\n{len(features)}. {candidate_id}")
        print(f"   Lat/Lon: {lat:.4f}, {lon:.4f}")
        print(f"   Score: {score:.3f} ({priority})")
        print(f"   Convergencia: {conv_count}/3")
    
    geojson = {
        'type': 'FeatureCollection',
        'features': features,
        'metadata': {
            'total_candidates': len(features),
            'data_type': 'REAL_SATELLITE_DATA',
            'sources': ['NASA POWER', 'Open-Elevation', 'Sentinel-2'],
            'generation_date': '2026-01-25'
        }
    }
    
    # Guardar GeoJSON
    output_file = 'frontend/real_candidates.geojson'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"GEOJSON GENERADO")
    print(f"{'='*80}")
    
    print(f"\nArchivo: {output_file}")
    print(f"Features: {len(features)}")
    
    cursor.close()
    conn.close()
    
    return True


if __name__ == "__main__":
    print("\nGenerando GeoJSON...\n")
    
    success = generate_geojson()
    
    if success:
        print("\nOK - GeoJSON generado exitosamente!")
        print("\nProximo paso:")
        print("   1. Abrir: http://localhost:8080/priority_zones_map.html")
        print("   2. Las candidatas REALES apareceran en el mapa")
    else:
        print("\nERROR")
