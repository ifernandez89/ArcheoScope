#!/usr/bin/env python3
"""
Análisis Batch de Candidatos Arqueológicos
Analiza sitios propuestos con todos los instrumentos disponibles
y guarda resultados en BD para referencia futura
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "http://localhost:8002"

# Candidatos arqueológicos propuestos
ARCHAEOLOGICAL_CANDIDATES = [
    {
        "id": "valeriana_maya",
        "name": "Valeriana - Ciudad Maya (LiDAR)",
        "region": "Campeche, México",
        "environment": "forest",
        "description": "Ciudad maya recién descubierta con LiDAR. Miles de estructuras reveladas, gran parte sin analizar.",
        "lat": 18.72,
        "lon": -90.75,
        "bbox_size": 0.05,  # ~5km
        "priority": "high",
        "research_gaps": [
            "Estructuras menores fuera del núcleo urbano",
            "Rutas de conexión entre plazas",
            "Clasificación sistemática de características LiDAR"
        ]
    },
    {
        "id": "el_viandar_castle",
        "name": "El Viandar Castle & Settlement",
        "region": "Córdoba, España",
        "environment": "forest",
        "description": "Fortaleza con LiDAR parcial. Estructuras habitacionales sin revelar completamente.",
        "lat": 38.05,
        "lon": -4.30,
        "bbox_size": 0.03,  # ~3km
        "priority": "medium",
        "research_gaps": [
            "Estructuras residenciales no evidentes en LiDAR",
            "Microtopografía alrededor de fortaleza",
            "Integración geofísica + LiDAR"
        ]
    },
    {
        "id": "cedar_creek_earthworks",
        "name": "Cedar Creek Earthworks",
        "region": "Ontario, Canadá",
        "environment": "mountain",  # Llanura templada
        "description": "Earthworks con LiDAR no explotado en detalle. Palisadas y terraplenes.",
        "lat": 42.37,
        "lon": -82.95,
        "bbox_size": 0.04,  # ~4km
        "priority": "medium",
        "research_gaps": [
            "Conexión palisadas con redes regionales",
            "Microtopografía sin excavación",
            "Enterramientos o estructuras perimetrales"
        ]
    },
    {
        "id": "ocomtun_maya",
        "name": "Ocomtún - Ciudad Maya (Calakmul)",
        "region": "Calakmul, México",
        "environment": "forest",
        "description": "Ciudad maya descubierta con LiDAR. Solo reconocimiento superficial, falta análisis integral.",
        "lat": 18.55,
        "lon": -89.75,
        "bbox_size": 0.05,  # ~5km
        "priority": "high",
        "research_gaps": [
            "Patrones urbano vs rural",
            "Hidrología terrestre antigua",
            "Correlación con sitios LiDAR cercanos"
        ]
    },
    {
        "id": "amazonian_earthworks",
        "name": "Ancient Amazonian Earthworks (Kuhikugu)",
        "region": "Pará, Brasil",
        "environment": "forest",
        "description": "Miles de earthworks detectados. Observaciones preliminares sin modelado detallado.",
        "lat": -12.50,
        "lon": -53.00,
        "bbox_size": 0.06,  # ~6km
        "priority": "high",
        "research_gaps": [
            "Clasificación redes urbanas vs agrícolas",
            "Microtopografía y sistemas de agua",
            "Integración multiespectral natural vs cultural"
        ]
    }
]


def get_db_connection():
    """Obtener conexión a BD"""
    try:
        return psycopg2.connect(os.getenv("DATABASE_URL"))
    except Exception as e:
        print(f" Error conectando a BD: {e}")
        return None


def analyze_candidate(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analizar un candidato arqueológico con ArcheoScope
    """
    print(f"\n{'='*80}")
    print(f" ANALIZANDO: {candidate['name']}")
    print(f" Región: {candidate['region']}")
    print(f" Ambiente: {candidate['environment']}")
    print(f"{'='*80}\n")
    
    # Construir bbox
    offset = candidate['bbox_size'] / 2
    bbox = {
        "lat_min": candidate['lat'] - offset,
        "lat_max": candidate['lat'] + offset,
        "lon_min": candidate['lon'] - offset,
        "lon_max": candidate['lon'] + offset,
        "region_name": candidate['name']
    }
    
    print(f" BBox: [{bbox['lat_min']:.4f}, {bbox['lat_max']:.4f}] x [{bbox['lon_min']:.4f}, {bbox['lon_max']:.4f}]")
    print(f"  Iniciando análisis...\n")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json=bbox,
            timeout=120
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            # Extraer métricas clave
            metrics = {
                "candidate_id": candidate['id'],
                "candidate_name": candidate['name'],
                "region": candidate['region'],
                "environment_detected": result.get('environment_classification', {}).get('environment_type', 'unknown'),
                "environment_confidence": result.get('environment_classification', {}).get('confidence', 0),
                "archaeological_probability": result.get('archaeological_results', {}).get('archaeological_probability', 0),
                "confidence": result.get('archaeological_results', {}).get('confidence', 0),
                "result_type": result.get('archaeological_results', {}).get('result_type', 'unknown'),
                "instruments_measuring": len(result.get('instrumental_measurements', [])),
                "instruments_total": len(result.get('environment_classification', {}).get('primary_sensors', [])) + len(result.get('environment_classification', {}).get('secondary_sensors', [])),
                "convergence_achieved": result.get('convergence_analysis', {}).get('convergence_met', False),
                "temporal_analysis": result.get('temporal_analysis', {}).get('years_analyzed', 0) > 0,
                "ai_available": result.get('ai_explanations', {}).get('ai_available', False),
                "analysis_time_seconds": round(elapsed, 2),
                "timestamp": datetime.now().isoformat(),
                "full_result": result
            }
            
            print(f" Análisis completado en {elapsed:.1f}s")
            print(f"\n RESULTADOS:")
            print(f"   Ambiente detectado: {metrics['environment_detected']} ({metrics['environment_confidence']:.1%})")
            print(f"   Probabilidad arqueológica: {metrics['archaeological_probability']:.1%}")
            print(f"   Instrumentos: {metrics['instruments_measuring']}/{metrics['instruments_total']}")
            print(f"   Convergencia: {' SÍ' if metrics['convergence_achieved'] else ' NO'}")
            print(f"   Análisis temporal: {' SÍ' if metrics['temporal_analysis'] else ' NO'}")
            print(f"   IA disponible: {' SÍ' if metrics['ai_available'] else ' NO'}")
            
            return metrics
            
        else:
            print(f" Error HTTP {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}")
            return None
            
    except requests.Timeout:
        print(f"  Timeout después de 120s")
        return None
    except Exception as e:
        print(f" Error: {e}")
        return None


def save_to_database(metrics: Dict[str, Any]) -> bool:
    """
    Guardar resultados en BD
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        # Crear tabla si no existe
        cur.execute("""
            CREATE TABLE IF NOT EXISTS archaeological_candidate_analyses (
                id SERIAL PRIMARY KEY,
                candidate_id VARCHAR(100) NOT NULL,
                candidate_name VARCHAR(255) NOT NULL,
                region VARCHAR(255),
                environment_detected VARCHAR(50),
                environment_confidence FLOAT,
                archaeological_probability FLOAT,
                confidence FLOAT,
                result_type VARCHAR(50),
                instruments_measuring INTEGER,
                instruments_total INTEGER,
                convergence_achieved BOOLEAN,
                temporal_analysis BOOLEAN,
                ai_available BOOLEAN,
                analysis_time_seconds FLOAT,
                timestamp TIMESTAMP,
                full_result JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insertar resultado (manejar valores None correctamente)
        cur.execute("""
            INSERT INTO archaeological_candidate_analyses (
                candidate_id, candidate_name, region,
                environment_detected, environment_confidence,
                archaeological_probability, confidence, result_type,
                instruments_measuring, instruments_total,
                convergence_achieved, temporal_analysis, ai_available,
                analysis_time_seconds, timestamp, full_result
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            metrics['candidate_id'],
            metrics['candidate_name'],
            metrics['region'],
            metrics['environment_detected'],
            metrics['environment_confidence'],
            metrics['archaeological_probability'],
            metrics['confidence'] if metrics['confidence'] != 'none' else None,
            metrics['result_type'],
            metrics['instruments_measuring'],
            metrics['instruments_total'],
            metrics['convergence_achieved'],
            metrics['temporal_analysis'],
            metrics['ai_available'],
            metrics['analysis_time_seconds'],
            metrics['timestamp'],
            json.dumps(metrics['full_result'])
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f" Guardado en BD: {metrics['candidate_name']}")
        return True
        
    except Exception as e:
        print(f" Error guardando en BD: {e}")
        if conn:
            conn.close()
        return False


def generate_comparative_report(all_results: List[Dict[str, Any]]) -> str:
    """
    Generar reporte comparativo de todos los candidatos
    """
    report = []
    report.append("\n" + "="*80)
    report.append("REPORTE COMPARATIVO - CANDIDATOS ARQUEOLOGICOS")
    report.append("="*80 + "\n")
    
    # Resumen general
    report.append(f"Total candidatos analizados: {len(all_results)}")
    report.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Tabla comparativa
    report.append("┌" + "─"*78 + "┐")
    report.append(f"│ {'Candidato':<35} │ {'Prob%':<6} │ {'Inst':<5} │ {'Conv':<5} │ {'Tiempo':<8} │")
    report.append("├" + "─"*78 + "┤")
    
    for result in all_results:
        name = result['candidate_name'][:35]
        prob = f"{result['archaeological_probability']*100:.1f}%"
        inst = f"{result['instruments_measuring']}/{result['instruments_total']}"
        conv = "" if result['convergence_achieved'] else ""
        time_str = f"{result['analysis_time_seconds']:.1f}s"
        
        report.append(f"│ {name:<35} │ {prob:<6} │ {inst:<5} │ {conv:<5} │ {time_str:<8} │")
    
    report.append("└" + "─"*78 + "┘\n")
    
    # Estadísticas
    avg_prob = sum(r['archaeological_probability'] for r in all_results) / len(all_results)
    avg_time = sum(r['analysis_time_seconds'] for r in all_results) / len(all_results)
    convergence_count = sum(1 for r in all_results if r['convergence_achieved'])
    
    report.append("ESTADISTICAS:")
    report.append(f"   Probabilidad promedio: {avg_prob*100:.1f}%")
    report.append(f"   Tiempo promedio: {avg_time:.1f}s")
    report.append(f"   Convergencia alcanzada: {convergence_count}/{len(all_results)}")
    
    # Ranking por probabilidad
    report.append("\nRANKING POR PROBABILIDAD ARQUEOLOGICA:")
    sorted_results = sorted(all_results, key=lambda x: x['archaeological_probability'], reverse=True)
    for i, result in enumerate(sorted_results, 1):
        report.append(f"   {i}. {result['candidate_name']}: {result['archaeological_probability']*100:.1f}%")
    
    # Ambientes detectados
    report.append("\nAMBIENTES DETECTADOS:")
    environments = {}
    for result in all_results:
        env = result['environment_detected']
        if env not in environments:
            environments[env] = []
        environments[env].append(result['candidate_name'])
    
    for env, sites in environments.items():
        report.append(f"   {env}: {len(sites)} sitios")
        for site in sites:
            report.append(f"      - {site}")
    
    report.append("\n" + "="*80)
    
    return "\n".join(report)


def main():
    """
    Ejecutar análisis batch de todos los candidatos
    """
    print("\n" + "="*80)
    print("ARCHEOSCOPE - ANALISIS BATCH DE CANDIDATOS ARQUEOLOGICOS")
    print("="*80)
    print(f"\nTotal candidatos: {len(ARCHAEOLOGICAL_CANDIDATES)}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_results = []
    
    for i, candidate in enumerate(ARCHAEOLOGICAL_CANDIDATES, 1):
        print(f"\n[{i}/{len(ARCHAEOLOGICAL_CANDIDATES)}] Procesando: {candidate['name']}")
        
        # Analizar
        metrics = analyze_candidate(candidate)
        
        if metrics:
            all_results.append(metrics)
            
            # Guardar en BD
            save_to_database(metrics)
            
            # Guardar JSON individual
            filename = f"candidate_analysis_{candidate['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2, ensure_ascii=False)
            print(f" JSON guardado: {filename}")
        
        # Pausa entre análisis
        if i < len(ARCHAEOLOGICAL_CANDIDATES):
            print(f"\n  Pausa de 3s antes del siguiente análisis...")
            time.sleep(3)
    
    # Generar reporte comparativo
    if all_results:
        report = generate_comparative_report(all_results)
        print(report)
        
        # Guardar reporte
        report_filename = f"comparative_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n Reporte guardado: {report_filename}")
        
        # Guardar JSON consolidado
        consolidated_filename = f"all_candidates_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(consolidated_filename, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f" JSON consolidado: {consolidated_filename}")
    
    print(f"\n Análisis batch completado!")
    print(f"   Candidatos analizados: {len(all_results)}/{len(ARCHAEOLOGICAL_CANDIDATES)}")
    print(f"   Resultados guardados en BD y archivos JSON\n")


if __name__ == "__main__":
    main()
