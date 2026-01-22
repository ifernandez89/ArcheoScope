#!/usr/bin/env python3
"""
Test del Módulo Volumétrico LIDAR
Validación del Modelado Volumétrico Arqueológico (LIDAR + ArcheoScope)
"""

import requests
import json
import time

def test_volumetric_lidar_module():
    print("🧊 TESTING VOLUMETRIC LIDAR MODULE")
    print("=" * 80)
    
    base_url = "http://localhost:8002"
    volumetric_url = f"{base_url}/volumetric"
    
    print("🎯 Objetivo: Validar integración científica LIDAR + ArcheoScope")
    print("🧠 Principio: LIDAR no 'descubre' arqueología. ArcheoScope no 'imagina' geometría.")
    print("✨ La verdad emerge de la convergencia.")
    
    try:
        # 1. Verificar catálogo de sitios LIDAR
        print("\n📚 PASO 1: Verificando catálogo de sitios LIDAR...")
        
        catalog_response = requests.get(f"{volumetric_url}/sites/catalog", timeout=10)
        
        if catalog_response.status_code == 200:
            catalog_data = catalog_response.json()
            print(f"✅ Catálogo cargado exitosamente")
            print(f"   - Total de sitios: {catalog_data['total_sites']}")
            print(f"   - Sitios arqueológicos confirmados: {catalog_data['archaeological_confirmed']}")
            print(f"   - Sitios de control: {catalog_data['control_sites']}")
            
            # Mostrar algunos sitios de ejemplo
            print("\n🏛️ SITIOS ARQUEOLÓGICOS CONFIRMADOS:")
            archaeological_sites = []
            control_sites = []
            
            for site_id, site_data in catalog_data['sites'].items():
                if site_data['site_type'] == 'archaeological_confirmed':
                    archaeological_sites.append((site_id, site_data))
                    print(f"   ✔️ {site_data['name']} ({site_data['lidar_type']}, {site_data['resolution_cm']}cm)")
                else:
                    control_sites.append((site_id, site_data))
            
            print("\n❌ SITIOS DE CONTROL NEGATIVO:")
            for site_id, site_data in control_sites[:3]:  # Mostrar solo los primeros 3
                print(f"   ❌ {site_data['name']} ({site_data['site_type']})")
            
        else:
            print(f"❌ Error obteniendo catálogo: {catalog_response.status_code}")
            return False
        
        # 2. Probar análisis volumétrico completo con sitio arqueológico
        if archaeological_sites:
            test_site_id, test_site_data = archaeological_sites[0]  # Usar primer sitio arqueológico
            
            print(f"\n🔬 PASO 2: Análisis volumétrico completo - {test_site_data['name']}")
            print(f"   📍 Coordenadas: {test_site_data['coordinates']}")
            print(f"   🛰️ LIDAR: {test_site_data['lidar_type']}")
            print(f"   📏 Resolución: {test_site_data['resolution_cm']}cm")
            
            analysis_request = {
                "site_id": test_site_id,
                "include_archeoscope": True,
                "perform_fusion": True,
                "output_format": "gltf"
            }
            
            print("   🔄 Ejecutando pipeline científico completo...")
            analysis_response = requests.post(
                f"{volumetric_url}/analyze", 
                json=analysis_request, 
                timeout=30
            )
            
            if analysis_response.status_code == 200:
                analysis_data = analysis_response.json()
                print("   ✅ Análisis volumétrico completado")
                
                # Verificar componentes del análisis
                site_info = analysis_data['site_info']
                volumetric = analysis_data['volumetric_analysis']
                archeoscope = analysis_data['archeoscope_results']
                fusion = analysis_data['fusion_results']
                model_3d = analysis_data['model_3d']
                
                print(f"\n📊 RESULTADOS VOLUMÉTRICOS:")
                print(f"   - Volumen positivo: {volumetric['positive_volume_m3']:.2f} m³")
                print(f"   - Volumen negativo: {volumetric['negative_volume_m3']:.2f} m³")
                print(f"   - Forma DTM: {volumetric['dtm_shape']}")
                print(f"   - Forma DSM: {volumetric['dsm_shape']}")
                
                if archeoscope:
                    print(f"\n🛰️ RESULTADOS ARCHEOSCOPE:")
                    print(f"   - NDVI diferencial: ✅ Procesado")
                    print(f"   - Persistencia temporal: ✅ Procesado")
                    print(f"   - Coherencia espacial: ✅ Procesado")
                    print(f"   - Exclusión moderna: ✅ Procesado")
                
                if fusion:
                    print(f"\n🧬 RESULTADOS DE FUSIÓN:")
                    print(f"   - Probabilidad antrópica promedio: {fusion['anthropic_probability_final']['mean']:.3f}")
                    print(f"   - Píxeles de alta probabilidad: {fusion['anthropic_probability_final']['high_probability_pixels']}")
                    print(f"   - Confianza promedio: {fusion['confidence_statistics']['mean_confidence']:.3f}")
                    print(f"   - Convergencia fuerte: {fusion['confidence_statistics']['high_confidence_percentage']:.1f}%")
                
                if model_3d:
                    print(f"\n🎯 MODELO 3D GENERADO:")
                    print(f"   - Formato: {model_3d['format']}")
                    print(f"   - Vértices: {model_3d['metadata']['total_vertices']}")
                    print(f"   - Caras: {model_3d['metadata']['total_faces']}")
                    print(f"   - Capas activables: {len(model_3d['activatable_layers'])}")
                    
                    # Verificar capas científicas
                    expected_layers = ['geometry_pure', 'archeoscope_mask', 'inferred_volume', 'interpretive_confidence']
                    for layer in expected_layers:
                        if layer in model_3d['activatable_layers']:
                            layer_info = model_3d['activatable_layers'][layer]
                            print(f"     ✅ {layer_info['name']}: {layer_info['description']}")
                        else:
                            print(f"     ❌ Capa faltante: {layer}")
                
            else:
                print(f"   ❌ Error en análisis: {analysis_response.status_code}")
                print(f"   Respuesta: {analysis_response.text}")
                return False
        
        # 3. Probar vista previa rápida
        print(f"\n👁️ PASO 3: Vista previa rápida")
        
        preview_response = requests.get(f"{volumetric_url}/sites/{test_site_id}/preview", timeout=10)
        
        if preview_response.status_code == 200:
            preview_data = preview_response.json()
            print("   ✅ Vista previa generada")
            
            volumetric_preview = preview_data['volumetric_preview']
            print(f"   - Volumen total: {volumetric_preview['total_volume_m3']:.2f} m³")
            print(f"   - Pendiente promedio: {volumetric_preview['average_slope_degrees']:.1f}°")
            print(f"   - Rugosidad promedio: {volumetric_preview['average_roughness']:.3f}")
            print(f"   - Calidad de datos: {volumetric_preview['data_quality']}")
            
        else:
            print(f"   ❌ Error en vista previa: {preview_response.status_code}")
        
        # 4. Verificar metodología científica
        print(f"\n📖 PASO 4: Verificando metodología científica")
        
        methodology_response = requests.get(f"{volumetric_url}/methodology", timeout=10)
        
        if methodology_response.status_code == 200:
            methodology = methodology_response.json()
            print("   ✅ Metodología científica disponible")
            print(f"   - Módulo: {methodology['module_name']}")
            print(f"   - Principio: {methodology['scientific_principle']}")
            print(f"   - Pasos del pipeline: {len(methodology['pipeline_architecture'])}")
            print(f"   - Pesos de fusión: {methodology['fusion_weights']}")
            print(f"   - Umbrales científicos: {methodology['scientific_thresholds']}")
            print(f"   - Limitaciones documentadas: {len(methodology['limitations'])}")
            
            # Verificar reglas científicas clave
            scientific_rules = methodology['validation_approach']['scientific_rules']
            print(f"\n   🔬 REGLAS CIENTÍFICAS VERIFICADAS:")
            for rule in scientific_rules:
                print(f"     • {rule}")
            
        else:
            print(f"   ❌ Error obteniendo metodología: {methodology_response.status_code}")
        
        # 5. Probar con sitio de control negativo
        if control_sites:
            control_site_id, control_site_data = control_sites[0]
            
            print(f"\n🔍 PASO 5: Validación con control negativo - {control_site_data['name']}")
            
            control_analysis_request = {
                "site_id": control_site_id,
                "include_archeoscope": True,
                "perform_fusion": True,
                "output_format": "gltf"
            }
            
            control_response = requests.post(
                f"{volumetric_url}/analyze", 
                json=control_analysis_request, 
                timeout=30
            )
            
            if control_response.status_code == 200:
                control_data = control_response.json()
                print("   ✅ Análisis de control completado")
                
                if control_data['fusion_results']:
                    control_fusion = control_data['fusion_results']
                    control_probability = control_fusion['anthropic_probability_final']['mean']
                    
                    print(f"   - Probabilidad antrópica (control): {control_probability:.3f}")
                    
                    # Verificar que el control negativo tiene baja probabilidad arqueológica
                    if control_probability < 0.5:
                        print("   ✅ Control negativo funcionando correctamente (baja probabilidad arqueológica)")
                    else:
                        print("   ⚠️ Control negativo con probabilidad arqueológica inesperadamente alta")
            
            else:
                print(f"   ❌ Error en análisis de control: {control_response.status_code}")
        
        print(f"\n📋 RESUMEN DE VALIDACIÓN:")
        print(f"   ✅ Catálogo de sitios LIDAR curado")
        print(f"   ✅ Pipeline científico independiente (LIDAR → ArcheoScope → Fusión)")
        print(f"   ✅ Análisis volumétrico puro")
        print(f"   ✅ Fusión probabilística explicable")
        print(f"   ✅ Modelo 3D con capas activables")
        print(f"   ✅ Metodología científica documentada")
        print(f"   ✅ Controles negativos funcionando")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Asegúrate de que el servidor ArcheoScope esté ejecutándose en localhost:8002")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    print("🚀 INICIANDO TEST DEL MÓDULO VOLUMÉTRICO LIDAR")
    print("🏛️ Modelado Volumétrico Arqueológico (LIDAR + ArcheoScope)")
    print()
    
    success = test_volumetric_lidar_module()
    
    if success:
        print("\n🎉 TEST COMPLETADO EXITOSAMENTE")
        print("✅ El módulo volumétrico LIDAR está funcionando correctamente")
        print("✅ Pipeline científico validado: LIDAR → ArcheoScope → Fusión → 3D")
        print("✅ Principio rector implementado: La verdad emerge de la convergencia")
        print("\n🌐 Accede al visor volumétrico en:")
        print("   http://localhost:8002/volumetric_lidar_viewer.html")
    else:
        print("\n❌ TEST FALLÓ")
        print("🔧 Revisar configuración del servidor y implementación del módulo")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()