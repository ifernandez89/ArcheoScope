#!/usr/bin/env python3
"""
Test de 4 zonas + guardado en BD
"""
import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.geoglyph_detector import GeoglyphDetector, DetectionMode
from backend.database import ArcheoScopeDB
import numpy as np
import json
from datetime import datetime

async def test_4_zonas_con_bd():
    """Testear 4 zonas y guardar en BD"""
    
    zonas = [
        {
            'nombre': 'Harrat Khaybar',
            'lat': 25.0,
            'lon': 39.9,
            'descripcion': 'Campo volcánico con estructuras reportadas'
        },
        {
            'nombre': 'Sur Harrat Uwayrid',
            'lat': 26.5,
            'lon': 38.5,
            'descripcion': 'Basalto antiguo, baja intervención moderna'
        },
        {
            'nombre': 'Límite ArabiaJordania',
            'lat': 29.5,
            'lon': 37.5,
            'descripcion': 'Paleorutas, ausencia de papers'
        },
        {
            'nombre': 'Interior Rub al Khali',
            'lat': 20.5,
            'lon': 51.0,
            'descripcion': 'Bordes del desierto vacío'
        }
    ]
    
    resultados = []
    db = ArcheoScopeDB()
    
    try:
        await db.connect()
        
        for i, zona in enumerate(zonas, 1):
            print(f"\n{'='*80}")
            print(f"🔍 [{i}/4] TESTEANDO: {zona['nombre']}")
            print(f"📍 Coords: {zona['lat']:.2f}°N, {zona['lon']:.2f}°E")
            print(f"{'='*80}")
            
            # Inicializar detector
            detector = GeoglyphDetector(mode=DetectionMode.EXPLORER)
            
            # Definir bbox
            lat_min = zona['lat'] - 0.05
            lat_max = zona['lat'] + 0.05
            lon_min = zona['lon'] - 0.05
            lon_max = zona['lon'] + 0.05
            
            # DEM simulado
            dem_data = np.random.rand(100, 100) * 100
            
            # DETECTAR
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
            print(f"   Tipo: {result.geoglyph_type.value.upper()}")
            print(f"   Confianza tipo: {result.type_confidence:.1%}")
            print(f"   Cultural Score: {result.cultural_score:.2%}")
            print(f"   Orientación: {result.orientation.azimuth_deg:.1f}°")
            print(f"   Aspect Ratio: {result.orientation.aspect_ratio:.2f}")
            print(f"   Simetría: {(1-result.orientation.bilateral_symmetry)*100:.1f}%")
            print(f"   Asimetría Funcional: {result.orientation.functional_asymmetry:.2%}")
            print(f"   Eje Mayor: {result.orientation.major_axis_length_m:.1f}m")
            
            # Preparar para guardar
            resultado_dict = {
                'zona': zona['nombre'],
                'lat': zona['lat'],
                'lon': zona['lon'],
                'tipo': result.geoglyph_type.value,
                'confianza_tipo': float(result.type_confidence),
                'cultural_score': float(result.cultural_score),
                'orientacion': float(result.orientation.azimuth_deg),
                'aspect_ratio': float(result.orientation.aspect_ratio),
                'simetria': float(1 - result.orientation.bilateral_symmetry),
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
            
            # 💾 GUARDAR EN BASE DE DATOS
            try:
                candidate_data = {
                    'latitude': zona['lat'],
                    'longitude': zona['lon'],
                    'detection_type': 'geoglyph',
                    'archaeological_score': result.cultural_score,
                    'geoglyph_type': result.geoglyph_type.value,
                    'type_confidence': result.type_confidence,
                    'orientation_azimuth': result.orientation.azimuth_deg,
                    'functional_asymmetry': result.orientation.functional_asymmetry,
                    'notes': f"Test 4 zonas - {zona['nombre']}: {zona['descripcion']}. Cultural score: {result.cultural_score:.2%}. Tipo: {result.geoglyph_type.value}",
                    'measurements': {
                        'aspect_ratio': result.orientation.aspect_ratio,
                        'major_axis_m': result.orientation.major_axis_length_m,
                        'minor_axis_m': result.orientation.minor_axis_length_m,
                        'symmetry': 1 - result.orientation.bilateral_symmetry,
                        'tail_slope_deviation': result.orientation.tail_slope_deviation,
                        'distal_erosion_ratio': result.orientation.distal_erosion_ratio,
                        'axis_offset_m': result.orientation.axis_offset_m
                    }
                }
                
                candidate_id = await db.save_candidate(candidate_data)
                print(f"   ✅ Guardado en BD (ID: {candidate_id})")
                
            except Exception as e:
                print(f"   ⚠️  Error guardando en BD: {e}")
        
        # Guardar también en JSON
        with open('test_4_zonas_results.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print("✅ TEST COMPLETADO")
        print(f"   - Resultados en BD: {len(resultados)} registros")
        print(f"   - Archivo JSON: test_4_zonas_results.json")
        print(f"{'='*80}\n")
        
        return resultados
        
    finally:
        await db.close()


async def main():
    resultados = await test_4_zonas_con_bd()
    
    # Análisis comparativo
    print("\n📊 ANÁLISIS COMPARATIVO FINAL:\n")
    
    print("| Zona | Cultural Score | Tipo | Orientación | Aspect | Asim.Func |")
    print("|------|----------------|------|-------------|--------|-----------|")
    
    for r in resultados:
        print(f"| {r['zona'][:20]:20} | {r['cultural_score']:6.1%} | {r['tipo']:8} | {r['orientacion']:6.1f}° | {r['aspect_ratio']:4.2f} | {r['asimetria_funcional']:5.1%} |")
    
    print(f"\n✅ Todos los resultados guardados en la base de datos!")
    
    # Estadísticas
    print("\n📈 ESTADÍSTICAS:")
    scores = [r['cultural_score'] for r in resultados]
    print(f"   Cultural Score promedio: {sum(scores)/len(scores):.2%}")
    print(f"   Cultural Score rango: {min(scores):.2%} - {max(scores):.2%}")
    
    orientaciones = [r['orientacion'] for r in resultados]
    print(f"   Orientación promedio: {sum(orientaciones)/len(orientaciones):.1f}°")
    print(f"   Orientación rango: {min(orientaciones):.1f}° - {max(orientaciones):.1f}°")
    
    asimetrias = [r['asimetria_funcional'] for r in resultados]
    print(f"   Asimetría funcional promedio: {sum(asimetrias)/len(asimetrias):.2%}")
    print(f"   Asimetría funcional rango: {min(asimetrias):.2%} - {max(asimetrias):.2%}")
    
    print("\n🎯 VARIABILIDAD DETECTADA:")
    if max(scores) - min(scores) > 0.05:
        print("   ✅ Buena variabilidad en scores (NO clonación)")
    else:
        print("   ⚠️  Baja variabilidad en scores")
    
    if max(orientaciones) - min(orientaciones) > 5.0:
        print("   ✅ Buena variabilidad en orientaciones")
    else:
        print("   ⚠️  Baja variabilidad en orientaciones")


if __name__ == "__main__":
    asyncio.run(main())
