#!/usr/bin/env python3
"""
Test TOP TIER - Patagonia Árida (Meseta Central) CON GUARDADO EN BD
====================================================================

IMPORTANTE: Este script SIEMPRE guarda los resultados en la base de datos.

Zona: Meseta Central Patagónica (Argentina)
Coordenadas: -46.5 a -47.5 (Lat), -69.5 a -68.5 (Lon)

Características:
- Desierto frío
- Baja vegetación (estepa patagónica)
- Buena coherencia SAR
- Preservación excepcional por aridez

Objetivos de detección:
- Corrales prehispánicos
- Estructuras circulares (chenques, parapetos)
- Ocupaciones dispersas (cazadores-recolectores)
- Cuevas colapsadas
- Arte rupestre asociado
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
        elif etp.ess_superficial < 0.6:
            environment_type = "GRASSLAND"
        else:
            environment_type = "UNKNOWN"
        
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


async def test_patagonia_meseta():
    """Test de la Meseta Central Patagónica con guardado en BD."""
    
    print("="*80)
    print("🧊 ArcheoScope - Test TOP TIER: Patagonia Árida (Meseta Central)")
    print("="*80)
    print()
    print("📍 Región: Meseta Central Patagónica (Argentina)")
    print("   Características:")
    print("   - Desierto frío (estepa patagónica)")
    print("   - Baja vegetación (arbustos dispersos)")
    print("   - Buena coherencia SAR (sin ruido biológico)")
    print("   - Preservación excepcional por aridez")
    print()
    print("🎯 Objetivos de detección:")
    print("   - Corrales prehispánicos (manejo de guanacos)")
    print("   - Estructuras circulares (chenques, parapetos)")
    print("   - Ocupaciones dispersas (cazadores-recolectores)")
    print("   - Cuevas colapsadas")
    print("   - Arte rupestre asociado")
    print()
    
    # Definir región de interés (centro del rango sugerido)
    lat_center = -47.0
    lon_center = -69.0
    size_km = 15.0
    
    lat_offset = size_km / 111.32 / 2
    lon_offset = size_km / (111.32 * abs(lat_center)) / 2
    
    bounds = BoundingBox(
        lat_min=lat_center - lat_offset,
        lat_max=lat_center + lat_offset,
        lon_min=lon_center - lon_offset,
        lon_max=lon_center + lon_offset,
        depth_min=0.0,
        depth_max=-5.0
    )
    
    region_name = "Patagonia Árida - Meseta Central"
    
    print(f"📦 Bounding Box:")
    print(f"   Lat: [{bounds.lat_min:.4f}, {bounds.lat_max:.4f}]")
    print(f"   Lon: [{bounds.lon_min:.4f}, {bounds.lon_max:.4f}]")
    print(f"   Área: {bounds.area_km2:.2f} km²")
    print(f"   Altitud: ~600-800 msnm")
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
        print("   Prioridad: SAR + Thermal + NDVI")
        print("   Ventana temporal: 5 años")
        print()
        
        etp = await etp_generator.generate_etp(bounds, resolution_m=150.0)
        
        print()
        print("="*80)
        print("📊 RESULTADOS CIENTÍFICOS - PATAGONIA MESETA CENTRAL")
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
        
        # Análisis específico para Patagonia
        print("="*80)
        print("🔍 ANÁLISIS ESPECÍFICO - PATAGONIA MESETA CENTRAL")
        print("="*80)
        print()
        
        # Clasificación según escala calibrada
        if etp.ess_volumetrico < 0.30:
            clasificacion = "PISO - Sin huella humana persistente"
            emoji = "🟢"
        elif 0.45 <= etp.ess_volumetrico <= 0.60:
            clasificacion = "ZONA HABITABLE - Paisaje cultural difuso"
            emoji = "🟡"
        elif etp.ess_volumetrico > 0.60:
            clasificacion = "TECHO - Paisaje antropizado intenso"
            emoji = "🔴"
        else:
            clasificacion = "INTERMEDIO - Señal moderada"
            emoji = "🟠"
        
        print(f"{emoji} CLASIFICACIÓN: {clasificacion}")
        print()
        
        # Evaluación de condiciones TOP TIER para Patagonia
        print("✅ EVALUACIÓN TOP TIER (PATAGONIA):")
        print()
        
        # 1. Baja vegetación (estepa)
        ndvi_bajo = etp.ess_superficial < 0.3
        print(f"{'✅' if ndvi_bajo else '❌'} Baja vegetación (estepa):")
        print(f"   NDVI: {etp.ess_superficial:.3f} {'(bajo - estepa árida)' if ndvi_bajo else '(alto - vegetación densa)'}")
        
        # 2. SAR coherente
        if etp.tas_signature:
            sar_coherente = etp.tas_signature.sar_coherence > 0.4
            print(f"{'✅' if sar_coherente else '❌'} SAR coherente:")
            print(f"   Coherencia SAR: {etp.tas_signature.sar_coherence:.3f} {'(buena - señal clara)' if sar_coherente else '(baja - ruido)'}")
        
        # 3. Thermal stability (desierto frío)
        if etp.tas_signature:
            thermal_ok = etp.tas_signature.thermal_stability > 0.6
            print(f"{'✅' if thermal_ok else '❌'} Estabilidad térmica:")
            print(f"   Thermal Stability: {etp.tas_signature.thermal_stability:.3f} {'(alta - modificación persistente)' if thermal_ok else '(baja)'}")
        
        # 4. Coherencia 3D
        coherencia_ok = 0.30 <= etp.coherencia_3d <= 0.70
        print(f"{'✅' if coherencia_ok else '❌'} Coherencia 3D:")
        print(f"   Coherencia: {etp.coherencia_3d:.3f} {'(rango óptimo)' if coherencia_ok else '(fuera de rango)'}")
        
        print()
        
        # Interpretación arqueológica específica para Patagonia
        print("="*80)
        print("🏛️ INTERPRETACIÓN ARQUEOLÓGICA - PATAGONIA")
        print("="*80)
        print()
        
        if etp.ess_volumetrico > 0.50:
            print("🎯 ALTA PROBABILIDAD DE HUELLA HUMANA")
            print()
            print("Señales detectadas:")
            if etp.tas_signature and etp.tas_signature.thermal_stability > 0.7:
                print("  • Persistencia térmica alta → estructuras de piedra")
            if etp.tas_signature and etp.tas_signature.sar_coherence > 0.5:
                print("  • SAR coherente → corrales, parapetos, chenques")
            if etp.dil_signature and etp.dil_signature.dil_score > 0.5:
                print(f"  • DIL alto → profundidad estimada {etp.dil_signature.estimated_depth_m:.1f}m")
            
            print()
            print("Posibles características patagónicas:")
            print("  - Corrales de piedra (manejo de guanacos)")
            print("  - Chenques (estructuras funerarias circulares)")
            print("  - Parapetos de caza")
            print("  - Campamentos de cazadores-recolectores")
            print("  - Cuevas con ocupación")
        
        elif 0.30 < etp.ess_volumetrico <= 0.50:
            print("⚠️ SEÑAL MODERADA")
            print()
            print("Posible ocupación humana dispersa:")
            print("  - Campamentos temporales")
            print("  - Tránsito de grupos móviles")
            print("  - Modificación natural del paisaje")
            print("  - Señal arqueológica débil")
        
        else:
            print("🟢 SEÑAL BAJA")
            print()
            print("Paisaje natural estable sin huella humana persistente")
            print("Típico de meseta patagónica sin ocupación intensiva")
        
        print()
        
        # Guardar resultado en JSON
        result = {
            "nombre": "Patagonia Árida - Meseta Central (TOP TIER)",
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
            "top_tier_evaluation": {
                "baja_vegetacion": bool(ndvi_bajo),
                "sar_coherente": bool(sar_coherente) if etp.tas_signature else None,
                "thermal_ok": bool(thermal_ok) if etp.tas_signature else None,
                "coherencia_ok": bool(coherencia_ok)
            }
        }
        
        output_file = f"patagonia_meseta_central_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
    asyncio.run(test_patagonia_meseta())
