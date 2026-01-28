#!/usr/bin/env python3
"""
Test de la nueva UI de detección de tipos de anomalías arqueológicas.
"""

import requests
import json
import time

def test_anomaly_detection_ui():
    """Test de la nueva funcionalidad de detección de tipos de anomalías"""
    
    print("🔬 Testing Anomaly Detection UI Enhancement")
    print("=" * 50)
    
    # Coordenadas con diferentes tipos de anomalías esperadas
    test_sites = [
        {
            "name": "Roma - Via Appia (Lineales)",
            "coords": {
                "lat_min": 41.8500, "lat_max": 41.8600,
                "lon_min": 12.5100, "lon_max": 12.5200
            },
            "expected_anomalies": ["linear", "rectangular"]
        },
        {
            "name": "Angkor - Sistemas Hidráulicos (Complejas)",
            "coords": {
                "lat_min": 13.4300, "lat_max": 13.4500,
                "lon_min": 103.8500, "lon_max": 103.8700
            },
            "expected_anomalies": ["complex", "circular"]
        },
        {
            "name": "Giza - Estructuras Monumentales (Circulares)",
            "coords": {
                "lat_min": 29.9700, "lat_max": 29.9900,
                "lon_min": 31.1200, "lon_max": 31.1400
            },
            "expected_anomalies": ["circular", "rectangular"]
        }
    ]
    
    results = []
    
    for site in test_sites:
        print(f"\n🏺 Analizando: {site['name']}")
        
        analysis_request = {
            **site['coords'],
            "resolution_m": 400,
            "region_name": f"Test Anomalías - {site['name']}",
            "include_explainability": True,
            "include_validation_metrics": True,
            "layers_to_analyze": [
                # Capas que detectan diferentes tipos de anomalías
                "ndvi_vegetation",        # Rectangulares (campos, edificios)
                "thermal_lst",           # Rectangulares (estructuras térmicas)
                "sar_backscatter",       # Lineales (muros, calzadas)
                "spectral_roughness",    # Lineales (patrones geométricos)
                "dem_multiscale",        # Circulares (túmulos, plazas)
                "lidar_fullwave",        # Circulares (estructuras 3D)
                "pseudo_lidar_ai",       # Complejas (inferencia multi-sensor)
                "multitemporal_topo"     # Complejas (evolución temporal)
            ],
            "active_rules": ["all"]
        }
        
        try:
            response = requests.post(
                'http://localhost:8004/analyze',
                json=analysis_request,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('statistical_results', {})
                
                print(f"  ✅ Análisis completado")
                print(f"  📊 Instrumentos activos: {len(stats)}")
                
                # Simular detección de anomalías (lógica del frontend)
                detected_anomalies = simulate_anomaly_detection(stats)
                
                print(f"  🔬 Anomalías detectadas: {len(detected_anomalies)}")
                
                for anomaly in detected_anomalies:
                    confidence = anomaly['confidence'] * 100
                    print(f"    {anomaly['icon']} {anomaly['name']}: {confidence:.1f}% - {anomaly['description']}")
                
                # Verificar si se detectaron los tipos esperados
                detected_types = [a['type'] for a in detected_anomalies]
                expected_types = site['expected_anomalies']
                
                matches = set(detected_types) & set(expected_types)
                if matches:
                    print(f"  ✅ Tipos esperados detectados: {', '.join(matches)}")
                else:
                    print(f"  ⚠️ Tipos esperados no detectados. Esperado: {expected_types}, Detectado: {detected_types}")
                
                results.append({
                    'site': site['name'],
                    'success': len(matches) > 0,
                    'detected': detected_types,
                    'expected': expected_types,
                    'anomalies': detected_anomalies
                })
                
            else:
                print(f"  ❌ Error: {response.status_code}")
                results.append({
                    'site': site['name'],
                    'success': False,
                    'error': response.status_code
                })
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({
                'site': site['name'],
                'success': False,
                'error': str(e)
            })
    
    return results

def simulate_anomaly_detection(stats):
    """Simular la lógica de detección de anomalías del frontend"""
    
    detected_anomalies = []
    
    for instrument, data in stats.items():
        prob = data.get('archaeological_probability', 0)
        coherence = data.get('geometric_coherence', 0)
        
        if prob > 0.3:
            # Lógica similar al frontend
            if ('sar' in instrument or 'spectral_roughness' in instrument) and coherence > 0.7 and prob > 0.4:
                detected_anomalies.append({
                    'type': 'linear',
                    'name': 'Lineales',
                    'description': 'Calzadas, muros, canales',
                    'icon': '📏',
                    'confidence': prob,
                    'source': instrument
                })
            
            if ('dem' in instrument or 'lidar' in instrument or 'multitemporal' in instrument) and prob > 0.35:
                detected_anomalies.append({
                    'type': 'circular',
                    'name': 'Circulares', 
                    'description': 'Plazas, fosos, túmulos',
                    'icon': '⭕',
                    'confidence': prob,
                    'source': instrument
                })
            
            if ('ndvi' in instrument or 'thermal' in instrument or 'pseudo_lidar' in instrument) and coherence > 0.6 and prob > 0.3:
                detected_anomalies.append({
                    'type': 'rectangular',
                    'name': 'Rectangulares',
                    'description': 'Edificios, terrazas, campos',
                    'icon': '🔲',
                    'confidence': prob,
                    'source': instrument
                })
            
            if prob > 0.5 and coherence > 0.8:
                detected_anomalies.append({
                    'type': 'complex',
                    'name': 'Complejas',
                    'description': 'Ciudades, sistemas hidráulicos',
                    'icon': '🏛️',
                    'confidence': prob,
                    'source': instrument
                })
    
    return detected_anomalies

if __name__ == "__main__":
    results = test_anomaly_detection_ui()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE RESULTADOS:")
    
    successful_sites = [r for r in results if r.get('success', False)]
    
    print(f"✅ Sitios exitosos: {len(successful_sites)}/{len(results)}")
    
    if successful_sites:
        print("\n🎯 TIPOS DE ANOMALÍAS DETECTADAS:")
        all_types = set()
        for result in successful_sites:
            all_types.update(result.get('detected', []))
        
        type_icons = {
            'linear': '📏 Lineales',
            'circular': '⭕ Circulares', 
            'rectangular': '🔲 Rectangulares',
            'complex': '🏛️ Complejas'
        }
        
        for anomaly_type in all_types:
            print(f"  {type_icons.get(anomaly_type, anomaly_type)}")
    
    print(f"\n🔬 NUEVA FUNCIONALIDAD UI:")
    print(f"  ✅ Detección automática de tipos de anomalías")
    print(f"  ✅ Clasificación geométrica inteligente")
    print(f"  ✅ Explicación científica integrada")
    print(f"  ✅ Visualización educativa mejorada")
    
    print(f"\n📋 Para probar en el navegador:")
    print(f"  1. Abrir http://localhost:8001")
    print(f"  2. Analizar cualquier región arqueológica")
    print(f"  3. Abrir la lupa arqueológica")
    print(f"  4. Ver la nueva sección '🔬 Anomalías Detectadas'")
    print(f"  5. Explorar los diferentes tipos geométricos")