# REPORTE DE FALLAS DE INSTRUMENTOS SATELITALES
**Fecha:** 2026-01-26 22:05:00  
**Sistema:** ArcheoScope v2.1  
**Análisis:** Diagnóstico completo de APIs satelitales

---

## RESUMEN EJECUTIVO

**Estado General:** 1/8 instrumentos funcionando correctamente (12.5%)

| Instrumento | Estado | Problema Principal |
|------------|--------|-------------------|
| NSIDC | ✅ FUNCIONANDO | Credenciales BD OK |
| ICESat-2 | ⚠️ CONFIGURADO | Devuelve inf/nan |
| Sentinel-2 | ❌ FALLA | stackstac DLL conflict |
| Sentinel-1 SAR | ❌ FALLA | Error lectura tiles COG |
| Landsat Thermal | ❌ FALLA | stackstac DLL conflict |
| MODIS LST | ⚠️ NO PROBADO | Credenciales OK |
| Copernicus Marine | ❌ NO IMPLEMENTADO | Módulo faltante |
| OpenTopography | ❌ NO IMPLEMENTADO | Módulo faltante |

---

## ANÁLISIS DETALLADO POR INSTRUMENTO

### 1. ✅ NSIDC (National Snow and Ice Data Center)

**Estado:** FUNCIONANDO  
**Credenciales:** Configuradas en BD  
**Última prueba:** 2026-01-26 21:50:00

**Detalles:**
- Conecta correctamente con credenciales desde BD
- Devuelve datos (modo DERIVED para regiones sin cobertura)
- Tiempo de respuesta: <5s
- Confianza: 70% (datos estimados)

**Ejemplo de respuesta:**
```json
{
  "value": 0.4,
  "data_mode": "DERIVED",
  "source": "NSIDC (estimated)",
  "confidence": 0.7,
  "unit": "fraction"
}
```

**Acción requerida:** Ninguna - funcionando correctamente

---

### 2. ⚠️ ICESat-2 (NASA Earthdata)

**Estado:** CONFIGURADO PERO DEVUELVE DATOS INVÁLIDOS  
**Credenciales:** Configuradas en BD  
**Última prueba:** 2026-01-26 21:50:00

**Problema:**
```
[FAIL] ICESat-2 devolvio valores invalidos (inf/nan)
```

**Causa raíz:**
- Credenciales funcionan correctamente
- Encuentra granules exitosamente
- Descarga datos exitosamente
- **PROBLEMA:** Procesamiento de datos H5 devuelve inf/nan

**Detalles técnicos:**
- Granules encontrados: ✅
- Descarga exitosa: ✅
- Lectura H5: ✅
- Cálculo de elevación: ❌ (inf/nan)

**Posibles causas:**
1. Datos de baja calidad en región específica
2. Error en cálculo de elevación promedio
3. Filtrado insuficiente de valores inválidos

**Código problemático:**
```python
# backend/satellite_connectors/icesat2_connector.py
elevation_mean = float(np.nanmean(elevations))  # Devuelve inf/nan
```

**Acción requerida:**
- Agregar validación de valores antes de calcular promedio
- Filtrar inf/nan explícitamente
- Retornar None si todos los valores son inválidos

**Fix sugerido:**
```python
# Filtrar valores válidos
valid_elevations = elevations[np.isfinite(elevations)]
if len(valid_elevations) == 0:
    return None
elevation_mean = float(np.mean(valid_elevations))
```

---

### 3. ❌ Sentinel-2 (Planetary Computer)

**Estado:** FALLA POR CONFLICTO DLL  
**Credenciales:** No requiere (acceso público)  
**Última prueba:** 2026-01-26 21:50:00

**Problema:**
```
Error fetching Sentinel-2 data: name 'stackstac' is not defined
```

**Causa raíz:**
- `stackstac` requiere `pyproj`
- `pyproj` tiene conflicto DLL con PostgreSQL
- Import de `stackstac` falla silenciosamente

**Detalles técnicos:**
```
ImportError: DLL load failed while importing _context: 
No se puede encontrar el módulo especificado.
```

**Intentos de solución:**
1. ✅ Configurar PROJ_LIB antes de imports
2. ✅ Importar stackstac después de configurar PROJ
3. ❌ Conflicto persiste (PostgreSQL vs rasterio)

**Solución implementada (parcial):**
- Lectura directa con `rasterio.windows`
- Sin dependencia de stackstac
- **Estado:** Implementado pero devuelve ventanas vacías

**Código actual:**
```python
# backend/satellite_connectors/planetary_computer.py
with rasterio.open(signed_href) as src:
    window = rasterio.windows.from_bounds(
        lon_min, lat_min, lon_max, lat_max,
        transform=src.transform
    )
    band_data = src.read(1, window=window)  # Devuelve array vacío
```

**Problema secundario:**
- Ventanas calculadas incorrectamente
- Transform no coincide con bbox
- Necesita reprojectar coordenadas

**Acción requerida:**
- Completar implementación sin stackstac
- Usar `rasterio.warp.transform_bounds` para reprojectar
- Validar que ventana contenga datos

---

### 4. ❌ Sentinel-1 SAR (Planetary Computer)

**Estado:** FALLA EN LECTURA DE TILES  
**Credenciales:** No requiere (acceso público)  
**Última prueba:** 2026-01-26 21:50:00

**Problema:**
```
[SAR] ERROR cargando bandas: Read failed. See previous exception for details.
rasterio.errors.RasterioIOError: TIFFReadEncodedTile() failed.
```

**Causa raíz:**
- Tiles COG (Cloud Optimized GeoTIFF) corruptos o incompletos
- Descarga parcial desde Planetary Computer
- Error de lectura en tiles específicos

**Detalles técnicos:**
```
TIFFReadEncodedTile() failed at X offset 24, Y offset 14
```

**Posibles causas:**
1. Timeout durante descarga de tiles
2. Tiles corruptos en servidor
3. Problema de red intermitente
4. Cache corrupto local

**Acción requerida:**
- Implementar retry con backoff exponencial
- Validar integridad de tiles antes de leer
- Usar overview de menor resolución como fallback
- Limpiar cache corrupto

**Fix sugerido:**
```python
# Usar overview de menor resolución
with rasterio.open(signed_href) as src:
    # Leer overview 1 (resolución reducida) en lugar de full resolution
    data = src.read(1, out_shape=(src.height // 2, src.width // 2))
```

---

### 5. ❌ Landsat Thermal (Planetary Computer)

**Estado:** FALLA POR stackstac  
**Credenciales:** No requiere (acceso público)  
**Última prueba:** 2026-01-26 21:50:00

**Problema:**
```
Error fetching Landsat thermal data: name 'stackstac' is not defined
```

**Causa raíz:** Mismo problema que Sentinel-2 (conflicto DLL)

**Acción requerida:** Misma solución que Sentinel-2

---

### 6. ⚠️ MODIS LST (NASA Earthdata)

**Estado:** NO PROBADO (credenciales configuradas)  
**Credenciales:** Configuradas en BD  
**Última prueba:** No ejecutado

**Acción requerida:** Ejecutar test para verificar funcionamiento

---

### 7. ❌ Copernicus Marine

**Estado:** MÓDULO NO IMPLEMENTADO  
**Credenciales:** Configuradas en BD  
**Última prueba:** 2026-01-26 21:50:00

**Problema:**
```
No module named 'satellite_connectors.copernicus_marine'
```

**Acción requerida:** Implementar módulo `copernicus_marine.py`

---

### 8. ❌ OpenTopography

**Estado:** MÓDULO NO IMPLEMENTADO  
**Credenciales:** Configuradas en BD  
**Última prueba:** 2026-01-26 21:50:00

**Problema:**
```
No module named 'satellite_connectors.opentopography'
```

**Acción requerida:** Implementar módulo `opentopography.py`

---

## IMPACTO EN ANÁLISIS ARQUEOLÓGICO

### Análisis Batch de 5 Candidatos

**Resultado:** 0/5 análisis exitosos

**Error común:**
```
HTTP 500: Out of range float values are not JSON compliant
```

**Causa:** ICESat-2 devuelve inf/nan → JSON serialization falla

**Regiones afectadas:**
1. Valeriana (México) - Selva maya
2. El Viandar Castle (España) - Bosque mediterráneo
3. Cedar Creek Earthworks (Canadá) - Llanura templada
4. Ocomtún (México) - Selva maya
5. Amazonian Earthworks (Brasil) - Selva amazónica

**Instrumentos intentados por región:**
- **Forest:** NDVI, SAR, Thermal (todos fallaron)
- **Mountain:** Elevation, Slope, SAR (todos fallaron)

---

## LOGROS DE LA SESIÓN

### ✅ Sistema de Credenciales Encriptadas

**Implementado:** `backend/credentials_manager.py`

**Características:**
- Encriptación AES-256 con PBKDF2
- Almacenamiento en PostgreSQL
- Migración automática desde .env
- Lectura transparente por conectores

**Credenciales migradas:**
- ✅ NASA Earthdata (username, password, token)
- ✅ Copernicus Marine (username, password)
- ✅ OpenTopography (api_key)

**Beneficios:**
- Centralización de credenciales
- Seguridad mejorada
- No depende de .env en runtime
- Fácil rotación de credenciales

### ✅ Clasificador de Ambientes Corregido

**Fix crítico:** Valeriana (México) ya no se detecta como océano

**Cambios:**
- Península de Yucatán correctamente identificada como tierra
- Golfo de México con lógica mejorada
- Ambiente `forest` detectado (60% confianza)

---

## PLAN DE ACCIÓN PRIORITARIO

### 🔴 CRÍTICO (Bloquea análisis)

1. **Fix inf/nan en ICESat-2**
   - Tiempo estimado: 30 min
   - Impacto: Desbloquea análisis batch
   - Prioridad: MÁXIMA

2. **Fix JSON serialization**
   - Agregar validación de valores antes de serializar
   - Convertir inf/nan a None
   - Tiempo estimado: 15 min

### 🟡 ALTA (Mejora capacidad)

3. **Completar Sentinel-2 sin stackstac**
   - Tiempo estimado: 2 horas
   - Impacto: +1 instrumento funcionando
   - Prioridad: ALTA

4. **Fix Sentinel-1 SAR tiles**
   - Implementar retry + fallback a overview
   - Tiempo estimado: 1 hora
   - Impacto: +1 instrumento funcionando

### 🟢 MEDIA (Expansión)

5. **Implementar Copernicus Marine**
   - Tiempo estimado: 3 horas
   - Impacto: +1 instrumento (hielo marino)

6. **Implementar OpenTopography**
   - Tiempo estimado: 3 horas
   - Impacto: +1 instrumento (DEM/LiDAR)

---

## RECOMENDACIONES

### Corto Plazo (Hoy)

1. **Arreglar inf/nan** → Desbloquea análisis batch
2. **Ejecutar análisis batch** → Validar sistema end-to-end
3. **Documentar resultados** → Baseline de funcionamiento

### Mediano Plazo (Esta Semana)

1. **Completar Sentinel-2** → Instrumento clave para vegetación
2. **Arreglar SAR** → Instrumento clave para estructuras
3. **Implementar MODIS** → Redundancia térmica

### Largo Plazo (Próximas Semanas)

1. **Implementar Copernicus** → Datos marinos/hielo
2. **Implementar OpenTopography** → DEM alta resolución
3. **Optimizar performance** → Cache, paralelización

---

## CONCLUSIÓN

**Estado actual:** Sistema parcialmente funcional

**Instrumentos operativos:** 1/8 (12.5%)

**Bloqueador principal:** Valores inf/nan rompen JSON serialization

**Próximo paso crítico:** Fix inf/nan en ICESat-2 (30 min)

**Tiempo estimado para sistema funcional:** 4-6 horas de trabajo

**Prioridad:** Desbloquear análisis batch antes de expandir instrumentos

---

**Generado:** 2026-01-26 22:05:00  
**Sistema:** ArcheoScope v2.1  
**Autor:** Kiro AI Assistant
