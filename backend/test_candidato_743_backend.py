#!/usr/bin/env python3
"""
Test Candidato 743 - Ejecutado desde backend/
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/archeoscope")

async def test_candidato_743():
    """Test del candidato 743 usando pipeline científico"""
    
    print("=" * 80)
    print("🔬 TEST CANDIDATO 743 - PIPELINE CIENTÍFICO")
    print("=" * 80)
    
    try:
        # Conectar a BD
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Conectado a BD")
        
        # Obtener candidato 743
        print("\n📍 Buscando candidato 743...")
        
        candidato = await conn.fetchrow("""
            SELECT id, name, slug, "siteType", "environmentType", "confidenceLevel",
                   latitude, longitude, country, region, description, "createdAt"
            FROM archaeological_sites
            ORDER BY "createdAt" DESC
            LIMIT 1 OFFSET 742
        """)
        
        if not candidato:
            print("❌ Candidato 743 no encontrado")
            await conn.close()
            return
        
        print(f"✅ Candidato encontrado:")
        print(f"   ID: {candidato['id']}")
        print(f"   Nombre: {candidato['name']}")
        print(f"   País: {candidato['country']}")
        print(f"   Coordenadas: {candidato['latitude']}, {candidato['longitude']}")
        print(f"   Tipo: {candidato['siteType']}")
        print(f"   Ambiente: {candidato['environmentType']}")
        print(f"   Confianza: {candidato['confidenceLevel']}")
        
        # Crear pool de BD
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
        
        # Importar componentes
        print("\n🔧 Inicializando componentes...")
        from scientific_pipeline import ScientificPipeline
        from validation.real_archaeological_validator import RealArchaeologicalValidator
        from environment_classifier import EnvironmentClassifier
        from satellite_connectors.real_data_integrator import RealDataIntegrator
        
        validator = RealArchaeologicalValidator()
        classifier = EnvironmentClassifier()
        integrator = RealDataIntegrator()
        pipeline = ScientificPipeline(db_pool=db_pool, validator=validator)
        
        print("✅ Componentes inicializados")
        
        # Preparar coordenadas
        lat = float(candidato['latitude'])
        lon = float(candidato['longitude'])
        
        lat_min = lat - 0.01
        lat_max = lat + 0.01
        lon_min = lon - 0.01
        lon_max = lon + 0.01
        
        center_lat = (lat_min + lat_max) / 2
        center_lon = (lon_min + lon_max) / 2
        
        print(f"\n🔬 Ejecutando análisis...")
        print(f"   Centro: {center_lat:.6f}, {center_lon:.6f}")
        
        # PASO 1: Clasificar ambiente
        print("\n[PASO 1] Clasificando ambiente...")
        env_context = classifier.classify(center_lat, center_lon)
        print(f"  ✅ Ambiente: {env_context.environment_type.value}")
        print(f"  ✅ Confianza: {env_context.confidence:.2f}")
        
        # PASO 2: Medir con instrumentos
        print("\n[PASO 2] Midiendo con instrumentos...")
        all_instruments = list(set(env_context.primary_sensors + env_context.secondary_sensors))
        print(f"  Total instrumentos: {len(all_instruments)}")
        
        measurements = []
        for instrument_name in all_instruments:
            try:
                measurement = await integrator.get_instrument_measurement(
                    instrument_name=instrument_name,
                    lat_min=lat_min,
                    lat_max=lat_max,
                    lon_min=lon_min,
                    lon_max=lon_max
                )
                if measurement is not None:
                    measurements.append(measurement)
                    print(f"  ✅ {instrument_name}: {measurement.get('value', 0):.3f}")
                else:
                    print(f"  ❌ {instrument_name}: Sin datos")
            except Exception as e:
                print(f"  ❌ {instrument_name}: Error")
                continue
        
        print(f"\n  📊 {len(measurements)}/{len(all_instruments)} instrumentos exitosos")
        
        # PASO 3: Preparar datos
        print("\n[PASO 3] Preparando datos...")
        raw_measurements = {
            'candidate_id': str(candidato['id']),
            'region_name': candidato['name'],
            'center_lat': center_lat,
            'center_lon': center_lon,
            'environment_type': env_context.environment_type.value,
            'instruments_available': len(all_instruments)
        }
        
        for m in measurements:
            if m is not None:
                instrument_name = m.get('instrument_name', 'unknown')
                raw_measurements[instrument_name] = {
                    'value': m.get('value', 0),
                    'threshold': m.get('threshold', 0),
                    'exceeds_threshold': m.get('exceeds_threshold', False),
                    'confidence': m.get('confidence', 0),
                    'data_mode': m.get('data_mode', 'unknown'),
                    'source': m.get('source', 'unknown')
                }
        
        # PASO 4: Ejecutar pipeline
        print("\n[PASO 4] Ejecutando pipeline científico...")
        result = await pipeline.analyze(
            raw_measurements,
            lat_min, lat_max,
            lon_min, lon_max
        )
        
        print("\n✅ Análisis completado")
        
        # Extraer resultados
        output = result.get('scientific_output', {})
        
        print(f"\n" + "=" * 80)
        print("📊 RESULTADOS CIENTÍFICOS")
        print("=" * 80)
        
        print(f"\n🎯 MÉTRICAS SEPARADAS:")
        print(f"   Origen Antropogénico: {output.get('anthropic_origin_probability', 0):.1%}")
        print(f"   Actividad Antropogénica: {output.get('anthropic_activity_probability', 0):.1%}")
        print(f"   Anomalía Instrumental: {output.get('instrumental_anomaly_probability', 0):.1%}")
        print(f"   Confianza del Modelo: {output.get('model_inference_confidence', 'unknown')}")
        
        # ESS
        ess = output.get('explanatory_strangeness', {})
        if ess:
            print(f"\n🔮 ESS (Explanatory Strangeness Score):")
            if isinstance(ess, dict):
                print(f"   Nivel: {ess.get('level', 'none').upper()}")
                print(f"   Score: {ess.get('score', 0):.3f}")
                if ess.get('explanation'):
                    print(f"   Explicación: {ess.get('explanation', 'N/A')[:100]}...")
            else:
                print(f"   Valor: {ess}")
        
        # Instrumentos
        print(f"\n🛰️ COBERTURA INSTRUMENTAL:")
        print(f"   Medidos: {output.get('instruments_measured', 0)}/{output.get('instruments_available', 10)}")
        print(f"   Cobertura raw: {output.get('coverage_raw', 0):.1%}")
        print(f"   Cobertura normalizada: {output.get('coverage_normalized', 0):.1%}")
        
        # Recomendación
        print(f"\n💡 RECOMENDACIÓN:")
        print(f"   Acción: {output.get('recommended_action', 'unknown')}")
        print(f"   Tipo: {output.get('candidate_type', 'unknown')}")
        print(f"   Prioridad: {output.get('priority_score', 0):.2f}")
        
        # Guardar resultados
        import json
        from datetime import datetime
        
        output_file = f"../candidato_743_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'candidato': dict(candidato),
                'analisis': result
            }, f, indent=2, default=str, ensure_ascii=False)
        
        print(f"\n💾 Resultados guardados en: {output_file}")
        print("\n" + "=" * 80)
        print("✅ TEST COMPLETADO CON ÉXITO")
        print("=" * 80)
        
        # Cerrar conexiones
        await db_pool.close()
        await conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_candidato_743())
