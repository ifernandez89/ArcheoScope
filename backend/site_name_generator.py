#!/usr/bin/env python3
"""
Generador de nombres descriptivos para sitios arqueológicos.
Usa geocoding reverso para obtener nombres de lugares reales.
"""

import requests
from typing import Optional, Dict
import time

class SiteNameGenerator:
    """Genera nombres descriptivos para sitios basados en coordenadas."""
    
    def __init__(self):
        self.cache = {}
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Respetar rate limits
    
    def generate_name(self, lat: float, lon: float, environment_type: str) -> Dict[str, str]:
        """
        Generar nombre descriptivo para un sitio.
        
        Returns:
            Dict con:
            - name: Nombre principal del sitio
            - slug: Slug único para URL
            - country: País
            - region: Región/estado
        """
        
        # Intentar geocoding reverso
        location_info = self._reverse_geocode(lat, lon)
        
        if location_info:
            # Construir nombre descriptivo
            parts = []
            
            # Agregar lugar más específico disponible
            if location_info.get('city'):
                parts.append(location_info['city'])
            elif location_info.get('town'):
                parts.append(location_info['town'])
            elif location_info.get('village'):
                parts.append(location_info['village'])
            elif location_info.get('county'):
                parts.append(location_info['county'])
            elif location_info.get('state'):
                parts.append(location_info['state'])
            
            # Agregar país si no está en el nombre
            if location_info.get('country') and len(parts) == 0:
                parts.append(location_info['country'])
            
            # Agregar tipo de ambiente
            env_suffix = self._get_environment_suffix(environment_type)
            if env_suffix:
                parts.append(env_suffix)
            
            # Construir nombre
            if parts:
                name = " - ".join(parts)
            else:
                # Fallback a coordenadas
                name = f"Site {lat:.4f}°N {abs(lon):.4f}°{'W' if lon < 0 else 'E'}"
            
            # Generar slug
            slug = self._generate_slug(name, lat, lon)
            
            return {
                'name': name,
                'slug': slug,
                'country': location_info.get('country', 'Unknown'),
                'region': location_info.get('state') or location_info.get('county')
            }
        else:
            # Fallback sin geocoding
            name = f"Site {lat:.4f}°N {abs(lon):.4f}°{'W' if lon < 0 else 'E'}"
            env_suffix = self._get_environment_suffix(environment_type)
            if env_suffix:
                name += f" - {env_suffix}"
            
            return {
                'name': name,
                'slug': self._generate_slug(name, lat, lon),
                'country': 'Unknown',
                'region': None
            }
    
    def _reverse_geocode(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Obtener información de ubicación usando Nominatim (OpenStreetMap).
        Respeta rate limits.
        """
        
        # Check cache
        cache_key = f"{lat:.4f},{lon:.4f}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        
        try:
            # Nominatim API (OpenStreetMap)
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'zoom': 10,  # Nivel de detalle
                'addressdetails': 1
            }
            headers = {
                'User-Agent': 'ArcheoScope/2.0 (Archaeological Research)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            self.last_request_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                address = data.get('address', {})
                
                result = {
                    'city': address.get('city'),
                    'town': address.get('town'),
                    'village': address.get('village'),
                    'county': address.get('county'),
                    'state': address.get('state'),
                    'country': address.get('country'),
                    'country_code': address.get('country_code', '').upper()
                }
                
                # Cache result
                self.cache[cache_key] = result
                return result
            else:
                print(f"[GEOCODING] Error {response.status_code} para {lat}, {lon}")
                return None
                
        except Exception as e:
            print(f"[GEOCODING] Exception: {e}")
            return None
    
    def _get_environment_suffix(self, environment_type: str) -> Optional[str]:
        """Obtener sufijo descriptivo según tipo de ambiente."""
        suffixes = {
            'desert': 'Desert Zone',
            'forest': 'Forest Area',
            'tropical_forest': 'Tropical Forest',
            'polar_ice': 'Polar Region',
            'glacier': 'Glacial Area',
            'mountain': 'Mountain Region',
            'agricultural': 'Agricultural Zone',
            'grassland': 'Grassland',
            'shallow_sea': 'Coastal Waters',
            'urban': 'Urban Area'
        }
        return suffixes.get(environment_type)
    
    def _generate_slug(self, name: str, lat: float, lon: float) -> str:
        """Generar slug único para URL."""
        import re
        import time
        
        # Convertir a minúsculas y reemplazar espacios
        slug = name.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # Agregar coordenadas Y timestamp para unicidad
        coord_suffix = f"{int(abs(lat)*1000)}-{int(abs(lon)*1000)}"
        timestamp_suffix = str(int(time.time()))[-6:]  # Últimos 6 dígitos del timestamp
        slug = f"{slug[:40]}-{coord_suffix}-{timestamp_suffix}"
        
        return slug

# Instancia global
site_name_generator = SiteNameGenerator()
