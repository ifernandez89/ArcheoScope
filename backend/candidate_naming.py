#!/usr/bin/env python3
"""
Sistema de nomenclatura inteligente para candidatos arqueológicos.
Genera nombres descriptivos basados en características geográficas.
"""

from typing import Dict, Any, Optional
import requests
from datetime import datetime

def get_location_name(lat: float, lon: float) -> Optional[str]:
    """
    Obtener nombre de ubicación usando reverse geocoding (Nominatim).
    
    Returns:
        Nombre descriptivo o None si falla
    """
    try:
        # Usar Nominatim (OpenStreetMap) - gratuito y sin API key
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "zoom": 10,  # Nivel de detalle (10 = ciudad/pueblo)
            "accept-language": "en"
        }
        headers = {
            "User-Agent": "ArcheoScope/2.0 (Archaeological Research)"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            address = data.get("address", {})
            
            # Prioridad de nombres
            location_parts = []
            
            # 1. Característica natural o lugar específico
            if "natural" in address:
                location_parts.append(address["natural"])
            elif "peak" in address:
                location_parts.append(address["peak"])
            elif "water" in address:
                location_parts.append(address["water"])
            
            # 2. Ciudad/pueblo
            if "city" in address:
                location_parts.append(address["city"])
            elif "town" in address:
                location_parts.append(address["town"])
            elif "village" in address:
                location_parts.append(address["village"])
            elif "municipality" in address:
                location_parts.append(address["municipality"])
            
            # 3. Región/estado
            if "state" in address:
                location_parts.append(address["state"])
            elif "region" in address:
                location_parts.append(address["region"])
            elif "province" in address:
                location_parts.append(address["province"])
            
            # 4. País
            if "country" in address:
                location_parts.append(address["country"])
            
            if location_parts:
                # Tomar máximo 3 partes más relevantes
                return ", ".join(location_parts[:3])
        
        return None
        
    except Exception as e:
        print(f"[NAMING] Error en reverse geocoding: {e}", flush=True)
        return None

def generate_candidate_name(
    lat: float,
    lon: