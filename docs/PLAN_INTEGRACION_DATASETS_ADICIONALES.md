# 🚀 PLAN DE INTEGRACIÓN - DATASETS ADICIONALES
## ArcheoScope - Expansión a 15 Instrumentos

---

## 📊 RESUMEN

**Objetivo**: Integrar 5 datasets públicos adicionales para análisis multimodal completo

**Total instrumentos**: 10 → 15 (+50%)

**Tiempo estimado**: 2 semanas

---

## 1️⃣ DATASETS A INTEGRAR

### Dataset 11: HydroSHEDS (Hidrografía)
```
Fuente: HydroSHEDS
URL: https://www.hydrosheds.org/
Tipo: Vectorial (shapefiles) + Raster
Resolución: 15 arc-seconds (~500m)
Cobertura: Global
Acceso: Descarga libre, sin API

Capas:
- Ríos y cursos de agua
- Cuencas hidrográficas
- Dirección de flujo
- Acumulación de flujo
- Elevación hidrológica

Aporte:
✅ Correlación humedad-drenaje
✅ Detección de canales antiguos
✅ Patrones de asentamiento cerca de agua
✅ Micro-relieve hidrológico
```

### Dataset 12: USGS Geology (Geología)
```
Fuente: USGS / Open Geology Maps
URL: https://mrdata.usgs.gov/geology/
Tipo: Vectorial (shapefiles/GeoJSON)
Resolución: Variable (1:500,000 típico)
Cobertura: Global
Acceso: Descarga libre, sin API

Capas:
- Litología (tipo de roca)
- Edad geológica
- Tipo de suelo
- Mineralogía superficial

Aporte:
✅ Contexto geológico de anomalías
✅ Tipo de suelo para correlación con SMAP
✅ Mineralogía para correlación con salinidad
✅ Potencial de preservación arqueológica
```

### Dataset 13: ERA5 Climate (Clima Histórico)
```
Fuente: Copernicus Climate Data Store
URL: https://cds.climate.copernicus.eu/
Tipo: Raster (NetCDF)
Resolución: 0.25° (~30km)
Cobertura: Global, 1979-presente
Acceso: Requiere cuenta gratuita + API key

Variables:
- Precipitación (mm/día)
- Temperatura 2m (°C)
- Humedad relativa (%)
- Velocidad del viento (m/s)
- Evapotranspiración

Aporte:
✅ Series temporales climáticas (40+ años)
✅ Correlación NDVI/LST/SMAP con clima
✅ Detección de cambios de uso de suelo
✅ Análisis 4D completo
```

### Dataset 14: OpenArchaeo (Sitios Históricos)
```
Fuente: OpenStreetMap + OpenArchaeo
URL: https://www.openstreetmap.org/
Tipo: Vectorial (GeoJSON/OSM)
Resolución: Puntual
Cobertura: Variable por región
Acceso: Descarga libre, API Overpass

Tags OSM:
- historic=archaeological_site
- historic=ruins
- historic=monument
- historic=castle
- historic=fort

Aporte:
✅ Contexto de sitios conocidos
✅ Caminos antiguos
✅ Patrones de asentamiento
✅ Validación de candidatos
```

### Dataset 15: MODIS/Landsat Extended (Series Temporales)
```
Fuente: NASA EarthData / USGS
URL: https://earthdata.nasa.gov/
Tipo: Raster (HDF/GeoTIFF)
Resolución: 250m-1km (MODIS), 30m (Landsat)
Cobertura: Global, 2000-presente (MODIS), 1984-presente (Landsat)
Acceso: Requiere Earthdata Login gratuito

Variables:
- NDVI histórico (mensual, 20+ años)
- LST histórico (mensual, 20+ años)
- EVI (Enhanced Vegetation Index)
- NDWI (Water Index)

Aporte:
✅ Series temporales extendidas
✅ Detección de cambios históricos
✅ Estacionalidad multi-anual
✅ Análisis de tendencias
```

---

## 2️⃣ ARQUITECTURA DE INTEGRACIÓN

### 2.1 Estructura de Conectores
```
backend/
├── satellite_connectors/
│   ├── hydrosheds_connector.py       # NUEVO
│   ├── usgs_geology_connector.py     # NUEVO
│   ├── era5_climate_connector.py     # NUEVO
│   ├── openarchaeo_connector.py      # NUEVO
│   └── modis_extended_connector.py   # NUEVO
├── data/
│   ├── hydrosheds/                   # Cache local
│   ├── geology/                      # Cache local
│   ├── climate/                      # Cache local
│   └── archaeology/                  # Cache local
└── environment_classifier.py         # ACTUALIZAR mapeo
```

### 2.2 Mapeo Ambiente → Instrumentos (ACTUALIZADO)
```python
# backend/environment_classifier.py

INSTRUMENT_MAPPING = {
    'DESERT': {
        'primary': [
            'ndvi_vegetation',
            'thermal_lst',
            'sar_backscatter',
            'surface_roughness',
            'soil_salinity',
            'elevation_dem',
            'usgs_geology',        # NUEVO
            'hydrosheds'           # NUEVO
        ],
        'secondary': [
            'sar_l_band',
            'smap_soil_moisture',
            'era5_climate',        # NUEVO
            'openarchaeo'          # NUEVO
        ]
    },
    
    'FOREST': {
        'primary': [
            'ndvi_vegetation',
            'sar_backscatter',
            'sar_l_band',
            'gedi_vegetation',
            'elevation_dem',
            'hydrosheds',          # NUEVO
            'modis_extended'       # NUEVO
        ],
        'secondary': [
            'thermal_lst',
            'smap_soil_moisture',
            'usgs_geology',        # NUEVO
            'era5_climate',        # NUEVO
            'openarchaeo'          # NUEVO
        ]
    },
    
    # ... más ambientes
}
```

---

## 3️⃣ IMPLEMENTACIÓN POR DATASET

### 3.1 HydroSHEDS Connector
```python
# backend/satellite_connectors/hydrosheds_connector.py

import geopandas as gpd
import rasterio
from pathlib import Path
import requests

class HydroSHEDSConnector:
    """Conector para datos hidrográficos HydroSHEDS"""
    
    BASE_URL = "https://data.hydrosheds.org/file/"
    CACHE_DIR = Path("backend/data/hydrosheds")
    
    def __init__(self):
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    def measure(self, lat, lon, bounds):
        """
        Medir características hidrográficas
        
        Returns:
            {
                'instrument_name': 'hydrosheds',
                'value': float,  # Densidad de drenaje
                'threshold': 0.5,
                'exceeds_threshold': bool,
                'confidence': float,
                'data_mode': 'real',
                'source': 'HydroSHEDS',
                'metadata': {
                    'rivers_count': int,
                    'drainage_density': float,
                    'flow_accumulation': float,
                    'nearest_river_distance': float
                }
            }
        """
        
        try:
            # 1. Descargar/cargar datos de la región
            rivers = self._get_rivers(bounds)
            basins = self._get_basins(bounds)
            flow_dir = self._get_flow_direction(bounds)
            
            # 2. Calcular métricas
            drainage_density = self._calculate_drainage_density(rivers, bounds)
            flow_accumulation = self._calculate_flow_accumulation(flow_dir, lat, lon)
            nearest_river = self._find_nearest_river(rivers, lat, lon)
            
            # 3. Score combinado
            value = (drainage_density * 0.4 + 
                    flow_accumulation * 0.3 + 
                    (1 / (nearest_river + 1)) * 0.3)
            
            return {
                'instrument_name': 'hydrosheds',
                'value': value,
                'threshold': 0.5,
                'exceeds_threshold': value > 0.5,
                'confidence': 0.85,
                'data_mode': 'real',
                'source': 'HydroSHEDS',
                'metadata': {
                    'rivers_count': len(rivers),
                    'drainage_density': drainage_density,
                    'flow_accumulation': flow_accumulation,
                    'nearest_river_distance': nearest_river
                }
            }
            
        except Exception as e:
            print(f"[HydroSHEDS] Error: {e}")
            return None
    
    def _get_rivers(self, bounds):
        """Obtener ríos en la región"""
        # Determinar tile de HydroSHEDS
        tile = self._get_tile_name(bounds)
        
        # Descargar si no existe
        local_path = self.CACHE_DIR / f"rivers_{tile}.shp"
        if not local_path.exists():
            self._download_tile(tile, 'rivers')
        
        # Cargar y filtrar
        rivers = gpd.read_file(local_path)
        rivers = rivers.cx[bounds['lon_min']:bounds['lon_max'], 
                            bounds['lat_min']:bounds['lat_max']]
        
        return rivers
    
    def _calculate_drainage_density(self, rivers, bounds):
        """Calcular densidad de drenaje (km/km²)"""
        total_length = rivers.geometry.length.sum()  # km
        area = self._calculate_area(bounds)  # km²
        return total_length / area if area > 0 else 0
```

### 3.2 USGS Geology Connector
```python
# backend/satellite_connectors/usgs_geology_connector.py

import geopandas as gpd
from pathlib import Path

class USGSGeologyConnector:
    """Conector para datos geológicos USGS"""
    
    BASE_URL = "https://mrdata.usgs.gov/geology/state/"
    CACHE_DIR = Path("backend/data/geology")
    
    def measure(self, lat, lon, bounds):
        """
        Medir características geológicas
        
        Returns:
            {
                'instrument_name': 'usgs_geology',
                'value': float,  # Score de anomalía geológica
                'threshold': 0.3,
                'exceeds_threshold': bool,
                'confidence': float,
                'data_mode': 'real',
                'source': 'USGS',
                'metadata': {
                    'lithology': str,
                    'age': str,
                    'soil_type': str,
                    'preservation_potential': float
                }
            }
        """
        
        try:
            # 1. Obtener datos geológicos del punto
            geology = self._get_geology_at_point(lat, lon)
            
            # 2. Calcular score de anomalía
            # Ciertos tipos de roca/suelo son más propensos a anomalías
            anomaly_score = self._calculate_geological_anomaly(geology)
            
            # 3. Potencial de preservación
            preservation = self._calculate_preservation_potential(geology)
            
            return {
                'instrument_name': 'usgs_geology',
                'value': anomaly_score,
                'threshold': 0.3,
                'exceeds_threshold': anomaly_score > 0.3,
                'confidence': 0.80,
                'data_mode': 'real',
                'source': 'USGS',
                'metadata': {
                    'lithology': geology.get('lithology', 'unknown'),
                    'age': geology.get('age', 'unknown'),
                    'soil_type': geology.get('soil_type', 'unknown'),
                    'preservation_potential': preservation
                }
            }
            
        except Exception as e:
            print(f"[USGS Geology] Error: {e}")
            return None
```

### 3.3 ERA5 Climate Connector
```python
# backend/satellite_connectors/era5_climate_connector.py

import cdsapi
import xarray as xr
from pathlib import Path

class ERA5ClimateConnector:
    """Conector para datos climáticos ERA5"""
    
    CACHE_DIR = Path("backend/data/climate")
    
    def __init__(self):
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        # Requiere API key en ~/.cdsapirc
        self.client = cdsapi.Client()
    
    def measure_timeseries(self, lat, lon, start_year=2010, end_year=2024):
        """
        Obtener series temporales climáticas
        
        Returns:
            {
                'instrument_name': 'era5_climate',
                'value': float,  # Anomalía climática
                'threshold': 0.2,
                'exceeds_threshold': bool,
                'confidence': float,
                'data_mode': 'real',
                'source': 'ERA5',
                'timeseries': {
                    'precipitation': array,
                    'temperature': array,
                    'humidity': array,
                    'dates': array
                }
            }
        """
        
        try:
            # 1. Descargar datos si no existen
            cache_file = self.CACHE_DIR / f"era5_{lat}_{lon}_{start_year}_{end_year}.nc"
            
            if not cache_file.exists():
                self._download_era5_data(lat, lon, start_year, end_year, cache_file)
            
            # 2. Cargar datos
            ds = xr.open_dataset(cache_file)
            
            # 3. Extraer series temporales
            precip = ds['tp'].values  # Total precipitation
            temp = ds['t2m'].values - 273.15  # Temperature (K → °C)
            humidity = ds['rh'].values  # Relative humidity
            
            # 4. Calcular anomalías
            precip_anomaly = self._calculate_anomaly(precip)
            temp_anomaly = self._calculate_anomaly(temp)
            
            # 5. Score combinado
            climate_anomaly = (precip_anomaly + temp_anomaly) / 2
            
            return {
                'instrument_name': 'era5_climate',
                'value': climate_anomaly,
                'threshold': 0.2,
                'exceeds_threshold': climate_anomaly > 0.2,
                'confidence': 0.90,
                'data_mode': 'real',
                'source': 'ERA5',
                'timeseries': {
                    'precipitation': precip.tolist(),
                    'temperature': temp.tolist(),
                    'humidity': humidity.tolist(),
                    'dates': ds['time'].values.tolist()
                }
            }
            
        except Exception as e:
            print(f"[ERA5] Error: {e}")
            return None
    
    def _download_era5_data(self, lat, lon, start_year, end_year, output_file):
        """Descargar datos ERA5 via CDS API"""
        self.client.retrieve(
            'reanalysis-era5-single-levels-monthly-means',
            {
                'product_type': 'monthly_averaged_reanalysis',
                'variable': [
                    'total_precipitation',
                    '2m_temperature',
                    'relative_humidity'
                ],
                'year': [str(y) for y in range(start_year, end_year + 1)],
                'month': [f'{m:02d}' for m in range(1, 13)],
                'time': '00:00',
                'area': [lat + 0.5, lon - 0.5, lat - 0.5, lon + 0.5],  # N, W, S, E
                'format': 'netcdf'
            },
            str(output_file)
        )
```

### 3.4 OpenArchaeo Connector
```python
# backend/satellite_connectors/openarchaeo_connector.py

import requests
from shapely.geometry import Point
import geopandas as gpd

class OpenArchaeoConnector:
    """Conector para sitios arqueológicos de OpenStreetMap"""
    
    OVERPASS_URL = "https://overpass-api.de/api/interpreter"
    
    def measure(self, lat, lon, radius_km=10):
        """
        Buscar sitios arqueológicos cercanos
        
        Returns:
            {
                'instrument_name': 'openarchaeo',
                'value': float,  # Densidad de sitios
                'threshold': 0.1,
                'exceeds_threshold': bool,
                'confidence': float,
                'data_mode': 'real',
                'source': 'OpenStreetMap',
                'metadata': {
                    'sites_count': int,
                    'nearest_site_distance': float,
                    'site_types': list,
                    'sites': list
                }
            }
        """
        
        try:
            # 1. Query Overpass API
            sites = self._query_archaeological_sites(lat, lon, radius_km)
            
            # 2. Calcular métricas
            sites_count = len(sites)
            area_km2 = 3.14159 * (radius_km ** 2)
            density = sites_count / area_km2
            
            # 3. Distancia al sitio más cercano
            if sites_count > 0:
                nearest_distance = min([
                    self._calculate_distance(lat, lon, s['lat'], s['lon'])
                    for s in sites
                ])
            else:
                nearest_distance = float('inf')
            
            return {
                'instrument_name': 'openarchaeo',
                'value': density,
                'threshold': 0.1,
                'exceeds_threshold': density > 0.1,
                'confidence': 0.70,  # Depende de completitud OSM
                'data_mode': 'real',
                'source': 'OpenStreetMap',
                'metadata': {
                    'sites_count': sites_count,
                    'nearest_site_distance': nearest_distance,
                    'site_types': list(set([s.get('type', 'unknown') for s in sites])),
                    'sites': sites[:10]  # Primeros 10
                }
            }
            
        except Exception as e:
            print(f"[OpenArchaeo] Error: {e}")
            return None
    
    def _query_archaeological_sites(self, lat, lon, radius_km):
        """Query Overpass API para sitios arqueológicos"""
        radius_m = radius_km * 1000
        
        query = f"""
        [out:json];
        (
          node["historic"="archaeological_site"](around:{radius_m},{lat},{lon});
          node["historic"="ruins"](around:{radius_m},{lat},{lon});
          node["historic"="monument"](around:{radius_m},{lat},{lon});
          way["historic"="archaeological_site"](around:{radius_m},{lat},{lon});
          way["historic"="ruins"](around:{radius_m},{lat},{lon});
        );
        out center;
        """
        
        response = requests.post(self.OVERPASS_URL, data={'data': query})
        data = response.json()
        
        sites = []
        for element in data.get('elements', []):
            sites.append({
                'id': element['id'],
                'type': element.get('tags', {}).get('historic', 'unknown'),
                'name': element.get('tags', {}).get('name', 'Unnamed'),
                'lat': element.get('lat') or element.get('center', {}).get('lat'),
                'lon': element.get('lon') or element.get('center', {}).get('lon')
            })
        
        return sites
```

### 3.5 MODIS Extended Connector
```python
# backend/satellite_connectors/modis_extended_connector.py

import requests
from datetime import datetime, timedelta
import numpy as np

class MODISExtendedConnector:
    """Conector para series temporales extendidas MODIS"""
    
    def measure_extended_timeseries(self, lat, lon, years=10):
        """
        Obtener series temporales extendidas de NDVI y LST
        
        Returns:
            {
                'instrument_name': 'modis_extended',
                'value': float,  # Tendencia temporal
                'threshold': 0.1,
                'exceeds_threshold': bool,
                'confidence': float,
                'data_mode': 'real',
                'source': 'MODIS',
                'timeseries': {
                    'ndvi': array,
                    'lst': array,
                    'dates': array,
                    'trend_ndvi': float,
                    'trend_lst': float,
                    'seasonality_ndvi': float,
                    'anomalies_count': int
                }
            }
        """
        
        try:
            # 1. Obtener datos históricos
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            
            ndvi_series = self._get_modis_ndvi_timeseries(lat, lon, start_date, end_date)
            lst_series = self._get_modis_lst_timeseries(lat, lon, start_date, end_date)
            
            # 2. Calcular tendencias
            trend_ndvi = self._calculate_trend(ndvi_series)
            trend_lst = self._calculate_trend(lst_series)
            
            # 3. Detectar anomalías
            anomalies = self._detect_anomalies(ndvi_series, lst_series)
            
            # 4. Score de cambio temporal
            temporal_change = abs(trend_ndvi) + abs(trend_lst)
            
            return {
                'instrument_name': 'modis_extended',
                'value': temporal_change,
                'threshold': 0.1,
                'exceeds_threshold': temporal_change > 0.1,
                'confidence': 0.85,
                'data_mode': 'real',
                'source': 'MODIS',
                'timeseries': {
                    'ndvi': ndvi_series.tolist(),
                    'lst': lst_series.tolist(),
                    'dates': self._generate_dates(start_date, end_date).tolist(),
                    'trend_ndvi': trend_ndvi,
                    'trend_lst': trend_lst,
                    'seasonality_ndvi': self._calculate_seasonality(ndvi_series),
                    'anomalies_count': len(anomalies)
                }
            }
            
        except Exception as e:
            print(f"[MODIS Extended] Error: {e}")
            return None
```

---


## 4️⃣ ROADMAP DE IMPLEMENTACIÓN

### Semana 1: HydroSHEDS + USGS Geology
```
Día 1-2: HydroSHEDS
✅ Implementar HydroSHEDSConnector
✅ Descargar tiles necesarios
✅ Calcular densidad de drenaje
✅ Tests unitarios

Día 3-4: USGS Geology
✅ Implementar USGSGeologyConnector
✅ Descargar mapas geológicos
✅ Calcular anomalía geológica
✅ Tests unitarios

Día 5: Integración
✅ Actualizar environment_classifier
✅ Integrar en pipeline
✅ Tests de integración
```

### Semana 2: ERA5 + OpenArchaeo + MODIS Extended
```
Día 1-2: ERA5 Climate
✅ Configurar CDS API
✅ Implementar ERA5ClimateConnector
✅ Descargar series temporales
✅ Tests unitarios

Día 3: OpenArchaeo
✅ Implementar OpenArchaeoConnector
✅ Query Overpass API
✅ Tests unitarios

Día 4: MODIS Extended
✅ Implementar MODISExtendedConnector
✅ Series temporales extendidas
✅ Tests unitarios

Día 5: Integración Final
✅ Actualizar pipeline completo
✅ Tests E2E con 15 instrumentos
✅ Documentación
```

---

## 5️⃣ CONFIGURACIÓN REQUERIDA

### 5.1 Cuentas y API Keys
```bash
# 1. Copernicus CDS (ERA5)
# Crear cuenta: https://cds.climate.copernicus.eu/
# Configurar ~/.cdsapirc:
cat > ~/.cdsapirc << EOF
url: https://cds.climate.copernicus.eu/api/v2
key: YOUR_UID:YOUR_API_KEY
EOF

# 2. NASA EarthData (MODIS Extended)
# Crear cuenta: https://urs.earthdata.nasa.gov/
# Configurar ~/.netrc:
cat > ~/.netrc << EOF
machine urs.earthdata.nasa.gov
login YOUR_USERNAME
password YOUR_PASSWORD
EOF
chmod 600 ~/.netrc

# 3. HydroSHEDS, USGS, OpenArchaeo
# No requieren API key (descarga directa)
```

### 5.2 Dependencias Python
```bash
# requirements-additional.txt

# HydroSHEDS
geopandas>=0.12.0
fiona>=1.9.0
pyproj>=3.4.0

# USGS Geology
shapely>=2.0.0

# ERA5 Climate
cdsapi>=0.6.0
xarray>=2023.0.0
netCDF4>=1.6.0

# OpenArchaeo
overpy>=0.6.0  # Overpass API wrapper

# MODIS Extended
h5py>=3.8.0
pyhdf>=0.10.0

# Instalar
pip install -r requirements-additional.txt
```

### 5.3 Estructura de Caché
```bash
backend/data/
├── hydrosheds/
│   ├── rivers/
│   ├── basins/
│   └── flow/
├── geology/
│   ├── lithology/
│   └── soil/
├── climate/
│   ├── era5/
│   └── cache/
├── archaeology/
│   └── osm_cache/
└── modis_extended/
    ├── ndvi/
    └── lst/
```

---

## 6️⃣ ACTUALIZACIÓN DEL PIPELINE

### 6.1 Nuevo Flujo de Análisis
```python
# backend/scientific_pipeline.py

async def analyze_with_extended_instruments(self, lat, lon, bounds):
    """
    Análisis con 15 instrumentos (10 originales + 5 nuevos)
    
    Fases:
    A. Clasificación de ambiente
    B. Selección de instrumentos (ahora 15 disponibles)
    C. Medición instrumental (paralela)
    D. Análisis estadístico
    D+. ESS
    E. Probabilidades
    F. Métricas separadas
    G. NUEVO: Análisis contextual (hidrografía, geología, clima, arqueología)
    H. NUEVO: Análisis temporal extendido
    """
    
    # Fase G: Análisis Contextual
    contextual_analysis = await self._analyze_context(
        lat, lon, bounds,
        hydro_data=measurements.get('hydrosheds'),
        geology_data=measurements.get('usgs_geology'),
        climate_data=measurements.get('era5_climate'),
        archaeology_data=measurements.get('openarchaeo')
    )
    
    # Fase H: Análisis Temporal Extendido
    temporal_analysis = await self._analyze_temporal_extended(
        lat, lon,
        modis_data=measurements.get('modis_extended'),
        climate_data=measurements.get('era5_climate')
    )
    
    return {
        'scientific_output': {...},
        'contextual_analysis': contextual_analysis,
        'temporal_analysis': temporal_analysis
    }
```

### 6.2 Análisis Contextual
```python
def _analyze_context(self, lat, lon, bounds, hydro_data, geology_data, 
                     climate_data, archaeology_data):
    """
    Análisis contextual con nuevos datasets
    
    Returns:
        {
            'hydrological_context': {
                'drainage_density': float,
                'nearest_river_km': float,
                'water_accessibility': str,
                'flood_risk': str
            },
            'geological_context': {
                'lithology': str,
                'soil_type': str,
                'preservation_potential': float,
                'geological_anomaly': float
            },
            'climatic_context': {
                'precipitation_annual_mm': float,
                'temperature_annual_c': float,
                'climate_trend': str,
                'climate_anomaly': float
            },
            'archaeological_context': {
                'known_sites_nearby': int,
                'nearest_site_km': float,
                'site_density': float,
                'historical_significance': str
            }
        }
    """
    
    context = {}
    
    # 1. Contexto hidrológico
    if hydro_data:
        context['hydrological_context'] = {
            'drainage_density': hydro_data['metadata']['drainage_density'],
            'nearest_river_km': hydro_data['metadata']['nearest_river_distance'],
            'water_accessibility': self._classify_water_access(
                hydro_data['metadata']['nearest_river_distance']
            ),
            'flood_risk': self._assess_flood_risk(
                hydro_data['metadata']['flow_accumulation']
            )
        }
    
    # 2. Contexto geológico
    if geology_data:
        context['geological_context'] = {
            'lithology': geology_data['metadata']['lithology'],
            'soil_type': geology_data['metadata']['soil_type'],
            'preservation_potential': geology_data['metadata']['preservation_potential'],
            'geological_anomaly': geology_data['value']
        }
    
    # 3. Contexto climático
    if climate_data:
        ts = climate_data['timeseries']
        context['climatic_context'] = {
            'precipitation_annual_mm': np.mean(ts['precipitation']) * 365,
            'temperature_annual_c': np.mean(ts['temperature']),
            'climate_trend': 'warming' if ts['temperature'][-1] > ts['temperature'][0] else 'cooling',
            'climate_anomaly': climate_data['value']
        }
    
    # 4. Contexto arqueológico
    if archaeology_data:
        context['archaeological_context'] = {
            'known_sites_nearby': archaeology_data['metadata']['sites_count'],
            'nearest_site_km': archaeology_data['metadata']['nearest_site_distance'],
            'site_density': archaeology_data['value'],
            'historical_significance': self._assess_historical_significance(
                archaeology_data['metadata']['sites_count'],
                archaeology_data['metadata']['site_types']
            )
        }
    
    return context
```

### 6.3 Análisis Temporal Extendido
```python
def _analyze_temporal_extended(self, lat, lon, modis_data, climate_data):
    """
    Análisis temporal extendido (10-20 años)
    
    Returns:
        {
            'ndvi_trend': float,
            'lst_trend': float,
            'precipitation_trend': float,
            'seasonality': {
                'ndvi_amplitude': float,
                'lst_amplitude': float,
                'precipitation_amplitude': float
            },
            'anomalies': {
                'ndvi_anomalies': int,
                'lst_anomalies': int,
                'climate_anomalies': int
            },
            'change_detection': {
                'land_use_change': bool,
                'deforestation': bool,
                'urbanization': bool,
                'agricultural_expansion': bool
            }
        }
    """
    
    analysis = {}
    
    if modis_data:
        ts = modis_data['timeseries']
        
        # Tendencias
        analysis['ndvi_trend'] = ts['trend_ndvi']
        analysis['lst_trend'] = ts['trend_lst']
        
        # Estacionalidad
        analysis['seasonality'] = {
            'ndvi_amplitude': ts['seasonality_ndvi'],
            'lst_amplitude': self._calculate_seasonality(ts['lst'])
        }
        
        # Anomalías
        analysis['anomalies'] = {
            'ndvi_anomalies': ts['anomalies_count'],
            'lst_anomalies': self._count_anomalies(ts['lst'])
        }
        
        # Detección de cambios
        analysis['change_detection'] = self._detect_land_use_changes(
            ts['ndvi'], ts['lst']
        )
    
    if climate_data:
        ts = climate_data['timeseries']
        
        # Tendencia de precipitación
        analysis['precipitation_trend'] = self._calculate_trend(ts['precipitation'])
        
        # Estacionalidad climática
        analysis['seasonality']['precipitation_amplitude'] = (
            np.max(ts['precipitation']) - np.min(ts['precipitation'])
        )
        
        # Anomalías climáticas
        analysis['anomalies']['climate_anomalies'] = self._count_anomalies(
            ts['precipitation']
        )
    
    return analysis
```

---

## 7️⃣ NUEVAS MÉTRICAS Y SCORES

### 7.1 Score Contextual
```python
def calculate_contextual_score(self, contextual_analysis):
    """
    Calcular score basado en contexto
    
    Componentes:
    - Hidrológico (25%): Acceso a agua, drenaje
    - Geológico (25%): Preservación, anomalías
    - Climático (25%): Estabilidad, tendencias
    - Arqueológico (25%): Sitios cercanos, densidad
    
    Returns: Score [0, 1]
    """
    
    scores = {}
    
    # 1. Score hidrológico
    if 'hydrological_context' in contextual_analysis:
        hydro = contextual_analysis['hydrological_context']
        scores['hydrological'] = (
            (1 / (hydro['nearest_river_km'] + 1)) * 0.5 +
            hydro['drainage_density'] * 0.3 +
            (1 if hydro['water_accessibility'] == 'high' else 0.5) * 0.2
        )
    
    # 2. Score geológico
    if 'geological_context' in contextual_analysis:
        geo = contextual_analysis['geological_context']
        scores['geological'] = (
            geo['preservation_potential'] * 0.6 +
            geo['geological_anomaly'] * 0.4
        )
    
    # 3. Score climático
    if 'climatic_context' in contextual_analysis:
        climate = contextual_analysis['climatic_context']
        scores['climatic'] = (
            (1 - climate['climate_anomaly']) * 0.7 +  # Estabilidad
            (1 if climate['climate_trend'] == 'stable' else 0.5) * 0.3
        )
    
    # 4. Score arqueológico
    if 'archaeological_context' in contextual_analysis:
        arch = contextual_analysis['archaeological_context']
        scores['archaeological'] = (
            min(arch['site_density'] * 10, 1.0) * 0.5 +
            (1 / (arch['nearest_site_km'] + 1)) * 0.3 +
            (1 if arch['historical_significance'] == 'high' else 0.5) * 0.2
        )
    
    # Score global contextual
    contextual_score = np.mean(list(scores.values()))
    
    return {
        'contextual_score': contextual_score,
        'components': scores
    }
```

### 7.2 Score Temporal
```python
def calculate_temporal_score(self, temporal_analysis):
    """
    Calcular score basado en análisis temporal
    
    Componentes:
    - Estabilidad (40%): Baja variabilidad = alto score
    - Tendencias (30%): Cambios significativos
    - Anomalías (30%): Eventos anómalos
    
    Returns: Score [0, 1]
    """
    
    # 1. Score de estabilidad (inverso de variabilidad)
    stability_score = 1 - abs(temporal_analysis.get('ndvi_trend', 0))
    
    # 2. Score de tendencias
    trend_score = (
        abs(temporal_analysis.get('ndvi_trend', 0)) * 0.4 +
        abs(temporal_analysis.get('lst_trend', 0)) * 0.3 +
        abs(temporal_analysis.get('precipitation_trend', 0)) * 0.3
    )
    
    # 3. Score de anomalías
    anomalies = temporal_analysis.get('anomalies', {})
    total_anomalies = sum(anomalies.values())
    anomaly_score = min(total_anomalies / 10, 1.0)  # Normalizar
    
    # Score global temporal
    temporal_score = (
        stability_score * 0.40 +
        trend_score * 0.30 +
        anomaly_score * 0.30
    )
    
    return {
        'temporal_score': temporal_score,
        'stability_score': stability_score,
        'trend_score': trend_score,
        'anomaly_score': anomaly_score
    }
```

### 7.3 Score Global Actualizado
```python
def calculate_global_score_v2(self, scientific_output, contextual_score, temporal_score):
    """
    Score global con 15 instrumentos
    
    Componentes:
    - Scientific Output (50%): Pipeline original
    - Contextual Score (25%): Nuevos datasets contextuales
    - Temporal Score (25%): Series temporales extendidas
    
    Returns: Score [0, 1]
    """
    
    # 1. Score científico original
    scientific_score = (
        scientific_output['anthropic_origin_probability'] * 0.4 +
        scientific_output['ess_score'] * 0.3 +
        (1 - scientific_output['instrumental_anomaly_probability']) * 0.3
    )
    
    # 2. Score global v2
    global_score_v2 = (
        scientific_score * 0.50 +
        contextual_score * 0.25 +
        temporal_score * 0.25
    )
    
    return {
        'global_score_v2': global_score_v2,
        'scientific_score': scientific_score,
        'contextual_score': contextual_score,
        'temporal_score': temporal_score,
        'classification': self._classify_score_v2(global_score_v2)
    }
```

---

## 8️⃣ TESTS Y VALIDACIÓN

### 8.1 Tests Unitarios
```python
# tests/test_additional_datasets.py

def test_hydrosheds_connector():
    """Test HydroSHEDS connector"""
    connector = HydroSHEDSConnector()
    result = connector.measure(
        lat=-13.163, lon=-72.545,
        bounds={'lat_min': -13.17, 'lat_max': -13.15,
                'lon_min': -72.55, 'lon_max': -72.54}
    )
    
    assert result is not None
    assert 'drainage_density' in result['metadata']
    assert result['value'] >= 0

def test_usgs_geology_connector():
    """Test USGS Geology connector"""
    connector = USGSGeologyConnector()
    result = connector.measure(lat=29.9792, lon=31.1342, bounds={...})
    
    assert result is not None
    assert 'lithology' in result['metadata']
    assert 'preservation_potential' in result['metadata']

def test_era5_climate_connector():
    """Test ERA5 Climate connector"""
    connector = ERA5ClimateConnector()
    result = connector.measure_timeseries(
        lat=40.7128, lon=-74.0060,
        start_year=2020, end_year=2024
    )
    
    assert result is not None
    assert 'timeseries' in result
    assert len(result['timeseries']['precipitation']) > 0

def test_openarchaeo_connector():
    """Test OpenArchaeo connector"""
    connector = OpenArchaeoConnector()
    result = connector.measure(lat=41.8902, lon=12.4922, radius_km=10)  # Roma
    
    assert result is not None
    assert result['metadata']['sites_count'] > 0

def test_modis_extended_connector():
    """Test MODIS Extended connector"""
    connector = MODISExtendedConnector()
    result = connector.measure_extended_timeseries(
        lat=0, lon=0, years=10
    )
    
    assert result is not None
    assert 'trend_ndvi' in result['timeseries']
```

### 8.2 Tests de Integración
```python
# tests/test_integration_15_instruments.py

async def test_full_pipeline_15_instruments():
    """Test pipeline completo con 15 instrumentos"""
    
    # Coordenadas de Machu Picchu
    result = await pipeline.analyze_with_extended_instruments(
        lat=-13.163, lon=-72.545,
        bounds={'lat_min': -13.17, 'lat_max': -13.15,
                'lon_min': -72.55, 'lon_max': -72.54}
    )
    
    # Verificar outputs
    assert 'scientific_output' in result
    assert 'contextual_analysis' in result
    assert 'temporal_analysis' in result
    
    # Verificar contexto hidrológico
    assert 'hydrological_context' in result['contextual_analysis']
    assert result['contextual_analysis']['hydrological_context']['drainage_density'] > 0
    
    # Verificar análisis temporal
    assert 'ndvi_trend' in result['temporal_analysis']
    assert 'seasonality' in result['temporal_analysis']
```

---

## 9️⃣ DOCUMENTACIÓN Y DEPLOYMENT

### 9.1 Actualizar Documentación
```markdown
# Archivos a actualizar:

1. INSTRUMENTOS_DISPONIBLES.md
   - Agregar 5 nuevos instrumentos
   - Total: 15 instrumentos

2. AUDITORIA_SISTEMA_COMPLETA_2026-01-27.md
   - Sección de instrumentos
   - Nuevas métricas

3. README.md
   - Requisitos de configuración
   - API keys necesarias

4. AGENTS.md
   - Nuevos conectores
   - Comandos de instalación
```

### 9.2 Deployment Checklist
```bash
# 1. Instalar dependencias
pip install -r requirements-additional.txt

# 2. Configurar API keys
# - Copernicus CDS
# - NASA EarthData

# 3. Descargar datos base
python scripts/download_hydrosheds_tiles.py
python scripts/download_geology_maps.py

# 4. Ejecutar tests
pytest tests/test_additional_datasets.py
pytest tests/test_integration_15_instruments.py

# 5. Actualizar BD
python scripts/update_instrument_mapping.py

# 6. Commit y push
git add .
git commit -m "feat: Integración de 5 datasets adicionales (15 instrumentos total)"
git push origin main
```

---

## 🔟 RESUMEN Y PRÓXIMOS PASOS

### Resumen
```
✅ 5 nuevos datasets identificados
✅ Conectores diseñados
✅ Pipeline actualizado
✅ Nuevas métricas definidas
✅ Tests planificados
✅ Roadmap de 2 semanas

Total instrumentos: 10 → 15 (+50%)
```

### Próximos Pasos Inmediatos
```
1. Crear cuentas en CDS y EarthData
2. Implementar HydroSHEDSConnector (Día 1)
3. Implementar USGSGeologyConnector (Día 2)
4. Tests unitarios (Día 3)
5. Continuar con ERA5, OpenArchaeo, MODIS Extended
```

### Beneficios Esperados
```
✅ Análisis contextual completo
✅ Series temporales extendidas (10-20 años)
✅ Correlaciones hidrología-vegetación-clima
✅ Validación con sitios conocidos
✅ Detección de cambios de uso de suelo
✅ Potencial de preservación arqueológica
✅ Score global más robusto
```

---

**Fecha**: 27 de Enero de 2026  
**Sistema**: ArcheoScope v2.2  
**Módulo**: Integración de Datasets Adicionales  
**Estado**: Plan completo ✅ | Listo para implementar 🚀
