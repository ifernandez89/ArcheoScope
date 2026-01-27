# ESTRATEGIA: INSTRUMENT CONTRACT
**Fecha:** 2026-01-26 22:15:00  
**Prioridad:** CRÍTICA  
**Impacto:** Desbloquea sistema completo

---

## EL PROBLEMA REAL

❌ **NO es** que ICESat-2 devuelva inf/nan  
✅ **ES** que no tenemos un contrato robusto de salida

### Síntomas Actuales

```python
# ❌ ANTES: Instrumentos devuelven floats crudos
elevation = 1234.56  # ¿De dónde viene? ¿Es confiable? ¿Qué pasa si es inf?
```

**Consecuencias:**
- Sistema crashea con inf/nan
- No hay trazabilidad de calidad
- Decisiones binarias "sirve/no sirve"
- Imposible razonar con ausencia de datos

---

## LA SOLUCIÓN: INSTRUMENT CONTRACT

### Contrato Estándar

```python
@dataclass
class InstrumentMeasurement:
    # Identificación
    instrument_name: str
    measurement_type: str
    
    # Valor medido
    value: Optional[float]              # None si no hay dato válido
    unit: str
    
    # Estado y calidad
    status: InstrumentStatus            # OK | NO_DATA | INVALID | DERIVED | ERROR
    confidence: float                   # 0.0 - 1.0
    
    # Contexto científico
    reason: Optional[str]               # Por qué este estado
    quality_flags: Dict[str, Any]       # Flags específicos del instrumento
    
    # Metadatos
    source: str
    acquisition_date: Optional[str]
    processing_notes: Optional[str]
```

### Estados Posibles

| Estado | Significado | value | Usable |
|--------|-------------|-------|--------|
| `OK` | Medición exitosa | float | ✅ Sí |
| `NO_DATA` | Sin datos disponibles | None | ❌ No |
| `INVALID` | Datos inválidos (inf/nan) | None | ❌ No |
| `LOW_QUALITY` | Baja calidad (nubes, flags) | None | ⚠️ Depende |
| `DERIVED` | Estimado/derivado | float | ⚠️ Con precaución |
| `TIMEOUT` | Timeout en API | None | ❌ No |
| `ERROR` | Error técnico | None | ❌ No |

---

## BENEFICIOS INMEDIATOS

### 1. ✅ Robustez ante Datos Reales

```python
# ✅ DESPUÉS: Contrato robusto
measurement = InstrumentMeasurement(
    instrument_name="ICESat-2",
    value=None,
    status=InstrumentStatus.INVALID,
    reason="all_values_nan - insufficient valid points after quality filtering",
    confidence=0.0
)

# Sistema NO crashea
# Razón documentada
# Decisión arqueológica informada
```

### 2. ✅ Trazabilidad Científica

Cada medición incluye:
- **Fuente:** De dónde viene el dato
- **Calidad:** Qué tan confiable es
- **Razón:** Por qué este estado
- **Flags:** Detalles técnicos

### 3. ✅ Razonamiento con Ausencia

```python
# Ausencia de datos TAMBIÉN es información
if measurement.status == InstrumentStatus.NO_DATA:
    if measurement.reason == "cloud_cover_high":
        # Región con nubes frecuentes → posible selva
        archaeological_context.add_evidence("high_precipitation_zone")
```

### 4. ✅ JSON Serialization Garantizada

```python
# NUNCA más "Out of range float values"
measurement.to_dict()  # Siempre serializable
```

---

## IMPLEMENTACIÓN POR FASES

### FASE 1: Contrato Base (✅ COMPLETADO)

- [x] Definir `InstrumentMeasurement` dataclass
- [x] Definir `InstrumentStatus` enum
- [x] Factories para casos comunes
- [x] Validación automática
- [x] Ejemplos de uso

**Archivo:** `backend/instrument_contract.py`

### FASE 2: Migrar ICESat-2 (30 min)

**Antes:**
```python
# ❌ Devuelve float crudo o None
elevation_mean = float(np.nanmean(elevations))  # Puede ser inf/nan
return elevation_mean
```

**Después:**
```python
# ✅ Devuelve InstrumentMeasurement
# Filtrar por quality flags
valid_elevations = elevations[
    (quality_flags == 0) & 
    np.isfinite(elevations)
]

if len(valid_elevations) < 10:  # Mínimo 10 puntos
    return InstrumentMeasurement.create_invalid(
        instrument_name="ICESat-2",
        measurement_type="elevation",
        reason=f"insufficient_valid_points - only {len(valid_elevations)} points after quality filtering",
        source="NASA Earthdata",
        unit="meters"
    )

elevation_mean = float(np.mean(valid_elevations))
return InstrumentMeasurement(
    instrument_name="ICESat-2",
    measurement_type="elevation",
    value=elevation_mean,
    unit="meters",
    status=InstrumentStatus.OK,
    confidence=0.95,
    reason=None,
    quality_flags={'valid_points': len(valid_elevations)},
    source="NASA Earthdata",
    acquisition_date=acquisition_date,
    processing_notes="Filtered by quality flags and finite values"
)
```

### FASE 3: Migrar NSIDC (15 min)

**Cambio clave:** Usar `InstrumentStatus.DERIVED` para datos estimados

```python
return InstrumentMeasurement.create_derived(
    instrument_name="NSIDC",
    measurement_type="sea_ice_concentration",
    value=0.4,
    unit="fraction",
    confidence=0.7,
    derivation_method="Location-based seasonal model",
    source="NSIDC (estimated)"
)
```

### FASE 4: Migrar Sentinel-2 (20 min)

Estados posibles:
- `NO_DATA`: No scenes found
- `LOW_QUALITY`: Cloud cover > 80%
- `OK`: NDVI calculado exitosamente

### FASE 5: Migrar Sentinel-1 SAR (20 min)

Estados posibles:
- `ERROR`: TIFFReadEncodedTile failed
- `OK`: Backscatter calculado (con retry exitoso)

### FASE 6: Actualizar Core Detector (30 min)

```python
# Antes: Espera floats
measurements = [1.2, 3.4, None, 5.6]  # ❌ Frágil

# Después: Espera InstrumentMeasurement
measurements = [m1, m2, m3, m4]

# Filtrar solo usables
usable = [m for m in measurements if m.is_usable()]

# Filtrar solo alta calidad
high_quality = [m for m in measurements if m.is_high_quality()]

# Razonar con ausencia
no_data_count = sum(1 for m in measurements if m.status == InstrumentStatus.NO_DATA)
if no_data_count > 3:
    # Región con poca cobertura satelital → posible zona remota
    pass
```

---

## DEFENSA CIENTÍFICA

### Antes (Indefendible)

**Arqueólogo:** "¿Por qué descartaste este sitio?"  
**Sistema:** "ICESat-2 devolvió NaN"  
**Arqueólogo:** "¿Y eso qué significa?"  
**Sistema:** "🤷 No sé, crasheó"

### Después (Defendible)

**Arqueólogo:** "¿Por qué descartaste este sitio?"  
**Sistema:** "ICESat-2 status: INVALID"  
**Arqueólogo:** "¿Por qué?"  
**Sistema:** "Reason: insufficient_valid_points - only 3 points after quality filtering (minimum required: 10)"  
**Arqueólogo:** "¿Qué flags usaste?"  
**Sistema:** "Quality flags: signal_conf >= 3, quality_flag == 0"  
**Arqueólogo:** "✅ Metodología sólida"

---

## IMPACTO EN ANÁLISIS BATCH

### Problema Actual

```
HTTP 500: Out of range float values are not JSON compliant
```

**Causa:** ICESat-2 devuelve inf → JSON.dumps() crashea

### Con Instrument Contract

```python
# ICESat-2 devuelve inf
measurement = InstrumentMeasurement.create_invalid(
    instrument_name="ICESat-2",
    measurement_type="elevation",
    reason="all_values_inf",
    source="NASA Earthdata"
)

# JSON serialization SIEMPRE funciona
json.dumps(measurement.to_dict())  # ✅ OK
```

**Resultado:** Análisis batch 5/5 exitosos

---

## PRÓXIMOS PASOS (ORDEN ESTRICTO)

### 1. Migrar ICESat-2 (30 min) 🔴 CRÍTICO

**Archivo:** `backend/satellite_connectors/icesat2_connector.py`

**Cambios:**
- Importar `InstrumentMeasurement`, `InstrumentStatus`
- Filtrar por quality flags
- Devolver `InstrumentMeasurement` en lugar de float
- Mínimo 10 puntos válidos

### 2. Actualizar Core Detector (30 min) 🔴 CRÍTICO

**Archivo:** `backend/core_anomaly_detector.py`

**Cambios:**
- Aceptar `List[InstrumentMeasurement]`
- Filtrar por `is_usable()`
- Contar estados para razonamiento
- Serializar correctamente a JSON

### 3. Ejecutar Análisis Batch (15 min) ✅ VALIDACIÓN

**Comando:** `python analyze_archaeological_candidates.py`

**Expectativa:** 5/5 análisis exitosos

### 4. Migrar Resto de Instrumentos (2 horas) 🟡 MEJORA

- NSIDC (15 min)
- Sentinel-2 (20 min)
- Sentinel-1 SAR (20 min)
- Landsat (20 min)
- MODIS (20 min)

---

## MÉTRICAS DE ÉXITO

### Antes del Contract

- ❌ Análisis batch: 0/5 exitosos
- ❌ Instrumentos funcionando: 1/8 (12.5%)
- ❌ JSON serialization: Crashea con inf/nan
- ❌ Trazabilidad: Ninguna
- ❌ Defensa científica: Imposible

### Después del Contract (Objetivo)

- ✅ Análisis batch: 5/5 exitosos
- ✅ Instrumentos reportando: 8/8 (100%)
- ✅ JSON serialization: Siempre funciona
- ✅ Trazabilidad: Completa
- ✅ Defensa científica: Sólida

**Nota:** "Reportando" ≠ "Midiendo exitosamente"  
Un instrumento que devuelve `NO_DATA` con razón documentada es **más valioso** que uno que crashea silenciosamente.

---

## CONCLUSIÓN

### El Cambio de Paradigma

**Antes:** "¿Funciona el instrumento?"  
**Después:** "¿Qué nos dice el instrumento (incluso si no tiene datos)?"

### Por Qué Esto Es Crítico

1. **Robustez:** Sistema resiste datos reales, feos, incompletos
2. **Honestidad:** No inventa datos cuando no los hay
3. **Trazabilidad:** Cada decisión es auditable
4. **Defensa:** Metodología científicamente sólida

### El Salto Cualitativo

Este cambio convierte ArcheoScope de:
- "Prototipo que funciona en teoría"

A:
- "Sistema de producción que resiste el mundo real"

**Ese salto es el que el 90% de los proyectos nunca cruza.**

---

**Implementado:** 2026-01-26 22:15:00  
**Próximo paso:** Migrar ICESat-2 (30 min)  
**Impacto esperado:** Desbloquea análisis batch completo
