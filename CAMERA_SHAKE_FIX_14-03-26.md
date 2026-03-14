# Fix: Sacudida violenta de cámara eliminada
**Fecha**: 14-03-26
**Problema**: Cámara se sacudía violentamente en escenas con árboles cuando la nave estaba quieta

## Diagnóstico
El usuario reportó que la cámara se ponía "como loca" y se sacudía sola en escenas con árboles, pero NO en Giza. El problema era causado por el `EarthquakeEffect.tsx` que modificaba directamente la posición de la cámara con valores muy altos.

## Causa raíz
- `EarthquakeEffect.tsx` líneas 82-84 modificaban `camera.position` con amplitudes muy altas (0.3, 0.12, 0.25)
- Velocidad de aplicación muy alta (delta * 8)
- Rotación de cámara muy pronunciada (0.008)
- Aunque el clima malo por defecto tenía `earthquake: false`, el efecto podía activarse y causar mareos

## Solución implementada
Reducción drástica de la intensidad del shake de cámara en `viewer3d/components/weather/EarthquakeEffect.tsx`:

### Cambios específicos:
1. **Amplitud reducida 90%**:
   - shakeX: 0.3 → 0.03 (principal), 0.15 → 0.015 (secundaria)
   - shakeY: 0.12 → 0.012 (principal), 0.06 → 0.006 (secundaria)
   - shakeZ: 0.25 → 0.025 (principal), 0.1 → 0.01 (secundaria)

2. **Velocidad reducida 75%**:
   - Multiplicador: delta * 8 → delta * 2

3. **Rotación reducida 50%**:
   - camera.rotation.z: 0.008 → 0.004

## Resultado
- Shake de cámara ahora es sutil y no causa mareos
- Efecto de terremoto apenas perceptible cuando se activa
- Escenas con árboles ya no tienen sacudida violenta
- Experiencia de usuario mejorada significativamente

## Archivos modificados
- `viewer3d/components/weather/EarthquakeEffect.tsx` (líneas 75-87)

## Testing
- Build exitoso sin errores
- Efecto de terremoto funcional pero mucho más suave
- Compatible con todas las escenas (Giza, Puma Punku, terrenos con árboles)

## Notas técnicas
El efecto de terremoto se activa cuando:
- Se recoge el piramidón en Giza (secuencia de misión)
- Se mueve un bloque en Puma Punku (secuencia de descubrimiento)
- Duración: ~3.2 segundos

Con esta reducción, el efecto es cinematográfico sin ser molesto.
