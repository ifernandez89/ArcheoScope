#!/usr/bin/env python3
"""
Test de Datos Satelitales Reales
Verifica conexión a Planetary Computer y descarga de datos
"""

import asyncio
import sys
import logging
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_planetary_computer():
    """Test completo de Planetary Computer"""
    
    print("=" * 80)
    print("🛰️  TEST: DATOS SATELITALES REALES - PLANETARY COMPUTER")
    print("=" * 80)
    
    try:
        from backend.async_satellite_processor import async_satellite_processor
        from backend.satellite_cache import satellite_cache
    except ImportError as e:
        print(f"\n❌ Error importando módulos: {e}")
        print("\n📦 Instala las dependencias:")
        print("   pip install -r requirements-satellite.txt")
        return False
    
    # Test 1: Zona en Senegal (tu candidata CRITICAL)
    print("\n" + "=" * 80)
    print("TEST 1: Candidata CRITICAL en Senegal")
    print("=" * 80)
    
    lat_min, lat_max = -7.1600, -7.1400
    lon_min, lon_max = -109.3750, -109.3550
    
    print(f"\n📍 Bbox: [{lat_min}, {lat_max}, {lon_min}, {lon_max}]")
    print(f"📅 Período: Últimos 30 días")
    
    try:
        print("\n⏳ Descargando datos satelitales (puede tomar 15-30 segundos)...")
        
        start_time = asyncio.get_event_loop().time()
        
        # Obtener todos los datos
        all_data = await async_satellite_processor.get_all_data(
            lat_min, lat_max, lon_min, lon_max
        )
        
        total_time = asyncio.get_event_loop().time() - start_time
        
        print(f"\n✅ Datos obtenidos en {total_time:.2f} segundos")
        
        # Mostrar resultados
        print("\n" + "-" * 80)
        print("📊 RESULTADOS:")
        print("-" * 80)
        
        for data_type, data in all_data.items():
            print(f"\n🛰️  {data_type.upper()}:")
            
            if data is None:
                print("   ❌ No disponible")
                continue
            
            print(f"   ✅ Fuente: {data.source}")
            print(f"   📅 Fecha: {data.acquisition_date.strftime('%Y-%m-%d')}")
            print(f"   ☁️  Nubes: {data.cloud_cover:.1f}%")
            print(f"   📏 Resolución: {data.resolution_m}m")
            print(f"   ⚡ Anomalía: {data.anomaly_score:.3f} ({data.anomaly_type})")
            print(f"   🎯 Confianza: {data.confidence:.3f}")
            print(f"   ⏱️  Tiempo: {data.processing_time_s:.2f}s")
            print(f"   💾 Caché: {'SÍ' if data.cached else 'NO'}")
            
            # Mostrar índices
            if data.indices:
                print(f"   📈 Índices:")
                for key, value in data.indices.items():
                    print(f"      • {key}: {value:.4f}")
        
        # Test 2: Verificar caché
        print("\n" + "=" * 80)
        print("TEST 2: Verificación de Caché")
        print("=" * 80)
        
        print("\n⏳ Repitiendo consulta (debería usar caché)...")
        
        start_time = asyncio.get_event_loop().time()
        
        all_data_cached = await async_satellite_processor.get_all_data(
            lat_min, lat_max, lon_min, lon_max
        )
        
        cached_time = asyncio.get_event_loop().time() - start_time
        
        print(f"\n✅ Datos obtenidos en {cached_time:.2f} segundos")
        
        # Verificar que usó caché
        cached_count = sum(1 for d in all_data_cached.values() if d and d.cached)
        print(f"\n💾 Datos desde caché: {cached_count}/3")
        
        if cached_count > 0:
            speedup = total_time / cached_time if cached_time > 0 else float('inf')
            print(f"⚡ Aceleración: {speedup:.1f}x más rápido")
        
        # Test 3: Estadísticas de caché
        print("\n" + "=" * 80)
        print("TEST 3: Estadísticas de Caché")
        print("=" * 80)
        
        stats = satellite_cache.get_stats()
        
        print(f"\n📊 Estadísticas:")
        print(f"   • Total entradas: {stats['total_entries']}")
        print(f"   • Tamaño total: {stats['total_size_mb']:.2f} MB")
        print(f"   • Por tipo:")
        for data_type, count in stats['by_type'].items():
            print(f"      - {data_type}: {count}")
        print(f"   • Directorio: {stats['cache_dir']}")
        
        # Test 4: Resumen rápido
        print("\n" + "=" * 80)
        print("TEST 4: Resumen Rápido (API optimizada)")
        print("=" * 80)
        
        print("\n⏳ Obteniendo resumen...")
        
        start_time = asyncio.get_event_loop().time()
        
        summary = await async_satellite_processor.get_quick_summary(
            lat_min, lat_max, lon_min, lon_max
        )
        
        summary_time = asyncio.get_event_loop().time() - start_time
        
        print(f"\n✅ Resumen obtenido en {summary_time:.2f} segundos")
        print(f"\n📊 Score Multi-Instrumental: {summary['multi_instrumental_score']:.3f}")
        print(f"⚡ Convergencia: {summary['convergence_count']}/3 ({summary['convergence_ratio']*100:.0f}%)")
        
        # Resumen final
        print("\n" + "=" * 80)
        print("✅ TODOS LOS TESTS COMPLETADOS")
        print("=" * 80)
        
        print(f"\n🎯 Resultados:")
        print(f"   • Primera descarga: {total_time:.2f}s")
        print(f"   • Con caché: {cached_time:.2f}s")
        print(f"   • Resumen rápido: {summary_time:.2f}s")
        print(f"   • Datos exitosos: {sum(1 for d in all_data.values() if d)}/3")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_small_area():
    """Test con área pequeña para ser más rápido"""
    
    print("\n" + "=" * 80)
    print("TEST RÁPIDO: Área Pequeña (Giza, Egipto)")
    print("=" * 80)
    
    try:
        from backend.async_satellite_processor import async_satellite_processor
    except ImportError:
        print("❌ Módulos no disponibles")
        return False
    
    # Área pequeña en Giza
    lat_min, lat_max = 29.975, 29.980
    lon_min, lon_max = 31.130, 31.135
    
    print(f"\n📍 Bbox: [{lat_min}, {lat_max}, {lon_min}, {lon_max}]")
    print(f"📏 Área: ~0.5 km²")
    
    try:
        print("\n⏳ Descargando datos...")
        
        start_time = asyncio.get_event_loop().time()
        
        summary = await async_satellite_processor.get_quick_summary(
            lat_min, lat_max, lon_min, lon_max
        )
        
        total_time = asyncio.get_event_loop().time() - start_time
        
        print(f"\n✅ Completado en {total_time:.2f} segundos")
        print(f"\n📊 Score: {summary['multi_instrumental_score']:.3f}")
        print(f"⚡ Convergencia: {summary['convergence_count']}/3")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("\n🚀 Iniciando tests de datos satelitales reales...\n")
    
    # Elegir test
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        success = asyncio.run(test_small_area())
    else:
        success = asyncio.run(test_planetary_computer())
    
    if success:
        print("\n✅ Tests exitosos!")
        sys.exit(0)
    else:
        print("\n❌ Tests fallidos")
        sys.exit(1)
