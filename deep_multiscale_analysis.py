#!/usr/bin/env python3
"""
Deep Multi-Scale Analysis - Phase C & D
========================================

Phase C: ICESat-2 micro-ajustes verticales
- Micro-variaciones del nivel superficial
- Correlación con mareas/presión
- Rigidez subyacente (el agua reacciona distinto)

Phase D: Análisis MULTI-ESCALA (CLAVE)
- Repetir TODAS las métricas en: 50m, 100m, 250m, 500m
- Buscar puntos donde la coherencia NO decae
- Las formaciones naturales pierden coherencia al bajar escala
- Las masas integradas NO tanto

100% con lo que ya tenemos
"""

import asyncio
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple
import json

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from territorial_inferential_tomography import TerritorialInferentialTomographyEngine
from territorial_context_profile import AnalysisObjective
from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2

class MultiScaleAnalyzer:
    """
    Análisis multi-escala: coherencia a través de resoluciones
    """
    
    def __init__(self):
        self.integrator = RealDataIntegratorV2()
        self.engine = TerritorialInferentialTomographyEngine(self.integrator)
        
        # Escalas a analizar
        self.scales = [50, 100, 250, 500]  # metros
    
    async def analyze_scale_invariance(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        zone_name: str
    ) -> Dict[str, Any]:
        """
        Analizar invariancia de escala - CLAVE para distinguir natural vs artificial
        """
        
        print(f"\n📏 ANÁLISIS MULTI-ESCALA")
        print(f"   Zona: {zone_name}")
        print(f"   Región: [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
        print(f"   Escalas: {self.scales} metros")
        
        results_by_scale = {}
        
        for scale in self.scales:
            print(f"\n🔍 Analizando escala {scale}m...")
            
            try:
                result = await asyncio.wait_for(
                    self.engine.analyze_territory(
                        lat_min=lat_min,
                        lat_max=lat_max,
                        lon_min=lon_min,
                        lon_max=lon_max,
                        analysis_objective=AnalysisObjective.VALIDATION,
                        resolution_m=float(scale)
                    ),
                    timeout=300.0  # 5 minutos por escala
                )
                
                # Extraer métricas clave
                metrics = {
                    'resolution_m': scale,
                    'coherence_3d': result.tomographic_profile.coherencia_3d if result.tomographic_profile else 0.0,
                    'ess_superficial': result.tomographic_profile.ess_superficial if result.tomographic_profile else 0.0,
                    'ess_volumetrico': result.tomographic_profile.ess_volumetrico if result.tomographic_profile else 0.0,
                    'tas_score': result.tomographic_profile.tas_signature.tas_score if result.tomographic_profile and result.tomographic_profile.tas_signature else 0.0,
                    'territorial_coherence': result.territorial_coherence_score,
                    'scientific_rigor': result.scientific_rigor_score
                }
                
                results_by_scale[scale] = metrics
                
                print(f"   ✅ Coherencia 3D: {metrics['coherence_3d']:.3f}")
                print(f"   ✅ TAS Score: {metrics['tas_score']:.3f}")
                print(f"   ✅ G1 (Territorial): {metrics['territorial_coherence']:.3f}")
                
            except asyncio.TimeoutError:
                print(f"   ⏱️ Timeout en escala {scale}m")
                results_by_scale[scale] = None
            except Exception as e:
                print(f"   ❌ Error en escala {scale}m: {e}")
                results_by_scale[scale] = None
        
        # Analizar invariancia
        print("\n📊 Analizando invariancia de escala...")
        invariance = self._analyze_scale_invariance(results_by_scale)
        
        print(f"\n🎯 SCALE INVARIANCE SCORE: {invariance['invariance_score']:.3f}")
        print(f"   Coherence Decay Rate: {invariance['coherence_decay_rate']:.4f}")
        print(f"   TAS Stability: {invariance['tas_stability']:.3f}")
        
        return {
            'zone_name': zone_name,
            'scales_analyzed': self.scales,
            'results_by_scale': results_by_scale,
            'scale_invariance': invariance,
            'interpretation': self._interpret_scale_behavior(invariance)
        }
    
    def _analyze_scale_invariance(
        self,
        results: Dict[int, Dict]
    ) -> Dict[str, float]:
        """
        Analizar cómo cambian las métricas con la escala
        """
        # Filtrar resultados válidos
        valid_results = {k: v for k, v in results.items() if v is not None}
        
        if len(valid_results) < 2:
            return {
                'invariance_score': 0.0,
                'coherence_decay_rate': 1.0,
                'tas_stability': 0.0,
                'g1_stability': 0.0
            }
        
        scales = sorted(valid_results.keys())
        
        # Extraer series
        coherence_series = [valid_results[s]['coherence_3d'] for s in scales]
        tas_series = [valid_results[s]['tas_score'] for s in scales]
        g1_series = [valid_results[s]['territorial_coherence'] for s in scales]
        
        # Calcular tasa de decaimiento de coherencia
        # Natural: decae rápido con escala
        # Artificial: decae lento o no decae
        if len(coherence_series) > 1:
            # Ajustar modelo lineal: y = mx + b
            x = np.array(scales)
            y = np.array(coherence_series)
            
            # Pendiente (negativa = decae)
            slope = np.polyfit(x, y, 1)[0] if len(x) > 1 else 0.0
            
            # Normalizar: 0 = no decae, 1 = decae mucho
            decay_rate = abs(slope) * 1000  # Escalar para que sea interpretable
            decay_rate = np.clip(decay_rate, 0, 1)
        else:
            decay_rate = 0.5
        
        # Estabilidad de TAS (debe mantenerse en 1.0)
        tas_stability = 1.0 - np.std(tas_series) if len(tas_series) > 0 else 0.0
        
        # Estabilidad de G1
        g1_stability = 1.0 - np.std(g1_series) if len(g1_series) > 0 else 0.0
        
        # Score de invariancia (alto = no decae = sospechoso)
        invariance_score = (
            (1.0 - decay_rate) * 0.5 +  # Baja tasa de decaimiento
            tas_stability * 0.3 +
            g1_stability * 0.2
        )
        
        return {
            'invariance_score': float(np.clip(invariance_score, 0, 1)),
            'coherence_decay_rate': float(decay_rate),
            'tas_stability': float(np.clip(tas_stability, 0, 1)),
            'g1_stability': float(np.clip(g1_stability, 0, 1)),
            'coherence_at_50m': coherence_series[0] if len(coherence_series) > 0 else 0.0,
            'coherence_at_500m': coherence_series[-1] if len(coherence_series) > 0 else 0.0
        }
    
    def _interpret_scale_behavior(
        self,
        invariance: Dict[str, float]
    ) -> str:
        """
        Interpretar comportamiento multi-escala
        """
        score = invariance['invariance_score']
        decay = invariance['coherence_decay_rate']
        
        if score > 0.7 and decay < 0.3:
            return "INVARIANCIA DE ESCALA ANÓMALA: La coherencia NO decae significativamente con la escala. Esto es ALTAMENTE INUSUAL en formaciones naturales, que típicamente pierden coherencia al reducir resolución. Sugiere estructura integrada con organización multi-escala."
        elif score > 0.5:
            return "INVARIANCIA MODERADA: Alguna persistencia de coherencia a través de escalas. Requiere análisis adicional para determinar si es natural o artificial."
        else:
            return "DECAIMIENTO NORMAL: La coherencia decae con la escala como se espera en formaciones naturales."


class ICESat2Analyzer:
    """
    Análisis ICESat-2: micro-ajustes verticales
    """
    
    def __init__(self):
        from satellite_connectors.icesat2_connector import ICESat2Connector
        self.icesat2 = ICESat2Connector()
    
    async def analyze_vertical_microvariations(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Dict[str, Any]:
        """
        Analizar micro-variaciones verticales con ICESat-2
        
        ESTRATEGIA:
        1. Usar ICESat2Connector para obtener datos de elevación
        2. Analizar rugosidad superficial
        3. Detectar anomalías de rigidez (agua vs superficie sólida)
        """
        
        print(f"\n🛰️ ANÁLISIS ICESat-2 - Micro-ajustes Verticales")
        print(f"   Región: [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
        
        try:
            # Obtener datos de elevación
            print("\n📡 Fase 1: Adquisición de datos ICESat-2...")
            
            elevation_data = await self.icesat2.get_elevation_data(
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                product="ATL06"  # Land Ice Height
            )
            
            # Verificar si hay datos
            if not elevation_data or elevation_data.status != 'success':
                print(f"   ⚠️ ICESat-2: {elevation_data.status if elevation_data else 'no data'}")
                print(f"   💡 Esto es NORMAL - ICESat-2 tiene cobertura orbital limitada")
                
                return {
                    'status': 'no_coverage',
                    'surface_microvariations': {
                        'std_deviation_cm': 0.0,
                        'tidal_correlation': 0.0,
                        'pressure_correlation': 0.0
                    },
                    'rigidity_indicators': {
                        'water_response_anomaly': False,
                        'vertical_stability': 0.0
                    },
                    'interpretation': f"ICESat-2 no coverage in region - {elevation_data.reason if elevation_data else 'orbital limitations'}"
                }
            
            # Extraer métricas de rugosidad
            metadata = elevation_data.metadata
            rugosity = metadata.get('rugosity', 0.0)
            elevation_std = metadata.get('elevation_std', 0.0)
            elevation_gradient = metadata.get('elevation_gradient', 0.0)
            valid_points = metadata.get('valid_points', 0)
            
            print(f"   ✅ ICESat-2 datos obtenidos")
            print(f"   📊 Puntos válidos: {valid_points}")
            print(f"   📊 Rugosidad: {rugosity:.2f}m")
            print(f"   📊 Gradiente: {elevation_gradient:.2f}m")
            
            # Analizar rigidez subyacente
            print("\n🔍 Fase 2: Análisis de rigidez...")
            
            # Rugosidad alta = superficie irregular = posible estructura rígida
            # Rugosidad baja = superficie plana = agua o hielo
            
            if rugosity > 5.0:
                rigidity_score = 0.8
                water_anomaly = True
                interpretation = "ANOMALÍA DE RIGIDEZ DETECTADA: Rugosidad superficial alta incompatible con superficie oceánica dinámica. Sugiere estructura rígida subyacente."
            elif rugosity > 2.0:
                rigidity_score = 0.5
                water_anomaly = False
                interpretation = "Rugosidad moderada - Requiere análisis adicional para determinar origen"
            else:
                rigidity_score = 0.2
                water_anomaly = False
                interpretation = "Rugosidad baja - Consistente con superficie oceánica o hielo plano"
            
            print(f"   🎯 Rigidity Score: {rigidity_score:.2f}")
            print(f"   🎯 Water Anomaly: {water_anomaly}")
            
            # Convertir rugosidad a cm para reporte
            std_deviation_cm = elevation_std * 100
            
            return {
                'status': 'success',
                'surface_microvariations': {
                    'std_deviation_cm': float(std_deviation_cm),
                    'rugosity_m': float(rugosity),
                    'elevation_gradient_m': float(elevation_gradient),
                    'valid_points': int(valid_points),
                    'tidal_correlation': 0.0,  # Requiere análisis temporal
                    'pressure_correlation': 0.0  # Requiere análisis temporal
                },
                'rigidity_indicators': {
                    'water_response_anomaly': bool(water_anomaly),
                    'vertical_stability': float(rigidity_score),
                    'rigidity_score': float(rigidity_score)
                },
                'interpretation': interpretation,
                'confidence': float(elevation_data.confidence)
            }
            
        except Exception as e:
            print(f"   ❌ Error en análisis ICESat-2: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                'status': 'error',
                'surface_microvariations': {
                    'std_deviation_cm': 0.0,
                    'tidal_correlation': 0.0,
                    'pressure_correlation': 0.0
                },
                'rigidity_indicators': {
                    'water_response_anomaly': False,
                    'vertical_stability': 0.0
                },
                'interpretation': f"ICESat-2 analysis error: {str(e)}"
            }


async def main():
    """
    Ejecutar análisis multi-escala completo
    """
    
    print("="*80)
    print("📏 DEEP MULTI-SCALE ANALYSIS - Phase C & D")
    print("   Invariancia de Escala + ICESat-2")
    print("="*80)
    
    # Phase D: Multi-escala
    print("\n" + "="*80)
    print("PHASE D: ANÁLISIS MULTI-ESCALA")
    print("="*80)
    
    multiscale = MultiScaleAnalyzer()
    
    # Puerto Rico North
    result_multiscale = await multiscale.analyze_scale_invariance(
        lat_min=19.80,
        lat_max=19.98,
        lon_min=-66.80,
        lon_max=-66.56,
        zone_name="Puerto Rico North Continental Slope"
    )
    
    # Guardar resultados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"deep_multiscale_analysis_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(result_multiscale, f, indent=2, default=str)
    
    print(f"\n📄 Resultados guardados: {filename}")
    
    # Mostrar interpretación
    print("\n" + "="*80)
    print("🎯 INTERPRETACIÓN MULTI-ESCALA")
    print("="*80)
    print(result_multiscale['interpretation'])
    print("="*80)
    
    # Phase C: ICESat-2
    print("\n" + "="*80)
    print("PHASE C: ANÁLISIS ICESat-2")
    print("="*80)
    
    icesat2 = ICESat2Analyzer()
    
    result_icesat2 = await icesat2.analyze_vertical_microvariations(
        lat_min=19.80,
        lat_max=19.98,
        lon_min=-66.80,
        lon_max=-66.56
    )
    
    print(f"\n📄 ICESat-2: {result_icesat2['interpretation']}")


if __name__ == "__main__":
    asyncio.run(main())
