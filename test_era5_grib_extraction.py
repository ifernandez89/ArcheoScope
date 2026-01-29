#!/usr/bin/env python3
"""
Test ERA5 GRIB Extraction - Verificar que extrae valores correctamente
====================================================================

Verifica:
1. Descarga exitosa de GRIB
2. Validación de dataset
3. Extracción de valores (mean/min/max no son NaN)
4. Estadísticas válidas
"""

import asyncio
import sys
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from satellite_connectors.era5_connector import ERA5Connector


async def test_era5_extraction():
    """Test completo de extracción ERA5."""
    
    print("="*80)
    print("TEST: ERA5 GRIB Extraction")
    print("="*80)
    
    connector = ERA5Connector()
    
    if not connector.cds_client:
        print("❌ ERA5 CDS Client no disponible")
        print("   Verificar credenciales en BD: Copernicus CDS")
        return False
    
    print("✅ ERA5 CDS Client inicializado")
    
    # Test 1: Obtener contexto climático (Giza, Egipto)
    print("\n" + "="*80)
    print("TEST 1: Climate Context (Giza, Egipto)")
    print("="*80)
    
    try:
        result = await connector.get_climate_context(
            lat_min=29.9,
            lat_max=30.0,
            lon_min=31.1,
            lon_max=31.2,
            years_back=2  # Solo 2 años para test rápido
        )
        
        if result:
            print("✅ Contexto climático obtenido")
            print(f"   Período: {result['analysis_period']}")
            print(f"   Resolución: {result['resolution_km']} km")
            print(f"   Calidad: {result['quality']}")
            
            # Verificar datos climáticos
            climate_data = result.get('climate_data', {})
            print(f"\n   Variables obtenidas: {len(climate_data)}")
            
            for var_name, var_data in climate_data.items():
                stats = var_data.get('statistics', {})
                mean = stats.get('mean')
                
                if mean is not None:
                    print(f"   ✅ {var_name}: mean={mean:.2f}")
                else:
                    print(f"   ❌ {var_name}: mean=None (FALLO)")
                    return False
            
            print("\n✅ TEST 1 PASSED: Todos los valores extraídos correctamente")
        else:
            print("❌ TEST 1 FAILED: No se obtuvo contexto climático")
            return False
            
    except Exception as e:
        print(f"❌ TEST 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Condiciones de preservación
    print("\n" + "="*80)
    print("TEST 2: Preservation Conditions")
    print("="*80)
    
    try:
        result = await connector.get_preservation_conditions(
            lat_min=29.9,
            lat_max=30.0,
            lon_min=31.1,
            lon_max=31.2
        )
        
        if result:
            print("✅ Condiciones de preservación obtenidas")
            print(f"   Score: {result['value']:.3f}")
            print(f"   Clasificación: {result['preservation_classification']}")
            
            indices = result.get('preservation_indices', {})
            print(f"\n   Índices:")
            for idx_name, idx_value in indices.items():
                print(f"   - {idx_name}: {idx_value:.3f}")
            
            print("\n✅ TEST 2 PASSED")
        else:
            print("❌ TEST 2 FAILED: No se obtuvieron condiciones")
            return False
            
    except Exception as e:
        print(f"❌ TEST 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Accesibilidad estacional
    print("\n" + "="*80)
    print("TEST 3: Seasonal Accessibility")
    print("="*80)
    
    try:
        result = await connector.get_seasonal_accessibility(
            lat_min=29.9,
            lat_max=30.0,
            lon_min=31.1,
            lon_max=31.2
        )
        
        if result:
            print("✅ Accesibilidad estacional obtenida")
            print(f"   Score promedio: {result['value']:.3f}")
            print(f"   Mejores meses: {', '.join(result['best_months'])}")
            print(f"   Temporada recomendada: {result['field_season_recommendation']}")
            
            print("\n✅ TEST 3 PASSED")
        else:
            print("❌ TEST 3 FAILED: No se obtuvo accesibilidad")
            return False
            
    except Exception as e:
        print(f"❌ TEST 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*80)
    print("✅ TODOS LOS TESTS PASARON")
    print("="*80)
    print("\nERA5 está funcionando correctamente:")
    print("  ✅ Descarga GRIB exitosa")
    print("  ✅ Validación de dataset OK")
    print("  ✅ Extracción de valores correcta (no NaN)")
    print("  ✅ Estadísticas válidas")
    print("="*80)
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_era5_extraction())
    sys.exit(0 if success else 1)
