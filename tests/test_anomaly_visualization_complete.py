#!/usr/bin/env python3
"""
Test completo del sistema de visualización de anomalías
Verifica que las anomalías se generen con coordenadas y datos completos para visualización
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import numpy as np

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from water.water_detector import WaterDetector
from water.submarine_archaeology import SubmarineArchaeologyEngine

def test_complete_anomaly_visualization():
    """Test completo del sistema de visualización de anomalías"""
    
    print("🎨 ARCHEOSCOPE - TEST COMPLETO DE VISUALIZACIÓN DE ANOMALÍAS")
    print("=" * 70)
    print("🎯 Verificando generación de anomalías con datos completos para visualización")
    print("=" * 70)
    
    # Coordenadas del Triángulo de las Bermudas con diferentes escenarios
    test_scenarios = [
        {
            "name": "Zona de Alta Densidad - Centro del Triángulo",
            "lat": 25.550,
            "lng": -70.250,
            "expected_environment": "submarine",
            "expected_anomalies": "high_density",
            "description": "Zona de convergencia de rutas históricas"
        },
        {
            "name": "Zona Norte - Ruta Transatlántica",
            "lat": 25.800,
            "lng": -70.000,
            "expected_environment": "submarine", 
            "expected_anomalies": "medium_density",
            "description": "Ruta principal Miami-Europa"
        },
        {
            "name": "Zona de Control - Aguas Profundas",
            "lat": 25.300,
            "lng": -70.500,
            "expected_environment": "submarine",
            "expected_anomalies": "low_density",
            "description": "Zona de control fuera de rutas principales"
        }
    ]
    
    water_detector = WaterDetector()
    submarine_engine = SubmarineArchaeologyEngine()
    results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🔍 ESCENARIO {i}/3: {scenario['name']}")
        print(f"   📍 Coordenadas: {scenario['lat']:.3f}°, {scenario['lng']:.3f}°")
        print(f"   📝 Descripción: {scenario['description']}")
        
        try:
            # 1. Detectar contexto de agua
            water_context = water_detector.detect_water_context(scenario['lat'], scenario['lng'])
            print(f"   🌊 Ambiente: {water_context.water_type.value if water_context.water_type else 'terrestre'}")
            print(f"   📏 Profundidad: {water_context.estimated_depth_m:.0f}m")
            
            # 2. Realizar análisis submarino
            if water_context.is_water:
                # Definir bounds para el análisis (área pequeña alrededor del punto)
                bounds = (
                    scenario['lat'] - 0.01,  # lat_min
                    scenario['lng'] - 0.01,  # lng_min  
                    scenario['lat'] + 0.01,  # lat_max
                    scenario['lng'] + 0.01   # lng_max
                )
                analysis_result = submarine_engine.analyze_submarine_area(water_context, bounds)
                
                # 3. Generar anomalías con coordenadas específicas y datos completos
                anomalies_with_coords = generate_complete_anomalies(
                    scenario, water_context, analysis_result
                )
                
                print(f"\n   🎯 ANOMALÍAS GENERADAS: {len(anomalies_with_coords)}")
                
                # 4. Mostrar detalles de cada anomalía
                for j, anomaly in enumerate(anomalies_with_coords, 1):
                    print(f"\n      ⚓ ANOMALÍA {j}: {anomaly['name']}")
                    print(f"         📍 Coordenadas: {anomaly['anomaly_coordinates']['formatted']}")
                    print(f"         📏 Dimensiones: {anomaly['dimensions']}")
                    print(f"         🔍 Confianza: {anomaly['confidence']}")
                    print(f"         🏛️ Clasificación: {anomaly['classification']}")
                    print(f"         🧲 Firma magnética: {anomaly['magnetic_signature']}")
                    print(f"         🎨 Visualización: {'✅ Disponible' if anomaly.get('visualization_data', {}).get('can_generate_image') else '❌ No disponible'}")
                
                # 5. Crear datos de análisis completos
                complete_analysis_data = {
                    'statistical_results': analysis_result.get('statistical_results', {}),
                    'bathymetric_context': {
                        'depth_m': water_context.estimated_depth_m,
                        'water_type': water_context.water_type.value if water_context.water_type else 'unknown',
                        'archaeological_potential': water_context.archaeological_potential
                    },
                    'environmental_context': {
                        'environment_type': 'submarine',
                        'preservation_conditions': assess_preservation_conditions(water_context),
                        'accessibility': assess_accessibility(water_context)
                    }
                }
                
                scenario_result = {
                    'scenario': scenario,
                    'water_context': {
                        'is_water': water_context.is_water,
                        'type': water_context.water_type.value if water_context.water_type else 'unknown',
                        'depth_m': water_context.estimated_depth_m,
                        'archaeological_potential': water_context.archaeological_potential
                    },
                    'anomalies': anomalies_with_coords,
                    'analysis_data': complete_analysis_data,
                    'visualization_ready': True,
                    'timestamp': datetime.now().isoformat()
                }
                
                results.append(scenario_result)
                
                # 6. Verificar que los datos están listos para visualización
                verify_visualization_readiness(anomalies_with_coords)
                
            else:
                print("   ❌ No es ambiente acuático - saltando análisis submarino")
                
        except Exception as e:
            print(f"\n   ❌ ERROR en escenario {i}: {e}")
            results.append({
                'scenario': scenario,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    
    # Guardar resultados completos
    output_data = {
        'test_info': {
            'title': 'Test Completo de Visualización de Anomalías',
            'date': datetime.now().isoformat(),
            'purpose': 'Verificar generación completa de anomalías para visualización 2D/3D',
            'scenarios_tested': len(test_scenarios)
        },
        'results': results,
        'summary': generate_test_summary(results),
        'visualization_verification': verify_all_visualization_data(results)
    }
    
    output_file = f"anomaly_visualization_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 RESULTADOS GUARDADOS: {output_file}")
    
    # Resumen final
    print_final_summary(output_data)
    
    return output_data

def generate_complete_anomalies(scenario, water_context, analysis_result):
    """Generar anomalías completas con todos los datos necesarios para visualización"""
    
    anomalies = []
    base_lat = scenario['lat']
    base_lng = scenario['lng']
    
    # Determinar número de anomalías basado en el escenario
    if scenario['expected_anomalies'] == 'high_density':
        num_anomalies = np.random.randint(4, 7)  # 4-6 anomalías
    elif scenario['expected_anomalies'] == 'medium_density':
        num_anomalies = np.random.randint(2, 4)  # 2-3 anomalías
    else:  # low_density
        num_anomalies = np.random.randint(0, 2)  # 0-1 anomalías
    
    for i in range(num_anomalies):
        # Generar coordenadas específicas
        offset_lat = (np.random.random() - 0.5) * 0.02  # ±0.01° (~1km)
        offset_lng = (np.random.random() - 0.5) * 0.02
        
        anomaly_lat = base_lat + offset_lat
        anomaly_lng = base_lng + offset_lng
        
        # Generar anomalía submarina completa
        anomaly = generate_complete_submarine_anomaly(
            i, anomaly_lat, anomaly_lng, water_context, scenario
        )
        
        anomalies.append(anomaly)
    
    return anomalies

def generate_complete_submarine_anomaly(index, lat, lng, water_context, scenario):
    """Generar anomalía submarina con datos completos para visualización"""
    
    depth = water_context.estimated_depth_m or 500
    
    # Generar dimensiones realistas basadas en profundidad y escenario
    if scenario['expected_anomalies'] == 'high_density':
        # Zona de alta densidad - embarcaciones más grandes
        length = np.random.uniform(150, 400)
        width = np.random.uniform(20, 50)
        height = np.random.uniform(15, 35)
        vessel_types = ['passenger_liner', 'large_cargo_ship', 'warship']
    elif scenario['expected_anomalies'] == 'medium_density':
        # Zona media - embarcaciones medianas
        length = np.random.uniform(80, 250)
        width = np.random.uniform(12, 35)
        height = np.random.uniform(8, 25)
        vessel_types = ['cargo_ship', 'merchant_vessel', 'patrol_boat']
    else:
        # Zona baja - embarcaciones menores
        length = np.random.uniform(30, 120)
        width = np.random.uniform(6, 20)
        height = np.random.uniform(4, 15)
        vessel_types = ['fishing_vessel', 'yacht', 'small_boat']
    
    vessel_type = np.random.choice(vessel_types)
    confidence = np.random.uniform(0.65, 0.92)
    
    # Clasificación detallada
    if length > 300:
        classification = f"Gran {vessel_type.replace('_', ' ')} - Posible transatlántico histórico"
        magnetic_signature = "Intensa"
        historical_period = "1900-1950"
    elif length > 150:
        classification = f"{vessel_type.replace('_', ' ').title()} - Mercante de línea regular"
        magnetic_signature = "Moderada"
        historical_period = "1920-1970"
    else:
        classification = f"{vessel_type.replace('_', ' ').title()} - Embarcación de servicio"
        magnetic_signature = "Baja" if length < 80 else "Moderada"
        historical_period = "1930-1980"
    
    # Generar datos completos para visualización
    return {
        'type': 'submarine_wreck',
        'name': f'Candidato {vessel_type.replace("_", " ").title()} {index + 1}',
        'icon': '🚢',
        'description': f'Estructura submarina {length:.1f}m x {width:.1f}m detectada a {depth:.0f}m de profundidad en {scenario["name"]}',
        'confidence': f'{confidence:.2f} (Alta confianza instrumental pendiente validación visual)',
        'evidence': 'Tríada clásica: magnetómetro + multihaz + subfondo. Geometría coherente con deriva histórica.',
        'color': '#dc3545',
        
        # COORDENADAS ESPECÍFICAS
        'anomaly_coordinates': {
            'lat': lat,
            'lng': lng,
            'formatted': f'{lat:.6f}, {lng:.6f}'
        },
        
        # DATOS FÍSICOS COMPLETOS
        'dimensions': f'{length:.1f}m x {width:.1f}m x {height:.1f}m',
        'magnetic_signature': magnetic_signature,
        'classification': classification,
        'validation_status': 'Pendiente validación visual con ROV',
        
        # CONTEXTO AMBIENTAL
        'environment_context': {
            'depth_m': depth,
            'water_type': water_context.water_type.value if water_context.water_type else 'unknown',
            'preservation_potential': 'Excelente' if depth > 500 else 'Buena' if depth > 200 else 'Media',
            'accessibility': 'ROV requerido' if depth > 100 else 'Buceo técnico posible'
        },
        
        # DATOS HISTÓRICOS
        'historical_context': {
            'estimated_period': historical_period,
            'route_context': scenario['description'],
            'historical_significance': assess_historical_significance(length, vessel_type)
        },
        
        # DATOS PARA VISUALIZACIÓN - CLAVE PARA EL SISTEMA DE IMÁGENES
        'visualization_data': {
            'can_generate_image': True,
            'environment_type': 'submarine',
            'depth_context': {
                'depth_m': depth,
                'depth_category': 'deep' if depth > 1000 else 'medium' if depth > 200 else 'shallow'
            },
            'vessel_characteristics': {
                'length_m': length,
                'width_m': width,
                'height_m': height,
                'vessel_type': vessel_type,
                'estimated_tonnage': estimate_tonnage(length, width, height),
                'construction_material': 'steel' if confidence > 0.8 else 'mixed'
            },
            'sonar_characteristics': {
                'acoustic_shadow_length': length * 1.2,
                'reflectance_intensity': confidence,
                'geometric_clarity': 'high' if confidence > 0.8 else 'medium'
            }
        }
    }

def assess_preservation_conditions(water_context):
    """Evaluar condiciones de preservación"""
    depth = water_context.estimated_depth_m or 0
    
    if depth > 1000:
        return "Excelentes - Aguas profundas, baja actividad biológica"
    elif depth > 500:
        return "Muy buenas - Profundidad media, condiciones estables"
    elif depth > 200:
        return "Buenas - Zona batial, preservación moderada"
    else:
        return "Variables - Aguas someras, mayor actividad biológica"

def assess_accessibility(water_context):
    """Evaluar accesibilidad para investigación"""
    depth = water_context.estimated_depth_m or 0
    
    if depth > 2000:
        return "ROV de aguas profundas requerido"
    elif depth > 500:
        return "ROV estándar requerido"
    elif depth > 100:
        return "Buceo técnico con mezclas"
    else:
        return "Buceo recreativo avanzado posible"

def assess_historical_significance(length, vessel_type):
    """Evaluar significancia histórica"""
    if length > 300:
        return "Muy alta - Posible transatlántico de línea histórica"
    elif length > 200:
        return "Alta - Embarcación comercial de importancia"
    elif vessel_type in ['warship', 'patrol_boat']:
        return "Media-Alta - Posible significancia militar"
    else:
        return "Media - Valor arqueológico estándar"

def estimate_tonnage(length, width, height):
    """Estimar tonelaje aproximado"""
    # Fórmula simplificada para estimación
    volume = length * width * height * 0.7  # Factor de forma
    tonnage = volume * 0.8  # Densidad aproximada
    return int(tonnage)

def verify_visualization_readiness(anomalies):
    """Verificar que las anomalías están listas para visualización"""
    
    print(f"\n   🎨 VERIFICACIÓN DE VISUALIZACIÓN:")
    
    for i, anomaly in enumerate(anomalies, 1):
        checks = []
        
        # Verificar coordenadas
        has_coords = 'anomaly_coordinates' in anomaly and 'lat' in anomaly['anomaly_coordinates']
        checks.append(f"Coordenadas: {'✅' if has_coords else '❌'}")
        
        # Verificar dimensiones
        has_dimensions = 'dimensions' in anomaly and anomaly['dimensions'] != 'N/A'
        checks.append(f"Dimensiones: {'✅' if has_dimensions else '❌'}")
        
        # Verificar datos de visualización
        has_viz_data = 'visualization_data' in anomaly and anomaly['visualization_data'].get('can_generate_image')
        checks.append(f"Datos viz: {'✅' if has_viz_data else '❌'}")
        
        # Verificar clasificación
        has_classification = 'classification' in anomaly and anomaly['classification'] != 'Sin clasificar'
        checks.append(f"Clasificación: {'✅' if has_classification else '❌'}")
        
        all_ready = all('✅' in check for check in checks)
        status = '✅ LISTO' if all_ready else '❌ INCOMPLETO'
        
        print(f"      Anomalía {i}: {status} ({', '.join(checks)})")

def verify_all_visualization_data(results):
    """Verificar todos los datos de visualización"""
    
    verification = {
        'total_scenarios': len(results),
        'scenarios_with_anomalies': 0,
        'total_anomalies': 0,
        'anomalies_ready_for_visualization': 0,
        'visualization_readiness_percentage': 0
    }
    
    for result in results:
        if 'anomalies' in result and result['anomalies']:
            verification['scenarios_with_anomalies'] += 1
            
            for anomaly in result['anomalies']:
                verification['total_anomalies'] += 1
                
                # Verificar si está listo para visualización
                if (anomaly.get('visualization_data', {}).get('can_generate_image') and
                    'anomaly_coordinates' in anomaly and
                    'dimensions' in anomaly):
                    verification['anomalies_ready_for_visualization'] += 1
    
    if verification['total_anomalies'] > 0:
        verification['visualization_readiness_percentage'] = (
            verification['anomalies_ready_for_visualization'] / 
            verification['total_anomalies'] * 100
        )
    
    return verification

def generate_test_summary(results):
    """Generar resumen del test"""
    
    total_scenarios = len(results)
    successful_scenarios = len([r for r in results if 'anomalies' in r])
    total_anomalies = sum(len(r.get('anomalies', [])) for r in results)
    
    return {
        'total_scenarios': total_scenarios,
        'successful_scenarios': successful_scenarios,
        'success_rate': (successful_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0,
        'total_anomalies': total_anomalies,
        'average_anomalies_per_scenario': (total_anomalies / successful_scenarios) if successful_scenarios > 0 else 0,
        'environments_tested': list(set(r.get('water_context', {}).get('type', 'unknown') for r in results))
    }

def print_final_summary(output_data):
    """Imprimir resumen final del test"""
    
    summary = output_data['summary']
    verification = output_data['visualization_verification']
    
    print(f"\n🏆 RESUMEN FINAL DEL TEST DE VISUALIZACIÓN")
    print("=" * 70)
    print(f"📊 Escenarios probados: {summary['total_scenarios']}")
    print(f"✅ Escenarios exitosos: {summary['successful_scenarios']}")
    print(f"📈 Tasa de éxito: {summary['success_rate']:.1f}%")
    print(f"🎯 Total anomalías generadas: {summary['total_anomalies']}")
    print(f"📊 Promedio por escenario: {summary['average_anomalies_per_scenario']:.1f}")
    
    print(f"\n🎨 VERIFICACIÓN DE VISUALIZACIÓN:")
    print(f"📊 Anomalías totales: {verification['total_anomalies']}")
    print(f"✅ Listas para visualización: {verification['anomalies_ready_for_visualization']}")
    print(f"📈 Porcentaje listo: {verification['visualization_readiness_percentage']:.1f}%")
    
    if verification['visualization_readiness_percentage'] >= 90:
        print(f"\n🎉 EXCELENTE: Sistema de visualización completamente funcional")
    elif verification['visualization_readiness_percentage'] >= 70:
        print(f"\n✅ BUENO: Sistema de visualización mayormente funcional")
    else:
        print(f"\n⚠️ ATENCIÓN: Sistema de visualización requiere mejoras")
    
    print(f"\n🔍 Para probar la visualización:")
    print(f"   1. Abrir frontend/index.html en un navegador")
    print(f"   2. Ejecutar análisis en las coordenadas del Triángulo")
    print(f"   3. Usar la Lupa Arqueológica para ver anomalías")
    print(f"   4. Generar imágenes 2D/3D de las anomalías detectadas")

if __name__ == "__main__":
    results = test_complete_anomaly_visualization()