import asyncio
import httpx
import json
import os
import numpy as np
from datetime import datetime

async def analyze_user_nodes():
    # 1. Definir los nuevos sitios proporcionados por el usuario
    sitios = [
        {"name": "Gran Pirámide en Xi'an (China)", "lat": 34.3828, "lon": 109.2753}
    ]
    
    delta = 0.005 # ~1km2 (Mismo que en mission_statistical_global.py)
    url = "http://localhost:8003/api/scientific/analyze"
    results = []
    
    # Umbrales del Clasificador Universal v2.0
    THRESHOLDS = {
        "G1_GEOMETRY": 0.92,      # Coherencia 3D
        "G2_PERSISTENCE": 0.70,   # Persistencia (Afectada por MSF)
        "G3_ANOMALY": 0.58,       # Contraste ESS
        "G4_MODULARITY": 140      # HRM Peaks
    }
    
    print(f"\n🚀 EJECUTANDO ANÁLISIS DE INVARIANTES: {len(sitios)} NUEVOS NODOS")
    print(f"====================================================")
    
    async def show_progress():
        """Muestra un indicador de progreso mientras espera la respuesta."""
        start_time = asyncio.get_event_loop().time()
        spin_chars = "|/-\\"
        idx = 0
        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            sys.stdout.write(f"\r⏳ Procesando datos satelitales masivos... {spin_chars[idx]} [Tiempo transcurrido: {elapsed:.0f}s]")
            sys.stdout.flush()
            idx = (idx + 1) % len(spin_chars)
            await asyncio.sleep(0.1)

    async with httpx.AsyncClient(timeout=None) as client:  # Timeout infinito para procesos científicos largos
        for i, site in enumerate(sitios):
            print(f"\n[{i+1}/{len(sitios)}] Analizando {site['name']}...")
            payload = {
                "lat_min": site['lat'] - delta,
                "lat_max": site['lat'] + delta,
                "lon_min": site['lon'] - delta,
                "lon_max": site['lon'] + delta,
                "region_name": f"USER_TEST_{site['name'].split()[0]}" # Revert to original region_name logic
            }
            
            # Iniciar spinner y request simultáneamente
            spinner_task = asyncio.create_task(show_progress())
            
            try:
                response = await client.post(url, json=payload)
                spinner_task.cancel()  # Detener spinner
                sys.stdout.write("\r✅ Análisis completado!                                          \n")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extraer métricas (Invariantes)
                    ess = float(data.get('etp_summary', {}).get('ess_superficial', 0))
                    coh = float(data.get('etp_summary', {}).get('coherencia_3d', 0))
                    per = float(data.get('etp_summary', {}).get('persistencia_temporal', 0))
                    hrm = int(data.get('anomaly_map', {}).get('metadata', {}).get('geometric_features_count', 0))
                    prob = float(data.get('archaeological_results', {}).get('anthropic_probability', 0))
                    
                    # Aplicar MSF (Material Sensitivity Factor)
                    # XI'AN: Adobe/Tierra apisonada -> MSF = 0.75
                    msf = 1.0
                    if "xi'an" in site['name'].lower():
                        msf = 0.75
                    
                    effective_g2 = per / msf
                    
                    # Evaluación de reglas v2.0
                    g1 = coh >= THRESHOLDS["G1_GEOMETRY"]
                    g2_pass = effective_g2 >= THRESHOLDS["G2_PERSISTENCE"]
                    g3_pass = ess >= THRESHOLDS["G3_ANOMALY"]
                    g4_pass = hrm >= THRESHOLDS["G4_MODULARITY"]
                    
                    # Lógica Decisora: (G1 AND G2) OR (G1 AND G4) OR (G2 AND G3)
                    is_anthropic = (g1 and g2_pass) or (g1 and g4_pass) or (g2_pass and g3_pass)
                    
                    # Clasificación Formal
                    veredicto = "NATURAL"
                    if is_anthropic:
                        if msf < 1.0:
                            veredicto = "AMB (MATERIAL BLANDO)"
                        else:
                            veredicto = "ANTRÓPICO PÉTREO"
                    
                    invariants = {
                        "name": site['name'],
                        "coords": f"{site['lat']:.4f}, {site['lon']:.4f}",
                        "ess_score": ess,
                        "geo_coherence": coh,
                        "persistence": per,
                        "msf": msf,
                        "effective_g2": effective_g2,
                        "hrm_peaks": hrm,
                        "anthropic_prob": prob,
                        "veredicto": veredicto,
                        "checks": {
                            "G1_Geometria": "PASSED" if g1 else "FAILED",
                            "G2_Estratigrafia": "PASSED" if g2 else "FAILED",
                            "G3_Anomalia": "PASSED" if g3 else "FAILED",
                            "G4_Modularidad": "PASSED" if g4 else "FAILED"
                        }
                    }
                    results.append(invariants)
                    
                    print(f"📊 Métricas: Coh={coh:.4f} | Per={per:.4f} | ESS={ess:.4f} | HRM={hrm}")
                    print(f"⚖️ Veredicto: {invariants['veredicto']}")
                else:
                    print(f"❌ Error {response.status_code} para {site['name']}")
                    print(f"Detalle: {response.text}")
            except Exception as e:
                print(f"💥 Excepción: {e}")
                
    # 3. Reporte Final
    print("\n" + "="*90)
    print("📊 REPORTE DE VALIDACIÓN DE INVARIANTES ARQUEOLÓGICOS")
    print("="*90)
    print("| Sitio | Coh (G1) | Per (G2) | ESS (G3) | HRM (G4) | Veredicto |")
    print("|-------|----------|----------|----------|----------|-----------|")
    for r in results:
        print(f"| {r['name'][:15]:15} | {r['geo_coherence']:.3f} | {r['persistence']:.3f} | {r['ess_score']:.3f} | {r['hrm_peaks']:8} | {r['veredicto']:11} |")
    
    # Guardar Resultados
    filename = f"REPORTE_INVARIANTES_USER_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ Análisis completado. Resultados guardados en {filename}")
    print("="*90 + "\n")

if __name__ == "__main__":
    import sys
    # Verificar si el backend está vivo antes de empezar
    async def check_backend():
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get("http://localhost:8003/status")
                return res.status_code == 200
        except:
            return False

    # if asyncio.run(check_backend()):
    asyncio.run(analyze_user_nodes())
    # else:
    #     print("❌ ERROR: El backend de ArcheoScope no está respondiendo en el puerto 8003.")
    #     print("Por favor, inicia el backend con 'python run_archeoscope.py' antes de correr este test.")
