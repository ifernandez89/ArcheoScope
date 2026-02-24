# 📊 Presupuesto de Recursos - ArcheoScope 3D Viewer

**Versión:** 1.0  
**Fecha:** 24 de Febrero 2026  
**Propósito:** Definir límites de recursos para garantizar performance óptimo

---

## 🎯 Regla de Oro

**SOLO 1 MUNDO ACTIVO A LA VEZ**

Implementado mediante `WorldManager` que garantiza:
- ✅ Máximo 1 mundo en memoria
- ✅ Dispose automático al cambiar de mundo
- ✅ Logging de transiciones y recursos

---

## 🌍 Presupuesto por Escena

### Escena: Globo (Globe Scene)

**Límites de Recursos:**
- **Polígonos:** 100,000 max
- **Draw Calls:** 50 max
- **Memory:** 150MB max
- **Texturas:** 50MB max

**Componentes:**
- Tierra: ~50K polígonos
- Sistema Solar: ~30K polígonos
- Estrellas: ~10K partículas
- UFO espacial: ~5K polígonos
- Marcadores: ~5K polígonos

**Optimizaciones:**
- LOD en planetas distantes
- Culling de objetos fuera de vista
- Instancing para estrellas

---

### Escena: Terreno (Model Scene)

**Límites de Recursos:**
- **Polígonos:** 200,000 max
- **Draw Calls:** 100 max
- **Memory:** 300MB max
- **Texturas:** 100MB max

**Componentes:**
- Terreno procedural: ~80K polígonos
- Vegetación (árboles): ~40K polígonos (lazy load)
- Rocas y elementos: ~20K polígonos
- Avatar/UFO: ~5K polígonos
- Clima (partículas): ~1,000 partículas max
- Agua: ~10K polígonos

**Optimizaciones:**
- Culling agresivo (CullingSystem)
- LOD en vegetación
- Lazy load de árboles pesados
- Instancing para rocas y flores

---

### Transición entre Mundos

**Duración:** 2000ms (2 segundos)

**Comportamiento:**
- **Overlap:** 0ms (dispose inmediato del mundo anterior)
- **Garantía:** WorldManager asegura que solo 1 mundo existe
- **Logging:** Cada transición se registra con métricas

**Proceso:**
1. Usuario inicia transición (click en globo o botón)
2. `mode` cambia a 'transition'
3. Animación cinematográfica (2s)
4. `mode` cambia a nuevo mundo
5. WorldManager hace dispose del mundo anterior
6. Nuevo mundo se renderiza

---

## 🎮 Límites por Tipo de Asset

### Modelos 3D

| Asset | Cantidad | Tamaño | Estrategia |
|-------|----------|--------|------------|
| UFO models | 5 | ~2MB cada | Preload selectivo |
| Tree models | 3 | 12-17MB cada | Lazy load on demand |
| Rock models | 1 | ~500KB | Preload |
| Terrain | 1 | Procedural | Generado en runtime |

### Texturas

| Tipo | Resolución Max | Formato | Compresión |
|------|----------------|---------|------------|
| Planetas | 2048x2048 | JPG | Alta |
| Terreno | 1024x1024 | JPG | Media |
| Vegetación | 512x512 | PNG | Alta |
| UI | 256x256 | PNG | Baja |

### Partículas

| Sistema | Cantidad Max | Estrategia |
|---------|--------------|------------|
| Estrellas | 10,000 | Instancing |
| Nieve | 1,000 | Pooling |
| Lluvia | 1,000 | Pooling |
| Rayos | 50 | Event-based |
| Tornado | 500 | Condicional |

---

## 📈 Métricas Objetivo

### Performance

| Métrica | Desktop | Mobile | Crítico |
|---------|---------|--------|---------|
| **FPS** | 60 | 30 | Sí |
| **Frame Time** | <16ms | <33ms | Sí |
| **Load Time (inicial)** | <3s | <5s | No |
| **Load Time (transición)** | <1s | <2s | No |

### Memoria

| Métrica | Límite | Acción si excede |
|---------|--------|------------------|
| **Memory Growth** | <10MB/min | Investigar leaks |
| **Peak Memory** | <500MB | Reducir assets |
| **Baseline Memory** | ~200MB | Normal |

### Red

| Métrica | Límite | Estrategia |
|---------|--------|------------|
| **Initial Bundle** | <5MB | Code splitting |
| **Total Assets** | <50MB | Lazy loading |
| **API Calls** | <10/min | Caching |

---

## 🔍 Monitoreo

### Herramientas Activas

1. **Logger System** (`@/core/Logger`)
   - Logs de transiciones de mundo
   - Métricas de dispose
   - Errores de carga

2. **WorldManager Stats**
   ```typescript
   WorldCore.getWorldStats()
   // Retorna: { activeWorld, activeCount, totalWorlds, worlds[] }
   ```

3. **Browser DevTools**
   - Performance tab para FPS
   - Memory tab para leaks
   - Network tab para assets

### Debugging

Acceso global en consola:
```javascript
// Ver estado del WorldManager
window.__worldManager.getStats()

// Ver mundo activo
window.__worldManager.getActiveWorldId()

// Verificar que solo hay 1 mundo
window.__worldManager.getActiveWorldCount() // Debe ser 0 o 1
```

---

## ⚠️ Alertas y Límites

### Alertas Automáticas

| Condición | Acción |
|-----------|--------|
| `getActiveWorldCount() > 1` | 🚨 ERROR CRÍTICO - Revisar WorldManager |
| FPS < 30 (desktop) | ⚠️ Warning - Reducir calidad |
| Memory > 500MB | ⚠️ Warning - Revisar leaks |
| Load time > 5s | ⚠️ Warning - Optimizar assets |

### Proceso de Escalado

Si se exceden límites:

1. **Inmediato:** Reducir calidad de renderizado
   - Deshabilitar sombras
   - Reducir resolución de texturas
   - Disminuir partículas

2. **Corto plazo:** Optimizar assets
   - Comprimir texturas
   - Reducir polígonos
   - Implementar LOD más agresivo

3. **Largo plazo:** Refactorizar arquitectura
   - Streaming de chunks
   - Virtualización de objetos distantes
   - Occlusion culling

---

## 🎨 Presets de Calidad

### Ultra (Desktop High-End)
- Sombras: Sí (2048x2048)
- Post-processing: Completo
- Partículas: 100%
- LOD: Mínimo
- Target: 60 FPS

### Alto (Desktop Mid-Range)
- Sombras: Sí (1024x1024)
- Post-processing: Bloom + Vignette
- Partículas: 75%
- LOD: Moderado
- Target: 60 FPS

### Medio (Desktop Low-End / Mobile High)
- Sombras: Simplificadas
- Post-processing: Solo Vignette
- Partículas: 50%
- LOD: Agresivo
- Target: 30 FPS

### Bajo (Mobile Low-End)
- Sombras: No
- Post-processing: No
- Partículas: 25%
- LOD: Muy agresivo
- Target: 30 FPS

---

## 📝 Notas de Implementación

### Sistemas de Optimización Activos

1. **CullingSystem** - Oculta objetos fuera de vista
2. **LOD System** - Reduce detalle con distancia
3. **Lazy Loading** - Carga assets bajo demanda
4. **Instancing** - Reutiliza geometrías
5. **Object Pooling** - Recicla partículas
6. **WorldManager** - Garantiza 1 mundo activo

### Próximas Optimizaciones

- [ ] Streaming de terrain chunks
- [ ] Occlusion culling
- [ ] Texture atlasing
- [ ] GPU instancing para vegetación
- [ ] Web Workers para generación procedural

---

## 🔄 Historial de Cambios

### v1.0 - 24 Feb 2026
- ✅ Documento inicial creado
- ✅ WorldManager implementado
- ✅ Límites definidos por escena
- ✅ Métricas objetivo establecidas

---

**Mantenido por:** Equipo ArcheoScope  
**Próxima revisión:** Después de testing de performance
