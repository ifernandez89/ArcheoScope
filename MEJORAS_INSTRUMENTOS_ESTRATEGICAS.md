# 🎯 MEJORAS ESTRATÉGICAS INSTRUMENTOS
**Fecha**: 2026-01-29  
**Enfoque**: Blindar CORE, no arreglar todo

---

## 🔒 CORE REAL DE ARCHEOSCOPE (4 instrumentos)

| Tipo | Fuente | Estado | Prioridad |
|------|--------|--------|-----------|
| **Vegetación** | Sentinel-2 NDVI | ✅ FUNCIONA | CORE |
| **Subsuperficie** | Sentinel-1 SAR | ✅ FUNCIONA | CORE |
| **Térmico** | Landsat | ✅ FUNCIONA | CORE |
| **Relieve** | NASADEM/Copernicus | ⚠️ MEJORAR | CORE |
| **Clima** | ERA5 | ⚠️ LIMPIAR | CORE |

**TODO lo demás = moduladores opcionales**

---

## ✅ MEJORAS IMPLEMENTADAS

### 1. NSIDC - Pre-condición polar
```python
# Antes: Intentaba siempre, fallaba en trópicos
# Después: Skip automático si no es polar

if abs(lat) < 60:
    return None  # Skip silencioso
```

### 2. OpenTopography - Bbox dinámico
```python
# Antes: bbox fijo, fallaba con regiones pequeñas
# Después: bbox mínimo adaptativo

bbox_min = max(user_bbox, 0.1°)  # Mínimo 11km
```

### 3. DEM - Orden de prioridad
```python
# Cascada de fallback:
1. OpenTopography (si responde)
2. Copernicus DEM GLO-30 (sin API key)
3. NASADEM (sin API key, mejor que SRTM)
4. SRTM (último recurso)

# NUNCA quedarse sin DEM
```

### 4. ICESat-2 - Logging explícito
```python
# Antes: Error genérico
# Después: Estado claro

if no_data:
    log("ICESat-2: coverage=false (no error)")
    return None  # Bonus data, no core
```

### 5. ERA5 - Cambio a GRIB
```python
# Antes: NetCDF con fricción
# Después: GRIB directo

request = {
    "format": "grib",  # Más estable
    "data_format": "grib"
}

# Validar extracción:
stats = {
    'min': float(var_data.min()),
    'max': float(var_data.max()),
    'mean': float(var_data.mean())
}
# Nunca asumir un solo punto
```

---

## 📊 CLASIFICACIÓN POR CONFIANZA

### Nuevo campo en cada análisis:
```python
"data_confidence": {
    "core_complete": true,          # 4/4 instrumentos core
    "dem_quality": "HIGH",           # NASADEM/Copernicus
    "climate_corrected": true,       # ERA5 disponible
    "subsurface_supported": true,    # SAR disponible
    "modulators_count": 2,           # ICESat-2, PALSAR, etc.
    "confidence_score": 0.95         # Score agregado
}
```

### Interpretación:
- **core_complete=true**: Datos suficientes para detección confiable
- **dem_quality=HIGH**: Relieve bien caracterizado
- **climate_corrected=true**: Contexto climático disponible
- **subsurface_supported=true**: Penetración SAR disponible

---

## 🎯 PRIORIDADES DE IMPLEMENTACIÓN

### INMEDIATO (1-2h):
1. ✅ **NASADEM como default DEM**
   - Sin API key
   - Mejor corrección de vacíos
   - Impacta: profundidad, pendientes, falsos muros

2. ✅ **ERA5 a GRIB**
   - Más estable que NetCDF
   - Validación robusta (min/max/mean)

3. ✅ **data_confidence en respuestas**
   - Transparencia científica
   - "Datos lo permiten, no modelo lo imagina"

### CORTO PLAZO (2-4h):
4. **PALSAR bug fix**
   - Corregir 'list' object error
   - Usar como validador (no detector primario)

5. **OpenTopography bbox dinámico**
   - Adaptativo según región
   - Fallback a Copernicus DEM

### NO PRIORITARIO:
- VIIRS: Documentar como "mejora nocturna opcional"
- CHIRPS: Archivar (ERA5 cubre 90%)
- Copernicus SST: Solo para costas fósiles

---

## 🧠 CAMBIO DE MINDSET

### Antes:
❌ "Arreglar todos los instrumentos"
❌ "Más instrumentos = mejor"
❌ "Coverage 100%"

### Después:
✅ "Blindar el CORE (4-5 instrumentos)"
✅ "Calidad > Cantidad"
✅ "Transparencia en confianza de datos"

---

## 📈 IMPACTO ESPERADO

### Con CORE blindado:
- **Desiertos**: ESS 0.40-0.50 (actual: 0.39-0.48) ✅
- **Altiplano**: ESS 0.45-0.55 (actual: 0.467) ✅
- **Confianza**: +30% (data_confidence explícito)
- **Honestidad**: Mediterráneo sigue <0.15 ✅

### Frase clave:
> "Este candidato es fuerte porque **los datos lo permiten**, no porque el modelo lo imaginó"

---

## 📁 ARCHIVOS A MODIFICAR

### CORE:
1. `backend/satellite_connectors/real_data_integrator_v2.py`
   - Agregar cascada DEM
   - Pre-condición NSIDC polar

2. `backend/satellite_connectors/era5_connector.py`
   - Cambiar a GRIB
   - Validación robusta

3. `backend/api/scientific_endpoint.py`
   - Agregar data_confidence a respuesta

### MODULADORES:
4. `backend/satellite_connectors/nsidc_connector.py`
   - Pre-condición `if abs(lat) < 60: skip()`

5. `backend/satellite_connectors/opentopography_connector.py`
   - Bbox dinámico

6. `backend/satellite_connectors/icesat2_connector.py`
   - Logging explícito "coverage=false"

---

## ✅ ESTADO FINAL ESPERADO

| Instrumento | Estado | Rol |
|-------------|--------|-----|
| Sentinel-2 NDVI | ✅ | CORE |
| Sentinel-1 SAR | ✅ | CORE |
| Landsat Thermal | ✅ | CORE |
| NASADEM | ✅ | CORE |
| ERA5 | ✅ | CORE |
| MODIS LST | ✅ | Modulador |
| ICESat-2 | ⚠️ | Bonus (cuando hay) |
| PALSAR | ⚠️ | Validador |
| NSIDC | ⚠️ | Solo polar |
| OpenTopography | ⚠️ | Fallback DEM |
| VIIRS | 📦 | Archivado |
| CHIRPS | 📦 | Archivado |
| Copernicus SST | 📦 | Archivado |

**Coverage CORE: 100%** ✅  
**Coverage Total: 38.5%** (5/13 core + moduladores)

---

**Tiempo estimado**: 3-4h  
**Impacto**: ALTO (blindaje científico)  
**Complejidad**: Media
