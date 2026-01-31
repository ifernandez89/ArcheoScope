#!/usr/bin/env python3
"""
Test de 4 zonas - REPORTE FINAL
================================

Testea 4 zonas y genera reporte comparativo completo
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.geoglyph_detector import GeoglyphDetector, DetectionMode
import numpy as np
import json
from datetime import datetime

def test_4_zonas():
    """Testear 4 zonas solicitadas"""
    
    zonas = [
        {
            'numero': 1,
            'nombre': 'Harrat Khaybar',
            'lat': 25.0,
            'lon': 39.9,
            'descripcion': 'Campo volcánico con estructuras reportadas',
            'region': 'Arabia Central'
        },
        {
            'numero': 2,
            'nombre': 'Sur Harrat Uwayrid',
            'lat': 26.5,
            'lon': 38.5,
            'descripcion': 'Basalto antiguo, baja intervención moderna',
            'region': 'Arabia Central'
        },
        {
            'numero': 3,
            'nombre': 'Límite Arabia-Jordania',
            'lat': 29.5,
            'lon': 37.5,
            'descripcion': 'Paleorutas, ausencia de papers',
            'region': 'Arabia Norte'
        },
        {
            'numero': 4,
            'nombre': 'Interior Rub al Khali',
            'lat': 20.5,
            'lon': 51.0,
            'descripcion': 'Bordes del desierto vacío (NO centro)',
            'region': 'Arabia Sur'
        }
    ]
    
    resultados = []
    
    print("\n" + "="*90)
    print("🔍 ARCHEOSCOPE - TEST DE 4 ZONAS (POST-AJUSTES METODOLÓGICOS)")
    print("="*90)
    
    for zona in zonas:
        print(f"\n{'─'*90}")
        print(f"[{zona['numero']}/4] 📍 {zona['nombre']}")
        print(f"{'─'*90}")
        print(f"Región: {zona['region']}")
        print(f"Coords: {zona['lat']:.2f}°N, {zona['lon']:.2f}°E")
        print(f"Descripción: {zona['descripcion']}")
        
        # Inicializar detector en modo Explorador
        detector = GeoglyphDetector(mode=DetectionMode.EXPLORER)
        
        # Definir bbox
        lat_min = zona['lat'] - 0.05
        lat_max = zona['lat'] + 0.05
        lon_min = zona['lon'] - 0.05
        lon_max = zona['lon'] + 0.05
        
        # DEM simulado (en producción vendría de SRTM)
        dem_data = np.random.rand(100, 100) * 100
        
        # DETECTAR
        print("\n⏳ Ejecutando detección...")
        result = detector.detect_geoglyph(
            lat=zona['lat'],
            lon=zona['lon'],
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max,
            dem_data=dem_data,
            resolution_m=1.0
        )
        
        # Mostrar resultados
        print(f"\n✅ RESULTADO:")
        print(f"├─ Tipo: {result.geoglyph_type.value.upper()}")
        print(f"├─ Confianza tipo: {result.type_confidence:.1%}")
        print(f"├─ Cultural Score: {result.cultural_score:.2%}")
        print(f"├─ Orientación: {result.orientation.azimuth_deg:.1f}°")
        print(f"├─ Aspect Ratio: {result.orientation.aspect_ratio:.2f}")
        print(f"├─ Simetría bilateral: {(1-result.orientation.bilateral_symmetry)*100:.1f}%")
        print(f"├─ 🆕 Asimetría Funcional: {result.orientation.functional_asymmetry:.2%}")
        print(f"├─ Eje Mayor: {result.orientation.major_axis_length_m:.1f}m")
        print(f"├─ Eje Menor: {result.orientation.minor_axis_length_m:.1f}m")
        print(f"├─ Tail Slope Dev: {result.orientation.tail_slope_deviation:.1f}°")
        print(f"├─ Distal Erosion: {result.orientation.distal_erosion_ratio:.2f}")
        print(f"└─ Axis Offset: {result.orientation.axis_offset_m:.1f}m")
        
        # Guardar resultado
        resultado_dict = {
            'numero': zona['numero'],
            'zona': zona['nombre'],
            'region': zona['region'],
            'lat': zona['lat'],
            'lon': zona['lon'],
            'tipo': result.geoglyph_type.value,
            'confianza_tipo': float(result.type_confidence),
            'cultural_score': float(result.cultural_score),
            'orientacion_deg': float(result.orientation.azimuth_deg),
            'aspect_ratio': float(result.orientation.aspect_ratio),
            'simetria_pct': float((1 - result.orientation.bilateral_symmetry) * 100),
            'asimetria_funcional': float(result.orientation.functional_asymmetry),
            'eje_mayor_m': float(result.orientation.major_axis_length_m),
            'eje_menor_m': float(result.orientation.minor_axis_length_m),
            'tail_slope_deviation': float(result.orientation.tail_slope_deviation),
            'distal_erosion_ratio': float(result.orientation.distal_erosion_ratio),
            'axis_offset_m': float(result.orientation.axis_offset_m),
            'transicion_sedimento': result.paleo_hydrology.on_sediment_transition if result.paleo_hydrology else False,
            'dist_wadi_km': float(result.paleo_hydrology.distance_to_wadi_km) if result.paleo_hydrology else 0.0,
            'superficie_estable': result.volcanic_context.on_stable_surface if result.volcanic_context else False,
            'timestamp': datetime.now().isoformat()
        }
        
        resultados.append(resultado_dict)
    
    # Guardar JSON
    timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'REPORTE_FINAL_4_ZONAS_{timestamp_file}.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'test_info': {
                'fecha': datetime.now().isoformat(),
                'version': '2.0 (Post-ajustes metodológicos)',
                'modo': 'Explorer',
                'zonas_testeadas': 4
            },
            'resultados': resultados
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{' ='*90}")
    print("📊 ANÁLISIS COMPARATIVO FINAL")
    print(f"{'='*90}\n")
    
    # Tabla comparativa
    print("| # | Zona | Cultural | Tipo | Orient° | Aspect | Simᵃ | AsimFunc |")
    print("|---|------|----------|------|---------|--------|------|----------|")
    
    for r in resultados:
        print(f"| {r['numero']} | {r['zona'][:20]:20} | {r['cultural_score']:6.1%} | {r['tipo']:8} | {r['orientacion_deg']:6.1f}° | {r['aspect_ratio']:4.2f} | {r['simetria_pct']:4.1f}% | {r['asimetria_funcional']:6.2%} |")
    
    # Estadísticas
    print(f"\n📈 ESTADÍSTICAS DE VARIABILIDAD:\n")
    
    scores = [r['cultural_score'] for r in resultados]
    print(f"Cultural Score:")
    print(f"  └─ Promedio: {sum(scores)/len(scores):.2%}")
    print(f"  └─ Rango: {min(scores):.2%} - {max(scores):.2%}")
    print(f"  └─ Variación: ±{(max(scores)-min(scores))/2*100:.1f}%")
    
    orientaciones = [r['orientacion_deg'] for r in resultados]
    print(f"\nOrientación:")
    print(f"  └─ Promedio: {sum(orientaciones)/len(orientaciones):.1f}°")
    print(f"  └─ Rango: {min(orientaciones):.1f}° - {max(orientaciones):.1f}°")
    print(f"  └─ Variación: ±{(max(orientaciones)-min(orientaciones))/2:.1f}°")
    
    asimetrias = [r['asimetria_funcional'] for r in resultados]
    print(f"\n🆕 Asimetría Funcional:")
    print(f"  └─ Promedio: {sum(asimetrias)/len(asimetrias):.2%}")
    print(f"  └─ Rango: {min(asimetrias):.2%} - {max(asimetrias):.2%}")
    
    aspects = [r['aspect_ratio'] for r in resultados]
    print(f"\nAspect Ratio:")
    print(f"  └─ Promedio: {sum(aspects)/len(aspects):.2f}")
    print(f"  └─ Rango: {min(aspects):.2f} - {max(aspects):.2f}")
    
    # Evaluación de variabilidad
    print(f"\n🎯 EVALUACIÓN DE CLONACIÓN MÉTRICA:\n")
    
    score_var = max(scores) - min(scores)
    orient_var = max(orientaciones) - min(orientaciones)
    asim_var = max(asimetrias) - min(asimetrias)
    
    if score_var > 0.05:
        print("✅ Cultural Score: Buena variabilidad (NO clonación)")
    else:
        print("⚠️  Cultural Score: Baja variabilidad")
    
    if orient_var > 5.0:
        print("✅ Orientación: Buena variabilidad (±{:.1f}°)".format(orient_var/2))
    else:
        print("⚠️  Orientación: Baja variabilidad")
    
    if asim_var > 0.05:
        print("✅ Asimetría Funcional: Buena variabilidad")
    else:
        print("⚠️  Asimetría Funcional: Baja variabilidad")
    
    # Conclusiones
    print(f"\n🏆 CONCLUSIONES:\n")
    
    # Tipo más común
    tipos = [r['tipo'] for r in resultados]
    tipo_comun = max(set(tipos), key=tipos.count)
    print(f"1. Tipo predominante: {tipo_comun.upper()} ({tipos.count(tipo_comun)}/4 zonas)")
    
    # Pattern coherence
    nw_se_count = sum(1 for o in orientaciones if 300 <= o <= 330)
    print(f"2. Orientación NW-SE: {nw_se_count}/4 zonas ({nw_se_count/4*100:.0f}%)")
    
    # High scores    
    high_scores = sum(1 for s in scores if s >= 0.70)
    print(f"3. Cultural Score ≥70%: {high_scores}/4 zonas")
    
    # Transición sedimento
    transiciones = sum(1 for r in resultados if r['transicion_sedimento'])
    print(f"4. Transición roca-sedimento: {transiciones}/4 zonas (🏆 ORO)")
    
    print(f"\n💾 Reporte guardado en: {filename}")
    print(f"\n{'='*90}\n")
    
    return resultados, filename


if __name__ == "__main__":
    test_4_zonas()
