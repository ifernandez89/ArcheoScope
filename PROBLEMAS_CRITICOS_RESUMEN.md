# 🚨 PROBLEMAS CRÍTICOS - RESUMEN EJECUTIVO

**Fecha**: 2026-01-23  
**Estado**: 🔴 CRÍTICO - Sistema no funcional

---

## 🐛 PROBLEMA #1: LUPA ARQUEOLÓGICA GENERA NÚMEROS ALEATORIOS

### Síntoma
- Mismas coordenadas (25.511, -70.361) producen números diferentes:
  - Primera ejecución: 12 candidatos
  - Segunda ejecución: 8 candidatos
  - Tercera ejecución: 3 candidatos

### Evidencia
```
Frontend logs:
(index):2711 🚢 Candidatos a naufragios: 12
(index):2711 🚢 Candidatos a naufragios: 8
(index):2711 🚢 Candidatos a naufragios: 3

Backend test (Python):
Run 1: 0 candidatos
Run 2: 0 candidatos
Run 3: 0 candidatos
```

### Análisis
- **Backend es 100% determinístico** ✅
- **Frontend recibe números diferentes** ❌
- **Conclusión**: El problema está en el FRONTEND o en la comunicación

### Causa Probable
El frontend está:
1. Generando datos sintéticos aleatorios
2. Modificando los datos del backend
3. O hay un bug en cómo se parsean los datos

### Estado
🔴 **NO RESUELTO** - Requiere investigación urgente

---

## 🐛 PROBLEMA #2: SECCIONES VACÍAS EN UI

### Síntoma
Panel de resultados muestra secciones con "--" y "Esperando análisis...":
- Método Recomendado
- Sistema de Inferencia Volumétrica
- Modelo Volumétrico
- Interpretación Sintética

### Estado
🟡 **PARCIALMENTE RESUELTO** - Función `hideEmptySections()` creada pero puede no estar funcionando

---

## 🐛 PROBLEMA #3: ERROR "DATOS INCOMPLETOS"

### Síntoma
```
archaeological_app.js:528 ❌ Datos incompletos en displayResults
```

### Causa
`displayResults()` solo buscaba `anomaly_map.statistics` (terrestre) pero análisis de agua devuelve `statistical_results`

### Estado
✅ **RESUELTO** - Ahora soporta ambas estructuras

---

## 🐛 PROBLEMA #4: INPUTS PRE-RELLENADOS

### Síntoma
Los 4 inputs (latMin, latMax, lonMin, lonMax) tienen valores por defecto que pueden interferir

### Estado
⚠️ **NO ES UN PROBLEMA** - Funcionan correctamente cuando se usa el input de búsqueda

---

## 🐛 PROBLEMA #5: CALIBRACIÓN FUERA DEL CUADRO

### Síntoma
Rectángulo de calibración no coincide con coordenadas ingresadas

### Estado
⚠️ **NECESITA VERIFICACIÓN** - Puede estar relacionado con problema #1

---

## 🎯 PRIORIDADES

### URGENTE (Hacer AHORA)
1. 🔴 **Arreglar lupa arqueológica** - Números aleatorios
   - Encontrar donde se generan los números aleatorios
   - Asegurar que use datos del backend sin modificar

### IMPORTANTE (Hacer después)
2. 🟡 **Verificar hideEmptySections()** funciona
3. 🟡 **Verificar calibración** usa coordenadas correctas

---

## 📋 PLAN DE ACCIÓN

### Paso 1: Encontrar el código que genera números aleatorios
- Buscar en frontend donde se crea `statistical_results`
- Buscar `Math.random()` relacionado con candidatos
- Verificar que datos del backend no se modifican

### Paso 2: Arreglar la lupa
- Asegurar que usa `wreck_candidates` del backend directamente
- Eliminar cualquier generación sintética de datos
- Verificar con logs del backend

### Paso 3: Verificar otros problemas
- Confirmar que secciones vacías se ocultan
- Confirmar que calibración funciona

---

## 🔍 INFORMACIÓN NECESARIA DEL USUARIO

Para resolver el problema #1 (CRÍTICO), necesito:

1. **Logs del backend** cuando ejecutas 3 análisis seguidos
   - Mostrarán las coordenadas exactas recibidas
   - Mostrarán el número de candidatos que devuelve el backend

2. **Confirmar qué archivo HTML estás usando**
   - ¿`frontend/index.html`?
   - ¿Otro archivo?

3. **¿Qué significa "la lupa está rota"?**
   - ¿No se abre?
   - ¿Muestra datos incorrectos?
   - ¿Muestra números aleatorios?
   - ¿Otro problema?

---

**ESTADO ACTUAL**: 🔴 BLOQUEADO - Necesito más información para resolver problema crítico #1
