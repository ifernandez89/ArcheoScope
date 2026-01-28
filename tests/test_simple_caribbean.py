#!/usr/bin/env python3
"""
Test simple para las coordenadas del Caribe
"""

import sys
from pathlib import Path

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from water.water_detector import WaterDetector
from water.submarine_archaeology import SubmarineArchaeologyEngine

def test_simple_caribbean():
    """Test simple para coordenadas del Caribe"""
    
    print("🏝️ TEST SIMPLE - COORDENADAS DEL CARIBE")
    print("=" * 50)
    
    # Coordenadas específicas
    lat, lon = 25.800, -70.000
    
    print(f"Analizando: {lat}°N, {lon}°W")
    
    # Detectar agua
    water_detector = WaterDetector()
    water_context = water_detector.detect_water_context(lat, lon)
    
    print(f"\n🌊 DETECCIÓN DE AGUA:")
    print(f"   Agua detectada: {water_context.is_water}")
    
    if water_context.is_water:
        print(f"   Tipo: {water_context.water_type.value}")
        print(f"   Profundidad: {water_context.estimated_depth_m:.0f}m")
        print(f"   Potencial arqueológico: {water_context.archaeological_potential}")
        
        # Análisis básico sin errores
        try:
            submarine_engine = SubmarineArchaeologyEngine()
            
            # Área pequeña para análisis
            bounds = (lat - 0.01, lat + 0.01, lon - 0.01, lon + 0.01)
            
            print(f"\n🔍 ANÁLISIS SUBMARINO:")
            results = submarine_engine.analyze_submarine_area(water_context, bounds)
            
            print(f"   Instrumentos: {len(results['instruments_used'])}")
            print(f"   Anomalías: {results['volumetric_anomalies']}")
            print(f"   Candidatos: {len(results['wreck_candidates'])}")
            
            if results['wreck_candidates']:
                print(f"\n⚓ PRIMER CANDIDATO:")
                candidate = results['wreck_candidates'][0]
                print(f"   ID: {candidate['anomaly_id']}")
                print(f"   Coordenadas: {candidate['coordinates']}")
                
                sig = candidate['signature']
                print(f"   Dimensiones: {sig['length_m']:.1f}m x {sig['width_m']:.1f}m")
                print(f"   Confianza: {sig['detection_confidence']:.2f}")
                
                # Clasificación de embarcación
                vessel_types = candidate['vessel_type_probability']
                if vessel_types:
                    top_type = max(vessel_types, key=vessel_types.get)
                    print(f"   Tipo probable: {top_type} ({vessel_types[top_type]:.1%})")
                
                print(f"   Prioridad: {candidate['archaeological_priority']}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n✅ Test completado!")

if __name__ == "__main__":
    test_simple_caribbean()