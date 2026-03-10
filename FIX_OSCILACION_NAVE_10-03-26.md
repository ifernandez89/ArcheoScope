# Fix: Oscilación de Nave - 10/03/2026

## Problema
La nave presentaba un movimiento de oscilación o "terremoto" leve cuando estaba quieta, incluso con el clima desactivado.

## Causa Identificada
Dos fuentes de oscilación en `WalkableAvatar.tsx`:

1. **Oscilación vertical intencional** (línea 471)
   - `Math.sin(timeAccumulator.current * 2) * 0.15`
   - Simulaba flotación pero causaba meneo constante

2. **Ajuste continuo de altura** (línea 475)
   - `group.current.position.y += (finalTargetHeight - group.current.position.y) * 8 * delta`
   - Se ejecutaba en cada frame sin umbral mínimo
   - Micro-variaciones en `targetHeight` causaban oscilación visible

## Solución Implementada

### 1. Desactivación de Oscilación Vertical
```typescript
// Antes:
const oscillation = Math.sin(timeAccumulator.current * 2) * 0.15

// Después:
const oscillation = 0  // Desactivada para evitar meneo
```

### 2. Umbral de Ajuste de Altura
```typescript
// Antes:
group.current.position.y += (finalTargetHeight - group.current.position.y) * 8 * delta

// Después:
const heightDifference = Math.abs(finalTargetHeight - group.current.position.y)
if (heightDifference > 0.01) {  // Solo ajustar si diferencia > 1cm
  group.current.position.y += (finalTargetHeight - group.current.position.y) * 8 * delta
}
```

## Resultados

✅ Nave completamente estable cuando está quieta
✅ Sin oscilaciones o movimientos no deseados
✅ Ajuste de altura solo cuando es necesario (diferencia > 1cm)
✅ Experiencia de usuario más profesional y estable

## Archivo Modificado
- `viewer3d/components/WalkableAvatar.tsx`

## Notas Técnicas
- El umbral de 0.01 unidades (1cm) es suficiente para eliminar micro-oscilaciones
- El ajuste de altura sigue funcionando para cambios significativos de terreno
- Las animaciones de movimiento (cuando isMoving = true) no se ven afectadas
