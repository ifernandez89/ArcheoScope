#!/usr/bin/env python3
"""
Generar la mejor versión de un MOAI de Rapa Nui
"""

import requests
import json
import time

def generate_moai():
    """Generar MOAI con coordenadas de Rapa Nui."""
    
    print("🗿 GENERANDO EL MEJOR MOAI DE RAPA NUI")
    print("="*70)
    
    # Coordenadas de Rano Raraku (cantera de moais)
    moai_data = {
        "lat": -27.1261,
        "lon": -109.2868,
        "region_name": "Rano Raraku Quarry, Rapa Nui (Easter Island)"
    }
    
    print(f"\n📍 Ubicación: {moai_data['region_name']}")
    print(f"   Coordenadas: {moai_data['lat']}, {moai_data['lon']}")
    print(f"\n🔄 Enviando solicitud al MIG Nivel 3...")
    
    try:
        response = requests.post(
            "http://localhost:8003/api/geometric-inference-3d",
            json=moai_data,
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
            local_filename = f"MOAI_RAPA_NUI_BEST_{int(time.time())}.png"
            with open(local_filename, 'wb') as f:
                f.write(png_response.content)
            
            print(f"✅ Imagen descargada: {local_filename}")
            print(f"   Tamaño: {len(png_response.content):,} bytes")
            print(f"\n🎨 Ruta completa: {result['png_path']}")
            print(f"🎨 Copia local: {local_filename}")
        else:
            print(f"⚠️  No se pudo descargar PNG: {png_response.status_code}")
        
        print("\n" + "="*70)
        print("🗿 MOAI DE RAPA NUI GENERADO CON ÉXITO")
        print("="*70)
        print("\n📋 Características del Moai:")
        print(f"   • Forma vertical monolítica (cabeza enorme)")
        print(f"   • Constreñido por invariantes culturales de Rapa Nui")
        print(f"   • Basado en {result.get('morphological_score', 0):.2%} de compatibilidad morfológica")
        print(f"   • Color: Toba volcánica gris")
        print(f"   • Vista: Frontal optimizada")
        print(f"   • Calidad: Alta resolución (DPI 200)")
        
        return result
        
    except Exception as e:
        print(f"\n❌ EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = generate_moai()
    
    if result:
        print("\n✨ ¡Disfruta tu Moai culturalmente constreñido!")
    else:
        print("\n❌ No se pudo generar el Moai")
