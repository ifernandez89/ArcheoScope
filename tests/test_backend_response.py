#!/usr/bin/env python3
"""
Test rápido para verificar la estructura de respuesta del backend
"""

import requests
import json

def test_backend_structure():
    """Test de estructura de respuesta del backend"""
    print("🔍 ===== TEST DE ESTRUCTURA DE RESPUESTA =====")
    
    coords = {
        "lat_min": 25.0,
        "lat_max": 25.1,
        "lon_min": -70.1,
        "lon_max": -70.0
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze",
            json=coords,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend responde correctamente")
            print(f"📊 Claves principales: {list(data.keys())}")
            
            # Verificar anomaly_map
            if 'anomaly_map' in data:
                anomaly_map = data['anomaly_map']
                print(f"🗺️ anomaly_map presente: {type(anomaly_map)}")
                if isinstance(anomaly_map, dict):
                    print(f"   Claves en anomaly_map: {list(anomaly_map.keys())}")
                    if 'anomaly_mask' in anomaly_map:
                        mask = anomaly_map['anomaly_mask']
                        print(f"   anomaly_mask tipo: {type(mask)}")
                        if isinstance(mask, list):
                            print(f"   anomaly_mask dimensiones: {len(mask)} x {len(mask[0]) if mask and isinstance(mask[0], list) else 'N/A'}")
                        else:
                            print(f"   ⚠️ anomaly_mask no es lista: {mask}")
                    else:
                        print("   ❌ anomaly_mask no encontrado en anomaly_map")
                else:
                    print(f"   ❌ anomaly_map no es dict: {anomaly_map}")
            else:
                print("❌ anomaly_map no encontrado en respuesta")
                print("   Esto explica el error en frontend")
            
            # Verificar region_info
            if 'region_info' in data:
                region_info = data['region_info']
                print(f"📍 region_info presente: {type(region_info)}")
                if isinstance(region_info, dict) and 'coordinates' in region_info:
                    coords_info = region_info['coordinates']
                    print(f"   coordinates: {coords_info}")
                else:
                    print("   ⚠️ coordinates no encontrado en region_info")
            else:
                print("❌ region_info no encontrado")
            
            return True
        else:
            print(f"❌ Error en backend: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

if __name__ == "__main__":
    test_backend_structure()