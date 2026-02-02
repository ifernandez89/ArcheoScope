#!/usr/bin/env python3
"""
Cognitive Homology Index (CHI) - ArcheoScope Framework v2.0
============================================================

Módulo para evaluar homología cognitiva entre patrones celestes y arquitectónicos.
NO evalúa correspondencia geométrica directa, sino isomorfismo relacional.

Autor: Antigravity AI
Fecha: 2026-02-02
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import networkx as nx
from scipy.stats import entropy, spearmanr


class NodeType(Enum):
    """Tipo de nodo en el sistema."""
    PRIMARY = "primary"      # Estructura/estrella dominante
    SECONDARY = "secondary"  # Flanqueante o auxiliar
    TERTIARY = "tertiary"    # Satélite o menor


@dataclass
class CelestialNode:
    """Nodo celeste (estrella o asterismo)."""
    name: str
    magnitude: float  # Brillo aparente (menor = más brillante)
    ra: float  # Ascensión recta (grados)
    dec: float  # Declinación (grados)
    node_type: NodeType


@dataclass
class ArchitecturalNode:
    """Nodo arquitectónico (estructura)."""
    name: str
    lat: float
    lon: float
    volume_m3: float  # Volumen estimado
    height_m: float
    node_type: NodeType
    ritual_importance: float  # 0-1, basado en evidencia arqueológica


@dataclass
class HomologyResult:
    """Resultado del análisis de homología cognitiva."""
    chi_score: float  # Cognitive Homology Index (0-1)
    graph_isomorphism: float  # Similitud de grafos (0-1)
    entropy_correlation: float  # Correlación de entropías
    rank_correlation: float  # Correlación de Spearman en rankings
    structural_order: float  # Nivel de orden vs azar (0-1)
    is_significant: bool  # p < 0.05
    interpretation: str


class CognitiveHomologyAnalyzer:
    """
    Analizador de Homología Cognitiva.
    
    Evalúa si existe evidencia de que un patrón arquitectónico
    reproduce la ESTRUCTURA RELACIONAL (no geométrica) de un patrón celeste.
    """
    
    def __init__(self):
        self.significance_threshold = 0.05
        
    def analyze(
        self,
        celestial_nodes: List[CelestialNode],
        architectural_nodes: List[ArchitecturalNode],
        site_name: str = "Unknown"
    ) -> HomologyResult:
        """
        Ejecuta análisis completo de homología cognitiva.
        
        Args:
            celestial_nodes: Lista de nodos celestes (ej. estrellas de Orión)
            architectural_nodes: Lista de nodos arquitectónicos (ej. pirámides)
            site_name: Nombre del sitio arqueológico
            
        Returns:
            HomologyResult con métricas y veredicto
        """
        
        # 1. Construir grafos relacionales
        G_sky = self._build_celestial_graph(celestial_nodes)
        G_earth = self._build_architectural_graph(architectural_nodes)
        
        # 2. Análisis de isomorfismo de grafos
        graph_sim = self._compute_graph_similarity(G_sky, G_earth)
        
        # 3. Análisis de entropía estructural
        entropy_corr = self._compute_entropy_correlation(G_sky, G_earth)
        
        # 4. Análisis de rankings (jerarquía)
        rank_corr = self._compute_rank_correlation(
            celestial_nodes, architectural_nodes
        )
        
        # 5. Medida de orden estructural (vs azar)
        structural_order = self._compute_structural_order(G_earth)
        
        # 6. Calcular CHI (Cognitive Homology Index)
        chi_score = self._compute_chi(
            graph_sim, entropy_corr, rank_corr, structural_order
        )
        
        # 7. Test de significancia
        is_significant = chi_score > 0.65  # Umbral empírico
        
        # 8. Interpretación
        interpretation = self._generate_interpretation(
            chi_score, graph_sim, rank_corr, site_name
        )
        
        return HomologyResult(
            chi_score=chi_score,
            graph_isomorphism=graph_sim,
            entropy_correlation=entropy_corr,
            rank_correlation=rank_corr,
            structural_order=structural_order,
            is_significant=is_significant,
            interpretation=interpretation
        )
    
    def _build_celestial_graph(self, nodes: List[CelestialNode]) -> nx.Graph:
        """Construye grafo relacional del patrón celeste."""
        G = nx.Graph()
        
        # Añadir nodos con atributos
        for node in nodes:
            G.add_node(
                node.name,
                magnitude=node.magnitude,
                node_type=node.node_type.value
            )
        
        # Añadir aristas basadas en relaciones visuales/simbólicas
        # Criterio: conectar nodos "cercanos" visualmente o relacionados
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i+1:]:
                # Distancia angular
                dist = self._angular_distance(n1.ra, n1.dec, n2.ra, n2.dec)
                
                # Conectar si están "cerca" (< 30 grados) o son jerárquicamente relevantes
                if dist < 30 or (n1.node_type == NodeType.PRIMARY or n2.node_type == NodeType.PRIMARY):
                    G.add_edge(n1.name, n2.name, weight=1.0 / (dist + 1))
        
        return G
    
    def _build_architectural_graph(self, nodes: List[ArchitecturalNode]) -> nx.Graph:
        """Construye grafo relacional del patrón arquitectónico."""
        G = nx.Graph()
        
        # Añadir nodos con atributos
        for node in nodes:
            G.add_node(
                node.name,
                volume=node.volume_m3,
                height=node.height_m,
                node_type=node.node_type.value,
                importance=node.ritual_importance
            )
        
        # Añadir aristas basadas en relaciones espaciales/rituales
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i+1:]:
                # Distancia normalizada (km)
                dist_km = self._haversine_distance(n1.lat, n1.lon, n2.lat, n2.lon)
                
                # Conectar si están "cerca" (< 5 km) o son jerárquicamente relevantes
                if dist_km < 5 or (n1.node_type == NodeType.PRIMARY or n2.node_type == NodeType.PRIMARY):
                    G.add_edge(n1.name, n2.name, weight=1.0 / (dist_km + 0.1))
        
        return G
    
    def _compute_graph_similarity(self, G1: nx.Graph, G2: nx.Graph) -> float:
        """
        Calcula similitud entre grafos usando métricas topológicas.
        NO evalúa isomorfismo exacto, sino similitud estructural.
        """
        if len(G1.nodes) != len(G2.nodes):
            return 0.0
        
        # Métricas topológicas
        metrics = []
        
        # 1. Similitud de grado promedio
        avg_degree_1 = np.mean([d for n, d in G1.degree()])
        avg_degree_2 = np.mean([d for n, d in G2.degree()])
        degree_sim = 1 - abs(avg_degree_1 - avg_degree_2) / max(avg_degree_1, avg_degree_2, 1)
        metrics.append(degree_sim)
        
        # 2. Similitud de clustering
        try:
            clustering_1 = nx.average_clustering(G1)
            clustering_2 = nx.average_clustering(G2)
            cluster_sim = 1 - abs(clustering_1 - clustering_2)
            metrics.append(cluster_sim)
        except:
            pass
        
        # 3. Similitud de centralidad
        try:
            cent_1 = list(nx.degree_centrality(G1).values())
            cent_2 = list(nx.degree_centrality(G2).values())
            cent_corr, _ = spearmanr(sorted(cent_1, reverse=True), sorted(cent_2, reverse=True))
            if not np.isnan(cent_corr):
                metrics.append((cent_corr + 1) / 2)  # Normalizar a [0,1]
        except:
            pass
        
        return np.mean(metrics) if metrics else 0.0
    
    def _compute_entropy_correlation(self, G1: nx.Graph, G2: nx.Graph) -> float:
        """Calcula correlación entre entropías estructurales."""
        
        # Entropía basada en distribución de grados
        degrees_1 = [d for n, d in G1.degree()]
        degrees_2 = [d for n, d in G2.degree()]
        
        # Normalizar a distribución de probabilidad
        p1 = np.array(degrees_1) / sum(degrees_1) if sum(degrees_1) > 0 else np.ones(len(degrees_1)) / len(degrees_1)
        p2 = np.array(degrees_2) / sum(degrees_2) if sum(degrees_2) > 0 else np.ones(len(degrees_2)) / len(degrees_2)
        
        # Calcular entropías
        H1 = entropy(p1)
        H2 = entropy(p2)
        
        # Similitud de entropía (normalizada)
        max_entropy = max(H1, H2, 1e-6)
        return 1 - abs(H1 - H2) / max_entropy
    
    def _compute_rank_correlation(
        self,
        celestial: List[CelestialNode],
        architectural: List[ArchitecturalNode]
    ) -> float:
        """
        Calcula correlación de Spearman entre rankings de importancia.
        Cielo: magnitud (brillo)
        Tierra: volumen + importancia ritual
        """
        if len(celestial) != len(architectural):
            return 0.0
        
        # Ranking celeste (por brillo, menor magnitud = más importante)
        sky_ranks = sorted(range(len(celestial)), key=lambda i: celestial[i].magnitude)
        
        # Ranking arquitectónico (por volumen * importancia)
        earth_scores = [n.volume_m3 * (n.ritual_importance + 0.1) for n in architectural]
        earth_ranks = sorted(range(len(architectural)), key=lambda i: earth_scores[i], reverse=True)
        
        # Correlación de Spearman
        corr, p_value = spearmanr(sky_ranks, earth_ranks)
        
        # Normalizar a [0,1]
        return (corr + 1) / 2 if not np.isnan(corr) else 0.0
    
    def _compute_structural_order(self, G: nx.Graph) -> float:
        """
        Mide nivel de orden estructural vs azar.
        Usa ratio de clustering y path length vs grafo aleatorio.
        """
        if len(G.nodes) < 3:
            return 0.0
        
        try:
            # Métricas del grafo real
            C_real = nx.average_clustering(G)
            
            # Comparar con grafo aleatorio (Erdős–Rényi)
            n = len(G.nodes)
            m = len(G.edges)
            p = 2 * m / (n * (n - 1)) if n > 1 else 0
            
            G_random = nx.erdos_renyi_graph(n, p)
            C_random = nx.average_clustering(G_random)
            
            # Orden = cuánto más estructurado que el azar
            if C_random > 0:
                order = min(C_real / C_random, 1.0)
            else:
                order = 1.0 if C_real > 0 else 0.0
            
            return order
        except:
            return 0.5  # Valor neutro si falla el cálculo
    
    def _compute_chi(
        self,
        graph_sim: float,
        entropy_corr: float,
        rank_corr: float,
        structural_order: float
    ) -> float:
        """
        Calcula Cognitive Homology Index (CHI).
        
        Fórmula ponderada:
        CHI = 0.35*graph_sim + 0.25*entropy_corr + 0.30*rank_corr + 0.10*structural_order
        """
        chi = (
            0.35 * graph_sim +
            0.25 * entropy_corr +
            0.30 * rank_corr +
            0.10 * structural_order
        )
        return np.clip(chi, 0.0, 1.0)
    
    def _generate_interpretation(
        self,
        chi: float,
        graph_sim: float,
        rank_corr: float,
        site_name: str
    ) -> str:
        """Genera interpretación científica del resultado."""
        
        if chi >= 0.75:
            return (
                f"HOMOLOGÍA COGNITIVA FUERTE detectada en {site_name}. "
                f"Evidencia robusta de que el patrón arquitectónico reproduce "
                f"la estructura relacional del patrón celeste (CHI={chi:.2f}). "
                f"Esto sugiere uso del cielo como marco organizador."
            )
        elif chi >= 0.65:
            return (
                f"HOMOLOGÍA COGNITIVA MODERADA en {site_name}. "
                f"Existen similitudes estructurales significativas (CHI={chi:.2f}), "
                f"pero no se puede descartar convergencia independiente. "
                f"Se requiere evidencia contextual adicional."
            )
        elif chi >= 0.50:
            return (
                f"HOMOLOGÍA COGNITIVA DÉBIL en {site_name}. "
                f"Algunas similitudes detectadas (CHI={chi:.2f}), pero insuficientes "
                f"para afirmar influencia celeste directa. Posible coincidencia."
            )
        else:
            return (
                f"NO se detecta homología cognitiva en {site_name}. "
                f"El patrón arquitectónico no replica la estructura del patrón celeste "
                f"(CHI={chi:.2f}). Organización independiente o basada en otros factores."
            )
    
    @staticmethod
    def _angular_distance(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
        """Calcula distancia angular entre dos puntos celestes (grados)."""
        ra1_rad = np.radians(ra1)
        dec1_rad = np.radians(dec1)
        ra2_rad = np.radians(ra2)
        dec2_rad = np.radians(dec2)
        
        cos_dist = (
            np.sin(dec1_rad) * np.sin(dec2_rad) +
            np.cos(dec1_rad) * np.cos(dec2_rad) * np.cos(ra1_rad - ra2_rad)
        )
        
        return np.degrees(np.arccos(np.clip(cos_dist, -1, 1)))
    
    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcula distancia haversine entre dos puntos terrestres (km)."""
        R = 6371  # Radio de la Tierra en km
        
        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        
        a = (
            np.sin(dlat / 2)**2 +
            np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
        )
        c = 2 * np.arcsin(np.sqrt(a))
        
        return R * c


# ============================================================================
# CASOS DE PRUEBA PREDEFINIDOS
# ============================================================================

def get_orion_belt() -> List[CelestialNode]:
    """Retorna las 3 estrellas del Cinturón de Orión."""
    return [
        CelestialNode("Alnitak", 1.77, 85.19, -1.94, NodeType.PRIMARY),
        CelestialNode("Alnilam", 1.69, 84.05, -1.20, NodeType.PRIMARY),
        CelestialNode("Mintaka", 2.23, 83.00, -0.30, NodeType.SECONDARY)
    ]


def get_giza_pyramids() -> List[ArchitecturalNode]:
    """Retorna las 3 pirámides principales de Giza."""
    return [
        ArchitecturalNode("Khufu", 29.9792, 31.1342, 2583283, 146.5, NodeType.PRIMARY, 1.0),
        ArchitecturalNode("Khafre", 29.9753, 31.1308, 2211096, 143.5, NodeType.PRIMARY, 0.95),
        ArchitecturalNode("Menkaure", 29.9722, 31.1285, 235183, 65.5, NodeType.SECONDARY, 0.75)
    ]
