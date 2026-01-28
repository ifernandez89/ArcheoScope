#!/usr/bin/env python3
"""
Test Simple de Coordenadas Específicas
=======================================

Coordenadas: -75.3544, -109.8832
Ubicación: Pacífico Sur / Antártida

Test directo del backend sin dependencias complejas.
"""

import requests
import json
from datetime import datetime

# Coordenadas del usuario
LAT = -75.3544360283405
LON = -109.8831958757251

# Bounding box (±0.05 grados)
LAT_MIN = LAT - 0.05
LAT_MAX = LAT + 0.05
LON_MIN = LON - 0.05
LON_MAX = LON + 0.05

def test_coordenadas():
    """Test de coordenadas vía API"""
    
    print("="*80)
    print("🔍 TEST DE COORDENADAS ESPECÍFICAS - ArcheoScope")
    print("="*80)
    print(f"\n📍 COORDENADAS:")
    print(f"   Latitud:  {LAT:.6f}° S")
    print(f"   Longitud: {LON:.6f}° W")
    print(f"\n📦 BOUNDING BOX:")
    print(f"   Lat: {LAT_MIN:.4f} a {LAT_MAX:.4f}")
    print(f"   Lon: {LON_MIN:.4f} a {LON_MAX:.4f}")
    print()
    
    # Determinar ubicación aproximada
    print("="*80)
    print("🌍 ANÁLISIS PRELIMINAR DE UBICACIÓN")
    print("="*80)
    print()
    
    if LAT < -60:
        print("   🧊 ZONA ANTÁRTICA")
        print("   Características:")
        print("   - Latitud muy al sur (-75°)")
        print("   - Posible hielo polar o aguas antárticas")
        print("   - Ambiente extremo")
        print("   - Baja probabilidad de arqueología humana")
        print("   - Posible interés para paleoclima o geología")
    
    # Preparar request
    payload = {
        "lat_min": LAT_MIN,
        "lat_max": LAT_MAX,
        "lon_min": LON_MIN,
        "lon_max": LON_MAX,
        "region_name": "Coordenadas Específicas (-75.35, -109.88)"
    }
    
    print("\n" + "="*80)
    print("🔬 EJECUTANDO ANÁLISIS INSTRUMENTAL")
    print("="*80)
    print("\n⏳ Conectando al backend...")
    print("   URL: http://localhost:8003/analyze")
    print("   (Esto puede tomar 30-60 segundos)")
    print()
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # RESULTADOS
            print("="*80)
            print("🎯 RESULTADOS DEL ANÁLISIS")
            print("="*80)
            print()
            
            # Ambiente
            if 'spatial_context' in result:
                spatial = result['spatial_context']
                print(f"🌍 CONTEXTO ESPACIAL:")
                print(f"   Área: {spatial.get('area_km2', 'N/A')} km²")
                print(f"   Modo: {spatial.get('analysis_mode', 'N/A')}")
                print(f"   Resolución: {spatial.get('resolution_m', 'N/A')} m")
                print()
            
            # Clasificación de ambiente
            if 'environment_classification' in result:
                env = result['environment_classification']
                print(f"📍 CLASIFICACIÓN DE AMBIENTE:")
                print(f"   Tipo: {env.get('environment_type', 'unknown').upper()}")
                print(f"   Confianza: {env.get('confidence', 0):.2%}")
                if 'primary_sensors' in env:
                    print(f"   Sensores: {', '.join(env['primary_sensors'])}")
                print()
            
            # Resultados arqueológicos
            if 'archaeological_results' in result:
                arch = result['archaeological_results']
                
                result_type = arch.get('result_type', 'unknown')
                confidence = arch.get('confidence', 0)
                probability = arch.get('archaeological_probability', 0)
                
                if result_type == 'archaeological':
                    print("🔴 ANOMALÍA DETECTADA")
                elif result_type == 'anomalous':
                    print("🟡 ANOMALÍA DETECTADA (sin contexto arqueológico)")
                else:
                    print("🟢 NO HAY ANOMALÍA")
                
                print()
                print(f"📊 MÉTRICAS:")
                print(f"   Tipo de resultado: {result_type.upper()}")
                print(f"   Confianza: {confidence:.2%}")
                print(f"   Probabilidad arqueológica: {probability:.2%}")
                
                if 'affected_pixels' in arch:
                    print(f"   Píxeles afectados: {arch['affected_pixels']}")
                
                print()
            
            # Explicaciones IA
            if 'ai_explanations' in result:
                ai = result['ai_explanations']
                if ai.get('ai_available') and ai.get('explanation'):
                    print(f"🤖 EXPLICACIÓN IA:")
                    print(f"   {ai['explanation']}")
                    print()
            
            # Capas de evidencia
            if 'evidence_layers' in result and result['evidence_layers']:
                print(f"🔬 CAPAS DE EVIDENCIA ({len(result['evidence_layers'])}):")
                for layer in result['evidence_layers'][:5]:
                    print(f"   • {layer.get('layer_name', 'Unknown')}")
                    print(f"     Tipo: {layer.get('layer_type', 'N/A')}")
                    print(f"     Confianza: {layer.get('confidence', 0):.2%}")
                print()
            
            # Validación
            if 'validation_metrics' in result:
                val = result['validation_metrics']
                print(f"✅ VALIDACIÓN:")
                if val.get('known_site_nearby'):
                    print(f"   🏛️ Sitio conocido cercano: {val.get('known_site_name', 'N/A')}")
                    print(f"   📏 Distancia: {val.get('distance_km', 'N/A')} km")
                else:
                    print(f"   ℹ️ No hay sitios conocidos en la región")
                print()
            
            # Guardar resultado
            output_file = f"test_coordenadas_{LAT:.4f}_{LON:.4f}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Resultado completo guardado en: {output_file}")
            
        elif response.status_code == 503:
            print("❌ Backend no disponible")
            print("   Iniciar con: python run_archeoscope.py")
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"   {response.text[:200]}")
    
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend")
        print()
        print("   SOLUCIÓN:")
        print("   1. Abrir otra terminal")
        print("   2. Ejecutar: python run_archeoscope.py")
        print("   3. Esperar a que inicie (puerto 8003)")
        print("   4. Volver a ejecutar este test")
    
    except requests.exceptions.Timeout:
        print("❌ Timeout - El análisis tomó demasiado tiempo")
        print("   Esto puede ocurrir en zonas remotas con pocos datos")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # CONCLUSIÓN
    print()
    print("="*80)
    print("✅ TEST COMPLETADO")
    print("="*80)
    print()
    print("⚠️ DISCLAIMER CIENTÍFICO:")
    print("   Este análisis genera HIPÓTESIS basadas en anomalías instrumentales.")
    print("   NO constituye confirmación arqueológica.")
    print("   Requiere validación física por arqueólogos profesionales.")
    print()
    print("   Modo de datos:")
    print("   - REAL: Mediciones directas de APIs satelitales")
    print("   - DERIVED: Estimaciones basadas en modelos")
    print("   - INFERRED: Inferencias geométricas/estadísticas")
    print()
    print("="*80)


if __name__ == "__main__":
    test_coordenadas()
