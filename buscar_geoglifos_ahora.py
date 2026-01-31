#!/usr/bin/env python3
"""
🔍 BÚSQUEDA DE GEOGLIFOS - MODO EXPLORADOR
==========================================

Script para buscar geoglifos en zonas prometedoras de Arabia
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.geoglyph_detector import GeoglyphDetector, DetectionMode
import numpy as np
import json
from datetime import datetime

def buscar_en_zona(zona_nombre, lat, lon, bbox_size=0.1, mode=DetectionMode.EXPLORER):
    """
    Buscar geoglifos en una zona específica
    
    Args:
        zona_nombre: Nombre descriptivo de la zona
        lat, lon: Coordenadas centrales
        bbox_size: Tamaño del área a analizar (grados)
        mode: Modo de detección
    """
    print(f"\n{'='*80}")
    print(f"🔍 BUSCANDO GEOGLIFOS EN: {zona_nombre}")
    print(f"📍 Coordenadas: {lat:.4f}°N, {lon:.4f}°E")
    print(f"🤖 Modo: {mode.value}")
    print(f"{'='*80}\n")
    
    # Inicializar detector
    detector = GeoglyphDetector(mode=mode)
    
    # Definir área de búsqueda
    lat_min = lat - bbox_size / 2
    lat_max = lat + bbox_size / 2
    lon_min = lon - bbox_size / 2
    lon_max = lon + bbox_size / 2
    
    print(f"📐 Área de búsqueda:")
    print(f"   Lat: {lat_min:.4f}° a {lat_max:.4f}°")
    print(f"   Lon: {lon_min:.4f}° a {lon_max:.4f}°")
    print(f"   Tamaño: ~{bbox_size * 111:.1f}km × {bbox_size * 111:.1f}km\n")
    
    # Simular DEM data (en producción, esto vendría de SRTM/NASADEM)
    # TODO: Integrar con satellite_connectors reales
    dem_data = np.random.rand(100, 100) * 100  # Placeholder
    
    try:
        print("⏳ Analizando área...")
        
        # Detectar geoglifo
        result = detector.detect_geoglyph(
            lat=lat,
            lon=lon,
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max,
            dem_data=dem_data,
            resolution_m=1.0  # 1 metro/pixel (ideal para geoglifos)
        )
        
        # Mostrar resultados
        print(f"\n{'─'*80}")
        print("📊 RESULTADOS DE DETECCIÓN")
        print(f"{'─'*80}\n")
        
        print(f"🏷️  Tipo detectado: {result.geoglyph_type.value.upper()}")
        print(f"📈 Confianza tipo: {result.type_confidence:.2%}")
        print(f"🎯 Cultural Score: {result.cultural_score:.2%}")
        print(f"⭐ Prioridad validación: {result.validation_priority}")
        print(f"📏 Resolución recomendada: {result.recommended_resolution_m}m/pixel")
        
        if result.paper_level_discovery:
            print("\n🏆 ¡DESCUBRIMIENTO NIVEL PAPER!")
        
        print(f"\n📐 CARACTERÍSTICAS GEOMÉTRICAS:")
        print(f"   Orientación: {result.orientation.azimuth_deg:.1f}°")
        print(f"   Eje mayor: {result.orientation.major_axis_length_m:.1f}m")
        print(f"   Eje menor: {result.orientation.minor_axis_length_m:.1f}m")
        print(f"   Aspect ratio: {result.orientation.aspect_ratio:.2f}")
        print(f"   Simetría bilateral: {result.orientation.bilateral_symmetry:.2%}")
        print(f"   Confianza orientación: {result.orientation.orientation_confidence:.2%}")
        
        if result.orientation.is_nw_se:
            print("   ✅ Orientación NW-SE detectada")
        if result.orientation.is_e_w:
            print("   ✅ Orientación E-W detectada")
        if result.orientation.points_to_lowland:
            print("   ✅ Apunta hacia zona baja")
        
        print(f"\n🌋 CONTEXTO VOLCÁNICO:")
        print(f"   Distancia a flujo basáltico: {result.volcanic_context.distance_to_basalt_flow_km:.1f}km")
        print(f"   Superficie estable: {'✅ SÍ' if result.volcanic_context.on_stable_surface else '❌ NO'}")
        print(f"   Flujo joven: {'❌ SÍ (malo)' if result.volcanic_context.on_young_flow else '✅ NO (bueno)'}")
        print(f"   Confianza volcánica: {result.volcanic_context.volcanic_confidence:.2%}")
        
        print(f"\n💧 PALEOHIDROLOGÍA:")
        print(f"   Distancia a paleocanal: {result.paleo_hydrology.distance_to_paleochannel_km:.1f}km")
        print(f"   Distancia a wadi: {result.paleo_hydrology.distance_to_wadi_km:.1f}km")
        print(f"   En transición sedimento: {'🏆 SÍ (ORO)' if result.paleo_hydrology.on_sediment_transition else 'NO'}")
        print(f"   Prob. agua estacional: {result.paleo_hydrology.seasonal_water_probability:.2%}")
        print(f"   Confianza hidrológica: {result.paleo_hydrology.hydrological_confidence:.2%}")
        
        print(f"\n🌌 ALINEACIONES ASTRONÓMICAS:")
        print(f"   Mejor alineación solar: {result.celestial_alignment.best_solar_alignment}")
        print(f"   Solsticio verano: {result.celestial_alignment.summer_solstice_alignment:.2%}")
        print(f"   Solsticio invierno: {result.celestial_alignment.winter_solstice_alignment:.2%}")
        print(f"   Equinoccio: {result.celestial_alignment.equinox_alignment:.2%}")
        print(f"   Coherencia regional: {result.celestial_alignment.regional_coherence:.2%}")
        print(f"   Confianza alineación: {result.celestial_alignment.alignment_confidence:.2%}")
        
        if result.celestial_alignment.regional_coherence > 0.70:
            print("   🏆 ALTA coherencia regional - potencial paper!")
        
        print(f"\n📝 RAZONAMIENTO DE DETECCIÓN:")
        for i, reason in enumerate(result.detection_reasoning, 1):
            print(f"   {i}. {reason}")
        
        print(f"\n⚠️  RIESGOS DE FALSO POSITIVO:")
        for i, risk in enumerate(result.false_positive_risks, 1):
            print(f"   {i}. {risk}")
        
        # Guardar resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"geoglyph_{zona_nombre.replace(' ', '_')}_{timestamp}.json"
        
        result_dict = {
            "zona": zona_nombre,
            "coordenadas": {"lat": lat, "lon": lon},
            "tipo": result.geoglyph_type.value,
            "cultural_score": result.cultural_score,
            "paper_level": result.paper_level_discovery,
            "orientacion": {
                "azimuth": result.orientation.azimuth_deg,
                "eje_mayor_m": result.orientation.major_axis_length_m,
                "aspect_ratio": result.orientation.aspect_ratio
            },
            "timestamp": timestamp
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultado guardado en: {filename}")
        print(f"\n{'='*80}\n")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error en detección: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Función principal - buscar en zonas prometedoras"""
    
    print("\n" + "="*80)
    print("🔍 ARCHEOSCOPE - BÚSQUEDA DE GEOGLIFOS")
    print("="*80)
    print("\n🎯 ZONAS PROMETEDORAS PRE-CONFIGURADAS:\n")
    
    zonas_prometedoras = {
        # ARABIA CLÁSICA (ya exploradas)
        "1": {
            "nombre": "Sur Harrat Uwayrid",
            "lat": 26.5,
            "lon": 38.5,
            "descripcion": "Basalto antiguo, baja intervención moderna",
            "prioridad": "🔴 CRÍTICA",
            "region": "Arabia Central"
        },
        "2": {
            "nombre": "Límite Arabia-Jordania",
            "lat": 29.5,
            "lon": 37.5,
            "descripcion": "Paleorutas, ausencia de papers arqueológicos",
            "prioridad": "🔴 CRÍTICA",
            "region": "Arabia Norte"
        },
        "3": {
            "nombre": "Bordes Rub al Khali Norte",
            "lat": 20.5,
            "lon": 51.0,
            "descripcion": "Bordes del desierto vacío, no centro",
            "prioridad": "🟡 MEDIA",
            "region": "Arabia Sur"
        },
        "4": {
            "nombre": "Harrat Khaybar",
            "lat": 25.0,
            "lon": 39.9,
            "descripcion": "Campo volcánico con estructuras reportadas",
            "prioridad": "🟢 ALTA",
            "region": "Arabia Central"
        },
        
        # 🆕 NUEVAS ZONAS - FUERA DE ARABIA CLÁSICA
        "5": {
            "nombre": "Jordania Profunda (Badia Oriental)",
            "lat": 32.0,
            "lon": 38.0,
            "descripcion": "🎯 BUSCAR CUARTO CASO - Zona poco estudiada",
            "prioridad": "🔴 CRÍTICA",
            "region": "Jordania",
            "note": "Patrón cultural fuera de Arabia clásica"
        },
        "6": {
            "nombre": "Sinaí Central",
            "lat": 30.0,
            "lon": 34.0,
            "descripcion": "🎯 Conexión Arabia-Levante, basaltos antiguos",
            "prioridad": "🟢 ALTA",
            "region": "Sinaí",
            "note": "Ruta de paleocontacto"
        },
        "7": {
            "nombre": "Norte del Hijaz (Desconocido)",
            "lat": 27.5,
            "lon": 38.0,
            "descripcion": "🎯 Terreno virgen científicamente",
            "prioridad": "🟢 ALTA",
            "region": "Hijaz Norte",
            "note": "Zona no catalogada arqueológicamente"
        },
        "8": {
            "nombre": "Corredor Wadi Sirhan",
            "lat": 30.0,
            "lon": 38.5,
            "descripcion": "🏆 ORO: Paleocanal mayor + contexto cultural",
            "prioridad": "🔴 CRÍTICA",
            "region": "Arabia-Jordania",
            "note": "Antiguo corredor migratorio"
        },
        "9": {
            "nombre": "PERSONALIZADA",
            "descripcion": "Ingresa tus propias coordenadas"
        }
    }
    
    for key, zona in zonas_prometedoras.items():
        print(f"  {key}. {zona['nombre']}")
        print(f"     {zona['descripcion']}")
        if 'prioridad' in zona:
            print(f"     Prioridad: {zona['prioridad']}")
        if 'lat' in zona:
            print(f"     Coords: {zona['lat']:.2f}°N, {zona['lon']:.2f}°E")
        print()
    
    # Selección de zona
    try:
        opcion = input("Selecciona una zona (1-9) o 'q' para salir: ").strip()
        
        if opcion.lower() == 'q':
            print("\n👋 ¡Hasta luego!\n")
            return
        
        if opcion not in zonas_prometedoras:
            print("\n❌ Opción inválida\n")
            return
        
        zona = zonas_prometedoras[opcion]
        
        if opcion == "9":
            # Zona personalizada
            print("\n📍 ZONA PERSONALIZADA")
            lat = float(input("Latitud (ej: 26.5): "))
            lon = float(input("Longitud (ej: 38.5): "))
            nombre = input("Nombre de la zona (opcional): ") or "Personalizada"
        else:
            lat = zona["lat"]
            lon = zona["lon"]
            nombre = zona["nombre"]
        
        # Modo de detección
        print("\n🤖 MODO DE DETECCIÓN:")
        print("  1. Científico (estricto, para papers)")
        print("  2. Explorador (moderado, recomendado)")
        print("  3. Cognitivo (permisivo, hipótesis)")
        
        modo_opcion = input("\nSelecciona modo (1-3, default=2): ").strip() or "2"
        
        modos = {
            "1": DetectionMode.SCIENTIFIC,
            "2": DetectionMode.EXPLORER,
            "3": DetectionMode.COGNITIVE
        }
        
        mode = modos.get(modo_opcion, DetectionMode.EXPLORER)
        
        # ¡BUSCAR!
        resultado = buscar_en_zona(nombre, lat, lon, bbox_size=0.1, mode=mode)
        
        if resultado:
            print("\n✅ Búsqueda completada exitosamente!")
            
            # Preguntar si buscar otra zona
            otra = input("\n¿Buscar en otra zona? (s/n): ").strip().lower()
            if otra == 's':
                main()  # Recursivo
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Búsqueda interrumpida por el usuario\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║            🔍 ARCHEOSCOPE - SISTEMA DE DETECCIÓN DE GEOGLIFOS            ║
    ║                                                                           ║
    ║  Busca estructuras arqueológicas antiguas (gates, pendants, wheels)     ║
    ║  en zonas desérticas usando análisis multi-espectral                    ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    main()
    
    print("\n" + "="*80)
    print("¡Gracias por usar ArcheoScope!")
    print("="*80 + "\n")
