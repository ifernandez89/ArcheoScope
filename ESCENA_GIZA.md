# 🏜️ Escena de Giza - Las Tres Pirámides

## 📍 Ubicación
**Coordenadas:** 29.9792°N, 31.1342°E (Meseta de Giza, Egipto)

## 🎮 Activación
La escena se activa automáticamente cuando el jugador viaja a las coordenadas de Giza (±0.05° de tolerancia).

## 🏛️ Elementos de la Escena

### 1. 🔺 Gran Pirámide de Keops (Khufu)
- **Posición:** Centro de la escena (0, 0, 0)
- **Dimensiones:** 138m base × 88m altura (60% escala real)
- **Escala real:** 230m × 146m
- **Características:**
  - Alineación cardinal casi perfecta (~0.05° de error)
  - Cada cara mira exactamente: Norte, Sur, Este, Oeste
  - Ligera concavidad en las caras (detalle histórico real)
  - Entrada original en cara norte a 17m de altura
  - Bloques visibles en las primeras 8 filas
  - Material: Caliza amarillenta (núcleo expuesto)

### 2. 🔺 Pirámide de Kefrén (Khafre)
- **Posición:** (-150, 0, -150) - Al suroeste
- **Dimensiones:** 130m base × 86m altura
- **Características:**
  - Conserva parte del revestimiento blanco en la cima
  - Caliza blanca de Tura (originalmente cubría toda la pirámide)
  - Alineación cardinal idéntica a Keops

### 3. 🔺 Pirámide de Micerino (Menkaure)
- **Posición:** (-220, 0, -220) - Más al suroeste
- **Dimensiones:** 65m base × 40m altura
- **Características:**
  - La más pequeña de las tres
  - Sin revestimiento visible
  - Misma alineación cardinal

### 4. 🦁 La Gran Esfinge
- **Posición:** (100, 0, 50) - Al este de las pirámides
- **Orientación:** Mira hacia el Este (salida del sol en equinoccio)
- **Dimensiones:** 73m largo × 20m alto
- **Características:**
  - Cuerpo de león, cabeza humana (faraón Kefrén)
  - Tallada en roca caliza natural
  - Guardiana del complejo funerario
  - Interacción disponible al acercarse (15m)

### 5. 🏛️ Templo del Valle
- **Posición:** (120, 0, 50) - Junto a la Esfinge
- **Dimensiones:** 40m × 30m × 10m altura
- **Características:**
  - Estructura megalítica de granito
  - Columnas interiores
  - Conectado originalmente con la pirámide de Kefrén

## 🧭 Alineación Astronómica

### Orientación Cardinal
Las tres pirámides están alineadas con precisión astronómica:
- **Error de orientación:** ~0.05° (increíble para 2500 a.C.)
- **Método usado:** Observación de estrellas circumpolares
- **Cada cara mira exactamente:**
  - Norte: Estrella Polar (Thuban en esa época)
  - Sur: Meridiano celeste
  - Este: Salida del sol en equinoccio
  - Oeste: Puesta del sol en equinoccio

### Alineación con Orión
Las tres pirámides están posicionadas para reflejar las tres estrellas del Cinturón de Orión:
- **Keops** → Alnitak
- **Kefrén** → Alnilam
- **Micerino** → Mintaka

Esta teoría (Correlación de Orión) sugiere que el complejo de Giza es un mapa estelar terrestre.

## 🎨 Detalles Técnicos

### Materiales
1. **Núcleo interno (visible hoy):**
   - Caliza local amarillenta
   - Rugosa e irregular
   - Color: #d4a574 (beige/arena/ocre)
   - Roughness: 0.9

2. **Revestimiento exterior (perdido):**
   - Caliza blanca de Tura
   - Pulida y reflectante
   - Color: #f5f5dc (blanco hueso)
   - Roughness: 0.3
   - Solo visible en cima de Kefrén

### Optimización
- **Bloques:** No se modelan los 2.3 millones de bloques reales
- **Método:** Geometría simplificada + bloques visibles solo en base
- **Filas visibles:** 8 primeras filas (optimización GPU)
- **Bloques por cara:** Cada 3 bloques (sampling)

### Concavidad de las Caras
Detalle histórico real implementado:
- Las caras no son perfectamente planas
- Están ligeramente hundidas hacia el centro
- Factor de concavidad: 0.3
- Propósito original: Estabilidad estructural y precisión visual

## 🎮 Uso en el Juego

### Misiones Potenciales
- **Cámara del Rey:** Exploración interior de la Gran Pirámide
- **Secretos de la Esfinge:** Descubrir cámaras ocultas
- **Observatorio Astronómico:** Usar la alineación para navegación estelar
- **Portal Antiguo:** Conexión con otras civilizaciones
- **Textos de las Pirámides:** Descifrar jeroglíficos

### Interacciones
- **Esfinge:** Diálogo/acertijo al acercarse
- **Entrada de pirámides:** Acceso a cámaras interiores
- **Templo del Valle:** Rituales o descubrimientos

### Navegación
- La alineación cardinal perfecta sirve como brújula natural
- La Esfinge siempre mira al Este (referencia de orientación)

## 📊 Comparación de Escalas

| Elemento | Escala Real | Escala Juego (60%) | Razón |
|----------|-------------|-------------------|-------|
| Gran Pirámide | 230m × 146m | 138m × 88m | Balance visual |
| Kefrén | 215m × 143m | 130m × 86m | Proporción |
| Micerino | 108m × 66m | 65m × 40m | Optimización |
| Esfinge | 73m × 20m | 73m × 20m | Escala real |

## 🌟 Datos Curiosos Implementados

1. **Concavidad de caras:** Las caras están ligeramente hundidas (casi imperceptible)
2. **Revestimiento de Kefrén:** Única pirámide que conserva parte del revestimiento blanco
3. **Orientación de Esfinge:** Mira exactamente al Este (equinoccio)
4. **Entrada de Keops:** 17m de altura en cara norte (históricamente preciso)
5. **Alineación Orión:** Posición relativa refleja el Cinturón de Orión

## 🔮 Futuras Expansiones

### Cámaras Interiores
- Cámara del Rey
- Cámara de la Reina
- Gran Galería
- Pasajes ascendentes/descendentes

### Eventos Astronómicos
- Alineación solar en equinoccios
- Sombra de la Esfinge
- Luz penetrando cámaras en fechas específicas

### Misterios
- Cámaras ocultas (detectadas por muografía)
- Shafts estelares apuntando a Orión y Sirio
- Conexión con otros sitios megalíticos

## 📝 Notas de Implementación

### Archivo
`viewer3d/components/GizaScene.tsx`

### Dependencias
- Three.js geometrías: ConeGeometry, BoxGeometry, CylinderGeometry
- useGLTF para modelo de Esfinge (fallback a geometría simple)
- Detección de proximidad con useFrame

### Integración
Se activa automáticamente en `ImmersiveScene.tsx` cuando:
```typescript
location.lat ≈ 29.9792 && location.lon ≈ 31.1342
```

### Performance
- Geometrías memoizadas con useMemo
- Bloques optimizados (sampling cada 3)
- Shadows habilitados solo en elementos principales
- Modelo de Esfinge con LOD si está disponible

---

**Creado:** 2026-03-10
**Versión:** 1.0
**Estado:** ✅ Implementado y funcional
