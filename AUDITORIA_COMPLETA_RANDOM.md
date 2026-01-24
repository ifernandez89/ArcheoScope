# 🚨 AUDITORÍA COMPLETA: USO DE np.random

**Fecha:** 23 de Enero, 2026  
**Estado:** ⚠️ **PROBLEMAS CRÍTICOS ENCONTRADOS**

---

## 🔴 PROBLEMA CRÍTICO IDENTIFICADO

Las funciones de generación de datos sintéticos **TODAVÍA USAN np.random** de forma inconsistente:

### Funciones Problemáticas en `backend/water/submarine_archaeology.py`:

1. **`_generate_bathymetry_data()`** - Línea 254
   ```python
   # ❌ PROBLEMA: Número variable de anomalías
   num_anomalies = np.random.randint(1, 3)  # Puede ser 1 o 2
   num_anomalies = np.random.randint(0, 2)  # Puede ser 0 o 1
   
   # ❌ PROBLEMA: Posiciones aleatorias
   x, y = np.random.randint(10, grid_size-10, 2)
   
   # ❌ PROBLEMA: Dimensiones aleatorias
   wreck_length = np.random.uniform(150, 350)
   wreck_width = np.random.uniform(20, 50)
   ```

2. **`_generate_acoustic_image_data()`** - Línea 319
   ```python
   # ❌ PROBLEMA: Número variable de targets
   num_targets = np.random.randint(0, 3)  # Puede ser 0, 1 o 2
   
   # ❌ PROBLEMA: Posiciones aleatorias
   x, y = np.random.randint(5, grid_size-5, 2)
   ```

3. **`_generate_sediment_profile_data()`** - Línea 345
   ```python
   # ❌ PROBLEMA: Número variable de objetos enterrados
   num_buried = np.random.randint(0, 2)  # Puede ser 0 o 1
   ```

4. **`_generate_magnetic_data()`** - Línea 366
   ```python
   # ❌ PROBLEMA: Número variable de anomalías magnéticas
   num_anomalies = np.random.randint(0, 3)  # Puede ser 0, 1 o 2
   ```

---

## ⚠️ POR QUÉ ESTO ES CRÍTICO

Aunque estas funciones establecen `np.random.seed(seed)`, el problema es que:

1. **Generan MÚLTIPLES anomalías en diferentes sensores**
2. **Cada sensor puede generar 0-3 anomalías**
3. **El total se SUMA**: bathymetry (0-2) + acoustic (0-2) + magnetic (0-2) = **0-6 anomalías**
4. **La detección luego encuentra TODAS estas anomalías**

### Ejemplo del Problema:
```
Coordenadas: 18.5, -77.5

Ejecución #1:
  - bathymetry genera: 2 anomalías
  - acoustic genera: 1 anomalía
  - magnetic genera: 0 anomalías
  - TOTAL: 3 anomalías detectadas

Ejecución #2:
  - bathymetry genera: 1 anomalía
  - acoustic genera: 0 anomalías
  - magnetic genera: 0 anomalías
  - TOTAL: 1 anomalía detectada

Ejecución #3:
  - bathymetry genera: 2 anomalías
  - acoustic genera: 2 anomalías
  - magnetic genera: 2 anomalías
  - TOTAL: 6 anomalías detectadas
```

---

## ✅ SOLUCIÓN REQUERIDA

### Opción 1: ELIMINAR Generación de Datos Sintéticos (RECOMENDADO)

Ya que la nueva función `_detect_submarine_volumetric_anomalies()` es determinística y NO usa estos datos sintéticos, debemos:

1. **ELIMINAR** las llamadas a `_generate_submarine_sensor_data()`
2. **ELIMINAR** o **DEPRECAR** todas las funciones `_generate_*_data()`
3. **USAR SOLO** la nueva función determinística

### Opción 2: HACER Generación Completamente Determinística

Si necesitamos mantener la generación de datos sintéticos:

1. **ELIMINAR** todos los `np.random.randint()` para número de anomalías
2. **USAR** número FIJO basado en coordenadas
3. **ELIMINAR** todos los `np.random.uniform()` para dimensiones
4. **USAR** dimensiones FIJAS basadas en coordenadas

---

## 🔍 OTROS LUGARES CON np.random

### `backend/water/water_detector.py`

✅ **CORRECTO** - Usa semilla consistente:
```python
seed = int((abs(lat) * 1000 + abs(lon) * 1000) % 2147483647)
np.random.seed(seed)
return np.random.uniform(3700, 3900)  # ✅ Consistente con semilla
```

**PERO** - Usa `np.random.uniform()` para rangos de profundidad. Esto es ACEPTABLE porque:
- La semilla se establece ANTES
- El rango es pequeño (variación de ±100m es realista)
- NO afecta el NÚMERO de anomalías

---

## 📋 PLAN DE ACCIÓN INMEDIATO

### PASO 1: Verificar si `_generate_submarine_sensor_data()` se usa

```bash
grep -r "_generate_submarine_sensor_data" backend/
```

### PASO 2: Si se usa, REEMPLAZAR con datos determinísticos

### PASO 3: ELIMINAR o DEPRECAR funciones problemáticas

### PASO 4: PROBAR con 10 ejecuciones de las mismas coordenadas

---

## 🎯 CRITERIO DE ÉXITO

```python
# Test de consistencia
coords = (18.5, -77.5)
results = []

for i in range(10):
    analysis = submarine_engine.analyze_submarine_area(water_context, bounds)
    num_anomalies = len(analysis['wreck_candidates'])
    results.append(num_anomalies)

# DEBE PASAR:
assert len(set(results)) == 1, f"Resultados inconsistentes: {results}"
assert all(r == results[0] for r in results), "Todas las ejecuciones deben ser idénticas"
```

---

## ⚠️ RECOMENDACIÓN FINAL

**ELIMINAR COMPLETAMENTE** la generación de datos sintéticos y usar SOLO la función determinística nueva.

**Razón:** La generación de datos sintéticos es inherentemente problemática porque:
1. Intenta simular sensores reales con ruido aleatorio
2. El ruido aleatorio causa inconsistencias
3. No necesitamos simular sensores - necesitamos resultados determinísticos

**Solución:** Generar anomalías directamente basadas en coordenadas y contexto arqueológico, sin simular sensores intermedios.

---

**Estado:** ⚠️ **REQUIERE CORRECCIÓN INMEDIATA**
