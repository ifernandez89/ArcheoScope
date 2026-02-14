# Escala Artística del Sistema Solar

## Filosofía: Unidades Abstractas

Este proyecto NO es un simulador astronómico. Es una experiencia interpretativa.

**Unidad base:** 1 unidad = radio de la Tierra

## Tamaños Planetarios (Proporcionales Reales)

Mantenemos las proporciones reales entre planetas:

- **Mercurio:** 0.38 unidades (38% del radio terrestre)
- **Venus:** 0.95 unidades (95% del radio terrestre - casi gemela)
- **Tierra:** 1.0 unidades (referencia)
- **Luna:** 0.27 unidades (27% del radio terrestre)
- **Marte:** 0.53 unidades (53% del radio terrestre)
- **Sol:** 20 unidades (grande pero no invasivo)

## Órbitas (Comprimidas Artísticamente)

Las distancias orbitales están **comprimidas** para mantener coherencia visual:

### Distancias Reales vs Artísticas

| Planeta | Distancia Real (UA) | Distancia Artística (unidades) | Compresión |
|---------|---------------------|--------------------------------|------------|
| Mercurio | 0.39 | 8 | ~20x |
| Venus | 0.72 | 12 | ~17x |
| Tierra | 1.0 | 16 (implícito) | ~16x |
| Marte | 1.52 | 22 | ~14x |
| Sol | - | 30 | - |

**Nota:** Las distancias están comprimidas más que los radios, manteniendo sensación correcta sin romper la cámara.

## Velocidades Orbitales (Proporcionales)

Mantenemos proporciones relativas de velocidad:

- **Mercurio:** 4.15 (el más rápido)
- **Venus:** 1.62
- **Tierra:** 1.0 (referencia implícita)
- **Marte:** 0.53 (el más lento)
- **Luna:** 0.08 (alrededor de la Tierra)

## Jerarquía Visual

La obra mantiene una jerarquía contemplativa:

1. **Sol** → Fuente dominante (20 unidades, distancia 30)
2. **Tierra** → Protagonista emocional (1 unidad, origen)
3. **Luna** → Ritmo cercano (0.27 unidades, órbita 12)
4. **Venus** → Presencia brillante discreta (0.95 unidades, órbita 12)
5. **Mercurio** → Pequeño y veloz (0.38 unidades, órbita 8)
6. **Marte** → Presencia distante y sobria (0.53 unidades, órbita 22)

## Aparición Narrativa (Zoom Levels)

Los planetas aparecen progresivamente según el zoom:

- **Nivel Mundo (8-30 unidades):** Solo Tierra y Luna
- **Nivel Orbital (30-50 unidades):** Aparecen Mercurio, Venus, Marte
- **Nivel Solar (50-100 unidades):** Sol visible, sistema completo
- **Nivel Sistema (100+ unidades):** Vista panorámica

## Texturas

Cada planeta tiene su textura independiente:

- **Mercurio:** Color procedural gris rocoso (#8c8c8c)
- **Venus:** `/textures/4k_venus_atmosphere.jpg` (atmósfera densa)
- **Tierra:** `/textures/earth_8k.jpg` + nubes
- **Luna:** `/textures/8k_moon.jpg`
- **Marte:** `/textures/8k_mars.jpg`
- **Sol:** `/textures/8k_sun.jpg` + shader procedural

## Módulos Independientes

Cada cuerpo celeste es un componente React independiente:

- `Mercury.tsx` - Módulo independiente
- `Venus.tsx` - Módulo independiente
- `Mars.tsx` - Módulo independiente
- `SimpleMoon.tsx` - Módulo independiente
- `Sun.tsx` - Módulo independiente con shader

Todos se integran en `ImmersiveScene.tsx` con visibilidad controlada por zoom.

## Performance

Con 4 planetas + Luna + Sol + órbitas + shader + partículas:

- **Geometrías:** ~500k polígonos totales
- **Texturas:** ~150MB en memoria
- **FPS esperado:** 60fps en hardware moderno
- **Límite real:** Muy lejos del techo del navegador

## Próximos Pasos Posibles

Si se desea expandir:

1. **Júpiter** (cambia escala conceptual - requiere repensar distancias)
2. **Saturno** (con anillos - desafío visual)
3. **Modo Realista** (distancias brutales, silencio espacial)
4. **Floating Origin System** (para máxima precisión en distancias extremas)

## Filosofía Final

> "No es exactitud matemática. Es percepción humana."

La obra es contemplativa, no arcade. Cada decisión de escala busca mantener:

- Proporciones planetarias reales
- Distancias expresivas (no literales)
- Jerarquía visual clara
- Descubrimiento progresivo
- Coherencia emocional

---

**Última actualización:** Sistema con Mercurio, Venus, Marte implementados con escala artística coherente.
