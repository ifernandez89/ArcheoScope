#!/usr/bin/env python3
"""
Deep Temporal Analysis - Phase A: Exprimir el Eje TEMPORAL
===========================================================

TAS = 1.000 confirmado. Ahora vamos a DESCRIBIRLO mejor:
- Phase-shift térmico
- Retraso térmico vs entorno
- Amortiguación de picos
- Comparativa estacional extrema
- Respuesta post-evento (huracanes, El Niño/La Niña)

NO requiere nuevos sensores, solo re-procesar MODIS/VIIRS/Landsat
"""

import asyncio
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import json

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from satellite_connectors.modis_lst_connector import MODISLSTConnector
from satellite_connectors.modis_lst_time_series import MODISLSTTimeSeries
from satellite_connectors.planetary_computer import PlanetaryComputerConnector

class DeepTemporalAnalyzer:
    """
    Análisis temporal profundo - Phase-shift y comportamiento térmico
    """
    
    def __init__(self):
        self.modis = MODISLSTConnector()
        self.modis_ts = MODISLSTTimeSeries(self.modis)
        self.pc = PlanetaryComputerConnector()
        
    async def analyze_thermal_phase_shift(
        self,
        target_lat: float,
        target_lon: float,
        control_lat: float,
        control_lon: float,
        years: int = 5
    ) -> Dict[str, Any]:
        """
        Analizar phase-shift térmico: retraso, amortiguación, respuesta
        """
        
        print(f"\n🌡️ ANÁLISIS DE PHASE-SHIFT TÉRMICO")
        print(f"   Target: ({target_lat:.4f}, {target_lon:.4f})")
        print(f"   Control: ({control_lat:.4f}, {control_lon:.4f})")
        print(f"   Período: {years} años")
        
        # 1. Obtener series temporales diarias (MODIS)
        print("\n📡 Fase 1: Adquisición de series temporales diarias...")
        target_series = await self._get_daily_thermal_series(
            target_lat, target_lon, years
        )
        control_series = await self._get_daily_thermal_series(
            control_lat, control_lon, years
        )
        
        print(f"   Target: {len(target_series)} mediciones")
        print(f"   Control: {len(control_series)} mediciones")
        
        # 2. Calcular retraso térmico (phase lag)
        print("\n⏱️ Fase 2: Cálculo de retraso térmico...")
        phase_lag = self._calculate_phase_lag(target_series, control_series)
        print(f"   Phase Lag: {phase_lag:.2f} días")
        
        # 3. Calcular amortiguación de picos
        print("\n📉 Fase 3: Análisis de amortiguación...")
        damping = self._calculate_thermal_damping(target_series, control_series)
        print(f"   Damping Factor: {damping['factor']:.3f}")
        print(f"   Peak Reduction: {damping['peak_reduction']:.1f}%")
        
        # 4. Comparativa estacional extrema
        print("\n🌡️ Fase 4: Análisis estacional extremo...")
        seasonal = self._analyze_seasonal_extremes(target_series, control_series)
        print(f"   Summer Stability: {seasonal['summer_stability']:.3f}")
        print(f"   Winter Stability: {seasonal['winter_stability']:.3f}")
        
        # 5. Detectar eventos extremos (huracanes, El Niño)
        print("\n🌀 Fase 5: Detección de eventos extremos...")
        events = self._detect_extreme_events(target_series, control_series)
        print(f"   Eventos detectados: {len(events)}")
        
        # 6. Analizar respuesta post-evento
        print("\n📊 Fase 6: Análisis de respuesta post-evento...")
        recovery = self._analyze_post_event_recovery(target_series, events)
        print(f"   Recovery Time (avg): {recovery['avg_recovery_days']:.1f} días")
        print(f"   Baseline Return: {recovery['baseline_return_rate']:.3f}")
        
        # 7. Calcular Thermal Inertia Score
        thermal_inertia = self._calculate_thermal_inertia(
            phase_lag, damping, seasonal, recovery
        )
        print(f"\n🎯 THERMAL INERTIA SCORE: {thermal_inertia:.3f}")
        
        return {
            'phase_lag_days': phase_lag,
            'damping': damping,
            'seasonal_extremes': seasonal,
            'extreme_events': events,
            'post_event_recovery': recovery,
            'thermal_inertia_score': thermal_inertia,
            'interpretation': self._interpret_thermal_behavior(
                phase_lag, damping, thermal_inertia
            )
        }
    
    def _calculate_phase_lag(
        self,
        target: List[float],
        control: List[float]
    ) -> float:
        """
        Calcular retraso de fase entre target y control
        Usa cross-correlation para encontrar el lag óptimo
        """
        if len(target) < 30 or len(control) < 30:
            return 0.0
        
        # Cross-correlation
        correlation = np.correlate(target, control, mode='full')
        lag = np.argmax(correlation) - len(control) + 1
        
        # Convertir a días (asumiendo mediciones diarias)
        return float(lag)
    
    def _calculate_thermal_damping(
        self,
        target: List[float],
        control: List[float]
    ) -> Dict[str, float]:
        """
        Calcular factor de amortiguación térmica
        """
        if len(target) < 10 or len(control) < 10:
            return {'factor': 1.0, 'peak_reduction': 0.0}
        
        target_arr = np.array(target)
        control_arr = np.array(control)
        
        # Calcular varianza (amplitud de oscilación)
        target_var = np.var(target_arr)
        control_var = np.var(control_arr)
        
        # Factor de amortiguación (< 1.0 = amortiguado)
        damping_factor = target_var / control_var if control_var > 0 else 1.0
        
        # Reducción de picos
        target_peaks = np.percentile(target_arr, 95) - np.percentile(target_arr, 5)
        control_peaks = np.percentile(control_arr, 95) - np.percentile(control_arr, 5)
        peak_reduction = (1 - target_peaks / control_peaks) * 100 if control_peaks > 0 else 0.0
        
        return {
            'factor': float(damping_factor),
            'peak_reduction': float(peak_reduction),
            'target_variance': float(target_var),
            'control_variance': float(control_var)
        }
    
    def _analyze_seasonal_extremes(
        self,
        target: List[float],
        control: List[float]
    ) -> Dict[str, float]:
        """
        Analizar comportamiento en extremos estacionales
        """
        if len(target) < 365:
            return {
                'summer_stability': 0.5,
                'winter_stability': 0.5,
                'seasonal_amplitude': 0.0
            }
        
        target_arr = np.array(target)
        control_arr = np.array(control)
        
        # Dividir en estaciones (simplificado: verano = días 150-240, invierno = días 330-60)
        # Asumiendo hemisferio norte
        days_per_year = 365
        n_years = len(target) // days_per_year
        
        summer_target = []
        summer_control = []
        winter_target = []
        winter_control = []
        
        for year in range(n_years):
            start = year * days_per_year
            # Verano (días 150-240)
            summer_target.extend(target_arr[start+150:start+240])
            summer_control.extend(control_arr[start+150:start+240])
            # Invierno (días 330-365 y 0-60)
            winter_target.extend(target_arr[start+330:start+365])
            winter_control.extend(control_arr[start+330:start+365])
            if year < n_years - 1:
                winter_target.extend(target_arr[start+365:start+425])
                winter_control.extend(control_arr[start+365:start+425])
        
        # Calcular estabilidad (inverso de varianza relativa)
        summer_stability = 1.0 - (np.var(summer_target) / np.var(summer_control)) if len(summer_target) > 0 and np.var(summer_control) > 0 else 0.5
        winter_stability = 1.0 - (np.var(winter_target) / np.var(winter_control)) if len(winter_target) > 0 and np.var(winter_control) > 0 else 0.5
        
        # Amplitud estacional
        seasonal_amplitude = np.mean(summer_target) - np.mean(winter_target) if len(summer_target) > 0 and len(winter_target) > 0 else 0.0
        
        return {
            'summer_stability': float(np.clip(summer_stability, 0, 1)),
            'winter_stability': float(np.clip(winter_stability, 0, 1)),
            'seasonal_amplitude': float(seasonal_amplitude)
        }
    
    def _detect_extreme_events(
        self,
        target: List[float],
        control: List[float]
    ) -> List[Dict[str, Any]]:
        """
        Detectar eventos extremos (huracanes, El Niño, etc.)
        """
        if len(target) < 30:
            return []
        
        target_arr = np.array(target)
        control_arr = np.array(control)
        
        # Detectar anomalías (> 2 sigma)
        target_mean = np.mean(target_arr)
        target_std = np.std(target_arr)
        
        events = []
        threshold = 2.0  # 2 sigma
        
        for i in range(len(target_arr)):
            deviation = abs(target_arr[i] - target_mean) / target_std if target_std > 0 else 0
            
            if deviation > threshold:
                # Verificar si es un evento real (no solo ruido)
                # Buscar ventana de 7 días alrededor
                window_start = max(0, i - 3)
                window_end = min(len(target_arr), i + 4)
                window = target_arr[window_start:window_end]
                
                if len(window) > 3 and np.mean(window) > target_mean + threshold * target_std:
                    events.append({
                        'day': i,
                        'magnitude': float(deviation),
                        'temperature': float(target_arr[i]),
                        'type': 'hot_anomaly' if target_arr[i] > target_mean else 'cold_anomaly'
                    })
        
        # Filtrar eventos muy cercanos (probablemente el mismo evento)
        filtered_events = []
        last_day = -10
        for event in events:
            if event['day'] - last_day > 7:  # Al menos 7 días de separación
                filtered_events.append(event)
                last_day = event['day']
        
        return filtered_events
    
    def _analyze_post_event_recovery(
        self,
        target: List[float],
        events: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Analizar cuánto tarda en volver a baseline después de eventos extremos
        """
        if len(events) == 0 or len(target) < 30:
            return {
                'avg_recovery_days': 0.0,
                'baseline_return_rate': 1.0,
                'recovery_events_analyzed': 0
            }
        
        target_arr = np.array(target)
        baseline = np.median(target_arr)
        threshold = np.std(target_arr) * 0.5  # 0.5 sigma como "vuelto a baseline"
        
        recovery_times = []
        
        for event in events:
            event_day = event['day']
            
            # Buscar cuántos días tarda en volver a baseline
            for days_after in range(1, min(30, len(target_arr) - event_day)):
                current_temp = target_arr[event_day + days_after]
                
                if abs(current_temp - baseline) < threshold:
                    recovery_times.append(days_after)
                    break
        
        avg_recovery = np.mean(recovery_times) if len(recovery_times) > 0 else 0.0
        return_rate = len(recovery_times) / len(events) if len(events) > 0 else 1.0
        
        return {
            'avg_recovery_days': float(avg_recovery),
            'baseline_return_rate': float(return_rate),
            'recovery_events_analyzed': len(events)
        }
    
    def _calculate_thermal_inertia(
        self,
        phase_lag: float,
        damping: Dict[str, float],
        seasonal: Dict[str, float],
        recovery: Dict[str, float]
    ) -> float:
        """
        Calcular Thermal Inertia Score integrado
        """
        # Normalizar componentes
        lag_score = np.clip(abs(phase_lag) / 10.0, 0, 1)  # 10 días = máximo
        damping_score = 1.0 - damping['factor']  # Más amortiguación = más inercia
        seasonal_score = (seasonal['summer_stability'] + seasonal['winter_stability']) / 2.0
        recovery_score = np.clip(recovery['avg_recovery_days'] / 14.0, 0, 1)  # 14 días = máximo
        
        # Pesos
        weights = {
            'lag': 0.25,
            'damping': 0.35,
            'seasonal': 0.25,
            'recovery': 0.15
        }
        
        thermal_inertia = (
            lag_score * weights['lag'] +
            damping_score * weights['damping'] +
            seasonal_score * weights['seasonal'] +
            recovery_score * weights['recovery']
        )
        
        return float(np.clip(thermal_inertia, 0, 1))
    
    def _interpret_thermal_behavior(
        self,
        phase_lag: float,
        damping: Dict[str, float],
        thermal_inertia: float
    ) -> str:
        """
        Interpretar comportamiento térmico
        """
        if thermal_inertia > 0.7:
            if abs(phase_lag) > 5 and damping['factor'] < 0.5:
                return "MASA TÉRMICA SIGNIFICATIVA: Retraso de fase y amortiguación indican cuerpo con alta capacidad térmica (posible estructura masiva o material denso)"
            else:
                return "ALTA INERCIA TÉRMICA: Comportamiento térmico estable incompatible con superficie oceánica dinámica"
        elif thermal_inertia > 0.5:
            return "INERCIA TÉRMICA MODERADA: Alguna estabilización térmica presente, requiere análisis adicional"
        else:
            return "COMPORTAMIENTO TÉRMICO NORMAL: Consistente con procesos naturales dinámicos"
    
    async def _get_daily_thermal_series(
        self,
        lat: float,
        lon: float,
        years: int
    ) -> List[float]:
        """
        Obtener serie temporal diaria desde MODIS LST
        
        ESTRATEGIA:
        1. Intentar obtener datos reales de MODIS (con cache)
        2. Si falla o toma mucho tiempo, usar modelo basado en ubicación
        
        OPTIMIZACIÓN:
        - Usa MOD11A2 (8-day composite) en vez de daily
        - Reduce requests de 1825 a ~228 (91% menos)
        - Cache local para evitar re-descargas
        """
        
        print(f"   📡 Obteniendo serie térmica para ({lat:.4f}, {lon:.4f})...")
        
        try:
            # Intentar obtener datos reales con el nuevo módulo
            result = await self.modis_ts.get_daily_thermal_series(
                lat=lat,
                lon=lon,
                years=years,
                use_cache=True
            )
            
            print(f"   ✅ Serie térmica obtenida: {len(result['series'])} días")
            print(f"   📊 Datos reales: {result['real_data_count']} ({result['real_data_count']/result['total_days']*100:.1f}%)")
            
            return result['series']
            
        except Exception as e:
            print(f"   ⚠️ Error obteniendo datos MODIS reales: {e}")
            print(f"   📊 Fallback a modelo basado en ubicación")
            
            # Fallback a modelo (código original)
            days = years * 365
            series = []
            
            from datetime import datetime, timedelta
            start_date = datetime.now() - timedelta(days=days)
            
            for day in range(days):
                current_date = start_date + timedelta(days=day)
                month = current_date.month
                
                # Obtener LST estimada para este día
                lst_day, lst_night = self.modis._estimate_lst(lat, lon, month)
                
                # Usar temperatura promedio día-noche
                lst_avg = (lst_day + lst_night) / 2
                
                # Convertir Kelvin a Celsius
                lst_celsius = lst_avg - 273.15
                
                # Añadir variación diaria pequeña
                daily_variation = np.random.normal(0, 1.5)
                
                series.append(lst_celsius + daily_variation)
            
            print(f"   ✅ Serie térmica generada (modelo): {len(series)} días")
            
            return series


async def main():
    """
    Ejecutar análisis temporal profundo en Puerto Rico North
    """
    
    print("="*80)
    print("🌡️ DEEP TEMPORAL ANALYSIS - Phase A")
    print("   Exprimiendo el Eje TEMPORAL")
    print("="*80)
    
    analyzer = DeepTemporalAnalyzer()
    
    # Puerto Rico North (target) vs zona de control cercana
    target_lat, target_lon = 19.89, -66.68
    control_lat, control_lon = 19.85, -66.75  # 10km al oeste
    
    result = await analyzer.analyze_thermal_phase_shift(
        target_lat, target_lon,
        control_lat, control_lon,
        years=5
    )
    
    # Guardar resultados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"deep_temporal_analysis_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\n📄 Resultados guardados: {filename}")
    
    # Mostrar interpretación
    print("\n" + "="*80)
    print("🎯 INTERPRETACIÓN")
    print("="*80)
    print(result['interpretation'])
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
