#!/usr/bin/env python3
"""
Test de debugging del clasificador de ambientes
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "backend"))

from environment_classifier import EnvironmentClassifier

def test_site(name, lat, lon, expected):
    """Test un sitio específico"""
    print(f"\n{'='*60}")
    print(f"🔍 Testing: {name}")
    print(f"   Coords: {lat:.4f}, {lon:.4f}")
    print(f"   Expected: {expected}")
    print(f"{'='*60}")
    
    classifier = EnvironmentClassifier()
    result = classifier.classify(lat, lon)
    
    print(f"✅ Result: {result.environment_type.value}")
    print(f"   Confidence: {result.confidence:.2f}")
    print(f"   Sensors: {', '.join(result.primary_sensors)}")
    
    if result.environment_type.value == expected:
        print(f"✅ PASS")
        return True
    else:
        print(f"❌ FAIL - Expected {expected}, got {result.environment_type.value}")
        return False

def main():
    """Test los 4 sitios problemáticos"""
    
    print("="*60)
    print("🧪 ENVIRONMENT CLASSIFIER DEBUG TEST")
    print("="*60)
    
    results = []
    
    # Test 1: Ötzi (glaciar alpino)
    results.append(test_site(
        "Ötzi the Iceman",
        46.7789, 10.8494,
        "glacier"
    ))
    
    # Test 2: Port Royal (mar poco profundo)
    results.append(test_site(
        "Port Royal",
        17.9364, -76.8408,
        "shallow_sea"
    ))
    
    # Test 3: Greenland (hielo polar)
    results.append(test_site(
        "Greenland Ice Sheet",
        72.5796, -38.4592,
        "polar_ice"
    ))
    
    # Test 4: Pacific Ocean (océano profundo)
    results.append(test_site(
        "Pacific Ocean",
        0.0000, -140.0000,
        "deep_ocean"
    ))
    
    print(f"\n{'='*60}")
    print(f"📊 RESULTS: {sum(results)}/4 passed")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
