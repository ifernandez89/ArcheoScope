#!/usr/bin/env python3
"""
Test Rápido - 5 Nuevos Instrumentos Satelitales
==============================================

OBJETIVO: Verificar que los 5 nuevos instrumentos están correctamente integrados:

11. VIIRS (térmico/NDVI/fuego)
12. SRTM (DEM topográfico)  
13. ALOS PALSAR-2 (SAR L-band)
14. ERA5 (clima/preservación)
15. CHIRPS (precipitación histórica)

COORDENADAS DE PRUEBA: Giza, Egipto (sitio conocido en desierto)
"""

import asyncio
import sys
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar path del backend
sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_nuevos_instrumentos():
    """Test específico de los 5 nuevos instrumentos."""
    
    print("🆕 ARCHEOSCOPE - TEST DE 5 NUEVOS INSTRUMENTOS")
    print("=" * 60)
    print("OBJETIVO: Verificar integración de VIIRS, SRTM, PALSAR-2, ERA5, CHIRPS")
    print("COORDENADAS: Giza, Egipto (29.95°N, 31.15°E)")
    print("=" * 60)
    
    try:
        # Importar integrador
        from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
        integrator = RealDataIntegratorV2()
        
        print("✅ RealDataIntegratorV2 inicializado correctamente")
        
    except Exception as e:
        print(f"❌ Error importando integrador: {e}")
        return False
    
    # Coordenadas de Giza
    lat_min, lat_max = 29.9, 30.0
    lon_min, lon_max = 31.1, 31.2
    
    print(f"\n🎯 Región de prueba: [{lat_min:.1f}, {lat_max:.1f}] x [{lon_min:.1f}, {lon_max:.1f}]")
    
    # Definir nuevos instrumentos a probar
    nuevos_instrumentos = [
        {
            'name': 'viirs_thermal',
            'description': 'VIIRS - Detección térmica (375m)',
            'expected': 'Anomalías térmicas en estructuras'
        },
        {
            'name': 'srtm_elevation', 
            'description': 'SRTM - Modelo digital elevación (30m)',
            'expected': 'Elevaciones de pirámides'
        },
        {
            'name': 'palsar_backscatter',
            'description': 'PALSAR-2 - SAR L-band (25m)',
            'expected': 'Backscatter de estructuras'
        },
        {
            'name': 'era5_climate',
            'description': 'ERA5 - Contexto climático (25km)',
            'expected': 'Condiciones áridas estables'
        },
        {
            'name': 'chirps_precipitation',
            'description': 'CHIRPS - Precipitación histórica (5km)',
            'expected': 'Patrón de precipitación desértico'
        }
    ]
    
    resultados = {}
    instrumentos_exitosos = 0
    
    # Probar cada instrumento
    for i, instrumento in enumerate(nuevos_instrumentos, 1):
        print(f"\n🛰️ [{i}/5] PROBANDO: {instrumento['name']}")
        print(f"    📝 {instrumento['description']}")
        print(f"    🎯 Esperado: {instrumento['expected']}")
        
        try:
            # Realizar medición
            print("    🔄 Ejecutando medición...")
            
            resultado = await integrator.get_instrument_measurement_robust(
                instrument_name=instrumento['name'],
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max
            )
            
            if resultado:
                # Extraer información del resultado
                status = getattr(resultado, 'status', 'UNKNOWN')
                value = getattr(resultado, 'value', None)
                unit = getattr(resultado, 'unit', 'units')
                processing_time = getattr(resultado, 'processing_time_s', 0)
                reason = getattr(resultado, 'reason', '')
                
                print(f"    ✅ STATUS: {status}")
                
                if value is not None:
                    print(f"    📊 VALOR: {value:.3f} {unit}")
                else:
                    print(f"    📊 VALOR: N/A")
                
                print(f"    ⏱️ TIEMPO: {processing_time:.2f}s")
                
                if reason:
                    print(f"    💬 RAZÓN: {reason}")
                
                # Evaluar éxito
                exito = status in ['SUCCESS', 'DEGRADED'] and value is not None
                
                if exito:
                    print(f"    🎉 ¡INSTRUMENTO FUNCIONANDO!")
                    instrumentos_exitosos += 1
                else:
                    print(f"    ⚠️ Instrumento con problemas")
                
                resultados[instrumento['name']] = {
                    'success': exito,
                    'status': status,
                    'value': value,
                    'unit': unit,
                    'processing_time': processing_time,
                    'reason': reason
                }
                
            else:
                print(f"    ❌ SIN DATOS - API no respondió")
                resultados[instrumento['name']] = {
                    'success': False,
                    'status': 'NO_DATA',
                    'reason': 'API no respondió'
                }
                
        except Exception as e:
            print(f"    💥 ERROR: {e}")
            resultados[instrumento['name']] = {
                'success': False,
                'status': 'ERROR',
                'error': str(e)
            }
    
    # Reporte final
    print("\n" + "=" * 60)
    print("📋 REPORTE FINAL - NUEVOS INSTRUMENTOS")
    print("=" * 60)
    
    tasa_exito = instrumentos_exitosos / len(nuevos_instrumentos)
    
    print(f"🎯 INSTRUMENTOS EXITOSOS: {instrumentos_exitosos}/{len(nuevos_instrumentos)}")
    print(f"🎯 TASA DE ÉXITO: {tasa_exito:.1%}")
    
    # Detalles por instrumento
    print(f"\n📊 DETALLES POR INSTRUMENTO:")
    for instrumento in nuevos_instrumentos:
        name = instrumento['name']
        resultado = resultados.get(name, {})
        
        if resultado.get('success'):
            status_icon = "✅"
            status_text = f"OK ({resultado.get('status', 'SUCCESS')})"
        else:
            status_icon = "❌"
            status_text = f"FALLO ({resultado.get('status', 'ERROR')})"
        
        print(f"  {status_icon} {name}: {status_text}")
        
        if resultado.get('value') is not None:
            print(f"      Valor: {resultado['value']:.3f} {resultado.get('unit', 'units')}")
        
        if resultado.get('reason'):
            print(f"      Razón: {resultado['reason']}")
    
    # Evaluación general
    print(f"\n🔍 EVALUACIÓN GENERAL:")
    
    if tasa_exito >= 0.8:  # 4/5 o más
        print("🎉 ¡EXCELENTE! La mayoría de instrumentos funcionan correctamente")
        print("✅ Sistema listo para análisis arqueológico completo")
        evaluation = "EXCELENTE"
    elif tasa_exito >= 0.6:  # 3/5
        print("👍 BUENO. Suficientes instrumentos para análisis básico")
        print("⚠️ Algunos instrumentos necesitan revisión")
        evaluation = "BUENO"
    elif tasa_exito >= 0.4:  # 2/5
        print("⚠️ REGULAR. Funcionalidad limitada")
        print("🔧 Revisar configuración de APIs")
        evaluation = "REGULAR"
    else:  # <2/5
        print("❌ PROBLEMAS SERIOS. Mayoría de instrumentos fallan")
        print("🚨 Revisar configuración completa del sistema")
        evaluation = "PROBLEMAS"
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    
    if 'viirs_thermal' in resultados and not resultados['viirs_thermal'].get('success'):
        print("  🔧 VIIRS: Verificar credenciales NASA Earthdata")
    
    if 'srtm_elevation' in resultados and not resultados['srtm_elevation'].get('success'):
        print("  🔧 SRTM: Verificar API key OpenTopography")
    
    if 'palsar_backscatter' in resultados and not resultados['palsar_backscatter'].get('success'):
        print("  🔧 PALSAR-2: Verificar acceso ASF DAAC")
    
    if 'era5_climate' in resultados and not resultados['era5_climate'].get('success'):
        print("  🔧 ERA5: Verificar configuración Copernicus CDS")
    
    if 'chirps_precipitation' in resultados and not resultados['chirps_precipitation'].get('success'):
        print("  🔧 CHIRPS: Verificar acceso ClimateSERV API")
    
    if tasa_exito >= 0.6:
        print("  🏠 LISTO PARA CASA: Puedes probar con coordenadas candidatas")
    else:
        print("  🔧 CONFIGURAR PRIMERO: Resolver problemas antes de usar en casa")
    
    print(f"\n{'='*60}")
    
    return tasa_exito >= 0.6  # Éxito si al menos 3/5 funcionan

if __name__ == "__main__":
    async def main():
        exito = await test_nuevos_instrumentos()
        
        if exito:
            print("\n🎉 ¡TEST EXITOSO!")
            print("✅ Nuevos instrumentos integrados correctamente")
            print("🚀 Continúa con test completo de 15 instrumentos")
        else:
            print("\n⚠️ Test con problemas")
            print("🔧 Revisar configuración antes de continuar")
        
        return exito
    
    # Ejecutar
    success = asyncio.run(main())
    sys.exit(0 if success else 1)