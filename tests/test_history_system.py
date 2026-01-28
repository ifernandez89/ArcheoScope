#!/usr/bin/env python3
"""
Test simple del sistema de historial de anomalías
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from water.water_detector import WaterDetector
from water.submarine_archaeology import SubmarineArchaeologyEngine

def test_simple_history_system():
    """Test simple del sistema de historial"""
    
    print("🧪 TEST SIMPLE DEL SISTEMA DE HISTORIAL")
    print("=" * 50)
    
    # Coordenadas de prueba simples
    test_coords = [
        {"name": "Test Point 1", "lat": 25.800, "lon": -70.000},
        {"name": "Test Point 2", "lat": 25.300, "lon": -70.500}
    ]
    
    water_detector = WaterDetector()
    submarine_engine = SubmarineArchaeologyEngine()
    
    results = []
    
    for coord in test_coords:
        print(f"\n📍 Analizando: {coord['name']} ({coord['lat']}, {coord['lon']})")
        
        try:
            # Detectar agua
            water_context = water_detector.detect_water_context(coord['lat'], coord['lon'])
            
            if water_context.is_water:
                print(f"   ✅ Agua detectada: {water_context.water_type.value}")
                
                # Análisis submarino básico
                bounds = (
                    coord['lat'] - 0.01,
                    coord['lat'] + 0.01,
                    coord['lon'] - 0.01,
                    coord['lon'] + 0.01
                )
                
                submarine_results = submarine_engine.analyze_submarine_area(water_context, bounds)
                
                print(f"   📊 Anomalías detectadas: {submarine_results['volumetric_anomalies']}")
                print(f"   🚢 Candidatos a naufragios: {len(submarine_results['wreck_candidates'])}")
                
                # Crear datos para el historial
                analysis_data = {
                    'statistical_results': {
                        'multibeam_sonar': {'archaeological_probability': 0.85},
                        'magnetometer': {'archaeological_probability': 0.72}
                    }
                }
                
                # Simular anomalías detectadas
                anomalies_detected = []
                for i, candidate in enumerate(submarine_results['wreck_candidates'][:3], 1):  # Máximo 3
                    anomaly = {
                        'type': 'submarine_wreck',
                        'name': f'Candidato Submarino {i}',
                        'icon': '🚢',
                        'description': f'Estructura de {candidate["signature"]["length_m"]:.1f}m x {candidate["signature"]["width_m"]:.1f}m',
                        'confidence': candidate['signature']['detection_confidence'],
                        'evidence': 'Detección multi-sensor submarina',
                        'color': '#dc3545'
                    }
                    anomalies_detected.append(anomaly)
                
                result = {
                    'coordinates': coord,
                    'water_detected': True,
                    'analysis_data': analysis_data,
                    'anomalies_detected': anomalies_detected,
                    'timestamp': datetime.now().isoformat()
                }
                
                results.append(result)
                
            else:
                print(f"   ❌ No se detectó agua")
                result = {
                    'coordinates': coord,
                    'water_detected': False,
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            result = {
                'coordinates': coord,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            results.append(result)
    
    # Guardar resultados
    output_file = f"history_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    
    # Resumen
    water_points = [r for r in results if r.get('water_detected')]
    total_anomalies = sum(len(r.get('anomalies_detected', [])) for r in water_points)
    
    print(f"\n📊 RESUMEN:")
    print(f"   Puntos analizados: {len(results)}")
    print(f"   Puntos con agua: {len(water_points)}")
    print(f"   Total anomalías: {total_anomalies}")
    
    print(f"\n✅ Test del sistema de historial completado!")
    
    return results

if __name__ == "__main__":
    test_simple_history_system()