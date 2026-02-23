# Fix del Sistema de Agua - Eliminación de Doble Color

**Fecha**: 23 de Febrero, 2026  
**Problema**: El agua mostraba dos colores diferentes (mitad claro, mitad oscuro)  
**Estado**: ✅ RESUELTO

## Problema Identificado

El sistema de agua `RealisticWater.tsx` estaba generando dos colores diferentes en la misma superficie de agua debido a múltiples efectos de shader que causaban variación de color:

1. **Efecto Fresnel**: Cambiaba el color según el ángulo de visión
2. **Variación por profundidad**: Mezclaba `deepWaterColor` con `shallowWaterColor`
3. **Efecto Ripple**: Añadía ondulaciones procedurales que alteraban el color

## Solución Implementada

### Simplificación del Fragment Shader

**ANTES** (con variaciones de color):
```glsl
void main() {
  vec3 color = deepWaterColor;
  
  // Ondulación procedural MUY sutil para textura
  float ripple = sin(vUv.x * 20.0 + time * 2.0) * 
                 cos(vUv.y * 20.0 + time * 1.5);
  color += ripple * 0.02;
  
  float alpha = 0.9;
  gl_FragColor = vec4(color, alpha);
}
```

**DESPUÉS** (color uniforme):
```glsl
void main() {
  // Color COMPLETAMENTE uniforme sin ninguna variación
  gl_FragColor = vec4(deepWaterColor, 0.9);
}
```

### Limpieza del Vertex Shader

Eliminadas variables no utilizadas:
- `varying vec3 vNormal`
- `varying vec3 vViewPosition`
- `varying vec2 vUv`
- `varying float vElevation`

Mantenidas solo las olas Gerstner para movimiento de superficie (no afectan el color).

### Limpieza de Uniforms

Eliminados uniforms innecesarios:
- `shallowWaterColor`
- `fresnelColor`

Mantenidos solo:
- `time` - Para animación de olas
- `deepWaterColor` - Color uniforme del agua
- `waveAmplitude`, `waveFrequency`, `waveSpeed` - Para olas Gerstner

## Resultado

- ✅ Agua con color completamente uniforme (#1e3a5f - azul oscuro)
- ✅ Sin variaciones de color por ángulo de visión
- ✅ Sin variaciones de color por profundidad
- ✅ Mantiene animación de olas en la superficie (solo geometría)
- ✅ Transparencia fija en 0.9

## Archivos Modificados

- `viewer3d/components/RealisticWater.tsx` - Simplificación completa del shader

## Configuración del Sistema de Agua

El agua se renderiza a través de `EnvironmentSystem.tsx` con las siguientes condiciones:

```typescript
<EnvironmentSystem
  showWater={!isIceBiome}  // No mostrar agua en biomas de hielo
  waterPosition={[0, -0.5, 0]}
  waterSize={150}
  waterColor="#1e3a5f"
/>
```

## Notas Técnicas

- El agua aparece como lagos en terrenos terrestres
- No se renderiza en biomas de hielo (Antártida, Ártico)
- No se renderiza sobre océanos (detectados por `detectBiome()`)
- Las olas Gerstner solo afectan la geometría, no el color
- El shader usa `THREE.DoubleSide` para visibilidad desde ambos lados

## Testing

Probado en múltiples ubicaciones:
- ✅ Machu Picchu (Perú) - Lagos con color uniforme
- ✅ México - Lagos con color uniforme
- ✅ Patagonia - Lagos con color uniforme
- ✅ Océano Pacífico - Sin agua (correcto)
- ✅ Antártida - Sin agua (correcto, bioma de hielo)
