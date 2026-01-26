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
    print("🎯 TEST: Zonas Recomendadas - Estrategia BUFFER + Scoring LiDAR")
    print("="*80)
    print()
    
    # Región de Petén, Guatemala (alta probabilidad de LiDAR)
    test_data = {
        "lat_min": 16.0,
        "lat_max": 18.0,
        "lon_min": -91.0,
        "lon_max": -89.0,
        "strategy": "buffer",
        "max_zones": 20,
        "lidar_priority": True,
        "include_scoring": True
    }
    
    print(f"📍 Región: Petén, Guatemala (Maya Lowlands)")
    print(f"   Área: ~{(18-16) * (91-89) * 111.32**2:.0f} km²")
    print(f"   Estrategia: buffer + scoring LiDAR")
    print(f"   Prioridad LiDAR: Activada")
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
            print(f"   Zonas CRITICAL: {metadata['critical_priority_zones']}")
            print(f"   Zonas HIGH: {metadata['high_priority_zones']}")
            print(f"   Zonas MEDIUM: {metadata['medium_priority_zones']}")
            print(f"   🔥 LiDAR GOLD CLASS: {metadata['lidar_gold_class']}")
            print(f"   📡 LiDAR disponible: {metadata['lidar_available_zones']}")
            print(f"   Cobertura: {metadata['coverage_percentage']:.1f}%")
            print()
            
            # Interpretación
            interpretation = result['interpretation']
            print(f"🔍 Interpretación:")
            print(f"   {interpretation['message']}")
            print(f"   {interpretation['efficiency']}")
            print(f"   🔥 {interpretation['lidar_opportunity']}")
            print()
            
            # Mostrar zonas GOLD CLASS
            gold_zones = [z for z in result['zones'] 
                         if z.get('lidar_available') and z.get('excavation_status') == 'unexcavated']
            
            if len(gold_zones) > 0:
                print(f"🔥 GOLD CLASS ZONES (LiDAR + Unexcavated):")
                print()
                
                for i, zone in enumerate(gold_zones[:3], 1):
                    print(f"{i}. {zone['zone_id']} - {zone['priority_class']} {zone.get('priority_color', '')}")
                    print(f"   Score: {zone.get('priority_score', 0):.3f}")
                    print(f"   Área: {zone['area_km2']:.2f} km²")
                    print(f"   Terreno: {zone.get('terrain_type', 'unknown')}")
                    print(f"   Centro: {zone['center']['lat']:.4f}, {zone['center']['lon']:.4f}")
                    
                    if 'recommendation' in zone:
                        rec = zone['recommendation']
                        print(f"   Recomendaciones:")
                        for r in rec.get('recommendations', [])[:2]:
                            print(f"     • {r}")
                        print(f"   Clases LiDAR: {', '.join(rec.get('lidar_candidate_classes', []))}")
                    print()
            
            # Mostrar top 3 zonas por score
            print(f"🎯 Top 3 Zonas por Score:")
            print()
            
            for i, zone in enumerate(result['zones'][:3], 1):
                print(f"{i}. {zone['zone_id']} - {zone.get('priority_class', 'N/A')} {zone.get('priority_color', '')}")
                print(f"   Score: {zone.get('priority_score', 0):.3f}")
                print(f"   LiDAR: {'✅' if zone.get('lidar_available') else '❌'}")
                print(f"   Excavación: {zone.get('excavation_status', 'unknown')}")
                
                if 'scoring_details' in zone:
                    scoring = zone['scoring_details']
                    print(f"   Scoring breakdown:")
                    print(f"     Cultural prior: {scoring['cultural_prior']['score']:.3f}")
                    print(f"     Terrain: {scoring['terrain_favorable']['score']:.3f}")
                    print(f"     LiDAR complement: {scoring['lidar_complement']['score']:.3f}")
                    print(f"     Excavation gap: {scoring['excavation_gap']['score']:.3f}")
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


def test_lidar_gold_class():
    """Test específico para zonas GOLD CLASS (LiDAR + unexcavated)"""
    
    print("\n" + "="*80)
    print("🔥 TEST: LiDAR GOLD CLASS - Máxima Prioridad")
    print("="*80)
    print()
    
    # Regiones con alta probabilidad de LiDAR
    test_regions = [
        {
            "name": "Petén, Guatemala (Maya)",
            "lat_min": 16.0,
            "lat_max": 18.0,
            "lon_min": -91.0,
            "lon_max": -89.0
        },
        {
            "name": "Amazonia, Brasil",
            "lat_min": -5.0,
            "lat_max": -3.0,
            "lon_min": -62.0,
            "lon_max": -60.0
        },
        {
            "name": "Angkor, Camboya",
            "lat_min": 13.0,
            "lat_max": 14.0,
            "lon_min": 103.0,
            "lon_max": 104.0
        }
    ]
    
    gold_class_summary = []
    
    for region in test_regions:
        print(f"📍 Región: {region['name']}")
        
        test_data = {
            "lat_min": region['lat_min'],
            "lat_max": region['lat_max'],
            "lon_min": region['lon_min'],
            "lon_max": region['lon_max'],
            "strategy": "buffer",
            "max_zones": 15,
            "lidar_priority": True,
            "include_scoring": True
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/archaeological-sites/recommended-zones",
                json=test_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                metadata = result['metadata']
                
                gold_count = metadata.get('lidar_gold_class', 0)
                lidar_count = metadata.get('lidar_available_zones', 0)
                
                print(f"   🔥 GOLD CLASS: {gold_count} zonas")
                print(f"   📡 LiDAR disponible: {lidar_count} zonas")
                print(f"   ✅ Total zonas: {len(result['zones'])}")
                
                if gold_count > 0:
                    # Mostrar primera zona GOLD
                    gold_zones = [z for z in result['zones'] 
                                 if z.get('lidar_available') and z.get('excavation_status') == 'unexcavated']
                    
                    if len(gold_zones) > 0:
                        zone = gold_zones[0]
                        print(f"\n   🎯 Ejemplo GOLD CLASS:")
                        print(f"      ID: {zone['zone_id']}")
                        print(f"      Score: {zone.get('priority_score', 0):.3f}")
                        print(f"      Clase: {zone.get('priority_class', 'N/A')}")
                        
                        if 'recommendation' in zone:
                            rec = zone['recommendation']
                            if 'recommendations' in rec and len(rec['recommendations']) > 0:
                                print(f"      Recomendación: {rec['recommendations'][0]}")
                
                gold_class_summary.append({
                    'region': region['name'],
                    'gold_count': gold_count,
                    'lidar_count': lidar_count,
                    'total_zones': len(result['zones'])
                })
                
                print()
            else:
                print(f"   ❌ Error: {response.status_code}")
                print()
        
        except Exception as e:
            print(f"   ❌ Excepción: {e}")
            print()
    
    # Resumen
    if len(gold_class_summary) > 0:
        print("="*80)
        print("📊 RESUMEN GOLD CLASS")
        print("="*80)
        print()
        
        total_gold = sum(r['gold_count'] for r in gold_class_summary)
        total_lidar = sum(r['lidar_count'] for r in gold_class_summary)
        
        print(f"Total GOLD CLASS detectadas: {total_gold}")
        print(f"Total zonas con LiDAR: {total_lidar}")
        print()
        
        for r in gold_class_summary:
            print(f"  {r['region']:<30} GOLD: {r['gold_count']:>3}  LiDAR: {r['lidar_count']:>3}")
        
        print()
        print("🔥 GOLD CLASS = LiDAR detectado + NO excavado")
        print("   → Máxima prioridad para análisis complementario")
        print("   → Thermal + SAR + NDVI + Multi-temporal")
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
    print("  1. Zonas recomendadas - Estrategia BUFFER + Scoring LiDAR")
    print("  2. Zonas recomendadas - Estrategia GRADIENT")
    print("  3. Zonas recomendadas - Estrategia GAPS")
    print("  4. Workflow completo (zonas → análisis)")
    print("  5. Métricas de optimización")
    print("  6. LiDAR GOLD CLASS (máxima prioridad)")
    print()
    
    results = []
    
    # Test 1: Buffer + Scoring
    results.append(("Estrategia BUFFER + Scoring LiDAR", test_recommended_zones_buffer()))
    
    # Test 2: Gradient
    results.append(("Estrategia GRADIENT", test_recommended_zones_gradient()))
    
    # Test 3: Gaps
    results.append(("Estrategia GAPS", test_recommended_zones_gaps()))
    
    # Test 4: Workflow
    results.append(("Workflow completo", test_zone_analysis_workflow()))
    
    # Test 5: Métricas
    results.append(("Métricas de optimización", test_optimization_metrics()))
    
    # Test 6: LiDAR GOLD CLASS
    results.append(("LiDAR GOLD CLASS", test_lidar_gold_class()))
    
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
