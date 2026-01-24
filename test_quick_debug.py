#!/usr/bin/env python3
from backend.water.water_detector import WaterDetector
from backend.water.submarine_archaeology import SubmarineArchaeologyEngine

wd = WaterDetector()
se = SubmarineArchaeologyEngine()

# Test Jamaica
ctx = wd.detect_water_context(18.5, -77.5)
print(f"Jamaica:")
print(f"  Potential: {ctx.archaeological_potential}")
print(f"  Shipping: {ctx.historical_shipping_routes}")
print(f"  Wrecks: {ctx.known_wrecks_nearby}")

result = se.analyze_submarine_area(ctx, (18.4, 18.6, -77.6, -77.4))
print(f"  Candidates: {len(result.get('wreck_candidates', []))}")
print(f"  Volumetric anomalies: {result.get('volumetric_anomalies', 0)}")
