# Sistema de Sol Visible Astronómico
**Fecha**: 14-03-26
**Feature**: Nueva opción "Sol Visible" en el sistema climático

## Descripción
Implementado un sol visible en el cielo que sigue la posición astronómica real, permitiendo estimar la hora del día mediante la brújula y la posición del sol.

## Características implementadas

### 1. Sol visible astronómicamente preciso
- **Posición real**: El sol se posiciona según `solarDirection` calculado astronómicamente
- **Salida/Puesta**: Sale por el Este y se oculta por el Oeste
- **Altura variable**: Cambia de posición según la hora del día y ubicación geográfica

### 2. Iluminación coherente
- **Luz direccional**: La luz proviene directamente desde la posición del sol
- **Sombras precisas**: Las sombras de los objetos coinciden con la posición solar
- **Intensidad dinámica**: Varía según la altura del sol (más intensa al mediodía)

### 3. Efectos visuales realistas
- **Color dinámico**:
  - Amanecer/Atardecer (y < 0.1): Naranja rojizo (#ff6b35)
  - Mañana/Tarde (y < 0.3): Amarillo dorado (#ffaa33)
  - Mediodía (y >= 0.3): Amarillo brillante (#fff8e7)

- **Tamaño aparente**:
  - Horizonte: 25 unidades (ilusión óptica)
  - Alto en el cielo: 20 unidades

- **Efectos atmosféricos**:
  - Núcleo brillante con opacidad 0.95
  - Glow exterior con blending aditivo
  - Corona difusa para atmósfera
  - Pulsación sutil (respiración)

### 4. Integración con sistema climático
- Nueva opción en WeatherControl: "☀️ Sol Visible"
- Se activa/desactiva desde el panel de clima
- Compatible con otros efectos climáticos
- Clima despejado (CALM_WEATHER) tiene sol visible por defecto

## Archivos creados
- `viewer3d/components/weather/VisibleSun.tsx` - Componente del sol visible

## Archivos modificados
- `viewer3d/components/WeatherControl.tsx` - Agregada opción `visibleSun`
- `viewer3d/components/systems/WeatherSystem.tsx` - Integración del VisibleSun
- `viewer3d/components/ImmersiveScene.tsx` - Actualización de constantes de clima

## Uso práctico

### Estimar hora del día
1. Activar "Sol Visible" en el panel de clima
2. Observar la posición del sol en el cielo
3. Usar la brújula para determinar dirección
4. Combinar ambos datos:
   - Sol en el Este + bajo: Amanecer (~6am)
   - Sol en el Sur + alto: Mediodía (~12pm)
   - Sol en el Oeste + bajo: Atardecer (~6pm)

### Verificar sombras
- Las sombras de objetos apuntan en dirección opuesta al sol
- Longitud de sombras varía con altura solar:
  - Sombras largas: Amanecer/Atardecer
  - Sombras cortas: Mediodía

## Parámetros configurables
```typescript
<VisibleSun 
  solarDirection={solarDirection}  // Dirección astronómica
  intensity={3.0}                  // Intensidad de luz
  distance={500}                   // Distancia aparente
/>
```

## Notas técnicas
- El sol solo se renderiza si está sobre el horizonte (y > -0.1)
- La luz direccional tiene sombras de alta calidad (2048x2048)
- Shadow camera configurada para cubrir 200x200 unidades
- Luz ambiental adicional para iluminación suave (30% de intensidad)

## Testing
- Build exitoso sin errores
- Compatible con todos los biomas
- Funciona correctamente con sistema astronómico
- Sombras alineadas con posición solar

## Beneficios
✅ Navegación mejorada (orientación por el sol)
✅ Estimación de hora del día sin UI
✅ Inmersión realista
✅ Educativo (movimiento solar real)
✅ Sombras coherentes con física real
