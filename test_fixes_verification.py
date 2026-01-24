#!/usr/bin/env python3
"""
Test para verificar que las correcciones funcionan correctamente
"""

import sys
import json
from backend.water.water_detector import WaterDetector
from backend.water.submarine_archaeology import SubmarineArchaeologyEngine

def test_deterministic_detection():
    """
    PRUEBA CRÍTICA: Verificar que las mismas coordenadas producen SIEMPRE los mismos resultados
    """
    print("=" * 80)
    print("🧪 PRUEBA DE DETECCIÓN DETERMINÍSTICA")
    print("=" * 80)
    
    # Coordenadas de prueba (Caribe)
    test_coords = [
        (18.5, -77.5),  # Jamaica
        (21.3, -157.9), # Pearl Harbor
        (40.5, -69.9),  # Andrea Doria
    ]
    
    water_detector = WaterDetector()
    submarine_engine = SubmarineArchaeologyEngine()
    
    for lat, lon in test_coords:
        print(f"\n📍 Probando coordenadas: {lat}, {lon}")
        print("-" * 80)
        
        # Ejecutar 3 veces las MISMAS coordenadas
        results = []
        for run in range(1, 4):
            print(f"\n   Ejecución #{run}...")
            
            # Detectar contexto de agua
            water_context = water_detector.detect_water_context(lat, lon)
            
            if not water_context.is_water:
                print(f"   ⚠️ No es agua, saltando...")
                continue
            
            # Analizar área submarina
            bounds = (lat - 0.1, lat + 0.1, lon - 0.1, lon + 0.1)
            analysis = submarine_engine.analyze_submarine_area(water_context, bounds)
            
            num_anomalies = len(analysis.get('wreck_candidates', []))
            results.append(num_anomalies)
            
            print(f"   ✓ Anomalías detectadas: {num_anomalies}")
            
            # Mostrar detalles de primera anomalía si existe
            if num_anomalies > 0:
                first = analysis['wreck_candidates'][0]
                dims = first['signature']
                print(f"      - Dimensiones: {dims['length_m']:.1f}m x {dims['width_m']:.1f}m x {dims['height_m']:.1f}m")
                print(f"      - Confianza: {dims['detection_confidence']:.2f}")
        
        # VERIFICAR CONSISTENCIA
        print(f"\n   📊 RESULTADOS DE LAS 3 EJECUCIONES: {results}")
        
        if len(set(results)) == 1:
            print(f"   ✅ ÉXITO: Todas las ejecuciones produjeron {results[0]} anomalías")
        else:
            print(f"   ❌ FALLO: Resultados inconsistentes! {results}")
            print(f"   ⚠️ ESTO ES INACEPTABLE - El instrumento debe ser determinístico")
            return False
    
    print("\n" + "=" * 80)
    print("✅ TODAS LAS PRUEBAS PASARON - DETECCIÓN DETERMINÍSTICA VERIFICADA")
    print("=" * 80)
    return True

def test_javascript_syntax():
    """
    Verificar que el archivo JavaScript no tiene errores de sintaxis
    """
    print("\n" + "=" * 80)
    print("🧪 VERIFICACIÓN DE SINTAXIS JAVASCRIPT")
    print("=" * 80)
    
    try:
        with open('frontend/professional_3d_viewer.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que no hay funciones duplicadas (buscar definiciones completas)
        function_defs = content.count('updateAIInterpretation() {')
        if function_defs > 1:
            print(f"❌ FALLO: Función updateAIInterpretation() está duplicada ({function_defs} veces)")
            return False
        
        # Verificar que el archivo termina correctamente
        if not content.strip().endswith('}'):
            print("❌ FALLO: El archivo no termina correctamente")
            return False
        
        # Contar llaves para verificar balance
        open_braces = content.count('{')
        close_braces = content.count('}')
        
        print(f"   Llaves abiertas: {open_braces}")
        print(f"   Llaves cerradas: {close_braces}")
        print(f"   Definiciones de updateAIInterpretation: {function_defs}")
        
        if open_braces != close_braces:
            print(f"❌ FALLO: Llaves desbalanceadas ({open_braces} vs {close_braces})")
            return False
        
        print("✅ ÉXITO: Sintaxis JavaScript verificada")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("\n🔬 INICIANDO VERIFICACIÓN DE CORRECCIONES\n")
    
    # Test 1: Sintaxis JavaScript
    js_ok = test_javascript_syntax()
    
    # Test 2: Detección determinística
    det_ok = test_deterministic_detection()
    
    print("\n" + "=" * 80)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 80)
    print(f"   JavaScript Syntax: {'✅ PASS' if js_ok else '❌ FAIL'}")
    print(f"   Detección Determinística: {'✅ PASS' if det_ok else '❌ FAIL'}")
    print("=" * 80)
    
    if js_ok and det_ok:
        print("\n🎉 TODAS LAS CORRECCIONES VERIFICADAS EXITOSAMENTE")
        sys.exit(0)
    else:
        print("\n⚠️ ALGUNAS CORRECCIONES FALLARON - REVISAR")
        sys.exit(1)
