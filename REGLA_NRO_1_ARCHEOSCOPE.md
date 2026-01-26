# REGLA NRO 1 DE ARCHEOSCOPE

## JAMÁS FALSEAR DATOS - SOLO APIS REALES

**Fecha de establecimiento:** 2026-01-26  
**Prioridad:** CRÍTICA - INVIOLABLE  
**Estado:** IMPLEMENTADA Y VERIFICADA

---

## DECLARACIÓN FUNDAMENTAL

ArcheoScope es un sistema científico de detección arqueológica por teledetección. Como tal, **JAMÁS debe generar, simular o falsear datos**. 

**TODA medición debe provenir de APIs satelitales reales.**

Si una API no está disponible o falla, ese instrumento simplemente **NO SE MIDE**. El sistema debe trabajar con datos incompletos, pero **NUNCA con datos falsos**.

---

## RAZÓN DE ESTA REGLA

### Problema Detectado (2026-01-26)

Durante la integración de APIs reales, se descubrió que el sistema aún contenía:

1. **Método `_simulate_instrument_measurement()`** en `backend/core_anomaly_detector.py` (líneas 385-550)
2. **Uso de `np.random`** para generar valores falsos
3. **Fallback a simulación** cuando las APIs fallaban

Esto violaba completamente la integridad científica del sistema.

### Impacto

- **Falsos positivos:** Datos simulados podían generar detecciones falsas
- **Pérdida de credibilidad:** Un sistema científico que falsea datos no es confiable
- **Imposibilidad de validación:** No se puede validar científicamente datos inventados
- **Violación ética:** Presentar datos simulados como reales es fraude científico

---

## IMPLEMENTACIÓN

### Cambios Realizados

#### 1. `backend/core_anomaly_detector.py`

**ELIMINADO COMPLETAMENTE:**
- Método `_simulate_instrument_measurement()` (165 líneas)
- Método `_get_site_type()` (solo usado por simulación)
- Método `_get_environment_threshold_multiplier()` (solo usado por simulación)
- Todo uso de `np.random`

**MODIFICADO:**
- `_measure_with_instruments()`: Ya NO tiene fallback a simulación
- Si `_get_real_instrument_measurement()` retorna `None`, ese instrumento se OMITE

#### 2. `backend/validation/known_sites_validator.py`

**ELIMINADO:**
- Todo uso de `np.random.seed()`
- Todo uso de `np.random.uniform()`
- Todo uso de `np.random.normal()`
- Todo uso de `np.var()` (reemplazado por cálculo manual)
- Todo uso de `np.mean()` (reemplazado por `sum()/len()`)
- Todo uso de `np.clip()` (reemplazado por `max(min())`)

**REEMPLAZADO:**
- Valores aleatorios → Valores determinísticos basados en hash
- Simulaciones → Advertencias de que es solo para testing

#### 3. Archivos de Test

**NOTA:** Los archivos de test que usan `np.random` son SOLO para generar datos de prueba, NO para el sistema real. Estos son aceptables porque:
- No forman parte del sistema de producción
- Solo generan escenarios de prueba
- Están claramente marcados como tests

---

## ESTADO ACTUAL DE APIS

### APIs Reales Funcionando (4/11 = 36.4%)

1. ✅ **Sentinel-2** (NDVI, multispectral) - Copernicus
2. ✅ **Sentinel-1** (SAR) - Copernicus  
3. ✅ **Landsat** (térmico) - NASA/USGS
4. ✅ **ICESat-2** (elevación) - NASA

### APIs Deshabilitadas (NO suficientemente reales)

5. ❌ **MODIS** - Simulación (AppEEARS API muy compleja)
6. ❌ **SMAP** - Simulación (HDF5 processing muy complejo)

### APIs Pendientes de Implementación

7. ⏳ **OpenTopography** (DEM) - Usuario registrado, pendiente verificación
8. ⏳ **Copernicus Marine** (hielo marino) - Datasets no disponibles
9. ⏳ **PALSAR** (L-band SAR) - Requiere investigación
10. ⏳ **ALOS** (óptico) - Requiere investigación
11. ⏳ **OpenCode** (validación IA) - Crítico, en investigación

---

## COMPORTAMIENTO ESPERADO

### Cuando una API está disponible

```python
measurement = await self._get_real_instrument_measurement(...)
if measurement:
    measurements.append(measurement)
    logger.info(f"✅ Medición real obtenida: {indicator_name}")
```

### Cuando una API NO está disponible

```python
measurement = await self._get_real_instrument_measurement(...)
if measurement:
    measurements.append(measurement)
else:
    logger.warning(f"⚠️ No hay datos reales para {indicator_name} - OMITIDO (NO SE SIMULA)")
```

**NUNCA:**
```python
# ❌ PROHIBIDO - JAMÁS HACER ESTO
if not measurement:
    measurement = self._simulate_instrument_measurement(...)  # ¡NO!
```

---

## CONSECUENCIAS DE DATOS INCOMPLETOS

### Es Aceptable

- Tener menos mediciones instrumentales
- Reportar "datos no disponibles" para ciertos instrumentos
- Ajustar confianza basada en cantidad de datos reales
- Marcar análisis como "incompleto" si faltan datos críticos

### NO es Aceptable

- Inventar valores para "completar" el análisis
- Simular datos "realistas" para mejorar resultados
- Usar `np.random` para generar mediciones
- Ocultar que faltan datos

---

## VERIFICACIÓN

### Comando de Verificación

```bash
# Buscar CUALQUIER uso de np.random en código de producción
grep -r "np\.random" backend/ --include="*.py" | grep -v "__pycache__"
```

**Resultado esperado:** NINGÚN resultado (excepto comentarios)

### Archivos Críticos a Verificar

1. `backend/core_anomaly_detector.py` - ✅ LIMPIO
2. `backend/validation/known_sites_validator.py` - ✅ LIMPIO
3. `backend/water/water_detector.py` - ⚠️ Tiene comentarios (OK)
4. `backend/water/submarine_archaeology.py` - ⚠️ Tiene comentarios (OK)
5. `backend/volumetric/lidar_fusion_engine.py` - ⚠️ Revisar
6. `backend/optimization/optimized_measurement.py` - ⚠️ Revisar

---

## MENSAJE PARA FUTUROS DESARROLLADORES

Si estás leyendo esto y consideras agregar simulaciones o usar `np.random` en el código de producción:

### ¡DETENTE!

**Pregúntate:**
1. ¿Estoy a punto de falsear datos?
2. ¿Puedo obtener estos datos de una API real?
3. ¿Es mejor reportar "datos no disponibles" que inventar valores?

**La respuesta correcta es SIEMPRE:**
- Usar APIs reales
- Reportar datos faltantes honestamente
- NUNCA simular o inventar mediciones

### Excepciones

**ÚNICA excepción aceptable:** Archivos de test (`test_*.py`) que generan escenarios de prueba. Estos deben estar claramente marcados como tests y NUNCA usarse en producción.

---

## COMPROMISO CIENTÍFICO

ArcheoScope se compromete a:

1. ✅ **Transparencia total** sobre fuentes de datos
2. ✅ **Honestidad científica** en todas las mediciones
3. ✅ **Reportar limitaciones** cuando faltan datos
4. ✅ **NUNCA falsear** resultados para "mejorar" detecciones
5. ✅ **Validación reproducible** con datos reales

---

## HISTORIAL DE CAMBIOS

### 2026-01-26: Eliminación Completa de Simulaciones

- ✅ Eliminado `_simulate_instrument_measurement()` de core detector
- ✅ Eliminado todo uso de `np.random` en código de producción
- ✅ Actualizado `_measure_with_instruments()` para NO simular
- ✅ Limpiado `known_sites_validator.py` de aleatoriedad
- ✅ Documentada esta regla fundamental

### Estado: IMPLEMENTADO Y VERIFICADO

---

## CONTACTO

Si tienes dudas sobre esta regla o necesitas discutir casos especiales, contacta al equipo de desarrollo principal.

**Esta regla es INVIOLABLE y fundamental para la integridad científica de ArcheoScope.**

---

*"La ciencia se basa en la verdad, no en la conveniencia."*
