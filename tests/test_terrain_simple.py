#!/usr/bin/env python3
"""
Simple Terrain Detection Test
Tests environment classification for the 4 reference sites
"""

import requests
import json

API_BASE_URL = "http://localhost:8002"

# 4 REFERENCE SITES - One per critical environment
REFERENCE_SITES = {
    "giza_pyramids": {
        "name": "Giza Pyramids Complex",
        "environment_expected": "desert",
        "coordinates": {"lat": 29.9792, "lon": 31.1342},
        "country": "Egypt"
    },
    "angkor_wat": {
        "name": "Angkor Wat Temple Complex",
        "environment_expected": "forest",
        "coordinates": {"lat": 13.4125, "lon": 103.8670},
        "country": "Cambodia"
    },
    "otzi_iceman": {
        "name": "Otzi the Iceman Discovery Site",
        "environment_expected": "glacier",
        "coordinates": {"lat": 46.7789, "lon": 10.8494},
        "country": "Italy/Austria"
    },
    "port_royal": {
        "name": "Port Royal Submerged City",
        "environment_expected": "shallow_sea",
        "coordinates": {"lat": 17.9364, "lon": -76.8408},
        "country": "Jamaica"
    }
}

def test_terrain_classification(site_id, site_data):
    """Test terrain classification for a single site"""
    
    print(f"\n{'='*60}")
    print(f"Testing: {site_data['name']}")
    print(f"Expected Environment: {site_data['environment_expected']}")
    print(f"Coordinates: {site_data['coordinates']}")
    
    lat = site_data['coordinates']['lat']
    lon = site_data['coordinates']['lon']
    
    request_data = {
        "lat_min": lat - 0.01,
        "lat_max": lat + 0.01,
        "lon_min": lon - 0.01,
        "lon_max": lon + 0.01,
        "region_name": site_data['name'],
        "resolution_m": 1000
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json=request_data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"ERROR: HTTP {response.status_code}")
            return {
                "site_id": site_id,
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }
        
        result = response.json()
        
        # Extract terrain classification
        env_detected = result.get("environment_classification", {}).get("environment_type", "unknown")
        env_confidence = result.get("environment_classification", {}).get("confidence", 0.0)
        primary_sensors = result.get("environment_classification", {}).get("primary_sensors", [])
        
        # Check if site is recognized
        site_recognized = False
        if "validation_metrics" in result:
            overlapping = result["validation_metrics"].get("overlapping_sites", [])
            site_recognized = len(overlapping) > 0
        
        # Archaeological detection
        arch_result = result.get("archaeological_results", {}).get("result_type", "unknown")
        arch_prob = result.get("archaeological_results", {}).get("archaeological_probability", 0.0)
        
        print(f"Environment Detected: {env_detected} (confidence: {env_confidence:.2f})")
        print(f"Primary Sensors: {primary_sensors}")
        print(f"Site Recognized: {'YES' if site_recognized else 'NO'}")
        print(f"Archaeological Result: {arch_result} (prob: {arch_prob:.2f})")
        
        # Check correctness
        env_correct = env_detected == site_data['environment_expected']
        print(f"Environment Classification: {'CORRECT' if env_correct else 'INCORRECT'}")
        
        return {
            "site_id": site_id,
            "site_name": site_data['name'],
            "status": "success",
            "environment_detected": env_detected,
            "environment_expected": site_data['environment_expected'],
            "environment_correct": env_correct,
            "environment_confidence": env_confidence,
            "primary_sensors": primary_sensors,
            "site_recognized": site_recognized,
            "archaeological_probability": arch_prob,
            "archaeological_result": arch_result
        }
        
    except Exception as e:
        print(f"ERROR: {e}")
        return {
            "site_id": site_id,
            "status": "error",
            "error": str(e)
        }

def main():
    """Run terrain classification test"""
    
    print("="*60)
    print("TERRAIN DETECTION CALIBRATION TEST")
    print("="*60)
    
    # Check backend
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
        print("Backend is running")
    except Exception as e:
        print(f"ERROR: Backend not running! ({e})")
        return
    
    results = []
    
    for site_id, site_data in REFERENCE_SITES.items():
        result = test_terrain_classification(site_id, site_data)
        results.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    correct_classifications = 0
    recognized_sites = 0
    archaeological_detections = 0
    
    for result in results:
        if result.get("environment_correct"):
            correct_classifications += 1
        if result.get("site_recognized"):
            recognized_sites += 1
        if result.get("archaeological_probability", 0) > 0.5:
            archaeological_detections += 1
        
        status = "PASS" if result.get("environment_correct") else "FAIL"
        print(f"{status}: {result.get('site_name', result['site_id'])}")
        print(f"    Environment: {result.get('environment_detected')} (expected: {result.get('environment_expected')})")
        print(f"    Recognized: {result.get('site_recognized')}")
        print(f"    Arch. Prob: {result.get('archaeological_probability', 0):.2f}")
    
    print(f"\nTerrain Classification Accuracy: {correct_classifications}/4 ({correct_classifications/4*100:.0f}%)")
    print(f"Site Recognition Rate: {recognized_sites}/4 ({recognized_sites/4*100:.0f}%)")
    print(f"Archaeological Detection Rate: {archaeological_detections}/4 ({archaeological_detections/4*100:.0f}%)")
    
    # Save results
    output_file = "terrain_test_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()