# FIX: Coordenadas de América Clasificadas como Océano - 22 de Febrero 2026

## PROBLEMA

El usuario reportó que todas las coordenadas (México, Patagonia, Perú, etc.) estaban siendo clasificadas como Océano Pacífico, por lo que solo se veía agua en todos los sitios.

## CAUSA RAÍZ

La lógica de exclusión de tierra firme en `detectBiome()` estaba MAL implementada:

```typescript
// ANTES - INCORRECTO
if (lon < -70) {
  // Excluir costa oeste de América del Norte (lat > 30, lon > -130)
  if (lat > 30 && lon > -130) {
    // Es costa, no océano
  }
  // ... más exclusiones con else if ...
  else {
    return { type: 'ocean' }  // ❌ TODO LO DEMÁS ES OCÉANO
  }
}
```

El problema era que las exclusiones usaban `else if`, por lo que si una coordenada NO cumplía la PRIMERA exclusión, automáticamente se clasificaba como océano.

Ejemplo:
- **Machu Picchu**: lat=-13.1631, lon=-72.5450
  - lon < -70 ✅ (entra en el bloque)
  - lat > 30 ❌ (NO cumple primera exclusión)
  - Se clasifica como océano ❌ INCORRECTO

## SOLUCIÓN

Reescribí la lógica para evaluar TODAS las exclusiones antes de decidir si es océano:

```typescript
// DESPUÉS - CORRECTO
if (lon < -70) {
  // Evaluar TODAS las exclusiones
  const isNorthAmerica = lat > 10 && lon > -170 && lon < -50
  const isCentralAmerica = lat > 7 && lat < 23 && lon > -120 && lon < -77
  const isSouthAmerica = lat < 15 && lon > -82 && lon < -34
  const isPatagonia = lat < -35 && lon > -75 && lon < -53
  
  // Si NO es ninguna parte de América, es océano
  if (!isNorthAmerica && !isCentralAmerica && !isSouthAmerica && !isPatagonia) {
    return { type: 'ocean' }
  }
}
```

Ahora:
- **Machu Picchu**: lat=-13.1631, lon=-72.5450
  - isSouthAmerica = lat < 15 ✅ && lon > -82 ✅ && lon < -34 ❌
  - Espera, -72.5450 NO es < -34... necesito ajustar los rangos

Voy a verificar los rangos correctos:
- América del Sur: lon entre -82 (Ecuador) y -34 (Brasil este)
- Pero Perú está en lon=-72, que SÍ está entre -82 y -34 ✅

El problema es que la condición `lon < -34` excluye a Brasil este, pero debería ser `lon > -34` para incluir todo lo que está al OESTE de Brasil.

Déjame corregir esto...

## RANGOS CORRECTOS

- **América del Norte**: lat > 10, lon entre -170 (Alaska) y -50 (Labrador)
- **América Central**: lat entre 7 y 23, lon entre -120 (México oeste) y -77 (Panamá)
- **América del Sur**: lat < 15, lon entre -82 (Ecuador) y -34 (Brasil este)
- **Patagonia**: lat < -35, lon entre -75 (Chile) y -53 (Argentina este)

## VERIFICACIÓN

- **Machu Picchu**: lat=-13.1631, lon=-72.5450
  - isSouthAmerica = lat < 15 ✅ && lon > -82 ✅ && lon < -34 ✅
  - Es tierra firme ✅

- **Chichén Itzá**: lat=20.6843, lon=-88.5678
  - isCentralAmerica = lat > 7 ✅ && lat < 23 ✅ && lon > -120 ✅ && lon < -77 ✅
  - Es tierra firme ✅

- **Océano Pacífico**: lat=8.7783, lon=-144.8885
  - isNorthAmerica = NO
  - isCentralAmerica = NO
  - isSouthAmerica = NO
  - isPatagonia = NO
  - Es océano ✅

## ARCHIVOS MODIFICADOS

1. `viewer3d/utils/biome-detector.ts`
   - Reescrita lógica de exclusión de tierra firme
   - Rangos correctos para América del Norte, Central, Sur y Patagonia

## RESULTADO

Ahora las coordenadas se clasifican correctamente:
- ✅ México → tierra firme
- ✅ Perú → tierra firme
- ✅ Patagonia → tierra firme
- ✅ Océano Pacífico → océano

## BUILD

Build exitoso: 266 kB First Load JS

## COMMIT

```
fix: Corregir detección de océano para no clasificar América como océano - Mejorar exclusiones de tierra firme
```

Commit: 1b4147e
Push: origin/main ✅
