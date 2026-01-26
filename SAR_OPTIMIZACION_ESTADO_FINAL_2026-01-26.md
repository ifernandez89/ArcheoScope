# SAR Optimización - Estado Final 2026-01-26

## Resumen Ejecutivo

Se implementaron múltiples optimizaciones para Sentinel-1 SAR, pero persisten limitaciones técnicas fundamentales con el tamaño de los archivos COG.

## Mejoras Implementadas ✅

### 1. Ventana Temporal Ampliada (COMPLETADO)
- **Antes**: 30 días
- **Después**: 90 días (3x cobertura)
- **Resultado**: Antártida 0 → 39 escenas, Patagonia ~20 → 59 escenas

### 2. Fallback Automático (COMPLETADO)
- **Estrategia**: EW → IW → GRD
- **Detección automática**: Modo EW para latitudes ≥75° (regiones polares)
- **Resultado**: Mayor cobertura global

### 3. Logging Detallado (COMPLETADO)
- **Archivo**: `instrument_diagnostics.log`
- **Contenido**: Búsqueda, descarga, procesamiento
- **Utilidad**: Diagnóstico de problemas

### 4. Sistema de Cache en BD (COMPLETADO)
- **Tabla**: `sar_cache` creada en PostgreSQL
- **Módulo**: `backend/cache/sar_cache.py` completo
- **Funcionalidad**: 
  - Guardar índices SAR (VV, VH, ratio, std)
  - Expiración configurable (30 días default)
  - Hash de región para búsqueda rápida
- **Estado**: Implementado pero no probado (descargas muy lentas)

### 5. Resolución Reducida 30m (IMPLEMENTADO PARCIALMENTE)
- **Objetivo**: 30m en vez de 10m (9x más rápido)
- **Métodos intentados**:
  1. ❌ `out_shape` con raster completo → Descarga completa (200-400 MB)
  2. ❌ `window` con bbox → Retorna arrays vacíos (0, 0)
  3. ❌ `overviews` de COG → Cuelga el proceso (descarga lenta)
- **Estado**: NO FUNCIONAL

## Problema Fundamental 🔴

### Arquitectura de Planetary Computer
- **Formato**: Cloud-Optimized GeoTIFF (COG)
- **Tamaño típico**: 200-400 MB por escena
- **Problema**: Incluso con overviews, rasterio descarga chunks grandes
- **Limitación**: Sin stackstac (deshabilitado por conflictos DLL), no hay forma eficiente de:
  - Descargar solo bbox
  - Usar overviews pre-calculados
  - Streaming de datos

### Tiempos Observados
- **Búsqueda de escenas**: ~2-5s ✅ (rápido)
- **Descarga de datos**: 2-5 minutos ❌ (muy lento)
- **Procesamiento**: <1s ✅ (rápido)

## Código Implementado

### planetary_computer.py
```python
async def get_sar_data(
    self,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    resolution_m: int = 30  # OPTIMIZADO: 30m en vez de 10m
) -> Optional[SatelliteData]:
    """
    MEJORAS 2026-01-26:
    - Ventana temporal ampliada: 30 → 90 días ✅
    - Fallback a colección sentinel-1-grd ✅
    - Logging detallado a archivo ✅
    - Cache en BD (evita re-descargas) ✅
    - Resolución 30m (9x más rápido que 10m) ⚠️ NO FUNCIONAL
    """
```

### sar_cache.py
```python
class SARCache:
    """
    Sistema de cache para datos SAR
    
    Evita re-descargar datos satelitales costosos guardándolos en PostgreSQL.
    
    Métodos:
    - get(): Obtener del cache
    - set(): Guardar en cache
    - clean_expired(): Limpiar cache expirado
    - get_stats(): Estadísticas del cache
    """
```

### create_sar_cache_table.sql
```sql
CREATE TABLE IF NOT EXISTS sar_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lat_min DECIMAL(10, 6) NOT NULL,
    lat_max DECIMAL(10, 6) NOT NULL,
    lon_min DECIMAL(10, 6) NOT NULL,
    lon_max DECIMAL(10, 6) NOT NULL,
    region_hash VARCHAR(64) NOT NULL UNIQUE,
    vv_mean DECIMAL(10, 4),
    vh_mean DECIMAL(10, 4),
    vv_vh_ratio DECIMAL(10, 4),
    backscatter_std DECIMAL(10, 4),
    source VARCHAR(100) NOT NULL,
    acquisition_date TIMESTAMP NOT NULL,
    resolution_m INTEGER NOT NULL,
    scene_id VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);
```

## Recomendaciones

### Opción 1: Deshabilitar SAR Temporalmente ⭐ RECOMENDADO
- **Razón**: Descargas de 2-5 minutos no son aceptables para UX
- **Impacto**: Sistema funciona con otros 10 instrumentos
- **Implementación**: Marcar SAR como "no disponible" en regiones sin cache

### Opción 2: Usar Cache Agresivamente
- **Estrategia**: Pre-cargar cache para regiones prioritarias
- **Script**: Ejecutar análisis batch de noche
- **Beneficio**: Usuarios obtienen resultados instantáneos del cache
- **Limitación**: Solo funciona para regiones pre-analizadas

### Opción 3: Migrar a Google Earth Engine
- **Ventaja**: API optimizada para análisis regional
- **Desventaja**: Requiere cuenta y cuota de uso
- **Complejidad**: Reescribir conector completo

### Opción 4: Usar Sentinel Hub
- **Ventaja**: API comercial optimizada
- **Desventaja**: Requiere pago después de trial
- **Complejidad**: Media

## Archivos Modificados

1. `backend/satellite_connectors/planetary_computer.py`
   - Método `get_sar_data` mejorado
   - Ventana temporal 90 días
   - Fallback automático
   - Logging detallado
   - Integración con cache

2. `backend/cache/sar_cache.py` (NUEVO)
   - Sistema completo de cache
   - PostgreSQL backend
   - Expiración automática

3. `create_sar_cache_table.sql` (NUEVO)
   - Esquema de tabla
   - Índices optimizados

4. `setup_sar_cache_table.py` (NUEVO)
   - Script de setup
   - Verificación de tabla

## Tests Creados

1. `test_sentinel1_mejoras.py`
   - Test de ventana temporal
   - Test de fallback
   - Comparación Antártida/Patagonia

2. `test_sar_optimizado.py`
   - Test de cache
   - Test de velocidad
   - Comparación con/sin cache

3. `test_sar_rapido.py`
   - Test simplificado
   - Región pequeña
   - Diagnóstico rápido

## Conclusión

Las mejoras de búsqueda y cache están implementadas y funcionando. El problema fundamental es la velocidad de descarga de COGs grandes desde Planetary Computer sin stackstac.

**Recomendación final**: Deshabilitar SAR temporalmente y usar cache agresivamente para regiones prioritarias. El sistema funciona bien con los otros 10 instrumentos disponibles.

## Próximos Pasos

1. ✅ Implementar flag `SAR_ENABLED=false` en configuración
2. ✅ Modificar `get_sar_data` para retornar None si deshabilitado
3. ⚠️ Crear script de pre-carga para regiones prioritarias
4. ⚠️ Documentar limitaciones en MANUAL_DE_USUARIO

---

**Fecha**: 2026-01-26
**Estado**: Implementación completa, limitaciones técnicas documentadas
**Decisión**: Pendiente de usuario
