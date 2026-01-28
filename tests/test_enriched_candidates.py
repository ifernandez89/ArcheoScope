#!/usr/bin/env python3
"""
Test del endpoint de candidatas enriquecidas multi-instrumentalmente
"""

import requests
import json

def test_enriched_candidates():
    """Test del endpoint de candidatas enriquecidas"""
    
    print("🔬 Testing Multi-Instrumental Enriched Candidates Endpoint")
    print("=" * 80)
    
    # Región de Petén, Guatemala
    url = "http://localhost:8002/archaeological-sites/enriched-candidates"
    params = {
        'lat_min': 16.0,
        'lat_max': 18.0,
        'lon_min': -91.0,
        'lon_max': -89.0,
        'strategy': 'buffer',
        'max_zones': 20,
        'lidar_priority': True,
        'min_convergence': 0.4
    }
    
    try:
        print(f"\n📡 Llamando a: {url}")
        print(f"   Parámetros: {params}")
        
        response = requests.get(url, params=params, timeout=60)
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n📊 Resultados:")
            print(f"   Total candidatas: {data['total_candidates']}")
            
            stats = data['statistics']
            print(f"\n🎯 Estadísticas:")
            print(f"   Field validation priority: {stats['field_validation_priority']}")
            print(f"   Detailed analysis: {stats['detailed_analysis']}")
            print(f"   Monitor: {stats['monitor']}")
            print(f"   Convergencia promedio: {stats['average_convergence']}")
            print(f"   Score multi-instrumental promedio: {stats['average_multi_score']}")
            print(f"   Persistencia temporal detectada: {stats['temporal_persistence_detected']}")
            
            print(f"\n🛰️ Instrumentos Detectores:")
            for instrument, count in stats['instrument_detection_counts'].items():
                print(f"   {instrument}: {count} detecciones")
            
            # Mostrar top 3 candidatas
            print(f"\n🔥 Top 3 Candidatas:")
            for i, candidate in enumerate(data['candidates'][:3]):
                print(f"\n   {i+1}. {candidate['candidate_id']}")
                print(f"      Score: {candidate['multi_instrumental_score']}")
                print(f"      Convergencia: {candidate['convergence']['count']}/{candidate['convergence']['total_instruments']} ({candidate['convergence']['ratio']})")
                print(f"      Acción: {candidate['recommended_action']}")
                print(f"      Persistencia: {candidate['temporal_persistence']['years']} años" if candidate['temporal_persistence']['detected'] else "      Persistencia: No detectada")
                
                print(f"      Señales detectadas:")
                for inst, signal in candidate['signals'].items():
                    if signal['detected']:
                        print(f"        ✅ {inst}: {signal['confidence']} - {signal['interpretation'][:60]}...")
            
            # Mostrar metodología
            print(f"\n🧠 Metodología:")
            method = data['methodology']
            print(f"   Approach: {method['approach']}")
            print(f"   Combo: {method['combo_strategy']}")
            print(f"   Nota: {method['note']}")
            
            print(f"\n{'='*80}")
            print(f"✅ TEST EXITOSO - Candidatas enriquecidas generadas correctamente")
            print(f"{'='*80}")
            
            # Guardar resultado para inspección
            with open('enriched_candidates_test_result.json', 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\n💾 Resultado guardado en: enriched_candidates_test_result.json")
            
            return True
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_enriched_candidates()
    exit(0 if success else 1)
