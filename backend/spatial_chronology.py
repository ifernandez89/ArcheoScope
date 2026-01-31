#!/usr/bin/env python3
"""
ArcheoScope - Spatial & Chronology Estimator
============================================
Módulo para estimar extensión física y cronología relativa 
basada en tipología y contexto paleoclimático.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import random

@dataclass
class SpatialMetrics:
    core_area_km2: float       # Área del núcleo denso
    total_area_km2: float      # Área funcional (con ritual belt)
    core_halo_ratio: float     # Relación núcleo/periferia
    estimated_population: int  # Estimación poblacional teórica

@dataclass
class ChronologyEstimate:
    period: str
    start_bc: int
    end_bc: int
    confidence: float
    basis: List[str]

class SiteAnalyzer:
    """
    Analizador avanzado de sitios para determinar escala y tiempo.
    """
    
    def estimate_spatial_metrics(self, noise_score: float, hydro_score: float) -> SpatialMetrics:
        """
        Estima el tamaño del sitio basado en la intensidad del ruido arquitectónico
        y la capacidad de carga hídrica.
        """
        # A mayor ruido y agua, mayor el sitio.
        base_size = (noise_score * 0.8 + hydro_score * 0.2)
        
        # Simulación de métricas realistas para "Proto-ciudades" del desierto
        core_area = base_size * random.uniform(0.6, 1.2) # 0.6 - 1.2 km2
        
        # El área total suele ser 5x-8x el núcleo (incluyendo zona ritual/agrícola efímera)
        multiplier = random.uniform(5.0, 8.0)
        total_area = core_area * multiplier
        
        # Estimación poblacional: ~150-200 personas por hectárea en núcleo denso neolítico?
        # Seamos conservadores: 50-80 pax/ha para proto-urbano disperso
        hectares = core_area * 100
        pop = int(hectares * random.uniform(40, 70))
        
        return SpatialMetrics(
            core_area_km2=round(core_area, 2),
            total_area_km2=round(total_area, 2),
            core_halo_ratio=round(1/multiplier, 2),
            estimated_population=pop
        )

    def estimate_chronology(self, typology: str, context_type: str) -> ChronologyEstimate:
        """
        Estima cronología basada en modelos paleoclimáticos conocidos (Green Arabia).
        """
        basis = []
        period = "Unknown"
        start_bc = 0
        end_bc = 0
        conf = 0.5
        
        # Regla: Paleolagos + Estructuras de Piedra = Holoceno Húmedo
        if "fossil_basin" in context_type or "hydro" in context_type:
            period = "Holocene Humid Period (Middle)"
            start_bc = -5500
            end_bc = -4000
            conf = 0.75
            basis.append("paleohydrology_association")
            basis.append("desertification_model")

        # Regla: Tipología Pendant/Kite = Neolítico Tardío / Calcolítico
        if typology in ["pendant", "kite", "settlement_complex"]:
            basis.append(f"{typology}_typology")
            if period == "Unknown":
                start_bc = -6000
                end_bc = -3000
                conf = 0.6
            else:
                # Refinar si ya tenemos contexto hídrico
                conf += 0.15 # Alta confianza por convergencia
                
        return ChronologyEstimate(
            period=period,
            start_bc=start_bc,
            end_bc=end_bc,
            confidence=round(conf, 2),
            basis=basis
        )
