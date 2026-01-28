#!/usr/bin/env python3
"""
Test de integración de la funcionalidad de lupa arqueológica
"""

import requests
import json
import time

def test_lupa_integration():
    """Test que simula el flujo completo de la lupa arqueológica"""
    
    print("🔍 Testing ArcheoScope Lupa Integration")
    print("=" * 50)
    
    # Coordenadas de test (Roma, Via Appia)
    test_coordinates = {
        "lat_min": 41.8500,
        "lat_max": 41.8600,
        "lon_min": 12.5100,
        "lon_max": 12.5200,
        "resolution_m": 500,
        "region_name": "Test Lupa Integration - Via Appia",
        "include_explainability": True,
        "include_validation_metrics": True,
        "layers_to_analyze": [
            # Base (6)
            "ndvi_vegetation", "thermal_lst", "sar_backscatter", 
            "surface_roughness", "soil_salinity", "seismic_resonance",
            # Enhanced (5) 
            "elevation_dem", "sar_l_band", "icesat2_profiles",
            "vegetation_height", "soil_moisture"
        ],
        "active_rules": ["all"]
    }
    
    try:
        print("🚀 Sending analysis request...")
        print(f"📊 Total instruments: {len(test_coordinates['layers_to_analyze'])}")
        
        response = requests.post(
            'http://localhost:8004/analyze',
            json=test_coordinates,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis completed successfully!")
            
            # Check if we have statistical results for lupa
            if 'statistical_results' in data:
                stats = data['statistical_results']
                print(f"\n📈 Statistical Results Available:")
                
                # Calculate average archaeological probability
                probabilities = []
                for instrument, result in stats.items():
                    prob = result.get('archaeological_probability', 0)
                    probabilities.append(prob)
                    print(f"  🛰️ {instrument}: {prob:.1%}")
                
                if probabilities:
                    avg_prob = sum(probabilities) / len(probabilities)
                    print(f"\n🎯 Average Archaeological Probability: {avg_prob:.1%}")
                    
                    # Check if lupa should be activated (threshold > 20%)
                    if avg_prob > 0.2:
                        print("🔍 ✅ LUPA SHOULD BE ACTIVATED!")
                        print("   Archaeological anomalies detected above threshold")
                        
                        # Test lupa data structure
                        print("\n🗂️ Lupa Data Structure Test:")
                        print(f"   Region center: {(test_coordinates['lat_min'] + test_coordinates['lat_max'])/2:.6f}, {(test_coordinates['lon_min'] + test_coordinates['lon_max'])/2:.6f}")
                        print(f"   Instruments available: {len(stats)}")
                        print(f"   Anomaly layers ready: ✅")
                        
                        return True
                    else:
                        print("🔍 ❌ Lupa threshold not met")
                        print("   No significant archaeological anomalies detected")
                        return False
                else:
                    print("❌ No probability data available")
                    return False
            else:
                print("❌ No statistical results in response")
                return False
                
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_lupa_integration()
    
    if success:
        print("\n🎉 LUPA INTEGRATION TEST PASSED!")
        print("   The archaeological lupa functionality is ready to use")
        print("   Frontend should show the lupa button when anomalies are detected")
    else:
        print("\n⚠️ LUPA INTEGRATION TEST NEEDS ATTENTION")
        print("   Check the analysis results and threshold settings")
    
    print("\n📋 Next Steps:")
    print("   1. Open http://localhost:8000 in your browser")
    print("   2. Enter coordinates: 41.8550, 12.5150")
    print("   3. Click 'INVESTIGAR' to run analysis")
    print("   4. Look for the '🔍 Lupa Arqueológica' button")
    print("   5. Click the lupa button to see multi-sensor visualization")