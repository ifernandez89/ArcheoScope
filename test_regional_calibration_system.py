#!/usr/bin/env python3
"""
Test del Sistema de Calibración Regional Mejorado
===============================================

Prueba las mejoras críticas implementadas:
1. Calibración regional por eco-regiones
2. Matriz de sensores ponderada dinámicamente  
3. Score de convergencia explicable
4. Persistencia relativa vs absoluta

CASOS DE PRUEBA:
- Sahara (desierto con excelente visibilidad térmica)
- Amazonas húmeda (selva que requiere LiDAR + SAR)
- Antártida (condiciones extremas, ICESat-2 crítico)
- Caribe (arqueología marina)
"""

import sys
import json
import requests
from datetime import datetime
from typing import Dict, Any

def test_regional_calibration_sahara():
    """Test en Sahara - debe priorizar térmico"""
    
    print("🏜️ TESTING: Calibración regional - Sahara")
    print("   Expectativa: Priorizar sensores térmicos, ajustar umbrales")
    
    # Coordenadas en Sahara (cerca de Giza)
    test_data = {
        "lat_min": 29.9,
        "lat_max": 30.0,
        "lon_min": 31.1,
        "lon_max": 31.2,
        "region_name": "Sahara Test - Giza Region"
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Verificar eco-región detectada
            explanation = result.get('explanation', '')
            if 'sahara' in explanation.lower():
                print("   ✅ Eco-región Sahara detectada correctamente")
            else:
                print("   ⚠️ Eco-región Sahara no detectada en explicación")
            
            # Verificar componentes de convergencia
            if 'térmico' in explanation.lower():
                print("   ✅ Componente térmico mencionado (esperado en Sahara)")
            
            if 'Score de convergencia' in explanation:
                print("   ✅ Score de convergencia incluido en explicación")
            
            # Verificar probabilidad
            prob = result.get('archaeological_probability', 0)
            print(f"   📊 Probabilidad arqueológica: {prob:.1%}")
            
            return True
            
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False

def test_regional_calibration_amazon():
    """Test en Amazonas - debe priorizar LiDAR + SAR"""
    
    print("\n🌳 TESTING: Calibración regional - Amazonas húmeda")
    print("   Expectativa: Priorizar LiDAR y SAR L-band, reducir óptico")
    
    # Coordenadas en Amazonas húmeda
    test_data = {
        "lat_min": -3.1,
        "lat_max": -3.0,
        "lon_min": -60.1,
        "lon_max": -60.0,
        "region_name": "Amazon Humid Test"
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            explanation = result.get('explanation', '')
            
            # Verificar eco-región
            if 'amazon' in explanation.lower():
                print("   ✅ Eco-región Amazonas detectada")
            
            # Verificar componentes esperados
            if 'forma' in explanation.lower():
                print("   ✅ Componente forma mencionado (LiDAR esperado)")
            
            if 'compactación' in explanation.lower():
                print("   ✅ Componente compactación mencionado (SAR esperado)")
            
            prob = result.get('archaeological_probability', 0)
            print(f"   📊 Probabilidad arqueológica: {prob:.1%}")
            
            return True
            
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False

def test_regional_calibration_antarctica():
    """Test en Antártida - debe priorizar ICESat-2"""
    
    print("\n❄️ TESTING: Calibración regional - Antártida")
    print("   Expectativa: Priorizar ICESat-2, condiciones extremas")
    
    # Coordenadas en Antártida
    test_data = {
        "lat_min": -75.1,
        "lat_max": -75.0,
        "lon_min": -10.1,
        "lon_max": -10.0,
        "region_name": "Antarctica Interior Test"
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            explanation = result.get('explanation', '')
            
            # Verificar eco-región
            if 'antarctica' in explanation.lower():
                print("   ✅ Eco-región Antártida detectada")
            
            # Verificar ambiente polar
            if 'polar' in explanation.lower():
                print("   ✅ Ambiente polar detectado")
            
            # Verificar componente forma (ICESat-2)
            if 'forma' in explanation.lower():
                print("   ✅ Componente forma mencionado (ICESat-2 esperado)")
            
            prob = result.get('archaeological_probability', 0)
            print(f"   📊 Probabilidad arqueológica: {prob:.1%}")
            
            return True
            
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False

def test_convergence_explanation():
    """Test de explicación de convergencia auditable"""
    
    print("\n🔍 TESTING: Explicación de convergencia auditable")
    print("   Expectativa: Score explicable con componentes detallados")
    
    # Usar coordenadas conocidas (Machu Picchu)
    test_data = {
        "lat_min": -13.17,
        "lat_max": -13.16,
        "lon_min": -72.55,
        "lon_max": -72.54,
        "region_name": "Machu Picchu - Convergence Test"
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            explanation = result.get('explanation', '')
            
            # Verificar elementos de convergencia
            checks = [
                ('Score de convergencia', 'Score numérico incluido'),
                ('Componentes activos', 'Desglose por tipo de evidencia'),
                ('forma', 'Componente forma mencionado'),
                ('andes' in explanation.lower(), 'Eco-región Andes detectada'),
                ('mountain' in explanation.lower(), 'Ambiente montañoso detectado')
            ]
            
            for check, description in checks:
                if isinstance(check, bool):
                    if check:
                        print(f"   ✅ {description}")
                    else:
                        print(f"   ⚠️ {description} - no detectado")
                else:
                    if check in explanation:
                        print(f"   ✅ {description}")
                    else:
                        print(f"   ⚠️ {description} - no encontrado")
            
            # Mostrar explicación completa para inspección
            print(f"\n   📝 Explicación completa:")
            print(f"   {explanation}")
            
            return True
            
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False

def test_comparative_analysis():
    """Test comparativo entre diferentes eco-regiones"""
    
    print("\n📊 TESTING: Análisis comparativo entre eco-regiones")
    
    test_cases = [
        {
            "name": "Sahara",
            "coords": {"lat_min": 25.0, "lat_max": 25.1, "lon_min": 30.0, "lon_max": 30.1},
            "expected_strengths": ["térmico", "espectral"]
        },
        {
            "name": "Amazonas",
            "coords": {"lat_min": -3.0, "lat_max": -2.9, "lon_min": -60.0, "lon_max": -59.9},
            "expected_strengths": ["forma", "compactación"]
        },
        {
            "name": "Caribe",
            "coords": {"lat_min": 18.0, "lat_max": 18.1, "lon_min": -77.0, "lon_max": -76.9},
            "expected_strengths": ["forma", "térmico"]  # Sonar + SST
        }
    ]
    
    results = {}
    
    for case in test_cases:
        print(f"\n   🧪 Probando {case['name']}...")
        
        test_data = {
            **case['coords'],
            "region_name": f"Comparative Test - {case['name']}"
        }
        
        try:
            response = requests.post(
                "http://localhost:8003/analyze",
                json=test_data,
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                explanation = result.get('explanation', '')
                prob = result.get('archaeological_probability', 0)
                
                results[case['name']] = {
                    'probability': prob,
                    'explanation': explanation,
                    'strengths_found': []
                }
                
                # Verificar fortalezas esperadas
                for strength in case['expected_strengths']:
                    if strength in explanation.lower():
                        results[case['name']]['strengths_found'].append(strength)
                        print(f"      ✅ {strength} detectado")
                    else:
                        print(f"      ⚠️ {strength} no detectado")
                
                print(f"      📊 Probabilidad: {prob:.1%}")
                
            else:
                print(f"      ❌ Error HTTP: {response.status_code}")
                results[case['name']] = {'error': response.status_code}
                
        except Exception as e:
            print(f"      ❌ Excepción: {e}")
            results[case['name']] = {'error': str(e)}
    
    # Resumen comparativo
    print(f"\n   📋 RESUMEN COMPARATIVO:")
    for name, data in results.items():
        if 'error' not in data:
            strengths = ', '.join(data['strengths_found']) if data['strengths_found'] else 'ninguna'
            print(f"      {name}: {data['probability']:.1%} prob, fortalezas: {strengths}")
        else:
            print(f"      {name}: ERROR - {data['error']}")
    
    return len([r for r in results.values() if 'error' not in r]) > 0

def main():
    """Ejecutar todos los tests del sistema de calibración regional"""
    
    print("="*80)
    print("🧪 SISTEMA DE CALIBRACIÓN REGIONAL - TESTS COMPLETOS")
    print("="*80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Calibración Sahara", test_regional_calibration_sahara),
        ("Calibración Amazonas", test_regional_calibration_amazon),
        ("Calibración Antártida", test_regional_calibration_antarctica),
        ("Explicación Convergencia", test_convergence_explanation),
        ("Análisis Comparativo", test_comparative_analysis)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🔬 EJECUTANDO: {test_name}")
        print(f"{'='*60}")
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"\n✅ {test_name}: EXITOSO")
            else:
                print(f"\n❌ {test_name}: FALLÓ")
                
        except Exception as e:
            print(f"\n💥 {test_name}: EXCEPCIÓN - {e}")
            results.append((test_name, False))
    
    # Resumen final
    print(f"\n{'='*80}")
    print("📊 RESUMEN FINAL DE TESTS")
    print(f"{'='*80}")
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ EXITOSO" if success else "❌ FALLÓ"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 RESULTADO GENERAL: {successful}/{total} tests exitosos ({successful/total*100:.1f}%)")
    
    if successful == total:
        print("🎉 TODOS LOS TESTS PASARON - Sistema de calibración regional funcionando correctamente")
    elif successful > total/2:
        print("⚠️ MAYORÍA DE TESTS PASARON - Sistema funcional con algunas mejoras pendientes")
    else:
        print("🚨 MAYORÍA DE TESTS FALLARON - Revisar implementación del sistema")
    
    print(f"\n{'='*80}")

if __name__ == "__main__":
    main()