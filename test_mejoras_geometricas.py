#!/usr/bin/env python3
"""
Test de mejoras geométricas - MOAI y ESFINGE
"""

import requests
import time

def generate_improved_model(lat, lon, region_name, output_prefix):
    """Generar modelo con mejoras geométricas."""
    
    print(f"\n{'='*70}")
    print(f"🎨 GENERANDO: {region_name}")
    print(f"{'='*70}")
    
    data = {
        "lat": lat,
        "lon": lon,
        "region_name": region_name
    }
    
    print(f"📍 Coordenadas: {lat}, {lon}")
    print(f"🔄 Generando con geometría mejorada...")
    
    try:
        response = requests.post(
            "http://localhost:8003/api/geometric-inference-3d",
            json=data,
            timeout=90
        )
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}")
            print(response.text)
            return None
        
        result = response.json()
        
        print(f"\n✅ GENERACIÓN EXITOSA")
        print(f"🏛️  Clase: {result['morphological_class'].upper()}")
        print(f"🌍 Origen: {result['cultural_origin']}")
        print(f"📊 Confianza: {result['confidence']:.2%}")
        print(f"📊 Score: {result['morphological_score']:.4f}")
        print(f"📦 Volumen: {result['volume_m3']:.2f} m³")
        
        # Esperar y descargar
        time.sleep(2)
        
        png_url = f"http://localhost:8003/api/geometric-model/{result['png_filename']}"
        png_response = requests.get(png_url, timeout=30)
        
        if png_response.status_code == 200:
            local_filename = f"{output_prefix}_MEJORADO_{int(time.time())}.png"
            with open(local_filename, 'wb') as f:
                f.write(png_response.content)
            
            print(f"\n📥 Imagen guardada: {local_filename}")
            print(f"   Tamaño: {len(png_response.content):,} bytes")
            
            return {
                'result': result,
                'local_file': local_filename,
                'size': len(png_response.content)
            }
        else:
            print(f"⚠️  Error descargando PNG: {png_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 TEST DE MEJORAS GEOMÉTRICAS")
    print("="*70)
    print("\n✨ MEJORAS IMPLEMENTADAS:")
    print("\n🗿 MOAI:")
    print("   • Más subdivisiones (10+ secciones vs 5 antes)")
    print("   • Hombros definidos")
    print("   • Cuello con transición suave (2 secciones)")
    print("   • Cabeza detallada (4 secciones: mandíbula, cara, frente, corona)")
    print("   • Frente prominente (característica moai)")
    print("   • Base y cuerpo con mejor proporción")
    
    print("\n🦁 ESFINGE:")
    print("   • Plataforma/base integrada")
    print("   • Cuerpo segmentado (trasero, medio, pecho)")
    print("   • Patas delanteras extendidas (izquierda y derecha)")
    print("   • Cuello de transición")
    print("   • Cabeza detallada (3 secciones: mandíbula, cara, corona/nemes)")
    print("   • Transiciones suaves entre todas las partes")
    
    results = []
    
    # 1. MOAI MEJORADO
    moai = generate_improved_model(
        lat=-27.1261,
        lon=-109.2868,
        region_name="Moai de Rano Raraku, Rapa Nui (Easter Island)",
        output_prefix="MOAI_RAPA_NUI"
    )
    results.append(('MOAI', moai))
    
    print("\n" + "="*70)
    time.sleep(3)
    
    # 2. ESFINGE MEJORADA
    sphinx = generate_improved_model(
        lat=29.9753,
        lon=31.1376,
        region_name="Gran Esfinge de Giza, Egipto",
        output_prefix="SPHINX_GIZA"
    )
    results.append(('ESFINGE', sphinx))
    
    # RESUMEN FINAL
    print("\n" + "="*70)
    print("📊 RESUMEN DE GENERACIÓN")
    print("="*70)
    
    for name, result in results:
        if result:
            print(f"\n✅ {name}")
            print(f"   Clase: {result['result']['morphological_class'].upper()}")
            print(f"   Origen: {result['result']['cultural_origin']}")
            print(f"   Confianza: {result['result']['confidence']:.2%}")
            print(f"   Archivo: {result['local_file']}")
            print(f"   Tamaño: {result['size']:,} bytes")
        else:
            print(f"\n❌ {name} - Error en generación")
    
    print("\n" + "="*70)
    print("🎉 GENERACIÓN COMPLETA")
    print("="*70)
    
    successful = sum(1 for _, r in results if r is not None)
    print(f"\n✅ Exitosos: {successful}/2")
    
    if successful == 2:
        print("\n🎨 Ambas imágenes mejoradas están listas!")
        print("\n📋 COMPARACIÓN CON VERSIÓN ANTERIOR:")
        print("   Antes: Geometría simple (cajas básicas)")
        print("   Ahora: Geometría detallada (10+ secciones por modelo)")
        print("\n   🗿 MOAI: Cabeza enorme con frente prominente")
        print("   🦁 ESFINGE: Cuerpo de león con patas extendidas")
        print("\n✨ ¡Mucho más detalle sin perder rigor científico!")
