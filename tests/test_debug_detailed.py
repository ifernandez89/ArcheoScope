#!/usr/bin/env python3
import logging
logging.basicConfig(level=logging.INFO)

from backend.water.water_detector import WaterDetector
from backend.water.submarine_archaeology import SubmarineArchaeologyEngine

wd = WaterDetector()
se = SubmarineArchaeologyEngine()

# Test Jamaica
print("\n" + "="*80)
print("TESTING JAMAICA")
print("="*80)
ctx = wd.detect_water_context(18.5, -77.5)
print(f"Potential: {ctx.archaeological_potential}")
print(f"Shipping: {ctx.historical_shipping_routes}")
print(f"Wrecks: {ctx.known_wrecks_nearby}")

result = se.analyze_submarine_area(ctx, (18.4, 18.6, -77.6, -77.4))
print(f"\nRESULTS:")
print(f"  Volumetric anomalies: {result.get('volumetric_anomalies', 0)}")
print(f"  Wreck candidates: {len(result.get('wreck_candidates', []))}")

if result.get('wreck_candidates'):
    for i, candidate in enumerate(result['wreck_candidates'], 1):
        print(f"\n  Candidate {i}:")
        print(f"    Dimensions: {candidate['signature']['length_m']:.1f}m x {candidate['signature']['width_m']:.1f}m")
        print(f"    Confidence: {candidate['signature']['detection_confidence']:.2f}")
