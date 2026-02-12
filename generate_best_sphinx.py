#!/usr/bin/env python3
"""
Generar la mejor versión de la Esfinge de Giza
"""

import requests
import json
import time

def generate_sphinx():
    """Generar Esfinge con coordenadas exactas de Giza."""
    
    print("🦁 GENERANDO LA MEJOR ESFINGE DE GIZA")
    print("="*70)
    
    # Coordenadas exactas de la Gran Esfinge de Giza
    sphinx_data = {
        "lat": 29.9753,
        "lon": 31.1376,
        "region_name": "Great Sphinx of Giza, Egypt"
    }
    
    print(f"\n📍 Ubicación: {sphinx_data['region_name']}")
    print(f"   Coordenadas: {sphinx_data['lat']}, {sphinx_data['lon']}")
    print(f"\n🔄 Enviando solicitud al MIG Nivel 3...")
    
    try:
        response = requests.post(
            "http://localhost:8003/api/geometric-inference-3d",
            json=sphinx_data,
            timeout=90
        )
        
        if response.status_code != 200:
            print(f"\n❌ Error HTTP {response.status_code}")
            print(response.text)
            return None
        
        result = response.json()
        
        print(f"\n✅ GENERACIÓN EXITOSA")
        print("="*70)
        print(f"🏛️  Clase Morfológica: {result['morphological_class'].upper()}")
        print(f"🌍 Origen Cultural: {result['cultural_origin']}")
        print(f"📊 Confianza: {result['confidence']:.2%}")
        print(f"📊 Score Morfológico: {result['morphological_score']:.4f}")
        print(f"📦 Volumen: {result['volume_m3']:.2f} m³")
        print(f"\n📁 Archivos Generados:")
        print(f"   🖼️  PNG: {result['png_filename']}")
        print(f"   📐 OBJ: {result['obj_filename']}")
        
        # Esperar a que el archivo se escriba completamente
        time.sleep(2)
        
        # Descargar PNG
        print(f"\n📥 Descargando imagen PNG...")
        png_url = f"http://localhost:8003/api/geometric-model/{result['png_filename']}"
        png_response = requests.get(png_url, timeout=30)
        
        if png_response.status_code == 200:
            # Guardar localmente
            local_filename = f"SPHINX_GIZA_BEST_{int(time.time())}.png"
            with open(local_filename, 'wb') as f:
                f.write(png_response.content)
            
            print(f"✅ Imagen descargada: {local_filename}")
            print(f"   Tamaño: {len(png_response.content):,} bytes")
            print(f"\n🎨 Ruta completa: {result['png_path']}")
            print(f"🎨 Copia local: {local_filename}")
        else:
            print(f"⚠️  No se pudo descargar PNG: {png_response.status_code}")
        
        print("\n" + "="*70)
        print("🦁 ESFINGE DE GIZA GENERADA CON ÉXITO")
        print("="*70)
        print("\n📋 Características de la Esfinge:")
        print(f"   • Forma horizontal (león recostado con cabeza humana)")
        print(f"   • Constreñida por invariantes culturales egipcios")
        print(f"   • Basada en {result.get('morphological_score', 0):.2%} de compatibilidad morfológica")
        print(f"   • Color: Piedra caliza dorada del desierto")
        print(f"   • Vista: Lateral-frontal optimizada")
        print(f"   • Calidad: Alta resolución (DPI 200)")
        
        return result
        
    except Exception as e:
        print(f"\n❌ EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = generate_sphinx()
    
    if result:
        print("\n✨ ¡Disfruta tu Esfinge culturalmente constreñida!")
    else:
        print("\n❌ No se pudo generar la Esfinge")
