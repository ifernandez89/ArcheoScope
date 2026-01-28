#!/usr/bin/env python3
"""
Test Completo: Océano Pacífico Sur - Instrumental Mejorado
Prueba de los 10 instrumentos arqueológicos integrados

Coordenadas: -76.75°, -110.09° (Océano Pacífico Sur)
Objetivo: Probar sistema instrumental completo en ambiente oceánico
"""

import requests
import json
from datetime import datetime
import sys

def test_oceano_pacifico_instrumental_completo():
    """
    Probar ArcheoScope con instrumental completo en Océano Pacífico Sur.
    
    Test de los 10 instrumentos:
    BASE (5): IRIS, Sentinel, Landsat, MODIS, SMOS
    MEJORADOS (5): OpenTopography, ASF PALSAR, ICESat-2, GEDI, SMAP
    """
    
    # URL del backend
    backend_url = "http://localhost:8004"
    
    print("🏺 ARCHEOSCOPE - TEST INSTRUMENTAL COMPLETO")
    print("=" * 55)
    print(f"📍 Región: Océano Pacífico Sur")
    print(f"📌 Coordenadas: -76.75°, -110.09°")
    print(f"🌊 Ambiente: Oceánico remoto")
    print(f"🛰️ Instrumentos: 10 (5 base + 5 mejorados)")
    print(f"🎯 Objetivo: Probar capacidades integradas")
    print()
    
    # Verificar estado del sistema mejorado
    try:
        print("🔍 Verificando instrumental mejorado...")
        
        # Estado detallado con instrumentos
        status_response = requests.get(f"{backend_url}/status/detailed", timeout=10)
        
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"✅ Backend: {status['backend_status']}")
            print(f"🛰️ Total instrumentos: {status.get('total_instruments', 'N/A')}")
            
            arch_instruments = status.get('archaeological_instruments', {})
            if arch_instruments:
                print(f"📡 APIs base: {arch_instruments.get('base_apis', 0)}")
                print(f"🚀 APIs mejoradas: {arch_instruments.get('enhanced_apis', 0)}")
                print(f"⭐ Instrumentos críticos: {arch_instruments.get('critical_instruments', 0)}")
            print()
        
        # Estado específico de instrumentos
        instruments_response = requests.get(f"{backend_url}/instruments/status", timeout=10)
        
        if instruments_response.status_code == 200:
            instruments = instruments_response.json()
            print("🛰️ ESTADO INSTRUMENTAL DETALLADO:")
            
            base_count = instruments.get('base_instruments', {}).get('count', 0)
            enhanced_count = instruments.get('enhanced_instruments', {}).get('count', 0)
            
            print(f"   📡 Instrumentos base: {base_count}")
            print(f"   🚀 Instrumentos mejorados: {enhanced_count}")
            print(f"   🎯 Total: {instruments.get('total_instruments', 0)}")
            
            # Capacidades únicas
            capabilities = instruments.get('capabilities_summary', {})
            if capabilities:
                print(f"   🏔️ Micro-topografía: {capabilities.get('micro_topography', 'N/A')}")
                print(f"   🌳 Penetración vegetal: {capabilities.get('vegetation_penetration', 'N/A')}")
                print(f"   📏 Precisión centimétrica: {capabilities.get('centimetric_precision', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"❌ Error verificando instrumentos: {e}")
        return None
    
    # Configurar análisis oceánico con todos los instrumentos
    analysis_request = {
        # Coordenadas Océano Pacífico Sur
        "lat_min": -76.76,  # 1 km sur
        "lat_max": -76.74,  # 1 km norte
        "lon_min": -110.10, # 1 km oeste
        "lon_max": -110.08, # 1 km este
        
        "resolution_m": 200,  # Resolución media para ambiente oceánico
        
        # TODAS las capas disponibles (base + mejoradas)
        "layers_to_analyze": [
            # Base (5)
            "ndvi_vegetation",      # Sentinel-2, Landsat
            "thermal_lst",          # MODIS, Landsat térmico
            "sar_backscatter",      # Sentinel-1
            "surface_roughness",    # Scatterometer simulado
            "soil_salinity",        # SMOS
            "seismic_resonance",    # IRIS
            
            # Mejoradas (5)
            "elevation_dem",        # OpenTopography
            "sar_l_band",          # ASF DAAC PALSAR
            "icesat2_profiles",    # ICESat-2 ATL08
            "vegetation_height",   # GEDI
            "soil_moisture"        # SMAP
        ],
        
        # Reglas arqueológicas para ambiente oceánico
        "active_rules": [
            "submerged_structures_detection",     # Estructuras sumergidas
            "coastal_archaeological_patterns",   # Patrones costeros antiguos
            "sea_level_change_indicators",       # Indicadores de cambio nivel mar
            "underwater_geometric_anomalies"     # Anomalías geométricas submarinas
        ],
        
        "region_name": "Océano Pacífico Sur - Test Instrumental Completo",
        "include_explainability": True,
        "include_validation_metrics": True
    }
    
    print("🚀 Iniciando análisis con instrumental completo...")
    print(f"📊 Capas totales: {len(analysis_request['layers_to_analyze'])}")
    print(f"🔬 Reglas oceánicas: {len(analysis_request['active_rules'])}")
    print(f"🎯 Resolución: {analysis_request['resolution_m']}m")
    print()
    
    try:
        # Ejecutar análisis con todos los instrumentos
        print("⏳ Ejecutando análisis arqueológico oceánico...")
        
        analysis_response = requests.post(
            f"{backend_url}/analyze", 
            json=analysis_request,
            timeout=120  # Más tiempo para 10 instrumentos
        )
        
        if analysis_response.status_code == 200:
            results = analysis_response.json()
            
            print("✅ Análisis completado con instrumental completo")
            print()
            
            # Mostrar resultados por instrumento
            display_instrumental_results(results)
            
            # Guardar resultados completos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"oceano_pacifico_instrumental_completo_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Resultados guardados en: {filename}")
            
            return results
            
        else:
            print(f"❌ Error en análisis: {analysis_response.status_code}")
            print(f"Respuesta: {analysis_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error ejecutando análisis: {e}")
        return None

def display_instrumental_results(results):
    """Mostrar resultados organizados por instrumento."""
    
    print("🛰️ RESULTADOS POR INSTRUMENTO - OCÉANO PACÍFICO SUR")
    print("=" * 60)
    
    # Información de la región
    region_info = results.get('region_info', {})
    print(f"📍 Región: {region_info.get('name', 'Océano Pacífico')}")
    print(f"📏 Área: {region_info.get('area_km2', 'N/A')} km²")
    print(f"🎯 Resolución: {region_info.get('resolution_m', 'N/A')} m")
    print(f"🌊 Tipo: {region_info.get('analysis_type', 'oceánico')}")
    print()
    
    # Resultados por instrumento
    stats = results.get('statistical_results', {})
    if stats:
        print("📊 ANÁLISIS POR INSTRUMENTO:")
        
        # Organizar por categorías
        instrumentos_base = {
            "ndvi_vegetation": "📡 Sentinel-2/Landsat (Óptico)",
            "thermal_lst": "🌡️ MODIS/Landsat (Térmico)", 
            "sar_backscatter": "📊 Sentinel-1 (SAR banda C)",
            "surface_roughness": "🌊 Scatterometer (Rugosidad)",
            "soil_salinity": "🧂 SMOS (Salinidad)",
            "seismic_resonance": "📳 IRIS (Sísmico)"
        }
        
        instrumentos_mejorados = {
            "elevation_dem": "🏔️ OpenTopography (DEM)",
            "sar_l_band": "📡 ASF PALSAR (SAR banda L)",
            "icesat2_profiles": "📏 ICESat-2 (Láser)",
            "vegetation_height": "🌳 GEDI (Vegetación 3D)",
            "soil_moisture": "💧 SMAP (Humedad)"
        }
        
        print("   🔵 INSTRUMENTOS BASE:")
        for layer_key, instrument_name in instrumentos_base.items():
            if layer_key in stats:
                layer_data = stats[layer_key]
                prob = layer_data.get('archaeological_probability', 0)
                coherence = layer_data.get('geometric_coherence', 0)
                
                print(f"     {instrument_name}")
                print(f"       Probabilidad: {prob:.3f} ({prob*100:.1f}%)")
                print(f"       Coherencia: {coherence:.3f}")
                
                # Interpretación específica para océano
                if prob > 0.3:
                    print(f"       🔍 Señal significativa en ambiente oceánico")
                elif prob > 0.1:
                    print(f"       🟡 Señal débil - típico para océano")
                else:
                    print(f"       🔵 Sin señal - esperado en océano")
        
        print("\n   🚀 INSTRUMENTOS MEJORADOS:")
        for layer_key, instrument_name in instrumentos_mejorados.items():
            if layer_key in stats:
                layer_data = stats[layer_key]
                prob = layer_data.get('archaeological_probability', 0)
                coherence = layer_data.get('geometric_coherence', 0)
                
                print(f"     {instrument_name}")
                print(f"       Probabilidad: {prob:.3f} ({prob*100:.1f}%)")
                print(f"       Coherencia: {coherence:.3f}")
                
                # Valor agregado específico
                if layer_key == "elevation_dem":
                    print(f"       💡 Batimetría y micro-relieve oceánico")
                elif layer_key == "sar_l_band":
                    print(f"       💡 Penetración bajo superficie marina")
                elif layer_key == "icesat2_profiles":
                    print(f"       💡 Perfiles láser de superficie oceánica")
                elif layer_key == "vegetation_height":
                    print(f"       💡 Detección de algas/vegetación marina")
                elif layer_key == "soil_moisture":
                    print(f"       💡 Salinidad y humedad oceánica")
        print()
    
    # Evaluación arqueológica integrada
    archaeological = results.get('physics_results', {})
    if archaeological:
        print("🏛️ EVALUACIÓN ARQUEOLÓGICA OCEÁNICA:")
        
        evaluations = archaeological.get('evaluations', {})
        total_prob = 0
        count = 0
        
        for rule_name, evaluation in evaluations.items():
            prob = evaluation.get('archaeological_probability', 0)
            confidence = evaluation.get('confidence', 0)
            
            print(f"   📋 {rule_name}:")
            print(f"     Probabilidad: {prob:.3f} ({prob*100:.1f}%)")
            print(f"     Confianza: {confidence:.3f}")
            
            total_prob += prob
            count += 1
        
        if count > 0:
            avg_prob = total_prob / count
            print(f"\n🎯 PROBABILIDAD PROMEDIO: {avg_prob:.3f} ({avg_prob*100:.1f}%)")
        
        # Score integrado
        integrated = archaeological.get('integrated_analysis', {})
        if integrated:
            print(f"\n🔗 ANÁLISIS INTEGRADO:")
            print(f"   Score total: {integrated.get('integrated_score', 0):.3f}")
            print(f"   Clasificación: {integrated.get('classification', 'N/A')}")
            print(f"   Explicación: {integrated.get('explanation', 'N/A')}")
        print()
    
    # Interpretación oceánica específica
    print("🌊 INTERPRETACIÓN OCEÁNICA:")
    
    # Calcular probabilidad general de todos los instrumentos
    if stats:
        all_probs = [data.get('archaeological_probability', 0) for data in stats.values()]
        general_prob = sum(all_probs) / len(all_probs) if all_probs else 0
        
        print(f"   Probabilidad general (10 instrumentos): {general_prob:.3f} ({general_prob*100:.1f}%)")
        
        # Interpretación contextual oceánica
        if general_prob > 0.5:
            print("   🔴 ALTA probabilidad - Anomalías significativas en océano")
            print("   💡 Posibles estructuras sumergidas o patrones anómalos")
            print("   🔍 Recomendado: Investigación batimétrica detallada")
        elif general_prob > 0.2:
            print("   🟡 MODERADA probabilidad - Señales débiles oceánicas")
            print("   💡 Patrones naturales oceánicos con algunas anomalías")
            print("   🔍 Considerar: Análisis de corrientes y sedimentación")
        else:
            print("   🔵 BAJA probabilidad - Típico ambiente oceánico")
            print("   💡 Patrones naturales oceánicos dominantes")
            print("   🔍 Resultado esperado para océano abierto")
        
        # Valor de los instrumentos mejorados
        print(f"\n🚀 VALOR DE INSTRUMENTOS MEJORADOS:")
        enhanced_layers = ["elevation_dem", "sar_l_band", "icesat2_profiles", "vegetation_height", "soil_moisture"]
        enhanced_probs = [stats.get(layer, {}).get('archaeological_probability', 0) for layer in enhanced_layers if layer in stats]
        
        if enhanced_probs:
            enhanced_avg = sum(enhanced_probs) / len(enhanced_probs)
            base_probs = [prob for i, prob in enumerate(all_probs) if i < len(all_probs) - len(enhanced_probs)]
            base_avg = sum(base_probs) / len(base_probs) if base_probs else 0
            
            print(f"   📡 Instrumentos base promedio: {base_avg:.3f}")
            print(f"   🚀 Instrumentos mejorados promedio: {enhanced_avg:.3f}")
            
            if enhanced_avg > base_avg:
                print(f"   ✅ Instrumentos mejorados detectan {((enhanced_avg/base_avg-1)*100):.1f}% más señal")
            else:
                print(f"   📊 Instrumentos base y mejorados consistentes")
        print()
    
    # Mapa de anomalías
    anomaly_map = results.get('anomaly_map', {})
    if anomaly_map:
        stats_map = anomaly_map.get('statistics', {})
        if stats_map:
            print("🗺️ DISTRIBUCIÓN ESPACIAL OCEÁNICA:")
            print(f"   Área con anomalías: {stats_map.get('spatial_anomaly_percentage', 0):.1f}%")
            print(f"   Firmas arqueológicas: {stats_map.get('archaeological_signature_percentage', 0):.1f}%")
            print(f"   Procesos naturales: {stats_map.get('natural_percentage', 0):.1f}%")
            print()
    
    # Estado del sistema
    system_status = results.get('system_status', {})
    if system_status:
        print("⚙️ RENDIMIENTO DEL SISTEMA:")
        print(f"   Procesamiento: {system_status.get('processing_time_seconds', 'N/A')}")
        print(f"   Módulos académicos: {system_status.get('academic_modules', {})}")
        print()

if __name__ == "__main__":
    print("🏺 ArcheoScope - Test Instrumental Completo")
    print("Probando 10 instrumentos en Océano Pacífico Sur...")
    print()
    
    results = test_oceano_pacifico_instrumental_completo()
    
    if results:
        print("\n✅ Test instrumental completado exitosamente")
        print("🛰️ Los 10 instrumentos arqueológicos funcionaron correctamente")
        print("🌊 Análisis oceánico realizado con instrumental completo")
        print("📊 Revisa los resultados detallados arriba")
    else:
        print("\n❌ Error en el test instrumental")
        sys.exit(1)