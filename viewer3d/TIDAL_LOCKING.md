# 🌙 Tidal Locking (Bloqueo por Marea)

## ¿Qué es el Tidal Locking?

El **tidal locking** o **bloqueo por marea** es un fenómeno físico real donde un cuerpo celeste siempre muestra la misma cara a otro cuerpo alrededor del cual orbita.

### Ejemplo Real: La Luna y la Tierra

La Luna está bloqueada por marea con la Tierra. Por eso:
- ✅ Siempre vemos la misma cara de la Luna desde la Tierra
- ✅ Los mismos cráteres son visibles cada noche
- ❌ Nunca vemos el "lado oscuro" de la Luna desde la Tierra

## La Física Detrás

### Regla Fundamental

```
Velocidad de rotación = Velocidad orbital
```

Si la Luna avanza un ángulo `θ` alrededor de la Tierra, debe rotar sobre su eje el mismo `θ`.

### Error Común

Muchos desarrolladores hacen esto:

```typescript
// ❌ INCORRECTO - Rompe el bloqueo
moon.position.x = Math.cos(angle) * distance
moon.position.z = Math.sin(angle) * distance
moon.rotation.y = 0 // ← Rotación constante = MALO
```

Resultado: La cara visible cambia constantemente (físicamente imposible).

### Solución Correcta

```typescript
// ✅ CORRECTO - Tidal locking real
const orbitAngle = time * orbitSpeed

// Posición orbital
moon.position.x = Math.cos(orbitAngle) * distance
moon.position.z = Math.sin(orbitAngle) * distance

// Rotación sincronizada
moon.rotation.y = orbitAngle // ← Mismo ángulo = CORRECTO
```

## Implementación en SimpleMoon.tsx

Nuestro componente `SimpleMoon.tsx` implementa tidal locking real:

```typescript
useFrame((state) => {
  const orbitAngle = time * orbitSpeed
  
  // Órbita
  moonRef.current.position.x = Math.cos(orbitAngle) * orbitRadius
  moonRef.current.position.z = Math.sin(orbitAngle) * orbitRadius
  
  // Tidal locking: rotación = órbita
  moonRef.current.rotation.y = orbitAngle
})
```

## Cómo Verificar que Funciona

### Test Visual

1. Acelera mucho la velocidad orbital (ej: `orbitSpeed = 0.5`)
2. Coloca la cámara en posición fija
3. Observa la Luna mientras orbita

**Resultado esperado:**
- ✅ Los mismos cráteres siempre visibles
- ✅ La textura no "gira" sobre sí misma
- ✅ La cara visible permanece constante

**Si falla:**
- ❌ Los cráteres cambian constantemente
- ❌ La textura parece "girar"
- ❌ El bloqueo está roto

## Ajuste de Orientación

Si la cara visible queda al revés:

```typescript
// Cambiar el signo
moon.rotation.y = -orbitAngle // En lugar de +orbitAngle
```

O si la textura está rotada 180°:

```typescript
moon.rotation.y = orbitAngle + Math.PI
```

## Método Alternativo: Estructura Jerárquica

Más elegante para sistemas complejos:

```typescript
// Estructura
EarthPivot
  └── MoonOrbitPivot (rota)
        └── MoonMesh (orientado hacia centro)

// Código
moonOrbitPivot.rotation.y = orbitAngle
moonMesh.lookAt(earth.position) // Siempre mira a la Tierra
```

Este método es visualmente robusto y garantiza el bloqueo.

## Detalles Avanzados

### Libración Lunar

La Luna real tiene una pequeña **libración** (oscilación aparente) debido a:
- Órbita elíptica (no circular perfecta)
- Inclinación del eje lunar
- Velocidad orbital variable

**No implementado aún** - Primero perfeccionamos el bloqueo básico.

### Inclinación Orbital

Nuestra implementación incluye la inclinación real de ~5°:

```typescript
const orbitalInclination = 5 * (Math.PI / 180)
moonRef.current.position.y = Math.sin(orbitAngle) * orbitRadius * Math.sin(orbitalInclination)
```

## Referencias Físicas

- **Período orbital Luna**: ~27.3 días
- **Período de rotación Luna**: ~27.3 días (¡idéntico!)
- **Inclinación orbital**: ~5.14°
- **Distancia real**: ~384,400 km (30 diámetros terrestres)
- **Nuestra distancia emocional**: 12 radios terrestres (visual)

## Importancia

Implementar tidal locking correctamente:
- ✅ Respeta la física real
- ✅ Eleva el nivel del proyecto
- ✅ Demuestra comprensión astronómica
- ✅ Hace la simulación creíble
- ✅ Permite expansión futura (Marte, Venus, etc.)

---

**Última actualización**: Implementación de tidal locking real en SimpleMoon.tsx
