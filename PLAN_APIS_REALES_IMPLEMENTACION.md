# 🚀 Plan de Implementación: APIs Reales en ArcheoScope

**Fecha:** 26 de Enero de 2026  
**Objetivo:** Reemplazar TODAS las simulaciones por APIs gratuitas reales

---

## 📊 AUDITORÍA RÁPIDA

### ✅ YA IMPLEMENTADO (NO INTEGRADO)
- **Sentinel-2** (Multispectral 10m) - Microsoft Planetary Computer
- **Sentinel-1** (SAR 10m) - Microsoft Planetary Computer  
- **Landsat** (Térmico 30m) - Microsoft Planetary Computer

**Problema:** Implementado en `backend/satellite_connectors/planetary_computer.py` pero NO usado en el flujo principal

### ❌ SIMULADO (NECESITA REEMPLAZO)
1. ICESat-2 (Elevación/Hielo) - usa hashes determinísticos
2. MODIS (Térmico regional) - usa np.random
3. OpenTopography (DEM) - usa np.random
4. PALSAR (L-band penetración) - usa np.random
5. SMOS (Salinidad) - usa np.random
6. SMAP (Humedad) - usa np.random
7. IRIS Seismic (Subsuperficie) - usa np.random

### 🆕 NO IMPLEMENTADO (PROPUESTA USUARIO)
8. Copernicus Marine (Hielo marino + series temporales)
9. NSIDC (Hielo histórico 1970s-presente)

---

## 🎯 PLAN DE ACCIÓN (4 SEMANAS)

### SEMANA 1: APIs Críticas

#### Día 1-2: ICESat-2 (Elevación Real)
```bash
pip install earthaccess h5py
```
```python
# backend/satellite_connectors/icesat2_connector.py
class ICESat2Connector:
    def get_atl06_data(lat, lon):  # Land Ice Height
        # NASA Earthdata API
        pass
```
**Beneficio:** Precisión centimétrica en hielo

#### Día 3-4: Copernicus Marine (Hielo Marino)
```bash
pip install copernicusmarine
```
```python
# backend/satellite_connectors/copernicus_marine_connector.py
class CopernicusMarineConnector:
    def get_sea_ice_timeseries(lat, lon, start, end):
        # Series temporales 1993-2023+
        pass
```
**Beneficio:** Series temporales reales de hielo

#### Día 5: OpenTopography (DEM Real)
```bash
pip install requests
```
```python
# backend/satellite_connectors/opentopography_connector.py
class OpenTopographyConnector:
    def get_dem(lat_min, lat_max, lon_min, lon_max):
        # SRTM 30m / ALOS 30m
        pass
```
**Beneficio:** Microtopografía real

---

### SEMANA 2: Integración Planetary Computer

#### Día 1-3: Integrar en Flujo Principal
```python
# backend/core_anomaly_detector.py
def _measure_instrument_real(self, indicator_name, bounds):
    if indicator_name == "sentinel_2_ndvi":
        pc = PlanetaryComputerConnector()
        data = pc.get_multispectral_data(bounds)
        return data.indices['ndvi']
    
    elif indicator_name == "sentinel_1_sar":
        pc = PlanetaryComputerConnector()
        data = pc.get_sar_data(bounds)
        return data.indices['vv_mean']
    
    elif indicator_name == "landsat_thermal":
        pc = PlanetaryComputerConnector()
        data = pc.get_thermal_data(bounds)
        return data.indices['lst_mean']
```

#### Día 4-5: Sistema de Caché
```python
# backend/satellite_connectors/cache_manager.py
class SatelliteCache:
    def get_or_fetch(self, connector, params, ttl_days=30):
        # Cachear datos por 30 días
        # Evitar descargas repetidas
        pass
```

---

### SEMANA 3: APIs Complementarias

#### MODIS (Térmico Regional)
```bash
pip install appeears
```

#### PALSAR (L-band)
```bash
pip install asf_search
```

#### SMOS/SMAP (Humedad)
```bash
pip install cdsapi
```

---

### SEMANA 4: Testing y Documentación

- Probar con 80,512 sitios de la BD
- Comparar resultados reales vs simulados
- Documentar mejoras
- Actualizar README

---

## 🔑 API KEYS NECESARIAS (TODAS GRATUITAS)

### 1. NASA Earthdata
- URL: https://urs.earthdata.nasa.gov/
- Uso: ICESat-2, MODIS, SMAP
- Variables: `EARTHDATA_USERNAME`, `EARTHDATA_PASSWORD`

### 2. Copernicus Marine
- URL: https://marine.copernicus.eu/
- Uso: Hielo marino
- Variables: `COPERNICUS_MARINE_USERNAME`, `COPERNICUS_MARINE_PASSWORD`

### 3. OpenTopography
- URL: https://portal.opentopography.org/
- Uso: DEM
- Variable: `OPENTOPOGRAPHY_API_KEY`

### 4. Copernicus CDS
- URL: https://cds.climate.copernicus.eu/
- Uso: SMOS
- Variable: `CDS_API_KEY`

---

## 📦 DEPENDENCIAS

```bash
# requirements-satellite-real.txt
earthaccess>=0.8.0          # NASA Earthdata
h5py>=3.10.0                # HDF5 para ICESat-2
copernicusmarine>=1.0.0     # Copernicus Marine
appeears>=1.0.0             # MODIS
cdsapi>=0.6.0               # SMOS
asf_search>=6.0.0           # PALSAR
```

---

## ✅ RESULTADO ESPERADO

### Antes (Actual)
- 3/12 instrumentos con APIs reales (25%)
- 7/12 simulados (58%)
- 2/12 no implementados (17%)

### Después (Meta)
- 12/12 instrumentos con APIs reales (100%)
- 0/12 simulados (0%)
- Sistema científicamente riguroso
- Publicable en journals peer-reviewed

---

## 🚀 EMPEZAR AHORA

### Paso 1: Registrar Cuentas (30 min)
```bash
# 1. NASA Earthdata
https://urs.earthdata.nasa.gov/users/new

# 2. Copernicus Marine
https://marine.copernicus.eu/register

# 3. OpenTopography
https://portal.opentopography.org/newUser

# 4. Copernicus CDS
https://cds.climate.copernicus.eu/user/register
```

### Paso 2: Configurar .env.local
```bash
# NASA Earthdata
EARTHDATA_USERNAME=tu_usuario
EARTHDATA_PASSWORD=tu_password

# Copernicus Marine
COPERNICUS_MARINE_USERNAME=tu_usuario
COPERNICUS_MARINE_PASSWORD=tu_password

# OpenTopography
OPENTOPOGRAPHY_API_KEY=tu_api_key

# Copernicus CDS
CDS_API_KEY=tu_api_key
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements-satellite-real.txt
```

### Paso 4: Implementar Primer Conector
```bash
# Empezar con ICESat-2 (crítico para hielo)
python backend/satellite_connectors/icesat2_connector.py
```

---

## 📊 MÉTRICAS DE ÉXITO

- [ ] 100% instrumentos con APIs reales
- [ ] 0% simulaciones
- [ ] Caché funcionando (reduce llamadas API)
- [ ] Tests pasando con datos reales
- [ ] Documentación actualizada
- [ ] Sistema listo para publicación académica

---

**Tiempo Total:** 4 semanas  
**Costo:** $0 (todas las APIs son gratuitas)  
**Beneficio:** Sistema científicamente riguroso y publicable

**¿Empezamos con ICESat-2 y Copernicus Marine?**
