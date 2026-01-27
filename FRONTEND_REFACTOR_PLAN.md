# ArcheoScope Frontend Refactorization Plan
## Post-Backend Stabilization - Scientific UI/UX

**Status**: Phase 4 Completed  
**Date**: January 27, 2026  
**Objective**: Transform frontend into reproducible, robust scientific workstation

**Progress**: 4/6 Phases Completed (67%)

---

## Core Principles

1. ✅ **NO modificar lógica científica** - Backend es fuente de verdad
2. ✅ **Vanilla JS only** - No frameworks (React, Vue)
3. ✅ **Event-driven architecture** - Desacoplamiento total
4. ✅ **Epistemic transparency** - Inferencia vs medición clara
5. ✅ **Reproducibility first** - Snapshots y replay mode
6. ✅ **Performance critical** - Throttling y fallbacks

---

## Phase 1: Architecture (✅ COMPLETED)

### 1.1 Event Bus (`frontend/core/event_bus.js`)

**Implementado**:
- ✅ Comunicación centralizada entre módulos
- ✅ Event logging para debugging
- ✅ Cleanup automático de listeners
- ✅ Snapshot del estado del bus

**Eventos estándar**:
```javascript
EVENTS = {
  ANALYSIS_STARTED, ANALYSIS_COMPLETED, ANALYSIS_FAILED,
  REGION_SELECTED, REGION_CLEARED,
  SCIENTIFIC_DATA_LOADED, SCIENTIFIC_DATA_UPDATED,
  UI_MODAL_OPENED, UI_MODAL_CLOSED, UI_LAYER_TOGGLED,
  LUPA_ACTIVATED, LUPA_DEACTIVATED,
  VIEWER_3D_OPENED, VIEWER_3D_CLOSED,
  SNAPSHOT_CREATED, SNAPSHOT_LOADED,
  REPLAY_MODE_ENABLED, REPLAY_MODE_DISABLED
}
```

### 1.2 Scientific State (`frontend/state/scientific_state.js`)

**Implementado**:
- ✅ Estado científico INMUTABLE
- ✅ Solo actualizable desde backend
- ✅ Etiquetado epistemológico integrado
- ✅ Sistema de snapshots para reproducibilidad
- ✅ Historial de análisis
- ✅ Exportación JSON

**Estructura**:
```javascript
{
  currentAnalysis: {...},
  scientificOutput: {...},
  phases: { phase_a, phase_b, ... phase_g },
  instrumentalMeasurements: [...],
  environmentContext: {...},
  epistemicLabels: {
    epistemic_mode: 'deterministic_scientific',
    ai_used: false,
    reproducible: true,
    method_transparency: 'full'
  },
  metadata: {...},
  history: [...]
}
```

### 1.3 UI State (`frontend/state/ui_state.js`)

**Implementado**:
- ✅ Estado UI separado de datos científicos
- ✅ Modales, capas, selección, vista
- ✅ Loading states por componente
- ✅ Modo replay
- ✅ Filtros de visualización

**Regla crítica**: UI State NO puede modificar Scientific State

---

## Phase 2: Component Decoupling (✅ COMPLETED)

### Módulos refactorizados:

#### 2.1 `frontend/modules/archaeological_lupa_module.js` ✅
**Implementado**:
- ✅ Eliminar acceso directo a DOM global
- ✅ Comunicar vía eventos únicamente
- ✅ Escuchar `LUPA_ACTIVATED`
- ✅ Emitir `LUPA_ANALYSIS_COMPLETED`
- ✅ Throttling de análisis (max 1/segundo)
- ✅ Cleanup automático de recursos Leaflet

#### 2.2 `frontend/modules/viewer_3d_module.js` ✅
**Implementado**:
- ✅ Desacoplar de mapa principal
- ✅ Escuchar `VIEWER_3D_OPENED`
- ✅ Emitir `VIEWER_3D_DATA_LOADED`
- ✅ Límite de FPS (30 fps max)
- ✅ Cleanup de geometrías Three.js
- ✅ Navegación entre anomalías
- ✅ Exportación de screenshots

#### 2.3 `frontend/modules/lidar_availability_module.js` ✅
**Implementado**:
- ✅ Convertir a módulo independiente
- ✅ Escuchar `REGION_SELECTED`
- ✅ Emitir resultados vía eventos
- ✅ Cache de consultas (1 hora)
- ✅ 10 regiones de cobertura LiDAR

#### 2.4 `frontend/modules/history_module.js` ✅
**Implementado**:
- ✅ Integrar con `scientificState.history`
- ✅ Escuchar `HISTORY_ENTRY_ADDED`
- ✅ Emitir `HISTORY_ENTRY_SELECTED`
- ✅ Persistencia en localStorage
- ✅ Exportar/Importar JSON
- ✅ Estadísticas de historial

---

## Phase 3: Reproducibility Mode (✅ COMPLETED)

### 3.1 Scientific Replay Mode ✅

**Implementado**:
- ✅ Captura completa de análisis:
  ```javascript
  {
    coordinates: {...},
    sensors: [...],
    scores: {...},
    timestamps: {...},
    inferenceFlags: {...}
  }
  ```

- ✅ UI para replay:
  - ✅ Indicador visual: "🔄 REPRODUCING ANALYSIS – NO LIVE DATA"
  - ✅ Timeline de eventos interactiva
  - ✅ Exportar/Importar snapshot JSON
  - ✅ Botones de control de snapshot

- ✅ Funcionalidad:
  - ✅ Congelar resultados
  - ✅ Compartir snapshot
  - ✅ Comparar análisis
  - ✅ Navegación por timeline
  - ✅ Descarga/carga de archivos

### 3.2 Snapshot System ✅

**Implementado en `scientificState` y `replayModeModule`**:
- ✅ `createSnapshot()` - Captura estado completo
- ✅ `loadSnapshot()` - Carga estado
- ✅ `exportSnapshot()` - Exporta JSON con metadata
- ✅ `importSnapshot()` - Importa desde JSON
- ✅ `compareSnapshots()` - Compara dos snapshots
- ✅ `downloadSnapshot()` - Descarga como archivo
- ✅ `uploadSnapshot()` - Carga desde archivo
- ✅ Límite de 50 snapshots en memoria
- ✅ Versioning (v2.0)

### 3.3 Estilos CSS ✅

**Archivo**: `frontend/styles/replay_mode.css`
- ✅ Indicador de replay con animación
- ✅ Timeline de eventos con scroll
- ✅ Controles de snapshot
- ✅ Badge de reproducibilidad
- ✅ Modal de comparación
- ✅ Responsive design

---

## Phase 4: Epistemic Integrity (✅ COMPLETED)

### 4.1 Visual Differentiation ✅

**Implementado**:

| Tipo | Color | Label | Tooltip |
|------|-------|-------|---------|
| **Medición directa** | Verde (#27ae60) | "MEASURED" 📡 | "Dato satelital directo" |
| **Inferencia** | Amarillo (#f39c12) | "INFERRED" 🧮 | "Calculado por pipeline" |
| **IA** | Naranja (#e67e22) | "AI-ASSISTED" 🤖 | "Explicación generada por IA" |
| **Simulado** | Rojo (#e74c3c) | "SIMULATED" ⚠️ | "Dato simulado - NO REAL" |

**CSS Implementado**:
```css
.measurement-direct { border-left: 4px solid #27ae60; }
.measurement-inferred { border-left: 4px solid #f39c12; }
.measurement-ai { border-left: 4px solid #e67e22; }
.measurement-simulated { border-left: 4px solid #e74c3c; }
```

### 4.2 Confidence Decay Visual ✅

**Implementado**:
- ✅ Barra de confianza con degradado
- ✅ Tooltip con intervalo de confianza
- ✅ Indicador de cobertura instrumental
- ✅ Animación de shimmer
- ✅ Colores dinámicos (verde/amarillo/rojo)

### 4.3 Epistemic Labels Display ✅

**Implementado**:
```html
<div class="epistemic-badge">
  <span class="badge-mode">🔬 Deterministic Scientific</span>
  <span class="badge-ai">🤖 AI: No</span>
  <span class="badge-reproducible">♻️ Reproducible: Yes</span>
  <span class="badge-transparency">📊 Transparency: Full</span>
</div>
```

### 4.4 Módulo Completo ✅

**Archivo**: `frontend/modules/epistemic_visual_module.js`
- ✅ Configuración de colores y estilos
- ✅ Etiquetado automático de mediciones
- ✅ Etiquetado de fases del pipeline
- ✅ Badges epistemológicos
- ✅ Métricas con barras visuales
- ✅ Confidence decay rendering
- ✅ Tooltips informativos
- ✅ Leyenda epistemológica

### 4.5 Estilos CSS ✅

**Archivo**: `frontend/styles/epistemic_visual.css`
- ✅ Variables CSS para colores
- ✅ Badges principales
- ✅ Métricas con barras
- ✅ Confidence decay
- ✅ Inline badges
- ✅ Leyenda epistemológica
- ✅ Advertencia de simulación
- ✅ Responsive design
- ✅ Animaciones suaves

---

## Phase 5: Performance & Safety (🔄 IN PROGRESS)

### 5.1 Guardrails

**Implementar**:

#### Lupa Arqueológica:
```javascript
const lupaThrottle = {
  maxCallsPerSecond: 1,
  lastCall: 0,
  queue: []
};
```

#### Visor 3D:
```javascript
const viewer3DLimits = {
  maxFPS: 30,
  maxGeometries: 10000,
  autoCleanup: true
};
```

#### Mapa:
```javascript
const mapLimits = {
  maxMarkers: 1000,
  clusterThreshold: 100,
  tileLoadTimeout: 5000
};
```

### 5.2 Memory Management

**Implementar**:
- [ ] Cleanup de event listeners al cerrar modales
- [ ] Dispose de geometrías Three.js
- [ ] Clear de capas Leaflet no visibles
- [ ] Garbage collection hints

### 5.3 Fallback Degradado

**Implementar**:
- [ ] Detectar sobrecarga (FPS < 15)
- [ ] Reducir calidad automáticamente
- [ ] Mostrar warning al usuario
- [ ] Opción de "Modo Ligero"

---

## Phase 6: Verification (⏳ PENDING)

### 6.1 Manual Testing

**Flujos a verificar**:
- [ ] Selección → Análisis → Resultados
- [ ] Lupa → Análisis detallado → Cierre
- [ ] Visor 3D → Carga → Rotación → Cierre
- [ ] Historial → Selección → Replay
- [ ] Exportación → Importación → Verificación

### 6.2 Automated Testing

**Tests mínimos**:
```javascript
// Event Bus
test('EventBus emits and receives events')
test('EventBus cleanup removes listeners')
test('EventBus logs events correctly')

// Scientific State
test('ScientificState only updates from backend')
test('ScientificState creates snapshots')
test('ScientificState exports valid JSON')

// UI State
test('UIState does not modify ScientificState')
test('UIState toggles modals correctly')
test('UIState manages loading states')
```

### 6.3 Integration Testing

**Verificar**:
- [ ] Frontend NO altera scores del backend
- [ ] Snapshots son reproducibles
- [ ] Event flow es correcto
- [ ] No hay memory leaks en sesiones largas (>1 hora)

---

## Current Status Summary

### ✅ Completed:
1. Event Bus architecture
2. Scientific State (immutable)
3. UI State (separated)
4. Snapshot system
5. Epistemic labeling structure
6. Archaeological Lupa Module (refactored)
7. Viewer 3D Module (refactored)
8. LiDAR Availability Module (refactored)
9. History Module (refactored)
10. Replay Mode Module (complete)
11. Replay Mode UI & CSS
12. Timeline de eventos
13. Snapshot export/import
14. Snapshot comparison
15. **Epistemic Visual Module (complete)**
16. **Diferenciación visual medición vs inferencia**
17. **Confidence decay visual**
18. **Badges epistemológicos**
19. **Métricas con barras visuales**
20. **Leyenda epistemológica**

### 🔄 In Progress:
1. Performance guardrails
2. Integration with main index.html

### ⏳ Pending:
1. Full integration testing
2. Testing suite
3. Documentation updates
4. User guide

---

## Next Steps

### Immediate (Week 1):
1. Refactor `archaeological_lupa.js` to use events
2. Implement replay mode UI
3. Add epistemic badges to results display

### Short-term (Week 2-3):
1. Refactor remaining components
2. Implement performance guardrails
3. Add visual differentiation (measurement vs inference)

### Medium-term (Month 1):
1. Complete testing suite
2. Performance optimization
3. User documentation

---

## Success Criteria

### Technical:
- ✅ Frontend modular y desacoplado
- ✅ Estado científico inalterable
- ✅ Reproducibilidad garantizada
- ⏳ Performance estable en sesiones largas
- ⏳ UX científicamente honesta

### Scientific:
- ✅ Diferenciación clara medición vs inferencia
- ✅ Etiquetado epistemológico visible
- ✅ Snapshots exportables
- ⏳ Replay mode funcional
- ⏳ Confidence decay visual

### User Experience:
- ⏳ Interfaz responsiva
- ⏳ Loading states claros
- ⏳ Error handling robusto
- ⏳ Tooltips informativos
- ⏳ Modo ligero disponible

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND ARCHITECTURE                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────┐             │
│  │ UI State     │         │ Scientific   │             │
│  │ (Mutable)    │         │ State        │             │
│  │              │         │ (Immutable)  │             │
│  │ - Modals     │         │ - Analysis   │             │
│  │ - Layers     │         │ - Phases     │             │
│  │ - Selection  │         │ - Epistemic  │             │
│  │ - View       │         │ - History    │             │
│  └──────┬───────┘         └──────┬───────┘             │
│         │                        │                      │
│         └────────┬───────────────┘                      │
│                  │                                      │
│         ┌────────▼────────┐                            │
│         │   Event Bus     │                            │
│         │  (Central Hub)  │                            │
│         └────────┬────────┘                            │
│                  │                                      │
│     ┌────────────┼────────────┐                        │
│     │            │            │                        │
│ ┌───▼───┐   ┌───▼───┐   ┌───▼───┐                    │
│ │ Lupa  │   │ 3D    │   │History│                    │
│ │Module │   │Viewer │   │Module │                    │
│ └───────┘   └───────┘   └───────┘                    │
│                                                          │
│                  ▲                                      │
│                  │                                      │
│         ┌────────┴────────┐                            │
│         │   BACKEND API   │                            │
│         │ (Source of      │                            │
│         │  Truth)         │                            │
│         └─────────────────┘                            │
└─────────────────────────────────────────────────────────┘
```

---

**Document Status**: Living Document  
**Last Updated**: January 27, 2026  
**Phase**: 1/6 Completed  
**Next Review**: February 2026
