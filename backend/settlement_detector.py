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
    SURFACE_GEOMETRY_SCAN = "surface_geometry_scan"   # Geoglifos, alineaciones superficiales

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
    signature: Optional[ArchitecturalSignature] = None # Firma detallada

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
            # ... (Lógica Taklamakan seleccionada)
            hotspots = [(40.50, 82.00), (40.35, 82.25), (40.65, 81.80)]
            hydro_sources = [(40.55, 81.95), (40.40, 82.10), (40.70, 81.70)]
            physics = {'hydro_decay': 15, 'noise_decay': 22}
        elif self.region == "RAK_VISIBLE":
            # RUB AL KHALI - VISIBLE MODE (High Contrast / Shadow)
            hotspots = [
                (19.92, 51.05), # RAK-VIS-01: Geoglyph/Kite
                (20.31, 50.41), # RAK-VIS-02: Lithic Alignments
                (19.65, 50.88)  # RAK-VIS-03: Elevated Node
            ]
            hydro_sources = [] 
            physics = {'hydro_decay': 0, 'noise_decay': 40} # Máxima sensibilidad a la forma
        elif self.region == "HARRAT_KHAYBAR":
            # THE GOLD STANDARD (Lava slate)
            hotspots = [(25.85, 39.65)]
            physics = {'hydro_decay': 0, 'noise_decay': 50} # Escala monumental y contraste máximo
        elif self.region == "GOBI_ALTAI":
            # MONGOLIA/KAZAKHSTAN (Steppe/Stone)
            hotspots = [(47.30, 90.80)]
            physics = {'hydro_decay': 0, 'noise_decay': 48}
        elif self.region == "ATACAMA_PEDREGOSO":
            # CHILE - NAZCA LEVEL BORDELANDS
            hotspots = [(-22.95, -68.20)]
            physics = {'hydro_decay': 0, 'noise_decay': 46}
        elif self.region == "RAK_VISIBLE":
            # RUB AL KHALI - CONTROL (Active Sand/Low visibility)
            hotspots = [] # No hay monumentos visibles de escala 300m+
            physics = {'hydro_decay': 0, 'noise_decay': 15} # Punitivo
        else: # DEFAULT
            hotspots = [(20.50, 51.00)]
            physics = {'hydro_decay': 8, 'noise_decay': 20}
            
        return hotspots, [], physics

    def analyze_architectural_noise(self, lat: float, lon: float) -> ArchitecturalSignature:
        """
        Simulación de detección de Geometría Monumental (Modo Extremo).
        """
        hotspots, _, physics = self._get_simulation_data()
        
        # Distancia al hotspot más cercano
        min_dist = min([np.sqrt((lat - hlat)**2 + (lon - hlon)**2) for hlat, hlon in hotspots]) if hotspots else 10.0
        
        # En modo extremo, si no estás cerca de un hito monumental, el score colapsa
        base_density = max(0.01, 1.0 - min_dist * physics['noise_decay'])
        
        ortho_base = 0.05
        if self.mode == SettlementMode.SURFACE_GEOMETRY_SCAN:
            # Requisito: Visibilidad inequívoca
            if min_dist < 0.003: # < 300m aprox
                ortho_base = random.uniform(0.92, 0.98) # NAZCA GRADE
            elif min_dist < 0.01:
                ortho_base = random.uniform(0.70, 0.85) # TYPE B
        
        return ArchitecturalSignature(
            density_index=base_density,
            entropy_score=random.uniform(0.2, 0.5), 
            orthogonality_ratio=ortho_base,
            linear_fragment_count=int(base_density * 200),
            clustering_coefficient=random.uniform(0.8, 0.99)
        )

    def analyze_hydro_strategic(self, lat: float, lon: float) -> float:
        """
        Analiza valor estratégico del agua.
        """
        _, hydro_sources, physics = self._get_simulation_data()
        
        # Manejo de regiones sin fuentes hídricas conocidas
        if not hydro_sources:
            return 0.05
            
        # Distancia a fuente hídrica más cercana
        min_dist = min([np.sqrt((lat - flat)**2 + (lon - flon)**2) for flat, flon in hydro_sources])
        
        if min_dist < 0.02: 
            # En GIZA/ATACAMA/IRAN, estar en la fuente es crítico (Oasis/Qanat)
            if self.region == "ATACAMA":
                return 0.98 if min_dist < 0.01 else 0.4 # Oasis binario
            if self.region == "TAKLAMAKAN":
                return 0.75 # Río activo (inundable)
            if self.region == "IRAN_CENTRAL":
                return 0.95 # Acceso directo a Qanat/Río
            return 0.90 if self.region == "GIZA" else 0.2 
            
        if 0.02 <= min_dist <= 0.12: 
            return 0.98 if self.region in ["TAKLAMAKAN", "IRAN_CENTRAL"] else 0.95
            
        return max(0.05, 1.0 - min_dist * physics['hydro_decay'])

    def detect_settlement(self, lat: float, lon: float) -> SettlementResult:
        # 1-2. Análisis
        arch_sig = self.analyze_architectural_noise(lat, lon)
        hydro_score = self.analyze_hydro_strategic(lat, lon)
        
        # 3. Final Scoring (Modo Extremo)
        final_score = 0.0
        if self.mode == SettlementMode.SURFACE_GEOMETRY_SCAN:
            # Ignoramos todo salvo la geometría pura y la escala
            final_score = (arch_sig.orthogonality_ratio * 0.95 + arch_sig.density_index * 0.05)
            # Penalización por arena activa (Rub' al Khali)
            if self.region == "RAK_VISIBLE":
                final_score *= 0.15 # Colapso científico por falta de plausibilidad óptica
        else:
            final_score = (arch_sig.density_index * 0.5 + arch_sig.clustering_coefficient * 0.3 + hydro_score * 0.2)

        # 4. Clasificación Estricta
        interp = "Negative / Pareidolia"
        if self.mode == SettlementMode.SURFACE_GEOMETRY_SCAN:
            if final_score >= 0.92: 
                interp = "🛰️ TYPE C: OBVIOUS FROM SPACE (Extreme Monumentality)"
            elif final_score >= 0.85: 
                interp = "👁️ TYPE B: HUMAN-CONFIRMABLE (Google Earth Grade)"
            else:
                interp = "❌ DISCARDED: Below Extreme Threshold"
        else:
            if final_score > 0.8: interp = "NUCLEO DE ASENTAMIENTO DENSO"

        return SettlementResult(
            candidate_id=f"EXT-{int(lat*1000)}-{int(lon*1000)}",
            lat=lat, lon=lon, mode=self.mode,
            probability_score=min(0.99, final_score),
            architectural_noise=arch_sig.density_index,
            hydro_context_score=hydro_score,
            is_proto_urban=(final_score > 0.9),
            interpretation=interp,
            signature=arch_sig
        )
