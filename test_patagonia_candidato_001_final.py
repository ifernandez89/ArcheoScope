#!/usr/bin/env python3
"""
Test Patagonia Candidato #001 - Análisis Completo
Sistema optimizado con SAR deshabilitado por defecto
"""

import sys
import os

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import requests
import json
from datetime import datetime

def test_patagonia_candidato_001():
    """Test completo del candidato Patagonia #001"""
    
    print("=" * 80)
    print("TEST PATAGONIA CANDIDATO #001 - ANALISIS COMPLETO")
    print("=" * 80)
    print()
    
    # Coordenadas del candidato
    data = {
        "lat_min": -50.55,
        "lat_max": -50.40,
        "lon_min": -73.15,
        "lon_max": -72.90,
        "region_name": "Patagonia Candidato #001"
    }
    
    print(f"Region: {data['region_name']}")
    print(f"Centro: -50.4760, -73.0450")
    print(f"Bbox: {data['lat_min']}, {data['lat_max']}, {data['lon_min']}, {data['lon_max']}")
    print(f"Area: ~35 x 20 km")
    print()
    print("Instrumentos esperados:")
    print("  - MODIS LST (termico)")
    print("  - NSIDC (hielo)")
    print("  - OpenTopography (DEM)")
    print("  - Sentinel-2 (multispectral)")
    print("  - Landsat (termico)")
    print("  - ICESat-2 (altimetria)")
    print("  - SMAP (humedad)")
    print("  - Copernicus Marine (hielo marino)")
    print("  - Sentinel-1 SAR (DESHABILITADO por defecto)")
    print()
    print("-" * 80)
    print("Iniciando analisis...")
    print("-" * 80)
    print()
    
    start_time = datetime.now()
    
    try:
        response = requests.post(
            "http://localhost:8002/analyze",
            json=data,
            timeout=180  # 3 minutos max
        )
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if response.status_code == 200:
            result = response.json()
            
            # Guardar resultado completo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"patagonia_candidato_001_final_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print("=" * 80)
            print("RESULTADO DEL ANALISIS")
            print("=" * 80)
            print()
            
            # Información básica
            print(f"Tiempo total: {elapsed:.1f}s")
            print(f"Region: {result.get('region_name', 'N/A')}")
            print()
            
            # Contexto espacial
            spatial = result.get('spatial_context', {})
            print(f"CONTEXTO ESPACIAL:")
            print(f"  Area: {spatial.get('area_km2', 0):.1f} km2")
            print(f"  Modo: {spatial.get('analysis_mode', 'N/A')}")
            print(f"  Resolucion: {spatial.get('resolution_m', 0)}m")
            print()
            
            # Ambiente detectado
            env = result.get('environment_classification', {})
            if env:
                print(f"AMBIENTE DETECTADO:")
                print(f"  Tipo: {env.get('environment_type', 'N/A')}")
                print(f"  Confianza: {env.get('confidence', 0)*100:.1f}%")
                print()
            
            # Instrumentos
            instruments = result.get('instrumental_measurements', {})
            if instruments:
                measurements = instruments.get('measurements', {})
                print(f"INSTRUMENTOS:")
                print(f"  Total disponibles: {instruments.get('total_instruments', 0)}")
                print(f"  Midiendo: {instruments.get('instruments_measuring', 0)}")
                print(f"  Convergencia: {instruments.get('convergence_count', 0)}/{instruments.get('convergence_required', 0)}")
                print()
                
                if measurements:
                    print(f"MEDICIONES:")
                    for key, value in measurements.items():
                        if isinstance(value, dict):
                            val = value.get('value', 'N/A')
                            unit = value.get('unit', '')
                            threshold = value.get('threshold', 'N/A')
                            print(f"  - {key}: {val} {unit} (umbral: {threshold})")
                        else:
                            print(f"  - {key}: {value}")
                    print()
            
            # Resultado arqueológico
            arch = result.get('archaeological_results', {})
            if arch:
                print(f"RESULTADO ARQUEOLOGICO:")
                print(f"  Tipo: {arch.get('result_type', 'N/A')}")
                print(f"  Confianza: {arch.get('confidence', 'N/A')}")
                print(f"  Probabilidad: {arch.get('archaeological_probability', 0)*100:.1f}%")
                print(f"  Pixeles afectados: {arch.get('affected_pixels', 0)}")
                print()
            
            # Capas de evidencia
            layers = result.get('evidence_layers', [])
            if layers:
                print(f"CAPAS DE EVIDENCIA: {len(layers)}")
                for layer in layers:
                    print(f"  - {layer.get('layer_name', 'N/A')}: {layer.get('description', 'N/A')}")
                print()
            
            # Validación
            validation = result.get('validation_metrics', {})
            if validation:
                print(f"VALIDACION:")
                print(f"  Consistencia: {validation.get('consistency_score', 0)*100:.1f}%")
                print(f"  Cobertura: {validation.get('data_coverage', 0)*100:.1f}%")
                print()
            
            # AI Explanation
            ai = result.get('ai_explanations', {})
            if ai and ai.get('ai_available'):
                print(f"EXPLICACION IA:")
                print(f"  {ai.get('explanation', 'N/A')}")
                print()
            
            print("=" * 80)
            print(f"Resultado guardado en: {filename}")
            print("=" * 80)
            print()
            
            # Resumen ejecutivo
            print("RESUMEN EJECUTIVO:")
            print()
            
            prob = arch.get('archaeological_probability', 0) * 100
            conv = instruments.get('convergence_count', 0)
            conv_req = instruments.get('convergence_required', 0)
            measuring = instruments.get('instruments_measuring', 0)
            
            if prob >= 70 and conv >= conv_req:
                print("RESULTADO: ANOMALIA ARQUEOLOGICA PROBABLE")
                print(f"  Probabilidad: {prob:.1f}%")
                print(f"  Convergencia: {conv}/{conv_req} instrumentos")
                print(f"  Recomendacion: INVESTIGACION DETALLADA")
            elif prob >= 50:
                print("RESULTADO: ANOMALIA DETECTADA")
                print(f"  Probabilidad: {prob:.1f}%")
                print(f"  Convergencia: {conv}/{conv_req} instrumentos")
                print(f"  Recomendacion: ANALISIS ADICIONAL")
            elif measuring < 3:
                print("RESULTADO: ANALISIS INCONCLUSO")
                print(f"  Instrumentos midiendo: {measuring}")
                print(f"  Razon: Cobertura instrumental insuficiente")
                print(f"  Recomendacion: Verificar disponibilidad de datos")
            else:
                print("RESULTADO: NO SE DETECTA ANOMALIA")
                print(f"  Probabilidad: {prob:.1f}%")
                print(f"  Convergencia: {conv}/{conv_req} instrumentos")
                print(f"  Recomendacion: Region natural sin anomalias")
            
            print()
            print(f"Tiempo de analisis: {elapsed:.1f}s")
            print()
            
            return True
            
        else:
            print(f"ERROR: HTTP {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"ERROR: Timeout despues de {elapsed:.1f}s")
        return False
        
    except Exception as e:
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_patagonia_candidato_001()
    exit(0 if success else 1)
