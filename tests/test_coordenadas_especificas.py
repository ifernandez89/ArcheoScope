#!/usr/bin/env python3
"""
Test de Coordenadas Específicas
================================

Coordenadas: -75.3544, -109.8832
Ubicación: Pacífico Sur / Antártida

Test completo del sistema ArcheoScope con integridad científica.
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from environment_classifier import EnvironmentClassifier
from validation.real_archaeological_validator import RealArchaeologicalValidator
from core_anomaly_detector import CoreAnomalyDetector
from data.archaeological_loader import ArchaeologicalDataLoader


async def test_coordenadas():
    """Test completo de coordenadas específicas"""
    
    # Coordenadas del usuario
    lat = -75.3544360283405
    lon = -109.8831958757251
    
    # Bounding box (±0.05 grados)
    lat_min = lat - 0.05
    lat_max = lat + 0.05
    lon_min = lon - 0.05
    lon_max = lon + 0.05
    
    print("="*80)
    print("🔍 TEST DE COORDENADAS ESPECÍFICAS - ArcheoScope")
    print("="*80)
    print(f"\n📍 COORDENADAS:")
    print(f"   Latitud:  {lat:.6f}° S")
    print(f"   Longitud: {lon:.6f}° W")
    print(f"\n📦 BOUNDING BOX:")
    print(f"   Lat: {lat_min:.4f} a {lat_max:.4f}")
    print(f"   Lon: {lon_min:.4f} a {lon_max:.4f}")
    print()
    
    # PASO 1: Clasificar ambiente
    print("="*80)
    print("📍 PASO 1: CLASIFICACIÓN DE AMBIENTE")
    print("="*80)
    
    classifier = EnvironmentClassifier()
    env_context = classifier.classify(lat, lon)
    
    print(f"\n✅ Ambiente detectado: {env_context.environment_type.value}")
    print(f"   Confianza: {env_context.confidence:.2%}")
    print(f"   Sensores primarios: {', '.join(env_context.primary_sensors)}")
    print(f"   Características:")
    for key, value in env_context.characteristics.items():
        print(f"      - {key}: {value}")
    
    # PASO 2: Validar contra BD arqueológica
    print("\n" + "="*80)
    print("🏛️ PASO 2: VALIDACIÓN CONTRA BD ARQUEOLÓGICA")
    print("="*80)
    
    try:
        validator = RealArchaeologicalValidator()
        validation = validator.validate_region(lat_min, lat_max, lon_min, lon_max)
        
        print(f"\n✅ Validación completada:")
        print(f"   Sitios superpuestos: {len(validation.get('overlapping_sites', []))}")
        print(f"   Sitios cercanos: {len(validation.get('nearby_sites', []))}")
        
        if validation.get('overlapping_sites'):
            print(f"\n   🏛️ SITIOS SUPERPUESTOS:")
            for site in validation['overlapping_sites'][:3]:
                print(f"      - {site.name}")
                print(f"        Tipo: {site.site_type}")
                print(f"        Confianza: {site.confidence_level}")
        
        if validation.get('nearby_sites'):
            print(f"\n   📍 SITIOS CERCANOS:")
            for site, distance in validation['nearby_sites'][:3]:
                print(f"      - {site.name} ({distance:.2f} km)")
                print(f"        Tipo: {site.site_type}")
    
    except Exception as e:
        print(f"\n⚠️ Validación de BD no disponible: {e}")
        validation = {'overlapping_sites': [], 'nearby_sites': []}
    
    # PASO 3: Detección de anomalías
    print("\n" + "="*80)
    print("🔬 PASO 3: DETECCIÓN DE ANOMALÍAS INSTRUMENTALES")
    print("="*80)
    
    try:
        # Inicializar detector
        data_loader = ArchaeologicalDataLoader()
        
        try:
            real_validator = RealArchaeologicalValidator()
        except:
            real_validator = None
        
        detector = CoreAnomalyDetector(
            environment_classifier=classifier,
            real_validator=real_validator,
            data_loader=data_loader
        )
        
        # Ejecutar detección
        print("\n🔍 Ejecutando análisis instrumental...")
        print("   (Esto puede tomar 30-60 segundos)")
        
        result = await detector.detect_anomaly(
            lat=lat,
            lon=lon,
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max,
            region_name="Coordenadas Específicas"
        )
        
        # RESULTADOS
        print("\n" + "="*80)
        print("🎯 RESULTADOS DEL ANÁLISIS")
        print("="*80)
        
        print(f"\n{'🔴 ANOMALÍA DETECTADA' if result.anomaly_detected else '🟢 NO HAY ANOMALÍA'}")
        print(f"\n📊 MÉTRICAS:")
        print(f"   Nivel de confianza: {result.confidence_level.upper()}")
        print(f"   Probabilidad arqueológica: {result.archaeological_probability:.2%}")
        print(f"   Instrumentos convergentes: {result.instruments_converging}/{result.minimum_required}")
        
        print(f"\n🌍 CONTEXTO AMBIENTAL:")
        print(f"   Tipo: {result.environment_type}")
        print(f"   Confianza: {result.environment_confidence:.2%}")
        
        if result.known_site_nearby:
            print(f"\n🏛️ SITIO CONOCIDO CERCANO:")
            print(f"   Nombre: {result.known_site_name}")
            print(f"   Distancia: {result.known_site_distance_km:.2f} km")
        
        print(f"\n📝 EXPLICACIÓN:")
        print(f"   {result.explanation}")
        
        if result.detection_reasoning:
            print(f"\n🔬 RAZONAMIENTO DE DETECCIÓN:")
            for reason in result.detection_reasoning:
                print(f"   • {reason}")
        
        if result.false_positive_risks:
            print(f"\n⚠️ RIESGOS DE FALSOS POSITIVOS:")
            for risk in result.false_positive_risks:
                print(f"   • {risk}")
        
        if result.recommended_validation:
            print(f"\n✅ VALIDACIÓN RECOMENDADA:")
            for rec in result.recommended_validation:
                print(f"   • {rec}")
        
        # MEDICIONES INSTRUMENTALES
        if result.measurements:
            print(f"\n🔬 MEDICIONES INSTRUMENTALES ({len(result.measurements)}):")
            for m in result.measurements:
                status = "✅ EXCEDE" if m.exceeds_threshold else "❌ NO EXCEDE"
                print(f"\n   {status} - {m.instrument_name}")
                print(f"      Valor: {m.value:.3f} {m.unit}")
                print(f"      Umbral: {m.threshold:.3f} {m.unit}")
                print(f"      Confianza: {m.confidence}")
                
                # Verificar data_mode si está disponible
                if hasattr(m, 'notes') and 'data_mode' in str(m.notes).lower():
                    print(f"      Modo: {m.notes}")
        
        # Guardar resultado
        output_file = f"test_coordenadas_{lat:.4f}_{lon:.4f}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        result_dict = {
            'coordinates': {
                'lat': lat,
                'lon': lon,
                'lat_min': lat_min,
                'lat_max': lat_max,
                'lon_min': lon_min,
                'lon_max': lon_max
            },
            'environment': {
                'type': result.environment_type,
                'confidence': result.environment_confidence
            },
            'anomaly_detected': result.anomaly_detected,
            'confidence_level': result.confidence_level,
            'archaeological_probability': result.archaeological_probability,
            'instruments_converging': result.instruments_converging,
            'minimum_required': result.minimum_required,
            'explanation': result.explanation,
            'detection_reasoning': result.detection_reasoning,
            'false_positive_risks': result.false_positive_risks,
            'recommended_validation': result.recommended_validation,
            'measurements': [
                {
                    'instrument': m.instrument_name,
                    'value': float(m.value),
                    'unit': m.unit,
                    'threshold': float(m.threshold),
                    'exceeds': m.exceeds_threshold,
                    'confidence': m.confidence
                }
                for m in result.measurements
            ],
            'known_site_nearby': result.known_site_nearby,
            'known_site_name': result.known_site_name,
            'known_site_distance_km': result.known_site_distance_km,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultado guardado en: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error en detección de anomalías: {e}")
        import traceback
        traceback.print_exc()
    
    # CONCLUSIÓN
    print("\n" + "="*80)
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


if __name__ == "__main__":
    asyncio.run(test_coordenadas())
