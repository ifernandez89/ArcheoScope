#!/usr/bin/env python3
"""
Control Sites Test - Should NOT detect archaeology
"""

import requests
import json

API_BASE_URL = "http://localhost:8002"

# CONTROL SITES - Should NOT detect archaeology
CONTROL_SITES = {
    "atacama_desert": {
        "name": "Atacama Desert Natural Control",
        "environment_expected": "desert",
        "coordinates": {"lat": -24.0000, "lon": -69.0000},
        "should_detect": False
    },
    "amazon_rainforest": {
        "name": "Amazon Rainforest Natural Control",
        "environment_expected": "forest",
        "coordinates": {"lat": -3.4653, "lon": -62.2159},
        "should_detect": False
    },
    "greenland_ice": {
        "name": "Greenland Ice Sheet Natural Control",
        "environment_expected": "polar_ice",
        "coordinates": {"lat": 72.5796, "lon": -38.4592},
        "should_detect": False
    },
    "pacific_ocean": {
        "name": "Pacific Ocean Natural Control",
        "environment_expected": "deep_ocean",
        "coordinates": {"lat": 0.0000, "lon": -140.0000},
        "should_detect": False
    }
}

def test_control_site(site_id, site_data):
    """Test control site that should NOT detect archaeology"""
    
    print(f"\n{'='*60}")
    print(f"Testing Control: {site_data['name']}")
    print(f"Expected Environment: {site_data['environment_expected']}")
    print(f"Should Detect Archaeology: NO")
    
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
            return {"site_id": site_id, "status": "error"}
        
        result = response.json()
        
        env_detected = result.get("environment_classification", {}).get("environment_type", "unknown")
        env_confidence = result.get("environment_classification", {}).get("confidence", 0.0)
        arch_result = result.get("archaeological_results", {}).get("result_type", "unknown")
        arch_prob = result.get("archaeological_results", {}).get("archaeological_probability", 0.0)
        
        print(f"Environment: {env_detected} (confidence: {env_confidence:.2f})")
        print(f"Archaeological: {arch_result} (prob: {arch_prob:.2f})")
        
        # Check if correctly NOT detecting archaeology
        correct_negative = arch_prob < 0.5
        print(f"Control Test: {'PASS' if correct_negative else 'FAIL - FALSE POSITIVE'}")
        
        return {
            "site_id": site_id,
            "site_name": site_data['name'],
            "environment_detected": env_detected,
            "environment_expected": site_data['environment_expected'],
            "archaeological_probability": arch_prob,
            "correct_negative": correct_negative
        }
        
    except Exception as e:
        print(f"ERROR: {e}")
        return {"site_id": site_id, "status": "error"}

def main():
    """Test control sites"""
    
    print("="*60)
    print("CONTROL SITES TEST - Should NOT detect archaeology")
    print("="*60)
    
    results = []
    for site_id, site_data in CONTROL_SITES.items():
        result = test_control_site(site_id, site_data)
        results.append(result)
    
    print("\n" + "="*60)
    print("CONTROL SITES SUMMARY")
    print("="*60)
    
    correct_negatives = 0
    for result in results:
        if result.get("correct_negative"):
            correct_negatives += 1
        
        status = "PASS" if result.get("correct_negative") else "FAIL"
        print(f"{status}: {result.get('site_name', result['site_id'])}")
        print(f"    Environment: {result.get('environment_detected')}")
        print(f"    Arch. Prob: {result.get('archaeological_probability', 0):.2f}")
    
    print(f"\nCorrect Negatives: {correct_negatives}/4 ({correct_negatives/4*100:.0f}%)")
    
    if correct_negatives == 4:
        print("EXCELLENT: No false positives detected")
    elif correct_negatives >= 3:
        print("GOOD: Low false positive rate")
    else:
        print("ISSUE: High false positive rate detected")

if __name__ == "__main__":
    main()