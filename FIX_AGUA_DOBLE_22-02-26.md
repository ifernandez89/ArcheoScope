# FIX: Agua Doble - 22 de Febrero 2026

## PROBLEMA IDENTIFICADO

Había DOS planos de agua superpuestos causando el efecto visual de "dos colores mezclados":

1. **RealisticWater** (azul oscuro) - Renderizado por `EnvironmentSystem` en posición y=-0.5
2. **VolcanicTerrain/IceTerrain** (azul claro) - Terreno procedural que NO se ocultaba en océano

## CAUSA RAÍZ

La lógica `isInOcean` en `VolcanicTerrain.tsx` tenía una condición redundante que causaba confusión:

```typescript
// ANTES - Lógica redundante
if (lon < -70) {
  // ... exclusiones ...
  return true
}
// ... más condiciones ...
if (Math.abs(lat) < 60 && (lon < -100 || lon > 150)) {
  return true  // ❌ Esta condición era redundante
}
```

La segunda condición era innecesaria porque ya estaba cubierta por la primera (lon < -70 incluye lon < -100).

Además, `IceTerrain.tsx` NO tenía ninguna lógica `isInOcean`, por lo que siempre se renderizaba incluso en océano.

## SOLUCIÓN IMPLEMENTADA

### 1. Simplificación de VolcanicTerrain.tsx

Eliminé la condición redundante y simplifiqué la lógica:

```typescript
// DESPUÉS - Lógica simplificada
const isInOcean = useMemo(() => {
  if (!location) return false
  
  const { lat, lon } = location
  
  // OCÉANO PACÍFICO CENTRAL (lon < -70)
  if (lon < -70) {
    // Exclusiones de costas...
    return true  // ✅ Incluye (8.7783°, -144.8885°)
  }
  
  // Océano Pacífico occidental (lon > 100)
  // Océano Atlántico central
  // Océano Índico
  
  return false  // ✅ Por defecto es tierra
}, [location])
```

### 2. Agregado de lógica isInOcean a IceTerrain.tsx

Implementé la MISMA lógica de detección de océano en `IceTerrain.tsx`:

```typescript
const isInOcean = useMemo(() => {
  // ... misma lógica que VolcanicTerrain ...
}, [location])

// No renderizar terreno si está en océano abierto
if (isInOcean) {
  return null
}
```

## ARCHIVOS MODIFICADOS

1. `viewer3d/components/VolcanicTerrain.tsx`
   - Simplificada lógica `isInOcean`
   - Eliminada condición redundante

2. `viewer3d/components/IceTerrain.tsx`
   - Agregada lógica `isInOcean` completa
   - Agregado `return null` cuando está en océano

## RESULTADO ESPERADO

Ahora en el Océano Pacífico (8.7783°, -144.8885°):

- ✅ Solo se renderiza `RealisticWater` (azul oscuro con shader realista)
- ✅ NO se renderiza `VolcanicTerrain` (detecta océano correctamente)
- ✅ NO se renderiza `IceTerrain` (detecta océano correctamente)
- ✅ Agua uniforme sin dos colores mezclados

## TESTING

Para verificar el fix:

1. Iniciar servidor de desarrollo: `npm run dev` (en viewer3d/)
2. Navegar a http://localhost:3000
3. Usar el panel de coordenadas para ir a "🌊 Océano Pacífico" (8.7783°, -144.8885°)
4. Verificar que el agua se vea uniforme (solo azul oscuro con shader realista)
5. NO debe haber dos colores mezclados

## BUILD

```bash
cd viewer3d
npm run build
```

Build exitoso: 266 kB First Load JS

## PRÓXIMOS PASOS

- Probar en otros océanos (Atlántico, Índico, Pacífico occidental)
- Verificar que la vegetación NO aparezca sobre océano (ya implementado)
- Considerar agregar más detalles al shader de agua (espuma en costas, etc.)
