#!/usr/bin/env python3
"""
Test completo de integración del sistema de historial de anomalías
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from water.water_detector import WaterDetector
from water.submarine_archaeology import SubmarineArchaeologyEngine

def test_complete_integration():
    """Test completo de integración del sistema"""
    
    print("🔬 TEST COMPLETO DE INTEGRACIÓN - SISTEMA DE HISTORIAL")
    print("=" * 65)
    print("Verificando que todos los componentes funcionen correctamente")
    print("=" * 65)
    
    # 1. Test de componentes backend
    print("\n🔧 FASE 1: VERIFICACIÓN DE COMPONENTES BACKEND")
    print("-" * 50)
    
    try:
        water_detector = WaterDetector()
        submarine_engine = SubmarineArchaeologyEngine()
        print("✅ Componentes backend inicializados correctamente")
    except Exception as e:
        print(f"❌ Error inicializando backend: {e}")
        return False
    
    # 2. Test de detección de agua
    print("\n🌊 FASE 2: TEST DE DETECCIÓN DE AGUA")
    print("-" * 50)
    
    test_coordinates = [
        {"name": "Caribe Norte", "lat": 25.800, "lng": -70.000},
        {"name": "Caribe Sur", "lat": 25.300, "lng": -70.500},
        {"name": "Caribe Centro", "lat": 25.550, "lng": -70.250}
    ]
    
    water_results = []
    
    for coord in test_coordinates:
        try:
            water_context = water_detector.detect_water_context(coord['lat'], coord['lng'])
            
            result = {
                'name': coord['name'],
                'coordinates': coord,
                'water_detected': water_context.is_water,
                'water_type': water_context.water_type.value if water_context.water_type else None,
                'depth_m': water_context.estimated_depth_m,
                'archaeological_potential': water_context.archaeological_potential
            }
            
            water_results.append(result)
            
            status = "✅" if water_context.is_water else "❌"
            print(f"{status} {coord['name']}: {water_context.water_type.value if water_context.water_type else 'No water'}")
            
        except Exception as e:
            print(f"❌ Error en {coord['name']}: {e}")
            water_results.append({
                'name': coord['name'],
                'coordinates': coord,
                'error': str(e)
            })
    
    # 3. Test de análisis submarino
    print("\n🚢 FASE 3: TEST DE ANÁLISIS SUBMARINO")
    print("-" * 50)
    
    submarine_results = []
    
    for result in water_results:
        if result.get('water_detected'):
            try:
                coord = result['coordinates']
                
                # Recrear contexto de agua
                water_context = water_detector.detect_water_context(coord['lat'], coord['lng'])
                
                # Definir área de análisis
                bounds = (
                    coord['lat'] - 0.01,
                    coord['lat'] + 0.01,
                    coord['lng'] - 0.01,
                    coord['lng'] + 0.01
                )
                
                # Análisis submarino
                analysis = submarine_engine.analyze_submarine_area(water_context, bounds)
                
                submarine_result = {
                    'name': result['name'],
                    'coordinates': coord,
                    'volumetric_anomalies': analysis['volumetric_anomalies'],
                    'wreck_candidates': len(analysis['wreck_candidates']),
                    'instruments_used': len(analysis['instruments_used']),
                    'high_priority_targets': analysis['summary']['high_priority_targets']
                }
                
                submarine_results.append(submarine_result)
                
                print(f"✅ {result['name']}: {analysis['volumetric_anomalies']} anomalías, {len(analysis['wreck_candidates'])} candidatos")
                
            except Exception as e:
                print(f"❌ Error en análisis submarino de {result['name']}: {e}")
                submarine_results.append({
                    'name': result['name'],
                    'coordinates': result['coordinates'],
                    'error': str(e)
                })
    
    # 4. Test de formato de datos para historial
    print("\n📋 FASE 4: TEST DE FORMATO DE DATOS PARA HISTORIAL")
    print("-" * 50)
    
    history_data = []
    
    for sub_result in submarine_results:
        if 'error' not in sub_result:
            try:
                # Simular datos de análisis para el historial
                analysis_data = {
                    'statistical_results': {
                        'multibeam_sonar': {'archaeological_probability': 0.85},
                        'side_scan_sonar': {'archaeological_probability': 0.78},
                        'magnetometer': {'archaeological_probability': 0.72},
                        'acoustic_reflectance': {'archaeological_probability': 0.80}
                    },
                    'summary': {
                        'total_instruments': sub_result['instruments_used'],
                        'analysis_type': 'submarine_archaeology'
                    }
                }
                
                # Simular anomalías detectadas
                anomalies_detected = []
                for i in range(min(3, sub_result['wreck_candidates'])):  # Máximo 3 para el ejemplo
                    anomaly = {
                        'type': 'submarine_wreck',
                        'name': f'Candidato Submarino {i+1}',
                        'icon': '🚢',
                        'description': f'Estructura submarina detectada por análisis multi-sensor',
                        'confidence': 0.75 + (i * 0.05),  # Variación en confianza
                        'evidence': 'Detección por sonar multihaz y magnetómetro',
                        'color': '#dc3545'
                    }
                    anomalies_detected.append(anomaly)
                
                history_entry = {
                    'name': sub_result['name'],
                    'coordinates': sub_result['coordinates'],
                    'analysis_data': analysis_data,
                    'anomalies_detected': anomalies_detected,
                    'metadata': {
                        'resolution': '10m',
                        'analysisType': 'submarine_archaeology',
                        'timestamp': datetime.now().isoformat()
                    }
                }
                
                history_data.append(history_entry)
                
                print(f"✅ {sub_result['name']}: Datos formateados para historial ({len(anomalies_detected)} anomalías)")
                
            except Exception as e:
                print(f"❌ Error formateando datos de {sub_result['name']}: {e}")
    
    # 5. Guardar resultados completos
    print("\n💾 FASE 5: GUARDADO DE RESULTADOS")
    print("-" * 50)
    
    complete_results = {
        'test_info': {
            'test_name': 'Complete Integration Test',
            'timestamp': datetime.now().isoformat(),
            'coordinates_tested': len(test_coordinates)
        },
        'water_detection_results': water_results,
        'submarine_analysis_results': submarine_results,
        'history_formatted_data': history_data,
        'summary': {
            'water_points_detected': len([r for r in water_results if r.get('water_detected')]),
            'successful_submarine_analyses': len([r for r in submarine_results if 'error' not in r]),
            'total_anomalies_detected': sum(len(h['anomalies_detected']) for h in history_data),
            'ready_for_history_system': len(history_data)
        }
    }
    
    output_file = f"complete_integration_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(complete_results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Resultados completos guardados en: {output_file}")
        
    except Exception as e:
        print(f"❌ Error guardando resultados: {e}")
    
    # 6. Resumen final
    print(f"\n🏆 RESUMEN FINAL DEL TEST DE INTEGRACIÓN")
    print("=" * 65)
    
    summary = complete_results['summary']
    
    print(f"📊 Estadísticas del Test:")
    print(f"   • Coordenadas probadas: {len(test_coordinates)}")
    print(f"   • Puntos con agua detectados: {summary['water_points_detected']}")
    print(f"   • Análisis submarinos exitosos: {summary['successful_submarine_analyses']}")
    print(f"   • Total anomalías detectadas: {summary['total_anomalies_detected']}")
    print(f"   • Entradas listas para historial: {summary['ready_for_history_system']}")
    
    # Verificar si el test fue exitoso
    success_rate = summary['successful_submarine_analyses'] / len(test_coordinates) if len(test_coordinates) > 0 else 0
    
    if success_rate >= 0.8:  # 80% de éxito
        print(f"\n✅ TEST DE INTEGRACIÓN EXITOSO")
        print(f"   Tasa de éxito: {success_rate:.1%}")
        print(f"   El sistema está listo para uso en producción")
    elif success_rate >= 0.5:  # 50% de éxito
        print(f"\n⚠️ TEST DE INTEGRACIÓN PARCIALMENTE EXITOSO")
        print(f"   Tasa de éxito: {success_rate:.1%}")
        print(f"   El sistema funciona pero requiere ajustes")
    else:
        print(f"\n❌ TEST DE INTEGRACIÓN FALLIDO")
        print(f"   Tasa de éxito: {success_rate:.1%}")
        print(f"   El sistema requiere revisión antes del uso")
    
    print(f"\n🔍 Para probar el frontend:")
    print(f"   1. Abrir 'test_history_frontend.html' en un navegador")
    print(f"   2. Ejecutar los tests de JavaScript")
    print(f"   3. Verificar que el sistema de historial funcione correctamente")
    
    return success_rate >= 0.8

if __name__ == "__main__":
    success = test_complete_integration()
    sys.exit(0 if success else 1)