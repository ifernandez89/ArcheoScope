#!/usr/bin/env python3
"""
Calibration Test Suite for ArcheoScope
=====================================

Comprehensive testing of the integrated AI system against known archaeological sites.
Provides surgical calibration of instruments and IA integration.

Test Sites:
1. Giza Pyramids (Egypt) - Desert monumental
2. Chichen Itza (Mexico) - Tropical dry forest
3. Machu Picchu (Peru) - Montane forest
4. Tikal (Guatemala) - Rainforest
5. Petra (Jordan) - Desert mountain
6. Stonehenge (UK) - Agricultural plains
7. Mohenjo-Daro (Pakistan) - Arid agricultural
8. Easter Island (Chile) - Volcanic island
9. Pompeii (Italy) - Mediterranean
10. Port Royal (Jamaica) - Submerged city
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class CalibrationTestSuite:
    """Surgical calibration test suite for ArcheoScope"""
    
    def __init__(self):
        self.api_base = "http://localhost:8002"
        self.results = []
        
        # 10 CALIBRATION SITES - Global distribution
        self.calibration_sites = [
            {
                "name": "Giza Pyramids Complex",
                "coordinates": {"lat_min": 29.975, "lat_max": 29.985, "lon_min": 31.130, "lon_max": 31.140},
                "expected_environment": "desert",
                "expected_probability": 0.9,  # Very high - massive structures
                "site_type": "monumental_complex",
                "period": "Old Kingdom Egypt (2580-2560 BCE)",
                "calibration_notes": "Should detect massive pyramids with very high confidence"
            },
            {
                "name": "Chichen Itza Pyramid Complex", 
                "coordinates": {"lat_min": 20.680, "lat_max": 20.690, "lon_min": -88.570, "lon_max": -88.560},
                "expected_environment": "dry_forest",
                "expected_probability": 0.8,  # High - pyramid and temples
                "site_type": "ceremonial_center",
                "period": "Maya Classic (600-1200 CE)",
                "calibration_notes": "Should detect El Castillo pyramid and temple complex"
            },
            {
                "name": "Machu Picchu Citadel",
                "coordinates": {"lat_min": -13.165, "lat_max": -13.155, "lon_min": -72.550, "lon_max": -72.540},
                "expected_environment": "montane_forest",
                "expected_probability": 0.85,  # High - well-preserved stone structures
                "site_type": "citadel", 
                "period": "Inca Empire (1450-1572 CE)",
                "calibration_notes": "Should detect terraces and stone buildings in cloud forest"
            },
            {
                "name": "Tikal Maya City",
                "coordinates": {"lat_min": 17.220, "lat_max": 17.230, "lon_min": -89.625, "lon_max": -89.615},
                "expected_environment": "rainforest",
                "expected_probability": 0.75,  # High - but dense vegetation may obscure
                "site_type": "maya_city",
                "period": "Maya Classic (200-900 CE)",
                "calibration_notes": "Should detect temple mounds through dense rainforest canopy"
            },
            {
                "name": "Petra Rock-Cut City",
                "coordinates": {"lat_min": 30.326, "lat_max": 30.336, "lon_min": 35.441, "lon_max": 35.451},
                "expected_environment": "desert",
                "expected_probability": 0.8,  # High - massive rock-cut structures
                "site_type": "rock_cut_city",
                "period": "Nabataean Kingdom (1st century BCE - 4th century CE)",
                "calibration_notes": "Should detect Treasury and Monastery through rock analysis"
            },
            {
                "name": "Stonehenge Megalithic Complex",
                "coordinates": {"lat_min": 51.176, "lat_max": 51.186, "lon_min": -1.830, "lon_max": -1.820},
                "expected_environment": "agricultural",
                "expected_probability": 0.6,  # Medium - subtle earthworks and standing stones
                "site_type": "megalithic_complex",
                "period": "Neolithic to Bronze Age (3100-1600 BCE)",
                "calibration_notes": "Should detect subtle earthworks and stone arrangements"
            },
            {
                "name": "Mohenjo-Daro Bronze Age City",
                "coordinates": {"lat_min": 27.322, "lat_max": 27.332, "lon_min": 68.136, "lon_max": 68.146},
                "expected_environment": "arid_agricultural",
                "expected_probability": 0.65,  # Medium - mud brick may be subtle
                "site_type": "bronze_age_city",
                "period": "Indus Valley Civilization (2600-1900 BCE)",
                "calibration_notes": "Should detect street grid and mud brick mound structures"
            },
            {
                "name": "Easter Island Moai Platforms",
                "coordinates": {"lat_min": -27.115, "lat_max": -27.105, "lon_min": -109.350, "lon_max": -109.340},
                "expected_environment": "volcanic_island",
                "expected_probability": 0.7,  # High-Medium - stone statues and platforms
                "site_type": "ceremonial_platforms_moai",
                "period": "Polynesian Settlement (1250-1500 CE)",
                "calibration_notes": "Should detect ahu platforms and fallen moai statues"
            },
            {
                "name": "Pompeii Roman City",
                "coordinates": {"lat_min": 40.747, "lat_max": 40.757, "lon_min": 14.491, "lon_max": 14.501},
                "expected_environment": "mediterranean",
                "expected_probability": 0.85,  # High - exceptionally preserved stone buildings
                "site_type": "roman_city",
                "period": "Roman Republic/Empire (7th century BCE - 79 CE)",
                "calibration_notes": "Should detect streets, houses, and public buildings"
            },
            {
                "name": "Port Royal Submerged City",
                "coordinates": {"lat_min": 17.934, "lat_max": 17.944, "lon_min": -76.842, "lon_max": -76.832},
                "expected_environment": "shallow_sea",
                "expected_probability": 0.7,  # High - but underwater detection is challenging
                "site_type": "submerged_city",
                "period": "Colonial Era (1518-1692 CE)",
                "calibration_notes": "Should detect submerged building foundations (water analysis)"
            }
        ]
    
    def test_site(self, site: Dict[str, Any]) -> Dict[str, Any]:
        """Test individual archaeological site"""
        print(f"\nTesting: {site['name']}")
        print(f"   Expected: {site['expected_environment']} | Prob: {site['expected_probability']}")
        print(f"   Period: {site['period']}")
        print(f"   Notes: {site['calibration_notes']}")
        
        # Prepare request
        request_data = {
            "lat_min": site["coordinates"]["lat_min"],
            "lat_max": site["coordinates"]["lat_max"],
            "lon_min": site["coordinates"]["lon_min"],
            "lon_max": site["coordinates"]["lon_max"],
            "region_name": f"Calibration Test - {site['name']}",
            "resolution_m": 100,
            "active_rules": ["archaeological_probability", "modern_exclusion"],
            "layers_to_analyze": ["all"]
        }
        
        # Make API call
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.api_base}/analyze",
                json=request_data,
                timeout=120  # Extended timeout for comprehensive analysis
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract key metrics
                env_class = result.get('environment_classification', {})
                arch_results = result.get('archaeological_results', {})
                ai_exp = result.get('ai_explanations', {})
                temporal = result.get('temporal_sensor_analysis', {})
                convergence = result.get('convergence_analysis', {})
                instruments = result.get('instrumental_measurements', [])
                
                # Calculate calibration metrics
                test_result = {
                    "site_name": site["name"],
                    "expected_environment": site["expected_environment"],
                    "actual_environment": env_class.get('environment_type'),
                    "expected_probability": site["expected_probability"],
                    "actual_probability": arch_results.get('archaeological_probability', 0),
                    "environment_match": env_class.get('environment_type') == site["expected_environment"],
                    "probability_difference": arch_results.get('archaeological_probability', 0) - site["expected_probability"],
                    "ai_available": ai_exp.get('ai_available', False),
                    "ai_mode": ai_exp.get('mode', 'unknown'),
                    "temporal_active": bool(temporal and temporal.get('persistence_score', 0) > 0.1),
                    "temporal_score": temporal.get('persistence_score', 0),
                    "convergence_met": convergence.get('convergence_met', False),
                    "instruments_converging": convergence.get('instruments_converging', 0),
                    "total_instruments": len(instruments),
                    "response_time_seconds": response_time,
                    "analysis_type": result.get('region_info', {}).get('analysis_type', 'unknown'),
                    "site_recognized": arch_results.get('site_recognized', False),
                    "validation_success": self._evaluate_calibration_result(site, result),
                    "calibration_score": self._calculate_calibration_score(site, result)
                }
                
                # Print quick results
                print(f"   Response: {response_time:.1f}s | Env: {test_result['actual_environment']}")
                print(f"   Probability: {test_result['actual_probability']:.3f} (expected: {test_result['expected_probability']})")
                print(f"   IA: {'OK' if test_result['ai_available'] else 'MISSING'} | Temporal: {'OK' if test_result['temporal_active'] else 'MISSING'}")
                print(f"   Calibration Score: {test_result['calibration_score']:.1f}/100")
                
                return test_result
                
            else:
                error_result = {
                    "site_name": site["name"],
                    "error": f"HTTP {response.status_code}: {response.text[:200]}",
                    "validation_success": False,
                    "calibration_score": 0
                }
                print(f"   ERROR: {response.status_code} - {response.text[:100]}...")
                return error_result
                
        except Exception as e:
            error_result = {
                "site_name": site["name"],
                "error": str(e),
                "validation_success": False,
                "calibration_score": 0
            }
            print(f"   EXCEPTION: {e}")
            return error_result
    
    def _evaluate_calibration_result(self, site: Dict[str, Any], result: Dict[str, Any]) -> bool:
        """Evaluate if calibration test passed"""
        env_class = result.get('environment_classification', {})
        arch_results = result.get('archaeological_results', {})
        
        # Environment must match
        env_ok = env_class.get('environment_type') == site["expected_environment"]
        
        # Probability should be within reasonable range
        actual_prob = arch_results.get('archaeological_probability', 0)
        expected_prob = site["expected_probability"]
        prob_ok = abs(actual_prob - expected_prob) <= 0.3  # Allow 30% tolerance
        
        # AI should be available for most sites
        ai_available = result.get('ai_explanations', {}).get('ai_available', False)
        
        return env_ok and prob_ok and ai_available
    
    def _calculate_calibration_score(self, site: Dict[str, Any], result: Dict[str, Any]) -> float:
        """Calculate detailed calibration score (0-100)"""
        score = 0.0
        
        # Environment classification (30 points)
        env_class = result.get('environment_classification', {})
        if env_class.get('environment_type') == site["expected_environment"]:
            score += 30
        
        # Probability accuracy (25 points)
        arch_results = result.get('archaeological_results', {})
        actual_prob = arch_results.get('archaeological_probability', 0)
        expected_prob = site["expected_probability"]
        prob_diff = abs(actual_prob - expected_prob)
        prob_score = max(0, 25 - (prob_diff * 50))  # Each 0.02 difference = 1 point
        score += prob_score
        
        # AI integration (20 points)
        ai_exp = result.get('ai_explanations', {})
        if ai_exp.get('ai_available'):
            score += 15
        if ai_exp.get('mode') == 'intelligent_integrated_analysis':
            score += 5
        
        # Instrument convergence (15 points)
        convergence = result.get('convergence_analysis', {})
        if convergence.get('convergence_met'):
            score += 10
        if convergence.get('instruments_converging', 0) >= 2:
            score += 5
        
        # Temporal analysis (10 points for terrestrial sites)
        if site["expected_environment"] not in ['shallow_sea', 'deep_sea', 'glacier']:
            temporal = result.get('temporal_sensor_analysis', {})
            if temporal and temporal.get('persistence_score', 0) > 0.1:
                score += 10
        
        return min(100, score)
    
    def run_calibration_suite(self) -> Dict[str, Any]:
        """Run complete calibration test suite"""
        print("=" * 80)
        print("ARCHEOSCOPE CALIBRATION SUITE")
        print("Testing 10 archaeological sites for surgical calibration")
        print("=" * 80)
        
        start_time = time.time()
        results = []
        
        for i, site in enumerate(self.calibration_sites, 1):
            print(f"\n📍 Test {i}/10: {site['name']}")
            print("-" * 50)
            
            result = self.test_site(site)
            results.append(result)
            
            # Brief pause between tests
            time.sleep(2)
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful_tests = sum(1 for r in results if r.get('validation_success', False))
        calibration_scores = [r.get('calibration_score', 0) for r in results]
        avg_score = sum(calibration_scores) / len(calibration_scores)
        
        # Generate summary
        summary = {
            "test_date": datetime.now().isoformat(),
            "total_sites": len(self.calibration_sites),
            "successful_tests": successful_tests,
            "success_rate": successful_tests / len(self.calibration_sites),
            "average_calibration_score": avg_score,
            "total_test_time_seconds": total_time,
            "results": results,
            "calibration_quality": self._assess_calibration_quality(avg_score),
            "recommendations": self._generate_calibration_recommendations(results)
        }
        
        # Print summary
        self._print_calibration_summary(summary)
        
        return summary
    
    def _assess_calibration_quality(self, avg_score: float) -> str:
        """Assess overall calibration quality"""
        if avg_score >= 85:
            return "EXCELLENT - Surgical calibration achieved"
        elif avg_score >= 75:
            return "GOOD - Calibration successful with minor adjustments needed"
        elif avg_score >= 60:
            return "ACCEPTABLE - Calibration functional but needs improvement"
        elif avg_score >= 40:
            return "POOR - Major calibration issues detected"
        else:
            return "CRITICAL - System needs immediate recalibration"
    
    def _generate_calibration_recommendations(self, results: List[Dict[str, Any]]) -> List[str]:
        """Generate calibration recommendations based on test results"""
        recommendations = []
        
        # Check environment classification
        env_errors = sum(1 for r in results if not r.get('environment_match', True))
        if env_errors > 2:
            recommendations.append("🌍 Improve environment classifier accuracy")
        
        # Check probability calibration
        prob_errors = sum(1 for r in results if abs(r.get('probability_difference', 0)) > 0.3)
        if prob_errors > 3:
            recommendations.append("📊 Recalibrate probability thresholds")
        
        # Check AI integration
        ai_missing = sum(1 for r in results if not r.get('ai_available', False))
        if ai_missing > 1:
            recommendations.append("🤖 Ensure IA assistant is always available")
        
        # Check temporal sensor
        terrestrial_sites = sum(1 for r in results if r.get('expected_environment') not in ['shallow_sea'])
        temporal_missing = sum(1 for r in results if not r.get('temporal_active', False) and r.get('expected_environment') not in ['shallow_sea'])
        if temporal_missing > terrestrial_sites * 0.5:
            recommendations.append("⏰ Improve temporal sensor for terrestrial sites")
        
        # Check instrument convergence
        convergence_missing = sum(1 for r in results if not r.get('convergence_met', False))
        if convergence_missing > len(results) * 0.7:
            recommendations.append("🔧 Adjust instrument sensitivity thresholds")
        
        if not recommendations:
            recommendations.append("✅ System properly calibrated - no major issues detected")
        
        return recommendations
    
    def _print_calibration_summary(self, summary: Dict[str, Any]):
        """Print detailed calibration summary"""
        print("\n" + "=" * 80)
        print("CALIBRATION TEST SUMMARY")
        print("=" * 80)
        
        print(f"Test Date: {summary['test_date']}")
        print(f"Total Sites: {summary['total_sites']}")
        print(f"Successful Tests: {summary['successful_tests']}/{summary['total_sites']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Average Calibration Score: {summary['average_calibration_score']:.1f}/100")
        print(f"Total Test Time: {summary['total_test_time_seconds']:.1f} seconds")
        print(f"Calibration Quality: {summary['calibration_quality']}")
        
        print("\n🎯 INDIVIDUAL SITE RESULTS:")
        print("-" * 80)
        for result in summary['results']:
            if 'error' in result:
                print(f"ERROR {result['site_name']}: ERROR - {result['error']}")
            else:
                status = "OK" if result['validation_success'] else "WARN"
                print(f"{status} {result['site_name']}: Score {result['calibration_score']:.1f}/100")
                print(f"   Env: {result['expected_environment']}→{result['actual_environment']}")
                print(f"   Prob: {result['expected_probability']}→{result['actual_probability']:.3f}")
                print(f"   AI: {'OK' if result['ai_available'] else 'MISSING'} | Temporal: {'OK' if result['temporal_active'] else 'MISSING'}")
        
        print("\n📋 RECOMMENDATIONS:")
        print("-" * 40)
        for rec in summary['recommendations']:
            print(rec)
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    # Run calibration suite
    calibrator = CalibrationTestSuite()
    results = calibrator.run_calibration_suite()
    
    # Save results to file
    output_file = f"calibration_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📁 Detailed results saved to: {output_file}")