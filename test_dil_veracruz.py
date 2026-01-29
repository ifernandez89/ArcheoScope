#!/usr/bin/env python3
"""
Test SALTO 2: Deep Inference Layer (DIL)
========================================

Test rápido del sistema DIL en la zona de Veracruz Laguna.
"""

import asyncio
import sys
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from deep_inference_layer import DeepInferenceLayerEngine
from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2


async def test_dil_veracruz():
    """Test DIL en zona Veracruz Laguna."""
    
    print("="*80)
    print("🔬 TEST: Deep Inference Layer (DIL) - SALTO EVOLUTIVO 2")
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
    
    # Inicializar motor DIL
    print("🔧 Inicializando DeepInferenceLayerEngine...")
    dil_engine = DeepInferenceLayerEngine(integrator)
    print("   ✅ Motor DIL inicializado")
    print()
    
    # Calcular DIL
    print("🚀 Calculando Deep Inference Layer...")
    print()
    
    dil = await dil_engine.calculate_dil(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max
    )
    
    print()
    print("="*80)
    print("📊 RESULTADOS DIL")
    print("="*80)
    print()
    
    print(f"🎯 DIL Score: {dil.dil_score:.3f}")
    print(f"📏 Profundidad Estimada: {dil.estimated_depth_m:.1f}m")
    print(f"📊 Confianza: {dil.confidence:.3f} ({dil.confidence_level.value})")
    print(f"🏛️ Relevancia Arqueológica: {dil.archaeological_relevance:.3f}")
    print()
    
    print("📈 Componentes de Inferencia:")
    print(f"   📡 SAR Coherence Loss:    {dil.sar_coherence_loss:.3f}")
    print(f"   🌡️ Thermal Inertia:       {dil.thermal_inertia:.3f}")
    print(f"   💧 Subsurface Moisture:   {dil.subsurface_moisture:.3f}")
    print(f"   🗻 Topographic Anomaly:   {dil.topographic_anomaly:.3f}")
    print()
    
    print("📊 Metadatos:")
    print(f"   🔬 Sensores Usados:       {len(dil.sensors_used)}")
    print(f"   📡 Sensores:              {', '.join(dil.sensors_used)}")
    print(f"   🧠 Método de Inferencia:  {dil.inference_method}")
    print()
    
    print("📝 Interpretación:")
    print(f"   {dil.interpretation}")
    print()
    
    # Interpretación adicional
    print("="*80)
    print("🧠 ANÁLISIS")
    print("="*80)
    print()
    
    # Interpretación de profundidad
    if dil.estimated_depth_m < 2.0:
        print("✅ PROFUNDIDAD SUPERFICIAL (< 2m)")
        print("   → Estructuras arqueológicas superficiales")
        print("   → Alta accesibilidad para excavación")
    elif dil.estimated_depth_m < 5.0:
        print("🟡 PROFUNDIDAD MEDIA (2-5m)")
        print("   → Estructuras enterradas")
        print("   → Requiere excavación profunda")
    elif dil.estimated_depth_m < 10.0:
        print("🟠 PROFUNDIDAD PROFUNDA (5-10m)")
        print("   → Estructuras muy enterradas")
        print("   → Requiere excavación especializada")
    else:
        print("🔴 PROFUNDIDAD MUY PROFUNDA (> 10m)")
        print("   → Estructuras excepcionalmente profundas")
        print("   → Requiere métodos especiales")
    
    print()
    
    # Interpretación de confianza
    if dil.confidence > 0.6:
        print("✅ ALTA CONFIANZA EN INFERENCIA")
        print("   → Múltiples señales coherentes")
        print("   → Profundidad confiable")
    elif dil.confidence > 0.4:
        print("🟡 CONFIANZA MODERADA")
        print("   → Algunas señales coherentes")
        print("   → Profundidad indicativa")
    else:
        print("⚪ BAJA CONFIANZA")
        print("   → Señales débiles o contradictorias")
        print("   → Profundidad tentativa")
    
    print()
    
    # Relevancia arqueológica
    if dil.archaeological_relevance > 0.7:
        print("🏛️ ALTA RELEVANCIA ARQUEOLÓGICA")
        print("   → Profundidad óptima para estructuras")
        print("   → Alta prioridad de investigación")
    elif dil.archaeological_relevance > 0.4:
        print("🏛️ RELEVANCIA ARQUEOLÓGICA MODERADA")
        print("   → Profundidad aceptable")
        print("   → Investigación recomendada")
    else:
        print("🏛️ BAJA RELEVANCIA ARQUEOLÓGICA")
        print("   → Profundidad subóptima")
        print("   → Prioridad baja")
    
    print()
    
    # Detalles por componente
    if dil.sar_coherence_loss > 0.5:
        print("📡 SAR: Pérdida de coherencia significativa")
        print("   → Cambio subsuperficial detectado")
    
    if dil.thermal_inertia > 0.6:
        print("🌡️ TÉRMICO: Alta inercia térmica")
        print("   → Posible masa enterrada")
    
    if dil.subsurface_moisture > 0.4:
        print("💧 HUMEDAD: Humedad subsuperficial anómala")
        print("   → Drenaje alterado")
    
    if dil.topographic_anomaly > 0.3:
        print("🗻 TOPOGRAFÍA: Anomalía topográfica")
        print("   → Micro-relieve anómalo")
    
    print()
    print("="*80)
    print("✅ TEST COMPLETADO")
    print("="*80)
    print()
    
    # Exportar a JSON
    dil_dict = dil.to_dict()
    
    import json
    output_file = f"dil_veracruz_result_{center_lat:.4f}_{center_lon:.4f}.json"
    with open(output_file, 'w') as f:
        json.dump(dil_dict, f, indent=2)
    
    print(f"💾 Resultado guardado en: {output_file}")
    print()


if __name__ == "__main__":
    asyncio.run(test_dil_veracruz())
