#!/usr/bin/env python3
"""
Generar modelos 3D para:
1. Anomalía de Patagonia
2. Pirámide del Sol, Teotihuacán
"""

import requests
import json
import time

def generate_model(lat, lon, region_name, output_prefix):
    """Generar modelo 3D para una ubicación."""
    
    print(f"\n{'='*70}")
    print(f"🔍 GENERANDO: {region_name}")
    print(f"{'='*70}")
    
    data = {
        "lat": lat,
        "lon": lon,
        "region_name": region_name
    }
    
    print(f"📍 Coordenadas: {lat}, {lon}")
    print(f"🔄 Enviando solicitud al MIG Nivel 3...")
    
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
        print(f"🏛️  Clase Morfológica: {result['morphological_class'].upper()}")
        print(f"🌍 Origen Cultural: {result['cultural_origin']}")
        print(f"📊 Confianza: {result['confidence']:.2%}")
        print(f"📊 Score Morfológico: {result['morphological_score']:.4f}")
        print(f"📦 Volumen: {result['volume_m3']:.2f} m³")
        
        # Esperar escritura de archivo
        time.sleep(2)
        
        # Descargar PNG
        print(f"\n📥 Descargando imagen PNG...")
        png_url = f"http://localhost:8003/api/geometric-model/{result['png_filename']}"
        png_response = requests.get(png_url, timeout=30)
        
        if png_response.status_code == 200:
            local_filename = f"{output_prefix}_{int(time.time())}.png"
            with open(local_filename, 'wb') as f:
                f.write(png_response.content)
            
            print(f"✅ Imagen guardada: {local_filename}")
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
    print("🌎 GENERACIÓN DE MODELOS 3D - PATAGONIA Y TEOTIHUACÁN")
    print("="*70)
    
    results = []
    
    # 1. ANOMALÍA DE PATAGONIA
    # Coordenadas de la anomalía detectada en Patagonia
    patagonia = generate_model(
        lat=-45.8,
        lon=-71.5,
        region_name="Anomalía Patagonia, Argentina",
        output_prefix="PATAGONIA_ANOMALY"
    )
    results.append(('Patagonia', patagonia))
    
    print("\n" + "="*70)
    time.sleep(3)  # Pausa entre generaciones
    
    # 2. PIRÁMIDE DEL SOL, TEOTIHUACÁN
    # Coordenadas de la Pirámide del Sol
    teotihuacan = generate_model(
        lat=19.6925,
        lon=-98.8438,
        region_name="Pirámide del Sol, Teotihuacán, México",
        output_prefix="TEOTIHUACAN_PYRAMID"
    )
    results.append(('Teotihuacán', teotihuacan))
    
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
        print("\n🎨 Ambas imágenes están listas!")
        print("   • PATAGONIA_ANOMALY_*.png")
        print("   • TEOTIHUACAN_PYRAMID_*.png")
