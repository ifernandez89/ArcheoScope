import asyncio
import httpx
import json
import os
import numpy as np
from datetime import datetime
from scipy import stats

async def run_statistical_mission():
    # 1. Expand Sites (Active Group)
    active_sites = [
        {"name": "Giza Pyramid", "lat": 29.9792, "lon": 31.1342, "group": "Active"},
        {"name": "Machu Picchu", "lat": -13.1631, "lon": -72.5450, "group": "Active"},
        {"name": "Sacsayhuaman", "lat": -13.5090, "lon": -71.9817, "group": "Active"},
        {"name": "Angkor Wat", "lat": 13.4125, "lon": 103.8670, "group": "Active"},
        {"name": "Tiwanaku", "lat": -16.5546, "lon": -68.6738, "group": "Active"},
        {"name": "Stonehenge", "lat": 51.1789, "lon": -1.8262, "group": "Active"},
        {"name": "Teotihuacan", "lat": 19.6925, "lon": -98.8438, "group": "Active"},
        {"name": "Gobekli Tepe", "lat": 37.2231, "lon": 38.9226, "group": "Active"},
        {"name": "Chavin de Huantar", "lat": -9.5925, "lon": -77.1775, "group": "Active"},
        {"name": "Baalbek", "lat": 34.0056, "lon": 36.2036, "group": "Active"},
        {"name": "Easter Island", "lat": -27.1259, "lon": -109.2765, "group": "Active"},
        {"name": "Nan Madol", "lat": 6.8447, "lon": 158.3306, "group": "Active"},
        {"name": "Petra", "lat": 30.3285, "lon": 35.4444, "group": "Active"},
        {"name": "Borobudur", "lat": -7.6079, "lon": 110.2038, "group": "Active"},
        {"name": "Caral", "lat": -10.8927, "lon": -77.5250, "group": "Active"}
    ]
    
    # 2. Expand Controls (Negative Group)
    control_sites = [
        {"name": "Sahara Central", "lat": 23.4162, "lon": 12.3308, "group": "Control"},
        {"name": "Atacama Plateau", "lat": -24.5, "lon": -69.25, "group": "Control"},
        {"name": "Australian Outback", "lat": -25.0, "lon": 133.0, "group": "Control"},
        {"name": "Siberian Plateau", "lat": 62.0, "lon": 105.0, "group": "Control"},
        {"name": "Greenland Ice Shield", "lat": 72.0, "lon": -40.0, "group": "Control"},
        {"name": "Patagonia Steppe", "lat": -48.5, "lon": -70.5, "group": "Control"},
        {"name": "Empty Amazonia", "lat": -5.0, "lon": -65.0, "group": "Control"},
        {"name": "Empty Antarctic Plains", "lat": -80.0, "lon": 40.0, "group": "Control"},
        {"name": "Grand Canyon Raw", "lat": 36.1069, "lon": -112.1129, "group": "Control"},
        {"name": "Taklamakan Deep", "lat": 39.0, "lon": 82.5, "group": "Control"},
        {"name": "Gobi Empty Sector", "lat": 44.0, "lon": 105.0, "group": "Control"},
        {"name": "Pacific Abyss Point", "lat": 0.0, "lon": -150.0, "group": "Control"},
        {"name": "Empty Icelandic Highlands", "lat": 64.8, "lon": -18.5, "group": "Control"},
        {"name": "Tibetan Wilderness", "lat": 33.5, "lon": 85.0, "group": "Control"},
        {"name": "Namib Dune Field", "lat": -24.5, "lon": 15.3, "group": "Control"}
    ]
    
    all_sites = active_sites + control_sites
    delta = 0.005 # ~1km2
    url = "http://localhost:8003/api/scientific/analyze"
    results = []
    
    print(f"\n🚀 STARTING MASSIVE STATISTICAL MISSION: 30 NODES")
    print(f"====================================================")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        for i, site in enumerate(all_sites):
            print(f"\n[{i+1}/30] Scanning {site['name']} ({site['group']})...")
            payload = {
                "lat_min": site['lat'] - delta,
                "lat_max": site['lat'] + delta,
                "lon_min": site['lon'] - delta,
                "lon_max": site['lon'] + delta,
                "region_name": f"MISSION_V3_{site['name']}"
            }
            
            try:
                response = await client.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    invariants = {
                        "name": site['name'],
                        "group": site['group'],
                        "ess_score": data.get('etp_summary', {}).get('ess_superficial', 0),
                        "geo_coherence": data.get('etp_summary', {}).get('coherencia_3d', 0),
                        "persistence": data.get('etp_summary', {}).get('persistencia_temporal', 0),
                        "anthropic_prob": data.get('archaeological_results', {}).get('anthropic_probability', 0),
                        "hrm_peaks": data.get('anomaly_map', {}).get('metadata', {}).get('geometric_features_count', 0)
                    }
                    results.append(invariants)
                    print(f"✅ Result: Coherence={invariants['geo_coherence']:.4f} | ESS={invariants['ess_score']:.4f}")
                else:
                    print(f"❌ Error {response.status_code} for {site['name']}")
            except Exception as e:
                print(f"💥 Exception: {e}")
                
    # 3. Statistical Analysis
    active_coherence = [r['geo_coherence'] for r in results if r['group'] == 'Active']
    control_coherence = [r['geo_coherence'] for r in results if r['group'] == 'Control']
    
    u_stat, p_value = stats.mannwhitneyu(active_coherence, control_coherence, alternative='greater')
    
    mission_data = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "node_count": len(results),
            "p_value_coherence": p_value,
            "mean_active_coherence": np.mean(active_coherence) if active_coherence else 0,
            "mean_control_coherence": np.mean(control_coherence) if control_coherence else 0
        },
        "results": results
    }
    
    # Save Results
    filename = "global_statistical_mission.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(mission_data, f, indent=2)
        
    print(f"\n📊 MISSION COMPLETE. P-Value (Mann-Whitney U): {p_value:.6f}")
    if p_value < 0.01:
        print("🚨 NULL HYPOTHESIS H0 REJECTED. Archaeological sites show significantly higher structural coherence.")
    else:
        print("⚪ H1 NOT SUPPORTED. No significant difference found between site groups.")

if __name__ == "__main__":
    asyncio.run(run_statistical_mission())
