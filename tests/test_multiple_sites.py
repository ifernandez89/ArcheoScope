#!/usr/bin/env python3
"""
Pruebas de múltiples sitios arqueológicos con ArcheoScope.
Versión optimizada para velocidad.
"""

import requests
import json
import time
from datetime import datetime

def test_archaeological_sites():
    """Probar múltiples sitios arqueológicos."""
    
    base_url = "http://localhost:8003"
    
    # Sitios arqueológicos seleccionados
    sites = {
        "nazca": {
            "name": "Nazca Lines",
            "lat_min": -14.8, "lat_max": -14.6,
            "lon_min": -75.2, "lon_max": -75.0,
            "expected_score": 70,  # Esperamos alta detección
            "landscape": "desert_plateau"
        },
        "machu_picchu": {
            "name": "Machu Picchu", 
            "lat_min": -13.18, "lat_max": -13.15,
            "lon_min": -72.58, "lon_max": -72.54,
            "expected_score": 80,  # Esperamos muy alta detección
            "landscape": "mountain_terraces"
        },
        "caral": {
            "name": "Caral",
            "lat_min": -10.92, "lat_max": -10.88,
            "lon_min": -77.54, "lon_max": -77.50,
            "expected_score": 75,  # Esperamos alta detección
            "landscape": "coastal_valley"
        }
    }
    
    print("🏛️  ARCHEOSCOPE - PRUEBAS DE SITIOS ARQUEOLÓGICOS")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Sitios a probar: {len(sites)}")
    
    # Verificar sistema
    print(f"\n🔍 Verificando sistema...")
    try:
        response = requests.get(f"{base_url}/status", timeout=10)
        if response.status_code != 200:
            print(f"❌ Sistema no disponible")
            return False
        
        status = response.json()
        print(f"✅ Backend: {status['backend_status']}")
        print(f"✅ IA: {status['ai_status']}")
        print(f"✅ Reglas: {len(status['available_rules'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Probar cada sitio
    results = []
    total_start = time.time()
    
    for site_key, site_data in sites.items():
        print(f"\n🏛️  ANALIZANDO: {site_data['name']}")
        print("-" * 50)
        
        # Preparar análisis (sin explicabilidad para velocidad)
        analysis_request = {
            "lat_min": site_data["lat_min"],
            "lat_max": site_data["lat_max"],
            "lon_min": site_data["lon_min"], 
            "lon_max": site_data["lon_max"],
            "region_name": f"{site_data['name']} Test",
            "resolution_m": 1000,  # Resolución moderada para velocidad
            "include_explainability": False,
            "include_validation_metrics": False
        }
        
        print(f"📍 Coordenadas: ({site_data['lat_min']:.2f}, {site_data['lon_min']:.2f}) - ({site_data['lat_max']:.2f}, {site_data['lon_max']:.2f})")
        print(f"🌍 Paisaje: {site_data['landscape']}")
        print("⏳ Analizando...")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{base_url}/analyze",
                json=analysis_request,
                timeout=120
            )
            
            analysis_time = time.time() - start_time
            
            if response.status_code != 200:
                print(f"❌ Error: {response.status_code}")
                results.append({
                    "site": site_key,
                    "name": site_data["name"],
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "time": analysis_time
                })
                continue
            
            result = response.json()
            
            # Extraer métricas
            region_info = result.get("region_info", {})
            anomaly_map = result.get("anomaly_map", {})
            stats = anomaly_map.get("statistics", {})
            physics_results = result.get("physics_results", {})
            evaluations = physics_results.get("evaluations", {})
            ai_explanations = result.get("ai_explanations", {})
            
            # Calcular puntuación
            archaeological_sig = stats.get("archaeological_signature_percentage", 0)
            spatial_anomalies = stats.get("spatial_anomaly_percentage", 0)
            natural_processes = stats.get("natural_percentage", 100)
            
            # Puntuación de reglas
            veg_prob = evaluations.get("vegetation_topography_decoupling", {}).get("archaeological_probability", 0)
            thermal_prob = evaluations.get("thermal_residual_patterns", {}).get("archaeological_probability", 0)
            
            # Puntuación total
            detection_score = min(100, (
                archaeological_sig * 3 +
                spatial_anomalies * 1.5 +
                (100 - natural_processes) * 0.5 +
                veg_prob * 30 +
                thermal_prob * 20
            ))
            
            # Mostrar resultados
            print(f"⏱️  Tiempo: {analysis_time:.1f}s")
            print(f"📏 Área: {region_info.get('area_km2', 0):.1f} km²")
            print(f"🔴 Firmas arqueológicas: {archaeological_sig:.1f}%")
            print(f"🟡 Anomalías espaciales: {spatial_anomalies:.1f}%")
            print(f"🟢 Procesos naturales: {natural_processes:.1f}%")
            print(f"🧪 Vegetación-Topografía: {veg_prob:.2f}")
            print(f"🌡️  Térmico: {thermal_prob:.2f}")
            print(f"🤖 IA: {'Sí' if ai_explanations.get('ai_available') else 'No'}")
            print(f"⭐ Puntuación: {detection_score:.1f}/100")
            
            # Evaluación
            expected = site_data["expected_score"]
            meets_expectations = detection_score >= expected * 0.8  # 80% del esperado
            
            if detection_score >= 80:
                quality = "EXCELENTE"
            elif detection_score >= 60:
                quality = "BUENA"
            elif detection_score >= 40:
                quality = "MODERADA"
            else:
                quality = "BAJA"
            
            print(f"📊 Calidad: {quality}")
            print(f"✅ Expectativas: {'CUMPLE' if meets_expectations else 'NO CUMPLE'} (esperado: {expected})")
            
            results.append({
                "site": site_key,
                "name": site_data["name"],
                "success": True,
                "time": analysis_time,
                "score": detection_score,
                "quality": quality,
                "meets_expectations": meets_expectations,
                "expected_score": expected,
                "archaeological_sig": archaeological_sig,
                "spatial_anomalies": spatial_anomalies,
                "natural_processes": natural_processes,
                "veg_prob": veg_prob,
                "thermal_prob": thermal_prob,
                "ai_available": ai_explanations.get('ai_available', False)
            })
            
        except Exception as e:
            analysis_time = time.time() - start_time
            print(f"❌ Error: {e}")
            results.append({
                "site": site_key,
                "name": site_data["name"],
                "success": False,
                "error": str(e),
                "time": analysis_time
            })
        
        # Pausa entre análisis
        time.sleep(3)
    
    total_time = time.time() - total_start
    
    # Resumen final
    print(f"\n🏆 RESUMEN FINAL")
    print("=" * 50)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"✅ Exitosos: {len(successful)}/{len(results)}")
    print(f"❌ Fallidos: {len(failed)}")
    print(f"⏱️  Tiempo total: {total_time:.1f}s")
    
    if successful:
        avg_score = sum(r["score"] for r in successful) / len(successful)
        avg_time = sum(r["time"] for r in successful) / len(successful)
        meets_exp_count = sum(1 for r in successful if r["meets_expectations"])
        ai_count = sum(1 for r in successful if r["ai_available"])
        
        print(f"📊 Puntuación promedio: {avg_score:.1f}/100")
        print(f"⏱️  Tiempo promedio: {avg_time:.1f}s")
        print(f"🎯 Cumplen expectativas: {meets_exp_count}/{len(successful)}")
        print(f"🤖 IA disponible: {ai_count}/{len(successful)}")
        
        print(f"\n📋 RESULTADOS POR SITIO:")
        for r in successful:
            status = "✅" if r["meets_expectations"] else "⚠️"
            print(f"   {status} {r['name']}: {r['score']:.1f}/100 ({r['quality']})")
        
        # Evaluación general
        success_rate = len(successful) / len(results) * 100
        expectation_rate = meets_exp_count / len(successful) * 100 if successful else 0
        
        if success_rate >= 80 and avg_score >= 60 and expectation_rate >= 70:
            overall = "🎉 EXCELENTE - ArcheoScope funciona muy bien en sitios arqueológicos"
        elif success_rate >= 60 and avg_score >= 45:
            overall = "👍 BUENO - ArcheoScope detecta anomalías arqueológicas correctamente"
        elif success_rate >= 40:
            overall = "⚠️  MODERADO - ArcheoScope requiere optimización"
        else:
            overall = "❌ NECESITA MEJORAS - ArcheoScope requiere desarrollo adicional"
        
        print(f"\n🎯 EVALUACIÓN GENERAL:")
        print(f"   {overall}")
        print(f"   Tasa de éxito: {success_rate:.1f}%")
        print(f"   Cumplimiento de expectativas: {expectation_rate:.1f}%")
    
    if failed:
        print(f"\n❌ SITIOS FALLIDOS:")
        for r in failed:
            print(f"   {r['name']}: {r.get('error', 'Error desconocido')}")
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"archeoscope_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_time": total_time,
            "results": results,
            "summary": {
                "total_tests": len(results),
                "successful": len(successful),
                "failed": len(failed),
                "success_rate": len(successful) / len(results) * 100,
                "average_score": sum(r["score"] for r in successful) / len(successful) if successful else 0,
                "average_time": sum(r["time"] for r in successful) / len(successful) if successful else 0
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {filename}")
    
    return len(successful) == len(results)

if __name__ == "__main__":
    success = test_archaeological_sites()
    if success:
        print(f"\n🎉 TODAS LAS PRUEBAS EXITOSAS")
    else:
        print(f"\n⚠️  ALGUNAS PRUEBAS FALLARON")