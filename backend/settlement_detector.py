#!/usr/bin/env python3
"""
ArcheoScope - Settlement Detection System
==========================================
Detección de "Proto-ciudades", asentamientos y ruido arquitectónico.
NO busca geoglifos (formas limpias), busca HABITACIÓN (caos organizado).
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from enum import Enum
import random

# Reutilizamos contextos físicos ya validados
# (Importamos lógica, no modificamos la clase original)
from backend.geoglyph_detector import PaleohydrologyContext

class SettlementMode(Enum):
    SETTLEMENT_PROBABILITY = "settlement_probability" # Densidad, micro-anomalías
    PALEO_HYDRO_SETTLEMENT = "paleo_hydro_settlement" # Bordes de cuencas, confluencias
    ARCHITECTURAL_NOISE = "architectural_noise"       # Ángulos humanos, muros colapsados

@dataclass
class ArchitecturalSignature:
    """Firma de ruido arquitectónico humano"""
    density_index: float           # 0-1: Densidad de micro-estructuras
    entropy_score: float           # 0-1: Caos (Alto es bueno para asentamientos)
    orthogonality_ratio: float     # 0-1: Presencia de ángulos rectos/humanos
    linear_fragment_count: int     # Cantidad de alineaciones cortas (<5m)
    clustering_coefficient: float  # Qué tan agrupados están los elementos

@dataclass
class SettlementResult:
    candidate_id: str
    lat: float
    lon: float
    mode: SettlementMode
    probability_score: float       # Probabilidad de ser asentamiento
    architectural_noise: float     # Nivel de "ruido humano"
    hydro_context_score: float     # Calidad del emplazamiento hídrico
    is_proto_urban: bool           # ¿Cumple criterios de complejidad?
    interpretation: str

class SettlementDetector:
    """
    Detector especializado en patrones de asentamiento y ruido antrópico.
    Filosofía: Buscar "Clusters Feos" y "Ruido Ordenado".
    """
    
    def __init__(self, mode: SettlementMode = SettlementMode.SETTLEMENT_PROBABILITY, region: str = "RUB_AL_KHALI"):
        self.mode = mode
        self.region = region
        print(f"🏘️ SettlementDetector inicializado | Modo: {mode.value.upper()} | Región: {region}")

    def _get_simulation_data(self):
        """Retorna hotspots hidro/ruido según la región activa"""
        if self.region == "GIZA":
            # ... (Lógica de Giza seleccionada)
            hotspots = [(29.95, 30.95), (29.40, 30.70), (29.60, 31.35)]
            hydro_sources = [(29.95, 31.15), (29.45, 30.60), (30.40, 30.50), (29.95, 30.95), (29.40, 30.70), (29.60, 31.35)]
            physics = {'hydro_decay': 12, 'noise_decay': 25}
        elif self.region == "ATACAMA":
            # ... (Lógica Atacama seleccionada)
            hotspots = [(-23.00, -68.00), (-22.90, -68.20), (-23.15, -67.85)]
            hydro_sources = [(-22.91, -68.20), (-23.05, -67.95), (-23.30, -68.10)]
            physics = {'hydro_decay': 20, 'noise_decay': 30}
        elif self.region == "TAKLAMAKAN":
            # TAKLAMAKAN DESERT (Silk Road / Tarim Basin)
            hotspots = [
                (40.50, 82.00), # Target Principal (Kucha Hinterland)
                (40.35, 82.25), # Silk Road Outpost
                (40.65, 81.80)  # Abandoned Irrigation Hub
            ]
            hydro_sources = [
                (40.55, 81.95), # Ancient Tarim River Branch
                (40.40, 82.10), # Oasis system
                (40.70, 81.70)  # Karez (subsurface canals) trace
            ]
            # Física: Desierto de arena (SAR penetra dunas). Menos ortogonalidad (barro).
            physics = {'hydro_decay': 15, 'noise_decay': 22}
        else: # RUB_AL_KHALI (Default)
            hotspots = [
                (20.50, 51.00), # RAK-STL-01
                (20.62, 51.38), # SITE A
                (20.18, 50.92), # SITE B
                (20.48, 50.55)  # SITE C
            ]
            hydro_sources = [
                (20.52, 51.02), (20.64, 51.40), 
                (20.15, 50.90), (20.50, 50.52)
            ]
            physics = {'hydro_decay': 8, 'noise_decay': 20}
            
        return hotspots, hydro_sources, physics

    def analyze_architectural_noise(self, lat: float, lon: float) -> ArchitecturalSignature:
        """
        Simula el análisis de ruido arquitectónico (muros, cimientos).
        """
        hotspots, _, physics = self._get_simulation_data()
        
        # Calcular distancia al hotspot más cercano
        min_dist = min([np.sqrt((lat - hlat)**2 + (lon - hlon)**2) for hlat, hlon in hotspots])
        
        base_density = max(0.0, 1.0 - min_dist * physics['noise_decay']) 
        if base_density < 0.1: base_density = 0.05
        
        # Variabilidad realista
        density = base_density * random.uniform(0.6, 1.0)
        
        # Asentamientos = Alta entropía local + Ángulos rectos ocultos
        orthogonality = random.uniform(0.1, 0.4) # Natural es bajo
        if density > 0.6: 
            # En EGIPTO la ortogonalidad es mayor (arquitectura faraónica/civil más rígida)
            boost = 0.5 if self.region == "GIZA" else 0.3
            orthogonality += random.uniform(0.2, boost)
            
        return ArchitecturalSignature(
            density_index=density,
            entropy_score=random.uniform(0.5, 0.9), 
            orthogonality_ratio=orthogonality,
            linear_fragment_count=int(density * 50),
            clustering_coefficient=random.uniform(0.7, 0.95)
        )

    def analyze_hydro_strategic(self, lat: float, lon: float) -> float:
        """
        Analiza valor estratégico del agua.
        """
        _, hydro_sources, physics = self._get_simulation_data()
        
        # Distancia a fuente hídrica más cercana
        min_dist = min([np.sqrt((lat - flat)**2 + (lon - flon)**2) for flat, flon in hydro_sources])
        
        if min_dist < 0.02: 
            # En GIZA/ATACAMA, estar en la fuente es crítico
            if self.region == "ATACAMA":
                return 0.98 if min_dist < 0.01 else 0.4 # Oasis binario
            if self.region == "TAKLAMAKAN":
                return 0.75 # Río activo (inundable en primavera)
            return 0.90 if self.region == "GIZA" else 0.2 
            
        if 0.02 <= min_dist <= 0.12: 
            # Borde ideal amplio para Taklamakan (zona de irrigación)
            return 0.98 if self.region == "TAKLAMAKAN" else 0.95
            
        return max(0.05, 1.0 - min_dist * physics['hydro_decay'])

    def detect_settlement(self, lat: float, lon: float) -> SettlementResult:
        
        # 1. Análisis de Ruido Arquitectónico
        arch_sig = self.analyze_architectural_noise(lat, lon)
        
        # 2. Análisis Hidrológico Estratégico
        hydro_score = self.analyze_hydro_strategic(lat, lon)
        
        # 3. Scoring según el Modo
        final_score = 0.0
        
        if self.mode == SettlementMode.SETTLEMENT_PROBABILITY:
            # Pesa densidad y clustering
            final_score = (arch_sig.density_index * 0.5 + 
                          arch_sig.clustering_coefficient * 0.3 +
                          hydro_score * 0.2)
            
        elif self.mode == SettlementMode.PALEO_HYDRO_SETTLEMENT:
            # Hidrología manda, pero necesita algo de estructura
            final_score = (hydro_score * 0.7 + 
                          arch_sig.density_index * 0.3)
            
        elif self.mode == SettlementMode.ARCHITECTURAL_NOISE:
            # Busca ángulos y fragmentos, ignora contexto un poco
            final_score = (arch_sig.orthogonality_ratio * 0.6 + 
                          arch_sig.linear_fragment_count / 50.0 * 0.4)

        # 4. Interpretación "Proto-Urban"
        # Requiere: Alta densidad + Ortogonalidad + Agua
        is_proto_urban = (arch_sig.density_index > 0.7 and 
                         arch_sig.orthogonality_ratio > 0.5 and
                         hydro_score > 0.6)

        interp = "Ruido Natural"
        if final_score > 0.6: interp = "Posible Ocupación Estacional"
        if final_score > 0.8: interp = "NUCLEO DE ASENTAMIENTO DENSO"
        if is_proto_urban: interp = "🔥 CANDIDATO PROTO-URBANO / NODO REGIONAL"

        return SettlementResult(
            candidate_id=f"STL-{int(lat*1000)}-{int(lon*1000)}",
            lat=lat, 
            lon=lon,
            mode=self.mode,
            probability_score=final_score,
            architectural_noise=arch_sig.density_index,
            hydro_context_score=hydro_score,
            is_proto_urban=is_proto_urban,
            interpretation=interp
        )
