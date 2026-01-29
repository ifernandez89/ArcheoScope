#!/usr/bin/env python3
"""
Test TOP TIER - Costas Fósiles Elevadas (Chile Norte) CON GUARDADO EN BD
=========================================================================

IMPORTANTE: Este script SIEMPRE guarda los resultados en la base de datos.

Zona: Costas Fósiles Elevadas (Chile Norte)
Coordenadas: -27.5 a -28.2 (Lat), -71.0 a -70.3 (Lon)

CARACTERÍSTICAS:
- Antiguos niveles marinos (terrazas elevadas)
- Ocupación temprana (cazadores-recolectores marinos)
- Aridez extrema (preservación excelente)
- Cambios térmicos nocturnos (detección de estructuras)

⚠️ NOTA: Más ruido que desiertos interiores, pero gran potencial

Objetivos de detección:
- Plataformas costeras (terrazas marinas fósiles)
- Campamentos antiguos (conchales, fogones)
- Cambios térmicos nocturnos (estructuras de piedra)
- Modificación de terrazas (ocupación humana)
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
            environment_type = "COASTAL"
        
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


async def test_costas_fosiles():
    """Test de Costas Fósiles Elevadas del norte de Chile."""
    
    print("="*80)
    print("🌊 ArcheoScope - Test TOP TIER: Costas Fósiles Elevadas (Chile Norte)")
    print("="*80)
    print()
    print("📍 Región: Costas Fósiles Elevadas (Chile Norte)")
    print("   Características:")
    print("   - Antiguos niveles marinos (terrazas elevadas)")
    print("   - Ocupación temprana (cazadores-recolectores marinos)")
    print("   - Aridez extrema (preservación excelente)")
    print("   - Cambios térmicos nocturnos")
    print()
    print("⚠️ NOTA: Más ruido que desiertos interiores")
    print("   - Influencia marina (humedad, sal)")
    print("   - Geomorfología compleja (terrazas)")
    print("   - Pero gran potencial arqueológico")
    print()
    print("🎯 Objetivos de detección:")
    print("   - Plataformas costeras (terrazas marinas fósiles)")
    print("   - Campamentos antiguos (conchales, fogones)")
    print("   - Cambios térmicos nocturnos (estructuras de piedra)")
    print("   - Modificación de terrazas (ocupación humana)")
    print()
    
    # Definir región de interés (centro del rango sugerido)
    lat_center = -27.85
    lon_center = -70.65
    size_km = 15.0
    
    lat_offset = size_km / 111.32 / 2
    lon_offset = size_km / (111.32 * abs(lat_center)) / 2
    
    bounds = BoundingBox(
        lat_min=lat_center - lat_offset,
        lat_max=lat_center + lat_offset,
        lon_min=lon_center - lon_offset,
        lon_max=lon_center + lon_offset,
        depth_min=0.0,
        depth_max=-3.0  # Campamentos superficiales
    )
    
    region_name = "Costas Fósiles Elevadas - Chile Norte"
    
    print(f"📦 Bounding Box:")
    print(f"   Lat: [{bounds.lat_min:.4f}, {bounds.lat_max:.4f}]")
    print(f"   Lon: [{bounds.lon_min:.4f}, {bounds.lon_max:.4f}]")
    print(f"   Área: {bounds.area_km2:.2f} km²")
    print(f"   Altitud: ~50-200 msnm (terrazas elevadas)")
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
        print("   Prioridad: Thermal + SAR + NDVI")
        print("   Ventana temporal: 5 años")
        print()
        
        etp = await etp_generator.generate_etp(bounds, resolution_m=150.0)
        
        print()
        print("="*80)
        print("📊 RESULTADOS CIENTÍFICOS - COSTAS FÓSILES CHILE NORTE")
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
        print("Desiertos interiores:")
        print("   Atacama Interior:    ESS 0.477 (bajo ruido)")
        print("   Altiplano Andino:    ESS 0.467 (bajo ruido)")
        print()
        print("Costas fósiles:")
        print(f"   Chile Norte:         ESS {etp.ess_volumetrico:.3f} (más ruido esperado)")
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
        
        # Análisis específico para costas fósiles
        print("="*80)
        print("🔍 ANÁLISIS ESPECÍFICO - COSTAS FÓSILES")
        print("="*80)
        print()
        
        # Evaluación de ruido costero
        print("⚠️ EVALUACIÓN DE RUIDO COSTERO:")
        print()
        
        # 1. Influencia marina
        print("🌊 Influencia marina:")
        print("   • Humedad relativa más alta que desierto interior")
        print("   • Sal en el aire (afecta SAR)")
        print("   • Niebla costera (camanchaca)")
        print()
        
        # 2. Geomorfología compleja
        print("🏔️ Geomorfología compleja:")
        print("   • Terrazas marinas escalonadas")
        print("   • Cambios de elevación abruptos")
        print("   • Erosión diferencial")
        print()
        
        # 3. Señal arqueológica esperada
        if etp.ess_volumetrico > 0.40:
            print("✅ SEÑAL ARQUEOLÓGICA CLARA (a pesar del ruido)")
            print()
            print("Señales detectadas:")
            if etp.tas_signature and etp.tas_signature.thermal_stability > 0.7:
                print("  • Persistencia térmica → campamentos, fogones")
            if etp.tas_signature and etp.tas_signature.sar_coherence > 0.5:
                print("  • SAR coherente → estructuras de piedra")
            if etp.dil_signature and etp.dil_signature.estimated_depth_m < 3.0:
                print(f"  • Profundidad superficial ({etp.dil_signature.estimated_depth_m:.1f}m) → conchales")
            
            print()
            print("Características costeras probables:")
            print("  - Campamentos de cazadores-recolectores marinos")
            print("  - Conchales (acumulación de conchas)")
            print("  - Fogones (cambios térmicos)")
            print("  - Modificación de terrazas")
            print("  - Estructuras de piedra (parapetos)")
            
        elif 0.30 < etp.ess_volumetrico <= 0.40:
            print("⚠️ SEÑAL MODERADA (ruido costero presente)")
            print()
            print("Posible ocupación humana:")
            print("  - Campamentos temporales")
            print("  - Tránsito de grupos móviles")
            print("  - Señal arqueológica débil pero presente")
            print("  - Ruido geomorfológico (terrazas naturales)")
            
        else:
            print("🟢 SEÑAL BAJA")
            print()
            print("Paisaje natural o ruido geomorfológico dominante")
            print("Terrazas marinas sin ocupación humana significativa")
        
        print()
        
        # Interpretación del ruido
        print("="*80)
        print("🧠 INTERPRETACIÓN DEL RUIDO COSTERO")
        print("="*80)
        print()
        
        if etp.ess_volumetrico > 0.40:
            print("✅ SEÑAL ARQUEOLÓGICA SUPERA EL RUIDO")
            print()
            print("El sistema detecta ocupación humana a pesar de:")
            print("  • Influencia marina")
            print("  • Geomorfología compleja")
            print("  • Cambios de elevación")
            print()
            print("Esto sugiere ocupación humana REAL y persistente.")
            
        elif 0.30 < etp.ess_volumetrico <= 0.40:
            print("⚠️ SEÑAL Y RUIDO COMPARABLES")
            print()
            print("Difícil distinguir:")
            print("  • Ocupación humana débil")
            print("  • vs Ruido geomorfológico")
            print()
            print("Requiere validación de campo.")
            
        else:
            print("🟢 RUIDO GEOMORFOLÓGICO DOMINANTE")
            print()
            print("Señal arqueológica ausente o muy débil.")
            print("Terrazas marinas naturales sin modificación humana.")
        
        print()
        
        # Comparación con desiertos interiores
        print("="*80)
        print("📊 COMPARACIÓN: COSTA vs INTERIOR")
        print("="*80)
        print()
        
        print("Desierto Interior (Atacama):")
        print("   ESS: 0.477")
        print("   Ruido: BAJO (aridez extrema)")
        print("   Señal: CLARA (modificación térmica)")
        print()
        
        print("Costa Fósil (Chile Norte):")
        print(f"   ESS: {etp.ess_volumetrico:.3f}")
        print("   Ruido: MODERADO (influencia marina)")
        if etp.ess_volumetrico > 0.40:
            print("   Señal: CLARA (supera el ruido)")
        elif etp.ess_volumetrico > 0.30:
            print("   Señal: MODERADA (comparable al ruido)")
        else:
            print("   Señal: DÉBIL (dominada por ruido)")
        print()
        
        diferencia = 0.477 - etp.ess_volumetrico
        print(f"Diferencia: {diferencia:.3f}")
        if diferencia > 0.10:
            print("   → Ruido costero reduce señal significativamente")
        elif diferencia > 0.05:
            print("   → Ruido costero reduce señal moderadamente")
        else:
            print("   → Ruido costero mínimo (señal comparable)")
        
        print()
        
        # Guardar resultado en JSON
        result = {
            "nombre": "Costas Fósiles Elevadas - Chile Norte",
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
                "costa_ess": float(etp.ess_volumetrico),
                "diferencia": float(diferencia),
                "ruido_costero": "significativo" if diferencia > 0.10 else "moderado" if diferencia > 0.05 else "minimo"
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
            "dil": etp.dil_signature.to_dict() if etp.dil_signature else None
        }
        
        output_file = f"costas_fosiles_chile_norte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
    asyncio.run(test_costas_fosiles())
