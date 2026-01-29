#!/usr/bin/env python3
"""
Test de Calibración con URUK como TECHO
========================================

A. PISO (Control Negativo) - Pampa Argentina
B. ZONA HABITABLE (Benchmark Real) - Laguna Veracruz
C. TECHO (Antropogénico Visible) - Uruk, Mesopotamia Sur

URUK: Mayor contraste térmico urbano + humedad histórica + estrés agrícola
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


async def test_caso(nombre, lat, lon, size_km, expected_ess_vol, expected_ess_temp, expected_coherence, justificacion):
    """Test de un caso de calibración."""
    
    print("\n" + "="*80)
    print(f"📍 {nombre}")
    print("="*80)
    print(f"   Coordenadas: {lat:.4f}, {lon:.4f}")
    print(f"   Justificación: {justificacion}")
    print(f"   Esperado ESS Vol: {expected_ess_vol[0]:.2f}-{expected_ess_vol[1]:.2f}")
    print(f"   Esperado ESS Temp: {expected_ess_temp[0]:.2f}-{expected_ess_temp[1]:.2f}")
    print(f"   Esperado Coherencia: {expected_coherence[0]:.2f}-{expected_coherence[1]:.2f}")
    print()
    
    # Crear bounding box
    lat_offset = size_km / 111.32 / 2
    lon_offset = size_km / (111.32 * abs(lat)) / 2
    
    bounds = BoundingBox(
        lat_min=lat - lat_offset,
        lat_max=lat + lat_offset,
        lon_min=lon - lon_offset,
        lon_max=lon + lon_offset,
        depth_min=0.0,
        depth_max=-5.0
    )
    
    print(f"📦 Bounding Box:")
    print(f"   Lat: [{bounds.lat_min:.4f}, {bounds.lat_max:.4f}]")
    print(f"   Lon: [{bounds.lon_min:.4f}, {bounds.lon_max:.4f}]")
    print(f"   Área: {bounds.area_km2:.2f} km²")
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
        print("   Prioridad: Thermal + SAR + NDVI persistente")
        etp = await etp_generator.generate_etp(bounds, resolution_m=150.0)
        
        print()
        print("="*80)
        print("📊 RESULTADOS CIENTÍFICOS")
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
        
        # TAS (si disponible)
        if etp.tas_signature:
            print("🕐 TEMPORAL ARCHAEOLOGICAL SIGNATURE (TAS):")
            print(f"   TAS Score:          {etp.tas_signature.tas_score:.3f}")
            print(f"   NDVI Persistence:   {etp.tas_signature.ndvi_persistence:.3f}")
            print(f"   Thermal Stability:  {etp.tas_signature.thermal_stability:.3f}")
            print(f"   SAR Coherence:      {etp.tas_signature.sar_coherence:.3f}")
            print(f"   Stress Frequency:   {etp.tas_signature.stress_frequency:.3f}")
            print(f"   Años analizados:    {etp.tas_signature.years_analyzed}")
            print()
        
        # DIL (si disponible)
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
        
        # Validación contra expectativas
        print("="*80)
        print("✅ VALIDACIÓN")
        print("="*80)
        print()
        
        ess_vol_ok = expected_ess_vol[0] <= etp.ess_volumetrico <= expected_ess_vol[1]
        ess_temp_ok = expected_ess_temp[0] <= etp.ess_temporal <= expected_ess_temp[1]
        coherence_ok = expected_coherence[0] <= etp.coherencia_3d <= expected_coherence[1]
        
        print(f"{'✅' if ess_vol_ok else '❌'} ESS Volumétrico:")
        print(f"   Obtenido: {etp.ess_volumetrico:.3f}")
        print(f"   Esperado: {expected_ess_vol[0]:.2f}-{expected_ess_vol[1]:.2f}")
        print()
        
        print(f"{'✅' if ess_temp_ok else '❌'} ESS Temporal:")
        print(f"   Obtenido: {etp.ess_temporal:.3f}")
        print(f"   Esperado: {expected_ess_temp[0]:.2f}-{expected_ess_temp[1]:.2f}")
        print()
        
        print(f"{'✅' if coherence_ok else '❌'} Coherencia 3D:")
        print(f"   Obtenido: {etp.coherencia_3d:.3f}")
        print(f"   Esperado: {expected_coherence[0]:.2f}-{expected_coherence[1]:.2f}")
        print()
        
        all_ok = ess_vol_ok and ess_temp_ok and coherence_ok
        
        if all_ok:
            print("✅ VALIDACIÓN EXITOSA - Dentro de rango esperado")
        else:
            print("⚠️ VALIDACIÓN FUERA DE RANGO - Revisar calibración")
        
        # Guardar resultado
        result = {
            "nombre": nombre,
            "coordenadas": {"lat": float(lat), "lon": float(lon)},
            "timestamp": datetime.now().isoformat(),
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
            "validacion": {
                "ess_volumetrico_ok": bool(ess_vol_ok),
                "ess_temporal_ok": bool(ess_temp_ok),
                "coherencia_ok": bool(coherence_ok),
                "all_ok": bool(all_ok)
            }
        }
        
        return result
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Ejecutar los 3 casos de calibración con URUK como techo."""
    
    print("="*80)
    print("🎯 TEST DE CALIBRACIÓN - ArcheoScope (URUK como TECHO)")
    print("="*80)
    print()
    print("A. PISO (Control Negativo) - Ancla del sistema")
    print("B. ZONA HABITABLE (Benchmark Real) - Oro puro")
    print("C. TECHO (Antropogénico Visible) - Uruk")
    print()
    print("URUK: Mayor contraste térmico + humedad + estrés agrícola")
    print()
    
    resultados = {}
    
    # A. PISO - Pampa Argentina (NO TOCAR)
    print("\n" + "🟢"*40)
    print("A. PISO (Control Negativo) - Pampa Argentina")
    print("🟢"*40)
    
    resultado_a = await test_caso(
        nombre="A. PISO - Pampa Argentina",
        lat=-35.150,
        lon=-61.800,
        size_km=15.0,
        expected_ess_vol=(0.0, 0.30),
        expected_ess_temp=(0.0, 0.30),
        expected_coherence=(0.65, 1.0),
        justificacion="Geología homogénea + uso agrícola continuo + sin memoria enterrada"
    )
    
    if resultado_a:
        resultados['A_PISO'] = resultado_a
    
    # B. ZONA HABITABLE - Laguna Veracruz (ORO PURO)
    print("\n" + "🟡"*40)
    print("B. ZONA HABITABLE (Benchmark Real) - Laguna Veracruz")
    print("🟡"*40)
    
    resultado_b = await test_caso(
        nombre="B. ZONA HABITABLE - Laguna Veracruz",
        lat=20.580,
        lon=-96.920,
        size_km=15.0,
        expected_ess_vol=(0.45, 0.60),
        expected_ess_temp=(0.45, 0.65),
        expected_coherence=(0.45, 0.60),
        justificacion="Transición agua-tierra + reuso histórico + señales térmicas y SAR reales"
    )
    
    if resultado_b:
        resultados['B_ZONA_HABITABLE'] = resultado_b
    
    # C. TECHO - URUK (Mesopotamia Sur)
    print("\n" + "🔴"*40)
    print("C. TECHO (Antropogénico Visible) - Uruk, Mesopotamia Sur")
    print("🔴"*40)
    
    resultado_c = await test_caso(
        nombre="C. TECHO - Uruk",
        lat=31.323,
        lon=45.636,
        size_km=15.0,
        expected_ess_vol=(0.60, 0.75),
        expected_ess_temp=(0.60, 0.75),
        expected_coherence=(0.30, 0.50),
        justificacion="Contraste térmico urbano + humedad histórica + estrés agrícola + menos orden geomorfológico"
    )
    
    if resultado_c:
        resultados['C_TECHO'] = resultado_c
    
    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN FINAL - CALIBRACIÓN DEFINITIVA")
    print("="*80)
    print()
    
    for key, resultado in resultados.items():
        val = resultado['validacion']
        status = "✅" if val['all_ok'] else "⚠️"
        print(f"{status} {resultado['nombre']}")
        print(f"   ESS Vol: {resultado['metricas']['ess_volumetrico']:.3f} {'✅' if val['ess_volumetrico_ok'] else '❌'}")
        print(f"   ESS Temp: {resultado['metricas']['ess_temporal']:.3f} {'✅' if val['ess_temporal_ok'] else '❌'}")
        print(f"   Coherencia: {resultado['metricas']['coherencia_3d']:.3f} {'✅' if val['coherencia_ok'] else '❌'}")
        
        # Mostrar TAS si está disponible
        if resultado.get('tas'):
            tas = resultado['tas']
            print(f"   TAS Score: {tas['tas_score']:.3f} | Thermal: {tas['thermal_stability']:.3f}")
        
        print()
    
    # Guardar resultados
    output_file = f"calibracion_uruk_definitiva_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(resultados, f, indent=2)
    
    print(f"💾 Resultados guardados en: {output_file}")
    print()
    
    # Análisis final
    print("="*80)
    print("🔬 ANÁLISIS CIENTÍFICO")
    print("="*80)
    print()
    
    if all(r['validacion']['all_ok'] for r in resultados.values()):
        print("✅ CALIBRACIÓN COMPLETA EXITOSA")
        print()
        print("El sistema está calibrado correctamente:")
        print("- PISO fija el cero absoluto")
        print("- ZONA HABITABLE define el planeta ArcheoScope")
        print("- TECHO establece el límite superior detectable")
        print()
        print("🎯 Sistema listo para uso científico")
    else:
        print("⚠️ CALIBRACIÓN PARCIAL")
        print()
        print("Casos validados:")
        for key, resultado in resultados.items():
            if resultado['validacion']['all_ok']:
                print(f"  ✅ {resultado['nombre']}")
            else:
                print(f"  ❌ {resultado['nombre']}")
    
    print()
    print("="*80)
    print("✅ TEST COMPLETADO")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
