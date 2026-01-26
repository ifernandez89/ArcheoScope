#!/usr/bin/env python3
"""
Test de anomalías con coordenadas específicas y registro en historial
Genera candidatos arqueológicos realistas con coordenadas exactas
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import numpy as np

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from water.water_detector import WaterDetector

def test_anomaly_with_coordinates():
    """Test que genera anomalías con coordenadas específicas"""
    
    print("🎯 ARCHEOSCOPE - TEST DE ANOMALÍAS CON COORDENADAS")
    print("=" * 60)
    print("🎨 Generando candidatos con coordenadas específicas para visualización")
    print("=" * 60)
    
    # Coordenadas del Triángulo Funcional con anomalías simuladas
    test_locations = [
        {
            "name": "Zona Norte - Candidato Mercante",
            "lat": 25.800,
            "lng": -70.000,
            "environment": "submarine",
            "expected_anomalies": 2
        },
        {
            "name": "Zona Centro - Concentración Excepcional", 
            "lat": 25.550,
            "lng": -70.250,
            "environment": "submarine",
            "expected_anomalies": 5
        },
        {
            "name": "Zona Terrestre - Estructuras Lineales",
            "lat": 41.872,
            "lng": 12.504,
            "environment": "terrestrial",
            "expected_anomalies": 3
        }
    ]
    
    water_detector = WaterDetector()
    results = []
    
    for i, location in enumerate(test_locations, 1):
        print(f"\n📍 ANÁLISIS {i}/3: {location['name']}")
        print(f"   Coordenadas: {location['lat']:.3f}°, {location['lng']:.3f}°")
        print(f"   Ambiente esperado: {location['environment']}")
        
        try:
            # Detectar ambiente
            water_context = water_detector.detect_water_context(location['lat'], location['lng'])
            
            # Generar anomalías realistas con coordenadas específicas
            anomalies = generate_anomalies_with_coordinates(
                location, 
                water_context, 
                location['expected_anomalies']
            )
            
            print(f"\n🎯 ANOMALÍAS GENERADAS: {len(anomalies)}")
            
            for j, anomaly in enumerate(anomalies, 1):
                print(f"\n   ⚓ ANOMALÍA {j}:")
                print(f"      📛 Nombre: {anomaly['name']}")
                print(f"      📍 Coordenadas: {anomaly['anomaly_coordinates']['formatted']}")
                print(f"      📏 Dimensiones: {anomaly['dimensions']}")
                print(f"      🔍 Confianza: {anomaly['confidence']}")
                print(f"      🏛️ Clasificación: {anomaly['classification']}")
                print(f"      🧲 Firma magnética: {anomaly['magnetic_signature']}")
            
            # Crear datos de análisis
            analysis_data = {
                'statistical_results': generate_statistical_results(len(anomalies)),
                'bathymetric_context': {
                    'depth_m': water_context.estimated_depth_m if water_context.is_water else 0,
                    'environment_type': 'submarine' if water_context.is_water else 'terrestrial'
                }
            }
            
            result = {
                'location': location,
                'water_context': {
                    'is_water': water_context.is_water,
                    'type': water_context.water_type.value if water_context.water_type else 'terrestrial',
                    'depth_m': water_context.estimated_depth_m,
                    'archaeological_potential': water_context.archaeological_potential
                },
                'anomalies': anomalies,
                'analysis_data': analysis_data,
                'timestamp': datetime.now().isoformat()
            }
            
            results.append(result)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            results.append({
                'location': location,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    
    # Guardar resultados
    output_data = {
        'test_info': {
            'title': 'Test de Anomalías con Coordenadas Específicas',
            'date': datetime.now().isoformat(),
            'purpose': 'Generar candidatos arqueológicos con coordenadas para visualización',
            'locations_tested': len(test_locations)
        },
        'results': results,
        'summary': {
            'total_locations': len(results),
            'total_anomalies': sum(len(r.get('anomalies', [])) for r in results),
            'environments': list(set(r.get('water_context', {}).get('type', 'unknown') for r in results))
        }
    }
    
    output_file = f"anomaly_coordinates_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 RESULTADOS GUARDADOS: {output_file}")
    
    # Resumen final
    total_anomalies = sum(len(r.get('anomalies', [])) for r in results)
    
    print(f"\n🏆 RESUMEN DEL TEST")
    print("=" * 60)
    print(f"📊 Ubicaciones analizadas: {len(results)}")
    print(f"🎯 Total anomalías generadas: {total_anomalies}")
    print(f"📍 Todas las anomalías incluyen coordenadas específicas")
    print(f"🎨 Listas para visualización 2D/3D")
    print(f"📋 Preparadas para registro en historial")
    
    # Mostrar ejemplo de coordenadas
    if results and results[0].get('anomalies'):
        example = results[0]['anomalies'][0]
        print(f"\n📍 EJEMPLO DE COORDENADAS GENERADAS:")
        print(f"   Anomalía: {example['name']}")
        print(f"   Coordenadas: {example['anomaly_coordinates']['formatted']}")
        print(f"   Dimensiones: {example['dimensions']}")
        print(f"   Visualización: ✅ Disponible")
    
    return output_data

def generate_anomalies_with_coordinates(location, water_context, num_anomalies):
    """Generar anomalías realistas con coordenadas específicas"""
    
    anomalies = []
    base_lat = location['lat']
    base_lng = location['lng']
    
    for i in range(num_anomalies):
        # Generar coordenadas específicas cerca de la ubicación base
        offset_lat = (np.random.random() - 0.5) * 0.02  # ±0.01° (~1km)
        offset_lng = (np.random.random() - 0.5) * 0.02
        
        anomaly_lat = base_lat + offset_lat
        anomaly_lng = base_lng + offset_lng
        
        # Generar características basadas en el ambiente
        if water_context.is_water:
            anomaly = generate_submarine_anomaly(i, anomaly_lat, anomaly_lng, water_context)
        else:
            anomaly = generate_terrestrial_anomaly(i, anomaly_lat, anomaly_lng)
        
        anomalies.append(anomaly)
    
    return anomalies

def generate_submarine_anomaly(index, lat, lng, water_context):
    """Generar anomalía submarina realista"""
    
    depth = water_context.estimated_depth_m or 500
    
    # Dimensiones basadas en profundidad
    if depth > 1000:  # Aguas profundas
        length = np.random.uniform(150, 350)
        width = np.random.uniform(20, 45)
        height = np.random.uniform(12, 30)
        vessel_types = ['passenger_liner', 'large_cargo_ship', 'warship']
    elif depth > 300:  # Aguas medias
        length = np.random.uniform(80, 250)
        width = np.random.uniform(12, 35)
        height = np.random.uniform(8, 20)
        vessel_types = ['cargo_ship', 'merchant_vessel', 'fishing_vessel']
    else:  # Aguas someras
        length = np.random.uniform(30, 150)
        width = np.random.uniform(6, 25)
        height = np.random.uniform(4, 15)
        vessel_types = ['fishing_vessel', 'patrol_boat', 'yacht']
    
    vessel_type = np.random.choice(vessel_types)
    confidence = np.random.uniform(0.65, 0.92)
    
    # Clasificación basada en dimensiones
    if length > 250:
        classification = f"Gran {vessel_type.replace('_', ' ')} - Posible transatlántico"
        magnetic_signature = "Intensa"
    elif length > 150:
        classification = f"{vessel_type.replace('_', ' ').title()} - Mercante medio"
        magnetic_signature = "Moderada"
    else:
        classification = f"{vessel_type.replace('_', ' ').title()} - Embarcación menor"
        magnetic_signature = "Baja" if length < 80 else "Moderada"
    
    return {
        'type': 'submarine_wreck',
        'name': f'Candidato {vessel_type.replace("_", " ").title()} {index + 1}',
        'icon': '🚢',
        'description': f'Estructura submarina {length:.1f}m x {width:.1f}m detectada a {depth:.0f}m de profundidad',
        'confidence': f'{confidence:.2f} (Alta confianza instrumental)',
        'evidence': 'Tríada clásica: magnetómetro + multihaz + subfondo. Geometría coherente.',
        'color': '#dc3545',
        'anomaly_coordinates': {
            'lat': lat,
            'lng': lng,
            'formatted': f'{lat:.6f}, {lng:.6f}'
        },
        'dimensions': f'{length:.1f}m x {width:.1f}m x {height:.1f}m',
        'magnetic_signature': magnetic_signature,
        'classification': classification,
        'validation_status': 'Pendiente validación visual con ROV',
        'environment_context': {
            'depth_m': depth,
            'water_type': water_context.water_type.value if water_context.water_type else 'unknown',
            'preservation_potential': 'Alta' if depth > 200 else 'Media'
        }
    }

def generate_terrestrial_anomaly(index, lat, lng):
    """Generar anomalía terrestre realista"""
    
    # Tipos de estructuras terrestres
    structure_types = [
        {'type': 'linear_structure', 'name': 'Estructura Lineal', 'icon': '🛤️'},
        {'type': 'circular_structure', 'name': 'Estructura Circular', 'icon': '⭕'},
        {'type': 'rectangular_structure', 'name': 'Estructura Rectangular', 'icon': '🔲'},
        {'type': 'complex_structure', 'name': 'Complejo Estructural', 'icon': '🏛️'}
    ]
    
    structure = np.random.choice(structure_types)
    
    # Dimensiones terrestres
    if structure['type'] == 'linear_structure':
        length = np.random.uniform(100, 2000)  # Caminos, muros
        width = np.random.uniform(2, 20)
        height = np.random.uniform(0.5, 5)
        classification = "Infraestructura lineal - Posible camino o muro"
    elif structure['type'] == 'circular_structure':
        diameter = np.random.uniform(20, 200)  # Plazas, fosos
        length = width = diameter
        height = np.random.uniform(1, 10)
        classification = "Estructura circular - Posible plaza o foso"
    elif structure['type'] == 'rectangular_structure':
        length = np.random.uniform(20, 150)  # Edificios
        width = np.random.uniform(15, 80)
        height = np.random.uniform(2, 15)
        classification = "Estructura rectangular - Posible edificio"
    else:  # complex_structure
        length = np.random.uniform(50, 500)  # Complejos
        width = np.random.uniform(40, 300)
        height = np.random.uniform(3, 20)
        classification = "Complejo estructural - Posible asentamiento"
    
    confidence = np.random.uniform(0.60, 0.88)
    
    return {
        'type': structure['type'],
        'name': f'{structure["name"]} {index + 1}',
        'icon': structure['icon'],
        'description': f'Estructura terrestre {length:.1f}m x {width:.1f}m detectada por análisis multi-espectral',
        'confidence': f'{confidence:.2f} (Confianza instrumental)',
        'evidence': 'Análisis NDVI + térmico + SAR. Geometría antrópica confirmada.',
        'color': '#8B4513',
        'anomaly_coordinates': {
            'lat': lat,
            'lng': lng,
            'formatted': f'{lat:.6f}, {lng:.6f}'
        },
        'dimensions': f'{length:.1f}m x {width:.1f}m x {height:.1f}m',
        'magnetic_signature': 'No aplicable (terrestre)',
        'classification': classification,
        'validation_status': 'Pendiente verificación de campo',
        'environment_context': {
            'terrain_type': 'terrestre',
            'vegetation_cover': np.random.choice(['baja', 'media', 'alta']),
            'accessibility': np.random.choice(['alta', 'media', 'baja'])
        }
    }

def generate_statistical_results(num_anomalies):
    """Generar resultados estadísticos basados en número de anomalías"""
    
    # Probabilidad base según número de anomalías
    base_prob = min(0.9, 0.4 + (num_anomalies * 0.1))
    
    return {
        'multibeam_sonar': {'archaeological_probability': base_prob + np.random.uniform(-0.1, 0.1)},
        'magnetometer': {'archaeological_probability': base_prob + np.random.uniform(-0.15, 0.1)},
        'side_scan_sonar': {'archaeological_probability': base_prob + np.random.uniform(-0.08, 0.12)},
        'sub_bottom_profiler': {'archaeological_probability': base_prob + np.random.uniform(-0.12, 0.08)},
        'acoustic_reflectance': {'archaeological_probability': base_prob + np.random.uniform(-0.1, 0.1)}
    }

if __name__ == "__main__":
    results = test_anomaly_with_coordinates()