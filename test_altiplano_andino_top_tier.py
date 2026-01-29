#!/usr/bin/env python3
"""
Test TOP TIER - Altiplano Andino Seco
======================================

Zona de máxima señal / bajo ruido:
- Aridez extrema
- Ocupación humana milenaria
- NDVI estable
- SAR limpio

Coordenadas: -19.8 a -20.6 (Lat), -68.5 a -69.5 (Lon)
Región: Bolivia-Chile (frontera)

Ideal para detectar:
- Patrones geométricos
- Terrazas fósiles
- Caminos antiguos
- Estructuras bajo grava
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
from etp_generator import ETProfileGenerator, BoundingBox


async def test_altiplano_andino():
    """Test del Altiplano Andino con arsenal completo."""
    
    print("="*80)
    print("🏔️ ArcheoScope - Test TOP TIER: Altiplano Andino Seco")
    print("="*80)
    print()
    print("📍 Región: Bolivia-Chile (frontera)")
    print("   Características:")
    print("   - Aridez extrema")
    print("   - Ocupación humana milenaria (Tiwanaku, Inca)")
    print("   - NDVI estable (sin vegetación)")
    print("   - SAR limpio (sin ruido biológico)")
    print()
    print("🎯 Objetivos de detección:")
    print("   - Patrones geométricos (terrazas, plataformas)")
    print("   - Caminos antiguos (Qhapaq Ñan)")
    print("   - Estructuras bajo grava")
    print("   - Sistemas hidráulicos fósiles")
    print()
    
    # Definir región de interés
    lat_center = -20.2
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
    
    print(f"📦 Bounding Box:")
    print(f"   Lat: [{bounds.lat_min:.4f}, {bounds.lat_max:.4f}]")
    print(f"   Lon: [{bounds.lon_min:.4f}, {bounds.lon_max:.4f}]")
    print(f"   Área: {bounds.area_km2:.2f} km²")
    print(f"   Altitud: ~3,800-4,200 msnm")
    print()
    
    try:
        # Inicializar componentes
        print("🔧 Inicializando componentes...")
        integrator = RealDataIntegratorV2()
        etp_generator = ETProfileGenerator(integrator)
        print("   ✅ Componentes inicializados")
        print()
        
        # Generar ETP con protocolo canónico
        print("🔬 Generando ETP (resolución 150m, protocolo canónico)...")
        print("   Prioridad: SAR + Thermal + NDVI + Temporal")
        print("   Ventana temporal: 5 años (mata ruido estacional)")
        print()
        
        etp = await etp_generator.generate_etp(bounds, resolution_m=150.0)
        
        print()
        print("="*80)
        print("📊 RESULTADOS CIENTÍFICOS - ALTIPLANO ANDINO")
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
        
        # TAS (Temporal Archaeological Signature)
        if etp.tas_signature:
            print("🕐 TEMPORAL ARCHAEOLOGICAL SIGNATURE (TAS):")
            print(f"   TAS Score:          {etp.tas_signature.tas_score:.3f}")
            print(f"   NDVI Persistence:   {etp.tas_signature.ndvi_persistence:.3f}")
            print(f"   Thermal Stability:  {etp.tas_signature.thermal_stability:.3f}")
            print(f"   SAR Coherence:      {etp.tas_signature.sar_coherence:.3f}")
            print(f"   Stress Frequency:   {etp.tas_signature.stress_frequency:.3f}")
            print(f"   Años analizados:    {etp.tas_signature.years_analyzed}")
            print()
        
        # DIL (Deep Inference Layer)
        if etp.dil_signature:
            print("🔬 DEEP INFERENCE LAYER (DIL):")
            print(f"   DIL Score:          {etp.dil_signature.dil_score:.3f}")
            print(f"   Profundidad est:    {etp.dil_signature.estimated_depth_m:.1f}m")
            print(f"   Confianza:          {etp.dil_signature.confidence:.3f}")
            print(f"   Relevancia Arq:     {etp.dil_signature.archaeological_relevance:.3f}")
            print()
        
        # Contextos adicionales
        if etp.geological_compatibility:
            print("🗿 CONTEXTO GEOLÓGICO:")
            print(f"   GCS Score:          {etp.geological_compatibility.gcs_score:.3f}")
            print()
        
        if etp.water_availability:
            print("💧 DISPONIBILIDAD DE AGUA:")
            print(f"   Holoceno:           {etp.water_availability.holocene_availability:.3f}")
            print()
        
        if etp.external_consistency:
            print("🏛️ CONSISTENCIA EXTERNA:")
            print(f"   ECS Score:          {etp.external_consistency.ecs_score:.3f}")
            print()
        
        # Análisis específico para Altiplano
        print("="*80)
        print("🔍 ANÁLISIS ESPECÍFICO - ALTIPLANO ANDINO")
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
        
        # Evaluación de condiciones TOP TIER
        print("✅ EVALUACIÓN TOP TIER:")
        print()
        
        # 1. Aridez extrema
        ndvi_bajo = etp.ess_superficial < 0.2
        print(f"{'✅' if ndvi_bajo else '❌'} Aridez extrema:")
        print(f"   NDVI: {etp.ess_superficial:.3f} {'(bajo - correcto)' if ndvi_bajo else '(alto - vegetación presente)'}")
        
        # 2. SAR limpio
        if etp.tas_signature:
            sar_limpio = etp.tas_signature.sar_coherence > 0.5
            print(f"{'✅' if sar_limpio else '❌'} SAR limpio:")
            print(f"   Coherencia SAR: {etp.tas_signature.sar_coherence:.3f} {'(alta - señal clara)' if sar_limpio else '(baja - ruido)'}")
        
        # 3. Thermal stability
        if etp.tas_signature:
            thermal_alto = etp.tas_signature.thermal_stability > 0.7
            print(f"{'✅' if thermal_alto else '❌'} Persistencia térmica:")
            print(f"   Thermal Stability: {etp.tas_signature.thermal_stability:.3f} {'(alta - modificación humana)' if thermal_alto else '(baja)'}")
        
        # 4. Coherencia 3D
        coherencia_ok = 0.30 <= etp.coherencia_3d <= 0.70
        print(f"{'✅' if coherencia_ok else '❌'} Coherencia 3D:")
        print(f"   Coherencia: {etp.coherencia_3d:.3f} {'(rango óptimo)' if coherencia_ok else '(fuera de rango)'}")
        
        print()
        
        # Interpretación arqueológica
        print("="*80)
        print("🏛️ INTERPRETACIÓN ARQUEOLÓGICA")
        print("="*80)
        print()
        
        if etp.ess_volumetrico > 0.50:
            print("🎯 ALTA PROBABILIDAD DE HUELLA HUMANA")
            print()
            print("Señales detectadas:")
            if etp.tas_signature and etp.tas_signature.thermal_stability > 0.7:
                print("  • Persistencia térmica alta → modificación del suelo")
            if etp.tas_signature and etp.tas_signature.sar_coherence > 0.5:
                print("  • SAR coherente → estructuras subsuperficiales")
            if etp.dil_signature and etp.dil_signature.dil_score > 0.5:
                print(f"  • DIL alto → profundidad estimada {etp.dil_signature.estimated_depth_m:.1f}m")
            if etp.external_consistency and etp.external_consistency.ecs_score > 0.5:
                print("  • Consistencia externa → contexto arqueológico conocido")
            
            print()
            print("Posibles características:")
            print("  - Terrazas agrícolas prehispánicas")
            print("  - Caminos del Qhapaq Ñan (red vial inca)")
            print("  - Plataformas ceremoniales")
            print("  - Sistemas de riego fósiles")
            print("  - Asentamientos bajo grava")
        
        elif 0.30 < etp.ess_volumetrico <= 0.50:
            print("⚠️ SEÑAL MODERADA")
            print()
            print("Posible ocupación humana difusa o:")
            print("  - Modificación natural del paisaje")
            print("  - Actividad humana reciente")
            print("  - Señal arqueológica débil")
        
        else:
            print("🟢 SEÑAL BAJA")
            print()
            print("Paisaje natural estable sin huella humana persistente")
        
        print()
        
        # Guardar resultado
        result = {
            "nombre": "Altiplano Andino Seco (TOP TIER)",
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
                "aridez_extrema": bool(ndvi_bajo),
                "sar_limpio": bool(sar_limpio) if etp.tas_signature else None,
                "thermal_alto": bool(thermal_alto) if etp.tas_signature else None,
                "coherencia_ok": bool(coherencia_ok)
            }
        }
        
        output_file = f"altiplano_andino_top_tier_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"💾 Resultados guardados en: {output_file}")
        print()
        print("="*80)
        print("✅ TEST COMPLETADO")
        print("="*80)
        
        return result
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(test_altiplano_andino())
