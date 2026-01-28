#!/usr/bin/env python3
"""
Test Directo - Coordenadas Antártida
=====================================

Coordenadas: -75.3544, -109.8832
Análisis directo con DATOS REALES

REGLA NRO 1: SOLO DATOS REALES - NO SIMULACIONES
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno PRIMERO
load_dotenv()

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

print("="*80)
print("🔍 ANÁLISIS ANTÁRTIDA - DATOS REALES")
print("="*80)
print()

# Coordenadas
LAT = -75.3544360283405
LON = -109.8831958757251
LAT_MIN = LAT - 0.05
LAT_MAX = LAT + 0.05
LON_MIN = LON - 0.05
LON_MAX = LON + 0.05

print(f"📍 COORDENADAS:")
print(f"   Latitud:  {LAT:.6f}° S")
print(f"   Longitud: {LON:.6f}° W")
print(f"   Bounding box: [{LAT_MIN:.4f}, {LAT_MAX:.4f}] x [{LON_MIN:.4f}, {LON_MAX:.4f}]")
print()

# PASO 1: Clasificar ambiente
print("="*80)
print("📍 PASO 1: CLASIFICACIÓN DE AMBIENTE")
print("="*80)
print()

try:
    from environment_classifier import EnvironmentClassifier
    
    classifier = EnvironmentClassifier()
    env_context = classifier.classify(LAT, LON)
    
    print(f"✅ Ambiente: {env_context.environment_type.value.upper()}")
    print(f"   Confianza: {env_context.confidence:.2%}")
    print(f"   Sensores: {', '.join(env_context.primary_sensors)}")
    print()

except Exception as e:
    print(f"❌ Error en clasificación: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# PASO 2: Obtener datos reales de instrumentos
print("="*80)
print("🛰️ PASO 2: OBTENCIÓN DE DATOS REALES")
print("="*80)
print()

async def get_real_data():
    """Obtener datos reales de APIs satelitales"""
    
    results = {}
    
    # Importar conectores
    try:
        from satellite_connectors.nsidc_connector import NSIDCConnector
        from satellite_connectors.modis_lst_connector import MODISLSTConnector
        from satellite_connectors.copernicus_marine_connector import CopernicusMarineConnector
        
        print("📡 Conectores importados exitosamente")
        print()
        
        # NSIDC - Hielo marino
        print("🧊 Obteniendo datos de NSIDC (hielo marino)...")
        try:
            nsidc = NSIDCConnector()
            if nsidc.available:
                ice_data = await nsidc.get_sea_ice_concentration(
                    LAT_MIN, LAT_MAX, LON_MIN, LON_MAX
                )
                if ice_data:
                    results['nsidc_ice'] = ice_data
                    print(f"   ✅ Concentración de hielo: {ice_data.get('value', 0):.2%}")
                    print(f"   📊 Modo de datos: {ice_data.get('data_mode', 'N/A')}")
                    print(f"   📊 Fuente: {ice_data.get('source', 'N/A')}")
                    if 'disclaimer' in ice_data:
                        print(f"   ⚠️  Disclaimer: {ice_data['disclaimer'][:80]}...")
                else:
                    print(f"   ⚠️  No hay datos disponibles")
            else:
                print(f"   ⚠️  NSIDC no disponible (credenciales faltantes)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # MODIS LST - Temperatura
        print("🌡️ Obteniendo datos de MODIS LST (temperatura)...")
        try:
            modis = MODISLSTConnector()
            if modis.available:
                lst_data = await modis.get_land_surface_temperature(
                    LAT_MIN, LAT_MAX, LON_MIN, LON_MAX
                )
                if lst_data:
                    results['modis_lst'] = lst_data
                    print(f"   ✅ LST día: {lst_data.get('lst_day_celsius', 0):.1f}°C")
                    print(f"   ✅ LST noche: {lst_data.get('lst_night_celsius', 0):.1f}°C")
                    print(f"   ✅ Inercia térmica: {lst_data.get('thermal_inertia', 0):.1f}K")
                    print(f"   📊 Modo de datos: {lst_data.get('data_mode', 'N/A')}")
                    print(f"   📊 Fuente: {lst_data.get('source', 'N/A')}")
                    if 'disclaimer' in lst_data:
                        print(f"   ⚠️  Disclaimer: {lst_data['disclaimer'][:80]}...")
                else:
                    print(f"   ⚠️  No hay datos disponibles")
            else:
                print(f"   ⚠️  MODIS LST no disponible (credenciales faltantes)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Copernicus Marine - Océano
        print("🌊 Obteniendo datos de Copernicus Marine (océano)...")
        try:
            copernicus = CopernicusMarineConnector()
            if copernicus.available:
                marine_data = await copernicus.get_sea_ice_concentration(
                    LAT_MIN, LAT_MAX, LON_MIN, LON_MAX
                )
                if marine_data:
                    results['copernicus_marine'] = marine_data
                    print(f"   ✅ Concentración hielo marino: {marine_data.get('value', 0):.2%}")
                    print(f"   📊 Modo de datos: {marine_data.get('data_mode', 'N/A')}")
                    print(f"   📊 Fuente: {marine_data.get('source', 'N/A')}")
                    if 'disclaimer' in marine_data:
                        print(f"   ⚠️  Disclaimer: {marine_data['disclaimer'][:80]}...")
                else:
                    print(f"   ⚠️  No hay datos disponibles")
            else:
                print(f"   ⚠️  Copernicus Marine no disponible")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
    except ImportError as e:
        print(f"❌ Error importando conectores: {e}")
        print("   Algunos conectores pueden no estar disponibles")
        print()
    
    return results

# Ejecutar obtención de datos
try:
    real_data = asyncio.run(get_real_data())
except Exception as e:
    print(f"❌ Error obteniendo datos reales: {e}")
    real_data = {}

# PASO 3: Análisis de resultados
print("="*80)
print("🎯 PASO 3: ANÁLISIS DE RESULTADOS")
print("="*80)
print()

if real_data:
    print(f"✅ Se obtuvieron datos de {len(real_data)} instrumentos")
    print()
    
    # Analizar cada instrumento
    anomalies_detected = []
    
    for instrument, data in real_data.items():
        print(f"📊 {instrument.upper()}:")
        print(f"   Valor: {data.get('value', 'N/A')}")
        print(f"   Modo: {data.get('data_mode', 'N/A')}")
        print(f"   Confianza: {data.get('confidence', 'N/A')}")
        
        # Verificar si hay anomalía (simplificado)
        value = data.get('value', 0)
        if isinstance(value, (int, float)):
            if value > 0.7:  # Umbral alto
                anomalies_detected.append(instrument)
                print(f"   🔴 ANOMALÍA: Valor alto detectado")
            elif value > 0.3:
                print(f"   🟡 VALOR MODERADO")
            else:
                print(f"   🟢 VALOR NORMAL")
        print()
    
    # Conclusión
    print("="*80)
    print("🎯 CONCLUSIÓN")
    print("="*80)
    print()
    
    if anomalies_detected:
        print(f"🔴 ANOMALÍAS INSTRUMENTALES DETECTADAS ({len(anomalies_detected)}):")
        for inst in anomalies_detected:
            print(f"   • {inst}")
        print()
        print("⚠️  INTERPRETACIÓN CORRECTA:")
        print("   • Anomalía instrumental en zona antártica")
        print("   • Compatible con fenómeno glaciológico/oceanográfico")
        print("   • NO tiene interpretación arqueológica")
        print("   • Zona sin ocupación humana prehistórica")
    else:
        print("🟢 NO SE DETECTARON ANOMALÍAS SIGNIFICATIVAS")
        print()
        print("   Valores instrumentales dentro de rangos normales")
        print("   para zona antártica")
    
else:
    print("⚠️  No se pudieron obtener datos reales")
    print()
    print("   Posibles razones:")
    print("   • Credenciales no configuradas en .env")
    print("   • APIs no disponibles para esta zona")
    print("   • Problemas de conectividad")

print()
print("="*80)
print("⚠️  DISCLAIMER CIENTÍFICO")
print("="*80)
print()
print("Este análisis usa DATOS REALES de APIs satelitales.")
print()
print("Modo de datos:")
print("  • REAL: Mediciones directas de APIs")
print("  • DERIVED: Estimaciones basadas en modelos")
print("  • INFERRED: Inferencias geométricas")
print()
print("IMPORTANTE:")
print("  • Zona antártica SIN contexto arqueológico")
print("  • Anomalías detectadas son fenómenos naturales")
print("  • NO hay interpretación arqueológica válida")
print("  • Requiere análisis por glaciólogos/oceanógrafos")
print()

# Guardar resultado
output_file = f"analisis_antartida_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
result = {
    'coordinates': {
        'lat': LAT,
        'lon': LON,
        'lat_min': LAT_MIN,
        'lat_max': LAT_MAX,
        'lon_min': LON_MIN,
        'lon_max': LON_MAX
    },
    'environment': {
        'type': env_context.environment_type.value,
        'confidence': env_context.confidence
    },
    'real_data': real_data,
    'timestamp': datetime.now().isoformat(),
    'note': 'Análisis con DATOS REALES - Zona antártica sin contexto arqueológico'
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False, default=str)

print(f"💾 Resultado guardado en: {output_file}")
print()
print("="*80)
print("✅ ANÁLISIS COMPLETADO")
print("="*80)
