# Corrección de Proporciones - Escena de Teotihuacán
**Fecha**: 18 de marzo de 2026

## Cambios Realizados

### 1. Ajuste de Escalas Realistas

Se corrigieron las escalas de los templos para reflejar las proporciones históricas reales:

**Templo de Kukulkán (Chichén Itzá)**:
- Altura real: 30 metros
- Base real: 55 x 55 metros
- Escala en juego: `0.3`
- Características únicas:
  - Precisión astronómica: 91 escalones × 4 lados + 1 = 365 días
  - Fenómeno de equinoccio: sombra de serpiente descendiendo
  - Representa a Kukulkán, la serpiente emplumada

**Templo Mayor Azteca (Tenochtitlán)**:
- Altura real: 60 metros (el doble que Kukulkán)
- Base real: 80 metros
- Escala en juego: `0.26`
- Características:
  - Doble templo ritual dedicado a Tláloc y Huitzilopochtli
  - Centro ceremonial de Tenochtitlán

**Calendario Maya**:
- Posición ajustada: Y=10 (sobre la punta de Kukulkán)
- Escala: 1.5

### 2. Comparación de Dimensiones

| Estructura | Altura Real | Base Real | Escala | Función |
|------------|-------------|-----------|--------|---------|
| Kukulkán (maya) | 30m | 55x55m | 0.3 | Astronómica/Calendario |
| Templo Mayor (azteca) | 60m | 80m | 0.26 | Ritual/Política |
| Pirámide del Sol | 65m | 225m | N/A | Monumental |

### 3. Corrección de next.config.js

Se corrigió el `assetPrefix` para evitar barras duplicadas en las rutas de GitHub Pages:

```javascript
// ANTES
assetPrefix: isProd ? '/ArcheoScope/' : '',

// DESPUÉS
assetPrefix: isProd ? '/ArcheoScope' : '',
```

Esto asegura que las rutas de los modelos 3D se generen correctamente:
- Desarrollo: `/moai.glb`
- Producción: `/ArcheoScope/moai.glb`

## Archivos Modificados

1. `viewer3d/components/TeotihuacanScene.tsx`
   - Escala de Kukulkán: 0.15 → 0.3
   - Escala de Templo Mayor: 0.13 → 0.26
   - Posición del Calendario: Y=6 → Y=10
   - Documentación actualizada con proporciones reales

2. `viewer3d/next.config.js`
   - Corrección de `assetPrefix` para GitHub Pages

## Verificación

✅ Build exitoso sin errores
✅ Modelos presentes en `viewer3d/out/`:
  - moai.glb
  - atlante.glb
  - kukulkan.glb
  - aztec_temple.glb
  - calendario_maya.glb
  - quetzalcoatl.glb

## Relación de Tamaños

La escena ahora refleja correctamente que:
- El Templo Mayor es aproximadamente el doble de alto que Kukulkán (60m vs 30m)
- Kukulkán mantiene su escala astronómica precisa
- El Calendario Maya flota sobre la punta de Kukulkán a la altura correcta

## Próximos Pasos

- [ ] Implementar diálogo de Quetzalcoatl (similar a Viracocha)
- [ ] Completar sistema de misión de Teotihuacán
- [ ] Agregar efectos visuales para el fenómeno de equinoccio
