import asyncio
import httpx
import json
import os
from datetime import datetime

async def run_blind_mission_non_iconic():
    # Path 2: Application to Non-Iconic or Forgotten Sites
    sites = [
        {"name": "Poverty Point (Earthworks)", "lat": 32.637, "lon": -91.411, "type": "Native American"},
        {"name": "Chan Chan (Adobe)", "lat": -8.110, "lon": -79.072, "type": "Chimu City"},
        {"name": "Great Zimbabwe (Stone)", "lat": -20.267, "lon": 30.933, "type": "Sub-Saharan"},
        {"name": "L'Anse aux Meadows (Subtle)", "lat": 51.595, "lon": -55.531, "type": "Viking Outpost"},
        {"name": "Tlatelolco (Urban)", "lat": 19.451, "lon": -99.135, "type": "Aztec Complex"},
        {"name": "Marajo Mounds (Earth)", "lat": -0.800, "lon": -48.600, "type": "Amazonian"},
        {"name": "Hattusa (Hittite)", "lat": 40.021, "lon": 34.613, "type": "Anatolian"},
        # Blind Controls
        {"name": "Sahara Blind North", "lat": 26.500, "lon": 23.200, "type": "NEG_CONTROL"},
        {"name": "Andes Blind Ridge", "lat": -15.500, "lon": -71.200, "type": "NEG_CONTROL"},
        {"name": "Siberian Blind Plain", "lat": 65.500, "lon": 95.000, "type": "NEG_CONTROL"}
    ]
    
    delta = 0.005 # ~1km2
    url = "http://localhost:8003/api/scientific/analyze"
    results = []
    
    print(f"\n🚀 BLIND MISSION: NON-ICONIC ARCHEO-STRUCTURAL TEST")
    print(f"====================================================")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        for site in sites:
            print(f"\n📍 Scanning {site['name']}...")
            payload = {
                "lat_min": site['lat'] - delta,
                "lat_max": site['lat'] + delta,
                "lon_min": site['lon'] - delta,
                "lon_max": site['lon'] + delta,
                "region_name": f"BLIND_TEST_{site['name'].split(' ')[0]}"
            }
            
            try:
                response = await client.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    # Calculate SII (Structural Invariant Index)
                    res = data.get('etp_summary', {})
                    coh = res.get('coherencia_3d', 0)
                    per = res.get('persistencia_temporal', 0)
                    ess = res.get('ess_superficial', 0)
                    hrm = data.get('anomaly_map', {}).get('metadata', {}).get('geometric_features_count', 0)
                    
                    sii = (coh * per) + (ess * (hrm / 200.0))
                    
                    invariants = {
                        "name": site['name'],
                        "type": site['type'],
                        "geo_coherence": coh,
                        "persistence": per,
                        "ess_score": ess,
                        "hrm_peaks": hrm,
                        "sii_index": sii,
                        "classification": "HISA" if sii > 0.90 else ("AMBIGUOUS" if sii > 0.75 else "GEOLOGICAL")
                    }
                    results.append(invariants)
                    print(f"✅ SII: {sii:.4f} | Result: {invariants['classification']}")
                else:
                    print(f"❌ Error {response.status_code} for {site['name']}")
            except Exception as e:
                print(f"💥 Exception scanning {site['name']}: {e}")
                
    # Save Mission Results
    with open("blind_mission_non_iconic_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"\n📊 BLIND MISSION COMPLETE. Results saved to blind_mission_non_iconic_results.json")

if __name__ == "__main__":
    asyncio.run(run_blind_mission_non_iconic())
