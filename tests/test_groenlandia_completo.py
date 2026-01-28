#!/usr/bin/env python3
"""
Test completo de instrumentos en Groenlandia
Verificar que las mediciones sean apropiadas para arqueología glaciar
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_groenlandia():
    print("="*80)
    print("ANÁLISIS COMPLETO - GROENLANDIA (Arqueología Glaciar)")
    print("="*80)
    
    from satellite_connectors.real_data_integrator import RealDataIntegrator
    integrator = RealDataIntegrator()
    
    # Groenlandia - Margen glaciar oeste (zona con retroceso)
    # Coordenadas: cerca de Ilulissat (zona con retroceso glaciar documentado)
    lat_min, lat_max = 69.2, 69.3
    lon_min, lon_max = -51.1, -51.0
    
    print(f"\nRegión: Ilulissat, Groenlandia Oeste")
    print(f"Coordenadas: {lat_min:.2f}°N - {lat_max:.2f}°N, {lon_min:.2f}°E - {lon_max:.2f}°E")
    print(f"Contexto: Margen glaciar con retroceso acelerado")
    print("="*80)
    
    # Test cada instrumento relevante para glaciares
    instrumentos = [
        ("icesat2", "ICESat-2 Elevación", "Detectar terrazas y alineamientos"),
        ("sentinel_1_sar", "Sentinel-1 SAR", "Penetración hielo, estructuras subsuperficiales"),
        ("sentinel_2_ndvi", "Sentinel-2 NDVI", "Vegetación en zonas deglaciadas"),
        ("landsat_thermal", "Landsat Thermal", "Inercia térmica de estructuras vs roca"),
        ("nsidc_sea_ice", "NSIDC Sea Ice", "Contexto de hielo marino costero"),
        ("modis_lst", "MODIS LST", "Patrones térmicos regionales"),
    ]
    
    resultados = {}
    
    for inst_name, inst_label, uso_arqueologico in instrumentos:
        print(f"\n{'='*80}")
        print(f"INSTRUMENTO: {inst_label}")
        print(f"Uso arqueológico: {uso_arqueologico}")
        print(f"{'='*80}")
        
        try:
            result = await integrator.get_instrument_measurement(
                instrument_name=inst_name,
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max
            )
            
            if result:
                status = result.get('status', 'UNKNOWN')
                value = result.get('value')
                confidence = result.get('confidence', 0.0)
                source = result.get('source', 'Unknown')
                
                print(f"✅ MEDICIÓN EXITOSA")
                print(f"   Status: {status}")
                print(f"   Valor: {value}")
                print(f"   Confidence: {confidence}")
                print(f"   Fuente: {source}")
                
                # Análisis de calidad para arqueología
                if status == 'OK':
                    print(f"   🎯 CALIDAD: EXCELENTE - Medición directa")
                elif status == 'DERIVED':
                    print(f"   ⚠️  CALIDAD: ESTIMADA - Usar con precaución")
                else:
                    print(f"   ❌ CALIDAD: NO USABLE")
                
                # Verificar si el valor es útil para arqueología
                if inst_name == "icesat2" and value:
                    if value > 0:
                        print(f"   📊 ANÁLISIS: Elevación {value:.1f}m - útil para detectar terrazas")
                    else:
                        print(f"   ⚠️  ANÁLISIS: Elevación negativa o cero - verificar")
                
                elif inst_name == "sentinel_1_sar" and value:
                    if -30 < value < 10:
                        print(f"   📊 ANÁLISIS: Backscatter {value:.1f}dB - rango normal para hielo/roca")
                    else:
                        print(f"   ⚠️  ANÁLISIS: Backscatter fuera de rango esperado")
                
                elif inst_name == "sentinel_2_ndvi" and value:
                    if value > 0.2:
                        print(f"   📊 ANÁLISIS: NDVI {value:.3f} - vegetación presente (zona deglaciada)")
                    elif value > 0:
                        print(f"   📊 ANÁLISIS: NDVI {value:.3f} - vegetación escasa (transición)")
                    else:
                        print(f"   📊 ANÁLISIS: NDVI {value:.3f} - sin vegetación (hielo/roca)")
                
                elif inst_name == "landsat_thermal" and value:
                    if 250 < value < 290:
                        print(f"   📊 ANÁLISIS: LST {value:.1f}K ({value-273.15:.1f}°C) - rango glaciar normal")
                    else:
                        print(f"   ⚠️  ANÁLISIS: Temperatura fuera de rango esperado para glaciar")
                
                resultados[inst_name] = {
                    'status': status,
                    'value': value,
                    'confidence': confidence,
                    'usable': status in ['OK', 'DERIVED']
                }
            else:
                print(f"❌ SIN DATOS")
                resultados[inst_name] = {'status': 'NO_DATA', 'usable': False}
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            resultados[inst_name] = {'status': 'ERROR', 'usable': False}
    
    # RESUMEN FINAL
    print("\n" + "="*80)
    print("RESUMEN - CAPACIDAD PARA ARQUEOLOGÍA GLACIAR EN GROENLANDIA")
    print("="*80)
    
    usables = sum(1 for r in resultados.values() if r.get('usable', False))
    total = len(resultados)
    
    print(f"\nInstrumentos usables: {usables}/{total} ({usables/total*100:.1f}%)")
    
    print("\nPor instrumento:")
    for inst_name, inst_label, uso in instrumentos:
        r = resultados.get(inst_name, {})
        status = r.get('status', 'UNKNOWN')
        usable = r.get('usable', False)
        
        if usable:
            print(f"  ✅ {inst_label}: {status}")
        else:
            print(f"  ❌ {inst_label}: {status}")
    
    # RECOMENDACIONES
    print("\n" + "="*80)
    print("RECOMENDACIONES PARA ARQUEOLOGÍA GLACIAR")
    print("="*80)
    
    if resultados.get('icesat2', {}).get('usable'):
        print("✅ ICESat-2 funciona - CRÍTICO para detectar terrazas y alineamientos")
    else:
        print("❌ ICESat-2 no disponible - PROBLEMA CRÍTICO para arqueología glaciar")
        print("   Solución: Ampliar ventana temporal o usar DEM alternativo")
    
    if resultados.get('sentinel_1_sar', {}).get('usable'):
        print("✅ SAR funciona - EXCELENTE para penetración de hielo")
    else:
        print("⚠️  SAR no disponible - Limita detección subsuperficial")
    
    if resultados.get('sentinel_2_ndvi', {}).get('usable'):
        print("✅ NDVI funciona - Útil para mapear zonas deglaciadas")
    else:
        print("⚠️  NDVI no disponible - Limita identificación de zonas expuestas")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    asyncio.run(test_groenlandia())
