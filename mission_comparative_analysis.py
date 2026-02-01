import asyncio
import httpx
import json
import os
from datetime import datetime

async def run_comparative_mission():
    sites = [
        {"name": "Giza Pyramid", "lat": 29.9792, "lon": 31.1342, "type": "Benchmark"},
        {"name": "Machu Picchu", "lat": -13.1631, "lon": -72.5450, "type": "Mountain Engineering"},
        {"name": "Sacsayhuaman", "lat": -13.5090, "lon": -71.9817, "type": "Megalithic"},
        {"name": "Angkor Wat", "lat": 13.4125, "lon": 103.8670, "type": "Urban/Hydraulic"},
        {"name": "Tiwanaku / Puma Punku", "lat": -16.5546, "lon": -68.6738, "type": "Modular"},
        {"name": "Sahara Control", "lat": 23.4162, "lon": 12.3308, "type": "Negative Control"}
    ]
    
    delta = 0.005 # ~1km2
    url = "http://localhost:8003/api/scientific/analyze"
    results = []
    
    print(f"\n🚀 STARTING COMPARATIVE ARCHEO-STRUCTURAL MISSION")
    print(f"====================================================")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        for site in sites:
            print(f"\n📍 Scanning {site['name']} ({site['type']})...")
            payload = {
                "lat_min": site['lat'] - delta,
                "lat_max": site['lat'] + delta,
                "lon_min": site['lon'] - delta,
                "lon_max": site['lon'] + delta,
                "region_name": f"MISSION_{site['name']}"
            }
            
            try:
                response = await client.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    # Extract key invariants mapping to the 5 requested ones
                    invariants = {
                        "name": site['name'],
                        "type": site['type'],
                        "ess_score": data.get('etp_summary', {}).get('ess_superficial', 0),
                        "geo_coherence": data.get('etp_summary', {}).get('coherencia_3d', 0),
                        "persistence": data.get('etp_summary', {}).get('persistencia_temporal', 0),
                        "anthropic_prob": data.get('archaeological_results', {}).get('anthropic_probability', 0),
                        "scientific_confidence": data.get('archaeological_results', {}).get('scientific_confidence', 'N/A'),
                        "hrm_peaks": data.get('anomaly_map', {}).get('metadata', {}).get('geometric_features_count', 0)
                    }
                    results.append(invariants)
                    print(f"✅ Coherence: {invariants['geo_coherence']:.4f} | ESS: {invariants['ess_score']:.4f}")
                else:
                    print(f"❌ Error {response.status_code} for {site['name']}")
            except Exception as e:
                print(f"💥 Exception scanning {site['name']}: {e}")
                
    # Save Mission Results
    with open("comparative_mission_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"\n📊 MISSION COMPLETE. Results saved to comparative_mission_results.json")

if __name__ == "__main__":
    asyncio.run(run_comparative_mission())
