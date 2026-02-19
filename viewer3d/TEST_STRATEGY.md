# 🧪 Estrategia de Testing - ArcheoScope

## 📋 Filosofía: Testing Inteligente

No buscamos 80% de coverage ahora. Nos enfocamos en **lógica determinista del núcleo**.

### ✅ Qué testeamos (Etapa 1)

1. **Store Zustand** (`scene-store.test.ts`)
   - Estado inicial
   - Mutaciones
   - Toggles
   - Secuencias de estado

2. **Biome Detector** (`biome-detector.test.ts`)
   - Detección de biomas por coordenadas
   - Regiones específicas (Ártico, Sahara, etc.)
   - Helpers (isIcyRegion, getSkyColor, etc.)
   - Casos edge

3. **ArcheoEngine** (`ArcheoEngine.test.ts`)
   - Singleton pattern
   - Búsqueda de sitios
   - Cálculo de distancias (Haversine)
   - Caché de modelos
   - Filtros por cultura/período

### ❌ Qué NO testeamos (por ahora)

- Three.js rendering
- React components
- Shaders
- Efectos visuales
- Interacciones de usuario

---

## 🚀 Comandos

### Instalar dependencias
```bash
cd viewer3d
npm install
```

### Ejecutar tests
```bash
npm test                 # Modo watch
npm run test:ui          # UI interactiva
npm run test:coverage    # Con coverage report
```

### Ejecutar tests específicos
```bash
npm test scene-store     # Solo store
npm test biome-detector  # Solo biome
npm test ArcheoEngine    # Solo engine
```

---

## 📊 Coverage Esperado (Etapa 1)

| Módulo | Coverage | Tests |
|--------|----------|-------|
| scene-store.ts | ~95% | 20+ tests |
| biome-detector.ts | ~90% | 30+ tests |
| ArcheoEngine.ts | ~85% | 25+ tests |

**Total**: ~75 tests cubriendo lógica crítica

---

## 🎯 Estructura de Tests

### scene-store.test.ts
```
✓ Estado inicial
✓ Mutaciones de modelo (loading, progress)
✓ Mutaciones de cámara (mode, autoRotate)
✓ Mutaciones de animación
✓ Mutaciones de timeline
✓ Toggles de UI (controls, grid, stats)
```

### biome-detector.test.ts
```
✓ Regiones polares (Ártico, Antártico)
✓ Glaciares específicos (Groenlandia, Himalaya, etc.)
✓ Regiones volcánicas (Hawái, Andes, Japón)
✓ Desiertos (Sahara, Atacama)
✓ Océano
✓ Helpers (isIcyRegion, getSkyColor, getFogColor)
✓ Casos edge (límites, coordenadas extremas)
```

### ArcheoEngine.test.ts
```
✓ Singleton pattern
✓ getAllSites
✓ getSiteById
✓ getNearestSites (con ordenamiento por distancia)
✓ Cálculo Haversine
✓ Caché de modelos
✓ Búsqueda por cultura
✓ Búsqueda por período
```

---

## 🔧 Configuración

### vitest.config.ts
- Environment: Node (no necesitamos jsdom)
- Coverage: v8 provider
- Alias: `@/` apunta a raíz del proyecto
- Include: Solo archivos `*.test.ts` y `*.test.tsx`

### Mocks
- `archaeological-sites.json`: Mock con 4 sitios de prueba
- No mocks de Three.js (no testeamos rendering)

---

## 📈 Próximas Etapas

### Etapa 2 (Futuro)
- Tests de integración para componentes React
- Tests de shaders (si es necesario)
- Tests E2E con Playwright

### Etapa 3 (Futuro)
- Performance benchmarks
- Visual regression tests
- Accessibility tests

---

## 💡 Principios

1. **Tests rápidos**: < 1s para toda la suite
2. **Tests deterministas**: Sin flakiness
3. **Tests legibles**: Nombres descriptivos
4. **Tests aislados**: Sin dependencias entre tests
5. **Tests útiles**: Detectan bugs reales

---

## 🐛 Debugging Tests

### Ver output detallado
```bash
npm test -- --reporter=verbose
```

### Ejecutar un solo test
```bash
npm test -- -t "debe detectar Ártico"
```

### Watch mode con filtro
```bash
npm test biome
```

---

## ✅ Checklist Pre-Commit

- [ ] Todos los tests pasan
- [ ] No hay console.log en tests
- [ ] Coverage > 80% en módulos testeados
- [ ] Tests son deterministas (correr 3 veces)

---

**Herramienta**: Vitest (más rápido que Jest)  
**Filosofía**: Testing inteligente, no exhaustivo  
**Objetivo**: Confianza en lógica del núcleo
