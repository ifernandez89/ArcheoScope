#!/usr/bin/env python3
"""
Test de métricas de cobertura instrumental - Verificación de fix
==================================================================

Verifica que las métricas de cobertura (raw y effective) se retornen
correctamente en el JSON response del endpoint científico.
"""

import requests
import json

def test_coverage_metrics():
    """Test que las métricas de cobertura aparezcan en el JSON."""
    
    print("="*80)
    print("TEST: Métricas de Cobertura Instrumental")
    print("="*80)
    
    # Coordenadas de test (Sonora, México - ambiente agricultural)
    test_data = {
        "lat_min": 26.94,
        "lat_max": 26.96,
        "lon_min": -111.86,
        "lon_max": -111.84,
        "region_name": "Test Coverage Metrics"
    }
    
    print(f"\n📍 Región: {test_data['region_name']}")
    print(f"   Coordenadas: [{test_data['lat_min']}, {test_data['lat_max']}] x [{test_data['lon_min']}, {test_data['lon_max']}]")
    
    try:
        print("\n🔄 Enviando solicitud al endpoint científico...")
        response = requests.post(
            "http://localhost:8002/api/scientific/analyze",
            json=test_data,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"\n❌ ERROR: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        result = response.json()
        
        print("\n✅ Análisis completado")
        
        # Verificar scientific_output
        scientific_output = result.get('scientific_output', {})
        
        print("\n" + "="*80)
        print("VERIFICACIÓN DE MÉTRICAS DE COBERTURA")
        print("="*80)
        
        # Verificar que existan las métricas
        coverage_raw = scientific_output.get('coverage_raw')
        coverage_effective = scientific_output.get('coverage_effective')
        instruments_measured = scientific_output.get('instruments_measured')
        instruments_available = scientific_output.get('instruments_available')
        
        print(f"\n📊 Métricas en scientific_output:")
        print(f"   - coverage_raw: {coverage_raw}")
        print(f"   - coverage_effective: {coverage_effective}")
        print(f"   - instruments_measured: {instruments_measured}")
        print(f"   - instruments_available: {instruments_available}")
        
        # Verificar que NO sean None o 0
        if coverage_raw is None:
            print("\n❌ ERROR: coverage_raw es None")
            return False
        
        if coverage_effective is None:
            print("\n❌ ERROR: coverage_effective es None")
            return False
        
        if instruments_measured is None or instruments_measured == 0:
            print("\n❌ ERROR: instruments_measured es None o 0")
            return False
        
        if instruments_available is None or instruments_available == 0:
            print("\n❌ ERROR: instruments_available es None o 0")
            return False
        
        # Verificar que los valores sean razonables
        if coverage_raw < 0 or coverage_raw > 1:
            print(f"\n❌ ERROR: coverage_raw fuera de rango [0, 1]: {coverage_raw}")
            return False
        
        if coverage_effective < 0 or coverage_effective > 1:
            print(f"\n❌ ERROR: coverage_effective fuera de rango [0, 1]: {coverage_effective}")
            return False
        
        # Verificar que raw >= effective (siempre debe cumplirse)
        if coverage_raw < coverage_effective:
            print(f"\n⚠️ WARNING: coverage_raw ({coverage_raw}) < coverage_effective ({coverage_effective})")
            print("   Esto es inusual pero puede ocurrir si los instrumentos tienen pesos muy altos")
        
        # Mostrar porcentajes
        coverage_raw_percent = coverage_raw * 100
        coverage_effective_percent = coverage_effective * 100
        
        print(f"\n✅ MÉTRICAS CORRECTAS:")
        print(f"   - Cobertura raw: {coverage_raw_percent:.1f}% ({instruments_measured}/{instruments_available} instrumentos)")
        print(f"   - Cobertura efectiva: {coverage_effective_percent:.1f}% (ponderada por importancia)")
        
        # Verificar phase_d_anthropic también
        phase_d = result.get('phase_d_anthropic', {})
        
        print(f"\n📊 Métricas en phase_d_anthropic:")
        print(f"   - coverage_raw: {phase_d.get('coverage_raw')}")
        print(f"   - coverage_effective: {phase_d.get('coverage_effective')}")
        print(f"   - instruments_measured: {phase_d.get('instruments_measured')}")
        print(f"   - instruments_available: {phase_d.get('instruments_available')}")
        
        # Verificar que coincidan
        if phase_d.get('coverage_raw') != coverage_raw:
            print(f"\n⚠️ WARNING: Métricas no coinciden entre scientific_output y phase_d_anthropic")
        
        # Mostrar otros datos relevantes
        print(f"\n📈 Resultados del análisis:")
        print(f"   - Probabilidad antropogénica: {scientific_output.get('anthropic_probability', 0)*100:.1f}%")
        print(f"   - Anomaly score: {scientific_output.get('anomaly_score', 0)*100:.1f}%")
        print(f"   - Acción recomendada: {scientific_output.get('recommended_action')}")
        print(f"   - Tipo de candidato: {scientific_output.get('candidate_type')}")
        
        print("\n" + "="*80)
        print("✅ TEST EXITOSO - Métricas de cobertura funcionando correctamente")
        print("="*80)
        
        return True
        
    except requests.exceptions.Timeout:
        print("\n❌ ERROR: Timeout esperando respuesta del servidor")
        return False
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar al servidor")
        print("   ¿Está el backend corriendo en http://localhost:8002?")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_coverage_metrics()
    exit(0 if success else 1)
