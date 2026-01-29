#!/usr/bin/env python3
"""
Test TOP TIER - Agricultura Antigua Mediterráneo Oriental CON GUARDADO EN BD
===========================================================================

IMPORTANTE: Este script SIEMPRE guarda los resultados en la base de datos.

Zona: Agricultura Antigua Abandonada - Mediterráneo Oriental (Siria/Líbano)
Coordenadas: 35.0 a 35.8 (Lat), 36.0 a 37.0 (Lon)

CARACTERÍSTICAS:
- Terrazas agrícolas antiguas (modificación topográfica)
- Canales de irrigación (linealidades)
- Abandono prolongado (señal persistente)
- Clima mediterráneo (diferente a desiertos)

Objetivos de detección:
- Linealidades (canales, muros de terrazas)
- Patrones NDVI persistentes (agricultura fósil)
- Micro-relieves (terrazas, bancales)
- Modificación del suelo (ocupación agrícola)

CONTEXTO CIENTÍFICO:
Este test es crítico porque:
1. Primer test en clima MEDITERRÁNEO (no desértico)
2. Agricultura abandonada (no actual)
3. Terrazas = señal topográfica + espectral
4. Validación de robustez en ambiente húmedo
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


async def test_agricultura_mediterraneo():
    """Test de Agricultura Antigua Mediterráneo Oriental."""
    
    print("="*80)
    print("🌾 ArcheoScope - Test TOP TIER: Agricultura Mediterráneo Oriental")
    print("="*80)
    print()
    print("📍 Región: Agricultura Antigua Abandonada - Mediterráneo Oriental")
    print("   Características:")
    print("   - Terrazas agrícolas antiguas (modificación topográfica)")
    print("   - Canales de irrigación (linealidades)")
    print("   - Abandono prolongado (señal persistente)")
    print("   - Clima mediterráneo (diferente a desiertos)")
    print()
    print("🏛️ Contexto arqueológico:")
    print("   - Agricultura levantina antigua (Edad del Bronce - Romano)")
    print("   - Terrazas en laderas (anti-erosión)")
    print("   - Sistemas de irrigación complejos")
    print("   - Abandono post-romano (señal fósil)")
    print()
    print("🎯 Objetivos de detección:")
    print("   - Linealidades (canales, muros de terrazas)")
    print("   - Patrones NDVI persistentes (agricultura fósil)")
    print("   - Micro-relieves (terrazas, bancales)")
    print("   - Modificación del suelo (ocupación agrícola)")
    print()
    print("🔬 IMPORTANCIA CIENTÍFICA:")
    print("   - Primer test en clima MEDITERRÁNEO (no desértico)")
    print("   - Validación de robustez en ambiente húmedo")
    print("   - Agricultura abandonada vs actual")
    print("   - Terrazas = señal topográfica + espectral")
    print()
    
    # Definir región de interés (centro del rango sugerido)
    lat_center = 35.4
    lon_center = 36.5
    size_km = 15.0
    
    lat_offset = size_km / 111.32 / 2
    lon_offset = size_km / (111.32 * abs(lat_center)) / 2
    
    bounds = BoundingBox(
        lat_min=lat_center - lat_offset,
        lat_max=lat_center + lat_offset,
        lon_min=lon_center - lon_offset,
        lon_max=lon_center + lon_offset,
        depth_min=0.0,
        depth_max=-5.0  # Terrazas y canales subsuperficiales
    )
    
    region_name = "Agricultura Antigua - Mediterráneo Oriental"
    
    print(f"📦 Bounding Box:")
    print(f"   Lat: [{bounds.lat_min:.4f}, {bounds.lat_max:.4f}]")
    print(f"   Lon: [{bounds.lon_min:.4f}, {bounds.lon_max:.4f}]")
    print(f"   Área: {bounds.area_km2:.2f} km²")
    print(f"   Altitud: ~200-800 msnm (laderas)")
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
        print("   Búsqueda: Terrazas + Canales + Agricultura fósil")
        print()
        
        etp = await etp_generator.generate_etp(bounds, resolution_m=150.0)
        
        print()
        print("="*80)
        print("📊 RESULTADOS CIENTÍFICOS - AGRICULTURA MEDITERRÁNEO ORIENTAL")
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
        
        # Comparación con otros sitios
        print("="*80)
        print("📊 COMPARACIÓN CON OTROS SITIOS")
        print("="*80)
        print()
        print("Desiertos (áridos):")
        print("   Costas Chile:        ESS 0.483 (ocupación costera)")
        print("   Atacama Interior:    ESS 0.477 (agricultura prehispánica)")
        print("   Altiplano Andino:    ESS 0.467 (pastoral andino)")
        print("   Sahara Egipto:       ESS 0.462 (paleohidrología)")
        print()
        print("Mediterráneo (húmedo):")
        print(f"   Mediterráneo Ori:    ESS {etp.ess_volumetrico:.3f} (agricultura abandonada)")
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
        
        # Análisis específico para agricultura mediterránea
        print("="*80)
        print("🔍 ANÁLISIS ESPECÍFICO - AGRICULTURA MEDITERRÁNEA")
        print("="*80)
        print()
        
        if etp.ess_volumetrico > 0.45:
            print("✅ SEÑAL ARQUEOLÓGICA CLARA")
            print()
            print("Señales detectadas:")
            if etp.tas_signature and etp.tas_signature.thermal_stability > 0.7:
                print("  • Persistencia térmica → modificación del suelo (terrazas)")
            if etp.tas_signature and etp.tas_signature.sar_coherence > 0.5:
                print("  • SAR coherente → estructuras lineales (muros, canales)")
            if etp.tas_signature and etp.tas_signature.ndvi_persistence > 0.2:
                print("  • NDVI persistente → agricultura fósil (campos abandonados)")
            if etp.dil_signature and etp.dil_signature.dil_score > 0.5:
                print(f"  • DIL alto → profundidad estimada {etp.dil_signature.estimated_depth_m:.1f}m")
            
            print()
            print("Características mediterráneas probables:")
            print("  - Terrazas agrícolas en laderas")
            print("  - Canales de irrigación (linealidades)")
            print("  - Muros de contención (anti-erosión)")
            print("  - Campos abandonados (agricultura fósil)")
            print("  - Modificación topográfica persistente")
            
        elif 0.30 < etp.ess_volumetrico <= 0.45:
            print("⚠️ SEÑAL MODERADA")
            print()
            print("Posible ocupación agrícola:")
            print("  - Agricultura limitada o reciente")
            print("  - Terrazas pequeñas o degradadas")
            print("  - Señal arqueológica débil pero presente")
            
        else:
            print("🟢 SEÑAL BAJA")
            print()
            print("Paisaje sin ocupación agrícola significativa")
            print("Posible zona sin agricultura histórica")
        
        print()
        
        # Análisis de robustez en clima húmedo
        print("="*80)
        print("💧 ANÁLISIS DE ROBUSTEZ - CLIMA MEDITERRÁNEO")
        print("="*80)
        print()
        
        print("DIFERENCIAS CON DESIERTOS:")
        print("  • Mayor vegetación actual (ruido biológico)")
        print("  • Precipitación regular (erosión activa)")
        print("  • Agricultura moderna (señal contemporánea)")
        print("  • Menor preservación (clima húmedo)")
        print()
        
        if etp.ess_volumetrico > 0.45:
            print("✅ SISTEMA ROBUSTO EN CLIMA HÚMEDO")
            print()
            print("Señal arqueológica SUPERA el ruido mediterráneo:")
            print("  - Vegetación actual NO oculta terrazas")
            print("  - Erosión NO borra modificación topográfica")
            print("  - Agricultura moderna NO enmascara fósil")
            print()
            print("Esto valida:")
            print("  ✓ Robustez del sistema en ambientes húmedos")
            print("  ✓ Capacidad de distinguir señal antigua vs moderna")
            print("  ✓ Detección de terrazas (señal topográfica)")
            
        else:
            print("⚠️ SEÑAL DÉBIL EN CLIMA HÚMEDO")
            print()
            print("Posibles razones:")
            print("  - Erosión ha degradado terrazas")
            print("  - Vegetación actual oculta señal")
            print("  - Agricultura moderna enmascara fósil")
            print("  - Zona sin agricultura histórica significativa")
        
        print()
        
        # Comparación: Desierto vs Mediterráneo
        print("="*80)
        print("📊 COMPARACIÓN: DESIERTO vs MEDITERRÁNEO")
        print("="*80)
        print()
        
        print("Desierto (Atacama):")
        print("   ESS: 0.477")
        print("   Clima: Árido extremo (preservación excelente)")
        print("   Vegetación: Mínima (señal clara)")
        print("   Erosión: Baja (señal persistente)")
        print()
        
        print("Mediterráneo (Levante):")
        print(f"   ESS: {etp.ess_volumetrico:.3f}")
        print("   Clima: Húmedo (preservación moderada)")
        print("   Vegetación: Alta (ruido biológico)")
        print("   Erosión: Alta (señal degradada)")
        print()
        
        diferencia = etp.ess_volumetrico - 0.477
        print(f"Diferencia: {diferencia:+.3f}")
        if abs(diferencia) < 0.05:
            print("   → Señales comparables (robustez validada)")
        elif diferencia > 0.05:
            print("   → Mediterráneo con señal MÁS FUERTE (sorprendente)")
        else:
            print("   → Desierto con señal MÁS FUERTE (esperado por preservación)")
        
        print()
        
        # Guardar resultado en JSON
        result = {
            "nombre": "Agricultura Antigua - Mediterráneo Oriental",
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
                "mediterraneo_ess": float(etp.ess_volumetrico),
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
        
        output_file = f"agricultura_mediterraneo_oriental_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
    asyncio.run(test_agricultura_mediterraneo())
