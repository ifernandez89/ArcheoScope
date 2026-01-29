#!/usr/bin/env python3
"""
Test SALTO 1: Temporal Archaeological Signature (TAS)
=====================================================

Test rápido del sistema TAS en la zona de Veracruz Laguna.
"""

import asyncio
import sys
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from temporal_archaeological_signature import (
    TemporalArchaeologicalSignatureEngine,
    TemporalScale
)
from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2


async def test_tas_veracruz():
    """Test TAS en zona Veracruz Laguna."""
    
    print("="*80)
    print("🕐 TEST: Temporal Archaeological Signature (TAS) - SALTO EVOLUTIVO 1")
    print("="*80)
    print()
    
    # Coordenadas Veracruz Laguna
    lat_min = 20.49
    lat_max = 20.67
    lon_min = -97.01
    lon_max = -96.83
    
    center_lat = (lat_min + lat_max) / 2
    center_lon = (lon_min + lon_max) / 2
    
    print(f"📍 Zona de Test: Veracruz Laguna")
    print(f"   Centro: {center_lat:.4f}, {center_lon:.4f}")
    print(f"   Bbox: [{lat_min}, {lat_max}] x [{lon_min}, {lon_max}]")
    print()
    
    # Inicializar integrador
    print("🔧 Inicializando RealDataIntegratorV2...")
    integrator = RealDataIntegratorV2()
    print("   ✅ Integrador inicializado")
    print()
    
    # Inicializar motor TAS
    print("🔧 Inicializando TemporalArchaeologicalSignatureEngine...")
    tas_engine = TemporalArchaeologicalSignatureEngine(integrator)
    print("   ✅ Motor TAS inicializado")
    print()
    
    # Calcular TAS
    print("🚀 Calculando Temporal Archaeological Signature...")
    print()
    
    tas = await tas_engine.calculate_tas(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
        temporal_scale=TemporalScale.LONG
    )
    
    print()
    print("="*80)
    print("📊 RESULTADOS TAS")
    print("="*80)
    print()
    
    print(f"🎯 TAS Score: {tas.tas_score:.3f}")
    print()
    
    print("📈 Métricas Individuales:")
    print(f"   📈 NDVI Persistence:    {tas.ndvi_persistence:.3f}")
    print(f"   🌡️ Thermal Stability:   {tas.thermal_stability:.3f}")
    print(f"   📡 SAR Coherence:       {tas.sar_coherence:.3f}")
    print(f"   🌿 Stress Frequency:    {tas.stress_frequency:.3f}")
    print()
    
    print("📊 Metadatos:")
    print(f"   📅 Años Analizados:     {tas.years_analyzed}")
    print(f"   🔬 Sensores Usados:     {len(tas.sensors_used)}")
    print(f"   📡 Sensores:            {', '.join(tas.sensors_used)}")
    print(f"   📊 Escala Temporal:     {tas.temporal_scale.value}")
    print(f"   🎯 Confianza:           {tas.confidence:.3f}")
    print()
    
    print("📝 Interpretación:")
    print(f"   {tas.interpretation}")
    print()
    
    # Interpretación adicional
    print("="*80)
    print("🧠 ANÁLISIS")
    print("="*80)
    print()
    
    if tas.tas_score > 0.7:
        print("✅ FIRMA ARQUEOLÓGICA TEMPORAL FUERTE")
        print("   → Alta probabilidad de persistencia arqueológica")
    elif tas.tas_score > 0.5:
        print("🟡 FIRMA ARQUEOLÓGICA TEMPORAL MODERADA")
        print("   → Evidencia temporal significativa")
    elif tas.tas_score > 0.3:
        print("🟠 FIRMA ARQUEOLÓGICA TEMPORAL DÉBIL")
        print("   → Señal temporal presente pero débil")
    else:
        print("⚪ SIN FIRMA ARQUEOLÓGICA TEMPORAL")
        print("   → No se detecta persistencia temporal significativa")
    
    print()
    
    # Detalles por métrica
    if tas.ndvi_persistence > 0.6:
        print("📈 NDVI: Persistencia de anomalía detectada")
        print("   → Zona que siempre reacciona distinto")
    
    if tas.thermal_stability > 0.7:
        print("🌡️ TÉRMICO: Alta estabilidad térmica")
        print("   → Posible masa enterrada (inercia térmica)")
    
    if tas.sar_coherence < 0.5:
        print("📡 SAR: Baja coherencia temporal")
        print("   → Cambio subsuperficial detectado")
    
    if tas.stress_frequency > 0.4:
        print("🌿 ESTRÉS: Alta frecuencia de estrés vegetal")
        print("   → Posible uso humano prolongado")
    
    print()
    print("="*80)
    print("✅ TEST COMPLETADO")
    print("="*80)
    print()
    
    # Exportar a JSON
    tas_dict = tas.to_dict()
    
    import json
    output_file = f"tas_veracruz_result_{center_lat:.4f}_{center_lon:.4f}.json"
    with open(output_file, 'w') as f:
        json.dump(tas_dict, f, indent=2)
    
    print(f"💾 Resultado guardado en: {output_file}")
    print()


if __name__ == "__main__":
    asyncio.run(test_tas_veracruz())
