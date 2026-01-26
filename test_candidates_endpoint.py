#!/usr/bin/env python3
"""
Test del endpoint de candidatas
"""

import requests

print("Testing candidates endpoint...")

try:
    response = requests.get("http://localhost:8002/archaeological-sites/candidates/priority?limit=10")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nOK - {len(data)} candidatas obtenidas")
        
        for i, candidate in enumerate(data, 1):
            print(f"\n{i}. {candidate.get('candidate_id', 'N/A')}")
            print(f"   Score: {candidate.get('multi_instrumental_score', 0):.3f}")
            print(f"   Lat/Lon: {candidate.get('center_lat', 0):.4f}, {candidate.get('center_lon', 0):.4f}")
            print(f"   Convergencia: {candidate.get('convergence_count', 0)}")
    else:
        print(f"ERROR - Status {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"ERROR: {e}")
    print("\nAsegurate de que el backend este corriendo:")
    print("  python run_archeoscope.py")
