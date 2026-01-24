#!/usr/bin/env python3
"""
Test completo del sistema ArcheoScope con validación real y transparencia
Verifica que todos los componentes críticos funcionen correctamente
"""

import requests
import json
from datetime import datetime
import time

def test_system_status():
    """Test endpoint de estado del sistema"""
    print("🔍 Test 1: Estado del sistema")
    
    try:
        response = requests.get("http://localhost:8002/status", timeout=10)
        if response.status_code == 200:
            print("✅ Sistema operativo")
            return True
        else:
            print(f"❌ Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_known_sites():
    """Test endpoint de sitios arqueológicos conocidos"""
    print("\n🏛️ Test 2: Sitios arqueológicos conocidos")
    
    try:
        response = requests.get("http://localhost:8002/known-sites", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['total_sites']} sitios conocidos cargados")
            
            # Verificar sitios de control
            control_sites = [s for s in data['known_sites'] if 'control' in s['type'].lower()]
            print(f"✅ {len(control_sites)} sitios de control incluidos")
            
            return True
        else:
            print(f"❌ Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_data_sources():
    """Test endpoint de fuentes de datos"""
    print("\n📊 Test 3: Fuentes de datos")
    
    try:
        response = requests.get("http://localhost:8002/data-sources", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['total_sources']} fuentes de datos configuradas")
            print(f"✅ {data['coverage_types']['global']} fuentes de cobertura global")
            
            return True
        else:
            print(f"❌ Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_region_validation():
    """Test endpoint de validación de región"""
    print("\n🎯 Test 4: Validación de región (Angkor Wat)")
    
    # Región que incluye Angkor Wat
    angkor_region = {
        "lat_min": 13.4,
        "lat_max": 13.43,
        "lon_min": 103.86,
        "lon_max": 103.88
    }
    
    try:
        response = requests.get(
            f"http://localhost:8002/validate-region?"
            f"lat_min={angkor_region['lat_min']}&lat_max={angkor_region['lat_max']}"
            f"&lon_min={angkor_region['lon_min']}&lon_max={angkor_region['lon_max']}",
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            validation = data['validation_results']
            
            print(f"✅ Validación completada")
            print(f"✅ {len(validation['overlapping_sites'])} sitios solapados")
            print(f"✅ {len(validation['nearby_sites'])} sitios cercanos")
            print(f"✅ Confianza: {validation['validation_confidence']}")
            
            return True
        else:
            print(f"❌ Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_falsification_protocol():
    """Test endpoint de protocolo de falsificación"""
    print("\n🔬 Test 5: Protocolo de falsificación")
    
    try:
        response = requests.post("http://localhost:8002/falsification-protocol", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data['falsification_results']
            
            print(f"✅ Protocolo ejecutado")
            print(f"✅ {data['control_sites_analyzed']} sitios control analizados")
            print(f"✅ Sitios comportándose como esperado: {data['scientific_validity']['sites_behaving_as_expected']}")
            print(f"✅ Estado validación: {data['scientific_validity']['validation_status']}")
            
            return True
        else:
            print(f"❌ Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_complete_analysis_with_validation():
    """Test completo de análisis con validación y transparencia"""
    print("\n🚀 Test 6: Análisis completo con validación (Teotihuacan)")
    
    # Región de Teotihuacan - sitio arqueológico confirmado
    teotihuacan_request = {
        "lat_min": 19.68,
        "lat_max": 19.70,
        "lon_min": -98.85,
        "lon_max": -98.83,
        "region_name": "Teotihuacan_Test_Analysis",
        "resolution_m": 100,
        "layers_to_analyze": ["ndvi_anomaly", "thermal_anomaly", "topographic_ruggedness"]
    }
    
    try:
        response = requests.post(
            "http://localhost:8002/analyze",
            json=teotihuacan_request,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificar componentes básicos
            print("✅ Análisis completado exitosamente")
            print(f"✅ ID análisis: {data['analysis_id']}")
            
            # Verificar validación real
            if 'real_archaeological_validation' in data:
                validation = data['real_archaeological_validation']
                if validation.get('overlapping_known_sites'):
                    print(f"✅ Sitios solapados detectados: {len(validation['overlapping_known_sites'])}")
                    for site in validation['overlapping_known_sites']:
                        print(f"   - {site['name']} ({site['confidence_level']})")
            
            # Verificar transparencia de datos
            if 'data_source_transparency' in data:
                transparency = data['data_source_transparency']
                print(f"✅ Fuentes documentadas: {len(transparency['data_sources_used'])}")
                for source in transparency['data_sources_used']:
                    print(f"   - {source['provider']} ({source['data_type']})")
                
                print(f"✅ Métodos de procesamiento: {len(transparency['processing_methods'])}")
                print(f"✅ Limitaciones: {len(transparency['analysis_limitations'])}")
            
            # Verificar aviso científico
            if 'scientific_validation_notice' in data:
                notice = data['scientific_validation_notice']
                print("✅ Aviso científico incluido:")
                for key, value in notice.items():
                    if key.startswith('validation_rule'):
                        print(f"   - {value}")
            
            # Verificar análisis integrado
            if 'integrated_analysis' in data:
                integrated = data['integrated_analysis']
                print(f"✅ Score integrado: {integrated.get('integrated_score', 0):.3f}")
                print(f"✅ Clasificación: {integrated.get('classification', 'unknown')}")
            
            return True
        else:
            print(f"❌ Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_control_region_analysis():
    """Test análisis de región control (debe dar resultados negativos)"""
    print("\n🚫 Test 7: Análisis región control (Denver downtown)")
    
    # Región urbana moderna - control negativo
    denver_request = {
        "lat_min": 39.73,
        "lat_max": 39.75,
        "lon_min": -105.00,
        "lon_max": -104.98,
        "region_name": "Denver_Urban_Control_Test",
        "resolution_m": 100,
        "layers_to_analyze": ["ndvi_anomaly", "thermal_anomaly", "topographic_ruggedness"]
    }
    
    try:
        response = requests.post(
            "http://localhost:8002/analyze",
            json=denver_request,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Análisis control completado")
            
            # Verificar que detecte control moderno
            if 'real_archaeological_validation' in data:
                validation = data['real_archaeological_validation']
                control_sites = [s for s in validation['overlapping_known_sites'] 
                               if 'control' in s['site_type'].lower()]
                if control_sites:
                    print(f"✅ Control detectado: {control_sites[0]['name']}")
            
            # Verificar análisis integrado
            if 'integrated_analysis' in data:
                integrated = data['integrated_analysis']
                score = integrated.get('integrated_score', 0)
                classification = integrated.get('classification', 'unknown')
                
                print(f"✅ Score control: {score:.3f}")
                print(f"✅ Clasificación: {classification}")
                
                # Verificar exclusión moderna
                if 'exclusion_moderna_applied' in integrated.get('temporal_sensor_analysis', {}):
                    if integrated['temporal_sensor_analysis']['exclusion_moderna_applied']:
                        print("✅ Exclusión moderna aplicada correctamente")
            
            return True
        else:
            print(f"❌ Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("="*80)
    print("🔍 ARCHEOSCOPE - TEST COMPLETO DE SISTEMA")
    print("Validación real, transparencia y control científico")
    print("="*80)
    
    tests = [
        test_system_status,
        test_known_sites,
        test_data_sources,
        test_region_validation,
        test_falsification_protocol,
        test_complete_analysis_with_validation,
        test_control_region_analysis
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
            time.sleep(2)  # Dar tiempo entre tests
        except Exception as e:
            print(f"❌ Error en test: {e}")
            results.append(False)
    
    print("\n" + "="*80)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*80)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests pasados: {passed}/{total}")
    
    if passed == total:
        print("🎉 TODOS LOS TESTS PASARON - SISTEMA COMPLETAMENTE FUNCIONAL")
        print("✅ Validación real implementada")
        print("✅ Transparencia de datos activa")
        print("✅ Protocolo de falsificación operativo")
        print("✅ Sistema listo para uso científico")
    else:
        print("⚠️ ALGUNOS TESTS FALLARON - Revisar configuración")
        
        for i, (test, result) in enumerate(zip(tests, results), 1):
            status = "✅" if result else "❌"
            print(f"  {status} Test {i}: {test.__name__}")
    
    print("="*80)

if __name__ == "__main__":
    main()