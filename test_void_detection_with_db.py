#!/usr/bin/env python3
"""
Test Subsurface Void Detection - PARA EJECUTAR EN CASA CON BD REAL
===================================================================

Este script está preparado para ejecutarse con:
- Base de datos PostgreSQL real
- Credenciales configuradas en .env
- Datos satelitales reales

REQUISITOS:
1. BD PostgreSQL corriendo
2. Archivo .env con DATABASE_URL
3. Tablas: timt_measurements, timt_analysis_results

MODO DE USO:
python test_void_detection_with_db.py --lat 30.0 --lon 31.0
"""

import sys
import os
import argparse
from datetime import datetime

# Agregar backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_void_detection_with_real_data(lat: float, lon: float):
    """
    Test completo de detección de vacíos con datos reales de BD.
    """
    print("=" * 80)
    print("🔬 TEST DETECCIÓN DE SUBESTRUCTURAS HUECAS")
    print("=" * 80)
    print(f"\n📍 Coordenadas: {lat:.6f}, {lon:.6f}")
    print(f"⏰ Timestamp: {datetime.utcnow().isoformat()}\n")
    
    try:
        # Importar módulos
        from environment_classifier import EnvironmentClassifier
        from subsurface_void_detector import subsurface_void_detector
        from contextual_validator import contextual_validator, EnvironmentType as CtxEnvType
        from database import get_db_connection
        
        print("✅ Módulos importados correctamente\n")
        
        # Conectar a BD
        conn = get_db_connection()
        
        # Cargar sitios conocidos como anclas contextuales
        print("Cargando sitios conocidos como anclas contextuales...")
        contextual_validator.load_known_sites_from_db(conn)
        print(f"✅ {len(contextual_validator.known_sites)} sitios cargados\n")
        
        # PASO 1: Clasificar ambiente
        print("PASO 1: Clasificación de Ambiente")
        print("-" * 80)
        
        classifier = EnvironmentClassifier()
        env_context = classifier.classify(lat, lon)
        
        print(f"Ambiente detectado: {env_context.environment_type.value}")
        print(f"Confianza: {env_context.confidence:.2%}")
        print(f"Sensores primarios: {', '.join(env_context.primary_sensors[:3])}")
        print(f"Visibilidad arqueológica: {env_context.archaeological_visibility}")
        print(f"Potencial de preservación: {env_context.preservation_potential}\n")
        
        # PASO 2: Obtener datos satelitales de BD
        print("PASO 2: Obtención de Datos Satelitales desde BD")
        print("-" * 80)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar mediciones existentes en un radio de 0.01 grados (~1km)
        query = """
        SELECT 
            lat, lon,
            sar_backscatter, sar_coherence,
            lst_day, lst_night,
            ndvi_mean, ndvi_variance,
            elevation, slope,
            created_at
        FROM timt_measurements
        WHERE 
            lat BETWEEN %s AND %s
            AND lon BETWEEN %s AND %s
        ORDER BY created_at DESC
        LIMIT 1
        """
        
        cursor.execute(query, (
            lat - 0.01, lat + 0.01,
            lon - 0.01, lon + 0.01
        ))
        
        row = cursor.fetchone()
        
        if row:
            print("✅ Datos encontrados en BD:")
            print(f"   Ubicación: {row[0]:.6f}, {row[1]:.6f}")
            print(f"   SAR Backscatter: {row[2]:.2f} dB" if row[2] else "   SAR Backscatter: N/A")
            print(f"   SAR Coherence: {row[3]:.3f}" if row[3] else "   SAR Coherence: N/A")
            print(f"   LST Día: {row[4]:.1f}°C" if row[4] else "   LST Día: N/A")
            print(f"   LST Noche: {row[5]:.1f}°C" if row[5] else "   LST Noche: N/A")
            print(f"   NDVI: {row[6]:.3f}" if row[6] else "   NDVI: N/A")
            print(f"   Elevación: {row[8]:.1f}m" if row[8] else "   Elevación: N/A")
            print(f"   Pendiente: {row[9]:.1f}°" if row[9] else "   Pendiente: N/A")
            print(f"   Fecha: {row[10]}\n")
            
            # Construir diccionario de datos satelitales
            satellite_data = {
                'sar_backscatter_db': row[2] if row[2] is not None else -10.0,
                'sar_coherence': row[3] if row[3] is not None else 0.8,
                'sar_spatial_symmetry': 0.5,  # Calcular en producción
                'lst_day_celsius': row[4] if row[4] is not None else 30.0,
                'lst_night_celsius': row[5] if row[5] is not None else 20.0,
                'expected_night_temp': 18.0,  # Calcular basado en elevación
                'thermal_temporal_variance': 1.5,  # Calcular de serie temporal
                'ndvi_mean': row[6] if row[6] is not None else 0.15,
                'ndvi_variance': row[7] if row[7] is not None else 0.03,
                'ndvi_temporal_stability': 0.8,  # Calcular de serie temporal
                'elevation_anomaly': -0.3,  # Calcular vs entorno
                'depression_symmetry': 0.7,  # Calcular de DEM
                'erosion_likelihood': 0.2,  # Calcular de contexto geológico
                'slope_degrees': row[9] if row[9] is not None else 5.0,
                'thermal_variance': 2.0,  # Varianza espacial
                'geometric_symmetry': 0.6,  # Calcular de análisis geométrico
                'right_angles_detected': False,  # Calcular de análisis geométrico
                'orientation_bias': 0.5,  # Calcular de análisis direccional
                'modular_repetition': False,  # Calcular de análisis espacial
                'data_quality_score': 0.85,  # Basado en cobertura de nubes, etc.
            }
        else:
            print("⚠️ No se encontraron datos en BD, usando valores simulados\n")
            satellite_data = _generate_simulated_data(env_context)
        
        cursor.close()
        
        # PASO 3: Detectar vacío
        print("PASO 3: Detección de Subestructura Hueca")
        print("-" * 80)
        
        result = subsurface_void_detector.detect_void(
            lat=lat,
            lon=lon,
            environment_context=env_context,
            satellite_data=satellite_data
        )
        
        # Mostrar resultados
        print(f"\n🔍 RESULTADOS DEL ANÁLISIS")
        print("=" * 80)
        
        print(f"\n1. ESTABILIDAD DEL TERRENO:")
        print(f"   ✓ Tierra estable: {'SÍ' if result.stability.is_stable else 'NO'}")
        if not result.stability.is_stable:
            print(f"   ✗ Razón de rechazo: {result.stability.rejection_reason}")
        else:
            print(f"   - Tipo de superficie: {result.stability.surface_type}")
            print(f"   - Pendiente: {result.stability.slope_degrees:.1f}°")
            print(f"   - NDVI medio: {result.stability.ndvi_mean:.3f}")
            print(f"   - Varianza térmica: {result.stability.thermal_variance:.1f}°C")
        
        if result.signals:
            print(f"\n2. SEÑALES DE VACÍO:")
            print(f"   SAR (peso 35%):")
            print(f"     - Score: {result.signals.sar_score:.3f}")
            print(f"     - Baja retrodispersión: {'✓' if result.signals.sar_low_backscatter else '✗'}")
            print(f"     - Caída de coherencia: {'✓' if result.signals.sar_coherence_drop else '✗'}")
            print(f"     - Simetría espacial: {'✓' if result.signals.sar_spatial_symmetry else '✗'}")
            
            print(f"   Térmico (peso 25%):")
            print(f"     - Score: {result.signals.thermal_score:.3f}")
            print(f"     - Anomalía nocturna: {result.signals.thermal_night_anomaly:.1f}°C")
            print(f"     - Desacople día/noche: {'✓' if result.signals.thermal_day_night_decoupling else '✗'}")
            print(f"     - Estabilidad temporal: {'✓' if result.signals.thermal_temporal_stable else '✗'}")
            
            print(f"   Humedad (peso 20%):")
            print(f"     - Score: {result.signals.humidity_score:.3f}")
            print(f"     - NDVI bajo: {'✓' if result.signals.humidity_ndvi_low else '✗'}")
            print(f"     - NDVI estable: {'✓' if result.signals.humidity_ndvi_stable else '✗'}")
            print(f"     - Persistencia: {'✓' if result.signals.humidity_persistent else '✗'}")
            
            print(f"   Micro-hundimiento (peso 20%):")
            print(f"     - Score: {result.signals.subsidence_score:.3f}")
            print(f"     - Depresión: {'✓' if result.signals.subsidence_depression else '✗'}")
            print(f"     - Simetría: {'✓' if result.signals.subsidence_symmetric else '✗'}")
            print(f"     - No erosión: {'✓' if result.signals.subsidence_not_erosion else '✗'}")
        
        print(f"\n3. PROBABILIDAD DE VACÍO:")
        print(f"   Score compuesto: {result.void_probability_score:.3f}")
        print(f"   Nivel: {result.void_probability_level.value.upper()}")
        print(f"   Clasificación: {result.classification.value}")
        
        print(f"\n4. INDICADORES GEOMÉTRICOS:")
        print(f"   Simetría: {result.geometric_symmetry:.3f}")
        print(f"   Ángulos rectos: {'✓' if result.right_angles else '✗'}")
        print(f"   Sesgo de orientación: {'✓' if result.orientation_bias else '✗'}")
        print(f"   Repetición modular: {'✓' if result.modular_repetition else '✗'}")
        
        print(f"\n5. CONCLUSIÓN CIENTÍFICA:")
        print(f"   {result.scientific_conclusion}")
        print(f"   Confianza de medida (sensores): {result.measurement_confidence:.1%}")
        print(f"   Confianza epistémica (inferencial): {result.epistemic_confidence:.1%}")
        
        # PASO 3.5: Validación Contextual (usando sitios conocidos como anclas)
        print(f"\n" + "=" * 80)
        print("PASO 3.5: Validación Contextual (Sitios Conocidos como Anclas)")
        print("-" * 80)
        
        # Mapear ambiente a tipo contextual
        env_type_map = {
            'desert': CtxEnvType.ARID,
            'semi_arid': CtxEnvType.SEMI_ARID,
            'mountain': CtxEnvType.MOUNTAIN,
            'grassland': CtxEnvType.GRASSLAND,
            'forest': CtxEnvType.FOREST,
            'coastal': CtxEnvType.COASTAL,
        }
        
        ctx_env = env_type_map.get(
            env_context.environment_type.value,
            CtxEnvType.UNKNOWN
        )
        
        validation = contextual_validator.validate_candidate(
            candidate_lat=lat,
            candidate_lon=lon,
            candidate_environment=ctx_env,
            candidate_terrain=env_context.environment_type.value,
            void_detection_result=result
        )
        
        print(f"\n📋 VALIDACIÓN CONTEXTUAL:")
        print(f"   Plausibilidad: {validation.plausibility_score:.3f}")
        print(f"   Es plausible: {'SÍ' if validation.is_plausible else 'NO'}")
        print(f"   Ambiente visto antes: {'✓' if validation.environment_seen_before else '✗'}")
        print(f"   Terreno compatible: {'✓' if validation.terrain_compatible else '✗'}")
        print(f"   Desviación de contexto: {validation.context_deviation:.3f}")
        print(f"   Riesgo de falso positivo: {validation.false_positive_risk:.3f}")
        print(f"   Sitios cercanos sin cavidades: {validation.similar_known_sites_without_cavities}")
        
        print(f"\n   AJUSTES RECOMENDADOS:")
        print(f"   Penalización al score: -{validation.score_penalty:.1%}")
        print(f"   Ajuste de confianza: {validation.confidence_adjustment:+.1%}")
        
        print(f"\n   NOTAS:")
        print(f"   {validation.validation_notes}")
        
        # Aplicar ajustes (se aplican principalmente a la confianza epistémica/solidez de inferencia)
        adjusted_score = max(0.0, result.void_probability_score - validation.score_penalty)
        adjusted_epistemic_conf = max(0.0, result.epistemic_confidence + validation.confidence_adjustment)
        
        print(f"\n   SCORES AJUSTADOS:")
        print(f"   Score original: {result.void_probability_score:.3f} → Ajustado: {adjusted_score:.3f}")
        print(f"   Confianza epistémica original: {result.epistemic_confidence:.1%} → Ajustada: {adjusted_epistemic_conf:.1%}")
        
        # PASO 4: Guardar en BD
        print(f"\n" + "=" * 80)
        print("PASO 4: Guardando Resultados en BD")
        print("-" * 80)
        
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO timt_analysis_results (
            lat, lon,
            analysis_type,
            void_probability_score,
            void_probability_level,
            void_classification,
            sar_score, thermal_score, humidity_score, subsidence_score,
            geometric_symmetry,
            scientific_conclusion,
            measurement_confidence,
            epistemic_confidence,
            is_stable_terrain,
            rejection_reason,
            created_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING id
        """
        
        cursor.execute(insert_query, (
            lat, lon,
            'subsurface_void_detection',
            result.void_probability_score,
            result.void_probability_level.value,
            result.classification.value,
            result.signals.sar_score if result.signals else None,
            result.signals.thermal_score if result.signals else None,
            result.signals.humidity_score if result.signals else None,
            result.signals.subsidence_score if result.signals else None,
            result.geometric_symmetry,
            result.scientific_conclusion,
            result.measurement_confidence,
            result.epistemic_confidence,
            result.stability.is_stable,
            result.stability.rejection_reason,
            datetime.utcnow()
        ))
        
        analysis_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Resultados guardados en BD (ID: {analysis_id})")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 80)
        print("✅ TEST COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        
        return 0
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("\nVerifica que:")
        print("  1. Estés en el directorio correcto")
        print("  2. El backend esté en ./backend/")
        print("  3. Todos los módulos existan")
        return 1
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def _generate_simulated_data(env_context):
    """Generar datos simulados para testing sin BD"""
    import random
    
    # Simular basado en tipo de ambiente
    if env_context.environment_type.value in ['desert', 'semi_arid']:
        # Desierto: buenas condiciones para detección
        return {
            'sar_backscatter_db': random.uniform(-18, -12),
            'sar_coherence': random.uniform(0.3, 0.7),
            'sar_spatial_symmetry': random.uniform(0.5, 0.8),
            'lst_day_celsius': random.uniform(35, 45),
            'lst_night_celsius': random.uniform(15, 20),
            'expected_night_temp': 18.0,
            'thermal_temporal_variance': random.uniform(1.0, 2.5),
            'ndvi_mean': random.uniform(0.05, 0.20),
            'ndvi_variance': random.uniform(0.02, 0.05),
            'ndvi_temporal_stability': random.uniform(0.7, 0.9),
            'elevation_anomaly': random.uniform(-1.0, 0.0),
            'depression_symmetry': random.uniform(0.6, 0.8),
            'erosion_likelihood': random.uniform(0.1, 0.3),
            'slope_degrees': random.uniform(2, 8),
            'thermal_variance': random.uniform(1.5, 3.0),
            'geometric_symmetry': random.uniform(0.5, 0.8),
            'right_angles_detected': random.choice([True, False]),
            'orientation_bias': random.uniform(0.4, 0.7),
            'modular_repetition': False,
            'data_quality_score': random.uniform(0.75, 0.95),
        }
    else:
        # Otros ambientes: condiciones normales
        return {
            'sar_backscatter_db': random.uniform(-12, -8),
            'sar_coherence': random.uniform(0.6, 0.9),
            'sar_spatial_symmetry': random.uniform(0.3, 0.5),
            'lst_day_celsius': random.uniform(25, 35),
            'lst_night_celsius': random.uniform(15, 22),
            'expected_night_temp': 18.0,
            'thermal_temporal_variance': random.uniform(2.0, 4.0),
            'ndvi_mean': random.uniform(0.25, 0.45),
            'ndvi_variance': random.uniform(0.05, 0.10),
            'ndvi_temporal_stability': random.uniform(0.5, 0.7),
            'elevation_anomaly': random.uniform(-0.3, 0.3),
            'depression_symmetry': random.uniform(0.3, 0.5),
            'erosion_likelihood': random.uniform(0.4, 0.6),
            'slope_degrees': random.uniform(5, 12),
            'thermal_variance': random.uniform(2.5, 4.5),
            'geometric_symmetry': random.uniform(0.3, 0.5),
            'right_angles_detected': False,
            'orientation_bias': random.uniform(0.3, 0.5),
            'modular_repetition': False,
            'data_quality_score': random.uniform(0.65, 0.85),
        }


def main():
    parser = argparse.ArgumentParser(
        description='Test detección de subestructuras huecas con BD real'
    )
    parser.add_argument('--lat', type=float, required=True, help='Latitud')
    parser.add_argument('--lon', type=float, required=True, help='Longitud')
    
    args = parser.parse_args()
    
    return test_void_detection_with_real_data(args.lat, args.lon)


if __name__ == "__main__":
    sys.exit(main())
