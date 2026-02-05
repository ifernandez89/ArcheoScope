#!/usr/bin/env python3
"""
Test Deep Analysis Connections
================================

Verifica que todas las conexiones a datos reales funcionen correctamente
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from deep_temporal_analysis import DeepTemporalAnalyzer
from deep_sar_analysis import DeepSARAnalyzer
from deep_multiscale_analysis import ICESat2Analyzer


async def test_temporal_connection():
    """Test Phase A: Temporal Analysis"""
    
    print("\n" + "="*80)
    print("🌡️ TEST: Phase A - Temporal Analysis Connection")
    print("="*80)
    
    analyzer = DeepTemporalAnalyzer()
    
    # Test con Puerto Rico North
    target_lat, target_lon = 19.89, -66.68
    control_lat, control_lon = 19.85, -66.75
    
    try:
        print("\n📡 Obteniendo serie térmica de 1 año (test rápido)...")
        
        # Test con 1 año en vez de 5 para velocidad
        result = await analyzer.analyze_thermal_phase_shift(
            target_lat=target_lat,
            target_lon=target_lon,
            control_lat=control_lat,
            control_lon=control_lon,
            years=1  # Solo 1 año para test
        )
        
        print(f"\n✅ Phase A: CONEXIÓN OK")
        print(f"   Thermal Inertia Score: {result['thermal_inertia_score']:.3f}")
        print(f"   Phase Lag: {result['phase_lag_days']:.1f} días")
        print(f"   Damping Factor: {result['damping']['factor']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Phase A: CONEXIÓN FALLÓ")
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_sar_connection():
    """Test Phase B: SAR Analysis"""
    
    print("\n" + "="*80)
    print("📡 TEST: Phase B - SAR Analysis Connection")
    print("="*80)
    
    analyzer = DeepSARAnalyzer()
    
    # Test con zona pequeña de Puerto Rico
    try:
        print("\n📡 Obteniendo escenas SAR...")
        
        result = await analyzer.analyze_sar_behavior(
            lat_min=19.85,
            lat_max=19.90,
            lon_min=-66.75,
            lon_max=-66.70
        )
        
        print(f"\n✅ Phase B: CONEXIÓN OK")
        print(f"   SAR Behavior Score: {result['behavior_score']:.3f}")
        print(f"   Rigidity Score: {result['multi_angle_geometry']['rigidity_score']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Phase B: CONEXIÓN FALLÓ")
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_icesat2_connection():
    """Test Phase C: ICESat-2 Analysis"""
    
    print("\n" + "="*80)
    print("🛰️ TEST: Phase C - ICESat-2 Connection")
    print("="*80)
    
    analyzer = ICESat2Analyzer()
    
    # Test con Puerto Rico
    try:
        print("\n📡 Buscando datos ICESat-2...")
        print("   ⚠️ Es normal no tener cobertura (limitación orbital)")
        
        result = await analyzer.analyze_vertical_microvariations(
            lat_min=19.85,
            lat_max=19.90,
            lon_min=-66.75,
            lon_max=-66.70
        )
        
        if result['status'] == 'success':
            print(f"\n✅ Phase C: DATOS ENCONTRADOS (raro pero bueno!)")
            print(f"   Rugosity: {result['surface_microvariations']['rugosity_m']:.2f}m")
            print(f"   Rigidity Score: {result['rigidity_indicators']['rigidity_score']:.2f}")
        elif result['status'] == 'no_coverage':
            print(f"\n✅ Phase C: CONEXIÓN OK (sin cobertura - normal)")
            print(f"   {result['interpretation']}")
        else:
            print(f"\n⚠️ Phase C: {result['status']}")
            print(f"   {result['interpretation']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Phase C: CONEXIÓN FALLÓ")
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """
    Ejecutar todos los tests de conexión
    """
    
    print("="*80)
    print("🔬 DEEP ANALYSIS - Connection Tests")
    print("="*80)
    print("\nVerificando conexiones a fuentes de datos reales...")
    
    results = {
        'phase_a_temporal': False,
        'phase_b_sar': False,
        'phase_c_icesat2': False
    }
    
    # Test Phase A
    results['phase_a_temporal'] = await test_temporal_connection()
    
    # Test Phase B
    results['phase_b_sar'] = await test_sar_connection()
    
    # Test Phase C
    results['phase_c_icesat2'] = await test_icesat2_connection()
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMEN DE TESTS")
    print("="*80)
    
    for phase, success in results.items():
        status = "✅ OK" if success else "❌ FALLÓ"
        print(f"{status} - {phase}")
    
    total_ok = sum(results.values())
    total = len(results)
    
    print(f"\nTotal: {total_ok}/{total} conexiones funcionando")
    
    if total_ok == total:
        print("\n🎉 Todas las conexiones funcionan correctamente!")
        print("   Puedes ejecutar: python run_deep_analysis_complete.py")
    elif total_ok > 0:
        print("\n⚠️ Algunas conexiones funcionan, otras requieren configuración")
        print("   Revisa los errores arriba para detalles")
    else:
        print("\n❌ Ninguna conexión funciona")
        print("   Verifica credenciales y dependencias")
    
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
