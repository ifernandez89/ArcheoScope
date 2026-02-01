import json
import numpy as np
import os

def formalize_invariant_classifier():
    # 1. Load Mission Data
    with open("global_statistical_mission.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    results = data['results']
    active = [r for r in results if r['group'] == 'Active']
    control = [r for r in results if r['group'] == 'Control']
    
    # 2. Extract Features
    def get_features(group):
        return {
            'coh': [r['geo_coherence'] for r in group],
            'per': [r['persistence'] for r in group],
            'ess': [r['ess_score'] for r in group],
            'hrm': [r['hrm_peaks'] for r in group]
        }
    
    feat_a = get_features(active)
    feat_c = get_features(control)
    
    # 3. Analyze Separation
    # We want to find a metric: SII = f(coh, per, ess, hrm)
    # Observation: Anthropic sites have high (Coh * Per) and high (ESS * HRM)
    
    def calculate_sii(r):
        # Weighted index of Invariants
        # Coherence + Persistence (Structural rigidity)
        # ESS + HRM (Lithological Anomaly + Modular repetition)
        return (r['geo_coherence'] * r['persistence']) + (r['ess_score'] * (r['hrm_peaks'] / 200.0))

    sii_a = [calculate_sii(r) for r in active]
    sii_c = [calculate_sii(r) for r in control]
    
    threshold = (np.mean(sii_a) + np.mean(sii_c)) / 2
    
    # 4. Refine Thresholds for the 4 Keys
    # Based on the data distribution:
    # Archaeological sites often cross AT LEAST 3 of these 4 thresholds.
    
    t_coh = 0.915  # Separates Giza/Teotihuacan from standard desert
    t_per = 0.65   # Deep structural continuity
    t_ess = 0.55   # Anomaly intensity
    t_hrm = 140    # Modular complexity
    
    print(f"--- PRELIMINARY CLASSIFIER STATS ---")
    print(f"Active SII Mean: {np.mean(sii_a):.4f}")
    print(f"Control SII Mean: {np.mean(sii_c):.4f}")
    print(f"Recommended SII Threshold: {threshold:.4f}")
    print()
    
    # 5. Formalize the Algorithm (The Invariant Classifer)
    classifier_report = {
        "classifier_name": "ArcheoScope Universal Classifier v1.0",
        "minimum_invariant_set": {
            "G1_GEOMETRY": {
                "metric": "geo_coherence",
                "threshold": "> 0.915",
                "function": "Detects systemic order vs stochastic noise"
            },
            "G2_STRATIGRAPHY": {
                "metric": "persistence",
                "threshold": "> 0.70",
                "function": "Detects 3D continuity vs superficial erosion"
            },
            "G3_ANOMALY": {
                "metric": "ess_score",
                "threshold": "> 0.58",
                "function": "Detects lithological rupture"
            },
            "G4_MODULARITY": {
                "metric": "hrm_peaks",
                "threshold": "> 140",
                "function": "Detects repeating engineering solutions"
            }
        },
        "logic": "ANTHROPIC_SIGNAL = (G1 AND G2) OR (G1 AND G4) OR (G2 AND G3)",
        "validation_score": {
            "sensitivity": len([s for s in sii_a if s > threshold]) / len(sii_a),
            "specificity": len([s for s in sii_c if s < threshold]) / len(sii_c)
        }
    }
    
    with open("archeoscope_classifier_logic.json", "w", encoding="utf-8") as f:
        json.dump(classifier_report, f, indent=2)
    
    print(f"✅ Classifier Formalized: archeoscope_classifier_logic.json")

if __name__ == "__main__":
    formalize_invariant_classifier()
