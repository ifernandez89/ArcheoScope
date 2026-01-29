#!/usr/bin/env python3
"""
Test TOP TIER - Oasis Antiguos Sahara (Egipto Occidental) CON GUARDADO EN BD
=============================================================================

IMPORTANTE: Este script SIEMPRE guarda los resultados en la base de datos.

Zona: Oasis Antiguos - Sahara (Egipto Occidental)
Coordenadas: 25.5 a 26.5 (Lat), 28.0 a 29.0 (Lon)

CARACTERÍSTICAS:
- Paleohidrología (antiguos sistemas hídricos)
- Asentamientos perdidos bajo arena
- Agricultura fósil (trazas de irrigación)
- Aridez extrema actual (preservación excelente)

Objetivos de detección:
- Anomalías de humedad (paleocauces)
- Trazas agrícolas fósiles (campos irrigados)
- Estructuras cubiertas por arena (asentamientos)
- Modificación del suelo (ocupación histórica)
"""

import asyncio
import sys
import json
import asyncpg
from pathlib import Path
from datetime import datetime
from uuid import uuid4

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
from etp_generator import ETProfileGenerator, BoundingBox


async def save_to_database(etp, bounds, region_name: str):
    """
    Guardar resultados en la base de datos PostgreSQL.
    
    CRÍTICO: Esta función SIEMPRE debe ejecutarse después de un análisis.
    """
    print()
    print("="*80)
    print("💾 GUARDANDO EN BASE DE DATOS")
    print("="*80)
    print()
    
    try:
        # Conectar a la base de datos
        conn = await asyncpg.connect(
            'postgresql://postgres:1464@localhost:5433/archeoscope_db'
        )
        print("✅ Conexión a BD establecida")
        
        # Preparar datos para inserción
        detection_id = str(uuid4())
        
        # Convertir measurements a JSON
        measurements_json = {
            "ess_superficial": float(etp.ess_superficial),
            "ess_volumetrico": float(etp.ess_volumetrico),
            "ess_temporal": float(etp.ess_temporal),
            "coherencia_3d": float(etp.coherencia_3d),
            "persistencia_temporal": float(etp.persistencia_temporal),
            "densidad_arqueologica_m3": float(etp.densidad_arqueologica_m3),
            "instrumental_coverage": etp.instrumental_coverage,
            "tas": etp.tas_signature.to_dict() if etp.tas_signature else None,
            "dil": etp.dil_signature.to_dict() if etp.dil_signature else None,
            "geological_compatibility": {
                "gcs_score": float(etp.geological_compatibility.gcs_score)
            } if etp.geological_compatibility else None,
            "water_availability": {
                "holocene_availability": float(etp.water_availability.holocene_availability)
            } if etp.water_availability else None,
            "external_consistency": {
                "ecs_score": float(etp.external_consistency.ecs_score)
            } if etp.external_consistency else None
        }
        
        # Determinar environment type
        if etp.ess_superficial < 0.2:
            environment_type = "DESERT"
        elif etp.ess_superficial < 0.4:
            environment_type = "SEMI_ARID"
        else:
            environment_type = "AGRICULTURAL"
        
        # Determinar confidence level
        if etp.ess_volumetrico > 0.60:
            confidence_level = "high"
        elif etp.ess_volumetrico > 0.45:
            confidence_level = "moderate"
        else:
            confidence_level = "low"
        
        # Calcular convergencia instrumental
        total_instruments = (
            etp.instrumental_coverage['superficial']['total'] +
            etp.instrumental_coverage['subsuperficial']['total'] +
            etp.instrumental_coverage['profundo']['total']
        )
        successful_instruments = (
            etp.instrumental_coverage['superficial']['successful'] +
            etp.instrumental_coverage['subsuperficial']['successful'] +
            etp.instrumental_coverage['profundo']['successful']
        )
        
        # Insertar en detection_history
        await conn.execute("""
            INSERT INTO detection_history (
                id,
                "regionName",
                "latMin",
                "latMax",
                "lonMin",
                "lonMax",
                "environmentDetected",
                "environmentConfidence",
                "archaeologicalProbability",
                "confidenceLevel",
                "instrumentsConverging",
                "minimumRequired",
                "convergenceMet",
                "siteRecognized",
                measurements,
                "detectionDate",
                "analysisVersion"
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17
            )
        """,
            detection_id,
            region_name,
            float(bounds.lat_min),
            float(bounds.lat_max),
            float(bounds.lon_min),
            float(bounds.lon_max),
            environment_type,
            float(etp.coherencia_3d),  # Usamos coherencia como confidence
            float(etp.ess_volumetrico),  # ESS como probabilidad arqueológica
            confidence_level,
            successful_instruments,
            2,  # Mínimo requerido
            successful_instruments >= 2,
            False,  # No es sitio reconocido
            json.dumps(measurements_json),
            datetime.now(),
            "ArcheoScope v1.0 + TAS + DIL"
        )
        
        print(f"✅ Registro guardado en BD con ID: {detection_id}")
        print(f"   Región: {region_name}")
        print(f"   ESS Volumétrico: {etp.ess_volumetrico:.3f}")
        print(f"   Ambiente: {environment_type}")
        print(f"   Confianza: {confidence_level}")
        print(f"   Instrumentos: {successful_instruments}/{total_instruments}")
        
        await conn.close()
        print("✅ Conexión a BD cerrada")
        
        return detection_id
        
    except Exception as e:
        print(f"❌ ERROR guardando en BD: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_oasis_sahara():
    """Test de Oasis Antiguos del Sahara (Egipto Occidental)."""
    
    print("="*80)
    print("💧 ArcheoScope - Test TOP TIER: Oasis Antiguos Sahara (Egipto)")
    print("="*80)
    print()
    print("📍 Región: Oasis Antiguos - Sahara (Egipto Occidental)")
    print("   Características:")
    print("   - Paleohidrología (antiguos sistemas hídricos)")
    print("   - Asentamientos perdidos bajo arena")
    print("   - Agricultura fósil (trazas de irrigación)")
    print("   - Aridez extrema actual (preservación excelente)")
    print()
    print("🏛️ Contexto arqueológico:")
    print("   - Oasis del Desierto Occidental (Farafra, Dakhla, Kharga)")
    print("   - Ocupación desde el Paleolítico")
    print("   - Agricultura egipcia antigua")
    print("   - Rutas comerciales trans-saharianas")
    print()
    print("🎯 Objetivos de detección:")
    print("   - Anomalías de humedad (paleocauces)")
    print("   - Trazas agrícolas fósiles (campos irrigados)")
    print("   - Estructuras cubiertas por arena (asentamientos)")
    print("   - Modificación del suelo (ocupación histórica)")
    print()
    
    # Definir región de interés (centro del rango sugerido)
    lat_center = 26.0
    lon_center = 28.5
    size_km = 15.0
    
    lat_offset = size_km / 111.32 / 2
    lon_offset = size_km / (111.32 * abs(lat_center)) / 2
    
    bounds = BoundingBox(
        lat_min=lat_center - lat_offset,
        lat_max=lat_center + lat_offset,
        lon_min=lon_center - lon_offset,
        lon_max=lon_center + lon_offset,
        depth_min=0.0,
        depth_max=-5.0  # Estructuras bajo arena
    )
    
    region_name = "Oasis Antiguos - Sahara (Egipto Occidental)"
    
    print(f"📦 Bounding Box:")
    print(f"   Lat: [{bounds.lat_min:.4f}, {bounds.lat_max:.4f}]")
    print(f"   Lon: [{bounds.lon_min:.4f}, {bounds.lon_max:.4f}]")
    print(f"   Área: {bounds.area_km2:.2f} km²")
    print(f"   Altitud: ~100-200 msnm")
    print()
    
    try:
        # Inicializar componentes
        print("🔧 Inicializando componentes...")
        integrator = RealDataIntegratorV2()
        etp_generator = ETProfileGenerator(integrator)
        print("   ✅ Componentes inicializados")
        print()
        
        # Generar ETP
        print("🔬 Generando ETP (resolución 150m, protocolo canónico)...")
        print("   Prioridad: SAR + Thermal + NDVI + Temporal")
        print("   Ventana temporal: 5 años")
        print("   Búsqueda: Paleohidrología + Agricultura fósil")
        print()
        
        etp = await etp_generator.generate_etp(bounds, resolution_m=150.0)
        
        print()
        print("="*80)
        print("📊 RESULTADOS CIENTÍFICOS - OASIS SAHARA EGIPTO")
        print("="*80)
        print()
        
        # Métricas principales
        print("📈 MÉTRICAS PRINCIPALES:")
        print(f"   ESS Superficial:    {etp.ess_superficial:.3f}")
        print(f"   ESS Volumétrico:    {etp.ess_volumetrico:.3f}")
        print(f"   ESS Temporal:       {etp.ess_temporal:.3f}")
        print(f"   Coherencia 3D:      {etp.coherencia_3d:.3f}")
        print(f"   Persistencia Temp:  {etp.persistencia_temporal:.3f}")
        print(f"   Densidad Arq m³:    {etp.densidad_arqueologica_m3:.3f}")
        print()
        
        # Cobertura instrumental
        print("📊 COBERTURA INSTRUMENTAL:")
        cov = etp.instrumental_coverage
        print(f"   🌍 Superficial:     {cov['superficial']['percentage']:.0f}% ({cov['superficial']['successful']}/{cov['superficial']['total']})")
        print(f"   📡 Subsuperficial:  {cov['subsuperficial']['percentage']:.0f}% ({cov['subsuperficial']['successful']}/{cov['subsuperficial']['total']})")
        print(f"   🔬 Profundo:        {cov['profundo']['percentage']:.0f}% ({cov['profundo']['successful']}/{cov['profundo']['total']})")
        print()
        
        # TAS
        if etp.tas_signature:
            print("🕐 TEMPORAL ARCHAEOLOGICAL SIGNATURE (TAS):")
            print(f"   TAS Score:          {etp.tas_signature.tas_score:.3f}")
            print(f"   NDVI Persistence:   {etp.tas_signature.ndvi_persistence:.3f}")
            print(f"   Thermal Stability:  {etp.tas_signature.thermal_stability:.3f}")
            print(f"   SAR Coherence:      {etp.tas_signature.sar_coherence:.3f}")
            print(f"   Stress Frequency:   {etp.tas_signature.stress_frequency:.3f}")
            print()
        
        # DIL
        if etp.dil_signature:
            print("🔬 DEEP INFERENCE LAYER (DIL):")
            print(f"   DIL Score:          {etp.dil_signature.dil_score:.3f}")
            print(f"   Profundidad est:    {etp.dil_signature.estimated_depth_m:.1f}m")
            print(f"   Confianza:          {etp.dil_signature.confidence:.3f}")
            print(f"   Relevancia Arq:     {etp.dil_signature.archaeological_relevance:.3f}")
            print()
        
        # Comparación con otros desiertos
        print("="*80)
        print("📊 COMPARACIÓN CON OTROS DESIERTOS")
        print("="*80)
        print()
        print("Desiertos sudamericanos:")
        print("   Atacama Interior:    ESS 0.477 (agricultura prehispánica)")
        print("   Altiplano Andino:    ESS 0.467 (pastoral andino)")
        print()
        print("Desierto africano:")
        print(f"   Sahara Egipto:       ESS {etp.ess_volumetrico:.3f} (paleohidrología)")
        print()
        
        # Clasificación según escala calibrada
        if etp.ess_volumetrico < 0.30:
            clasificacion = "PISO - Sin huella humana persistente"
            emoji = "🟢"
        elif 0.30 <= etp.ess_volumetrico < 0.45:
            clasificacion = "INTERMEDIO - Señal moderada"
            emoji = "🟠"
        elif 0.45 <= etp.ess_volumetrico <= 0.60:
            clasificacion = "ZONA HABITABLE - Paisaje cultural difuso"
            emoji = "🟡"
        else:
            clasificacion = "TECHO - Paisaje antropizado intenso"
            emoji = "🔴"
        
        print(f"{emoji} CLASIFICACIÓN: {clasificacion}")
        print()
        
        # Análisis específico para oasis saharianos
        print("="*80)
        print("🔍 ANÁLISIS ESPECÍFICO - OASIS SAHARIANOS")
        print("="*80)
        print()
        
        if etp.ess_volumetrico > 0.45:
            print("✅ SEÑAL ARQUEOLÓGICA CLARA")
            print()
            print("Señales detectadas:")
            if etp.tas_signature and etp.tas_signature.thermal_stability > 0.7:
                print("  • Persistencia térmica → modificación del suelo")
            if etp.tas_signature and etp.tas_signature.sar_coherence > 0.5:
                print("  • SAR coherente → estructuras bajo arena")
            if etp.tas_signature and etp.tas_signature.ndvi_persistence > 0.2:
                print("  • NDVI persistente → trazas agrícolas fósiles")
            if etp.dil_signature and etp.dil_signature.dil_score > 0.5:
                print(f"  • DIL alto → profundidad estimada {etp.dil_signature.estimated_depth_m:.1f}m")
            
            print()
            print("Características saharianas probables:")
            print("  - Paleocauces (antiguos ríos secos)")
            print("  - Campos irrigados fósiles")
            print("  - Asentamientos bajo arena")
            print("  - Pozos y sistemas hídricos antiguos")
            print("  - Rutas comerciales trans-saharianas")
            
        elif 0.30 < etp.ess_volumetrico <= 0.45:
            print("⚠️ SEÑAL MODERADA")
            print()
            print("Posible ocupación histórica:")
            print("  - Campamentos temporales")
            print("  - Tránsito de caravanas")
            print("  - Agricultura limitada")
            print("  - Señal arqueológica débil pero presente")
            
        else:
            print("🟢 SEÑAL BAJA")
            print()
            print("Paisaje desértico sin ocupación humana significativa")
            print("Posible zona sin agua histórica")
        
        print()
        
        # Análisis paleohidrológico
        print("="*80)
        print("💧 ANÁLISIS PALEOHIDROLÓGICO")
        print("="*80)
        print()
        
        if etp.water_availability and etp.water_availability.holocene_availability > 0.5:
            print("✅ DISPONIBILIDAD DE AGUA HISTÓRICA DETECTADA")
            print(f"   Holoceno: {etp.water_availability.holocene_availability:.3f}")
            print()
            print("Esto sugiere:")
            print("  • Paleocauces activos en el Holoceno")
            print("  • Oasis con agua permanente o estacional")
            print("  • Agricultura viable históricamente")
            print("  • Asentamientos humanos sostenibles")
        else:
            print("⚠️ DISPONIBILIDAD DE AGUA HISTÓRICA BAJA")
            if etp.water_availability:
                print(f"   Holoceno: {etp.water_availability.holocene_availability:.3f}")
            print()
            print("Esto sugiere:")
            print("  • Zona árida incluso en el Holoceno")
            print("  • Ocupación humana limitada")
            print("  • Dependencia de pozos profundos")
        
        print()
        
        # Comparación con Atacama
        print("="*80)
        print("📊 COMPARACIÓN: SAHARA vs ATACAMA")
        print("="*80)
        print()
        
        print("Atacama (Sudamérica):")
        print("   ESS: 0.477")
        print("   Tipo: Agricultura prehispánica (terrazas, canales)")
        print("   Agua: Escasa pero presente (quebradas)")
        print()
        
        print("Sahara (África):")
        print(f"   ESS: {etp.ess_volumetrico:.3f}")
        print("   Tipo: Paleohidrología + agricultura fósil")
        print("   Agua: Paleocauces (antiguos ríos)")
        print()
        
        diferencia = etp.ess_volumetrico - 0.477
        print(f"Diferencia: {diferencia:+.3f}")
        if abs(diferencia) < 0.05:
            print("   → Señales comparables (ambos desiertos con agricultura)")
        elif diferencia > 0.05:
            print("   → Sahara con señal MÁS FUERTE (paleohidrología más visible)")
        else:
            print("   → Atacama con señal MÁS FUERTE (terrazas más visibles)")
        
        print()
        
        # Guardar resultado en JSON
        result = {
            "nombre": "Oasis Antiguos - Sahara (Egipto Occidental)",
            "coordenadas": {
                "lat_center": lat_center,
                "lon_center": lon_center,
                "lat_min": bounds.lat_min,
                "lat_max": bounds.lat_max,
                "lon_min": bounds.lon_min,
                "lon_max": bounds.lon_max
            },
            "timestamp": datetime.now().isoformat(),
            "clasificacion": clasificacion,
            "comparacion_atacama": {
                "atacama_ess": 0.477,
                "sahara_ess": float(etp.ess_volumetrico),
                "diferencia": float(diferencia)
            },
            "metricas": {
                "ess_superficial": float(etp.ess_superficial),
                "ess_volumetrico": float(etp.ess_volumetrico),
                "ess_temporal": float(etp.ess_temporal),
                "coherencia_3d": float(etp.coherencia_3d),
                "persistencia_temporal": float(etp.persistencia_temporal),
                "densidad_arqueologica_m3": float(etp.densidad_arqueologica_m3)
            },
            "cobertura": etp.instrumental_coverage,
            "tas": etp.tas_signature.to_dict() if etp.tas_signature else None,
            "dil": etp.dil_signature.to_dict() if etp.dil_signature else None,
            "water_availability": {
                "holocene_availability": float(etp.water_availability.holocene_availability)
            } if etp.water_availability else None
        }
        
        output_file = f"oasis_sahara_egipto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"💾 Resultados guardados en JSON: {output_file}")
        print()
        
        # GUARDAR EN BASE DE DATOS (CRÍTICO)
        detection_id = await save_to_database(etp, bounds, region_name)
        
        if detection_id:
            print()
            print("="*80)
            print("✅ ANÁLISIS COMPLETADO Y GUARDADO EN BD")
            print("="*80)
            print(f"   ID de detección: {detection_id}")
        else:
            print()
            print("="*80)
            print("⚠️ ANÁLISIS COMPLETADO PERO NO SE GUARDÓ EN BD")
            print("="*80)
        
        return result, detection_id
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    asyncio.run(test_oasis_sahara())
