#!/usr/bin/env python3
"""
Pruebas exhaustivas de ArcheoScope con sitios arqueológicos reales.

Evalúa el rendimiento del sistema en:
- Nazca Lines (Perú)
- Machu Picchu (Perú) 
- Caral (Perú)
- Tiwanaku (Bolivia)
- Chichen Itza (México)
- Angkor Wat (Camboya)
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, Any, List

class ArchaeologicalSiteTester:
    """Tester para sitios arqueológicos con ArcheoScope."""
    
    def __init__(self, base_url: str = "http://localhost:8003"):
        self.base_url = base_url
        self.test_results = []
        
        # Sitios arqueológicos para probar
        self.archaeological_sites = {
            "nazca_lines": {
                "name": "Nazca Lines - Líneas de Nazca",
                "lat_min": -14.8, "lat_max": -14.6,
                "lon_min": -75.2, "lon_max": -75.0,
                "expected_features": ["geoglyphs", "linear_structures", "geometric_patterns"],
                "archaeological_significance": "high",
                "landscape_type": "desert_plateau",
                "known_structures": "geoglyphs, lines, animal figures"
            },
            "machu_picchu": {
                "name": "Machu Picchu - Ciudadela Inca",
                "lat_min": -13.18, "lat_max": -13.15,
                "lon_min": -72.58, "lon_max": -72.54,
                "expected_features": ["terraces", "stone_structures", "urban_layout"],
                "archaeological_significance": "very_high",
                "landscape_type": "mountain_terraces",
                "known_structures": "terraces, buildings, ceremonial areas"
            },
            "caral": {
                "name": "Caral - Civilización Caral",
                "lat_min": -10.92, "lat_max": -10.88,
                "lon_min": -77.54, "lon_max": -77.50,
                "expected_features": ["pyramids", "urban_complex", "ceremonial_structures"],
                "archaeological_significance": "very_high",
                "landscape_type": "coastal_valley",
                "known_structures": "pyramids, plazas, residential areas"
            },
            "tiwanaku": {
                "name": "Tiwanaku - Tiahuanaco",
                "lat_min": -16.57, "lat_max": -16.54,
                "lon_min": -68.69, "lon_max": -68.66,
                "expected_features": ["monumental_architecture", "ceremonial_complex", "stone_structures"],
                "archaeological_significance": "very_high", 
                "landscape_type": "altiplano",
                "known_structures": "Akapana pyramid, Kalasasaya temple, monoliths"
            },
            "chichen_itza": {
                "name": "Chichen Itza - Zona Maya",
                "lat_min": 20.68, "lat_max": 20.70,
                "lon_min": -88.57, "lon_max": -88.55,
                "expected_features": ["pyramids", "ball_court", "ceremonial_structures"],
                "archaeological_significance": "very_high",
                "landscape_type": "tropical_lowlands",
                "known_structures": "El Castillo pyramid, Great Ball Court, Temple of Warriors"
            },
            "angkor_wat": {
                "name": "Angkor Wat - Complejo Khmer",
                "lat_min": 13.41, "lat_max": 13.43,
                "lon_min": 103.86, "lon_max": 103.88,
                "expected_features": ["temple_complex", "moats", "urban_layout"],
                "archaeological_significance": "very_high",
                "landscape_type": "tropical_plains",
                "known_structures": "temple complex, moats, causeways, urban grid"
            }
        }
    
    def check_system_status(self) -> bool:
        """Verificar que el sistema esté operacional."""
        
        print("🔍 Verificando estado del sistema ArcheoScope...")
        
        try:
            # Estado básico
            response = requests.get(f"{self.base_url}/status", timeout=10)
            if response.status_code != 200:
                print(f"❌ Sistema no disponible: {response.status_code}")
                return False
            
            status = response.json()
            print(f"✅ Backend: {status['backend_status']}")
            print(f"✅ IA: {status['ai_status']}")
            print(f"✅ Reglas arqueológicas: {len(status['available_rules'])}")
            
            # Estado académico
            response = requests.get(f"{self.base_url}/academic/validation/status", timeout=10)
            if response.status_code == 200:
                validation = response.json()
                print(f"✅ Sistema de validación: {validation['validation_system']}")
                print(f"✅ Sitios conocidos: {validation['known_sites_database']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error conectando con ArcheoScope: {e}")
            print("   Asegúrate de ejecutar: python archeoscope/backend/api/main.py")
            return False
    
    def analyze_archaeological_site(self, site_key: str, site_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar un sitio arqueológico específico."""
        
        print(f"\n🏛️  ANALIZANDO: {site_data['name']}")
        print("=" * 60)
        
        # Preparar solicitud de análisis
        analysis_request = {
            "lat_min": site_data["lat_min"],
            "lat_max": site_data["lat_max"], 
            "lon_min": site_data["lon_min"],
            "lon_max": site_data["lon_max"],
            "region_name": site_data["name"],
            "resolution_m": 500,  # Alta resolución para sitios arqueológicos
            "include_explainability": True,
            "include_validation_metrics": True
        }
        
        start_time = time.time()
        
        try:
            print(f"📍 Coordenadas: ({site_data['lat_min']:.3f}, {site_data['lon_min']:.3f}) - ({site_data['lat_max']:.3f}, {site_data['lon_max']:.3f})")
            print(f"🌍 Tipo de paisaje: {site_data['landscape_type']}")
            print(f"🏺 Estructuras conocidas: {site_data['known_structures']}")
            print("⏳ Ejecutando análisis arqueológico...")
            
            # Ejecutar análisis
            response = requests.post(
                f"{self.base_url}/analyze", 
                json=analysis_request, 
                timeout=120  # 2 minutos para análisis completo
            )
            
            analysis_time = time.time() - start_time
            
            if response.status_code != 200:
                print(f"❌ Error en análisis: {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "site": site_key}
            
            result = response.json()
            
            # Extraer métricas clave
            metrics = self.extract_key_metrics(result, site_data, analysis_time)
            
            # Evaluar rendimiento
            performance = self.evaluate_performance(metrics, site_data)
            
            # Mostrar resultados
            self.display_results(metrics, performance, site_data)
            
            return {
                "site": site_key,
                "site_name": site_data["name"],
                "metrics": metrics,
                "performance": performance,
                "analysis_time": analysis_time,
                "success": True
            }
            
        except Exception as e:
            analysis_time = time.time() - start_time
            print(f"❌ Error durante análisis: {e}")
            return {
                "site": site_key,
                "site_name": site_data["name"], 
                "error": str(e),
                "analysis_time": analysis_time,
                "success": False
            }
    
    def extract_key_metrics(self, result: Dict[str, Any], site_data: Dict[str, Any], analysis_time: float) -> Dict[str, Any]:
        """Extraer métricas clave del análisis."""
        
        # Métricas básicas
        region_info = result.get("region_info", {})
        system_status = result.get("system_status", {})
        
        # Métricas de anomalías
        statistical_results = result.get("statistical_results", {})
        physics_results = result.get("physics_results", {})
        
        # Métricas de IA
        ai_explanations = result.get("ai_explanations", {})
        
        # Métricas académicas
        explainability = result.get("explainability_analysis", {})
        validation_metrics = result.get("validation_metrics", {})
        
        # Mapa de anomalías
        anomaly_map = result.get("anomaly_map", {})
        statistics = anomaly_map.get("statistics", {})
        
        return {
            "analysis_time_seconds": analysis_time,
            "area_km2": region_info.get("area_km2", 0),
            "resolution_m": region_info.get("resolution_m", 0),
            
            # Detección de anomalías
            "anomalies_detected": system_status.get("anomalies_detected", 0),
            "rules_evaluated": system_status.get("rules_evaluated", 0),
            "archaeological_signature_percentage": statistics.get("archaeological_signature_percentage", 0),
            "spatial_anomaly_percentage": statistics.get("spatial_anomaly_percentage", 0),
            "natural_percentage": statistics.get("natural_percentage", 100),
            
            # Evaluaciones de reglas
            "vegetation_rule": self.extract_rule_metrics(physics_results, "vegetation_topography_decoupling"),
            "thermal_rule": self.extract_rule_metrics(physics_results, "thermal_residual_patterns"),
            
            # IA y explicabilidad
            "ai_available": ai_explanations.get("ai_available", False),
            "ai_explanation": ai_explanations.get("explanation", "No disponible"),
            "archaeological_interpretation": ai_explanations.get("archaeological_interpretation", "No disponible"),
            "confidence_notes": ai_explanations.get("confidence_notes", "No disponible"),
            
            # Métricas académicas
            "explainability_count": explainability.get("total_explanations", 0) if explainability else 0,
            "academic_quality": validation_metrics.get("academic_quality", {}) if validation_metrics else {},
            "publication_ready": validation_metrics.get("validation_summary", {}).get("publication_ready", False) if validation_metrics else False
        }
    
    def extract_rule_metrics(self, physics_results: Dict[str, Any], rule_name: str) -> Dict[str, Any]:
        """Extraer métricas de una regla específica."""
        
        evaluations = physics_results.get("evaluations", {})
        rule_data = evaluations.get(rule_name, {})
        
        return {
            "result": rule_data.get("result", "unknown"),
            "archaeological_probability": rule_data.get("archaeological_probability", 0.0),
            "confidence": rule_data.get("confidence", 0.0),
            "geometric_coherence": rule_data.get("geometric_coherence", 0.0),
            "affected_pixels": rule_data.get("affected_pixels", 0)
        }
    
    def evaluate_performance(self, metrics: Dict[str, Any], site_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluar rendimiento del análisis."""
        
        # Criterios de evaluación
        archaeological_sig = metrics["archaeological_signature_percentage"]
        spatial_anomalies = metrics["spatial_anomaly_percentage"] 
        natural_processes = metrics["natural_percentage"]
        
        # Evaluación de reglas
        veg_prob = metrics["vegetation_rule"]["archaeological_probability"]
        thermal_prob = metrics["thermal_rule"]["archaeological_probability"]
        
        # Evaluación de IA
        ai_available = metrics["ai_available"]
        
        # Puntuación de detección (0-100)
        detection_score = min(100, (
            archaeological_sig * 3 +  # Firmas arqueológicas son más importantes
            spatial_anomalies * 1.5 +  # Anomalías espaciales
            (100 - natural_processes) * 0.5 +  # Menos procesos naturales = mejor
            veg_prob * 30 +  # Regla de vegetación
            thermal_prob * 20  # Regla térmica
        ))
        
        # Evaluación cualitativa
        if detection_score > 80:
            detection_quality = "EXCELENTE"
        elif detection_score > 60:
            detection_quality = "BUENA"
        elif detection_score > 40:
            detection_quality = "MODERADA"
        elif detection_score > 20:
            detection_quality = "BAJA"
        else:
            detection_quality = "MUY BAJA"
        
        # Evaluación de tiempo
        analysis_time = metrics["analysis_time_seconds"]
        if analysis_time < 30:
            time_performance = "RÁPIDO"
        elif analysis_time < 60:
            time_performance = "MODERADO"
        elif analysis_time < 120:
            time_performance = "LENTO"
        else:
            time_performance = "MUY LENTO"
        
        # Evaluación de IA
        if ai_available:
            ai_performance = "DISPONIBLE"
        else:
            ai_performance = "NO DISPONIBLE"
        
        return {
            "detection_score": detection_score,
            "detection_quality": detection_quality,
            "time_performance": time_performance,
            "ai_performance": ai_performance,
            "expected_significance": site_data["archaeological_significance"],
            "meets_expectations": detection_score > 50 if site_data["archaeological_significance"] in ["high", "very_high"] else detection_score > 30
        }
    
    def display_results(self, metrics: Dict[str, Any], performance: Dict[str, Any], site_data: Dict[str, Any]):
        """Mostrar resultados del análisis."""
        
        print(f"\n📊 RESULTADOS DEL ANÁLISIS")
        print("-" * 40)
        
        # Métricas básicas
        print(f"⏱️  Tiempo de análisis: {metrics['analysis_time_seconds']:.1f}s ({performance['time_performance']})")
        print(f"📏 Área analizada: {metrics['area_km2']:.1f} km²")
        print(f"🔍 Resolución: {metrics['resolution_m']}m")
        
        # Detección de anomalías
        print(f"\n🎯 DETECCIÓN DE ANOMALÍAS:")
        print(f"   🔴 Firmas arqueológicas: {metrics['archaeological_signature_percentage']:.1f}%")
        print(f"   🟡 Anomalías espaciales: {metrics['spatial_anomaly_percentage']:.1f}%")
        print(f"   🟢 Procesos naturales: {metrics['natural_percentage']:.1f}%")
        print(f"   📈 Anomalías totales detectadas: {metrics['anomalies_detected']}")
        
        # Evaluación de reglas
        print(f"\n🧪 EVALUACIÓN DE REGLAS ARQUEOLÓGICAS:")
        veg_rule = metrics['vegetation_rule']
        thermal_rule = metrics['thermal_rule']
        
        print(f"   🌱 Vegetación-Topografía: {veg_rule['result']} (prob: {veg_rule['archaeological_probability']:.2f})")
        print(f"   🌡️  Patrones Térmicos: {thermal_rule['result']} (prob: {thermal_rule['archaeological_probability']:.2f})")
        
        # IA y explicabilidad
        print(f"\n🤖 ANÁLISIS DE IA:")
        print(f"   Estado: {performance['ai_performance']}")
        if metrics['ai_available']:
            print(f"   🧠 Interpretación arqueológica disponible")
            print(f"   📝 Explicaciones generadas: {metrics['explainability_count']}")
        
        # Evaluación académica
        if metrics['academic_quality']:
            academic = metrics['academic_quality']
            print(f"\n🎓 CALIDAD ACADÉMICA:")
            print(f"   Rigor metodológico: {academic.get('methodological_rigor', 'unknown')}")
            print(f"   Listo para publicación: {'SÍ' if metrics['publication_ready'] else 'NO'}")
        
        # Puntuación final
        print(f"\n⭐ EVALUACIÓN FINAL:")
        print(f"   Puntuación de detección: {performance['detection_score']:.1f}/100")
        print(f"   Calidad de detección: {performance['detection_quality']}")
        print(f"   Cumple expectativas: {'SÍ' if performance['meets_expectations'] else 'NO'}")
        
        # Interpretación arqueológica de IA (si disponible)
        if metrics['ai_available'] and metrics['archaeological_interpretation'] != "No disponible":
            print(f"\n🏛️  INTERPRETACIÓN ARQUEOLÓGICA (IA):")
            interpretation = metrics['archaeological_interpretation'][:200]
            print(f"   {interpretation}{'...' if len(metrics['archaeological_interpretation']) > 200 else ''}")
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Ejecutar prueba comprehensiva de todos los sitios."""
        
        print("🏛️  ARCHEOSCOPE - PRUEBAS EXHAUSTIVAS DE SITIOS ARQUEOLÓGICOS")
        print("=" * 80)
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Sitios a probar: {len(self.archaeological_sites)}")
        
        # Verificar sistema
        if not self.check_system_status():
            return {"error": "Sistema no disponible"}
        
        # Analizar cada sitio
        results = []
        total_start_time = time.time()
        
        for site_key, site_data in self.archaeological_sites.items():
            result = self.analyze_archaeological_site(site_key, site_data)
            results.append(result)
            self.test_results.append(result)
            
            # Pausa entre análisis
            time.sleep(2)
        
        total_time = time.time() - total_start_time
        
        # Generar resumen
        summary = self.generate_summary(results, total_time)
        
        return {
            "summary": summary,
            "detailed_results": results,
            "total_time": total_time
        }
    
    def generate_summary(self, results: List[Dict[str, Any]], total_time: float) -> Dict[str, Any]:
        """Generar resumen de todas las pruebas."""
        
        print(f"\n🏆 RESUMEN GENERAL DE PRUEBAS")
        print("=" * 60)
        
        successful_tests = [r for r in results if r.get("success", False)]
        failed_tests = [r for r in results if not r.get("success", False)]
        
        print(f"✅ Pruebas exitosas: {len(successful_tests)}/{len(results)}")
        print(f"❌ Pruebas fallidas: {len(failed_tests)}")
        print(f"⏱️  Tiempo total: {total_time:.1f}s")
        
        if successful_tests:
            # Estadísticas de rendimiento
            detection_scores = [r["performance"]["detection_score"] for r in successful_tests]
            analysis_times = [r["analysis_time"] for r in successful_tests]
            ai_available_count = sum(1 for r in successful_tests if r["metrics"]["ai_available"])
            
            avg_detection = sum(detection_scores) / len(detection_scores)
            avg_time = sum(analysis_times) / len(analysis_times)
            
            print(f"\n📊 ESTADÍSTICAS DE RENDIMIENTO:")
            print(f"   Puntuación promedio de detección: {avg_detection:.1f}/100")
            print(f"   Tiempo promedio de análisis: {avg_time:.1f}s")
            print(f"   IA disponible en: {ai_available_count}/{len(successful_tests)} pruebas")
            
            # Mejores y peores resultados
            best_result = max(successful_tests, key=lambda x: x["performance"]["detection_score"])
            worst_result = min(successful_tests, key=lambda x: x["performance"]["detection_score"])
            
            print(f"\n🥇 MEJOR RESULTADO:")
            print(f"   {best_result['site_name']}: {best_result['performance']['detection_score']:.1f}/100")
            
            print(f"\n🥉 RESULTADO MÁS BAJO:")
            print(f"   {worst_result['site_name']}: {worst_result['performance']['detection_score']:.1f}/100")
            
            # Evaluación por tipo de sitio
            print(f"\n🏛️  EVALUACIÓN POR SITIO:")
            for result in successful_tests:
                site_name = result["site_name"]
                score = result["performance"]["detection_score"]
                quality = result["performance"]["detection_quality"]
                meets_exp = "✅" if result["performance"]["meets_expectations"] else "❌"
                
                print(f"   {meets_exp} {site_name}: {score:.1f}/100 ({quality})")
        
        if failed_tests:
            print(f"\n❌ PRUEBAS FALLIDAS:")
            for result in failed_tests:
                print(f"   {result['site_name']}: {result.get('error', 'Error desconocido')}")
        
        # Evaluación general del sistema
        success_rate = len(successful_tests) / len(results) * 100
        
        if success_rate >= 80 and avg_detection >= 60:
            system_evaluation = "EXCELENTE - Sistema listo para uso arqueológico profesional"
        elif success_rate >= 60 and avg_detection >= 45:
            system_evaluation = "BUENO - Sistema funcional con mejoras menores necesarias"
        elif success_rate >= 40:
            system_evaluation = "MODERADO - Sistema requiere optimización"
        else:
            system_evaluation = "NECESITA MEJORAS - Sistema requiere desarrollo adicional"
        
        print(f"\n🎯 EVALUACIÓN GENERAL DEL SISTEMA:")
        print(f"   {system_evaluation}")
        print(f"   Tasa de éxito: {success_rate:.1f}%")
        
        return {
            "total_tests": len(results),
            "successful_tests": len(successful_tests),
            "failed_tests": len(failed_tests),
            "success_rate": success_rate,
            "average_detection_score": avg_detection if successful_tests else 0,
            "average_analysis_time": avg_time if successful_tests else 0,
            "ai_availability_rate": (ai_available_count / len(successful_tests) * 100) if successful_tests else 0,
            "system_evaluation": system_evaluation,
            "best_site": best_result["site_name"] if successful_tests else None,
            "worst_site": worst_result["site_name"] if successful_tests else None
        }
    
    def save_results(self, filename: str = None):
        """Guardar resultados de las pruebas."""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"archeoscope_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Resultados guardados en: {filename}")

def main():
    """Ejecutar pruebas exhaustivas de ArcheoScope."""
    
    tester = ArchaeologicalSiteTester()
    
    try:
        # Ejecutar pruebas comprehensivas
        results = tester.run_comprehensive_test()
        
        if "error" in results:
            print(f"❌ Error en pruebas: {results['error']}")
            return False
        
        # Guardar resultados
        tester.save_results()
        
        print(f"\n🎉 PRUEBAS COMPLETADAS EXITOSAMENTE")
        print(f"📊 Resumen disponible arriba")
        print(f"💾 Resultados detallados guardados en archivo JSON")
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Pruebas interrumpidas por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)