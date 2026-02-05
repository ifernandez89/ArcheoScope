#!/usr/bin/env python3
"""
Temporal Forensics Module - ArcheoScope Framework
=================================================

Analiza la necesidad de corrección temporal extrema y redundancia cósmica
en arquitectura monumental para identificar posibles tipologías de colapso.

Basado en el razonamiento forense de inversión:
'¿Qué colapso haría imprescindible construir esto antes de que ocurra?'
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class CollapseCandidate(Enum):
    CLIMATE_NON_PERIODIC = "Clima (Cambio lento/abrupto)"
    GEOPHYSICAL_DRIFT = "Geofísica (Deriva de polos/orientación)"
    CIVILIZATIONAL_DESYNC = "Desincronización Civilizatoria (Reloj común)"
    LONG_CYCLE_COSMIC = "Eventos Cósmicos de Ciclo Largo"

@dataclass
class TemporalMarker:
    name: str
    target_azimuth: float  # Grados
    current_azimuth: float
    precision_error: float
    epoch_alignment: float  # Año (negativo para AC)

class TemporalRiskAnalyzer:
    """
    Analizador de Riesgo Temporal.
    Efectúa ingeniería inversa sobre la necesidad de monumentos astronómicos.
    """
    
    def __init__(self):
        self.precession_rate = 1.0 / 71.6  # Grados por año
        self.obliquity_cycle = 41000  # Ciclo de la oblicuidad
        
    def calculate_temporal_redundancy(self, markers: List[TemporalMarker]) -> float:
        """
        Calcula el índice de redundancia (0-1).
        Cuántos marcadores apuntan al mismo evento astronómico.
        """
        if not markers:
            return 0.0
        
        # Agrupar por 'target_azimuth' aproximado
        groups = {}
        for m in markers:
            key = round(m.target_azimuth / 5) * 5  # Tolerancia de 5 grados para agrupación inicial
            if key not in groups:
                groups[key] = []
            groups[key].append(m)
            
        redundancy_score = sum(len(g) for g in groups.values() if len(g) > 1) / len(markers)
        return np.clip(redundancy_score, 0.0, 1.0)

    def analyze_precession_offset(self, actual_azimuth: float, target_azimuth: float) -> float:
        """Calcula el offset temporal basado en precesión (años)."""
        diff = actual_azimuth - target_azimuth
        return diff / self.precession_rate

    def evaluate_necessity_matrix(self, metrics: Dict) -> Dict[CollapseCandidate, float]:
        """
        Matriz de Necesidad (ArcheoScope Key).
        Asigna probabilidades a los candidatos de colapso basados en requisitos observados.
        """
        
        # Requisitos observados (de 0 a 1)
        prec = metrics.get('precision_extreme', 0.5)
        redun = metrics.get('global_redundancy', 0.5)
        scale = metrics.get('milleanary_scale', 0.5)
        precession = metrics.get('precession_tracking', 0.5)
        literacy_indep = metrics.get('literacy_independence', 0.5)
        
        # Puntuaciones basadas en la tabla del usuario:
        # ✅ = 1.0, ⚠️ = 0.5, ❌ = 0.0
        
        scores = {
            CollapseCandidate.CLIMATE_NON_PERIODIC: (
                precession * 1.0 + redun * 0.0 + prec * 0.5 + scale * 1.0 + literacy_indep * 0.0
            ),
            CollapseCandidate.GEOPHYSICAL_DRIFT: (
                precession * 0.5 + redun * 0.0 + prec * 1.0 + scale * 1.0 + literacy_indep * 0.5
            ),
            CollapseCandidate.CIVILIZATIONAL_DESYNC: (
                precession * 0.5 + redun * 1.0 + prec * 0.5 + scale * 1.0 + literacy_indep * 1.0
            ),
            CollapseCandidate.LONG_CYCLE_COSMIC: (
                precession * 1.0 + redun * 0.5 + prec * 1.0 + scale * 1.0 + literacy_indep * 0.5
            )
        }
        
        # Normalizar probabilidades
        total = sum(scores.values())
        return {k: v/total for k, v in scores.items()}

    def generate_forensic_report(self, site_name: str, metrics: Dict) -> str:
        """Genera el reporte final de 'ingeniería temporal preventiva'."""
        
        probs = self.evaluate_necessity_matrix(metrics)
        best_candidate = max(probs, key=probs.get)
        
        report = []
        report.append(f"# Informe Forense Temporal: {site_name}")
        report.append(f"## Análisis de Necesidad de Corrección Extrema\n")
        
        report.append("### Métricas de Entrada:")
        for k, v in metrics.items():
            report.append(f"- **{k.replace('_', ' ').title()}**: {v:.2f}")
        
        report.append("\n### Matriz de Probabilidad de Colapso:")
        for cand, p in sorted(probs.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- **{cand.value}**: {p*100:.1f}%")
            
        report.append(f"\n### Veredicto de Ingeniería Preventiva:")
        report.append(f"El sistema en {site_name} parece haber sido diseñado primordialmente como una **medida de mitigación contra {best_candidate.value}**.")
        
        if best_candidate == CollapseCandidate.CIVILIZATIONAL_DESYNC:
            report.append("La alta redundancia y la independencia de escritura sugieren un protocolo de 'reinicio' o 'reloj maestro' para una civilización fragmentada.")
        elif best_candidate == CollapseCandidate.GEOPHYSICAL_DRIFT:
            report.append("La obsesión por la cardinalidad y la precisión externa sugieren que el 'norte local' dejó de ser confiable, requiriendo un ancla estelar.")
        elif best_candidate == CollapseCandidate.CLIMATE_NON_PERIODIC:
            report.append("El seguimiento de la precesión y la escala milenaria sugieren la necesidad de observar desfasajes climáticos invisibles en una vida humana.")
        elif best_candidate == CollapseCandidate.LONG_CYCLE_COSMIC:
            report.append("La combinación de precisión extrema y escala temporal indica el monitoreo de eventos que exceden los registros escritos tradicionales.")
            
        report.append("\n---")
        report.append("> *Análisis generado por ArcheoScope Temporal Forensics Module v1.0*")
        
        return "\n".join(report)

if __name__ == "__main__":
    # Test rápido
    analyzer = TemporalRiskAnalyzer()
    giza_metrics = {
        'precision_extreme': 0.98,
        'global_redundancy': 0.85,
        'milleanary_scale': 1.0,
        'precession_tracking': 0.95,
        'literacy_independence': 0.9
    }
    
    print(analyzer.generate_forensic_report("Sistema Giza/Tiwanaku", giza_metrics))
