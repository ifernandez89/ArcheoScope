#!/usr/bin/env python3
"""
Test the archaeological sites endpoint
"""

import requests
import json

def test_endpoint():
    """Test the /archaeological-sites/known endpoint"""
    
    url = "http://localhost:8002/archaeological-sites/known"
    
    print(f"🔍 Testing endpoint: {url}")
    print()
    
    try:
        response = requests.get(url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ Endpoint funcionando correctamente!")
            print(f"\nMetadata:")
            print(f"  - Total sitios: {data['metadata']['total_sites']:,}")
            print(f"  - Sitios de referencia: {data['metadata']['reference_sites']}")
            print(f"  - Última actualización: {data['metadata']['last_updated']}")
            print(f"  - Base de datos: {data['metadata']['database']}")
            
            print(f"\nTop 10 países con más sitios:")
            for country in data['top_countries']:
                print(f"  - {country['country']}: {country['count']:,} sitios")
            
            print(f"\nMuestra de sitios de referencia: {len(data['reference_sites_sample'])}")
            
            print("\n✅ TEST EXITOSO - Endpoint accediendo a PostgreSQL correctamente")
            return True
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = test_endpoint()
    sys.exit(0 if success else 1)
