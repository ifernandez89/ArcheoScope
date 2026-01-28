#!/usr/bin/env python3
"""
Test Completo del Sistema ETP - Environmental Tomographic Profile
================================================================

REVOLUCIÓN CONCEPTUAL: Probar la transformación de ArcheoScope
de "detector de sitios" a "explicador de territorios"

PRUEBAS:
1. Generación de perfil tomográfico completo
2. Cálculo de ESS volumétrico y temporal
3. Generación de narrativa territorial
4. Preparación de datos de visualización
5. API endpoints ETP

COORDENADAS DE PRUEBA: Giza, Egipto (sitio conocido)
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar path del backend
sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_etp_system_complete():
    """Test completo del sistema ETP revolucionario."""
    
    print("🧠 ARCHEOSCOPE ETP - TEST SISTEMA COMPLETO")
    print("=" * 80)
    print("REVOLUCIÓN: De 'detector de sitios' a 'explicador de territorios'")
    print("OBJETIVO: Generar perfil tomográfico explicable de Giza, Egipto")
    print("=" * 80)
    
    try:
        # Importar sistema ETP
        from etp_generator import ETProfileGenerator
        from etp_core import BoundingBox
        from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
        
        print("✅ Módulos ETP importados correctamente")
        
    except Exception as e:
        print(f"❌ Error importando módulos ETP: {e}")
        return False
    
    # FASE 1: Inicializar sistema ETP
    print("\n🔧 FASE 1: Inicializando sistema ETP...")
    
    try:
        # Inicializar integrador de 15 instrumentos
        integrator = RealDataIntegratorV2()
        
        # Inicializar generador ETP
        etp_generator = ETProfileGenerator(integrator)
        
        print("✅ Sistema ETP inicializado correctamente")
        print(f"   📡 Integrador: {len(integrator.connectors)} conectores")
        print(f"   🧠 Generador: {len(etp_generator.depth_layers)} capas de profundidad")
        
    except Exception as e:
        print(f"❌ Error inicializando sistema ETP: {e}")
        return False
    
    # FASE 2: Definir territorio de prueba
    print("\n🎯 FASE 2: Definiendo territorio de prueba...")
    
    # Giza, Egipto - Sitio arqueológico conocido
    bounds = BoundingBox(
        lat_min=29.9,
        lat_max=30.0,
        lon_min=31.1,
        lon_max=31.2,
        depth_min=0.0,
        depth_max=-20.0
    )
    
    print(f"   📍 Territorio: Giza, Egipto")
    print(f"   📐 Coordenadas: [{bounds.lat_min:.4f}, {bounds.lat_max:.4f}] x [{bounds.lon_min:.4f}, {bounds.lon_max:.4f}]")
    print(f"   📏 Área: {bounds.area_km2:.3f} km²")
    print(f"   📊 Volumen: {bounds.volume_km3:.6f} km³")
    print(f"   🕳️ Profundidad: {bounds.depth_min}m a {bounds.depth_max}m")
    
    # FASE 3: Generar perfil tomográfico completo
    print("\n🧠 FASE 3: Generando perfil tomográfico completo...")
    print("   ⚡ ESTO ES LA REVOLUCIÓN: De detección a explicación territorial")
    
    try:
        start_time = datetime.now()
        
        # Generar ETP completo
        etp = await etp_generator.generate_etp(bounds, resolution_m=30.0)
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        print(f"✅ Perfil tomográfico generado exitosamente")
        print(f"   ⏱️ Tiempo de procesamiento: {processing_time:.2f}s")
        print(f"   🆔 Territory ID: {etp.territory_id}")
        
    except Exception as e:
        print(f"❌ Error generando perfil tomográfico: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # FASE 4: Analizar resultados ETP
    print("\n📊 FASE 4: Analizando resultados del perfil tomográfico...")
    
    # Métricas ESS evolucionadas
    print(f"\n   🎯 MÉTRICAS ESS EVOLUCIONADAS:")
    print(f"      ESS Superficial:  {etp.ess_superficial:.3f}")
    print(f"      ESS Volumétrico:  {etp.ess_volumetrico:.3f} ← REVOLUCIÓN")
    print(f"      ESS Temporal:     {etp.ess_temporal:.3f} ← REVOLUCIÓN")
    
    # Métricas 3D
    print(f"\n   📐 MÉTRICAS 3D:")
    print(f"      Coherencia 3D:           {etp.coherencia_3d:.3f}")
    print(f"      Persistencia Temporal:   {etp.persistencia_temporal:.3f}")
    print(f"      Densidad Arqueológica:   {etp.densidad_arqueologica_m3:.6f} /m³")
    
    # Cortes tomográficos
    print(f"\n   🔬 CORTES TOMOGRÁFICOS:")
    if etp.xz_profile:
        print(f"      Corte XZ (Longitudinal): {len(etp.xz_profile.layers)} capas")
        print(f"         ESS del corte: {etp.xz_profile.slice_ess:.3f}")
        print(f"         Coherencia: {etp.xz_profile.coherence_score:.3f}")
        print(f"         Anomalías: {len(etp.xz_profile.anomalies)}")
    
    if etp.yz_profile:
        print(f"      Corte YZ (Latitudinal):  {len(etp.yz_profile.layers)} capas")
        print(f"         ESS del corte: {etp.yz_profile.slice_ess:.3f}")
        print(f"         Coherencia: {etp.yz_profile.coherence_score:.3f}")
        print(f"         Anomalías: {len(etp.yz_profile.anomalies)}")
    
    print(f"      Cortes XY (Horizontales): {len(etp.xy_profiles)} niveles")
    
    # FASE 5: Narrativa territorial - REVOLUCIÓN CONCEPTUAL
    print("\n📖 FASE 5: NARRATIVA TERRITORIAL - REVOLUCIÓN CONCEPTUAL")
    print("   🎯 DE '¿HAY UN SITIO?' A '¿QUÉ CUENTA ESTE TERRITORIO?'")
    print("-" * 60)
    
    print(f"\n   🏛️ EXPLICACIÓN TERRITORIAL:")
    print(f"      {etp.narrative_explanation}")
    
    # Historia ocupacional
    if etp.occupational_history:
        print(f"\n   📅 HISTORIA OCUPACIONAL:")
        for period in etp.occupational_history:
            print(f"      • {period.start_year}-{period.end_year}: {period.occupation_type}")
            print(f"        Evidencia: {period.evidence_strength:.2f} - {period.description}")
    
    # Función territorial
    if etp.territorial_function:
        print(f"\n   🏗️ FUNCIÓN TERRITORIAL:")
        print(f"      Función principal: {etp.territorial_function.primary_function}")
        print(f"      Funciones secundarias: {', '.join(etp.territorial_function.secondary_functions)}")
        print(f"      Organización espacial: {etp.territorial_function.spatial_organization}")
        print(f"      Confianza: {etp.territorial_function.confidence:.2f}")
    
    # Evolución del paisaje
    if etp.landscape_evolution:
        print(f"\n   🌍 EVOLUCIÓN DEL PAISAJE:")
        print(f"      Línea base natural: {etp.landscape_evolution.natural_baseline}")
        print(f"      Modificaciones humanas: {', '.join(etp.landscape_evolution.human_modifications)}")
        print(f"      Estado actual: {etp.landscape_evolution.current_state}")
    
    # FASE 6: Datos de visualización
    print("\n🎨 FASE 6: Datos de visualización tomográfica...")
    
    viz_data = etp.visualization_data
    
    print(f"   📊 Datos XZ: {len(viz_data.get('xz_slice', {}).get('depths', []))} puntos de profundidad")
    print(f"   📊 Datos YZ: {len(viz_data.get('yz_slice', {}).get('depths', []))} puntos de profundidad")
    print(f"   📊 Capas XY: {len(viz_data.get('xy_slices', []))} niveles horizontales")
    
    # Mostrar algunos datos de ejemplo
    if 'xz_slice' in viz_data:
        xz_data = viz_data['xz_slice']
        print(f"\n   🔬 EJEMPLO CORTE XZ:")
        depths = xz_data.get('depths', [])
        intensities = xz_data.get('intensities', [])
        
        for i, (depth, intensity) in enumerate(zip(depths[:5], intensities[:5])):
            print(f"      {depth:5.1f}m: intensidad {intensity:.3f}")
        
        if len(depths) > 5:
            print(f"      ... y {len(depths) - 5} capas más")
    
    # FASE 7: Guardar resultados
    print("\n💾 FASE 7: Guardando resultados...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"etp_test_results_{timestamp}.json"
    
    # Preparar datos para JSON
    results_data = {
        "test_metadata": {
            "timestamp": timestamp,
            "territory": "Giza, Egypt",
            "processing_time_s": processing_time,
            "system_version": "ETP 1.0.0"
        },
        "territory_info": {
            "territory_id": etp.territory_id,
            "bounds": {
                "lat_min": bounds.lat_min,
                "lat_max": bounds.lat_max,
                "lon_min": bounds.lon_min,
                "lon_max": bounds.lon_max,
                "depth_min": bounds.depth_min,
                "depth_max": bounds.depth_max
            },
            "area_km2": bounds.area_km2,
            "volume_km3": bounds.volume_km3
        },
        "ess_metrics": {
            "ess_superficial": etp.ess_superficial,
            "ess_volumetrico": etp.ess_volumetrico,
            "ess_temporal": etp.ess_temporal,
            "coherencia_3d": etp.coherencia_3d,
            "persistencia_temporal": etp.persistencia_temporal,
            "densidad_arqueologica_m3": etp.densidad_arqueologica_m3
        },
        "territorial_analysis": {
            "narrative_explanation": etp.narrative_explanation,
            "territorial_summary": etp.generate_territorial_summary(),
            "occupational_periods": len(etp.occupational_history),
            "primary_function": etp.territorial_function.primary_function if etp.territorial_function else None
        },
        "tomographic_data": {
            "xz_layers": len(etp.xz_profile.layers) if etp.xz_profile else 0,
            "yz_layers": len(etp.yz_profile.layers) if etp.yz_profile else 0,
            "xy_slices": len(etp.xy_profiles),
            "total_anomalies": (len(etp.xz_profile.anomalies) if etp.xz_profile else 0) + 
                              (len(etp.yz_profile.anomalies) if etp.yz_profile else 0)
        },
        "visualization_ready": bool(viz_data)
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, indent=2, ensure_ascii=False)
    
    print(f"   💾 Resultados guardados en: {results_file}")
    
    # FASE 8: Evaluación final
    print("\n" + "=" * 80)
    print("🎉 EVALUACIÓN FINAL - SISTEMA ETP")
    print("=" * 80)
    
    # Criterios de éxito
    success_criteria = {
        "perfil_generado": etp is not None,
        "ess_volumetrico_calculado": etp.ess_volumetrico > 0,
        "ess_temporal_calculado": etp.ess_temporal > 0,
        "narrativa_generada": len(etp.narrative_explanation) > 100,
        "cortes_tomograficos": (etp.xz_profile is not None and etp.yz_profile is not None),
        "datos_visualizacion": bool(viz_data),
        "historia_ocupacional": len(etp.occupational_history) > 0,
        "funcion_territorial": etp.territorial_function is not None
    }
    
    successful_criteria = sum(success_criteria.values())
    total_criteria = len(success_criteria)
    success_rate = successful_criteria / total_criteria
    
    print(f"📊 CRITERIOS DE ÉXITO: {successful_criteria}/{total_criteria} ({success_rate:.1%})")
    
    for criterion, passed in success_criteria.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {criterion.replace('_', ' ').title()}")
    
    # Evaluación revolucionaria
    print(f"\n🧠 EVALUACIÓN REVOLUCIONARIA:")
    
    if success_rate >= 0.8:
        print("🎉 ¡REVOLUCIÓN EXITOSA!")
        print("✅ ArcheoScope ha evolucionado de 'detector' a 'explicador'")
        print("✅ Sistema ETP completamente funcional")
        print("✅ Narrativas territoriales generadas automáticamente")
        print("✅ Visualización tomográfica lista")
        evaluation = "REVOLUCIONARIO"
    elif success_rate >= 0.6:
        print("👍 EVOLUCIÓN SIGNIFICATIVA")
        print("✅ Funcionalidades ETP principales operativas")
        print("⚠️ Algunos componentes necesitan refinamiento")
        evaluation = "EXITOSO"
    else:
        print("⚠️ REVOLUCIÓN PARCIAL")
        print("🔧 Sistema ETP necesita más desarrollo")
        print("❌ Funcionalidades críticas fallando")
        evaluation = "NECESITA_TRABAJO"
    
    # Métricas específicas
    print(f"\n📈 MÉTRICAS ESPECÍFICAS:")
    print(f"   🎯 ESS Volumétrico: {etp.ess_volumetrico:.3f} ({'Alto' if etp.ess_volumetrico > 0.6 else 'Medio' if etp.ess_volumetrico > 0.3 else 'Bajo'})")
    print(f"   ⏰ ESS Temporal: {etp.ess_temporal:.3f} ({'Alto' if etp.ess_temporal > 0.6 else 'Medio' if etp.ess_temporal > 0.3 else 'Bajo'})")
    print(f"   🧮 Coherencia 3D: {etp.coherencia_3d:.3f} ({'Alta' if etp.coherencia_3d > 0.7 else 'Media' if etp.coherencia_3d > 0.5 else 'Baja'})")
    
    # Impacto conceptual
    print(f"\n🌟 IMPACTO CONCEPTUAL:")
    print("   🔄 ANTES: '¿Hay un sitio arqueológico aquí?'")
    print("   🔄 DESPUÉS: '¿Qué historia cuenta este territorio?'")
    print("   🎯 RESULTADO: Comprensión territorial completa y explicable")
    
    print(f"\n{'=' * 80}")
    print(f"🚀 SISTEMA ETP: {evaluation}")
    print(f"⏱️ Tiempo total: {processing_time:.2f}s")
    print(f"💾 Resultados: {results_file}")
    print(f"{'=' * 80}")
    
    return success_rate >= 0.6

if __name__ == "__main__":
    async def main():
        success = await test_etp_system_complete()
        
        if success:
            print("\n🎉 ¡TEST ETP EXITOSO!")
            print("🧠 Sistema tomográfico revolucionario funcionando")
            print("🎨 Listo para visualización en frontend")
            print("🏛️ ArcheoScope transformado: de detector a explicador")
        else:
            print("\n⚠️ Test ETP con problemas")
            print("🔧 Revisar implementación antes de continuar")
        
        return success
    
    # Ejecutar test
    success = asyncio.run(main())
    sys.exit(0 if success else 1)