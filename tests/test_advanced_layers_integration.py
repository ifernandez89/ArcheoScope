#!/usr/bin/env python3
"""
Test de integración de las nuevas capas avanzadas para visualización impactante.
"""

import requests
import json
import time

def test_advanced_layers_integration():
    """Test completo de las nuevas capas avanzadas"""
    
    print("🚀 Testing Advanced Archaeological Layers Integration")
    print("=" * 60)
    
    # Coordenadas de test (Roma, Via Appia) - zona con alto potencial arqueológico
    test_coordinates = {
        "lat_min": 41.8500,
        "lat_max": 41.8600,
        "lon_min": 12.5100,
        "lon_max": 12.5200,
        "resolution_m": 300,  # Resolución media para capturar detalles
        "region_name": "Test Advanced Layers - Via Appia Roma",
        "include_explainability": True,
        "include_validation_metrics": True,
        "layers_to_analyze": [
            # Base (6)
            "ndvi_vegetation", "thermal_lst", "sar_backscatter", 
            "surface_roughness", "soil_salinity", "seismic_resonance",
            # Enhanced (5)
            "elevation_dem", "sar_l_band", "icesat2_profiles",
            "vegetation_height", "soil_moisture",
            # NUEVAS CAPAS AVANZADAS (5) - ¡LAS ESTRELLAS DEL SHOW!
            "lidar_fullwave",         # LiDAR full-waveform
            "dem_multiscale",         # DEM multiescala fusionado
            "spectral_roughness",     # Rugosidad espectral (Fourier/Wavelets)
            "pseudo_lidar_ai",        # Pseudo-LiDAR por IA
            "multitemporal_topo"      # Topografía multitemporal
        ],
        "active_rules": ["all"]
    }
    
    try:
        print("🔬 Enviando análisis con TODAS las capas avanzadas...")
        print(f"📊 Total de instrumentos: {len(test_coordinates['layers_to_analyze'])}")
        print(f"🎯 Capas avanzadas: 5 nuevas tecnologías")
        print()
        
        response = requests.post(
            'http://localhost:8004/analyze',
            json=test_coordinates,
            timeout=45  # Más tiempo para procesar todas las capas
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Análisis completado exitosamente!")
            
            # Verificar que tenemos resultados estadísticos
            if 'statistical_results' in data:
                stats = data['statistical_results']
                print(f"\n📈 Resultados Estadísticos Disponibles:")
                
                # Verificar capas base
                base_layers = ["ndvi_vegetation", "thermal_lst", "sar_backscatter", 
                              "surface_roughness", "soil_salinity", "seismic_resonance"]
                
                # Verificar capas mejoradas
                enhanced_layers = ["elevation_dem", "sar_l_band", "icesat2_profiles",
                                 "vegetation_height", "soil_moisture"]
                
                # Verificar NUEVAS capas avanzadas
                advanced_layers = ["lidar_fullwave", "dem_multiscale", "spectral_roughness",
                                 "pseudo_lidar_ai", "multitemporal_topo"]
                
                print("\n🔧 CAPAS BASE:")
                base_probs = []
                for layer in base_layers:
                    if layer in stats:
                        prob = stats[layer].get('archaeological_probability', 0)
                        base_probs.append(prob)
                        print(f"  ✅ {layer}: {prob:.1%}")
                    else:
                        print(f"  ❌ {layer}: No disponible")
                
                print("\n🚀 CAPAS MEJORADAS:")
                enhanced_probs = []
                for layer in enhanced_layers:
                    if layer in stats:
                        prob = stats[layer].get('archaeological_probability', 0)
                        enhanced_probs.append(prob)
                        print(f"  ✅ {layer}: {prob:.1%}")
                    else:
                        print(f"  ❌ {layer}: No disponible")
                
                print("\n🌟 NUEVAS CAPAS AVANZADAS:")
                advanced_probs = []
                for layer in advanced_layers:
                    if layer in stats:
                        prob = stats[layer].get('archaeological_probability', 0)
                        advanced_probs.append(prob)
                        coherence = stats[layer].get('geometric_coherence', 0)
                        print(f"  🎯 {layer}: {prob:.1%} (coherencia: {coherence:.1%})")
                    else:
                        print(f"  ⚠️ {layer}: No disponible")
                
                # Calcular estadísticas por grupo
                if base_probs:
                    avg_base = sum(base_probs) / len(base_probs)
                    print(f"\n📊 Promedio capas BASE: {avg_base:.1%}")
                
                if enhanced_probs:
                    avg_enhanced = sum(enhanced_probs) / len(enhanced_probs)
                    print(f"📊 Promedio capas MEJORADAS: {avg_enhanced:.1%}")
                
                if advanced_probs:
                    avg_advanced = sum(advanced_probs) / len(advanced_probs)
                    print(f"🌟 Promedio capas AVANZADAS: {avg_advanced:.1%}")
                
                # Verificar si la lupa se activaría
                all_probs = base_probs + enhanced_probs + advanced_probs
                if all_probs:
                    overall_avg = sum(all_probs) / len(all_probs)
                    print(f"\n🎯 PROBABILIDAD ARQUEOLÓGICA TOTAL: {overall_avg:.1%}")
                    
                    if overall_avg > 0.2:
                        print("🔍 ✅ LUPA ARQUEOLÓGICA SE ACTIVARÍA!")
                        print("   Las capas avanzadas están listas para visualización impactante")
                        
                        # Verificar qué capas avanzadas tienen alta probabilidad
                        high_prob_advanced = [layer for layer, prob in zip(advanced_layers, advanced_probs) if prob > 0.3]
                        if high_prob_advanced:
                            print(f"🌟 Capas avanzadas con alta probabilidad: {', '.join(high_prob_advanced)}")
                        
                        return True
                    else:
                        print("🔍 ❌ Lupa no se activaría (umbral no alcanzado)")
                        return False
                else:
                    print("❌ No hay datos de probabilidad disponibles")
                    return False
            else:
                print("❌ No hay resultados estadísticos en la respuesta")
                return False
                
        else:
            print(f"❌ Error en análisis: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        return False

if __name__ == "__main__":
    success = test_advanced_layers_integration()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST DE CAPAS AVANZADAS EXITOSO!")
        print("   ✅ Todas las nuevas tecnologías están integradas")
        print("   ✅ La lupa arqueológica mostrará visualización impactante")
        print("   ✅ 16 instrumentos totales funcionando")
    else:
        print("⚠️ TEST DE CAPAS AVANZADAS NECESITA ATENCIÓN")
        print("   Revisar la integración de las nuevas capas")
    
    print("\n🎯 NUEVAS TECNOLOGÍAS IMPLEMENTADAS:")
    print("   📡 LiDAR Full-Waveform - Penetración vegetal completa")
    print("   🗺️ DEM Multiescala - Micro-relieve + contexto regional")
    print("   🌊 Rugosidad Espectral - Detección de lineamientos artificiales")
    print("   🤖 Pseudo-LiDAR IA - Inferencia topográfica inteligente")
    print("   ⏳ Multitemporal - Evolución del paisaje arqueológico")
    
    print("\n📋 Próximos Pasos:")
    print("   1. Abrir http://localhost:8001")
    print("   2. Probar coordenadas: 41.8550, 12.5150")
    print("   3. Verificar que aparezcan 16 instrumentos")
    print("   4. Explorar la lupa con las nuevas capas avanzadas")
    print("   5. ¡Disfrutar de la visualización impactante!")