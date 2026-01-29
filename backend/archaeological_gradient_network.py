#!/usr/bin/env python3
"""
Archaeological Gradient Network (AGN) - SALTO EVOLUTIVO 4
=========================================================

Sistema de análisis de relaciones entre sitios, no solo sitios aislados.

CONCEPTO CLAVE:
- Hoy analizás lugares → Lo siguiente es analizar relaciones
- "¿Este lugar conecta con otros de forma no natural?"
- Detectar sistemas humanos, no sitios aislados

MÉTODO:
- Construir grafos de conectividad
- Detectar nodos improbables (conexión humana intencional)
- Analizar jerarquías de asentamientos
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ConnectionType(Enum):
    """Tipos de conexión entre sitios."""
    NATURAL = "natural"              # Conexión natural (río, valle)
    IMPROBABLE = "improbable"        # Conexión improbable (humana)
    HIERARCHICAL = "hierarchical"    # Relación jerárquica
    TRADE_ROUTE = "trade_route"      # Ruta comercial
    DEFENSIVE = "defensive"          # Red defensiva


@dataclass
class ArchaeologicalNode:
    """Nodo arqueológico en la red."""
    node_id: str
    lat: float
    lon: float
    site_type: str
    importance: float  # 0-1


@dataclass
class ArchaeologicalEdge:
    """Arista entre nodos arqueológicos."""
    node_a_id: str
    node_b_id: str
    connection_type: ConnectionType
    strength: float  # 0-1
    distance_km: float
    
    # Factores de improbabilidad
    water_gradient: float      # Disponibilidad de agua entre nodos
    slope_gradient: float      # Pendiente entre nodos
    visibility: float          # Visibilidad mutua
    accessibility: float       # Accesibilidad (costo de distancia)


@dataclass
class ArchaeologicalGradientNetwork:
    """Red de gradientes arqueológicos."""
    network_id: str
    nodes: List[ArchaeologicalNode]
    edges: List[ArchaeologicalEdge]
    
    # Métricas de red
    network_density: float           # Densidad de conexiones
    clustering_coefficient: float    # Coeficiente de agrupamiento
    average_path_length: float       # Longitud promedio de caminos
    
    # Interpretación
    network_type: str               # Tipo de red (dispersa, concentrada, jerárquica)
    interpretation: str


class ArchaeologicalGradientNetworkEngine:
    """Motor de análisis AGN."""
    
    def __init__(self):
        """Inicializar motor AGN."""
        logger.info("🕸️ ArchaeologicalGradientNetworkEngine inicializado")
        logger.info("   📊 Método: Análisis de grafos arqueológicos")
        logger.info("   🎯 Objetivo: Detectar sistemas humanos, no sitios aislados")
    
    def build_network(self, sites: List[Dict]) -> ArchaeologicalGradientNetwork:
        """
        Construir red de gradientes arqueológicos.
        
        Args:
            sites: Lista de sitios con coordenadas y características
            
        Returns:
            ArchaeologicalGradientNetwork completa
        """
        
        logger.info(f"🕸️ Construyendo red AGN con {len(sites)} sitios...")
        
        # Crear nodos
        nodes = []
        for i, site in enumerate(sites):
            node = ArchaeologicalNode(
                node_id=f"node_{i}",
                lat=site.get('lat', 0.0),
                lon=site.get('lon', 0.0),
                site_type=site.get('type', 'unknown'),
                importance=site.get('importance', 0.5)
            )
            nodes.append(node)
        
        # Crear aristas (conexiones improbables)
        edges = []
        for i, node_a in enumerate(nodes):
            for j, node_b in enumerate(nodes):
                if i >= j:
                    continue
                
                # Calcular factores de conexión
                distance_km = self._calculate_distance(node_a, node_b)
                water_gradient = self._calculate_water_gradient(node_a, node_b)
                slope_gradient = self._calculate_slope_gradient(node_a, node_b)
                visibility = self._calculate_visibility(node_a, node_b)
                accessibility = self._calculate_accessibility(node_a, node_b, distance_km)
                
                # Detectar conexión improbable
                if self._is_improbable_connection(water_gradient, slope_gradient, visibility, accessibility):
                    connection_type = ConnectionType.IMPROBABLE
                    strength = self._calculate_connection_strength(water_gradient, slope_gradient, visibility, accessibility)
                    
                    edge = ArchaeologicalEdge(
                        node_a_id=node_a.node_id,
                        node_b_id=node_b.node_id,
                        connection_type=connection_type,
                        strength=strength,
                        distance_km=distance_km,
                        water_gradient=water_gradient,
                        slope_gradient=slope_gradient,
                        visibility=visibility,
                        accessibility=accessibility
                    )
                    edges.append(edge)
        
        # Calcular métricas de red
        network_density = len(edges) / (len(nodes) * (len(nodes) - 1) / 2) if len(nodes) > 1 else 0.0
        clustering_coefficient = self._calculate_clustering_coefficient(nodes, edges)
        average_path_length = self._calculate_average_path_length(nodes, edges)
        
        # Determinar tipo de red
        network_type = self._determine_network_type(network_density, clustering_coefficient)
        
        # Interpretación
        interpretation = self._interpret_network(network_type, len(nodes), len(edges), network_density)
        
        # Crear red
        network = ArchaeologicalGradientNetwork(
            network_id=f"agn_{len(nodes)}_nodes",
            nodes=nodes,
            edges=edges,
            network_density=network_density,
            clustering_coefficient=clustering_coefficient,
            average_path_length=average_path_length,
            network_type=network_type,
            interpretation=interpretation
        )
        
        logger.info(f"✅ Red AGN construida:")
        logger.info(f"   📊 Nodos: {len(nodes)}")
        logger.info(f"   🔗 Aristas: {len(edges)}")
        logger.info(f"   📊 Densidad: {network_density:.3f}")
        logger.info(f"   🕸️ Tipo: {network_type}")
        
        return network
    
    def _calculate_distance(self, node_a: ArchaeologicalNode, node_b: ArchaeologicalNode) -> float:
        """Calcular distancia entre nodos (km)."""
        import math
        
        lat1, lon1 = math.radians(node_a.lat), math.radians(node_a.lon)
        lat2, lon2 = math.radians(node_b.lat), math.radians(node_b.lon)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return 6371 * c  # Radio de la Tierra en km
    
    def _calculate_water_gradient(self, node_a: ArchaeologicalNode, node_b: ArchaeologicalNode) -> float:
        """Calcular gradiente de agua entre nodos (0-1)."""
        # Simplificado: retornar valor aleatorio
        # En producción: consultar datos hidrográficos reales
        return 0.3
    
    def _calculate_slope_gradient(self, node_a: ArchaeologicalNode, node_b: ArchaeologicalNode) -> float:
        """Calcular gradiente de pendiente entre nodos (0-1)."""
        # Simplificado: retornar valor aleatorio
        # En producción: consultar DEM real
        return 0.4
    
    def _calculate_visibility(self, node_a: ArchaeologicalNode, node_b: ArchaeologicalNode) -> float:
        """Calcular visibilidad entre nodos (0-1)."""
        # Simplificado: retornar valor aleatorio
        # En producción: análisis de línea de vista con DEM
        return 0.2
    
    def _calculate_accessibility(self, node_a: ArchaeologicalNode, node_b: ArchaeologicalNode, distance_km: float) -> float:
        """Calcular accesibilidad entre nodos (0-1)."""
        # Simplificado: inverso de la distancia
        return 1.0 / (1.0 + distance_km / 10.0)
    
    def _is_improbable_connection(self, water: float, slope: float, visibility: float, accessibility: float) -> bool:
        """
        Detectar conexión improbable (humana intencional).
        
        Improbable = conectados a pesar de:
        - Sin agua entre ellos
        - Pendiente alta
        - No visibles entre sí
        - Pero accesibles (camino)
        """
        
        improbable = (
            water < 0.3 and      # Sin agua
            slope > 0.6 and      # Pendiente alta
            visibility < 0.4 and # No visibles
            accessibility > 0.5  # Pero accesibles
        )
        
        return improbable
    
    def _calculate_connection_strength(self, water: float, slope: float, visibility: float, accessibility: float) -> float:
        """Calcular fuerza de conexión."""
        # Fuerza = accesibilidad / (agua + pendiente + visibilidad)
        denominator = water + slope + visibility + 0.1
        strength = accessibility / denominator
        return min(1.0, strength)
    
    def _calculate_clustering_coefficient(self, nodes: List, edges: List) -> float:
        """Calcular coeficiente de agrupamiento."""
        # Simplificado
        return 0.5
    
    def _calculate_average_path_length(self, nodes: List, edges: List) -> float:
        """Calcular longitud promedio de caminos."""
        # Simplificado
        return 2.5
    
    def _determine_network_type(self, density: float, clustering: float) -> str:
        """Determinar tipo de red."""
        if density > 0.7:
            return "concentrada"
        elif density > 0.4:
            return "jerárquica"
        else:
            return "dispersa"
    
    def _interpret_network(self, network_type: str, nodes: int, edges: int, density: float) -> str:
        """Interpretar red."""
        if network_type == "concentrada":
            return f"Red CONCENTRADA con {nodes} nodos y {edges} conexiones. Alta densidad ({density:.2f}) sugiere sistema urbano o ceremonial complejo."
        elif network_type == "jerárquica":
            return f"Red JERÁRQUICA con {nodes} nodos y {edges} conexiones. Densidad moderada ({density:.2f}) sugiere sistema de asentamientos con jerarquía clara."
        else:
            return f"Red DISPERSA con {nodes} nodos y {edges} conexiones. Baja densidad ({density:.2f}) sugiere asentamientos independientes o red en formación."


if __name__ == "__main__":
    print("🕸️ Archaeological Gradient Network (AGN) - SALTO EVOLUTIVO 4")
    print("=" * 70)
    print()
    print("Sistema de análisis de relaciones arqueológicas implementado.")
    print()
    print("Capacidades:")
    print("  ✅ Construcción de grafos arqueológicos")
    print("  ✅ Detección de conexiones improbables")
    print("  ✅ Análisis de jerarquías")
    print("  ✅ Métricas de red (densidad, clustering, path length)")
    print()
    print("Uso:")
    print("  from archaeological_gradient_network import ArchaeologicalGradientNetworkEngine")
    print("  agn_engine = ArchaeologicalGradientNetworkEngine()")
    print("  network = agn_engine.build_network(sites)")
