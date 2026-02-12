#!/usr/bin/env python3
"""
Generar Teotihuacán FINAL con todas las mejoras geométricas
"""

import requests
import time

def generate_final():
    """Generar versión final mejorada."""
    
    print("🏛️ GENERANDO TEOTIHUACÁN - VERSIÓN FINAL MEJORADA")
    print("="*70)
    print("\n✨ MEJORAS IMPLEMENTADAS:")
    print("   • Talud-tablero (estilo Teotihuacán auténtico)")
    print("   • Escalinata frontal real con escalones individuales")
    print("   • 5-8 niveles escalonados (vs 4-7 antes)")
    print("   • Templo superior detallado (base + cuerpo + techo)")
    print("   • Transiciones suaves entre niveles")
    print("   • Más subdivisiones para geometría refinada")
    
    data = {
        "lat": 19.6925,
        "lon": -98.8438,
        "region_name": "Pirámide del Sol, Teotihuacán, México"
    }
    
    print(f"\n📍 Ubicación: {data['region_name']}")
    print(f"   Coordenadas: {data['lat']}, {data['lon']}")
    print(f"\n🔄 Generando...")
    
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
            local_filename = f"TEOTIHUACAN_FINAL_MEJORADO_{int(time.time())}.png"
            with open(local_filename, 'wb') as f:
                f.write(png_response.content)
            
            print(f"\n📥 Imagen guardada: {local_filename}")
            print(f"   Tamaño: {len(png_response.content):,} bytes")
            print(f"\n🎨 Características visuales:")
            print(f"   • Color: Piedra volcánica beige")
            print(f"   • Vista: Elevada (30°) para apreciar niveles")
            print(f"   • DPI: 200 (alta resolución)")
            print(f"   • Geometría: Escalonada con talud-tablero")
            print(f"   • Escalinata: Visible en el frente")
            print(f"   • Templo: Estructura detallada en la cima")
        
        print("\n" + "="*70)
        print("🎉 TEOTIHUACÁN FINAL GENERADO")
        print("="*70)
        
        return result
        
    except Exception as e:
        print(f"\n❌ EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = generate_final()
    
    if result:
        print("\n✨ ¡Disfruta tu pirámide mesoamericana mejorada!")
        print("   Ahora con geometría mucho más detallada y culturalmente precisa")
    else:
        print("\n❌ Error en generación")
