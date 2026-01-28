#!/usr/bin/env python3
"""Probar los nuevos endpoints de consulta de análisis."""

import requests
import json

API_BASE = "http://localhost:8002"

def test_recent_analyses():
    """Probar GET /api/scientific/analyses/recent"""
    print("\n" + "="*60)
    print("🧪 TEST 1: Análisis Recientes")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE}/api/scientific/analyses/recent?limit=5", timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Total análisis: {data['total']}")
            
            if data['total'] > 0:
                print("\n📋 Últimos análisis:")
                for i, analysis in enumerate(data['analyses'][:3], 1):
                    print(f"\n  {i}. ID: {analysis['id']}")
                    print(f"     Región: {analysis['region']}")
                    print(f"     Probabilidad: {analysis['archaeological_probability']:.3f}")
                    print(f"     Anomaly Score: {analysis['anomaly_score']:.3f}")
                    print(f"     Acción: {analysis['recommended_action']}")
                    print(f"     Fecha: {analysis['created_at']}")
            else:
                print("⚠️ No hay análisis guardados aún")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_analysis_by_id(analysis_id: int):
    """Probar GET /api/scientific/analyses/{id}"""
    print("\n" + "="*60)
    print(f"🧪 TEST 2: Análisis por ID ({analysis_id})")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE}/api/scientific/analyses/{analysis_id}", timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n📊 ANÁLISIS:")
            analysis = data['analysis']
            print(f"  ID: {analysis['id']}")
            print(f"  Candidato: {analysis['candidate_name']}")
            print(f"  Región: {analysis['region']}")
            print(f"  Probabilidad: {analysis['archaeological_probability']:.3f}")
            print(f"  Anomaly Score: {analysis['anomaly_score']:.3f}")
            print(f"  Tipo: {analysis['result_type']}")
            print(f"  Acción: {analysis['recommended_action']}")
            print(f"  Ambiente: {analysis['environment_type']}")
            print(f"  Confianza: {analysis['confidence_level']:.3f}")
            
            print(f"\n🔬 MEDICIONES: {len(data['measurements'])}")
            for i, m in enumerate(data['measurements'][:5], 1):
                print(f"  {i}. {m['instrument_name']}: {m['value']:.3f} ({m['data_mode']})")
            
            return True
        elif response.status_code == 404:
            print(f"⚠️ Análisis {analysis_id} no encontrado")
            return False
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_analyses_by_region(region_name: str):
    """Probar GET /api/scientific/analyses/by-region/{name}"""
    print("\n" + "="*60)
    print(f"🧪 TEST 3: Análisis por Región ({region_name})")
    print("="*60)
    
    try:
        response = requests.get(
            f"{API_BASE}/api/scientific/analyses/by-region/{region_name}?limit=5", 
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Región: {data['region']}")
            print(f"✅ Total análisis: {data['total']}")
            
            if data['total'] > 0:
                print("\n📋 Análisis encontrados:")
                for i, analysis in enumerate(data['analyses'], 1):
                    print(f"\n  {i}. {analysis['candidate_name']}")
                    print(f"     Probabilidad: {analysis['archaeological_probability']:.3f}")
                    print(f"     Fecha: {analysis['created_at']}")
            else:
                print(f"⚠️ No hay análisis para la región '{region_name}'")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("\n🚀 PROBANDO ENDPOINTS DE CONSULTA DE ANÁLISIS")
    print("="*60)
    
    # Test 1: Análisis recientes
    success1 = test_recent_analyses()
    
    # Test 2: Análisis por ID (usar el primer ID encontrado)
    if success1:
        try:
            response = requests.get(f"{API_BASE}/api/scientific/analyses/recent?limit=1")
            if response.status_code == 200:
                data = response.json()
                if data['total'] > 0:
                    first_id = data['analyses'][0]['id']
                    test_analysis_by_id(first_id)
                else:
                    print("\n⚠️ No hay análisis para probar endpoint by-id")
        except:
            pass
    
    # Test 3: Análisis por región
    test_analyses_by_region("Groenlandia Test")
    
    print("\n" + "="*60)
    print("✅ TESTS COMPLETADOS")
    print("="*60)
