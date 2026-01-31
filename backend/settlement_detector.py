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
    
    def __init__(self, mode: SettlementMode = SettlementMode.SETTLEMENT_PROBABILITY):
        self.mode = mode
        print(f"🏘️ SettlementDetector inicializado en modo: {mode.value.upper()}")

    def analyze_architectural_noise(self, lat: float, lon: float) -> ArchitecturalSignature:
        """
        Simula el análisis de ruido arquitectónico (muros, cimientos).
        En producción: Análisis de textura GLCM + detección de esquinas (Harris).
        """
        # SIMULACIÓN DE DETECCIÓN DE "RUIDO HUMANO"
        # Basado en la lat/lon para consistencia con el cluster anterior
        
        # Hipótesis: Cerca del cluster de geoglifos (20.5, 51.0), hay más ruido
        dist_to_cluster = np.sqrt((lat - 20.5)**2 + (lon - 51.0)**2)
        
        base_density = max(0.0, 1.0 - dist_to_cluster * 10) # Cae rápido al alejarse
        
        # Variabilidad realista
        density = base_density * random.uniform(0.6, 1.0)
        if density < 0.2: density = 0.05 # Ruido de fondo natural
        
        # Asentamientos = Alta entropía local + Ángulos rectos ocultos
        orthogonality = random.uniform(0.1, 0.4) # Natural es bajo
        if density > 0.6: 
            orthogonality += random.uniform(0.2, 0.4) # Sube en asentamientos
            
        return ArchitecturalSignature(
            density_index=density,
            entropy_score=random.uniform(0.5, 0.9), # Asentamientos son caóticos
            orthogonality_ratio=orthogonality,
            linear_fragment_count=int(density * 50),
            clustering_coefficient=random.uniform(0.7, 0.95) # Muy agrupado
        )

    def analyze_hydro_strategic(self, lat: float, lon: float) -> float:
        """
        Analiza valor estratégico del agua (Borde seguro vs Centro inundable).
        """
        # Simulación: El "borde" óptimo está ligeramente desplazado del centro del lago
        # Asumimos lago fósil en 20.52, 51.02
        dist_to_paleolake = np.sqrt((lat - 20.52)**2 + (lon - 51.02)**2)
        
        # Perfil tipo "Donut": 
        # Centro (0km) = Malo (inundable)
        # Borde (2-5km) = Óptimo (acceso + seguridad)
        # Lejos (>10km) = Malo (sin agua)
        
        if dist_to_paleolake < 0.02: return 0.2 # Muy cerca/dentro
        if 0.02 <= dist_to_paleolake <= 0.06: return 0.9 # BORDE IDEAL
        return max(0.1, 1.0 - dist_to_paleolake * 10)

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
