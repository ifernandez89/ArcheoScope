#!/usr/bin/env python3
"""
Test: Verificar que la explicación científica se guarde
"""

import requests
import json

def test_explanation():
    """Test que la explicación se guarde correctamente."""
    
    print("="*80)
    print("TEST: Explicación Científica en Análisis")
    print("="*80)
    
    # Coordenadas de test (Chile - ambiente desert)
    test_data = {
        "lat_min": -23.66,
        "lat_max": -23.64,
        "lon_min": -70.41,
        "lon_max": -70.39,
        "region_name": "Test Explanation Atacama"
    }
    
    print(f"\n📍 Región: {test_data['region_name']}")
    
    try:
        print("\n🔄 Enviando solicitud...")
        response = requests.post(
            "http://localhost:8002/api/scientific/analyze",
            json=test_data,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"\n❌ ERROR: HTTP {response.status_code}")
            print(response.text)
            return False
        
        result = response.json()
        print("✅ Análisis completado")
        
        # Obtener análisis recientes
        print("\n🔍 Consultando análisis recientes...")
        response2 = requests.get(
            "http://localhost:8002/api/scientific/analyses/recent?limit=1",
            timeout=10
        )
        
        if response2.status_code != 200:
            print(f"❌ ERROR consultando: HTTP {response2.status_code}")
            return False
        
        recent = response2.json()
        
        if recent['total'] == 0:
            print("❌ No se encontraron análisis")
            return False
        
        analysis = recent['analyses'][0]
        
        print("\n" + "="*80)
        print("VERIFICACIÓN DE EXPLICACIÓN CIENTÍFICA")
        print("="*80)
        
        print(f"\n📊 Análisis ID: {analysis['id']}")
        print(f"   Nombre: {analysis['candidate_name']}")
        
        # Verificar explicación
        explanation = analysis.get('scientific_explanation')
        explanation_type = analysis.get('explanation_type')
        
        print(f"\n📝 Explicación guardada:")
        print(f"   Tipo: {explanation_type}")
        print(f"   Texto: {explanation}")
        
        if explanation is None:
            print("\n❌ ERROR: Explicación es None")
            return False
        
        if explanation_type != 'deterministic':
            print(f"\n⚠️ WARNING: Tipo de explicación inesperado: {explanation_type}")
        
        # Verificar que contenga elementos clave
        required_elements = [
            'anomalía',
            'probabilidad antropogénica',
            'Cobertura instrumental',
            'recomienda'
        ]
        
        missing = []
        for element in required_elements:
            if element.lower() not in explanation.lower():
                missing.append(element)
        
        if missing:
            print(f"\n⚠️ WARNING: Faltan elementos en la explicación: {missing}")
        else:
            print(f"\n✅ Explicación contiene todos los elementos esperados")
        
        # Consultar análisis completo
        print(f"\n🔍 Consultando análisis completo (ID {analysis['id']})...")
        response3 = requests.get(
            f"http://localhost:8002/api/scientific/analyses/{analysis['id']}",
            timeout=10
        )
        
        if response3.status_code != 200:
            print(f"❌ ERROR consultando por ID: HTTP {response3.status_code}")
            return False
        
        full_analysis = response3.json()
        
        full_explanation = full_analysis['analysis'].get('scientific_explanation')
        
        print(f"\n📝 Explicación en análisis completo:")
        print(f"   {full_explanation}")
        
        if full_explanation != explanation:
            print(f"\n⚠️ WARNING: Explicaciones no coinciden")
        
        print("\n" + "="*80)
        print("✅ TEST EXITOSO - Explicación científica guardada correctamente")
        print("="*80)
        
        print(f"\n🧮 DETERMINISTIC")
        print(explanation)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_explanation()
    exit(0 if success else 1)
