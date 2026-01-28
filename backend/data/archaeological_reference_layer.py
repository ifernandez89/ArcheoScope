#!/usr/bin/env python3
"""
Archaeological Reference Layer - ArcheoScope
============================================

Capa base arqueológica-histórica que alimenta el sistema con sitios conocidos.

FUENTES:
- UNESCO World Heritage Sites (alta confianza: 0.95)
- OpenStreetMap via Overpass API (confianza media: 0.6)
- Curated datasets (Wikimedia, académicos) (confianza variable: 0.5-0.8)

FILOSOFÍA:
- Sitios conocidos NO son anomalías → son gold standards
- Usar como prior en pipeline (NO como señal directa)
- Enriquecer contexto arqueológico del análisis

ARQUITECTURA:
Python ETL → PostgreSQL + PostGIS → Backend consultas espaciales
"""

import requests
import json
import psycopg2
from psycopg2.extras import Json
from shapely.geometry import Point, Polygon, shape
from shapely.wkt import dumps as wkt_dumps
from typing import Dict, List, Any, Optional, Tuple
import time
from datetime import datetime

class ArchaeologicalReferenceLayer:
    """
    Gestor de la capa de referencia arqueológica.
    
    Permite:
    - Ingestar datos de múltiples fuentes
    - Normalizar a formato común
    - Consultas espaciales eficientes
    - Enriquecimiento del pipeline científico
    """
    
    def __init__(self, db_connection_string: str):
        """
        Inicializar capa de referencia.
        
        Args:
            db_connection_string: PostgreSQL connection string
        """
        self.conn_string = db_connection_string
        self.conn = None
        print("[ARCH REF] Archaeological Reference Layer inicializada", flush=True)
    
    def connect(self):
        """Conectar a PostgreSQL."""
        if not self.conn or self.conn.closed:
            self.conn = psycopg2.connect(self.conn_string)
            print("[ARCH REF] Conectado a PostgreSQL", flush=True)
    
    def close(self):
        """Cerrar conexión."""
        if self.conn and not self.conn.closed:
            self.conn.close()
            print("[ARCH REF] Conexión cerrada", flush=True)
    
    # =========================================================================
    # SETUP: Crear tablas y extensiones
    # =========================================================================
    
    def setup_database(self):
        """
        Crear extensión PostGIS y tabla de sitios arqueológicos.
        
        IMPORTANTE: Ejecutar una sola vez al inicializar el sistema.
        """
        print("[ARCH REF] 🗄️ Configurando base de datos...", flush=True)
        
        self.connect()
        cur = self.conn.cursor()
        
        try:
            # Habilitar PostGIS
            cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
            print("[ARCH REF] ✅ PostGIS habilitado", flush=True)
            
            # Crear tabla de sitios arqueológicos
            cur.execute("""
                CREATE TABLE IF NOT EXISTS archaeologica