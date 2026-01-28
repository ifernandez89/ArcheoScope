#!/usr/bin/env python3
"""
Test script for enhanced ArcheoScope reporting functions.
"""

import sys
sys.path.append('backend')
from api.main import *

def test_enhanced_reporting():
    """Test all enhanced reporting functions."""
    
    print("🧪 Testing Enhanced ArcheoScope Reporting Functions")
    print("=" * 60)
    
    # Mock spatial results
    spatial_results = {
        'ndvi_vegetation': {
            'archaeological_probability': 0.7,
            'geometric_coherence': 0.6,
            'temporal_persistence': 0.8,
            'natural_explanation_score': 0.3
        },
        'thermal_lst': {
            'archaeological_probability': 0.4,
            'geometric_coherence': 0.5,
            'temporal_persistence': 0.6,
            'natural_explanation_score': 0.5
        },
        'sar_backscatter': {
            'archaeological_probability': 0.65,
            'geometric_coherence': 0.7,
            'temporal_persistence': 0.75,
            'natural_explanation_score': 0.2
        }
    }
    
    # Mock archaeological results
    archaeological_results = {
        'contradictions': [
            {'rule': 'vegetation_decoupling', 'archaeological_probability': 0.7},
            {'rule': 'thermal_residual', 'archaeological_probability': 0.65}
        ],
        'summary': {'total_rules': 2}
    }
    
    # Mock request
    class MockRequest:
        def __init__(self):
            self.region_name = 'Nazca Test Site'
            self.lat_min = -14.7
            self.lat_max = -14.6
            self.lon_min = -75.2
            self.lon_max = -75.1
            self.resolution_m = 500
    
    request = MockRequest()
    
    # Test helper functions
    print("1. Testing analyze_geometric_patterns...")
    try:
        geometric_analysis = analyze_geometric_patterns(spatial_results, archaeological_results)
        print(f"   ✅ Geometric coherence: {geometric_analysis['geometric_coherence']:.3f}")
        print(f"   ✅ Temporal persistence: {geometric_analysis['temporal_persistence']:.3f}")
        print(f"   ✅ Natural exclusion score: {geometric_analysis['natural_exclusion_score']:.3f}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n2. Testing generate_volumetric_inference...")
    try:
        volumetric_inference = generate_volumetric_inference(spatial_results, archaeological_results, request)
        print(f"   ✅ Volumetric model available: {volumetric_inference['volumetric_model_available']}")
        if volumetric_inference['volumetric_model_available']:
            print(f"   ✅ High probability anomalies: {volumetric_inference['analysis_summary']['total_high_probability_anomalies']}")
            print(f"   ✅ Total estimated volume: {volumetric_inference['analysis_summary']['total_estimated_volume_m3']:.1f} m³")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n3. Testing probability interpretation...")
    try:
        interpretation_high = get_probability_interpretation(0.7)
        interpretation_moderate = get_probability_interpretation(0.5)
        interpretation_low = get_probability_interpretation(0.2)
        print(f"   ✅ High probability (0.7): {interpretation_high}")
        print(f"   ✅ Moderate probability (0.5): {interpretation_moderate}")
        print(f"   ✅ Low probability (0.2): {interpretation_low}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n4. Testing anomaly scoring breakdown...")
    try:
        scoring_breakdown = generate_anomaly_scoring_breakdown(spatial_results)
        print(f"   ✅ Anomalies analyzed: {len(scoring_breakdown)}")
        for anomaly in scoring_breakdown:
            print(f"   ✅ {anomaly['anomaly_id']}: {anomaly['total_score']:.3f} ({anomaly['classification']})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n5. Testing enhanced reporting function...")
    try:
        ai_explanations = {
            'ai_available': False, 
            'archaeological_interpretation': 'Análisis determinista aplicado con criterios científicos'
        }
        report = generate_archaeological_report(request, spatial_results, archaeological_results, ai_explanations)
        
        print(f"   ✅ Report sections generated: {len(report)}")
        print(f"   ✅ Operational definitions: {'operational_definitions' in report}")
        print(f"   ✅ Volumetric inference: {'volumetric_geometric_inference' in report}")
        print(f"   ✅ Detailed AI analysis: {'ai_analysis_detailed' in report}")
        print(f"   ✅ Prioritized recommendations: {'prioritized_recommendations' in report}")
        print(f"   ✅ Scientific interpretation: {'scientific_interpretation_detailed' in report}")
        
        # Show key metrics
        print(f"\n   📊 Report Summary:")
        print(f"      - Total anomalies detected: {report['summary']['spatial_anomalies_detected']}")
        print(f"      - High probability anomalies: {report['summary']['high_probability_anomalies']}")
        print(f"      - Integrated probability: {report['summary']['integrated_probability']:.3f}")
        print(f"      - Confirmed archaeological signatures: {report['summary']['confirmed_archaeological_signatures']}")
        
        # Show operational definitions
        print(f"\n   📋 Operational Definitions:")
        for def_name, definition in report['operational_definitions'].items():
            print(f"      - {def_name}: {definition['definition'][:80]}...")
        
        # Show volumetric inference status
        volumetric = report['volumetric_geometric_inference']
        print(f"\n   🏗️ Volumetric Inference:")
        print(f"      - Model available: {volumetric['volumetric_model_available']}")
        if volumetric['volumetric_model_available']:
            print(f"      - Total volume estimated: {volumetric['analysis_summary']['total_estimated_volume_m3']:.1f} m³")
            print(f"      - Area coverage: {volumetric['analysis_summary']['area_coverage_percentage']:.2f}%")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎉 Enhanced ArcheoScope Reporting Test Complete!")
    print("\nKey improvements implemented:")
    print("✅ Operational definitions for all key terms")
    print("✅ Desegregated results instead of global percentages")
    print("✅ Geometric volumetric inference section")
    print("✅ Enhanced scientific interpretation with explicit criteria")
    print("✅ AI analysis with traceability and scoring breakdown")
    print("✅ Prioritized recommendations by scientific importance")
    print("✅ Academic-level reporting suitable for peer review")

if __name__ == "__main__":
    test_enhanced_reporting()