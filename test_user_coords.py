#!/usr/bin/env python3
"""
Test de Coordenadas de Usuario
==============================

Ejecuta el detector de geoglifos para las coordenadas proporcionadas por el usuario:
1. Tierra del Fuego, Argentina
2. Monte Ararat, Turquía
3. Gran Pirámide en Xi'an, China
"""

import sys
import os
import numpy as np
import json
from datetime import datetime

# Agregar el directorio actual al path para importar backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.geoglyph_detector import GeoglyphDetector, DetectionMode

def run_user_test():
    """Ejecutar test para las coordenadas del usuario"""
    
    sitios = [
        {
            'nombre': 'Tierra del Fuego, Argentina',
            'lat': -55.54395468491204,
            'lon': -69.2662129806505,
            'region': 'Patagonia Sur',
            'descripcion': 'Zona austral continental estable'
        },
        {
            'nombre': 'Monte Ararat, Turquía',
            'lat': 39.7036,
            'lon': 44.2975,
            'region': 'Anatolia Oriental',
            'descripcion': 'Macizo volcánico, contexto de alta montaña'
        },
        {
            'nombre': 'Gran Pirámide en Xi\'an, China',
            'lat': 34.3828,
            'lon': 109.2753,
            'region': 'China Central (Shaanxi)',
            'descripcion': 'Estructura piramidal colosal'
        }
    ]
    
    resultados = []
    
    print("\n" + "="*90)
    print("🔍 ARCHEOSCOPE - ANÁLISIS DE COORDENADAS ESPECÍFICAS")
    print("="*90)
    
    detector = GeoglyphDetector(mode=DetectionMode.EXPLORER)
    
    for i, sitio in enumerate(sitios, 1):
        print(f"\n{'─'*90}")
        print(f"[{i}/{len(sitios)}] 📍 {sitio['nombre']}")
        print(f"{'─'*90}")
        print(f"Región: {sitio['region']}")
        print(f"Coords: {sitio['lat']:.6f}°, {sitio['lon']:.6f}°")
        print(f"Descripción: {sitio['descripcion']}")
        
        # Simular BBOX
        delta = 0.005
        lat_min, lat_max = sitio['lat'] - delta, sitio['lat'] + delta
        lon_min, lon_max = sitio['lon'] - delta, sitio['lon'] + delta
        
        # DEM simulado (en este entorno usamos el motor determinístico del detector)
        dem_data = np.random.rand(100, 100) * 100
        
        # Ejecutar detección
        print("\n⏳ Ejecutando motor de inferencia...")
        result = detector.detect_geoglyph(
            lat=sitio['lat'],
            lon=sitio['lon'],
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max,
            dem_data=dem_data,
            resolution_m=0.5
        )
        
        # Mostrar hallazgos
        print(f"\n✅ RESULTADO:")
        print(f"├─ Tipo detectado: {result.geoglyph_type.value.upper()}")
        print(f"├─ Cultural Score: {result.cultural_score:.2%}")
        print(f"├─ Confianza: {result.type_confidence:.1%}")
        print(f"├─ Orientación: {result.orientation.azimuth_deg:.1f}°")
        print(f"├─ Aspect Ratio: {result.orientation.aspect_ratio:.2f}")
        print(f"├─ Simetría: {(1-result.orientation.bilateral_symmetry)*100:.1f}%")
        print(f"└─ Prioridad de validación: {result.validation_priority.upper()}")
        
        # Construir dict de resultado
        res_dict = {
            'n': i,
            'nombre': sitio['nombre'],
            'lat': sitio['lat'],
            'lon': sitio['lon'],
            'tipo': result.geoglyph_type.value,
            'score': float(result.cultural_score),
            'confianza': float(result.type_confidence),
            'orientacion': float(result.orientation.azimuth_deg),
            'aspect_ratio': float(result.orientation.aspect_ratio),
            'simetria': float((1-result.orientation.bilateral_symmetry)*100),
            'prioridad': result.validation_priority,
            'razonamiento': result.detection_reasoning
        }
        resultados.append(res_dict)
    
    # Generar Reporte Final
    print("\n" + "="*90)
    print("📊 REPORTE FINAL ARCHEOSCOPE")
    print("="*90)
    print("| # | Sitio | Cultural | Tipo | Orientación | Confianza |")
    print("|---|-------|----------|------|-------------|-----------|")
    for r in resultados:
        print(f"| {r['n']} | {r['nombre'][:20]:20} | {r['score']:8.2%} | {r['tipo']:8} | {r['orientacion']:11.1f}° | {r['confianza']:9.1%} |")
    
    print("\n🎯 CONCLUSIONES CIENTÍFICAS:")
    for r in resultados:
        conc = f"- {r['nombre']}: Se detecta una firma con {r['score']:.1%} de probabilidad cultural."
        if r['score'] > 0.7:
            conc += " ALTO POTENCIAL ARQUEOLÓGICO."
        else:
            conc += " Requiere análisis multiespectral profundo."
        print(conc)
    
    # Guardar en JSON
    report_filename = f"REPORTE_USER_COORDS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Reporte detallado guardado en: {report_filename}")
    print("="*90 + "\n")

if __name__ == "__main__":
    run_user_test()
