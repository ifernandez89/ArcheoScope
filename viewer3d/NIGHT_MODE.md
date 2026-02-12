# 🌙 Modo Nocturno - Documentación

## Implementación Completada

El modo nocturno se activa automáticamente cuando el botón "Simulación Solar" está en OFF.

## Características

### 🌌 Cielo Nocturno
- Color: `#0a0a1a` (negro azulado profundo)
- Contrasta con el modo día: `#4a7ba7` (azul cielo)

### ⭐ Estrellas
- 15,000 estrellas procedurales
- Colores variados (tonos blancos/azulados)
- Distribución aleatoria en esfera de 2000 unidades
- Solo visibles cuando `solarSimulation = false`

### 💡 Iluminación Nocturna

#### Luz Ambiental
- Intensidad: 0.3 (reducida)
- Color: `#4a5a8a` (azul lunar)

#### Luz Direccional (Luna)
- Intensidad: 0.8
- Color: `#b0c4de` (azul claro lunar)
- Proyecta sombras suaves

#### Luces Puntuales (Fogata/Antorchas)
- Luz 1: Posición `[0, 2, 3]`, intensidad 2.0, color `#ff8c00` (naranja)
- Luz 2: Posición `[-5, 3, -5]`, intensidad 1.5, color `#ff6600` (naranja rojizo)
- Iluminan al avatar para mantener visibilidad

### 🌫️ Niebla Atmosférica
- Color nocturno: `#0a0a1a` (igual que el cielo)
- Rango: 40-120 unidades
- Crea profundidad y atmósfera

## Contraste Día/Noche

| Elemento | Día | Noche |
|----------|-----|-------|
| Cielo | `#4a7ba7` | `#0a0a1a` |
| Niebla | `#6b8ba7` | `#0a0a1a` |
| Luz Ambiental | 1.5 blanca | 0.3 azulada |
| Luz Direccional | 3.0 solar | 0.8 lunar |
| Estrellas | ❌ | ✅ |

## Uso

```tsx
// Toggle entre día y noche
<button onClick={() => setSolarSimulation(!solarSimulation)}>
  {solarSimulation ? '☀️ Simulación Solar ON' : '🌙 Simulación Solar OFF'}
</button>
```

## Experiencia Visual

### Modo Día
- Brillante y claro
- Sombras definidas
- Colores vibrantes
- Sin estrellas

### Modo Noche
- Oscuro y atmosférico
- Iluminación lunar suave
- Fogatas iluminan al avatar
- Campo estelar visible
- Sensación mística y arqueológica

## Notas Técnicas

- Las estrellas usan `THREE.Points` con geometría procedural
- Material con `vertexColors` para variación de color
- `depthWrite: false` para evitar conflictos de profundidad
- Geometría y material en `useMemo` para optimización
- Transición instantánea al cambiar modo (sin fade)

## Mejoras Futuras (Opcionales)

- [ ] Añadir luna visible como objeto 3D
- [ ] Transición gradual día/noche con fade
- [ ] Estrellas parpadeantes (twinkle effect)
- [ ] Vía Láctea visible en ciertas latitudes
- [ ] Constelaciones arqueológicas (Orión, Cruz del Sur, etc.)
