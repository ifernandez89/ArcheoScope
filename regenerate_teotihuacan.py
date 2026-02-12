#!/usr/bin/env python3
"""
Regenerar Teotihuacán con clases mesoamericanas
"""

import requests
import time

def regenerate_teotihuacan():
    """Regenerar Pirámide del Sol con nuevas clases."""
    
    print("🏛️ REGENERANDO TEOTIHUACÁN CON CLASES MESOAMERICANAS")
    print("="*70)
    
    data = {
        "lat": 19.6925,
        "lon": -98.8438,
        "region_name": "Pirámide del Sol, Teotihuacán, México"
    }
    
    print(f"\n📍 Ubicación: {data['region_name']}")
    print(f"   Coordenadas: {data['lat']}, {data['lon']}")
    print(f"\n🔄 Generando con repositorio morfológico expandido...")
    print(f"   ✅ Clases mesoamericanas agregadas:")
    print(f"      • PYRAMID_MESOAMERICAN")
    print(f"      • TEMPLE_PLATFORM")
    print(f"      • STELA_MAYA")
    
    try:
        response = requests.post(
            "http://localhost:8003/api/geometric-inference-3d",
            json=data,
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
        
        # Comparación con versión anterior
        print(f"\n📊 COMPARACIÓN:")
        print(f"   Antes: SPHINX (69.47% confianza) - Egipto")
        print(f"   Ahora: {result['morphological_class'].upper()} ({result['confidence']:.2%} confianza) - {result['cultural_origin']}")
        
        if "Mesoamerica" in result['cultural_origin']:
            print(f"\n   🎯 ✅ CORRECTO: Ahora clasifica como mesoamericana!")
        
        # Esperar y descargar
        time.sleep(2)
        
        png_url = f"http://localhost:8003/api/geometric-model/{result['png_filename']}"
        png_response = requests.get(png_url, timeout=30)
        
        if png_response.status_code == 200:
            local_filename = f"TEOTIHUACAN_MESOAMERICAN_{int(time.time())}.png"
            with open(local_filename, 'wb') as f:
                f.write(png_response.content)
            
            print(f"\n📥 Imagen guardada: {local_filename}")
            print(f"   Tamaño: {len(png_response.content):,} bytes")
        
        print("\n" + "="*70)
        print("🎉 TEOTIHUACÁN REGENERADO CON ÉXITO")
        print("="*70)
        
        return result
        
    except Exception as e:
        print(f"\n❌ EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = regenerate_teotihuacan()
    
    if result and "Mesoamerica" in result.get('cultural_origin', ''):
        print("\n✨ ¡Clasificación mesoamericana exitosa!")
    else:
        print("\n⚠️  Revisar clasificación")
