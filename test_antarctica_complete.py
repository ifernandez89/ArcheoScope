#!/usr/bin/env python3
"""
Test completo de coordenadas de Antártida
Verifica instrumentos usados, resultados y registro en BD
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import asyncpg
import json
from datetime import datetime

load_dotenv()

# Configurar PROJ
proj_path = Path(r"C:\Users\xiphos-pc1\AppData\Roaming\Python\Python311\site-packages\rasterio\proj_data")
os.environ['PROJ_LIB'] = str(proj_path)
os.environ['PROJ_DATA'] = str(proj_path)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import requests

async def test_antarctica_complete():
    """Test completo de análisis en Antártida"""
    
    # Coordenadas
    lat = -75.69969950817202
    lon = -111.35296997427601
    
    print("="*80)
    print("TEST COMPLETO - ANTARTIDA")
    print("="*80)
    print()
    print(f"Coordenadas: {lat}, {lon}")
    print(f"Ubicacion: Antartida Occidental")
    print()
    
    # Crear bounding box pequeño
    delta = 0.05
    lat_min = lat - delta
    lat_max = lat + delta
    lon_min = lon - delta
    lon_max = lon + delta
    
    print(f"Bounding box: [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
    print()
    
    # Conectar a BD para verificar mediciones ANTES
    database_url = os.getenv("DATABASE_URL")
    conn = await asyncpg.connect(database_url)
    
    count_before = await conn.fetchval("SELECT COUNT(*) FROM measurements")
    print(f"Mediciones en BD ANTES: {count_before}")
    print()
    
    # Hacer request al backend
    print("="*80)
    print("ENVIANDO REQUEST AL BACKEND")
    print("="*80)
    print()
    
    test_data = {
        "lat_min": lat_min,
        "lat_max": lat_max,
        "lon_min": lon_min,
        "lon_max": lon_max,
        "region_name": "Antartida Test"
    }
    
    try:
        print("Esperando respuesta del backend...")
        start_time = datetime.now()
        
        response = requests.post(
            "http://localhost:8002/analyze",
            json=test_data,
            timeout=60
        )
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        print(f"Status: {response.status_code}")
        print(f"Tiempo: {elapsed:.2f} segundos")
        print()
        
        if response.status_code == 200:
            result = response.json()
            
            # Guardar resultado completo
            output_file = f"antarctica_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print("="*80)
            print("RESULTADO DEL ANALISIS")
            print("="*80)
            print()
            
            # Contexto espacial
            spatial = result.get('spatial_context', {})
            print("CONTEXTO ESPACIAL:")
            print(f"  Area: {spatial.get('area_km2', 0):.2f} km2")
            print(f"  Ambiente: {spatial.get('environment_type', 'N/A')}")
            print(f"  Confianza ambiente: {spatial.get('environment_confidence', 0):.2%}")
            print()
            
            # Resultados arqueológicos
            arch = result.get('archaeological_results', {})
            print("RESULTADOS ARQUEOLOGICOS:")
            print(f"  Tipo: {arch.get('result_type', 'N/A')}")
            print(f"  Probabilidad: {arch.get('archaeological_probability', 0):.2%}")
            print(f"  Confianza: {arch.get('confidence_level', 'N/A')}")
            print(f"  Mediciones: {arch.get('measurements_count', 0)}")
            print(f"  Instrumentos convergiendo: {arch.get('instruments_converging', 0)}/{arch.get('minimum_required', 0)}")
            print()
            
            # Mediciones instrumentales
            measurements = arch.get('measurements', [])
            if measurements:
                print("INSTRUMENTOS USADOS:")
                for m in measurements:
                    print(f"  - {m.get('instrument_name', 'N/A')}")
                    print(f"    Valor: {m.get('value', 0):.3f} {m.get('unit', '')}")
                    print(f"    Umbral: {m.get('threshold', 0):.3f}")
                    print(f"    Excede: {'SI' if m.get('exceeds_threshold') else 'NO'}")
                    print(f"    Confianza: {m.get('confidence', 'N/A')}")
                    print()
            else:
                print("INSTRUMENTOS USADOS: Ninguno (0 mediciones)")
                print()
            
            # Sitio conocido
            if arch.get('known_site_nearby'):
                print("SITIO CONOCIDO:")
                print(f"  Nombre: {arch.get('known_site_name', 'N/A')}")
                print(f"  Distancia: {arch.get('known_site_distance_km', 0):.2f} km")
                print()
            
            # IA
            ai = result.get('ai_explanations', {})
            if ai.get('ai_available'):
                print("ANALISIS IA:")
                print(f"  {ai.get('explanation', 'N/A')[:200]}...")
                print()
            
            print(f"Resultado completo guardado en: {output_file}")
            print()
            
        else:
            print(f"ERROR: Status {response.status_code}")
            print(response.text[:500])
            return False
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Verificar mediciones en BD DESPUES
    print("="*80)
    print("VERIFICANDO BASE DE DATOS")
    print("="*80)
    print()
    
    count_after = await conn.fetchval("SELECT COUNT(*) FROM measurements")
    new_measurements = count_after - count_before
    
    print(f"Mediciones en BD DESPUES: {count_after}")
    print(f"Nuevas mediciones registradas: {new_measurements}")
    print()
    
    if new_measurements > 0:
        # Obtener las últimas mediciones
        recent = await conn.fetch("""
            SELECT 
                instrument_name,
                measurement_type,
                value,
                unit,
                source,
                data_mode,
                confidence,
                exceeds_threshold,
                anomaly_detected,
                created_at
            FROM measurements
            ORDER BY created_at DESC
            LIMIT $1
        """, new_measurements)
        
        print("MEDICIONES REGISTRADAS EN BD:")
        for i, m in enumerate(recent, 1):
            print(f"\n  {i}. {m['instrument_name']} ({m['measurement_type']})")
            print(f"     Valor: {m['value']} {m['unit']}")
            print(f"     Fuente: {m['source']}")
            print(f"     Data mode: {m['data_mode']}")
            print(f"     Confianza: {m['confidence']:.2%}" if m['confidence'] else "     Confianza: N/A")
            print(f"     Excede umbral: {'SI' if m['exceeds_threshold'] else 'NO'}")
            print(f"     Anomalia: {'SI' if m['anomaly_detected'] else 'NO'}")
            print(f"     Timestamp: {m['created_at']}")
    else:
        print("ADVERTENCIA: No se registraron mediciones en la BD")
        print("Esto puede indicar que los instrumentos no funcionaron")
    
    await conn.close()
    
    print()
    print("="*80)
    print("TEST COMPLETADO")
    print("="*80)
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_antarctica_complete())
    exit(0 if success else 1)
