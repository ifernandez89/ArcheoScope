"""
ODE (Orbital Data Explorer) Connector
======================================

Conector para acceder a datos de Marte a través de la API de ODE.
URL: https://ode.rsl.wustl.edu/

Instrumentos soportados:
- CTX (Context Camera)
- HiRISE (High Resolution Imaging Science Experiment)
- THEMIS (Thermal Emission Imaging System)
- MOLA (Mars Orbiter Laser Altimeter)
- SHARAD (Shallow Radar)
- CRISM (Compact Reconnaissance Imaging Spectrometer)
"""

import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ODEProduct:
    """Producto de datos de ODE."""
    product_id: str
    instrument: str
    target: str
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    resolution: float
    acquisition_date: str
    url: str
    file_size: int


class ODEConnector:
    """
    Conector para ODE (Orbital Data Explorer).
    
    Permite buscar y descargar datos de instrumentos marcianos.
    """
    
    BASE_URL = "https://ode.rsl.wustl.edu/mars"
    
    INSTRUMENTS = {
        'ctx': 'Context Camera',
        'hirise': 'High Resolution Imaging Science Experiment',
        'themis': 'Thermal Emission Imaging System',
        'mola': 'Mars Orbiter Laser Altimeter',
        'sharad': 'Shallow Radar',
        'crism': 'Compact Reconnaissance Imaging Spectrometer'
    }
    
    def __init__(self):
        """Inicializar conector ODE."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ArcheoScope-Planetary/1.0'
        })
    
    def search_products(
        self,
        instrument: str,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        max_results: int = 100
    ) -> List[ODEProduct]:
        """
        Buscar productos en ODE por región geográfica.
        
        Args:
            instrument: Instrumento ('ctx', 'hirise', 'themis', etc.)
            lat_min: Latitud mínima (-90 a 90)
            lat_max: Latitud máxima (-90 a 90)
            lon_min: Longitud mínima (0 a 360)
            lon_max: Longitud máxima (0 a 360)
            max_results: Número máximo de resultados
            
        Returns:
            Lista de productos encontrados
        """
        logger.info(f"🔍 Buscando productos {instrument} en ODE")
        logger.info(f"   Región: [{lat_min}, {lat_max}] x [{lon_min}, {lon_max}]")
        
        # Convertir longitudes a formato ODE (0-360)
        if lon_min < 0:
            lon_min += 360
        if lon_max < 0:
            lon_max += 360
        
        # Construir query
        params = {
            'query': 'product',
            'results': 'c',
            'output': 'JSON',
            'target': 'mars',
            'ihid': self._get_instrument_id(instrument),
            'minlat': lat_min,
            'maxlat': lat_max,
            'westlon': lon_min,
            'eastlon': lon_max,
            'limit': max_results
        }
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}/qjson",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            products = self._parse_products(data, instrument)
            
            logger.info(f"✅ Encontrados {len(products)} productos")
            return products
            
        except requests.RequestException as e:
            logger.error(f"❌ Error buscando en ODE: {e}")
            return []
    
    def download_product(
        self,
        product: ODEProduct,
        output_path: str
    ) -> bool:
        """
        Descargar un producto de ODE.
        
        Args:
            product: Producto a descargar
            output_path: Ruta donde guardar el archivo
            
        Returns:
            True si se descargó correctamente
        """
        logger.info(f"⬇️ Descargando {product.product_id}")
        
        try:
            response = self.session.get(
                product.url,
                stream=True,
                timeout=300
            )
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"✅ Descargado: {output_path}")
            return True
            
        except requests.RequestException as e:
            logger.error(f"❌ Error descargando: {e}")
            return False
    
    def get_coverage(
        self,
        instrument: str,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Dict[str, any]:
        """
        Obtener cobertura de datos para una región.
        
        Returns:
            Diccionario con estadísticas de cobertura
        """
        products = self.search_products(
            instrument, lat_min, lat_max, lon_min, lon_max
        )
        
        if not products:
            return {
                'available': False,
                'count': 0,
                'coverage_percent': 0.0
            }
        
        # Calcular área cubierta (simplificado)
        total_area = (lat_max - lat_min) * (lon_max - lon_min)
        covered_area = len(products) * 0.1  # Estimación
        coverage_percent = min(100.0, (covered_area / total_area) * 100)
        
        return {
            'available': True,
            'count': len(products),
            'coverage_percent': coverage_percent,
            'resolution_m': products[0].resolution if products else None,
            'latest_date': max(p.acquisition_date for p in products)
        }
    
    def _get_instrument_id(self, instrument: str) -> str:
        """Obtener ID de instrumento para ODE."""
        instrument_ids = {
            'ctx': 'mro-ctx',
            'hirise': 'mro-hirise',
            'themis': 'ody-themis',
            'mola': 'mgs-mola',
            'sharad': 'mro-sharad',
            'crism': 'mro-crism'
        }
        return instrument_ids.get(instrument.lower(), instrument)
    
    def _parse_products(
        self,
        data: Dict,
        instrument: str
    ) -> List[ODEProduct]:
        """Parsear respuesta JSON de ODE."""
        products = []
        
        if 'ODEResults' not in data:
            return products
        
        for item in data['ODEResults'].get('Products', {}).get('Product', []):
            try:
                product = ODEProduct(
                    product_id=item.get('Product_id', ''),
                    instrument=instrument,
                    target='mars',
                    lat_min=float(item.get('Minimum_latitude', 0)),
                    lat_max=float(item.get('Maximum_latitude', 0)),
                    lon_min=float(item.get('Westernmost_longitude', 0)),
                    lon_max=float(item.get('Easternmost_longitude', 0)),
                    resolution=float(item.get('Map_scale', 0)),
                    acquisition_date=item.get('UTC_start_time', ''),
                    url=item.get('Product_files', {}).get('Product_file', [{}])[0].get('URL', ''),
                    file_size=int(item.get('Product_files', {}).get('Product_file', [{}])[0].get('Size', 0))
                )
                products.append(product)
            except (ValueError, KeyError, IndexError) as e:
                logger.warning(f"⚠️ Error parseando producto: {e}")
                continue
        
        return products


# Conectores específicos por instrumento

class CTXConnector(ODEConnector):
    """Conector para CTX (Context Camera) - 6 m/pixel."""
    
    def __init__(self):
        super().__init__()
        self.instrument = 'ctx'
        self.resolution = 6.0  # metros/pixel


class HiRISEConnector(ODEConnector):
    """Conector para HiRISE - 25-50 cm/pixel."""
    
    def __init__(self):
        super().__init__()
        self.instrument = 'hirise'
        self.resolution = 0.25  # metros/pixel


class THEMISConnector(ODEConnector):
    """Conector para THEMIS (Thermal) - 100 m/pixel."""
    
    def __init__(self):
        super().__init__()
        self.instrument = 'themis'
        self.resolution = 100.0  # metros/pixel


class MOLAConnector(ODEConnector):
    """Conector para MOLA (Altimetría) - 463 m/pixel."""
    
    def __init__(self):
        super().__init__()
        self.instrument = 'mola'
        self.resolution = 463.0  # metros/pixel


class SHARADConnector(ODEConnector):
    """Conector para SHARAD (Radar) - 15 m penetración."""
    
    def __init__(self):
        super().__init__()
        self.instrument = 'sharad'
        self.penetration_depth = 15.0  # metros


class CRISMConnector(ODEConnector):
    """Conector para CRISM (Espectral) - 18 m/pixel."""
    
    def __init__(self):
        super().__init__()
        self.instrument = 'crism'
        self.resolution = 18.0  # metros/pixel
