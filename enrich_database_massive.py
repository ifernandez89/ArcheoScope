#!/usr/bin/env python3
"""
Enriquecimiento MASIVO de BD con sitios arqueológicos.

OBJETIVO: Analizar 100+ sitios arqueológicos importantes del mundo.

CATEGORÍAS:
- Civilizaciones antiguas (Egipto, Mesopotamia, Grecia, Roma)
- Mesoamérica (Maya, Azteca, Olmeca)
- Sudamérica (Inca, Nazca, Moche)
- Asia (China, India, Japón, Camboya)
- Europa (Megalíticos, Celtas, Vikingos)
- África (Nubia, Etiopía, Zimbabwe)
- Medio Oriente (Petra, Palmira, Babilonia)
"""

import requests
import json
import time
from typing import Dict, List
import sys

API_BASE_URL = "http://localhost:8002"

# MEGA LISTA DE SITIOS ARQUEOLÓGICOS
ARCHAEOLOGICAL_SITES = [
    # ========== EGIPTO (20 sitios) ==========
    {"name": "Pirámides de Giza", "country": "Egipto", "lat": 29.9792, "lon": 31.1342, "env": "desert"},
    {"name": "Valle de los Reyes", "country": "Egipto", "lat": 25.7402, "lon": 32.6014, "env": "desert"},
    {"name": "Karnak", "country": "Egipto", "lat": 25.7188, "lon": 32.6573, "env": "desert"},
    {"name": "Abu Simbel", "country": "Egipto", "lat": 22.3372, "lon": 31.6258, "env": "desert"},
    {"name": "Luxor", "country": "Egipto", "lat": 25.6872, "lon": 32.6396, "env": "desert"},
    {"name": "Saqqara", "country": "Egipto", "lat": 29.8714, "lon": 31.2166, "env": "desert"},
    {"name": "Dendera", "country": "Egipto", "lat": 26.1417, "lon": 32.6703, "env": "desert"},
    {"name": "Edfu", "country": "Egipto", "lat": 24.9778, "lon": 32.8736, "env": "desert"},
    {"name": "Kom Ombo", "country": "Egipto", "lat": 24.4517, "lon": 32.9317, "env": "desert"},
    {"name": "Philae", "country": "Egipto", "lat": 24.0253, "lon": 32.8844, "env": "desert"},
    
    # ========== PERÚ (15 sitios) ==========
    {"name": "Machu Picchu", "country": "Perú", "lat": -13.1631, "lon": -72.5450, "env": "mountain"},
    {"name": "Líneas de Nazca", "country": "Perú", "lat": -14.7390, "lon": -75.1300, "env": "desert"},
    {"name": "Cusco", "country": "Perú", "lat": -13.5319, "lon": -71.9675, "env": "mountain"},
    {"name": "Ollantaytambo", "country": "Perú", "lat": -13.2572, "lon": -72.2653, "env": "mountain"},
    {"name": "Sacsayhuamán", "country": "Perú", "lat": -13.5089, "lon": -71.9819, "env": "mountain"},
    {"name": "Chan Chan", "country": "Perú", "lat": -8.1061, "lon": -79.0747, "env": "coastal"},
    {"name": "Chavín de Huántar", "country": "Perú", "lat": -9.5944, "lon": -77.1772, "env": "mountain"},
    {"name": "Caral", "country": "Perú", "lat": -10.8933, "lon": -77.5203, "env": "coastal"},
    {"name": "Sipán", "country": "Perú", "lat": -6.7667, "lon": -79.6000, "env": "coastal"},
    {"name": "Kuélap", "country": "Perú", "lat": -6.4167, "lon": -77.9167, "env": "mountain"},
    
    # ========== MÉXICO (20 sitios) ==========
    {"name": "Teotihuacán", "country": "México", "lat": 19.6925, "lon": -98.8438, "env": "highland"},
    {"name": "Chichén Itzá", "country": "México", "lat": 20.6843, "lon": -88.5678, "env": "tropical_forest"},
    {"name": "Palenque", "country": "México", "lat": 17.4839, "lon": -92.0458, "env": "tropical_forest"},
    {"name": "Uxmal", "country": "México", "lat": 20.3597, "lon": -89.7714, "env": "tropical_forest"},
    {"name": "Tulum", "country": "México", "lat": 20.2114, "lon": -87.4289, "env": "coastal"},
    {"name": "Monte Albán", "country": "México", "lat": 17.0433, "lon": -96.7678, "env": "highland"},
    {"name": "Calakmul", "country": "México", "lat": 18.1050, "lon": -89.8119, "env": "tropical_forest"},
    {"name": "Tikal", "country": "Guatemala", "lat": 17.2221, "lon": -89.6236, "env": "tropical_forest"},
    {"name": "Copán", "country": "Honduras", "lat": 14.8400, "lon": -89.1419, "env": "tropical_forest"},
    {"name": "Tenochtitlán", "country": "México", "lat": 19.4326, "lon": -99.1332, "env": "urban"},
    
    # ========== GRECIA (10 sitios) ==========
    {"name": "Acrópolis de Atenas", "country": "Grecia", "lat": 37.9715, "lon": 23.7257, "env": "urban"},
    {"name": "Delfos", "country": "Grecia", "lat": 38.4824, "lon": 22.5011, "env": "mountain"},
    {"name": "Olimpia", "country": "Grecia", "lat": 37.6379, "lon": 21.6300, "env": "grassland"},
    {"name": "Micenas", "country": "Grecia", "lat": 37.7308, "lon": 22.7564, "env": "highland"},
    {"name": "Knossos", "country": "Grecia", "lat": 35.2980, "lon": 25.1631, "env": "coastal"},
    {"name": "Epidauro", "country": "Grecia", "lat": 37.5961, "lon": 23.0789, "env": "grassland"},
    {"name": "Delos", "country": "Grecia", "lat": 37.3964, "lon": 25.2683, "env": "coastal"},
    {"name": "Meteora", "country": "Grecia", "lat": 39.7217, "lon": 21.6306, "env": "mountain"},
    
    # ========== ITALIA (10 sitios) ==========
    {"name": "Pompeya", "country": "Italia", "lat": 40.7489, "lon": 14.4839, "env": "urban"},
    {"name": "Herculano", "country": "Italia", "lat": 40.8061, "lon": 14.3478, "env": "urban"},
    {"name": "Coliseo Romano", "country": "Italia", "lat": 41.8902, "lon": 12.4922, "env": "urban"},
    {"name": "Foro Romano", "country": "Italia", "lat": 41.8925, "lon": 12.4853, "env": "urban"},
    {"name": "Ostia Antica", "country": "Italia", "lat": 41.7556, "lon": 12.2917, "env": "coastal"},
    {"name": "Paestum", "country": "Italia", "lat": 40.4200, "lon": 15.0058, "env": "coastal"},
    {"name": "Valle de los Templos", "country": "Italia", "lat": 37.2903, "lon": 13.5844, "env": "coastal"},
    
    # ========== ASIA (15 sitios) ==========
    {"name": "Angkor Wat", "country": "Camboya", "lat": 13.4125, "lon": 103.8670, "env": "tropical_forest"},
    {"name": "Borobudur", "country": "Indonesia", "lat": -7.6079, "lon": 110.2038, "env": "tropical_forest"},
    {"name": "Gran Muralla China", "country": "China", "lat": 40.4319, "lon": 116.5704, "env": "mountain"},
    {"name": "Terracota de Xi'an", "country": "China", "lat": 34.3848, "lon": 109.2789, "env": "highland"},
    {"name": "Petra", "country": "Jordania", "lat": 30.3285, "lon": 35.4444, "env": "desert"},
    {"name": "Persépolis", "country": "Irán", "lat": 29.9344, "lon": 52.8906, "env": "highland"},
    {"name": "Bagan", "country": "Myanmar", "lat": 21.1717, "lon": 94.8578, "env": "grassland"},
    {"name": "Ayutthaya", "country": "Tailandia", "lat": 14.3532, "lon": 100.5775, "env": "tropical_forest"},
    {"name": "Hampi", "country": "India", "lat": 15.3350, "lon": 76.4600, "env": "highland"},
    {"name": "Mohenjo-daro", "country": "Pakistán", "lat": 27.3244, "lon": 68.1378, "env": "desert"},
    
    # ========== EUROPA (10 sitios) ==========
    {"name": "Stonehenge", "country": "Reino Unido", "lat": 51.1789, "lon": -1.8262, "env": "grassland"},
    {"name": "Carnac", "country": "Francia", "lat": 47.5828, "lon": -3.0758, "env": "coastal"},
    {"name": "Newgrange", "country": "Irlanda", "lat": 53.6947, "lon": -6.4753, "env": "grassland"},
    {"name": "Avebury", "country": "Reino Unido", "lat": 51.4289, "lon": -1.8536, "env": "grassland"},
    {"name": "Skara Brae", "country": "Reino Unido", "lat": 59.0489, "lon": -3.3428, "env": "coastal"},
    
    # ========== MEDIO ORIENTE (10 sitios) ==========
    {"name": "Palmira", "country": "Siria", "lat": 34.5561, "lon": 38.2692, "env": "desert"},
    {"name": "Babilonia", "country": "Irak", "lat": 32.5355, "lon": 44.4275, "env": "desert"},
    {"name": "Ur", "country": "Irak", "lat": 30.9625, "lon": 46.1031, "env": "desert"},
    {"name": "Nínive", "country": "Irak", "lat": 36.3600, "lon": 43.1528, "env": "highland"},
    {"name": "Jerash", "country": "Jordania", "lat": 32.2811, "lon": 35.8911, "env": "highland"},
    
    # ========== ÁFRICA (5 sitios) ==========
    {"name": "Gran Zimbabwe", "country": "Zimbabwe", "lat": -20.2667, "lon": 30.9333, "env": "grassland"},
    {"name": "Lalibela", "country": "Etiopía", "lat": 12.0333, "lon": 39.0472, "env": "mountain"},
    {"name": "Meroe", "country": "Sudán", "lat": 16.9383, "lon": 33.7483, "env": "desert"},
    {"name": "Cartago", "country": "Túnez", "lat": 36.8528, "lon": 10.3233, "env": "coastal"},
]

def analyze_site_batch(sites: List[Dict], start_idx: int = 0) -> List[Dict]:
    """
    Analizar un lote de sitios.
    
    Args:
        sites: Lista de sitios a analizar
        start_idx: Índice de inicio (para reanudar)
    
    Returns:
        Lista de resultados
    """
    results = []
    
    for i, site in enumerate(sites[start_idx:], start=start_idx + 1):
        print(f"\n{'#'*70}")
        print(f"# SITIO {i}/{len(sites)}")
        print(f"{'#'*70}")
        print(f"🏛️ {site['name']}, {site['country']}")
        print(f"📍 ({site['lat']:.4f}, {site['lon']:.4f})")
        
        try:
            request_data = {
                "lat_min": site['lat'] - 0.01,
                "lat_max": site['lat'] + 0.01,
                "lon_min": site['lon'] - 0.01,
                "lon_max": site['lon'] + 0.01,
                "region_name": f"{site['name']}, {site['country']}"
            }
            
            response = requests.post(
                f"{API_BASE_URL}/api/scientific/analyze",
                json=request_data,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                sci = result.get('scientific_output', {})
                
                # Extraer ESS
                ess = sci.get('explanatory_strangeness', 'none')
                ess_score = sci.get('strangeness_score', 0)
                
                print(f"✅ Análisis ID: {sci.get('analysis_id')}")
                print(f"   Anomaly: {sci.get('anomaly_score', 0):.3f}")
                print(f"   Prob: {sci.get('anthropic_probability', 0):.3f}")
                print(f"   ESS: {ess.upper()} ({ess_score:.3f})")
                print(f"   Action: {sci.get('recommended_action')}")
                
                results.append({
                    'site': site,
                    'success': True,
                    'analysis_id': sci.get('analysis_id'),
                    'ess': ess,
                    'ess_score': ess_score
                })
            else:
                print(f"❌ Error HTTP {response.status_code}")
                results.append({'site': site, 'success': False})
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({'site': site, 'success': False})
        
        # Pausa entre requests
        if i < len(sites):
            time.sleep(2)
    
    return results


def main():
    """Ejecutar enriquecimiento masivo."""
    
    print("\n" + "="*70)
    print("🏛️ ENRIQUECIMIENTO MASIVO DE BASE DE DATOS")
    print("="*70)
    print(f"\nTotal sitios a analizar: {len(ARCHAEOLOGICAL_SITES)}")
    print(f"API: {API_BASE_URL}")
    
    # Verificar backend
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=5)
        if response.status_code == 200:
            print("✅ Backend disponible")
        else:
            print("⚠️ Backend responde pero con error")
            return
    except:
        print("❌ Backend no disponible")
        print("   Ejecuta: python run_archeoscope.py")
        return
    
    input("\n▶️ Presiona Enter para comenzar el análisis masivo...")
    
    start_time = time.time()
    results = analyze_site_batch(ARCHAEOLOGICAL_SITES)
    end_time = time.time()
    
    # Resumen
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print("\n\n" + "="*70)
    print("📊 RESUMEN FINAL")
    print("="*70)
    print(f"\n✅ Exitosos: {successful}/{len(ARCHAEOLOGICAL_SITES)}")
    print(f"❌ Fallidos: {failed}/{len(ARCHAEOLOGICAL_SITES)}")
    print(f"⏱️ Tiempo total: {(end_time - start_time)/60:.1f} minutos")
    
    if successful > 0:
        # Estadísticas de ESS
        ess_counts = {}
        for r in results:
            if r['success']:
                ess = r.get('ess', 'none')
                ess_counts[ess] = ess_counts.get(ess, 0) + 1
        
        print(f"\n🔬 EXPLANATORY STRANGENESS SCORE:")
        for ess, count in sorted(ess_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {ess.upper()}: {count}")
        
        # Top ESS scores
        top_ess = sorted([r for r in results if r['success']], 
                        key=lambda x: x.get('ess_score', 0), reverse=True)[:10]
        
        print(f"\n🏆 TOP 10 ESS SCORES:")
        for r in top_ess:
            site = r['site']
            print(f"   {site['name']:<30} ESS={r['ess_score']:.3f} ({r['ess'].upper()})")
    
    # Guardar resultados
    output_file = "massive_enrichment_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    print("\n✅ ENRIQUECIMIENTO MASIVO COMPLETADO")


if __name__ == "__main__":
    main()
