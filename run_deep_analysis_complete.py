#!/usr/bin/env python3
"""
Deep Analysis Complete - Master Script
=======================================

Ejecuta las 4 fases de análisis profundo sobre Puerto Rico North:

Phase A: Temporal Deep Analysis (MODIS/VIIRS/Landsat)
Phase B: SAR Behavioral Analysis (Sentinel-1)
Phase C: ICESat-2 Micro-adjustments (vertical stability)
Phase D: Multi-Scale Analysis (50m, 100m, 250m, 500m)

OBJETIVO: Exprimir máximo valor de datos existentes antes de pedir nuevos sensores
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any
import sys
import os

# Agregar backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from deep_temporal_analysis import DeepTemporalAnalyzer
from deep_sar_analysis import DeepSARAnalyzer
from deep_multiscale_analysis import MultiScaleAnalyzer, ICESat2Analyzer


# Zonas prioritarias del scan
PRIORITY_ZONES = {
    'puerto_rico_north': {
        'name': 'Puerto Rico North Continental Slope',
        'lat_min': 19.80,
        'lat_max': 19.98,
        'lon_min': -66.80,
        'lon_max': -66.56,
        'priority': 1,
        'tas_score': 1.000,
        'sar_coherence': 0.997,
        'thermal_stability': 0.955
    },
    'bermuda_node_a': {
        'name': 'Bermuda Node A',
        'lat_min': 32.20,
        'lat_max': 32.45,
        'lon_min': -64.90,
        'lon_max': -64.60,
        'priority': 2,
        'tas_score': 1.000,
        'coherencia_3d': 0.943
    },
    'puerto_rico_trench': {
        'name': 'Puerto Rico Trench Deep',
        'lat_min': 19.50,
        'lat_max': 19.70,
        'lon_min': -66.50,
        'lon_max': -66.20,
        'priority': 3,
        'tas_score': 1.000
    }
}


async def run_phase_a_temporal(zone_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phase A: Análisis Temporal Profundo
    
    - Phase-shift térmico
    - Retraso térmico vs entorno
    - Amortiguación de picos
    - Comparativa estacional extrema
    - Respuesta post-evento
    """
    
    print("\n" + "="*80)
    print("🌡️ PHASE A: DEEP TEMPORAL ANALYSIS")
    print("="*80)
    print(f"Zona: {zone_config['name']}")
    print(f"TAS Score: {zone_config.get('tas_score', 'N/A')}")
    
    analyzer = DeepTemporalAnalyzer()
    
    # Target: centro de la zona
    target_lat = (zone_config['lat_min'] + zone_config['lat_max']) / 2
    target_lon = (zone_config['lon_min'] + zone_config['lon_max']) / 2
    
    # Control: 10km al oeste
    control_lat = target_lat
    control_lon = target_lon - 0.1  # ~10km
    
    try:
        result = await analyzer.analyze_thermal_phase_shift(
            target_lat=target_lat,
            target_lon=target_lon,
            control_lat=control_lat,
            control_lon=control_lon,
            years=5
        )
        
        print(f"\n✅ Phase A completada")
        print(f"   Thermal Inertia Score: {result['thermal_inertia_score']:.3f}")
        print(f"   Phase Lag: {result['phase_lag_days']:.1f} días")
        print(f"   Damping Factor: {result['damping']['factor']:.3f}")
        
        return {
            'status': 'success',
            'zone': zone_config['name'],
            'results': result
        }
        
    except Exception as e:
        print(f"\n❌ Phase A falló: {e}")
        return {
            'status': 'error',
            'zone': zone_config['name'],
            'error': str(e)
        }


async def run_phase_b_sar(zone_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phase B: Análisis SAR Profundo
    
    - Multi-ángulo (ascending vs descending)
    - VV vs VH divergence
    - Speckle persistence
    - Phase decorrelation rate
    """
    
    print("\n" + "="*80)
    print("📡 PHASE B: DEEP SAR ANALYSIS")
    print("="*80)
    print(f"Zona: {zone_config['name']}")
    print(f"SAR Coherence: {zone_config.get('sar_coherence', 'N/A')}")
    
    analyzer = DeepSARAnalyzer()
    
    try:
        result = await analyzer.analyze_sar_behavior(
            lat_min=zone_config['lat_min'],
            lat_max=zone_config['lat_max'],
            lon_min=zone_config['lon_min'],
            lon_max=zone_config['lon_max']
        )
        
        print(f"\n✅ Phase B completada")
        print(f"   SAR Behavior Score: {result['behavior_score']:.3f}")
        print(f"   Rigidity Score: {result['multi_angle_geometry']['rigidity_score']:.3f}")
        print(f"   Stratification Index: {result['stratification']['index']:.3f}")
        
        return {
            'status': 'success',
            'zone': zone_config['name'],
            'results': result
        }
        
    except Exception as e:
        print(f"\n❌ Phase B falló: {e}")
        return {
            'status': 'error',
            'zone': zone_config['name'],
            'error': str(e)
        }


async def run_phase_c_icesat2(zone_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phase C: ICESat-2 Micro-ajustes Verticales
    
    - Micro-variaciones del nivel superficial
    - Correlación con mareas/presión
    - Rigidez subyacente
    """
    
    print("\n" + "="*80)
    print("🛰️ PHASE C: ICESat-2 MICRO-ADJUSTMENTS")
    print("="*80)
    print(f"Zona: {zone_config['name']}")
    
    analyzer = ICESat2Analyzer()
    
    try:
        result = await analyzer.analyze_vertical_microvariations(
            lat_min=zone_config['lat_min'],
            lat_max=zone_config['lat_max'],
            lon_min=zone_config['lon_min'],
            lon_max=zone_config['lon_max']
        )
        
        print(f"\n✅ Phase C completada")
        print(f"   {result['interpretation']}")
        
        return {
            'status': 'success',
            'zone': zone_config['name'],
            'results': result
        }
        
    except Exception as e:
        print(f"\n❌ Phase C falló: {e}")
        return {
            'status': 'error',
            'zone': zone_config['name'],
            'error': str(e)
        }


async def run_phase_d_multiscale(zone_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phase D: Análisis Multi-Escala (CLAVE)
    
    - Repetir métricas en: 50m, 100m, 250m, 500m
    - Buscar puntos donde coherencia NO decae
    - Natural: pierde coherencia al bajar escala
    - Artificial: NO pierde coherencia
    """
    
    print("\n" + "="*80)
    print("📏 PHASE D: MULTI-SCALE ANALYSIS")
    print("="*80)
    print(f"Zona: {zone_config['name']}")
    print(f"Coherencia 3D: {zone_config.get('coherencia_3d', 'N/A')}")
    print("⚠️ ADVERTENCIA: Esta fase toma 20-30 minutos (4 escalas × análisis completo)")
    
    analyzer = MultiScaleAnalyzer()
    
    try:
        result = await analyzer.analyze_scale_invariance(
            lat_min=zone_config['lat_min'],
            lat_max=zone_config['lat_max'],
            lon_min=zone_config['lon_min'],
            lon_max=zone_config['lon_max'],
            zone_name=zone_config['name']
        )
        
        print(f"\n✅ Phase D completada")
        print(f"   Scale Invariance Score: {result['scale_invariance']['invariance_score']:.3f}")
        print(f"   Coherence Decay Rate: {result['scale_invariance']['coherence_decay_rate']:.3f}")
        
        return {
            'status': 'success',
            'zone': zone_config['name'],
            'results': result
        }
        
    except Exception as e:
        print(f"\n❌ Phase D falló: {e}")
        return {
            'status': 'error',
            'zone': zone_config['name'],
            'error': str(e)
        }


async def run_complete_deep_analysis(zone_key: str = 'puerto_rico_north', skip_phase_d: bool = False):
    """
    Ejecutar análisis profundo completo en zona prioritaria
    """
    
    zone_config = PRIORITY_ZONES[zone_key]
    
    print("="*80)
    print("🔬 DEEP ANALYSIS COMPLETE - Master Script")
    print("="*80)
    print(f"Zona: {zone_config['name']}")
    print(f"Prioridad: {zone_config['priority']}")
    print(f"Coordenadas: [{zone_config['lat_min']:.2f}, {zone_config['lat_max']:.2f}] x [{zone_config['lon_min']:.2f}, {zone_config['lon_max']:.2f}]")
    print("="*80)
    
    start_time = datetime.now()
    
    # Ejecutar las 4 fases
    results = {
        'zone': zone_config['name'],
        'zone_key': zone_key,
        'start_time': start_time.isoformat(),
        'phases': {}
    }
    
    # Phase A: Temporal
    print("\n🚀 Iniciando Phase A: Temporal Deep Analysis...")
    results['phases']['phase_a_temporal'] = await run_phase_a_temporal(zone_config)
    
    # Phase B: SAR
    print("\n🚀 Iniciando Phase B: SAR Behavioral Analysis...")
    results['phases']['phase_b_sar'] = await run_phase_b_sar(zone_config)
    
    # Phase C: ICESat-2
    print("\n🚀 Iniciando Phase C: ICESat-2 Micro-adjustments...")
    results['phases']['phase_c_icesat2'] = await run_phase_c_icesat2(zone_config)
    
    # Phase D: Multi-Scale (ADVERTENCIA: toma tiempo)
    if not skip_phase_d:
        print("\n🚀 Iniciando Phase D: Multi-Scale Analysis...")
        print("⏱️ Esta fase puede tomar 20-30 minutos...")
        
        try:
            user_input = input("\n¿Continuar con Phase D? (s/n): ")
            if user_input.lower() == 's':
                results['phases']['phase_d_multiscale'] = await run_phase_d_multiscale(zone_config)
            else:
                print("⏭️ Phase D omitida por usuario")
                results['phases']['phase_d_multiscale'] = {
                    'status': 'skipped',
                    'zone': zone_config['name'],
                    'reason': 'User skipped'
                }
        except EOFError:
            print("\n⏭️ Phase D omitida (no input disponible)")
            results['phases']['phase_d_multiscale'] = {
                'status': 'skipped',
                'zone': zone_config['name'],
                'reason': 'No input available'
            }
    else:
        print("\n⏭️ Phase D omitida (--skip-phase-d)")
        results['phases']['phase_d_multiscale'] = {
            'status': 'skipped',
            'zone': zone_config['name'],
            'reason': 'Skipped via command line'
        }
    
    # Finalizar
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    results['end_time'] = end_time.isoformat()
    results['duration_seconds'] = duration
    results['duration_minutes'] = duration / 60
    
    # Guardar resultados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"deep_analysis_complete_{zone_key}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str, ensure_ascii=False)
    
    # Resumen final
    print("\n" + "="*80)
    print("✅ DEEP ANALYSIS COMPLETE - FINALIZADO")
    print("="*80)
    print(f"Zona: {zone_config['name']}")
    print(f"Duración total: {duration/60:.1f} minutos")
    print(f"\nResultados por fase:")
    
    for phase_name, phase_result in results['phases'].items():
        status_emoji = "✅" if phase_result['status'] == 'success' else "❌" if phase_result['status'] == 'error' else "⏭️"
        print(f"   {status_emoji} {phase_name}: {phase_result['status']}")
    
    print(f"\n📄 Resultados guardados: {filename}")
    print("="*80)
    
    return results


async def main():
    """
    Punto de entrada principal
    """
    
    import sys
    
    # Parsear argumentos de línea de comandos
    skip_phase_d = '--skip-phase-d' in sys.argv
    zone_key = 'puerto_rico_north'  # Default
    
    # Buscar argumento de zona
    for arg in sys.argv[1:]:
        if arg in PRIORITY_ZONES:
            zone_key = arg
    
    if skip_phase_d:
        print("\n⏭️ Phase D será omitida (--skip-phase-d)")
    
    # Si no hay argumentos, mostrar menú interactivo
    if len(sys.argv) == 1:
        print("\n🔬 DEEP ANALYSIS COMPLETE")
        print("Selecciona zona a analizar:")
        print()
        
        for i, (key, zone) in enumerate(PRIORITY_ZONES.items(), 1):
            print(f"{i}. {zone['name']} (Prioridad {zone['priority']})")
            if 'tas_score' in zone:
                print(f"   TAS: {zone['tas_score']:.3f}", end="")
            if 'sar_coherence' in zone:
                print(f" | SAR: {zone['sar_coherence']:.3f}", end="")
            if 'coherencia_3d' in zone:
                print(f" | 3D: {zone['coherencia_3d']:.3f}", end="")
            print()
        
        print()
        try:
            choice = input("Selecciona zona (1-3) o Enter para Puerto Rico North: ")
            
            if choice and choice.isdigit():
                zone_keys = list(PRIORITY_ZONES.keys())
                zone_key = zone_keys[int(choice) - 1]
        except (EOFError, KeyboardInterrupt):
            print("\nUsando zona por defecto: Puerto Rico North")
    
    await run_complete_deep_analysis(zone_key, skip_phase_d=skip_phase_d)


if __name__ == "__main__":
    asyncio.run(main())
