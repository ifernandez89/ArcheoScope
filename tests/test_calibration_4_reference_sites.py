#!/usr/bin/env python3
"""
ArcheoScope Calibration Test - 4 Reference Sites
=================================================

Tests the 4 reference archaeological sites (one per critical environment):
1. DESERT: Giza Pyramids (Egypt)
2. FOREST: Angkor Wat (Cambodia)
3. ICE: Ötzi the Iceman (Alps)
4. WATER: Port Royal (Jamaica)

Verifies:
- Environment classification is correct
- Site recognition works
- Instrumental recommendations match environment
- Modern exclusion is working
- Archaeological detection is appropriate

Date: 2026-01-24
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, List

API_BASE_URL = "http://localhost:8002"

# 4 REFERENCE SITES - One per critical environment
REFERENCE_SITES = {
    "giza_pyramids": {
        "name": "Giza Pyramids Complex",
        "environment_expected": "desert",
        "coordinates": {"lat": 29.9792, "lon": 31.1342},
        "country": "Egypt",
        "should_detect": True,
        "expected_sensors": ["landsat_thermal", "sentinel2", "sar"],
        "notes": "DESERT reference - thermal/SAR detection"
    },
    "angkor_wat": {
        "name": "Angkor Wat Temple Complex",
        "environment_expected": "forest",
        "coordinates": {"lat": 13.4125, "lon": 103.8670},
        "country": "Cambodia",
        "should_detect": True,
        "expected_sensors": ["lidar", "sentinel2", "sar"],
        "notes": "FOREST reference - LiDAR penetration through canopy"
    },
    "otzi_iceman": {
        "name": "Ötzi the Iceman Discovery Site",
        "environment_expected": "glacier",
        "coordinates": {"lat": 46.7789, "lon": 10.8494},
        "country": "Italy/Austria",
        "should_detect": True,
        "expected_sensors": ["icesat2", "sentinel1_sar", "palsar"],
        "notes": "ICE reference - glacier archaeology, ICESat-2"
    },
    "port_royal": {
        "name": "Port Royal Submerged City",
        "environment_expected": "shallow_sea",
        "coordinates": {"lat": 17.9364, "lon": -76.8408},
        "country": "Jamaica",
        "should_detect": True,
        "expected_sensors": ["multibeam_sonar", "side_scan_sonar", "magnetometer"],
        "notes": "WATER reference - submarine archaeology"
    }
}

# CONTROL SITES - Should NOT detect archaeology
CONTROL_SITES = {
    "atacama_desert": {
        "name": "Atacama Desert Natural Control",
        "environment_expected": "desert",
        "coordinates": {"lat": -24.0000, "lon": -69.0000},
        "should_detect": False,
        "notes": "Natural desert - no archaeology"
    },
    "amazon_rainforest": {
        "name": "Amazon Rainforest Natural Control",
        "environment_expected": "forest",
        "coordinates": {"lat": -3.4653, "lon": -62.2159},
        "should_detect": False,
        "notes": "Pristine rainforest - no archaeology"
    },
    "greenland_ice": {
        "name": "Greenland Ice Sheet Natural Control",
        "environment_expected": "polar_ice",
        "coordinates": {"lat": 72.5796, "lon": -38.4592},
        "should_detect": False,
        "notes": "Pristine ice sheet - no archaeology"
    },
    "pacific_ocean": {
        "name": "Pacific Ocean Natural Control",
        "environment_expected": "deep_ocean",
        "coordinates": {"lat": 0.0000, "lon": -140.0000},
        "should_detect": False,
        "notes": "Deep ocean - no archaeology"
    }
}

def test_site(site_id: str, site_data: Dict[str, Any], is_control: bool = False) -> Dict[str, Any]:
    """Test a single archaeological or control site"""
    
    print(f"\n{'='*80}")
    print(f"🔬 TESTING: {site_data['name']}")
    print(f"   Environment: {site_data['environment_expected']}")
    print(f"   Type: {'CONTROL (no archaeology)' if is_control else 'REFERENCE (archaeological)'}")
    print(f"{'='*80}")
    
    # Prepare request
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
        # Call API
        print(f"📡 Calling /analyze endpoint...")
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json=request_data,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return {
                "site_id": site_id,
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }
        
        result = response.json()
        
        # Extract key information
        environment_detected = result.get("environment_classification", {}).get("environment_type", "unknown")
        environment_confidence = result.get("environment_classification", {}).get("confidence", 0.0)
        
        archaeological_result = result.get("archaeological_results", {}).get("result_type", "unknown")
        archaeological_prob = result.get("archaeological_results", {}).get("archaeological_probability", 0.0)
        
        site_recognized = False
        if "validation_metrics" in result:
            overlapping = result["validation_metrics"].get("overlapping_sites", [])
            site_recognized = len(overlapping) > 0
        
        primary_sensors = result.get("environment_classification", {}).get("primary_sensors", [])
        
        modern_score = result.get("archaeological_results", {}).get("modern_exclusion_score", 0.0)
        
        # Validation
        print(f"\n📊 RESULTS:")
        print(f"   Environment Detected: {environment_detected} (confidence: {environment_confidence:.2f})")
        print(f"   Archaeological Result: {archaeological_result} (prob: {archaeological_prob:.2f})")
        print(f"   Site Recognized: {'✅ YES' if site_recognized else '❌ NO'}")
        print(f"   Primary Sensors: {', '.join(primary_sensors)}")
        print(f"   Modern Exclusion Score: {modern_score:.2f}")
        
        # Check expectations
        checks = {
            "environment_correct": False,
            "sensors_correct": False,
            "detection_correct": False,
            "recognition_correct": False
        }
        
        # Check 1: Environment classification
        env_expected = site_data['environment_expected']
        if environment_detected == env_expected:
            print(f"   ✅ Environment classification CORRECT")
            checks["environment_correct"] = True
        else:
            print(f"   ⚠️  Environment classification: expected '{env_expected}', got '{environment_detected}'")
        
        # Check 2: Sensors (only for reference sites)
        if not is_control and "expected_sensors" in site_data:
            expected_sensors = site_data['expected_sensors']
            sensors_match = any(sensor in primary_sensors for sensor in expected_sensors)
            if sensors_match:
                print(f"   ✅ Sensors appropriate for environment")
                checks["sensors_correct"] = True
            else:
                print(f"   ⚠️  Expected sensors: {expected_sensors}, got: {primary_sensors}")
        else:
            checks["sensors_correct"] = True  # N/A for controls
        
        # Check 3: Detection (should detect archaeology or not)
        should_detect = site_data.get('should_detect', False)
        is_detected = archaeological_prob > 0.5
        
        if should_detect == is_detected:
            print(f"   ✅ Detection {'CORRECT' if should_detect else 'correctly NEGATIVE'}")
            checks["detection_correct"] = True
        else:
            if should_detect:
                print(f"   ❌ FALSE NEGATIVE: Should detect archaeology but didn't")
            else:
                print(f"   ❌ FALSE POSITIVE: Should NOT detect archaeology but did")
        
        # Check 4: Site recognition (only for reference sites)
        if not is_control:
            if site_recognized:
                print(f"   ✅ Site RECOGNIZED in database")
                checks["recognition_correct"] = True
            else:
                print(f"   ⚠️  Site NOT recognized (may need database update)")
        else:
            checks["recognition_correct"] = True  # N/A for controls
        
        # Overall pass/fail
        all_passed = all(checks.values())
        print(f"\n{'✅ PASS' if all_passed else '⚠️  PARTIAL PASS'}")
        
        return {
            "site_id": site_id,
            "site_name": site_data['name'],
            "status": "pass" if all_passed else "partial",
            "environment_detected": environment_detected,
            "environment_confidence": environment_confidence,
            "archaeological_probability": archaeological_prob,
            "site_recognized": site_recognized,
            "checks": checks,
            "full_result": result
        }
        
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT: Request took too long")
        return {
            "site_id": site_id,
            "status": "timeout",
            "error": "Request timeout"
        }
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return {
            "site_id": site_id,
            "status": "error",
            "error": str(e)
        }

def main():
    """Run calibration test on all 4 reference sites + 4 control sites"""
    
    print("="*80)
    print("🔬 ARCHEOSCOPE CALIBRATION TEST - 4 REFERENCE SITES")
    print("="*80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API: {API_BASE_URL}")
    print()
    print("Testing 4 reference archaeological sites (one per environment):")
    print("  1. DESERT: Giza Pyramids (Egypt)")
    print("  2. FOREST: Angkor Wat (Cambodia)")
    print("  3. ICE: Ötzi the Iceman (Alps)")
    print("  4. WATER: Port Royal (Jamaica)")
    print()
    print("Plus 4 control sites (should NOT detect archaeology)")
    print("="*80)
    
    # Check backend is running
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
        print("✅ Backend is running")
    except Exception as e:
        print(f"❌ ERROR: Backend is not running! ({e})")
        print("   Please start backend: python run_archeoscope.py")
        return
    
    # Test reference sites
    print("\n" + "="*80)
    print("PART 1: REFERENCE ARCHAEOLOGICAL SITES")
    print("="*80)
    
    reference_results = []
    for site_id, site_data in REFERENCE_SITES.items():
        result = test_site(site_id, site_data, is_control=False)
        reference_results.append(result)
    
    # Test control sites
    print("\n" + "="*80)
    print("PART 2: CONTROL SITES (Natural - No Archaeology)")
    print("="*80)
    
    control_results = []
    for site_id, site_data in CONTROL_SITES.items():
        result = test_site(site_id, site_data, is_control=True)
        control_results.append(result)
    
    # Summary
    print("\n" + "="*80)
    print("📊 CALIBRATION SUMMARY")
    print("="*80)
    
    # Reference sites summary
    print("\n🏛️  REFERENCE SITES (Archaeological):")
    ref_passed = sum(1 for r in reference_results if r.get("status") == "pass")
    ref_partial = sum(1 for r in reference_results if r.get("status") == "partial")
    ref_failed = len(reference_results) - ref_passed - ref_partial
    
    print(f"   ✅ Passed: {ref_passed}/4")
    print(f"   ⚠️  Partial: {ref_partial}/4")
    print(f"   ❌ Failed: {ref_failed}/4")
    
    for result in reference_results:
        status_icon = "✅" if result.get("status") == "pass" else "⚠️" if result.get("status") == "partial" else "❌"
        print(f"   {status_icon} {result.get('site_name', result['site_id'])}")
    
    # Control sites summary
    print("\n🌍 CONTROL SITES (Natural - No Archaeology):")
    ctrl_passed = sum(1 for r in control_results if r.get("status") == "pass")
    ctrl_partial = sum(1 for r in control_results if r.get("status") == "partial")
    ctrl_failed = len(control_results) - ctrl_passed - ctrl_partial
    
    print(f"   ✅ Passed: {ctrl_passed}/4")
    print(f"   ⚠️  Partial: {ctrl_partial}/4")
    print(f"   ❌ Failed: {ctrl_failed}/4")
    
    for result in control_results:
        status_icon = "✅" if result.get("status") == "pass" else "⚠️" if result.get("status") == "partial" else "❌"
        print(f"   {status_icon} {result.get('site_name', result['site_id'])}")
    
    # Overall calibration status
    total_passed = ref_passed + ctrl_passed
    total_tests = len(reference_results) + len(control_results)
    
    print(f"\n🎯 OVERALL CALIBRATION: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("✅ EXCELLENT: All calibration tests passed!")
    elif total_passed >= total_tests * 0.75:
        print("✅ GOOD: Most calibration tests passed")
    elif total_passed >= total_tests * 0.5:
        print("⚠️  FAIR: Some calibration issues detected")
    else:
        print("❌ POOR: Significant calibration issues - needs attention")
    
    # Save results
    output_file = f"calibration_4_sites_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_data = {
        "test_date": datetime.now().isoformat(),
        "api_url": API_BASE_URL,
        "reference_sites": reference_results,
        "control_sites": control_results,
        "summary": {
            "reference_passed": ref_passed,
            "reference_partial": ref_partial,
            "reference_failed": ref_failed,
            "control_passed": ctrl_passed,
            "control_partial": ctrl_partial,
            "control_failed": ctrl_failed,
            "total_passed": total_passed,
            "total_tests": total_tests,
            "pass_rate": total_passed / total_tests if total_tests > 0 else 0
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    print("="*80)

if __name__ == "__main__":
    main()
