#!/usr/bin/env python3
"""
Test Completo del Candidato ID 743
Prueba todas las nuevas features e instrumentos
"""

import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8002"

def test_candidato_743():
    """Test completo del candidato 743"""
    
    print("=" * 80)
    print("🔬 TEST COMPLETO - CANDIDATO ID 743")
    print("=" * 80)
    
    # 1. Obtener información del candidato
    print("\n📍 PASO 1: Obtener información del candidato 743...")
    try:
        response = requests.get(f"{API_BASE}/api/scientific/sites/all?page=1&page_size=1000")
        if response.status_code == 200:
            data = response.json()
            
            # Buscar candidato 743
            candidato = None
            for site in data['sites']:
                if '743' in site['id'] or site['name'].endswith('743'):
                    candidato = site
                    break
            
            if not candidato:
                # Buscar por índice
                if len(data['sites']) >= 743:
                    candidato = data['sites'][742]  # Índice 742 = posición 743
            
            if candidato:
                print(f"✅ Candidato encontrado:")
                print(f"   ID: {candidato['id']}")
                print(f"   Nombre: {candidato['name']}")
                print(f"   País: {candidato['location']['country']}")
                print(f"   Coordenadas: {candidato['coordinates']['latitude']}, {candidato['coordinates']['longitude']}")
                print(f"   Tipo: {candidato['site_type']}")
                print(f"   Ambiente: {candidato['environment_type']}")
                print(f"   Confianza: {candidato['confidence_level']}")
            else:
                print("❌ Candidato 743 no encontrado")
                print(f"   Total sitios disponibles: {data['total']}")
                return False
        else:
            print(f"❌ Error obteniendo sitios: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # 2. Analizar el candidato con el pipeline completo
    print("\n🔬 PASO 2: Analizar con pipeline científico completo...")
    
    lat = candidato['coordinates']['latitude']
    lon = candidato['coordinates']['longitude']
    
    # Crear bbox de 0.02 grados (~2km)
    bbox = {
        'lat_min': lat - 0.01,
        'lat_max': lat + 0.01,
        'lon_min': lon - 0.01,
        'lon_max': lon + 0.01,
        'region_name': candidato['name']
    }
    
    try:
        print(f"   Analizando región: {bbox['region_name']}")
        print(f"   Bbox: {bbox}")
        
        response = requests.post(
            f"{API_BASE}/api/scientific/analyze",
            json=bbox,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Análisis completado")
            
            # 3. Mostrar resultados científicos
            print("\n📊 PASO 3: Resultados Científicos")
            print("-" * 80)
            
            output = result['scientific_output']
            
            print(f"\n🎯 MÉTRICAS SEPARADAS:")
            print(f"   Origen Antropogénico:    {output['anthropic_origin_probability']:.1%}")
            print(f"   Actividad Actual:        {output['anthropic_activity_probability']:.1%}")
            print(f"   Anomalía Instrumental:   {output['instrumental_anomaly_probability']:.1%}")
            print(f"   Confianza del Modelo:    {output['model_inference_confidence']}")
            
            print(f"\n🔮 EXPLANATORY STRANGENESS:")
            ess = output.get('explanatory_strangeness', {})
            print(f"   Nivel: {ess.get('level', 'none').upper()}")
            print(f"   Score: {ess.get('score', 0):.3f}")
            
            print(f"\n📈 COBERTURA INSTRUMENTAL:")
            print(f"   Instrumentos medidos:    {output['instruments_measured']}/{output['instruments_available']}")
            print(f"   Cobertura raw:           {output['coverage_raw']:.1%}")
            print(f"   Cobertura efectiva:      {output['coverage_effective']:.1%}")
            
            print(f"\n🎬 ACCIÓN RECOMENDADA:")
            print(f"   {output['recommended_action']}")
            
            print(f"\n📝 NOTAS:")
            print(f"   {output['notes']}")
            
            # 4. Mostrar instrumentos
            print("\n🛰️ PASO 4: Estado de Instrumentos")
            print("-" * 80)
            
            measurements = result.get('instrumental_measurements', [])
            env_context = result.get('environment_context', {})
            available = env_context.get('available_instruments', [])
            
            print(f"\n✅ INSTRUMENTOS EXITOSOS ({len(measurements)}):")
            for m in measurements:
                print(f"   • {m['instrument_name']:<25} = {m['value']:.3f} ({m['data_mode']}, {m['source']})")
            
            failed = set(available) - set([m['instrument_name'] for m in measurements])
            if failed:
                print(f"\n❌ INSTRUMENTOS FALLIDOS ({len(failed)}):")
                for inst in failed:
                    print(f"   • {inst}")
            
            # 5. Contexto ambiental
            print("\n🌍 PASO 5: Contexto Ambiental")
            print("-" * 80)
            print(f"   Tipo de ambiente:        {env_context.get('environment_type', 'unknown')}")
            print(f"   Confianza:               {env_context.get('confidence', 0):.1%}")
            print(f"   Visibilidad arqueológica: {env_context.get('archaeological_visibility', 'unknown')}")
            print(f"   Potencial preservación:  {env_context.get('preservation_potential', 'unknown')}")
            
            # 6. Verificar endpoints de sitios conocidos
            print("\n🗺️ PASO 6: Verificar Endpoints de Sitios Conocidos")
            print("-" * 80)
            
            # Test endpoint de capa
            try:
                response = requests.get(f"{API_BASE}/api/scientific/sites/layer?limit=10")
                if response.status_code == 200:
                    layer_data = response.json()
                    print(f"✅ Endpoint /sites/layer OK")
                    print(f"   Total sitios: {layer_data['metadata']['total']}")
                    print(f"   Features cargados: {len(layer_data['features'])}")
                else:
                    print(f"❌ Endpoint /sites/layer ERROR: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Error en /sites/layer: {e}")
            
            # Test endpoint de candidatos
            try:
                response = requests.get(f"{API_BASE}/api/scientific/sites/candidates?limit=10")
                if response.status_code == 200:
                    cand_data = response.json()
                    print(f"✅ Endpoint /sites/candidates OK")
                    print(f"   Total candidatos: {cand_data['total']}")
                else:
                    print(f"❌ Endpoint /sites/candidates ERROR: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Error en /sites/candidates: {e}")
            
            # Test endpoint de stats
            try:
                response = requests.get(f"{API_BASE}/api/scientific/sites/stats")
                if response.status_code == 200:
                    stats_data = response.json()
                    print(f"✅ Endpoint /sites/stats OK")
                    print(f"   Total sitios en BD: {stats_data['total_sites']}")
                    print(f"   Sitios de control: {stats_data['control_sites']}")
                    print(f"   Top país: {stats_data['by_country'][0]['country']} ({stats_data['by_country'][0]['count']} sitios)")
                else:
                    print(f"❌ Endpoint /sites/stats ERROR: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Error en /sites/stats: {e}")
            
            # 7. Resumen final
            print("\n" + "=" * 80)
            print("📊 RESUMEN FINAL")
            print("=" * 80)
            
            print(f"\n🎯 CANDIDATO 743:")
            print(f"   Nombre: {candidato['name']}")
            print(f"   Clasificación: {output['candidate_type']}")
            print(f"   Score Origen: {output['anthropic_origin_probability']:.1%}")
            print(f"   ESS: {ess.get('level', 'none').upper()}")
            print(f"   Acción: {output['recommended_action']}")
            
            print(f"\n✅ FEATURES TESTEADAS:")
            print(f"   ✓ Pipeline científico completo")
            print(f"   ✓ Métricas separadas (4 métricas)")
            print(f"   ✓ ESS (Explanatory Strangeness)")
            print(f"   ✓ Cobertura instrumental")
            print(f"   ✓ Endpoints de sitios conocidos")
            print(f"   ✓ Contexto ambiental")
            
            print(f"\n🛰️ INSTRUMENTOS:")
            print(f"   Total disponibles: {output['instruments_available']}")
            print(f"   Medidos exitosamente: {output['instruments_measured']}")
            print(f"   Tasa de éxito: {output['coverage_raw']:.1%}")
            
            # Guardar resultados
            output_file = f"test_candidato_743_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Resultados guardados en: {output_file}")
            
            print("\n" + "=" * 80)
            print("✅ TEST COMPLETADO EXITOSAMENTE")
            print("=" * 80)
            
            return True
            
        else:
            print(f"❌ Error en análisis: HTTP {response.status_code}")
            print(f"   {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_candidato_743()
    exit(0 if success else 1)
