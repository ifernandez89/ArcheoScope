# 🔭 Sistema de Zoom Narrativo

## Filosofía

No es un simple alejamiento de cámara.  
Es una **revelación progresiva del cosmos**.  
Cada nivel tiene su propia escala coherente.

## Los 4 Niveles

### Nivel 0: Mundo 🌍
**Distancia de cámara**: 8-30 unidades  
**Escala**: Planetaria pura

**Elementos visibles:**
- Tierra con textura 8K
- Luna orbitando con tidal locking
- Estrellas de fondo

**Ambiente:**
- Profundo
- Sonido suave
- Enfoque íntimo

**Sin:**
- Órbitas visibles
- Planos orbitales
- Otros cuerpos celestes

---

### Nivel 1: Contexto Orbital 🌙
**Distancia de cámara**: 30-50 unidades  
**Escala**: Transición (planetaria → solar)

**Elementos que aparecen:**
- ✨ Órbita lunar (línea tenue azul)
- ✨ Plano orbital (disco muy sutil)

**Transición:**
- Fade in suave de elementos
- Sonido se vuelve más grave
- Sin texto, solo revelación
- Interpolación de escalas comienza

**Propósito:**
- Revelar la mecánica orbital
- Preparar para el cambio de escala
- Mantener coherencia visual

---

### Nivel 2: Aparición Solar ☀️
**Distancia de cámara**: 50-100 unidades  
**Escala**: Solar

**Elementos que aparecen:**
- ✨ Sol (distante, no gigante)
- ✨ Órbita terrestre (línea elíptica)
- ✨ Plano eclíptico

**Cambios:**
- La Tierra se hace pequeña
- El Sol aparece con glow sutil
- Luz puntual desde el Sol
- Sensación cósmica comienza

**Escala emocional:**
- Sol: 3 unidades de radio (no 109 Tierras)
- Distancia: 80 unidades (no 23,500 radios terrestres)
- Órbita terrestre: 80 unidades de radio

**Propósito:**
- Revelar el sistema Tierra-Sol
- Mostrar la órbita planetaria
- Introducir el plano eclíptico

---

### Nivel 3: Sistema Interno 🪐
**Distancia de cámara**: 100+ unidades  
**Escala**: Solar expandida

**Elementos que aparecen:**
- ✨ Venus (si está cerca angularmente)
- ✨ Marte (si está cerca angularmente)
- ✨ Plano eclíptico más visible

**Filosofía:**
- No como catálogo
- Que parezca descubrimiento
- Solo planetas cercanos angularmente
- Respeta posiciones reales (futuro)

**Propósito:**
- Revelar el sistema interno
- Mantener sensación de exploración
- No saturar visualmente

---

## Escalas Segmentadas

### ¿Por qué no usar escala real única?

**Problema con escala real:**
```
Sol: 109 diámetros terrestres
Distancia Tierra-Sol: 23,500 radios terrestres
```

Si respetas esto literal:
- ❌ La Tierra sería invisible
- ❌ La Luna sería un píxel
- ❌ El Sol estaría inalcanzable
- ❌ Inviable visualmente

### Solución: Escalas por Contexto

```typescript
scaleMode = "planetary" | "transition" | "solar"

if (cameraDistance > 30) {
  transitionToSolarScale()
}
```

**Durante transición:**
- Interpola tamaños
- Interpola distancias
- Oscurece ligeramente el fondo
- Cambia textura estelar (futuro)
- Parece cambio de "marco de referencia"

### Esto es válido

✅ Usado en visualización científica  
✅ Planetarios profesionales lo hacen  
✅ NASA lo usa en simulaciones educativas  
✅ Mantiene coherencia emocional

---

## Implementación Técnica

### Hook Principal

```typescript
const zoomState = useNarrativeZoom()

// Retorna:
{
  level: 'mundo' | 'orbital' | 'solar' | 'sistema',
  scaleMode: 'planetary' | 'transition' | 'solar',
  progress: 0-1, // Progreso dentro del nivel
  cameraDistance: number,
  transitionFactor: 0-1 // Para interpolación
}
```

### Componentes Reactivos

Cada elemento responde al estado de zoom:

```typescript
<LunarOrbit visible={zoomState.level !== 'mundo'} />
<SimpleSun visible={zoomState.level === 'solar'} scaleMode={zoomState.scaleMode} />
```

### Fade In/Out Suave

Todos los elementos usan interpolación:

```typescript
useFrame(() => {
  const targetOpacity = visible ? 0.15 : 0
  const currentOpacity = material.opacity
  material.opacity = THREE.MathUtils.lerp(currentOpacity, targetOpacity, 0.05)
})
```

---

## Estética Contemplativa

### Principios

✅ **Opacidad baja** - Líneas sutiles, no brillantes  
✅ **Colores fríos** - Azules, no neones  
✅ **Sin glow exagerado** - Sutil, no arcade  
✅ **Revelación progresiva** - No todo a la vez  
✅ **Respira** - Espacio negativo importante

### Órbitas

```typescript
<lineBasicMaterial
  color="#4a9eff"      // Azul frío
  transparent
  opacity={0.08}        // Muy sutil
  depthWrite={false}
  blending={THREE.AdditiveBlending}
/>
```

### Planos

```typescript
<meshBasicMaterial
  color="#1a2a4a"      // Azul oscuro
  transparent
  opacity={0.02}        // Casi invisible
  side={THREE.DoubleSide}
  depthWrite={false}
/>
```

---

## Audio (Futuro)

### Zoom Out
- Reducir frecuencias altas
- Aumentar grave profundo
- Quitar pájaros
- Introducir vacío

### Zoom In
- Vuelve viento
- Aparece textura ambiental
- Sonidos planetarios

**Propósito:**  
Dar sensación de escala a través del sonido.

---

## Mejoras Futuras

### Nivel 2: Aparición Solar
- [ ] Sombra real de la Tierra sobre la Luna
- [ ] Eclipse lunar cuando la Luna pasa detrás
- [ ] Rayos solares sutiles

### Nivel 3: Sistema Interno
- [ ] Venus con textura real
- [ ] Marte con textura real
- [ ] Posiciones orbitales reales (efemérides)
- [ ] Solo mostrar planetas cercanos angularmente

### Transiciones
- [ ] Cambio de textura estelar (más profunda en niveles altos)
- [ ] Oscurecimiento sutil del fondo
- [ ] Partículas cósmicas en transición

### Audio
- [ ] Drone ambiental que cambia con el nivel
- [ ] Frecuencias graves en niveles profundos
- [ ] Silencio cósmico en nivel sistema

---

## Verificación

### ¿Cómo saber si funciona?

1. **Nivel Mundo (8-30 unidades)**
   - Solo Tierra y Luna visibles
   - Sin órbitas ni planos

2. **Nivel Orbital (30-50 unidades)**
   - Órbita lunar aparece suavemente
   - Plano orbital sutil visible

3. **Nivel Solar (50-100 unidades)**
   - Sol aparece a la distancia
   - Órbita terrestre visible
   - Plano eclíptico sutil

4. **Nivel Sistema (100+ unidades)**
   - Plano eclíptico más visible
   - Sistema completo revelado

### Test de Transición

```typescript
// Acelerar para testing
const orbitSpeed = 0.5 // En SimpleMoon.tsx

// Observar:
// - Fade in/out suave de elementos
// - Sin saltos bruscos
// - Escalas coherentes en cada nivel
```

---

## Filosofía Final

> "No llenes el espacio con líneas brillantes.  
> Tu pieza es contemplativa, no arcade.  
> Que todo respire."

Este sistema respeta:
- ✅ Física real (donde importa)
- ✅ Coherencia emocional (donde la física es inviable)
- ✅ Revelación progresiva (narrativa)
- ✅ Estética minimalista (contemplación)

---

**Última actualización**: Implementación del sistema de zoom narrativo con 4 niveles
