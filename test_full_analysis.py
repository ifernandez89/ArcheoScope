
import requests
import json
import os

BASE_URL = "http://localhost:8003"

def test_full_analysis():
    print("Testing full analysis (Small Area)...")
    # Angkor Wat approx center
    payload = {
        "lat_min": 13.4120,
        "lat_max": 13.4130,
        "lon_min": 103.8660,
        "lon_max": 103.8670,
        "region_name": "Angkor Wat Verification"
    }
    response = requests.post(f"{BASE_URL}/api/scientific/analyze", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Analysis Status: {data.get('status')}")
        
        # Check for anomaly map
        anomaly_map = data.get('anomaly_map', {})
        print(f"Anomaly Map Path: {anomaly_map.get('path')}")
        
        if anomaly_map.get('anomaly_map_base64'):
            print("✅ Anomaly Map Base64 data present")
        else:
            print("❌ Anomaly Map Base64 data missing")
            
        # Check for archaeological results
        arch_results = data.get('archaeological_results', {})
        print(f"Archaeological Classification: {arch_results.get('classification')}")
        print(f"Anomaly Score: {arch_results.get('anomaly_score')}")
        
        # Check for TAS score (Scientific Output)
        sci_output = data.get('scientific_output', {})
        print(f"Instrumental Anomaly: {sci_output.get('instrumental_anomaly_probability')}")
        
    else:
        print(f"Response: {response.text}")

if __name__ == "__main__":
    test_full_analysis()
