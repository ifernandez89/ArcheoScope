#!/usr/bin/env python3
"""
Test del Sistema de Zonas Prioritarias
Optimización Bayesiana de Prospección Arqueológica
"""

import requests
import json
from typing import Dict, Any

API_BASE = "http://localhost:8002"


def test_recommended_zones_buffer():
    """Test de zonas recomendadas con estrategia buffer"""
    
    print("="*80)
    print("🎯 TEST: Zonas Recomendadas - Estrategia BUFFER")
    print("="*80)
    print()
    
    # Región de Egipto (Valle del Nilo)
    # Debería tener muchos hot zones conocidos
    test_data = {
        "lat_min": 25.0,
        "lat_max": 30.0,
        "lon_min": 30.0,
        "lon_max": 35.0,
        "strategy": "buffer",
        "max_zones": 20
    }
    
    print(f"📍 Región: Valle del Nilo, Egipto")
    print(f"   Área: ~{(30-25) * (35-30) * 111.32**2:.0f} km²")
    print(f"   Estrategia: buffer (anillos alrededor de hot zones)")
    print()
    
    try:
        response = requests.post(
            f"{API_BASE}/archaeological-sites/recommended-zones",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Zonas generadas exitosamente")
            print()
            
            # Metadata
            metadata = result['metadata']
            print(f"📊 Metadata:")
            print(f"   Sitios analizados: {metadata['sites_analyzed']:,}")
            print(f"   Zonas alta prioridad: {metadata['high_priority_zones']}")
            print(f"   Zonas media prioridad: {metadata['medium_priority_zones']}")
            print(f"   Área total zonas: {metadata['total_area_km2']:.1f} km²")
            print(f"   Área región: {metadata['region_area_km2']:.1f} km²")
            print(f"   Cobertura: {metadata['coverage_percentage']:.1f}%")
            print(f"   Tiempo estimado: {metadata['estimated_total_time_hours']:.1f} horas")
            print()
            
            # Interpretación
            interpretation = result['interpretation']
            print(f"🔍 Interpretación:")
            print(f"   {interpretation['message']}")
            print(f"   {interpretation['efficiency']}")
            print(f"   {interpretation['time_estimate']}")
            print()
            
            # Mostrar primeras 5 zonas
            zones = result['zones'][:5]
            print(f"🗺️ Top 5 Zonas Prioritarias:")
            print()
            
            for i, zone in enumerate(zones, 1):
                print(f"{i}. {zone['zone_id']} - {zone['priority']}")
                print(f"   Área: {zone['area_km2']:.2f} km²")
                print(f"   Densidad cultural: {zone['cultural_density']:.3f}")
                print(f"   Centro: {zone['center']['lat']:.4f}, {zone['center']['lon']:.4f}")
                print(f"   Razones:")
                for reason in zone['reason']:
                    print(f"     • {reason}")
                print(f"   Instrumentos: {', '.join(zone['recommended_instruments'])}")
                print(f"   Tiempo estimado: {zone['estimated_analysis_time_minutes']} min")
                print()
            
            return True
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"   {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def test_recommended_zones_gradient():
    """Test de zonas recomendadas con estrategia gradient"""
    
    print("\n" + "="*80)
    print("🎯 TEST: Zonas Recomendadas - Estrategia GRADIENT")
    print("="*80)
    print()
    
    # Región de Perú (Andes)
    test_data = {
        "lat_min": -15.0,
        "lat_max": -10.0,
        "lon_min": -77.0,
        "lon_max": -72.0,
        "strategy": "gradient",
        "max_zones": 15
    }
    
    print(f"📍 Región: Andes, Perú")
    print(f"   Estrategia: gradient (zonas de transición)")
    print()
    
    try:
        response = requests.post(
            f"{API_BASE}/archaeological-sites/recommended-zones",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Zonas generadas exitosamente")
            print()
            
            metadata = result['metadata']
            print(f"📊 Cobertura: {metadata['coverage_percentage']:.1f}% del territorio")
            print(f"   Alta prioridad: {metadata['high_priority_zones']} zonas")
            print(f"   Media prioridad: {metadata['medium_priority_zones']} zonas")
            print()
            
            return True
        else:
            print(f"❌ Error HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def test_recommended_zones_gaps():
    """Test de zonas recomendadas con estrategia gaps"""
    
    print("\n" + "="*80)
    print("🎯 TEST: Zonas Recomendadas - Estrategia GAPS")
    print("="*80)
    print()
    
    # Región de Grecia
    test_data = {
        "lat_min": 37.0,
        "lat_max": 40.0,
        "lon_min": 21.0,
        "lon_max": 24.0,
        "strategy": "gaps",
        "max_zones": 10
    }
    
    print(f"📍 Región: Grecia")
    print(f"   Estrategia: gaps (huecos culturales improbables)")
    print()
    
    try:
        response = requests.post(
            f"{API_BASE}/archaeological-sites/recommended-zones",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Zonas generadas exitosamente")
            print()
            
            zones = result['zones']
            print(f"📊 {len(zones)} huecos culturales detectados")
            
            if len(zones) > 0:
                print(f"\n🔍 Primer hueco cultural:")
                zone = zones[0]
                print(f"   ID: {zone['zone_id']}")
                print(f"   Área: {zone['area_km2']:.2f} km²")
                print(f"   Razones:")
                for reason in zone['reason']:
                    print(f"     • {reason}")
            
            return True
        else:
            print(f"❌ Error HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def test_zone_analysis_workflow():
    """Test del workflow completo: zonas → análisis"""
    
    print("\n" + "="*80)
    print("🔄 TEST: Workflow Completo - Zonas → Análisis")
    print("="*80)
    print()
    
    # 1. Obtener zonas recomendadas
    print("📍 Paso 1: Obtener zonas recomendadas (Giza)")
    
    zones_data = {
        "lat_min": 29.9,
        "lat_max": 30.1,
        "lon_min": 31.0,
        "lon_max": 31.2,
        "strategy": "buffer",
        "max_zones": 5
    }
    
    try:
        zones_response = requests.post(
            f"{API_BASE}/archaeological-sites/recommended-zones",
            json=zones_data,
            timeout=30
        )
        
        if zones_response.status_code != 200:
            print(f"❌ Error obteniendo zonas: {zones_response.status_code}")
            return False
        
        zones_result = zones_response.json()
        zones = zones_result['zones']
        
        print(f"✅ {len(zones)} zonas obtenidas")
        print()
        
        if len(zones) == 0:
            print("⚠️ No hay zonas para analizar")
            return True
        
        # 2. Analizar primera zona de alta prioridad
        high_priority_zones = [z for z in zones if z['priority'] == 'high_priority']
        
        if len(high_priority_zones) == 0:
            print("⚠️ No hay zonas de alta prioridad")
            return True
        
        zone = high_priority_zones[0]
        
        print(f"📍 Paso 2: Analizar zona {zone['zone_id']}")
        print(f"   Prioridad: {zone['priority']}")
        print(f"   Área: {zone['area_km2']:.2f} km²")
        print()
        
        # Preparar análisis
        analysis_data = {
            "lat_min": zone['bbox']['lat_min'],
            "lat_max": zone['bbox']['lat_max'],
            "lon_min": zone['bbox']['lon_min'],
            "lon_max": zone['bbox']['lon_max'],
            "region_name": f"Priority Zone {zone['zone_id']}"
        }
        
        # Ejecutar análisis
        analysis_response = requests.post(
            f"{API_BASE}/analyze",
            json=analysis_data,
            timeout=60
        )
        
        if analysis_response.status_code == 200:
            analysis_result = analysis_response.json()
            
            print("✅ Análisis completado")
            print()
            print(f"🎯 Resultados:")
            print(f"   Ambiente: {analysis_result.get('environment_type', 'N/A')}")
            print(f"   Probabilidad arqueológica: {analysis_result.get('archaeological_probability', 0):.2%}")
            print(f"   Confianza: {analysis_result.get('confidence_level', 'N/A')}")
            print(f"   Sitio conocido: {analysis_result.get('known_site_name', 'N/A')}")
            print()
            
            return True
        else:
            print(f"❌ Error en análisis: {analysis_response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def test_optimization_metrics():
    """Test de métricas de optimización"""
    
    print("\n" + "="*80)
    print("📊 TEST: Métricas de Optimización Bayesiana")
    print("="*80)
    print()
    
    # Comparar diferentes estrategias en la misma región
    region = {
        "lat_min": 29.0,
        "lat_max": 31.0,
        "lon_min": 30.0,
        "lon_max": 32.0,
        "max_zones": 30
    }
    
    strategies = ['buffer', 'gradient', 'gaps']
    results = {}
    
    for strategy in strategies:
        print(f"🔍 Probando estrategia: {strategy}")
        
        test_data = {**region, "strategy": strategy}
        
        try:
            response = requests.post(
                f"{API_BASE}/archaeological-sites/recommended-zones",
                json=test_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                metadata = result['metadata']
                
                results[strategy] = {
                    'zones': len(result['zones']),
                    'high_priority': metadata['high_priority_zones'],
                    'coverage': metadata['coverage_percentage'],
                    'time_hours': metadata['estimated_total_time_hours']
                }
                
                print(f"   ✅ {results[strategy]['zones']} zonas")
                print(f"   ✅ Cobertura: {results[strategy]['coverage']:.1f}%")
                print()
            else:
                print(f"   ❌ Error: {response.status_code}")
                print()
        
        except Exception as e:
            print(f"   ❌ Excepción: {e}")
            print()
    
    # Comparar resultados
    if len(results) > 0:
        print("📊 Comparación de Estrategias:")
        print()
        print(f"{'Estrategia':<12} {'Zonas':<8} {'Alta Prior.':<12} {'Cobertura':<12} {'Tiempo (h)':<12}")
        print("-" * 60)
        
        for strategy, data in results.items():
            print(f"{strategy:<12} {data['zones']:<8} {data['high_priority']:<12} "
                  f"{data['coverage']:<11.1f}% {data['time_hours']:<11.1f}")
        
        print()
        return True
    
    return False


def main():
    """Función principal"""
    
    print("="*80)
    print("🧪 SUITE DE TESTS: Sistema de Zonas Prioritarias")
    print("   Optimización Bayesiana de Prospección Arqueológica")
    print("="*80)
    print()
    print("Tests a ejecutar:")
    print("  1. Zonas recomendadas - Estrategia BUFFER")
    print("  2. Zonas recomendadas - Estrategia GRADIENT")
    print("  3. Zonas recomendadas - Estrategia GAPS")
    print("  4. Workflow completo (zonas → análisis)")
    print("  5. Métricas de optimización")
    print()
    
    results = []
    
    # Test 1: Buffer
    results.append(("Estrategia BUFFER", test_recommended_zones_buffer()))
    
    # Test 2: Gradient
    results.append(("Estrategia GRADIENT", test_recommended_zones_gradient()))
    
    # Test 3: Gaps
    results.append(("Estrategia GAPS", test_recommended_zones_gaps()))
    
    # Test 4: Workflow
    results.append(("Workflow completo", test_zone_analysis_workflow()))
    
    # Test 5: Métricas
    results.append(("Métricas de optimización", test_optimization_metrics()))
    
    # Resumen
    print("\n" + "="*80)
    print("📋 RESUMEN DE TESTS")
    print("="*80)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Resultado: {passed}/{total} tests pasados ({passed/total*100:.0f}%)")
    print()
    
    if passed == total:
        print("🎉 ¡Todos los tests pasaron!")
        print()
        print("🚀 Sistema de Zonas Prioritarias OPERATIVO")
        print()
        print("Próximos pasos:")
        print("  1. Generar zonas para regiones de interés")
        print("  2. Ejecutar análisis en zonas de alta prioridad")
        print("  3. Validar resultados con datos LiDAR")
        print("  4. Iterar y refinar estrategias")
        return 0
    else:
        print("⚠️ Algunos tests fallaron")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
