#!/usr/bin/env python3
"""
Test de los nuevos endpoints de sitios arqueológicos
"""

import requests
import json

API_URL = "http://localhost:8002"

def test_known_sites():
    """Probar endpoint de sitios conocidos"""
    print("="*80)
    print("🏛️  TEST: /archaeological-sites/known")
    print("="*80)
    
    response = requests.get(f"{API_URL}/archaeological-sites/known")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Total sitios: {data['total_sites']}")
        print(f"📅 Última actualización: {data['last_updated']}")
        print(f"🏛️  Sitios de referencia: {len(data['reference_sites'])}")
        print(f"🌍 Sitios de control: {len(data['control_sites'])}")
        
        print(f"\n📋 Sitios de referencia:")
        for site_id, site_data in data['reference_sites'].items():
            print(f"   - {site_data['name']} ({site_data['environment_type']})")
        
        print(f"\n🌍 Sitios de control:")
        for site_id, site_data in data['control_sites'].items():
            print(f"   - {site_data['name']} ({site_data['environment_type']})")
        
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def test_candidate_sites():
    """Probar endpoint de sitios candidatos"""
    print("\n" + "="*80)
    print("🔍 TEST: /archaeological-sites/candidates")
    print("="*80)
    
    response = requests.get(f"{API_URL}/archaeological-sites/candidates")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Total candidatos: {data['total_candidates']}")
        
        print(f"\n📋 Criterios de detección:")
        criteria = data['detection_criteria']
        print(f"   - Probabilidad mínima: {criteria['minimum_probability']}")
        print(f"   - Requiere convergencia: {criteria['requires_convergence']}")
        print(f"   - Excluye sitios conocidos: {criteria['excludes_known_sites']}")
        
        if data['total_candidates'] > 0:
            print(f"\n🎯 Top 3 candidatos:")
            for i, candidate in enumerate(data['candidates'][:3], 1):
                print(f"\n   {i}. {candidate['region_name']}")
                print(f"      Ambiente: {candidate['environment_type']}")
                print(f"      Probabilidad: {candidate['archaeological_probability']:.2%}")
                print(f"      Instrumentos convergentes: {candidate['instruments_converging']}")
        else:
            print(f"\n   ℹ️  No hay candidatos detectados aún")
            print(f"   💡 Ejecuta análisis con /analyze para generar candidatos")
        
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    print("\n🧪 TESTING NUEVOS ENDPOINTS DE ARCHEOSCOPE\n")
    
    test1 = test_known_sites()
    test2 = test_candidate_sites()
    
    print("\n" + "="*80)
    print("📊 RESUMEN")
    print("="*80)
    print(f"✅ /archaeological-sites/known: {'PASS' if test1 else 'FAIL'}")
    print(f"✅ /archaeological-sites/candidates: {'PASS' if test2 else 'FAIL'}")
    print("="*80)
