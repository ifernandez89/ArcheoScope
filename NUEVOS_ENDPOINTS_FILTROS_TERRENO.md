# 🗺️ Nuevos Endpoints: Filtros por Tipo de Terreno

## ✅ Implementación Completada

Se han agregado 3 nuevos endpoints para listar y filtrar sitios arqueológicos por tipo de terreno/ambiente, optimizados para selección de instrumentos de medición.

---

## 📡 Endpoints Disponibles

### 1. `/archaeological-sites/all` - Lista Completa con Filtros

**Método:** `GET`  
**Descripción:** Retorna lista paginada de todos los sitios con filtros opcionales

**Parámetros de consulta:**
- `limit` (opcional): Resultados por página (default: 100, max: 1000)
- `offset` (opcional): Desplazamiento para paginación (default: 0)
- `environment_type` (opcional): Filtrar por tipo de terreno
- `country` (opcional): Filtrar por país
- `site_type` (opcional): Filtrar por tipo de sitio

**Ejemplos:**
```bash
# Todos los sitios (primera página)
curl "http://localhost:8002/archaeological-sites/all"

# Sitios en desiertos (para instrumentos SAR/thermal)
curl "http://localhost:8002/archaeological-sites/all?environment_type=desert"

# Sitios en bosques (para LiDAR)
curl "http://localhost:8002/archaeological-sites/all?environment_type=forest&limit=50"

# Sitios en Italia
curl "http://localhost:8002/archaeological-sites/all?country=Italy&limit=200"

# Filtros combinados
curl "http://localhost:8002/archaeological-sites/all?environment_type=forest&country=France"

# Paginación (página 2)
curl "http://localhost:8002/archaeological-sites/all?limit=100&offset=100"
```

**Respuesta:**
```json
{
  "sites": [...],
  "total": 80457,
  "limit": 100,
  "offset": 0,
  "page": 1,
  "total_pages": 805,
  "filters_applied": {
    "environment_type": "desert",
    "country": "Egypt"
  }
}
```

---

### 2. `/archaeological-sites/by-environment/{environment_type}` - Por Ambiente

**Método:** `GET`  
**Descripción:** Endpoint especializado para filtrar por tipo de ambiente con recomendaciones de instrumentos

**Parámetros:**
- `environment_type` (requerido en URL): Tipo de ambiente
- `limit` (opcional): Número de resultados (default: 100)
- `offset` (opcional): Desplazamiento (default: 0)

**Tipos de ambiente válidos:**
- `desert` - Desiertos áridos
- `forest` - Bosques y selvas
- `glacier` - Glaciares de montaña
- `shallow_sea` - Aguas poco profundas
- `polar_ice` - Capas de hielo polares
- `mountain` - Regiones montañosas
- `grassland` - Praderas y estepas
- `wetland` - Humedales
- `urban` - Áreas urbanas
- `coastal` - Zonas costeras
- `unknown` - Ambiente no clasificado

**Ejemplos:**
```bash
# Sitios en desiertos
curl "http://localhost:8002/archaeological-sites/by-environment/desert"

# Sitios en bosques (para LiDAR)
curl "http://localhost:8002/archaeological-sites/by-environment/forest?limit=50"

# Sitios submarinos
curl "http://localhost:8002/archaeological-sites/by-environment/shallow_sea"

# Sitios en glaciares
curl "http://localhost:8002/archaeological-sites/by-environment/glacier"
```

**Respuesta:**
```json
{
  "sites": [...],
  "total": 1234,
  "environment_type": "forest",
  "environment_info": {
    "primary": ["LiDAR Aerotransportado", "PALSAR L-band", "GEDI 3D"],
    "secondary": ["Sentinel-1", "ICESat-2"],
    "characteristics": "Requiere penetración de vegetación, LiDAR esencial"
  },
  "recommended_instruments": {
    "primary": ["LiDAR Aerotransportado", "PALSAR L-band", "GEDI 3D"],
    "secondary": ["Sentinel-1", "ICESat-2"],
    "characteristics": "Requiere penetración de vegetación, LiDAR esencial"
  },
  "pagination": {
    "limit": 100,
    "offset": 0,
    "page": 1,
    "total_pages": 13
  }
}
```

---

### 3. `/archaeological-sites/environments/stats` - Estadísticas

**Método:** `GET`  
**Descripción:** Estadísticas de distribución de sitios por tipo de ambiente

**Ejemplos:**
```bash
curl "http://localhost:8002/archaeological-sites/environments/stats"
```

**Respuesta:**
```json
{
  "environment_stats": [
    {
      "environment_type": "UNKNOWN",
      "count": 80457,
      "percentage": 100.0
    }
  ],
  "total_sites": 80457,
  "total_environments": 1,
  "instrument_coverage": {
    "desert": {
      "coverage": "excellent",
      "instruments": 5,
      "primary": ["SAR", "Thermal", "Optical"]
    },
    "forest": {
      "coverage": "good",
      "instruments": 4,
      "primary": ["LiDAR", "L-band SAR"]
    }
  },
  "summary": {
    "most_common_environment": "UNKNOWN",
    "most_common_count": 80457,
    "environments_with_sites": 1
  }
}
```

---

## 🎯 Tipos de Ambiente e Instrumentos Recomendados

### Desert (Desiertos)
**Instrumentos primarios:**
- Sentinel-1 SAR
- Landsat Thermal
- MODIS NDVI

**Instrumentos secundarios:**
- OpenTopography DEM
- SMOS Salinity

**Características:**
- Alta visibilidad
- Mínima vegetación
- Excelente para detección térmica

**Ejemplos:** Giza, Petra, Nazca Lines

---

### Forest (Bosques y Selvas)
**Instrumentos primarios:**
- LiDAR Aerotransportado
- PALSAR L-band
- GEDI 3D

**Instrumentos secundarios:**
- Sentinel-1
- ICESat-2

**Características:**
- Requiere penetración de vegetación
- LiDAR esencial
- Sub-canopy structures

**Ejemplos:** Angkor Wat, Tikal, Amazonia

---

### Glacier (Glaciares)
**Instrumentos primarios:**
- ICESat-2
- SAR Interferométrico
- GPR (Ground Penetrating Radar)

**Instrumentos secundarios:**
- Sentinel-1
- Landsat

**Características:**
- Hielo
- Alta altitud
- Requiere radar penetrante

**Ejemplos:** Ötzi the Iceman, sitios alpinos

---

### Shallow Sea (Aguas Poco Profundas)
**Instrumentos primarios:**
- Sonar Multihaz
- Magnetometría
- Sub-bottom Profiler

**Instrumentos secundarios:**
- Optical Satellite
- Bathymetry

**Características:**
- Arqueología submarina
- <200m profundidad
- Requiere sonar

**Ejemplos:** Port Royal, Alejandría, Pavlopetri

---

### Mountain (Montañas)
**Instrumentos primarios:**
- OpenTopography DEM
- Optical Multispectral
- SAR

**Instrumentos secundarios:**
- ICESat-2
- GEDI

**Características:**
- Terrazas
- Pendientes pronunciadas
- Requiere DEM alta resolución

**Ejemplos:** Machu Picchu, sitios andinos

---

### Grassland (Praderas)
**Instrumentos primarios:**
- Multispectral
- Crop Marks
- Geofísica

**Instrumentos secundarios:**
- SAR
- Thermal

**Características:**
- Vegetación baja
- Excelente para crop marks
- Buena visibilidad

**Ejemplos:** Stonehenge, sitios de las estepas

---

## 📊 Estado Actual de la Base de Datos

**Total de sitios:** 80,457

**Distribución por ambiente:**
- UNKNOWN: 80,457 sitios (100%)

**Nota:** Todos los sitios actualmente tienen `environment_type = UNKNOWN` porque no se clasificaron durante la migración inicial. Se requiere clasificación automática o manual.

---

## 🔄 Próximos Pasos: Clasificación de Ambientes

### Opción 1: Clasificación Automática por Coordenadas

Usar bases de datos geográficas para clasificar automáticamente:

```python
# Script de clasificación automática
python scripts/classify_environments.py
```

**Fuentes de datos:**
- Biomas mundiales (WWF)
- Elevación (SRTM/ASTER)
- Cobertura terrestre (ESA CCI)
- Cuerpos de agua (OpenStreetMap)

### Opción 2: Clasificación por Wikidata

Durante el enriquecimiento con Wikidata, extraer información de ambiente:

```python
# Enriquecimiento incluye clasificación
python scripts/enrich_archaeological_data.py
```

### Opción 3: Clasificación Manual

Para sitios importantes, clasificación manual por expertos.

---

## 🧪 Testing

**Script de prueba:**
```bash
python test_new_endpoints.py
```

**Resultados:**
```
✅ PASS - Todos los sitios
✅ PASS - Filtro por ambiente
✅ PASS - Endpoint por ambiente
✅ PASS - Estadísticas de ambientes
✅ PASS - Filtro por país
✅ PASS - Filtros combinados

Resultado: 6/6 tests pasados
🎉 ¡TODOS LOS TESTS PASARON!
```

---

## 📚 Documentación API (Swagger)

Los nuevos endpoints están documentados en Swagger UI:

```
http://localhost:8002/docs
```

**Tags:**
- `Database` - Todos los endpoints de base de datos

---

## 💡 Casos de Uso

### Caso 1: Seleccionar sitios para campaña LiDAR
```bash
# Obtener sitios en bosques (requieren LiDAR)
curl "http://localhost:8002/archaeological-sites/by-environment/forest?limit=100"
```

### Caso 2: Planificar mediciones SAR
```bash
# Obtener sitios en desiertos y humedales
curl "http://localhost:8002/archaeological-sites/all?environment_type=desert"
curl "http://localhost:8002/archaeological-sites/all?environment_type=wetland"
```

### Caso 3: Arqueología submarina
```bash
# Obtener sitios en aguas poco profundas
curl "http://localhost:8002/archaeological-sites/by-environment/shallow_sea"
```

### Caso 4: Análisis por país
```bash
# Sitios en Italia con paginación
curl "http://localhost:8002/archaeological-sites/all?country=Italy&limit=200"
```

### Caso 5: Estadísticas generales
```bash
# Ver distribución de ambientes
curl "http://localhost:8002/archaeological-sites/environments/stats"
```

---

## 🔧 Archivos Modificados/Creados

### Modificados:
- `backend/database.py` - Nuevos métodos de consulta
- `backend/api/main.py` - 3 nuevos endpoints

### Creados:
- `test_new_endpoints.py` - Tests de endpoints
- `check_environment_values.py` - Verificación de valores
- `NUEVOS_ENDPOINTS_FILTROS_TERRENO.md` - Esta documentación

---

## ✅ Resumen

**Endpoints agregados:** 3  
**Tests pasados:** 6/6  
**Estado:** ✅ Completamente funcional  
**Próximo paso:** Clasificar ambientes de los 80,457 sitios

---

**Fecha:** 2026-01-25  
**Versión:** 1.0  
**Estado:** Producción
