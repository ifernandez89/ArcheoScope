# ArcheoScope Frontend Modules - Integration Guide
## How to Use the Refactored Event-Driven Modules

**Date**: January 27, 2026  
**Status**: Phase 2 Completed - Ready for Integration

---

## Overview

Los 4 módulos principales del frontend han sido refactorizados para usar el Event Bus:

1. **Archaeological Lupa Module** - Análisis detallado multi-sensor
2. **Viewer 3D Module** - Visualización 3D de anomalías
3. **LiDAR Availability Module** - Verificación de cobertura LiDAR
4. **History Module** - Gestión de historial de análisis

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    EVENT BUS (Central)                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐                  │
│  │ Scientific   │    │ UI State     │                  │
│  │ State        │    │              │                  │
│  └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                           │
│         └───────┬───────────┘                           │
│                 │                                       │
│     ┌───────────┼───────────┬───────────┬──────────┐   │
│     │           │           │           │          │   │
│ ┌───▼───┐  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐│
│ │ Lupa  │  │ 3D    │  │LiDAR  │  │History│  │ Main  ││
│ │Module │  │Viewer │  │Module │  │Module │  │ App   ││
│ └───────┘  └───────┘  └───────┘  └───────┘  └───────┘│
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Module Loading Order

### 1. Core Files (Load First)
```html
<!-- Event Bus -->
<script src="frontend/core/event_bus.js"></script>

<!-- State Management -->
<script src="frontend/state/scientific_state.js"></script>
<script src="frontend/state/ui_state.js"></script>
```

### 2. Modules (Load Second)
```html
<!-- Refactored Modules -->
<script src="frontend/modules/archaeological_lupa_module.js"></script>
<script src="frontend/modules/viewer_3d_module.js"></script>
<script src="frontend/modules/lidar_availability_module.js"></script>
<script src="frontend/modules/history_module.js"></script>
```

### 3. Main Application (Load Last)
```html
<!-- Main App -->
<script src="frontend/archaeological_app.js"></script>
```

---

## Usage Examples

### 1. Archaeological Lupa Module

#### Activar Lupa
```javascript
// Desde cualquier parte del código
eventBus.emit(EVENTS.LUPA_ACTIVATED, {
    coordinates: {
        lat: 64.2,
        lng: -51.7
    },
    analysisData: currentAnalysisData
});
```

#### Desactivar Lupa
```javascript
eventBus.emit(EVENTS.LUPA_DEACTIVATED);
```

#### Escuchar Resultados
```javascript
eventBus.on(EVENTS.LUPA_ANALYSIS_COMPLETED, (result) => {
    console.log('Lupa completada:', result);
    // result.coordinates
    // result.layersActive
});
```

#### Toggle de Capas
```javascript
// Activar/desactivar capa térmica
eventBus.emit(EVENTS.UI_LAYER_TOGGLED, {
    layer: 'lupa_thermal',
    visible: true
});
```

---

### 2. Viewer 3D Module

#### Abrir Visor 3D
```javascript
eventBus.emit(EVENTS.VIEWER_3D_OPENED, {
    anomalies: [
        {
            type: 'structure',
            name: 'Anomalía 1',
            confidence: 0.85
        },
        {
            type: 'mound',
            name: 'Anomalía 2',
            confidence: 0.72
        }
    ]
});
```

#### Cerrar Visor 3D
```javascript
eventBus.emit(EVENTS.VIEWER_3D_CLOSED);
```

#### Escuchar Carga de Datos
```javascript
eventBus.on(EVENTS.VIEWER_3D_DATA_LOADED, (result) => {
    console.log('Visor 3D listo:', result);
    // result.anomaliesCount
    // result.currentIndex
});
```

#### Navegación
```javascript
// Desde el módulo (acceso directo)
viewer3DModule.nextAnomaly();
viewer3DModule.previousAnomaly();

// Exportar screenshot
viewer3DModule.exportScreenshot();
```

---

### 3. LiDAR Availability Module

#### Verificar Disponibilidad (Automático)
```javascript
// Se activa automáticamente al seleccionar región
eventBus.emit(EVENTS.REGION_SELECTED, {
    center: {
        lat: 51.5,
        lng: -0.1
    }
});
```

#### Verificar Disponibilidad (Manual)
```javascript
const result = lidarAvailabilityModule.checkAvailability(51.5, -0.1);
console.log('LiDAR disponible:', result.available);
console.log('Regiones:', result.regions);
```

#### Escuchar Resultados
```javascript
eventBus.on('lidar:availability_checked', (result) => {
    if (result.available) {
        console.log(`✅ LiDAR disponible en ${result.regions.length} región(es)`);
        result.regions.forEach(region => {
            console.log(`  - ${region.name}: ${region.resolution}`);
        });
    } else {
        console.log('❌ LiDAR no disponible');
    }
});
```

#### Limpiar Cache
```javascript
lidarAvailabilityModule.clearCache();
```

---

### 4. History Module

#### Guardar Análisis (Automático)
```javascript
// Se guarda automáticamente al completar análisis
eventBus.emit(EVENTS.ANALYSIS_COMPLETED, {
    region: 'Nuuk, Groenlandia',
    coordinates: { lat: 64.2, lng: -51.7 },
    scientificOutput: {
        anthropic_probability: 0.327,
        anomaly_score: 0.750,
        recommended_action: 'discard',
        epistemic_mode: 'deterministic_scientific'
    }
});
```

#### Agregar Entrada Manual
```javascript
eventBus.emit(EVENTS.HISTORY_ENTRY_ADDED, {
    timestamp: new Date().toISOString(),
    region: 'Test Region',
    probability: 0.45,
    anomalyScore: 0.68,
    action: 'monitoring_targeted'
});
```

#### Seleccionar Entrada
```javascript
eventBus.emit(EVENTS.HISTORY_ENTRY_SELECTED, historyEntry);
```

#### Activar/Desactivar UI
```javascript
historyModule.activate();   // Abrir panel de historial
historyModule.deactivate(); // Cerrar panel
```

#### Exportar/Importar
```javascript
// Exportar
const json = historyModule.exportToJSON();
console.log(json);

// Importar
const success = historyModule.importFromJSON(jsonString);
```

#### Obtener Estadísticas
```javascript
const stats = historyModule.getStats();
console.log('Total entradas:', stats.totalEntries);
console.log('Por acción:', stats.byAction);
console.log('Probabilidad promedio:', stats.avgProbability);
```

---

## Event Flow Examples

### Complete Analysis Flow

```javascript
// 1. Usuario selecciona región
eventBus.emit(EVENTS.REGION_SELECTED, {
    bounds: { ... },
    center: { lat: 64.2, lng: -51.7 }
});

// 2. LiDAR module verifica disponibilidad (automático)
// → Emite 'lidar:availability_checked'

// 3. Usuario inicia análisis
eventBus.emit(EVENTS.ANALYSIS_STARTED, {
    coordinates: { lat: 64.2, lng: -51.7 }
});

// 4. Backend procesa y retorna datos
// → scientificState.updateFromBackend(backendData)
// → Emite EVENTS.SCIENTIFIC_DATA_UPDATED

// 5. Análisis completado
eventBus.emit(EVENTS.ANALYSIS_COMPLETED, {
    scientificOutput: { ... }
});

// 6. History module guarda automáticamente
// → Emite EVENTS.HISTORY_ENTRY_ADDED

// 7. Usuario activa lupa
eventBus.emit(EVENTS.LUPA_ACTIVATED, {
    coordinates: { ... },
    analysisData: { ... }
});

// 8. Lupa completa análisis
// → Emite EVENTS.LUPA_ANALYSIS_COMPLETED
```

---

## State Access Patterns

### ✅ CORRECTO: Leer estado
```javascript
// Leer scientific state
const analysis = scientificState.getCurrentAnalysis();
const output = scientificState.getScientificOutput();
const epistemic = scientificState.getEpistemicLabels();

// Leer UI state
const isLupaOpen = uiState.isModalOpen('lupa');
const hasSelection = uiState.hasSelection();
```

### ❌ INCORRECTO: Modificar estado directamente
```javascript
// ❌ NO HACER ESTO
scientificState.data.currentAnalysis = newData;
uiState.state.modals.lupaActive = true;
```

### ✅ CORRECTO: Modificar estado vía eventos
```javascript
// ✅ HACER ESTO
eventBus.emit(EVENTS.SCIENTIFIC_DATA_UPDATED, newData);
uiState.openModal('lupa');
```

---

## Performance Considerations

### Lupa Module
- **Throttling**: Máximo 1 análisis por segundo
- **Cleanup**: Automático al cerrar (Leaflet layers)

### Viewer 3D Module
- **FPS Limit**: 30 FPS máximo
- **Geometry Limit**: 10,000 geometrías máximo
- **Cleanup**: Automático al cerrar (Three.js resources)

### LiDAR Module
- **Cache**: 1 hora de duración
- **Precision**: 2 decimales para cache key

### History Module
- **Max Entries**: 100 entradas
- **Storage**: localStorage automático
- **Sync**: Con scientificState.history

---

## Debugging

### Event Log
```javascript
// Ver log de eventos
const log = eventBus.getEventLog();
console.table(log);

// Limpiar log
eventBus.clearEventLog();

// Snapshot del bus
const snapshot = eventBus.getSnapshot();
console.log('Listeners activos:', snapshot.activeListeners);
```

### Module State
```javascript
// Estado de cada módulo
console.log('Lupa:', archaeologicalLupaModule.getState());
console.log('Viewer 3D:', viewer3DModule.getState());
console.log('LiDAR:', lidarAvailabilityModule.getState());
console.log('History:', historyModule.getState());
```

### Scientific State
```javascript
// Verificar datos científicos
console.log('Has data:', scientificState.hasData());
console.log('Is reproducible:', scientificState.isReproducible());
console.log('Used AI:', scientificState.usedAI());

// Exportar snapshot
const snapshot = scientificState.exportSnapshot();
console.log(snapshot);
```

---

## Migration from Old Code

### Old Pattern (Direct DOM Access)
```javascript
// ❌ Código antiguo
function openLupaModal() {
    const modal = document.getElementById('lupaModal');
    modal.classList.add('active');
    initLupaMap();
}
```

### New Pattern (Event-Driven)
```javascript
// ✅ Código nuevo
function openLupaModal() {
    eventBus.emit(EVENTS.LUPA_ACTIVATED, {
        coordinates: selectedCoordinates,
        analysisData: currentAnalysisData
    });
}
```

### Old Pattern (Global Variables)
```javascript
// ❌ Código antiguo
let currentAnalysis = null;
let lupaMap = null;

function updateAnalysis(data) {
    currentAnalysis = data;
    if (lupaMap) {
        updateLupaLayers();
    }
}
```

### New Pattern (State Management)
```javascript
// ✅ Código nuevo
scientificState.updateFromBackend(data);
// Los módulos se actualizan automáticamente vía eventos
```

---

## Testing

### Unit Tests (Recommended)
```javascript
// Test Event Bus
test('EventBus emits and receives events', () => {
    let received = null;
    eventBus.on('test:event', (data) => { received = data; });
    eventBus.emit('test:event', { test: true });
    expect(received).toEqual({ test: true });
});

// Test Scientific State
test('ScientificState only updates from backend', () => {
    const data = { scientific_output: { ... } };
    scientificState.updateFromBackend(data);
    expect(scientificState.hasData()).toBe(true);
});

// Test Modules
test('Lupa module activates correctly', () => {
    eventBus.emit(EVENTS.LUPA_ACTIVATED, { ... });
    expect(archaeologicalLupaModule.isActive).toBe(true);
});
```

---

## Next Steps

### Phase 3: Reproducibility Mode (Next)
1. Implementar UI para replay mode
2. Timeline de eventos
3. Exportar/Importar snapshots completos

### Phase 4: Epistemic Integrity
1. Diferenciación visual medición vs inferencia
2. Badges epistemológicos
3. Confidence decay visual

### Phase 5: Performance & Safety
1. Implementar guardrails completos
2. Memory management
3. Fallback degradado

---

## Support

Para preguntas o issues:
1. Revisar este documento
2. Verificar event log: `eventBus.getEventLog()`
3. Verificar estado de módulos: `module.getState()`
4. Revisar `FRONTEND_REFACTOR_PLAN.md`

---

**Document Status**: Living Document  
**Last Updated**: January 27, 2026  
**Phase**: 2/6 Completed  
**Next Review**: February 2026
