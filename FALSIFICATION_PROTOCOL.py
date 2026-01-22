#!/usr/bin/env python3
"""
PROTOCOLO DE FALSACIÓN ACTIVA - ArcheoScope
Controles negativos para validar la hipótesis de persistencia funcional antrópica
"""

import requests
import json
import sys
from datetime import datetime

class FalsificationProtocol:
    """Protocolo científico para falsación activa de hipótesis ArcheoScope"""
    
    def __init__(self):
        self.base_url = "http://localhost:8002"
        self.results = {}
        
    def analyze_control_site(self, site_name, coordinates, expected_result):
        """Analizar sitio de control con predicción falsable"""
        
        print(f"\n🔬 CONTROL NEGATIVO: {site_name}")
        print("=" * 60)
        print(f"📍 Coordenadas: {coordinates['lat_min']}, {coordinates['lon_min']}")
        print(f"🎯 Predicción: {expected_result}")
        
        request_data = {
            **coordinates,
            "resolution_m": 500,
            "layers_to_analyze": [
                "ndvi_vegetation",
                "thermal_lst", 
                "sar_backscatter",
                "surface_roughness",
                "soil_salinity"
            ],
            "active_rules": ["all"],
            "region_name": f"Control Negativo: {site_name}",
            "include_explainability": True,
            "include_validation_metrics": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                json=request_data,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Guardar resultados
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"control_{site_name.lower().replace(' ', '_')}_{timestamp}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Evaluar falsación
                result = self.evaluate_falsification(data, expected_result, site_name)
                self.results[site_name] = result
                
                return data
                
            else:
                print(f"❌ Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def evaluate_falsification(self, data, expected_result, site_name):
        """Evaluar si los resultados falsifican o confirman la hipótesis"""
        
        # Extraer métricas clave
        stats = data.get('statistical_results', {})
        
        # Calcular persistencia temporal promedio
        temporal_scores = []
        for layer, metrics in stats.items():
            if 'temporal_persistence' in metrics:
                temporal_scores.append(metrics['temporal_persistence'])
        
        avg_temporal_persistence = sum(temporal_scores) / len(temporal_scores) if temporal_scores else 0
        
        # Calcular probabilidad arqueológica promedio
        archaeological_scores = []
        for layer, metrics in stats.items():
            if 'archaeological_probability' in metrics:
                archaeological_scores.append(metrics['archaeological_probability'])
        
        avg_archaeological_prob = sum(archaeological_scores) / len(archaeological_scores) if archaeological_scores else 0
        
        # Evaluación de falsación
        print(f"\n📊 RESULTADOS DE FALSACIÓN:")
        print(f"   Persistencia Temporal Promedio: {avg_temporal_persistence:.3f}")
        print(f"   Probabilidad Arqueológica Promedio: {avg_archaeological_prob:.3f}")
        
        # Criterios de falsación
        high_persistence_threshold = 0.80  # 80%
        high_archaeological_threshold = 0.60  # 60%
        
        if expected_result == "low_persistence":
            if avg_temporal_persistence > high_persistence_threshold:
                print(f"⚠️  FALSACIÓN PARCIAL: Persistencia inesperadamente alta ({avg_temporal_persistence:.1%})")
                print(f"   Esto sugiere que el sitio 'control' puede no ser natural")
                falsification_status = "FALSIFIED"
            else:
                print(f"✅ CONFIRMACIÓN: Persistencia baja como esperado ({avg_temporal_persistence:.1%})")
                falsification_status = "CONFIRMED"
        
        elif expected_result == "natural_processes":
            if avg_archaeological_prob > high_archaeological_threshold:
                print(f"⚠️  FALSACIÓN PARCIAL: Probabilidad arqueológica inesperadamente alta ({avg_archaeological_prob:.1%})")
                falsification_status = "FALSIFIED"
            else:
                print(f"✅ CONFIRMACIÓN: Procesos naturales dominantes ({avg_archaeological_prob:.1%})")
                falsification_status = "CONFIRMED"
        
        return {
            'site_name': site_name,
            'temporal_persistence': avg_temporal_persistence,
            'archaeological_probability': avg_archaeological_prob,
            'expected_result': expected_result,
            'falsification_status': falsification_status,
            'interpretation': self.interpret_result(falsification_status, site_name)
        }
    
    def interpret_result(self, status, site_name):
        """Interpretar resultado de falsación"""
        
        if status == "CONFIRMED":
            return f"El sitio {site_name} se comporta como esperado para un control negativo, fortaleciendo la hipótesis de que ArcheoScope detecta específicamente persistencia antrópica."
        
        elif status == "FALSIFIED":
            return f"El sitio {site_name} muestra persistencia inesperada, sugiriendo: (1) el sitio no es realmente 'natural', (2) ArcheoScope detecta procesos naturales no conocidos, o (3) la metodología requiere calibración."
        
        else:
            return "Resultado ambiguo - requiere análisis adicional."
    
    def run_complete_falsification_protocol(self):
        """Ejecutar protocolo completo de falsación"""
        
        print("🧪 PROTOCOLO DE FALSACIÓN ACTIVA - ARCHEOSCOPE")
        print("Validación científica de hipótesis de persistencia funcional antrópica")
        print("=" * 80)
        
        # Control 1: Selva Africana (Congo) - Sin contacto precolombino
        congo_coords = {
            "lat_min": -2.200,
            "lat_max": -2.100,
            "lon_min": 24.650,
            "lon_max": 24.750
        }
        self.analyze_control_site(
            "Selva Congo (África)", 
            congo_coords, 
            "low_persistence"
        )
        
        # Control 2: Bosque Boreal (Canadá) - Sin manejo milenario
        boreal_coords = {
            "lat_min": 55.100,
            "lat_max": 55.200,
            "lon_min": -112.200,
            "lon_max": -112.100
        }
        self.analyze_control_site(
            "Bosque Boreal Canadá", 
            boreal_coords, 
            "natural_processes"
        )
        
        # Control 3: Manglar Australia - Sistema natural puro
        mangrove_coords = {
            "lat_min": -16.300,
            "lat_max": -16.200,
            "lon_min": 145.400,
            "lon_max": 145.500
        }
        self.analyze_control_site(
            "Manglar Australia", 
            mangrove_coords, 
            "natural_processes"
        )
        
        # Control 4: Desierto Sahara - Ambiente extremo
        sahara_coords = {
            "lat_min": 23.100,
            "lat_max": 23.200,
            "lon_min": 5.400,
            "lon_max": 5.500
        }
        self.analyze_control_site(
            "Desierto Sahara", 
            sahara_coords, 
            "low_persistence"
        )
        
        # Control 5: Océano Pacífico - Control absoluto
        ocean_coords = {
            "lat_min": -10.100,
            "lat_max": -10.000,
            "lon_min": -140.100,
            "lon_max": -140.000
        }
        self.analyze_control_site(
            "Océano Pacífico", 
            ocean_coords, 
            "natural_processes"
        )
        
        # Generar reporte de falsación
        self.generate_falsification_report()
    
    def generate_falsification_report(self):
        """Generar reporte científico de falsación"""
        
        print("\n" + "=" * 80)
        print("📋 REPORTE DE FALSACIÓN CIENTÍFICA")
        print("=" * 80)
        
        confirmed_count = sum(1 for r in self.results.values() if r['falsification_status'] == 'CONFIRMED')
        falsified_count = sum(1 for r in self.results.values() if r['falsification_status'] == 'FALSIFIED')
        total_count = len(self.results)
        
        print(f"\n📊 RESUMEN ESTADÍSTICO:")
        print(f"   Total de controles: {total_count}")
        print(f"   Hipótesis confirmada: {confirmed_count} ({confirmed_count/total_count*100:.1f}%)")
        print(f"   Hipótesis falsificada: {falsified_count} ({falsified_count/total_count*100:.1f}%)")
        
        print(f"\n🔬 EVALUACIÓN CIENTÍFICA:")
        
        if confirmed_count >= total_count * 0.8:  # 80% o más confirmados
            print("✅ HIPÓTESIS FUERTEMENTE RESPALDADA")
            print("   Los controles negativos se comportan como esperado.")
            print("   ArcheoScope parece detectar específicamente persistencia antrópica.")
            
        elif falsified_count >= total_count * 0.6:  # 60% o más falsificados
            print("❌ HIPÓTESIS FALSIFICADA")
            print("   Los controles negativos muestran persistencia inesperada.")
            print("   La metodología requiere recalibración o la hipótesis es incorrecta.")
            
        else:
            print("⚠️  RESULTADOS MIXTOS")
            print("   Algunos controles confirman, otros falsifican la hipótesis.")
            print("   Se requiere análisis adicional y refinamiento metodológico.")
        
        print(f"\n📋 DETALLES POR SITIO:")
        for site_name, result in self.results.items():
            status_icon = "✅" if result['falsification_status'] == 'CONFIRMED' else "❌"
            print(f"   {status_icon} {site_name}:")
            print(f"      Persistencia: {result['temporal_persistence']:.1%}")
            print(f"      Prob. Arqueológica: {result['archaeological_probability']:.1%}")
            print(f"      Estado: {result['falsification_status']}")
        
        print(f"\n🎯 CONCLUSIÓN METODOLÓGICA:")
        print("   La validez de ArcheoScope para detectar persistencia antrópica")
        print("   depende de que los controles negativos se comporten como esperado.")
        print("   Este protocolo proporciona la base empírica para esa validación.")
        
        # Guardar reporte
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"falsification_report_{timestamp}.json"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump({
                'protocol_summary': {
                    'total_controls': total_count,
                    'confirmed': confirmed_count,
                    'falsified': falsified_count,
                    'confirmation_rate': confirmed_count/total_count if total_count > 0 else 0
                },
                'detailed_results': self.results,
                'scientific_conclusion': self.get_scientific_conclusion(confirmed_count, total_count)
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Reporte guardado en: {report_filename}")
    
    def get_scientific_conclusion(self, confirmed_count, total_count):
        """Obtener conclusión científica basada en resultados"""
        
        confirmation_rate = confirmed_count / total_count if total_count > 0 else 0
        
        if confirmation_rate >= 0.8:
            return "HYPOTHESIS_STRONGLY_SUPPORTED"
        elif confirmation_rate >= 0.6:
            return "HYPOTHESIS_MODERATELY_SUPPORTED"
        elif confirmation_rate >= 0.4:
            return "MIXED_RESULTS_REQUIRE_FURTHER_ANALYSIS"
        else:
            return "HYPOTHESIS_FALSIFIED_OR_METHODOLOGY_FLAWED"

def main():
    """Función principal"""
    
    protocol = FalsificationProtocol()
    
    print("⚠️  ADVERTENCIA CIENTÍFICA:")
    print("Este protocolo ejecutará análisis en múltiples sitios de control.")
    print("Los resultados determinarán la validez científica de ArcheoScope.")
    print("¿Continuar? (y/n): ", end="")
    
    # Para automatización, asumir 'y'
    response = 'y'  # input().lower()
    
    if response == 'y':
        protocol.run_complete_falsification_protocol()
    else:
        print("Protocolo cancelado.")

if __name__ == "__main__":
    main()