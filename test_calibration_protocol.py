#!/usr/bin/env python3
"""
Test del Protocolo de Calibración Científica
============================================

Ejecuta el protocolo completo de calibración con controles negativos y positivos.
"""

import asyncio
import sys
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from calibration_system import CalibrationSystem, ControlType
from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
from etp_generator import ETProfileGenerator, BoundingBox


async def test_calibration_site(site, integrator, etp_generator):
    """Test de un sitio de calibración."""
    
    print(f"\n{'='*80}")
    print(f"📍 ANALIZANDO: {site.name}")
    print(f"{'='*80}")
    print(f"   Tipo: {site.control_type.value.upper()}")
    print(f"   Coords: {site.lat:.4f}, {site.lon:.4f}")
    print(f"   Por qué: {site.why_chosen}")
    print()
    
    # Crear bounding box (15 km como especifica el protocolo)
    size_km = 15.0
    lat_offset = size_km / 111.32 / 2
    lon_offset = size_km / (111.32 * abs(site.lat)) / 2
    
    bounds = BoundingBox(
        lat_min=site.lat - lat_offset,
        lat_max=site.lat + lat_offset,
        lon_min=site.lon - lon_offset,
        lon_max=site.lon + lon_offset,
        depth_min=0.0,
        depth_max=-5.0
    )
    
    print(f"📦 Bounding Box:")
    print(f"   Lat: [{bounds.lat_min:.4f}, {bounds.lat_max:.4f}]")
    print(f"   Lon: [{bounds.lon_min:.4f}, {bounds.lon_max:.4f}]")
    print(f"   Área: {bounds.area_km2:.2f} km²")
    print()
    
    try:
        # Generar ETP con resolución canónica (150m)
        print("🔬 Generando ETP...")
        etp = await etp_generator.generate_etp(bounds, resolution_m=150.0)
        
        print()
        print(f"📊 RESULTADOS:")
        print(f"   ESS Volumétrico:  {etp.ess_volumetrico:.3f}")
        print(f"   ESS Temporal:     {etp.ess_temporal:.3f}")
        print(f"   Coherencia 3D:    {etp.coherencia_3d:.3f}")
        print()
        
        # Validar contra expectativas
        cal_system = CalibrationSystem()
        validation = cal_system.validate_result(
            site, 
            etp.ess_volumetrico, 
            etp.ess_temporal, 
            etp.coherencia_3d
        )
        
        print(f"✅ VALIDACIÓN:")
        print(f"   {validation['interpretation']}")
        print()
        
        print(f"📋 DETALLES:")
        for metric, data in validation['validation'].items():
            status = "✅" if data['ok'] else "❌"
            print(f"   {status} {metric}:")
            print(f"      Obtenido: {data['obtained']:.3f}")
            print(f"      Esperado: {data['expected'][0]:.2f}-{data['expected'][1]:.2f}")
        
        return validation
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


async def run_calibration_protocol():
    """Ejecutar protocolo completo de calibración."""
    
    print("="*80)
    print("🎯 PROTOCOLO DE CALIBRACIÓN CIENTÍFICA - ArcheoScope")
    print("="*80)
    print()
    
    # Inicializar sistema de calibración
    cal_system = CalibrationSystem()
    
    # Mostrar protocolo
    print("📋 SOLICITUD CANÓNICA:")
    print("-"*80)
    request = cal_system.get_canonical_request()
    request_dict = request.to_dict()
    for key, value in request_dict.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    print()
    
    # Inicializar componentes
    print("🔧 Inicializando componentes...")
    integrator = RealDataIntegratorV2()
    etp_generator = ETProfileGenerator(integrator)
    print("   ✅ Componentes inicializados")
    print()
    
    # Ejecutar tests
    results = {}
    
    # A. PISO (Control Negativo)
    print("\n" + "="*80)
    print("🟢 A. PISO (Control Negativo) - Debe dar BAJO")
    print("="*80)
    
    for site in cal_system.list_calibration_sites(ControlType.NEGATIVE):
        result = await test_calibration_site(site, integrator, etp_generator)
        if result:
            results[site.site_id] = result
    
    # B. TECHO (Control Positivo)
    print("\n" + "="*80)
    print("🔴 B. TECHO (Control Positivo) - Debe dar ALTO")
    print("="*80)
    
    for site in cal_system.list_calibration_sites(ControlType.POSITIVE):
        result = await test_calibration_site(site, integrator, etp_generator)
        if result:
            results[site.site_id] = result
    
    # C. INTERMEDIO (Validación)
    print("\n" + "="*80)
    print("🟡 C. INTERMEDIO (Validación) - Debe DISTINGUIR")
    print("="*80)
    
    for site in cal_system.list_calibration_sites(ControlType.VALIDATION):
        result = await test_calibration_site(site, integrator, etp_generator)
        if result:
            results[site.site_id] = result
    
    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN DE CALIBRACIÓN")
    print("="*80)
    print()
    
    total = len(results)
    passed = sum(1 for r in results.values() if r['all_ok'])
    
    print(f"Total de sitios analizados: {total}")
    print(f"Sitios que pasaron validación: {passed}")
    print(f"Tasa de éxito: {passed/total*100:.1f}%")
    print()
    
    # Detalles por tipo
    for control_type in [ControlType.NEGATIVE, ControlType.POSITIVE, ControlType.VALIDATION]:
        sites_of_type = [r for r in results.values() if r['control_type'] == control_type.value]
        passed_of_type = sum(1 for r in sites_of_type if r['all_ok'])
        
        if sites_of_type:
            print(f"{control_type.value.upper()}:")
            print(f"  Analizados: {len(sites_of_type)}")
            print(f"  Pasaron: {passed_of_type}")
            print(f"  Tasa: {passed_of_type/len(sites_of_type)*100:.1f}%")
            print()
    
    # Guardar resultados
    import json
    output_file = "calibration_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Resultados guardados en: {output_file}")
    print()
    
    print("="*80)
    print("✅ PROTOCOLO DE CALIBRACIÓN COMPLETADO")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(run_calibration_protocol())
