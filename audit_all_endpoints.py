#!/usr/bin/env python3
"""
AUDITORÍA COMPLETA DE ENDPOINTS - ArcheoScope
Probar todos los endpoints y marcar cuáles funcionan y cuáles no.
"""

import requests
import json
from typing import Dict, List

API_BASE = "http://localhost:8002"

# Lista completa de endpoints a auditar
ENDPOINTS = {
    "GET": [
        ("/", "Root endpoint"),
        ("/status", "System status"),
        ("/status/detailed", "Detailed system status"),
        ("/test-ai", "AI assistant test"),
        ("/known-sites", "Known archaeological sites"),
        ("/data-sources", "Data sources info"),
        ("/validate-region?lat_min=25&lat_max=26&lon_min=31&lon_max=32", "Validate region"),
        ("/comparison-data", "Comparison data"),
        ("/lidar-benchmark", "LIDAR benchmark"),
        ("/instruments/status", "Instruments status"),
        ("/instruments/archaeological-value", "Archaeological value matrix"),
        ("/archaeological-sites/known", "All known sites"),
        ("/archaeological-sites/candidates", "Candidate sites"),
        ("/archaeological-sites/all?limit=10", "All sites paginated"),
        ("/archaeological-sites/by-environment/desert?limit=10", "Sites by environment"),
        ("/archaeological-sites/environments/stats", "Environment statistics"),
        ("/archaeological-sites/recommended-zones-geojson?lat_min=25&lat_max=26&lon_min=31&lon_max=32", "Recommended zones GeoJSON"),
        ("/archaeological-sites/enriched-candidates?lat_min=25&lat_max=26&lon_min=31&lon_max=32", "Enriched candidates"),
        ("/archaeological-sites/candidates/priority?limit=10", "Priority candidates"),
        ("/archaeological-sites/candidates/statistics", "Candidates statistics"),
        ("/archaeological-sites/candidates/search?lat=25.5&lon=31.5&radius_km=50", "Search candidates"),
        ("/volumetric/sites/catalog", "Volumetric sites catalog"),
        ("/api/scientific/analyses/recent?limit=5", "Recent analyses (NEW)"),
        ("/api/scientific/analyses/by-region/Test?limit=5", "Analyses by region (NEW)"),
    ],
    "POST": [
        ("/falsification-protocol", "Falsification protocol", {}),
        ("/archaeological-sites/cultural-prior-map", "Cultural prior map", {
            "lat_min": 25.0, "lat_max": 26.0, "lon_min": 31.0, "lon_max": 32.0
        }),
        ("/archaeological-sites/recommended-zones", "Recommended zones", {
            "lat_min": 25.0, "lat_max": 26.0, "lon_min": 31.0, "lon_max": 32.0
        }),
        ("/academic/validation/blind-test", "Blind test", {}),
        ("/test-analyze", "Test analyze", {
            "lat_min": 25.0, "lat_max": 26.0, "lon_min": 31.0, "lon_max": 32.0, "region_name": "Test"
        }),
    ]
}

def test_get_endpoint(path: str, description: str) -> Dict:
    """Probar un endpoint GET."""
    try:
        response = requests.get(f"{API_BASE}{path}", timeout=10)
        
        return {
            "path": path,
            "description": description,
            "status": response.status_code,
            "success": response.status_code == 200,
            "error": None if response.status_code == 200 else response.text[:200]
        }
    except Exception as e:
        return {
            "path": path,
            "description": description,
            "status": 0,
            "success": False,
            "error": str(e)[:200]
        }

def test_post_endpoint(path: str, description: str, data: Dict) -> Dict:
    """Probar un endpoint POST."""
    try:
        response = requests.post(f"{API_BASE}{path}", json=data, timeout=30)
        
        return {
            "path": path,
            "description": description,
            "status": response.status_code,
            "success": response.status_code == 200,
            "error": None if response.status_code == 200 else response.text[:200]
        }
    except Exception as e:
        return {
            "path": path,
            "description": description,
            "status": 0,
            "success": False,
            "error": str(e)[:200]
        }

def main():
    """Ejecutar auditoría completa."""
    print("\n" + "="*80)
    print("🔍 AUDITORÍA COMPLETA DE ENDPOINTS - ArcheoScope")
    print("="*80)
    
    results = {
        "GET": [],
        "POST": []
    }
    
    # Probar endpoints GET
    print("\n📡 PROBANDO ENDPOINTS GET...")
    print("-"*80)
    for path, description in ENDPOINTS["GET"]:
        result = test_get_endpoint(path, description)
        results["GET"].append(result)
        
        status_icon = "✅" if result["success"] else "❌"
        print(f"{status_icon} [{result['status']:3d}] {path[:60]:<60} {description[:30]}")
        if not result["success"] and result["error"]:
            print(f"     Error: {result['error'][:100]}")
    
    # Probar endpoints POST
    print("\n📡 PROBANDO ENDPOINTS POST...")
    print("-"*80)
    for path, description, data in ENDPOINTS["POST"]:
        result = test_post_endpoint(path, description, data)
        results["POST"].append(result)
        
        status_icon = "✅" if result["success"] else "❌"
        print(f"{status_icon} [{result['status']:3d}] {path[:60]:<60} {description[:30]}")
        if not result["success"] and result["error"]:
            print(f"     Error: {result['error'][:100]}")
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMEN DE AUDITORÍA")
    print("="*80)
    
    total_get = len(results["GET"])
    success_get = sum(1 for r in results["GET"] if r["success"])
    total_post = len(results["POST"])
    success_post = sum(1 for r in results["POST"] if r["success"])
    
    print(f"\nGET Endpoints:")
    print(f"  Total: {total_get}")
    print(f"  ✅ Funcionando: {success_get}")
    print(f"  ❌ Rotos: {total_get - success_get}")
    print(f"  Tasa de éxito: {success_get/total_get*100:.1f}%")
    
    print(f"\nPOST Endpoints:")
    print(f"  Total: {total_post}")
    print(f"  ✅ Funcionando: {success_post}")
    print(f"  ❌ Rotos: {total_post - success_post}")
    print(f"  Tasa de éxito: {success_post/total_post*100:.1f}%")
    
    print(f"\nTOTAL:")
    total_all = total_get + total_post
    success_all = success_get + success_post
    print(f"  Total endpoints: {total_all}")
    print(f"  ✅ Funcionando: {success_all}")
    print(f"  ❌ Rotos: {total_all - success_all}")
    print(f"  Tasa de éxito: {success_all/total_all*100:.1f}%")
    
    # Listar endpoints rotos
    broken = []
    for r in results["GET"] + results["POST"]:
        if not r["success"]:
            broken.append(r)
    
    if broken:
        print("\n" + "="*80)
        print("❌ ENDPOINTS ROTOS QUE REQUIEREN ATENCIÓN:")
        print("="*80)
        for r in broken:
            print(f"\n  {r['path']}")
            print(f"    Descripción: {r['description']}")
            print(f"    Status: {r['status']}")
            if r['error']:
                print(f"    Error: {r['error'][:150]}")
    
    print("\n" + "="*80)
    print("✅ AUDITORÍA COMPLETADA")
    print("="*80)
    
    # Guardar resultados
    with open('endpoint_audit_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\n📄 Resultados guardados en: endpoint_audit_results.json")

if __name__ == "__main__":
    main()
