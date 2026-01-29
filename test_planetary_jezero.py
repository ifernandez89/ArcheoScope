#!/usr/bin/env python3
"""
Test de ArcheoScope Planetary - Jezero Crater
==============================================

Primer test del sistema planetario analizando Jezero Crater,
el sitio de aterrizaje del rover Perseverance.

Coordenadas: 18.38°N, 77.58°E
Interés: Paleolacustre, delta antiguo, búsqueda de vida
"""

import sys
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from planetary.mars.ode_connector import (
    CTXConnector,
    HiRISEConnector,
    THEMISConnector,
    MOLAConnector
)


def test_jezero_crater():
    """Test de cobertura de datos en Jezero Crater."""
    
    print("="*80)
    print("🚀 ArcheoScope Planetary - Test Jezero Crater")
    print("="*80)
    print()
    print("📍 Jezero Crater")
    print("   Coordenadas: 18.38°N, 77.58°E")
    print("   Rover: Perseverance (NASA)")
    print("   Interés: Paleolacustre, delta antiguo")
    print()
    
    # Definir región de interés (±0.5° alrededor del centro)
    lat_center = 18.38
    lon_center = 77.58
    delta = 0.5
    
    lat_min = lat_center - delta
    lat_max = lat_center + delta
    lon_min = lon_center - delta
    lon_max = lon_center + delta
    
    print(f"📦 Región de análisis:")
    print(f"   Lat: [{lat_min:.2f}, {lat_max:.2f}]")
    print(f"   Lon: [{lon_min:.2f}, {lon_max:.2f}]")
    print(f"   Área: ~{(2*delta*111)**2:.0f} km²")
    print()
    
    # Test de conectores
    instrumentos = [
        ('CTX', CTXConnector(), '6 m/pixel'),
        ('HiRISE', HiRISEConnector(), '25-50 cm/pixel'),
        ('THEMIS', THEMISConnector(), '100 m/pixel'),
        ('MOLA', MOLAConnector(), '463 m/pixel')
    ]
    
    print("="*80)
    print("📊 COBERTURA DE INSTRUMENTOS")
    print("="*80)
    print()
    
    resultados = {}
    
    for nombre, conector, resolucion in instrumentos:
        print(f"🔍 {nombre} ({resolucion})")
        print(f"   Buscando datos...")
        
        try:
            coverage = conector.get_coverage(
                conector.instrument,
                lat_min, lat_max,
                lon_min, lon_max
            )
            
            if coverage['available']:
                print(f"   ✅ Datos disponibles")
                print(f"   📊 Productos: {coverage['count']}")
                print(f"   📈 Cobertura: {coverage['coverage_percent']:.1f}%")
                if coverage.get('latest_date'):
                    print(f"   📅 Última adquisición: {coverage['latest_date']}")
                resultados[nombre] = coverage
            else:
                print(f"   ❌ Sin datos disponibles")
                resultados[nombre] = None
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            resultados[nombre] = None
        
        print()
    
    # Resumen
    print("="*80)
    print("📈 RESUMEN DE COBERTURA")
    print("="*80)
    print()
    
    disponibles = sum(1 for r in resultados.values() if r and r['available'])
    total = len(resultados)
    
    print(f"Instrumentos disponibles: {disponibles}/{total}")
    print()
    
    for nombre, resultado in resultados.items():
        if resultado and resultado['available']:
            status = "✅"
            info = f"{resultado['count']} productos, {resultado['coverage_percent']:.1f}% cobertura"
        else:
            status = "❌"
            info = "Sin datos"
        
        print(f"{status} {nombre:10s} - {info}")
    
    print()
    
    # Evaluación
    if disponibles >= 3:
        print("✅ JEZERO CRATER: Cobertura suficiente para análisis")
        print()
        print("Próximos pasos:")
        print("1. Descargar productos de alta resolución (HiRISE)")
        print("2. Generar DEM con MOLA")
        print("3. Análisis térmico con THEMIS")
        print("4. Contexto regional con CTX")
    elif disponibles >= 1:
        print("⚠️ JEZERO CRATER: Cobertura parcial")
        print("   Análisis limitado posible")
    else:
        print("❌ JEZERO CRATER: Cobertura insuficiente")
        print("   Verificar conectores y APIs")
    
    print()
    print("="*80)
    print("✅ TEST COMPLETADO")
    print("="*80)
    
    return resultados


if __name__ == "__main__":
    try:
        resultados = test_jezero_crater()
    except KeyboardInterrupt:
        print("\n⚠️ Test interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
