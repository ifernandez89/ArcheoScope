# 🔍 AUDITORÍA DE ARQUITECTURA Y ESCALABILIDAD
**Fecha:** 24 de Febrero 2026  
**Proyecto:** ArcheoScope 3D Viewer

---

## 📊 RESUMEN EJECUTIVO

### ✅ FORTALEZAS ACTUALES
- ✔ Sistemas con dispose implementados
- ✔ Monitoring real (Logger system)
- ✔ Culling agresivo (CullingSystem)
- ✔ LOD system funcional (WorldCore.LOD)
- ✔ Lazy loading de componentes pesados
- ✔ Preload optimizado (árboles deshabilitados)

### ❌ PUNTOS CRÍTICOS IDENTIFICADOS

#### 🔴 CRÍTICO 1: NO EXISTE LÍMITE DE 1 MUNDO ACTIVO
**Estado:** ❌ NO IMPLEMENTADO  
**Riesgo:** ALTO - Puede destruir escalabilidad  
**Ubicación:** `viewer3d/components/ImmersiveScene.tsx`

**Problema:**
```typescript
// Línea 442-450: Ambas escenas pueden coexistir
{mode === 'globe' ? (
  <GlobeScene />  // ← Mundo 1
) : mode === 'model' ? (
  <ModelScene />  // ← Mundo 2
) : null}
```

**Impacto:**
- No hay garantía de que solo 1 mundo esté activo
- Transiciones pueden tener ambos mundos en memoria
- Sin WorldManager, no hay policía central de recursos

---

#### 🟡 CRÍTICO 2: WorldCore EXISTE PERO SIN GOBERNANZA
**Estado:** ⚠️ PARCIALMENTE IMPLEMENTADO  
**Riesgo:** MEDIO - Inconsistencia arquitectónica

**Archivos afectados:**
- `viewer3d/engines/WorldCore/index.ts` - Existe como façade
- `viewer3d/engines/EngineCore.ts` - Lo usa para Time/State
- `viewer3d/systems/CullingSystem.ts` - Import directo
- `viewer3d/hooks/useLOD.ts` - Import directo
- `viewer3d/components/systems/SmartLOD.tsx` - Import directo

**Problema:**
- WorldCore existe pero NO controla cuántos mundos hay activos
- Es una colección de utilidades, no un orquestador
- No tiene método `setActiveWorld()` o `disposeWorld()`

**Estructura actual:**
```typescript
export const WorldCore = {
  State: WorldStateInstance,
  Time: WorldTimeInstance,
  LOD: LODSystemInstance,
  Entities: EntitySystemInstance,
  Procedural: ProceduralGeneratorInstance,
  Streaming: StreamingSystemInstance
}
```

**Falta:**
```typescript
// ❌ NO EXISTE
WorldCore.setActiveWorld(worldId)
WorldCore.disposeInactiveWorlds()
WorldCore.getActiveWorldCount() // Debería ser siempre 1
```

---

#### 🟡 CRÍTICO 3: CLEANUP EN useEffect
**Estado:** ⚠️ REVISAR  
**Riesgo:** MEDIO - Memory leaks silenciosos

**Componentes a auditar:**
1. `ImmersiveScene.tsx` - Transiciones de modo
2. `WalkableAvatar.tsx` - Event listeners
3. `GlobeScene` - Three.js objects
4. `ModelScene` - Three.js objects

**Búsqueda realizada:**
- ❌ No se encontraron patrones `useEffect(() => { return () => {} })`
- ⚠️ Necesita revisión manual de cada componente

---

#### 🟡 CRÍTICO 4: PRESUPUESTO NO DOCUMENTADO
**Estado:** ❌ NO EXISTE  
**Riesgo:** BAJO - Pero importante para disciplina

**Falta:**
- Documento de presupuesto de recursos
- Límites por escena (polys, draw calls, memory)
- Métricas objetivo de performance

---

## 🎯 PLAN DE ACCIÓN PRIORITARIO

### 1️⃣ IMPLEMENTAR WorldManager (URGENTE)

**Crear:** `viewer3d/engines/WorldManager.ts`

```typescript
/**
 * WorldManager - Orquestador central de mundos
 * REGLA: Solo 1 mundo activo a la vez
 */

class WorldManager {
  private activeWorld: string | null = null
  private worlds: Map<string, WorldInstance> = new Map()
  
  /**
   * Activar un mundo (desactiva el anterior automáticamente)
   */
  setActiveWorld(worldId: string): void {
    // Dispose del mundo anterior
    if (this.activeWorld && this.activeWorld !== worldId) {
      this.disposeWorld(this.activeWorld)
    }
    
    this.activeWorld = worldId
    loggers.world.info(`Mundo activo: ${worldId}`)
  }
  
  /**
   * Obtener mundo activo (siempre 0 o 1)
   */
  getActiveWorldCount(): number {
    return this.activeWorld ? 1 : 0
  }
  
  /**
   * Dispose completo de un mundo
   */
  private disposeWorld(worldId: string): void {
    const world = this.worlds.get(worldId)
    if (!world) return
    
    // Cleanup de recursos Three.js
    world.scene.traverse((obj) => {
      if (obj instanceof THREE.Mesh) {
        obj.geometry?.dispose()
        if (Array.isArray(obj.material)) {
          obj.material.forEach(m => m.dispose())
        } else {
          obj.material?.dispose()
        }
      }
    })
    
    this.worlds.delete(worldId)
    loggers.world.info(`Mundo disposed: ${worldId}`)
  }
}

export const worldManager = new WorldManager()
```

**Integrar en:** `ImmersiveScene.tsx`

```typescript
useEffect(() => {
  if (mode === 'globe') {
    worldManager.setActiveWorld('globe')
  } else if (mode === 'model') {
    worldManager.setActiveWorld('terrain')
  }
}, [mode])
```

---

### 2️⃣ RESOLVER WorldCore (IMPORTANTE)

**Opción A: Convertir en Orquestador Real**
```typescript
export const WorldCore = {
  // Existentes
  State, Time, LOD, Entities, Procedural, Streaming,
  
  // NUEVOS
  Manager: worldManager,  // ← Agregar WorldManager
  
  // Métodos de conveniencia
  setActiveWorld: (id: string) => worldManager.setActiveWorld(id),
  getActiveCount: () => worldManager.getActiveWorldCount()
}
```

**Opción B: Simplificar y Renombrar**
- Renombrar a `WorldUtils` (más honesto)
- Eliminar referencias como "Core"
- Crear `WorldCore` real que incluya Manager

**Recomendación:** Opción A (menos breaking changes)

---

### 3️⃣ AUDITAR CLEANUP useEffect (ESTA SEMANA)

**Checklist por componente:**

**ImmersiveScene.tsx:**
- [ ] Verificar cleanup en transiciones de modo
- [ ] Verificar dispose de Canvas al desmontar
- [ ] Verificar cleanup de event listeners

**WalkableAvatar.tsx:**
- [ ] Verificar cleanup de `addEventListener('keydown')`
- [ ] Verificar cleanup de `addEventListener('mousemove')`
- [ ] Verificar dispose de GLTF models

**GlobeScene:**
- [ ] Verificar dispose de Globe3D
- [ ] Verificar cleanup de markers
- [ ] Verificar dispose de geometries/materials

**ModelScene:**
- [ ] Verificar dispose de terrain
- [ ] Verificar cleanup de weather system
- [ ] Verificar dispose de avatar model

---

### 4️⃣ DOCUMENTAR PRESUPUESTO (ESTA SEMANA)

**Crear:** `RESOURCE_BUDGET.md`

```markdown
# Presupuesto de Recursos ArcheoScope

## Por Escena

### Globo (Globe Scene)
- Polígonos: 100K max
- Draw Calls: 50 max
- Memory: 150MB max
- Texturas: 50MB max

### Terreno (Model Scene)
- Polígonos: 200K max
- Draw Calls: 100 max
- Memory: 300MB max
- Texturas: 100MB max

### Transición
- Ambos mundos: 0ms overlap (dispose inmediato)

## Métricas Objetivo
- FPS: 60 (desktop), 30 (mobile)
- Load Time: <3s (initial), <1s (transitions)
- Memory Growth: <10MB/min
```

---

## 📈 EVALUACIÓN ACTUAL

### Nivel Arquitectónico: **INTERMEDIO-AVANZADO**

**Tienes:**
- ✅ Todos los sistemas correctos a nivel micro
- ✅ Monitoring y logging
- ✅ Optimizaciones de rendering
- ✅ Lazy loading

**Te falta:**
- ❌ Gobernanza central (WorldManager)
- ⚠️ Consistencia arquitectónica (WorldCore)
- ⚠️ Cleanup verificado
- ❌ Presupuesto documentado

---

## 🚦 REGLA DE ORO

### ⛔ NO AGREGAR MÁS FEATURES HASTA:

1. ✅ WorldManager implementado
2. ✅ WorldCore resuelto (Opción A o B)
3. ✅ Cleanup auditado en componentes críticos
4. ✅ Presupuesto documentado

---

## 🎯 CONCLUSIÓN

**Estado:** NO EN RIESGO INMEDIATO  
**Diseño:** BUENO a nivel micro  
**Falta:** Capa macro-orquestadora

**Analogía:**
```
Tienes un ejército bien entrenado (sistemas)
Pero sin un general (WorldManager)
```

**Próximo paso:** Implementar WorldManager antes de cualquier feature nueva.

---

## 📝 NOTAS TÉCNICAS

### Imports de WorldCore encontrados:
- `viewer3d/systems/CullingSystem.ts`
- `viewer3d/hooks/useLOD.ts`
- `viewer3d/components/systems/SmartLOD.tsx`
- `viewer3d/engines/EngineCore.ts`
- `viewer3d/components/debug/LODDebugPanel.tsx`

### Escenas activas simultáneas:
- `GlobeScene` (modo 'globe')
- `ModelScene` (modo 'model')
- Sin garantía de dispose entre transiciones

### Lazy loading implementado:
- `LazyImmersiveScene` en `utils/lazy-engines.ts`
- Preload de UFOs optimizado
- Árboles pesados en lazy load

---

**Auditoría realizada por:** Kiro AI  
**Próxima revisión:** Después de implementar WorldManager
