# Guía de Testing de Performance - ArcheoScope

**Branch**: hrmBackendWorld  
**Fecha**: 23 de Febrero, 2026

## 🎯 Sistema de Monitoreo Implementado

Se ha implementado un sistema completo de monitoreo de performance que registra métricas en consola sin UI visible.

---

## 📊 Métricas Monitoreadas

### Automáticas (cada 2 segundos):
- **FPS** (Frames Per Second)
- **Frame Time** (ms por frame)
- **Draw Calls** (llamadas de renderizado)
- **Triangles** (triángulos renderizados)
- **Geometries** (geometrías en memoria)
- **Textures** (texturas en memoria)
- **Programs** (shaders compilados)
- **Memory** (memoria JS usada - solo Chrome)

### Umbrales de Alerta:
```
FPS:
  ✅ GOOD: >30 FPS
  ⚠️ WARNING: 25-30 FPS
  🔴 CRITICAL: <25 FPS

Frame Time:
  ✅ GOOD: <33ms
  ⚠️ WARNING: 33-40ms
  🔴 CRITICAL: >40ms

Draw Calls:
  ✅ GOOD: <200
  ⚠️ WARNING: 200-300
  🔴 CRITICAL: >300

Triangles:
  ✅ GOOD: <500K
  ⚠️ WARNING: 500K-1M
  🔴 CRITICAL: >1M
```

---

## 🔧 Comandos de Consola

Abre DevTools Console (F12) y usa estos comandos:

### 1. Ver Ayuda
```javascript
perf.help()
```

### 2. Capturar Snapshot
```javascript
perf.snapshot("Machu Picchu", "Clear", 1)
perf.snapshot("Machu Picchu", "Rain+Wind", 1)
perf.snapshot("Machu Picchu", "Storm+Lightning", 1)
```

Parámetros:
- `location`: Nombre de la ubicación (ej: "Machu Picchu")
- `weather`: Condiciones climáticas (ej: "Rain+Wind+Fog")
- `anomalies`: Número de anomalías activas

### 3. Ver Reporte Completo
```javascript
perf.report()
```

### 4. Limpiar Snapshots
```javascript
perf.clear()
```

---

## 📋 Plan de Testing Sugerido

### Test 1: Baseline (Sin Efectos)
1. Ir a Machu Picchu
2. Sin clima activo
3. Capturar: `perf.snapshot("Machu Picchu", "Clear", 1)`

### Test 2: Clima Ligero
1. Activar: Lluvia ligera
2. Capturar: `perf.snapshot("Machu Picchu", "Light Rain", 1)`

### Test 3: Clima Moderado
1. Activar: Lluvia + Viento
2. Capturar: `perf.snapshot("Machu Picchu", "Rain+Wind", 1)`

### Test 4: Clima Extremo
1. Activar: Tormenta + Rayos + Viento
2. Capturar: `perf.snapshot("Machu Picchu", "Storm+Lightning+Wind", 1)`

### Test 5: Todo Activado
1. Activar: Tormenta + Rayos + Viento + Niebla + Tornado
2. Capturar: `perf.snapshot("Machu Picchu", "All Weather", 1)`

### Test 6: Movimiento Rápido
1. Mover la nave rápidamente
2. Observar si hay drops de FPS
3. Capturar: `perf.snapshot("Machu Picchu", "Fast Movement", 1)`

---

## 📈 Interpretación de Resultados

### Logs en Consola

Cada 2 segundos verás algo como:

```
📊 PERFORMANCE METRICS
  🎯 FPS: 58.3 (min: 52.1)
  ⏱️ Frame Time: 17.15ms (max: 19.23ms)
  🎨 Draw Calls: 145
  🔺 Triangles: 234.5K
  📦 Geometries: 89
  🖼️ Textures: 23
  🔧 Programs: 12
  💾 Memory: 156MB
```

### Colores:
- 🟢 Verde = GOOD (rendimiento óptimo)
- 🟡 Amarillo = WARNING (rendimiento aceptable)
- 🔴 Rojo = CRITICAL (rendimiento problemático)

### Warnings:
Si hay problemas, verás:
```
⚠️ WARNINGS:
  - FPS crítico: 24.5 (objetivo: >30)
  - Draw calls alto: 245 (objetivo: <200)
```

---

## 🔍 Análisis de "Pantallazos Verdes"

Los pantallazos verdes pueden ser causados por:

1. **Shader Compilation Stutter**
   - Ocurre cuando se compila un shader por primera vez
   - Solución: Precargar shaders

2. **Garbage Collection Spike**
   - JavaScript pausando para limpiar memoria
   - Verás spike en Frame Time

3. **GPU Overload**
   - Demasiados efectos visuales simultáneos
   - Verás FPS bajo + Frame Time alto

4. **Transparencias Pesadas**
   - El campo de resonancia usa transparencias
   - Verás Draw Calls alto

---

## 📊 Generar Reporte Final

Después de todos los tests:

```javascript
perf.report()
```

Esto generará un reporte completo con:
- Todos los snapshots capturados
- Análisis comparativo
- Peor escenario detectado
- Promedios generales

---

## 🎯 Objetivos de Performance

Para ArcheoScope, buscamos:

| Escenario | FPS Mínimo | Frame Time Máximo |
|-----------|------------|-------------------|
| Exploración normal | 45+ | <22ms |
| Clima activo | 35+ | <28ms |
| Clima extremo | 30+ | <33ms |
| Anomalías activas | 40+ | <25ms |

---

## 💡 Tips para Testing

1. **Espera 5 segundos** después de cada cambio antes de capturar snapshot
2. **Mueve la cámara** para asegurar que todo está renderizado
3. **Observa la consola** para ver métricas en tiempo real
4. **Captura múltiples snapshots** del mismo escenario para promedios
5. **Anota cualquier comportamiento visual extraño** (pantallazos, stuttering)

---

## 🐛 Debugging

Si ves problemas:

1. Verifica Draw Calls (debería ser <200)
2. Verifica Triangles (debería ser <500K)
3. Verifica Frame Time (debería ser <33ms)
4. Busca warnings en consola

---

## 📝 Formato de Reporte para Kiro

Después de testing, comparte:

```
Ubicación: Machu Picchu
Anomalías: 1 (Gravitacional)

Test 1 - Clear:
  FPS: XX
  Frame Time: XXms
  Draw Calls: XX
  Warnings: [lista]

Test 2 - Rain+Wind:
  FPS: XX
  Frame Time: XXms
  Draw Calls: XX
  Warnings: [lista]

... etc
```

O simplemente copia el output de `perf.report()`

---

## 🚀 Próximos Pasos

Basado en los resultados, podemos:
1. Optimizar shaders pesados
2. Reducir geometría de efectos
3. Implementar LOD para anomalías
4. Ajustar umbrales de culling
5. Simplificar efectos climáticos

---

**¡Listo para testing!** 🎮
